# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install in editable mode (run once after cloning)
pip install -e .

# Run all tests
pytest

# Run a single test file
pytest tests/test_reader.py

# Run the CLI
members-reader members.csv
members-reader members.csv --field email gender

# Or without installing
python -m members_reader members.csv
```

## Architecture

This is a Python package (`members_reader/`) with no third-party dependencies.

- `members_reader/reader.py` — core logic: `load_members(filepath)` returns `list[dict]`, `get_full_names(filepath)` returns `list[str]`
- `members_reader/__init__.py` — re-exports the two public functions
- `members_reader/__main__.py` — CLI (`argparse`); registered as the `members-reader` entry point in `pyproject.toml`
- `tests/test_reader.py` — pytest tests using `tmp_path` fixtures; no external dependencies

The CSV must contain `first_name` and `last_name` columns. All other columns are passed through untouched.
