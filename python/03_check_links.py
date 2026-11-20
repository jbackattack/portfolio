"""
03_check_links.py  (intermediate)

Checks that every internal link, image, script, and stylesheet on the site
points to a file that actually exists. Catches typos and broken pages before
you publish. External links (https://...) are skipped.

Run from the repo root:
    python3 python/03_check_links.py

Concepts you'll see: classes and inheritance, the standard-library HTML
parser, URL handling, sets, and mirroring Vercel's "clean URLs" behavior.
"""

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# Which HTML attribute holds the link, for each tag we care about.
LINK_ATTRS = {"a": "href", "link": "href", "script": "src", "img": "src"}


class LinkCollector(HTMLParser):
    """
    HTMLParser reads HTML piece by piece and calls handle_starttag() every time
    it sees an opening tag. We inherit from it and override that method to
    collect links and element ids.
    """

    def __init__(self):
        super().__init__()  # run HTMLParser's own setup first
        self.links = []     # every URL we find
        self.ids = set()    # every id="..." on the page (for #anchor links)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)  # [("href", "/about")] -> {"href": "/about"}

        if "id" in attrs:
            self.ids.add(attrs["id"])

        wanted = LINK_ATTRS.get(tag)
        if wanted and attrs.get(wanted):
            self.links.append(attrs[wanted])


def load_redirect_sources():
    """Read vercel.json so redirected URLs (like /work/spark) count as valid."""
    config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    return {r["source"] for r in config.get("redirects", [])}


def resolve(url_path):
    """
    Turn a URL path into a file on disk, the way Vercel does with cleanUrls:
        /           -> index.html
        /about      -> about.html
        /work/agents-> work/agents.html
        /assets/x.js-> assets/x.js
    Returns the Path if it exists, otherwise None.
    """
    relative = url_path.lstrip("/")
    candidates = [
        ROOT / relative,                  # exact file, e.g. assets/app.js
        ROOT / f"{relative}.html",        # clean URL, e.g. about -> about.html
        ROOT / relative / "index.html",   # folder index, e.g. / -> index.html
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def parse_page(html_file):
    collector = LinkCollector()
    collector.feed(html_file.read_text(encoding="utf-8"))
    return collector


def main():
    redirects = load_redirect_sources()
    pages = {p: parse_page(p) for p in sorted(ROOT.rglob("*.html"))}
    problems = []
    checked = 0

    for page, collector in pages.items():
        page_name = page.relative_to(ROOT)

        for link in collector.links:
            parsed = urlparse(link)

            # Skip external links and non-page schemes (mailto:, tel:, etc.).
            if parsed.scheme or parsed.netloc:
                continue

            checked += 1

            # A bare "#main" link points at an id on the same page.
            if not parsed.path:
                if parsed.fragment and parsed.fragment not in collector.ids:
                    problems.append(f"{page_name}: missing anchor #{parsed.fragment}")
                continue

            if parsed.path in redirects:
                continue

            # Vercel creates /_vercel/... files (like analytics) at deploy time,
            # so they never exist in the repo. Not a real broken link.
            if parsed.path.startswith("/_vercel/"):
                continue

            target = resolve(parsed.path)
            if target is None:
                problems.append(f"{page_name}: broken link {link}")
                continue

            # If the link has an #anchor, make sure that id exists on the target page.
            if parsed.fragment and target.suffix == ".html":
                target_ids = pages[target].ids
                if parsed.fragment not in target_ids:
                    problems.append(
                        f"{page_name}: {parsed.path} has no #{parsed.fragment}"
                    )

    for problem in problems:
        print(problem)

    print(f"\nChecked {checked} internal links across {len(pages)} pages.")
    if problems:
        print(f"{len(problems)} problem(s) found.")
        return 1
    print("All internal links look good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
