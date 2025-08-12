"""
Manifest Management
This module handles the creation and management of file manifests.
Checklist:
1.Walk directory tree while ignoring specified directories.
2.Build a manifest mapping relative paths to Filerecord.
3.Load manifest from JSON file
4.Save manifest to JSON file
5.Increase hashing performance
"""
import os
import json
from pathlib import Path
from dataclasses import asdict
from typing import Set, Tuple
from .models import FileRecord, Manifest
from .hash_utils import sha256_file
import concurrent.futures as cf

def iter_files(root: Path, ignored_dirs: Set[str]):
    """Yield all file paths under root, excluding ignored directories."""
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
        for name in filenames:
            p = Path(dirpath) / name
            if p.is_file():
                yield p

def build_manifest(root: Path, workers: int, ignored_dirs: Set[str]) -> Manifest:
    """Build a manifest (map of file paths to metadata) for all files in root."""
    root = root.resolve()

    def one(p: Path) -> Tuple[str, FileRecord]:
        rel = str(p.relative_to(root)).replace('\\', '/')
        stat = p.stat()
        return rel, FileRecord(rel, stat.st_size, stat.st_mtime, sha256_file(p))

    files = list(iter_files(root, ignored_dirs))
    if workers <= 1:
        return dict(one(p) for p in files)
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(ex.map(one, files))
    
def load_manifest(db_path: Path) -> Manifest:
    """Load a manifest from a JSON file; return empty dict if it doesn't exist."""
    if not db_path.exists():
        return {}
    with db_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return {k: FileRecord(**v) for k, v in raw.items()}


def save_manifest(db_path: Path, manifest: Manifest) -> None:
    """Save a manifest to a JSON file."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with db_path.open("w", encoding="utf-8") as f:
        json.dump({k: asdict(v) for k, v in manifest.items()}, f, indent=2, sort_keys=True)