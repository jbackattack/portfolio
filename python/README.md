# Python scripts for the portfolio

Small scripts that do real jobs for this site, written to be read and
modified while learning Python. They use only the standard library, so there
is nothing to install. Run each one from the repo root.

| Script | Level | What it does | What it teaches |
| --- | --- | --- | --- |
| `01_check_todos.py` | Beginner | Lists leftover `class="todo"` placeholders (Python version of `scripts/check-todos.sh`) | files, loops, `enumerate`, exit codes |
| `02_site_stats.py` | Beginner | Shows how much of the site is HTML, CSS, JavaScript | dictionaries, sorting, formatting |
| `03_check_links.py` | Intermediate | Finds broken internal links, images, and `#anchors` | classes, the HTML parser, sets, URLs |
| `04_serve.py` | Intermediate | Local preview server with clean URLs and redirects from `vercel.json` | subclassing, HTTP status codes |

```sh
python3 python/01_check_todos.py
python3 python/02_site_stats.py
python3 python/03_check_links.py
python3 python/04_serve.py      # then open http://localhost:8000
```

## Ways to practice

- In `01`, also flag the word `TODO` in plain text, not just `class="todo"`.
- In `02`, add a line count column next to bytes.
- In `03`, list pages that nothing links to.
- In `04`, add the `Cache-Control` header from `vercel.json` for `/assets/`.

The site itself stays plain HTML, CSS, and a little JavaScript. These scripts
sit beside it and are not part of the deployed pages.
