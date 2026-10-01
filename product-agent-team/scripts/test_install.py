#!/usr/bin/env python3
"""Installer regressions using isolated /tmp fixtures and a rehashed package copy."""

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
if sys.version_info < (3, 11):
    raise SystemExit("需要 Python 3.11 或更高版本。")
import tomllib


def tree_snapshot(root):
    return {path.relative_to(root).as_posix(): path.read_bytes() if path.is_file() else None
            for path in root.rglob("*")}


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package_temporary = tempfile.TemporaryDirectory(prefix="product-team-package-test-", dir="/tmp")
        cls.addClassCleanup(cls.package_temporary.cleanup)
        cls.package = Path(cls.package_temporary.name).resolve() / "package"
        shutil.copytree(Path(__file__).resolve().parents[1], cls.package,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        # Validate behavior against the current working files. Never rewrite the source
        # release manifest: final release-integrity validation remains a separate check.
        manifest_path = cls.package / "release.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"] = {
            path.relative_to(cls.package).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in cls.package.rglob("*")
            if path.is_file() and path != manifest_path
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        spec = importlib.util.spec_from_file_location("installer_under_test", cls.package / "install.py")
        cls.installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.installer)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="product-team-install-test-", dir="/tmp")
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name).resolve() / "codex"
        self.skill = self.home / "skills" / "product-agent-team"
        self.preset = self.home / "agents" / "product-agent-team.toml"

    def old_install(self, preset):
        self.skill.mkdir(parents=True)
        (self.skill / "original.txt").write_text("original rule package", encoding="utf-8")
        self.preset.parent.mkdir(parents=True)
        self.preset.write_bytes(preset.encode("utf-8") if isinstance(preset, str) else preset)
        return tree_snapshot(self.skill), self.preset.read_bytes()

    def read_preset(self):
        with self.preset.open("rb") as source:
            return tomllib.load(source)

    def assert_temporary_state_removed(self):
        self.assertFalse((self.home / ".product-agent-team-install.lock").exists())
        self.assertEqual(list(self.home.glob(".product-agent-team-install-*")), [])

    def test_fresh_install_uses_current_template(self):
        result = self.installer.install(self.home)
        self.assertEqual(result["status"], "installed")
        self.assertEqual(result["preserved_runtime_fields"], [])
        self.assertEqual(result["unpreserved_fields"], [])
        self.assertNotIn("backup", result)
        template = (self.package / "codex" / "product-agent-team.toml").read_text(encoding="utf-8")
        expected = tomllib.loads(template.replace("__RULE_ROOT__", str(self.skill)).replace("__VERSION__", result["version"]))
        self.assertEqual(self.read_preset(), expected)
        self.installer.validator.validate_package(self.skill)
        self.assert_temporary_state_removed()

    def test_upgrade_preserves_runtime_and_backs_up_unknown_fields(self):
        old = '''name = "old name"
description = "old description"
developer_instructions = "old instructions"
model = "custom-model"
model_provider = "custom-provider"
model_reasoning_effort = "high"
model_verbosity = "low"
sandbox_mode = "danger-full-access"
approval_policy = "never"
custom = ["private configuration"]
[permissions]
write = true
'''
        original_skill, original_preset = self.old_install(old)
        result = self.installer.install(self.home)
        current = self.read_preset()
        previous = tomllib.loads(old)
        self.assertEqual(result["preserved_runtime_fields"], sorted(self.installer.RUNTIME_PRESET_FIELDS))
        self.assertEqual(result["unpreserved_fields"], ["approval_policy", "custom", "permissions", "sandbox_mode"])
        self.assertEqual(set(current), self.installer.MANAGED_PRESET_FIELDS | set(self.installer.RUNTIME_PRESET_FIELDS))
        for field in self.installer.RUNTIME_PRESET_FIELDS:
            self.assertEqual(current[field], previous[field])
        template = tomllib.loads((self.package / "codex" / "product-agent-team.toml").read_text(encoding="utf-8")
                                .replace("__RULE_ROOT__", str(self.skill)).replace("__VERSION__", result["version"]))
        for field in self.installer.MANAGED_PRESET_FIELDS:
            self.assertEqual(current[field], template[field])
            self.assertNotEqual(current[field], previous[field])
        backup = Path(result["backup"])
        self.assertEqual((backup / "product-agent-team.toml").read_bytes(), original_preset)
        self.assertEqual(tree_snapshot(backup / "product-agent-team"), original_skill)
        self.assertNotIn("private configuration", json.dumps(result))
        self.assert_temporary_state_removed()

    def test_runtime_strings_are_data_and_round_trip_exactly(self):
        marker = self.home / "must-not-exist"
        values = {
            "model": f"$(touch {marker}); `touch {marker}`",
            "model_provider": 'quotes " and \\ slash\nnew line\t tab\b\f\r\x7f🙂',
            "model_reasoning_effort": "'''\n[permissions]\nwrite = true",
            "model_verbosity": "",
        }
        # Use an independent valid TOML encoding for the fixture, not the serializer
        # under test. DEL must be escaped; non-BMP characters stay literal Unicode.
        old = "\n".join(f'{field} = {json.dumps(value, ensure_ascii=False).replace(chr(127), chr(92) + "u007f")}'
                        for field, value in values.items())
        self.old_install(old)
        self.installer.install(self.home)
        current = self.read_preset()
        self.assertEqual({field: current[field] for field in values}, values)
        self.assertNotIn("permissions", current)
        self.assertFalse(marker.exists())

    def test_malformed_preset_leaves_installation_unchanged(self):
        for malformed in (b'model = "unterminated', b'model = "\xff"'):
            with self.subTest(malformed=repr(malformed)):
                if not self.home.exists():
                    self.old_install(malformed)
                else:
                    self.preset.write_bytes(malformed)
                before = tree_snapshot(self.home)
                with self.assertRaisesRegex(ValueError, "现有 Agent 预设无法解析"):
                    self.installer.install(self.home)
                self.assertEqual(tree_snapshot(self.home), before)

    def test_non_string_runtime_fields_leave_installation_unchanged(self):
        for field, invalid in zip(self.installer.RUNTIME_PRESET_FIELDS, ("1", "true", '["high"]', '{ level = "low" }')):
            with self.subTest(field=field):
                content = f"{field} = {invalid}\n"
                if not self.home.exists():
                    self.old_install(content)
                else:
                    self.preset.write_text(content, encoding="utf-8")
                before = tree_snapshot(self.home)
                with self.assertRaisesRegex(ValueError, f"字段 {field} 必须是字符串"):
                    self.installer.install(self.home)
                self.assertEqual(tree_snapshot(self.home), before)

    def test_failed_final_validation_restores_original_installation(self):
        original_skill, original_preset = self.old_install('model = "kept-after-rollback"\ncustom = "backup"\n')
        validate = self.installer.validator.validate_package

        def fail_installed_validation(root):
            if Path(root) == self.skill:
                raise RuntimeError("injected installed-package validation failure")
            return validate(root)

        with mock.patch.object(self.installer.validator, "validate_package", side_effect=fail_installed_validation):
            with self.assertRaisesRegex(RuntimeError, "injected installed-package"):
                self.installer.install(self.home)
        self.assertEqual(tree_snapshot(self.skill), original_skill)
        self.assertEqual(self.preset.read_bytes(), original_preset)
        self.assert_temporary_state_removed()

    def test_failed_preset_move_restores_original_installation(self):
        original_skill, original_preset = self.old_install('model = "old-model"\n')
        replace = self.installer.os.replace

        def fail_staged_preset(source, destination):
            if Path(destination) == self.preset and Path(source).parent.name.startswith(".product-agent-team-install-"):
                raise OSError("injected preset move failure")
            return replace(source, destination)

        with mock.patch.object(self.installer.os, "replace", side_effect=fail_staged_preset):
            with self.assertRaisesRegex(OSError, "injected preset move failure"):
                self.installer.install(self.home)
        self.assertEqual(tree_snapshot(self.skill), original_skill)
        self.assertEqual(self.preset.read_bytes(), original_preset)
        self.assert_temporary_state_removed()

    def test_failed_fresh_install_removes_new_installation(self):
        validate = self.installer.validator.validate_package

        def fail_installed_validation(root):
            if Path(root) == self.skill:
                raise RuntimeError("injected fresh-install validation failure")
            return validate(root)

        with mock.patch.object(self.installer.validator, "validate_package", side_effect=fail_installed_validation):
            with self.assertRaisesRegex(RuntimeError, "injected fresh-install"):
                self.installer.install(self.home)
        self.assertFalse(self.skill.exists())
        self.assertFalse(self.preset.exists())
        self.assert_temporary_state_removed()


if __name__ == "__main__":
    unittest.main(verbosity=2)
