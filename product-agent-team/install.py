#!/usr/bin/env python3
"""Install this release's Skill and Codex Agent preset, preserving the old version."""

import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
if sys.version_info < (3, 11):
    raise SystemExit("需要 Python 3.11 或更高版本；请使用 python3.11+ 执行 install.py。")
import tomllib

PACKAGE_ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("product_team_validator", PACKAGE_ROOT / "scripts" / "validate_package.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

MANAGED_PRESET_FIELDS = frozenset({"name", "description", "developer_instructions"})
RUNTIME_PRESET_FIELDS = ("model", "model_provider", "model_reasoning_effort", "model_verbosity")


def require_directory_or_missing(path):
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise ValueError(f"安装路径必须是普通目录：{path}")


def read_runtime_options(preset_path):
    """Migrate only known string runtime options; leave other fields in the backup."""
    if not preset_path.exists():
        return {}, []
    try:
        with preset_path.open("rb") as source:
            previous = tomllib.load(source)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as error:
        # Do not include parser messages, which can contain old configuration values.
        raise ValueError("现有 Agent 预设无法解析；未替换原安装") from error
    runtime = {}
    for field in RUNTIME_PRESET_FIELDS:
        if field in previous:
            if not isinstance(previous[field], str):
                raise ValueError(f"现有 Agent 预设字段 {field} 必须是字符串；未替换原安装")
            runtime[field] = previous[field]
    unpreserved = sorted(set(previous) - MANAGED_PRESET_FIELDS - set(runtime))
    return runtime, unpreserved


def toml_string(value):
    # JSON string escaping also works for TOML basic strings, with DEL escaped too.
    # Keep Unicode literal so astral characters do not become invalid surrogate escapes.
    return json.dumps(value, ensure_ascii=False).replace("\x7f", "\\u007f")


def install(codex_home):
    # Validate before creating the target home or acquiring an installation lock.
    validator.validate_package(PACKAGE_ROOT)
    codex_home = codex_home.expanduser().resolve()
    if codex_home.is_relative_to(PACKAGE_ROOT.resolve()):
        raise ValueError("Codex 安装目录不能位于发布包内部，请选择独立目录")
    skills = codex_home / "skills"
    agents = codex_home / "agents"
    backups = codex_home / "backups" / "product-agent-team"
    target_skill = skills / "product-agent-team"
    target_preset = agents / "product-agent-team.toml"
    for path in (codex_home, skills, agents, codex_home / "backups", backups, target_skill):
        require_directory_or_missing(path)
    if target_preset.is_symlink() or (target_preset.exists() and not target_preset.is_file()):
        raise ValueError(f"Agent 预设必须是普通文件：{target_preset}")
    codex_home.mkdir(parents=True, exist_ok=True)
    lock = codex_home / ".product-agent-team-install.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError(f"安装锁已存在，请确认没有其他安装进程：{lock}")
    os.close(descriptor)
    staging = None
    backup = None
    moved_skill = moved_preset = installed_skill = installed_preset = False
    cleanup_staging = True
    try:
        # Parse and check all migratable fields before staging or moving the old install.
        runtime, unpreserved = read_runtime_options(target_preset)
        staging = Path(tempfile.mkdtemp(prefix=".product-agent-team-install-", dir=codex_home))
        staged_skill = staging / "package"
        shutil.copytree(PACKAGE_ROOT, staged_skill, symlinks=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        manifest = validator.validate_package(staged_skill)
        template = (staged_skill / "codex" / "product-agent-team.toml").read_text(encoding="utf-8")
        rendered = template.replace("__RULE_ROOT__", str(target_skill)).replace("__VERSION__", manifest["version"])
        if runtime:
            # Keep these assignments at the TOML root, even if a later template has tables.
            rendered = "\n".join(f"{field} = {toml_string(value)}" for field, value in runtime.items()) + "\n\n" + rendered
        parsed = tomllib.loads(rendered)
        if "__RULE_ROOT__" in parsed["developer_instructions"] or str(target_skill) not in parsed["developer_instructions"]:
            raise ValueError("Agent 预设未正确引用安装目录")
        staged_preset = staging / "product-agent-team.toml"
        staged_preset.write_text(rendered, encoding="utf-8")
        skills.mkdir(exist_ok=True)
        agents.mkdir(exist_ok=True)
        if target_skill.exists() or target_preset.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = backups / f"{stamp}-{uuid.uuid4().hex[:8]}"
            backup.mkdir(parents=True)
        if target_skill.exists():
            os.replace(target_skill, backup / "product-agent-team")
            moved_skill = True
        if target_preset.exists():
            os.replace(target_preset, backup / "product-agent-team.toml")
            moved_preset = True
        os.replace(staged_skill, target_skill)
        installed_skill = True
        os.replace(staged_preset, target_preset)
        installed_preset = True
        validator.validate_package(target_skill)
        if target_preset.read_text(encoding="utf-8") != rendered:
            raise ValueError("安装后的 Agent 预设与目标版本不一致")
        result = {"status": "installed", "version": manifest["version"], "skill_root": str(target_skill), "agent_preset": str(target_preset),
                  "preserved_runtime_fields": sorted(runtime), "unpreserved_fields": unpreserved}
        if backup is not None:
            result["backup"] = str(backup)
        return result
    except BaseException as original_error:
        rollback_errors = []
        # Move the newly copied release aside before restoring the original files.
        operations = []
        if installed_preset:
            operations.append((target_preset, staging / "failed-preset.toml"))
        if installed_skill:
            operations.append((target_skill, staging / "failed-package"))
        if moved_skill:
            operations.append((backup / "product-agent-team", target_skill))
        if moved_preset:
            operations.append((backup / "product-agent-team.toml", target_preset))
        for source, destination in operations:
            try:
                os.replace(source, destination)
            except OSError as error:
                rollback_errors.append(str(error))
        if rollback_errors:
            cleanup_staging = False
            raise RuntimeError(f"安装失败：{original_error}；自动回滚未完全成功：{rollback_errors}；保留暂存 {staging} 和备份 {backup}") from original_error
        raise
    finally:
        if cleanup_staging and staging is not None:
            shutil.rmtree(staging, ignore_errors=True)
        lock.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME") or "~/.codex"), help="Codex 目录，默认 CODEX_HOME 或 ~/.codex")
    parser.add_argument("--check", action="store_true", help="仅校验包，不修改 Codex 安装")
    args = parser.parse_args()
    try:
        if args.check:
            manifest = validator.validate_package(PACKAGE_ROOT)
            result = {"status": "valid", "version": manifest["version"], "files": len(manifest["files"]), "skills": len(manifest["skills"])}
        else:
            result = install(args.codex_home)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"操作失败：{error}\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
