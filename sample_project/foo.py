# foo.py

import os        # used
import sys       # unused

# TODO: add error handling for missing directory
def list_dir(path):
    files = os.listdir(path)
    # FIXME: what if path is not a directory?
    return files

def hello():
    # TODO   support greeting in other languages
    print("Hello, world!")
