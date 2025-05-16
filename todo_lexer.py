#!/usr/bin/env python3
import ply.lex as lex

# Token names
tokens = (
    'COMMENT',
)

# Match C-style block comments (/*...*/), Python “#…”, JS “//…”, and Haskell “--…” comments
t_COMMENT = r'/\*(.|\n)*?\*/|//[^\n]*|\#[^\n]*|--[^\n]*'

# Track newlines inside comments and elsewhere
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Ignore spaces, tabs, and carriage returns
t_ignore = ' \t\r'

def t_error(t):
    # Skip invalid characters
    t.lexer.skip(1)

def build_lexer(**kwargs):
    """
    Build and return the PLY lexer instance.
    """
    return lex.lex(**kwargs)
