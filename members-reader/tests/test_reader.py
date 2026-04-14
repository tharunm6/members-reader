import csv
import pytest
from pathlib import Path
from members_reader import load_members, get_full_names


@pytest.fixture()
def members_csv(tmp_path: Path) -> Path:
    """Create a small members CSV for testing."""
    path = tmp_path / "members.csv"
    rows = [
        {"id": "1", "first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "gender": "Female", "ip_address": "1.2.3.4"},
        {"id": "2", "first_name": "Bob",   "last_name": "Jones", "email": "bob@example.com",   "gender": "Male",   "ip_address": "5.6.7.8"},
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.fixture()
def bad_csv(tmp_path: Path) -> Path:
    """CSV missing required columns."""
    path = tmp_path / "bad.csv"
    path.write_text("name,age\nAlice,30\n")
    return path


def test_load_members_returns_list(members_csv):
    members = load_members(members_csv)
    assert isinstance(members, list)
    assert len(members) == 2


def test_load_members_fields(members_csv):
    members = load_members(members_csv)
    assert members[0]["first_name"] == "Alice"
    assert members[0]["last_name"] == "Smith"
    assert members[0]["email"] == "alice@example.com"


def test_load_members_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_members("nonexistent.csv")


def test_load_members_missing_columns(bad_csv):
    with pytest.raises(KeyError):
        load_members(bad_csv)


def test_get_full_names(members_csv):
    names = get_full_names(members_csv)
    assert names == ["Alice Smith", "Bob Jones"]


def test_get_full_names_empty(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("first_name,last_name\n")
    assert get_full_names(path) == []
