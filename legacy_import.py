"""
Legacy Consolidation & Batch Importer Script for SecondSelf (Phase 0.5).
Imports existing notes, markdown files, and documents from a local directory into raw/
with automated deduplication and 'legacy-import' tagging.
"""

import sys
import argparse
from pathlib import Path
from typing import List

from capture import capture_file, capture_note


SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf", ".html", ".py", ".json", ".yaml", ".yml"}


def import_directory(target_dir: str) -> int:
    """Recursively scan target_dir and ingest supported document files into raw/."""
    dir_path = Path(target_dir).resolve()
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: Target directory '{target_dir}' does not exist or is not a directory.")
        return 0

    print(f"Scanning directory '{dir_path}' for legacy imports...")
    imported_count = 0

    for filepath in dir_path.rglob("*"):
        if filepath.is_file() and filepath.suffix.lower() in SUPPORTED_EXTENSIONS:
            # Avoid importing files inside raw/ or wiki/ or .git/
            parents_str = [str(p.name) for p in filepath.parents]
            if any(forbidden in parents_str for forbidden in ["raw", "wiki", "data", ".venv", ".git", "node_modules"]):
                continue

            print(f"Importing legacy document: {filepath.name}...")
            try:
                capture_file(str(filepath))
                imported_count += 1
            except Exception as e:
                print(f"Warning: Failed to import '{filepath.name}': {e}")

    print(f"Legacy import complete! Ingested {imported_count} documents into raw/.")
    return imported_count


def main():
    parser = argparse.ArgumentParser(description="SecondSelf Legacy Batch Importer")
    parser.add_argument("directory", type=str, help="Path to local folder containing legacy notes/docs")

    args = parser.parse_args()
    import_directory(args.directory)


if __name__ == "__main__":
    main()
