"""Verify a copied directory tree against its source by size and SHA-256.

Usage: python3 main.py source_dir dest_dir
Reports missing, extra and differing files; identical files are not listed.
"""
import argparse
import hashlib
import os
import sys


def snapshot(root):
    result = {}
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            digest = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    digest.update(chunk)
            result[rel] = (os.path.getsize(path), digest.hexdigest())
    return result


def compare(source, dest):
    missing = sorted(set(source) - set(dest))
    extra = sorted(set(dest) - set(source))
    differing = sorted(k for k in source if k in dest and source[k] != dest[k])
    return missing, extra, differing


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("dest")
    args = parser.parse_args(argv)
    missing, extra, differing = compare(snapshot(args.source), snapshot(args.dest))
    print(f"missing: {len(missing)}, extra: {len(extra)}, differing: {len(differing)}")
    for label, items in (("missing", missing), ("extra", extra), ("differing", differing)):
        for item in items:
            print(f"- {label}: {item}")
    return 1 if (missing or differing) else 0


if __name__ == "__main__":
    sys.exit(main())
