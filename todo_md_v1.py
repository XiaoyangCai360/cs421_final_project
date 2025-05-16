#!/usr/bin/env python3
"""
todo_md.py: extract TODO/FIXME comments into a Markdown report.
"""

import os
import re
import argparse
import sys

# Pattern to match TODO or FIXME markers and capture the following text
todo_pattern = re.compile(
    r'(?P<marker>TODO|FIXME)[\s:,-]*(?P<text>.*)',
    re.IGNORECASE,
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="TODO‑MD: extract TODO/FIXME comments into a Markdown report"
    )
    parser.add_argument(
        "directory",
        help="root folder to scan"
    )
    parser.add_argument(
        "-o", "--output",
        default="report.md",
        help="Markdown file to write"
    )
    return parser.parse_args()

def find_source_files(root):
    """
    Recursively yield all files under 'root' with extensions .py, .js, or .java
    """
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith((".py", ".js", ".java", ".hs")):
                yield os.path.join(dirpath, fname)

def collect_todos(file_path):
    """
    Scan a single file for TODO/FIXME comments.
    Returns a list of tuples: (line_number, marker, text).
    Only matches markers that start with an uppercase letter in source.
    """
    todos = []
    try:
        with open(file_path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                m = todo_pattern.search(line)
                if not m:
                    continue
                orig_marker = m.group("marker")
                # only accept markers that start uppercase (skip lowercase matches)
                if not orig_marker or not orig_marker[0].isupper():
                    continue
                marker = orig_marker.upper()
                text = m.group("text").strip()
                todos.append((lineno, marker, text))
    except (UnicodeDecodeError, FileNotFoundError):
        # Skip files that cannot be read
        pass
    return todos

def write_markdown(items, output_path, scanned_dir):
    """
    Write the collected TODO/FIXME items to a Markdown file.
    """
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("# TODO-MD Report\n\n")
        out.write(f"**Scanned directory:** `{scanned_dir}`  \n")
        out.write(f"**Found:** {len(items)} items\n\n")
        out.write("| # | File | Line | Marker | Comment |\n")
        out.write("|---|------|-----:|--------|---------|\n")
        for idx, (path, lineno, marker, text) in enumerate(items, start=1):
            out.write(f"| {idx} | `{path}` | {lineno} | {marker} | {text} |\n")
    print(f"Wrote Markdown report to {output_path}")

def main():
    args = parse_args()
    all_items = []

    # Collect TODO/FIXME from each source file
    for path in find_source_files(args.directory):
        for lineno, marker, text in collect_todos(path):
            all_items.append((path, lineno, marker, text))

    # If no items found, exit cleanly
    if not all_items:
        print("No TODOs/FIXMEs found.")
        sys.exit(0)

    # Write the Markdown report
    write_markdown(all_items, args.output, args.directory)

if __name__ == "__main__":
    main()
