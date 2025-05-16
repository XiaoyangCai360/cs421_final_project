# tests/test_todo_md_v2.py

import os
import pytest
import subprocess
import textwrap
from pathlib import Path

from todo_md_v2 import collect_todos_v2, write_markdown_v2
from todo_context import map_line_to_context

ROOT = os.path.dirname(os.path.dirname(__file__))
SP2  = os.path.join(ROOT, "sample_project_v2")
V2 = os.path.abspath("todo_md_v2.py")

# Skip if sample_project_v2 is missing
if not os.path.isdir(SP2):
    pytest.skip("sample_project_v2 missing; skipping v2 tests", allow_module_level=True)

def run_cli(script, src_dir, out_file):
    """Helper to invoke the CLI and return (returncode, stdout, stderr)."""
    proc = subprocess.run(
        ["python3", script, src_dir, "-o", out_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return proc.returncode, proc.stdout, proc.stderr


# ---------- Unit Tests ----------

def test_map_line_to_context_simple_function():
    code = "def foo():\n    pass\n"
    lookup = map_line_to_context(code)
    # line 2 inside foo()
    assert lookup.get(2) == "foo"


def test_collect_todos_v2_unit():
    # small in-memory C snippet
    path = Path(__file__).parent / "fixtures" / "util_block.c"
    # create fixture util_block.c
    path.write_text("/* TODO: block test */")
    items = collect_todos_v2(str(path))
    assert items == [(1, "TODO", "block test")]


# ---------- Feature Tests ----------

def test_collect_counts_per_file():
    cases = [
        ("util.c",     2),
        ("util.h",     1),
        ("test.js",    1),
        ("example.py", 3),
    ]
    for fname, exp in cases:
        items = collect_todos_v2(os.path.join(SP2, fname))
        assert len(items) == exp


def test_contexts_example_py():
    path = os.path.join(SP2, "example.py")
    raw  = collect_todos_v2(path)
    src  = open(path, encoding="utf-8").read()
    ctx  = map_line_to_context(src)
    mapping = {ln: ctx.get(ln, "<module>") for ln, _, _ in raw}
    assert mapping[3] == "<module>"
    assert mapping[6] == "foo"
    assert mapping[12] == "bar"


# ---------- Integration via CLI ----------

def test_cli_run_v2(tmp_path):
    sample = tmp_path / "sp2"
    sample.mkdir()
    # C multi-line example
    f = sample / "t.c"
    f.write_text("/* TODO: cli block\n   FIXME: another */")
    report = tmp_path / "out_v2.md"

    result = subprocess.run(
        ["python3", "todo_md_v2.py", str(sample), "-o", str(report)],
        capture_output=True
    )
    assert result.returncode == 0
    out = report.read_text()
    assert "TODO-MD v2 Report" in out
    assert "t.c" in out

def test_cli_multiple_markers_in_block_v2(tmp_path):
    # Single C file with one /* … */ containing two markers
    src = tmp_path / "block_test"
    src.mkdir()
    cfile = src / "multi.c"
    cfile.write_text(textwrap.dedent("""\
        /* 
         * TODO: first task in block
         * FIXME: second task in block
         */
        int foo() { return 0; }
    """))
    report = tmp_path / "out_block_v2.md"

    code, out, err = run_cli(V2, str(src), str(report))
    assert code == 0, f"v2 CLI failed: {err}"
    text = report.read_text()
    # Should find both markers separately
    assert "first task in block" in text
    assert "second task in block" in text
    # 'multi.c' should appear exactly twice
    assert text.count("multi.c") == 2

def test_cli_various_extensions_v2(tmp_path):
    # Create one file of each supported extension
    src = tmp_path / "mixed"
    src.mkdir()
    files = {
        "Test.java":    "// TODO: java marker\n",
        "Lib.hs":       "-- FIXME: haskell marker\n",
        "script.py":    "# TODO: python marker\n",
    }
    for name, content in files.items():
        (src / name).write_text(content)
    report = tmp_path / "out_ext_v2.md"

    code, out, err = run_cli(V2, str(src), str(report))
    assert code == 0, f"v2 CLI failed: {err}"
    text = report.read_text()
    # All three markers and filenames must appear
    for name in files:
        assert name in text
    assert "java marker" in text
    assert "haskell marker" in text
    assert "python marker" in text

if __name__ == "__main__":
    pytest.main()
