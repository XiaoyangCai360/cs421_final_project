# Todo-MD
## A TODO/FIXME Comment Extractor
_CS 421 Spring 2025 Final Project - Xiaoyang Cai_

Todo-MD is a command-line utility that scans your codebase for `TODO` and `FIXME` markers and spits out a neat Markdown report. It supports multiple languages (Python, JavaScript, Java, C, Haskell) in two modes:

- **v1**: Regex-based scanner (`todo_md_v1.py`)  
- **v2**: PLY lexer + context mapping (`todo_md_v2.py`)

---

## Repository Structure
```
.
├── Makefile
├── README.md
├── todo_md_v1.py
├── todo_md_v2.py
├── todo_lexer.py
├── todo_context.py
├── sample_project/
├── sample_project_v2/
├── sample_project_v3/
├── tests/
│   ├── fixtures/
│   ├── test_todo_md_v1.py
│   └── test_todo_md_v2.py
├── reports/        # generated Markdown reports (ignored by Git)
└── venv/           # Python virtual environment (ignored by Git)
```

---

## Prerequisites

- **Python** 3.9 or newer  
- Install required packages: 
```bash
  pip install ply pytest
```

- (Optional but recommended) create and activate a virtual environment:
```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install ply pytest
```

---
## Usage
### Build Both Reports
```Bash
    make run
```

This will generate:

- `reports/report_v1.md`

- `reports/report_v2.md`

### Build Only One Version
```Bash
    make run-v1         # Only v1 (regex-based)
    make run-v2         # Only v2 (lexer + context)
```

### Override Source Directory
By default `Makefile` uses `sample_project/`. To run on another directory:
```Bash
    make run SRC=sample_project_3
    make run-v2 SRC=other_repo
```

### Clean Generated Reports
```Bash
    make clear
```
---

## Examples
Scan the default sample project:
``` Bash
    python3 todo_md_v1.py sample_project
    python3 todo_md_v2.py sample_project
```

Scan a custom directory and output to a specific file:
``` Bash
    python3 todo_md_v2.py path/to/code -o reports/my_report.md
```
---

## Testing
Run the full test suite:
``` Bash
    make test
    # or
    pytest -q
```

Run only version-specific tests:
``` Bash
    make test-v1     # tests for todo_md_v1.py
    make test-v2     # tests for todo_md_v2.py
```

---
## Future Improvements
- **Haskell Mapping Limitation**: Enhance the Haskell mapper to look ahead and associate pre-definition comments with the function that follows.

- **Language Coverage**: Add context mapping for C, Java, and JavaScript functions and methods.

- **Configuration**: Support custom markers and file extensions via a config file (TOML/YAML).

- **Additional Outputs**: Export JSON or HTML reports for integration with dashboards.

---
## License
```
MIT © 2025 Xiaoyang Cai
```
