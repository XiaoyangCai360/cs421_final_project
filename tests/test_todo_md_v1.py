# tests/test_todo_md_v1.py

import os
import tempfile
import pytest
import subprocess
from pathlib import Path

from todo_md_v1 import collect_todos, write_markdown

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

V1 = os.path.abspath("todo_md_v1.py")
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

def test_collect_todos_single_line():
    # inline single-line TODO
    content = "# TODO: test unit\n"
    f = tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False)
    f.write(content); f.flush(); f.close()
    items = collect_todos(f.name)
    assert items == [(1, "TODO", "test unit")]

def test_collect_todos_multiple_markers():
    # two markers on different lines
    content = "# TODO: one\n# FIXME: two\n"
    path = tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False).name
    with open(path, "w") as f: f.write(content)
    items = collect_todos(path)
    assert len(items) == 2
    assert items[0][1] == "TODO"
    assert items[1][1] == "FIXME"


# ---------- Feature Tests ----------

def test_collect_no_todo_fixture():
    path = os.path.join(FIXTURE_DIR, "no_todo.py")
    assert collect_todos(path) == []

def test_collect_has_todo_fixture():
    path = os.path.join(FIXTURE_DIR, "has_todo.py")
    todos = collect_todos(path)
    # Expect exactly two TODOs and one FIXME
    markers = [m for (_, m, _) in todos]
    assert markers.count("TODO") == 2
    assert "FIXME" in markers


def test_write_markdown_creates_file(tmp_path):
    path = os.path.join(FIXTURE_DIR, "has_todo.py")
    todos = collect_todos(path)
    single = [(path, *todos[0])]
    md_file = tmp_path / "report.md"

    write_markdown(single, str(md_file), FIXTURE_DIR)
    text = md_file.read_text()
    assert "# TODO-MD Report" in text
    assert "| 1 |" in text


# ---------- Integration Test via CLI ----------

def test_cli_run_v1(tmp_path):
    # build a tiny sample project
    sample = tmp_path / "sample_proj"
    sample.mkdir()
    (sample / "a.py").write_text("# TODO: cli test\n")
    (sample / "b.js").write_text("// FIXME: cli test 2\n")
    report = tmp_path / "out_v1.md"

    result = subprocess.run(
        ["python3", "todo_md_v1.py", str(sample), "-o", str(report)],
        capture_output=True
    )
    assert result.returncode == 0
    out = report.read_text()
    assert "TODO-MD Report" in out
    assert "a.py" in out and "b.js" in out

def test_cli_nested_structure_v1(tmp_path):
    # Build nested directories with .py and .js files
    base = tmp_path / "proj"
    nested = base / "a" / "b"
    nested.mkdir(parents=True)
    (base / "root.py").write_text("# TODO: root level\n")
    (nested / "deep.js").write_text("// FIXME: deep level\n")
    report = tmp_path / "out_nested_v1.md"

    code, out, err = run_cli(V1, str(base), str(report))
    assert code == 0, f"v1 CLI failed: {err}"
    text = report.read_text()
    # Both files should appear, with relative paths preserved
    assert "root.py" in text
    assert "deep.js" in text
    # The markers should be present
    assert "TODO" in text and "FIXME" in text

if __name__ == "__main__":
    pytest.main()
