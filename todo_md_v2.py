#!/usr/bin/env python3
"""
todo_md_v2.py: PLY-based TODO/FIXME extractor with multi-line comment support
and AST-based context mapping.
"""

import os
import sys
import argparse
import re

from todo_lexer import build_lexer
from todo_context import map_line_to_context

# Regex to pull out the marker and comment text from a COMMENT token
TODO_PATTERN = re.compile(
    r"\b(TODO|FIXME)\b[:\s\-]*(.*)",
    re.IGNORECASE
)

# Pattern to remove trailing block comment delimiters
TRAILER_PATTERN = re.compile(r"\s*\*/\s*$")

def parse_args():
    parser = argparse.ArgumentParser(
        description="TODO-MD v2: PLY lexer + AST context"
    )
    parser.add_argument(
        "directory",
        help="root folder to scan for source files"
    )
    parser.add_argument(
        "-o", "--output",
        default="report_v2.md",
        help="Markdown file to write"
    )
    return parser.parse_args()


def find_source_files(root):
    """
    Yield all files under 'root' with common source extensions.
    """
    exts = (".py", ".js", ".java", ".c", ".h", ".hs")
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.endswith(exts):
                yield os.path.join(dirpath, f)


def collect_todos_v2(file_path):
    """
    Lex the entire file to get COMMENT tokens, then regex-find TODO markers.
    Returns list of (lineno, marker, comment_text).
    Strips trailing '*/' from block comments.
    """
    try:
        text = open(file_path, encoding="utf-8").read()
    except (UnicodeDecodeError, FileNotFoundError):
        return []

    lexer = build_lexer()
    lexer.input(text)

    comments = []
    for tok in lexer:
        if tok.type == "COMMENT":
            comments.append((tok.lineno, tok.value))

    results = []
    for lineno, comment in comments:
        for m in TODO_PATTERN.finditer(comment):
            marker = m.group(1).upper()
            comment_text = m.group(2).strip()
            # remove trailing block comment delimiters if present
            comment_text = TRAILER_PATTERN.sub("", comment_text)
            results.append((lineno, marker, comment_text))
    return results


def write_markdown_v2(items, output_path, scanned_dir):
    """
    Write a Markdown report with columns:
      # │ File │ Line │ Context │ Marker │ Comment
    """
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("# TODO-MD v2 Report\n\n")
        out.write(f"**Scanned directory:** `{scanned_dir}`  \n")
        out.write(f"**Found:** {len(items)} items\n\n")
        out.write("| # | File | Line | Context | Marker | Comment |\n")
        out.write("|---|------|-----:|---------|--------|---------|\n")
        for idx, (path, lineno, context, marker, text) in enumerate(items, start=1):
            out.write(
                f"| {idx} | `{path}` | {lineno} | {context} | {marker} | {text} |\n"
            )
    print(f"Wrote Markdown report to {output_path}")


def main():
    args = parse_args()
    all_items = []

    for path in find_source_files(args.directory):
        todos = collect_todos_v2(path)
        try:
            src = open(path, encoding="utf-8").read()
            ctx_map = map_line_to_context(src, path)
        except Exception:
            ctx_map = {}

        for lineno, marker, comment_text in todos:
            context = ctx_map.get(lineno, "<module>")
            all_items.append((path, lineno, context, marker, comment_text))

    if not all_items:
        print("No TODOs/FIXMEs found.")
        sys.exit(0)

    write_markdown_v2(all_items, args.output, args.directory)

if __name__ == "__main__":
    main()
