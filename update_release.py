#!/usr/bin/env python3
"""Update the release manifest after reviewing package changes."""

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "product-agent-team"
MANIFEST = ROOT / "release.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="New release version, for example 2026.10.01.1")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path == MANIFEST:
            continue
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or "__pycache__" in relative.parts or path.name == ".DS_Store" or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise SystemExit(f"Symlink is not allowed in the release: {relative}")
        files[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()

    manifest["version"] = args.version
    manifest["released"] = date.today().isoformat()
    manifest["files"] = files
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {MANIFEST}: {args.version}, {len(files)} files")


if __name__ == "__main__":
    main()
