.PHONY: all run run-v1 run-v2 test test-v1 test-v2 clear

REPORT_DIR := reports
SRC        ?= sample_project   # default source directory, but overrideable

# Default: build both reports and run all tests
all: run test

# Combined run of both versions
run: run-v1 run-v2

# Ensure REPORT_DIR exists
$(REPORT_DIR):
	mkdir -p $@

# Generate v1 report from $(SRC)
run-v1: $(REPORT_DIR)
	python3 todo_md_v1.py $(SRC) --output $(REPORT_DIR)/report_v1.md

# Generate v2 report from $(SRC)
run-v2: $(REPORT_DIR)
	python3 todo_md_v2.py $(SRC) --output $(REPORT_DIR)/report_v2.md

# Run only the v1 tests
test-v1:
	python3 -m pytest -q tests/test_todo_md_v1.py

# Run only the v2 tests
test-v2:
	python3 -m pytest -q tests/test_todo_md_v2.py

# Run the full test suite
test:
	python3 -m pytest -q

# Clean out all generated reports
clear:
	rm -rf $(REPORT_DIR)
