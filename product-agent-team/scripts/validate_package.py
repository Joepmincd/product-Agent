#!/usr/bin/env python3
"""Validate the distributable product-agent-team package without modifying it."""

import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
try:
    import tomllib
except ImportError:
    raise SystemExit("需要 Python 3.11 或更高版本（标准库 tomllib）；请使用 python3.11+ 执行。")


class PackageError(ValueError):
    """The package is incomplete, unsafe, or differs from its manifest."""


def relative_path(value, *, allow_root=False):
    if not isinstance(value, str) or not value or "\\" in value:
        raise PackageError(f"无效相对路径：{value!r}")
    if allow_root and value == ".":
        return Path(".")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        raise PackageError(f"路径必须是规范的包内相对路径：{value!r}")
    return Path(*path.parts)


def ignored(path):
    return "__pycache__" in path.parts or path.name == ".DS_Store" or path.suffix == ".pyc"


def package_files(root):
    found = {}
    # Do not follow symlinks, including links inside ignored cache directories.
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in directory.iterdir():
            mode = child.lstat().st_mode
            relative = child.relative_to(root)
            if stat.S_ISLNK(mode):
                raise PackageError(f"包内不允许符号链接：{relative}")
            if stat.S_ISDIR(mode):
                pending.append(child)
            elif stat.S_ISREG(mode):
                if relative.as_posix() != "release.json" and not ignored(relative):
                    found[relative.as_posix()] = child
            else:
                raise PackageError(f"包内只允许普通文件和目录：{relative}")
    return found


def frontmatter_name(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise PackageError(f"SKILL.md 缺少 YAML frontmatter：{path}")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise PackageError(f"SKILL.md frontmatter 未关闭：{path}")
    matches = [re.fullmatch(r"name:\s*([a-z0-9-]+|\"[a-z0-9-]+\"|'[a-z0-9-]+')\s*", line) for line in lines[1:end]]
    names = [match.group(1).strip("\"'") for match in matches if match]
    if len(names) != 1:
        raise PackageError(f"SKILL.md 需要唯一、合法的 name：{path}")
    return names[0]


def validate_package(root):
    root = Path(root).expanduser().absolute()
    if root.is_symlink() or not root.is_dir():
        raise PackageError(f"包根目录不存在或是符号链接：{root}")
    manifest_path = root / "release.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise PackageError("缺少普通文件 release.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise PackageError("release.json 必须是对象")
    if not isinstance(manifest.get("version"), str) or not manifest["version"].strip():
        raise PackageError("release.json 缺少有效 version")
    registered = manifest.get("skills")
    expected = manifest.get("files")
    if not isinstance(registered, dict) or not registered:
        raise PackageError("release.json 的 skills 必须是非空对象")
    if not isinstance(expected, dict) or not expected:
        raise PackageError("release.json 的 files 必须是非空对象")
    for name, digest in expected.items():
        relative_path(name)
        if not isinstance(digest, str) or re.fullmatch(r"[a-f0-9]{64}", digest) is None:
            raise PackageError(f"无效 SHA256：{name}")
    actual = package_files(root)
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    if missing or unexpected:
        raise PackageError(f"文件集合与 manifest 不一致；缺少：{missing}；额外：{unexpected}")
    for name, path in actual.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected[name]:
            raise PackageError(f"文件 SHA256 不匹配：{name}")
    if registered.get("product-agent-team") != ".":
        raise PackageError("skills 必须注册 product-agent-team: .")
    skill_files = set()
    for name, directory in registered.items():
        if not isinstance(name, str) or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is None:
            raise PackageError(f"无效 Skill 名称：{name!r}")
        relative = relative_path(directory, allow_root=True)
        if directory != "." and relative.name != name:
            raise PackageError(f"Skill 名称必须与目录名一致：{name}: {directory}")
        file_name = (relative / "SKILL.md").as_posix()
        if file_name in skill_files or file_name not in actual:
            raise PackageError(f"Skill 路径重复或缺失：{name}: {file_name}")
        if frontmatter_name(actual[file_name]) != name:
            raise PackageError(f"Skill frontmatter 与注册名称不一致：{name}")
        skill_files.add(file_name)
    discovered = {name for name in actual if PurePosixPath(name).name == "SKILL.md"}
    if discovered != skill_files:
        raise PackageError(f"存在未注册的 SKILL.md：{sorted(discovered - skill_files)}")
    preset_name = "codex/product-agent-team.toml"
    if preset_name not in actual:
        raise PackageError(f"缺少预设模板：{preset_name}")
    preset = tomllib.loads(actual[preset_name].read_text(encoding="utf-8"))
    instructions = preset.get("developer_instructions")
    if preset.get("name") != "product-agent-team" or not isinstance(instructions, str):
        raise PackageError("Agent 预设 name 或 developer_instructions 不合法")
    if "__RULE_ROOT__" not in instructions:
        raise PackageError("Agent 预设缺少 __RULE_ROOT__ 占位符")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        manifest = validate_package(args.root)
    except (PackageError, OSError, ValueError) as error:
        parser.exit(1, f"校验失败：{error}\n")
    print(json.dumps({"status": "valid", "version": manifest["version"], "files": len(manifest["files"]), "skills": len(manifest["skills"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
