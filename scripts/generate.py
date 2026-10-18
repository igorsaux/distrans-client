#!/usr/bin/env python3
"""Regenerate the vendored client from openapi/openapi.yml.

The generator emits a full package; only its generated artifacts are copied into
``src/distrans_client`` (``api/``, ``models/``, ``client.py``, ``errors.py``,
``types.py``). Hand-written modules and ``__init__.py`` are never touched, and
``scripts/generate.py --check`` fails when the vendored artifacts are stale.
"""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "openapi" / "openapi.yml"
PACKAGE = ROOT / "src" / "distrans_client"
GENERATED_DIRS = ("api", "models")
GENERATED_FILES = ("client.py", "errors.py", "types.py")
DEFAULT_GENERATOR_VERSION = "0.29.1"


def generate(spec: Path, output: Path, version: str) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "uvx",
            f"openapi-python-client@{version}",
            "generate",
            "--path",
            str(spec),
            "--meta=none",
            "--output-path",
            str(output),
        ],
        check=True,
        cwd=ROOT,
    )


def patch_generated(root: Path) -> None:
    """Apply target workarounds for known generator output bugs."""
    for path in root.rglob("*.py"):
        text = path.read_text()
        if "Unset" not in text:
            continue
        match = re.search(r"^from (\.+)types import (.+)$", text, re.MULTILINE)
        if not match:
            continue
        names = [name.strip() for name in match.group(2).split(",")]
        if "Unset" in names:
            continue
        names.append("Unset")
        text = text[: match.start(2)] + ", ".join(names) + text[match.end(2) :]
        path.write_text(text)


def sync(source: Path, target: Path) -> None:
    for name in GENERATED_DIRS:
        destination = target / name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source / name, destination)
    for name in GENERATED_FILES:
        shutil.copy2(source / name, target / name)


def differences(left: Path, right: Path) -> list[str]:
    result: list[str] = []
    comparison = filecmp.dircmp(left, right)
    result.extend(str(left / name) for name in comparison.left_only)
    result.extend(str(right / name) for name in comparison.right_only)
    for name in comparison.diff_files:
        result.append(str(left / name))
    for name in comparison.subdirs:
        result.extend(differences(left / name, right / name))
    return result


def compare(generated: Path, target: Path) -> list[str]:
    result: list[str] = []
    for name in GENERATED_DIRS:
        result.extend(differences(target / name, generated / name))
    for name in GENERATED_FILES:
        if not filecmp.cmp(target / name, generated / name, shallow=False):
            result.append(str(target / name))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=SPEC)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--generator-version",
        default=DEFAULT_GENERATOR_VERSION,
        help="openapi-python-client version to run via uvx",
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / "generated"
        generate(args.spec, fresh, args.generator_version)
        patch_generated(fresh)
        if args.check:
            diff = compare(fresh, PACKAGE)
            if diff:
                print("generated client is out of date:", file=sys.stderr)
                for path in diff:
                    print(f"  {path}", file=sys.stderr)
                print("run scripts/generate.py", file=sys.stderr)
                return 1
            print("generated client is up to date")
            return 0
        sync(fresh, PACKAGE)

    print(f"synced generated artifacts into {PACKAGE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
