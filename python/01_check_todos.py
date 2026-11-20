"""
01_check_todos.py  (beginner)

Python version of scripts/check-todos.sh.
Finds every placeholder left on the site (anything marked class="todo").

Run from the repo root:
    python3 python/01_check_todos.py

Concepts you'll see: pathlib, for loops, reading files, enumerate,
f-strings, exit codes.
"""

import sys
from pathlib import Path

# Path(__file__) is this script's location. .parent is the python/ folder,
# and .parent again is the repo root. This works no matter where you run it from.
ROOT = Path(__file__).resolve().parent.parent

MARKER = 'class="todo"'


def find_todos():
    """Return a list of (file, line_number, line_text) for every placeholder."""
    found = []

    # rglob("*.html") means "every .html file in this folder and all subfolders".
    # sorted() keeps the output in a predictable order.
    for html_file in sorted(ROOT.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")

        # splitlines() turns the file into a list of lines.
        # enumerate(..., start=1) gives us a line number alongside each line.
        for number, line in enumerate(text.splitlines(), start=1):
            if MARKER in line:
                found.append((html_file.relative_to(ROOT), number, line.strip()))

    return found


def main():
    todos = find_todos()

    if not todos:
        print("No placeholders left.")
        return 0

    for path, number, line in todos:
        # Trim long lines so the output stays readable.
        print(f"{path}:{number}: {line[:100]}")

    print(f"\n{len(todos)} placeholder(s). Replace them before publishing.")
    return 1  # a non-zero exit code means "something needs attention"


if __name__ == "__main__":
    # sys.exit passes main()'s return value to the shell, like `exit 1` in sh.
    sys.exit(main())
