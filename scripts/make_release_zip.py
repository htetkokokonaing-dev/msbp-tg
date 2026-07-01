#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT.parent / f"{ROOT.name}.zip"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
}
EXCLUDED_DIR_SUFFIXES = (".egg-info",)
EXCLUDED_FILE_NAMES = {
    ".DS_Store",
    "Thumbs.db",
}
EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
}
# Guard against accidentally packaging local/private development artifacts.
EXCLUDED_NAME_FRAGMENTS = (
    "Private_Manuscript",
    "build_stage19_revision.py",
    "render_contact_sheet",
)

def should_include(path: Path, root: Path = ROOT) -> bool:
    """Return True when a path is safe to include in the public release zip."""
    rel = path.relative_to(root)
    if any(part in EXCLUDED_DIR_NAMES for part in rel.parts):
        return False
    if any(part.endswith(EXCLUDED_DIR_SUFFIXES) for part in rel.parts):
        return False
    if path.name in EXCLUDED_FILE_NAMES:
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    rel_posix = rel.as_posix()
    if any(fragment in rel_posix for fragment in EXCLUDED_NAME_FRAGMENTS):
        return False
    return path.is_file()

def make_release_zip(output: Path = DEFAULT_OUT, root: Path = ROOT) -> Path:
    """Create a deterministic public-safe release zip for this repository."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if should_include(path, root=root):
                # Keep the top-level repository folder inside the archive.
                zf.write(path, path.relative_to(root.parent))
    return output

def main() -> None:
    parser = argparse.ArgumentParser(description="Build a public-safe MSBP-Tg release zip.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output zip path")
    args = parser.parse_args()
    out = make_release_zip(Path(args.out))
    print(out)

if __name__ == "__main__":
    main()
