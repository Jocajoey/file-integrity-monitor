"""
Diff Utils
for comparing file records.
Checklist:
1. Compare old asnd new manifests.
2. Identify added, removed, modified, and unchanged files.
3. Print a formated report of differences.
4. Return status code based on differences.
"""

from .models import FileRecord, Diff, Manifest

def diff_manifests(old: Manifest, new: Manifest) -> Diff:
    """Compare two manifests and return the differences."""
    added = [new[k] for k in sorted(set(new.keys()) - set(old.keys()))]
    removed = [old[k] for k in sorted(set(old.keys()) - set(new.keys()))]
    modified, unchanged = [], []

    for k in sorted(set(old.keys()) & set(new.keys())):
        if old[k].sha256 != new[k].sha256:
            modified.append((old[k], new[k]))
        else:
            unchanged.append(new[k])

    return Diff(added, removed, modified, unchanged)

def print_report(diff: Diff) -> int:
    """Print a report of the differences."""
    def header(title: str, count: int):
        print(f"\n=== {title} ({count}) ===")

    header("ADDED", len(diff.added))
    for r in diff.added:
        print(f"+ {r.path}  size={r.size}")

    header("REMOVED", len(diff.removed))
    for r in diff.removed:
        print(f"- {r.path}")

    header("MODIFIED", len(diff.modified))
    for o, n in diff.modified:
        print(f"~ {o.path}  {o.sha256[:10]} -> {n.sha256[:10]}  size {o.size}->{n.size}")

    header("UNCHANGED", len(diff.unchanged))
    return 0 if not (diff.added or diff.removed or diff.modified) else 1