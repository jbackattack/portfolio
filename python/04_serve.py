"""
04_serve.py  (intermediate)

A tiny local web server for previewing the site, a Python stand-in for
`npx serve .`. It reads vercel.json so clean URLs (/about) and redirects
(/work/spark -> /work/agents) behave the way they do on Vercel.

Run from the repo root:
    python3 python/04_serve.py
Then open http://localhost:8000 and press Ctrl+C to stop.

Concepts you'll see: subclassing, overriding methods, HTTP status codes
(200, 301, 404), and how a web server maps URLs to files.
"""

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PORT = 8000

CONFIG = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
REDIRECTS = {r["source"]: r["destination"] for r in CONFIG.get("redirects", [])}


class SiteHandler(SimpleHTTPRequestHandler):
    """
    SimpleHTTPRequestHandler already knows how to serve files from a folder.
    We subclass it and override do_GET (called for every page request) to add
    redirects, clean URLs, and the site's own 404 page.
    """

    def __init__(self, *args, **kwargs):
        # directory= tells the parent class which folder to serve.
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path

        # 1. Redirects from vercel.json.
        if path in REDIRECTS:
            self.send_response(301)  # 301 = moved permanently
            self.send_header("Location", REDIRECTS[path])
            self.end_headers()
            return

        # 2. Clean URLs: /about -> /about.html (only if that file exists).
        if not Path(path).suffix and path != "/":
            if (ROOT / f"{path.lstrip('/')}.html").is_file():
                self.path = f"{path}.html"

        # 3. Let the parent class serve the file.
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        # Swap the plain-text 404 for the site's own 404.html.
        if code == 404 and (ROOT / "404.html").is_file():
            body = (ROOT / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().send_error(code, message, explain)


def main():
    server = ThreadingHTTPServer(("localhost", PORT), SiteHandler)
    print(f"Serving {ROOT.name} at http://localhost:{PORT}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
