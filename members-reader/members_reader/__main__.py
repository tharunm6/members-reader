"""CLI entry point: python -m members_reader <file.csv>"""

import argparse
import sys

from .reader import load_members


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="members-reader",
        description="Print member names from a CSV file.",
    )
    parser.add_argument("csv_file", help="Path to the members CSV file")
    parser.add_argument(
        "--field",
        nargs="+",
        metavar="COLUMN",
        help="Extra columns to print alongside the name (e.g. --field email gender)",
    )
    args = parser.parse_args()

    try:
        members = load_members(args.csv_file)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    for m in members:
        line = f"{m['first_name']} {m['last_name']}"
        if args.field:
            extras = "  ".join(m.get(col, "") for col in args.field)
            line = f"{line}  {extras}"
        print(line)


if __name__ == "__main__":
    main()
