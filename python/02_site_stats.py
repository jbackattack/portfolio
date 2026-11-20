"""
02_site_stats.py  (beginner)

Shows how much of the site is HTML vs CSS vs JavaScript, so you can answer
"what is this written in?" with numbers instead of guessing.

Run from the repo root:
    python3 python/02_site_stats.py

Concepts you'll see: dictionaries, sorting, string formatting, skipping folders.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Map file extensions to a readable language name.
LANGUAGES = {
    ".html": "HTML",
    ".css": "CSS",
    ".js": "JavaScript",
    ".py": "Python",
    ".sh": "Shell",
    ".json": "JSON",
}

# Folders we never want to count.
SKIP_DIRS = {".git", "node_modules"}


def collect():
    """Return {language: [file_count, total_bytes]}."""
    totals = {}

    for path in ROOT.rglob("*"):
        # path.parts is a tuple like ("assets", "app.js"). If any part is a
        # skipped folder, ignore the file.
        if SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        if not path.is_file():
            continue

        language = LANGUAGES.get(path.suffix.lower())
        if language is None:
            continue  # images, PDFs, etc.

        # setdefault creates the entry the first time we see a language.
        entry = totals.setdefault(language, [0, 0])
        entry[0] += 1
        entry[1] += path.stat().st_size

    return totals


def main():
    totals = collect()
    grand_total = sum(size for _, size in totals.values())

    print(f"{'Language':<12}{'Files':>6}{'Bytes':>10}{'Share':>8}")
    print("-" * 36)

    # Sort languages by size, biggest first. key= tells sorted() what to compare.
    for language, (count, size) in sorted(
        totals.items(), key=lambda item: item[1][1], reverse=True
    ):
        share = size / grand_total * 100
        print(f"{language:<12}{count:>6}{size:>10,}{share:>7.1f}%")


if __name__ == "__main__":
    main()
