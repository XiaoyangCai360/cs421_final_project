#!/usr/bin/env python3
import ast
import re

# ———————————————————————————————————————————
# Python context
# ———————————————————————————————————————————
def get_end_lineno(node):
    max_line = getattr(node, "lineno", 0)
    for child in ast.walk(node):
        if hasattr(child, "lineno"):
            max_line = max(max_line, child.lineno)
    return max_line

def map_python_context(source_code: str) -> dict:
    tree = ast.parse(source_code)
    intervals = []
    class DefVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            start = node.lineno
            end   = get_end_lineno(node)
            intervals.append((start, end, node.name))
            self.generic_visit(node)
        def visit_AsyncFunctionDef(self, node):
            start = node.lineno
            end   = get_end_lineno(node)
            intervals.append((start, end, node.name))
            self.generic_visit(node)
        def visit_ClassDef(self, node):
            start = node.lineno
            end   = get_end_lineno(node)
            intervals.append((start, end, node.name))
            self.generic_visit(node)
    DefVisitor().visit(tree)

    lookup = {}
    for start, end, name in intervals:
        for ln in range(start, end+1):
            lookup[ln] = name
    return lookup

# ———————————————————————————————————————————
# Haskell context
# ———————————————————————————————————————————
HS_SIG_RE = re.compile(r"^([A-Za-z_][\w']*)\s*::")
HS_EQ_RE  = re.compile(r"^([A-Za-z_][\w']*)\s+.*=")

def map_haskell_context(source_code: str) -> dict:
    """
    Walk each line, updating `current` whenever we see
    NAME :: ...   or   NAME args = ...
    """
    lookup = {}
    current = "<module>"
    for lineno, line in enumerate(source_code.splitlines(), start=1):
        sig = HS_SIG_RE.match(line)
        eq  = HS_EQ_RE.match(line)
        if sig:
            current = sig.group(1)
        elif eq:
            current = eq.group(1)
        lookup[lineno] = current
    return lookup

# ———————————————————————————————————————————
# Unified mapper
# ———————————————————————————————————————————

def map_line_to_context(source_code: str, filename: str = None) -> dict:
    """
    If filename ends with .hs, use Haskell mapping;
    otherwise fall back to Python AST mapping.
    """
    if filename and filename.lower().endswith(".hs"):
        return map_haskell_context(source_code)
    return map_python_context(source_code)
