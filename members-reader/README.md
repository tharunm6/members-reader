# members-reader

A lightweight Python library and CLI for loading member records from a CSV file.

## Requirements

- Python 3.10+
- No third-party dependencies

## Installation

```bash
pip install members-reader
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/tharunm6/members-reader.git
```

## CSV format

Your CSV must include at minimum `first_name` and `last_name` columns. All other columns are passed through as-is.

```
id,first_name,last_name,email,gender,ip_address
1,Alice,Smith,alice@example.com,Female,1.2.3.4
2,Bob,Jones,bob@example.com,Male,5.6.7.8
```

## Usage as a library

```python
from members_reader import load_members, get_full_names

# Load all member dicts
members = load_members("members.csv")
for m in members:
    print(m["first_name"], m["email"])

# Just get a list of full names
for name in get_full_names("members.csv"):
    print(name)
```

### API

#### `load_members(filepath) -> list[dict]`

Reads the CSV at `filepath` and returns a list of dicts, one per row, keyed by column header.

Raises `FileNotFoundError` if the file does not exist.  
Raises `KeyError` if `first_name` or `last_name` columns are missing.

#### `get_full_names(filepath) -> list[str]`

Convenience wrapper that returns `["First Last", ...]` from the CSV.

## Usage as a CLI

After installing, a `members-reader` command is available:

```bash
# Print all names
members-reader members.csv

# Print names alongside extra columns
members-reader members.csv --field email gender
```

Or without installing:

```bash
python -m members_reader members.csv
python -m members_reader members.csv --field email
```

## Development

```bash
git clone https://github.com/tharunm6/members-reader.git
cd members-reader
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT
