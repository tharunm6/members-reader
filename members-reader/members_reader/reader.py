import csv
from pathlib import Path
from typing import Union


def load_members(filepath: Union[str, Path]) -> list:
    """Load members from a CSV file.

    The CSV must contain at minimum the columns: first_name, last_name.
    Additional columns (id, email, gender, ip_address, etc.) are included
    as-is in each returned dict.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of dicts, one per row, keyed by column header.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        KeyError: If the CSV is missing required columns (first_name, last_name).

    Example:
        >>> from members_reader import load_members
        >>> members = load_members("members.csv")
        >>> for m in members:
        ...     print(m["first_name"], m["last_name"])
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if rows:
        missing = {"first_name", "last_name"} - rows[0].keys()
        if missing:
            raise KeyError(f"CSV is missing required columns: {missing}")

    return rows


def get_full_names(filepath: Union[str, Path]) -> list:
    """Return a list of 'First Last' strings from a members CSV.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of full name strings.

    Example:
        >>> from members_reader import get_full_names
        >>> for name in get_full_names("members.csv"):
        ...     print(name)
    """
    return [
        f"{m['first_name']} {m['last_name']}"
        for m in load_members(filepath)
    ]
