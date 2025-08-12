"""
CLI
Checklist:
1. Parse command-line arguements and subcommands.
2. Implement init, scan, and update commands.
3. Use manifest and diff utilities functions
4. Exit with appropriate status codes.
5. Handle errors and print usage information.
"""

#!/usr/bin/env python3
import sys
from pathlib import Path
import argparse
from src.manifest import build_manifest, load_manifest, save_manifest
from src.diff_utils import diff_manifests, print_report

def parse_args():
    """Parse command-line arguments."""
    p = argparse.ArgumentParser(description="File Integrity Monitor")
    sub = p.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("root", type=Path, help="Directory to scan")
    common.add_argument("--db", type=Path, default=Path("baseline.json"), help="Path to baseline file")
    common.add_argument("--workers", type=int, default=4, help="Number of hashing worker threads")
    common.add_argument("--ignore-dirs", nargs="*", default=[".git", "__pycache__", ".venv"], help="Directories to ignore")
    sub.add_parser("init", parents=[common], help="Create baseline")
    sub.add_parser("scan", parents=[common], help="Scan and compare to baseline")
    sub.add_parser("update", parents=[common], help="Update baseline")
    return p.parse_args()

def cmd_init(args):
    """Create a new save and baseline manifest."""
    save_manifest(args.db, build_manifest(args.root, args.workers, set(args.ignore_dirs)))
    print(f"[ok] Baseline created: {args.db}")
    return 0

def cmd_scan(args):
    """Scan the directory and compare to the baseline."""
    old = load_manifest(args.db)
    new = build_manifest(args.root, args.workers, set(args.ignore_dirs))
    diff = diff_manifests(old, new)
    return print_report(diff)

def cmd_update(args):
    """Update the baseline with the current scan."""
    new = build_manifest(args.root, args.workers, set(args.ignore_dirs))
    save_manifest(args.db, new)
    print(f"[ok] Baseline updated: {args.db}")
    return 0

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    if args.cmd == "init":
        return cmd_init(args)
    if args.cmd == "scan":
        return cmd_scan(args)
    if args.cmd == "update":
        return cmd_update(args)

if __name__ == "__main__":
    sys.exit(main())
