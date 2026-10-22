[README (2).md](https://github.com/user-attachments/files/33845278/README.2.md)
# Portfolio site

Plain HTML, CSS, and a little JavaScript. No framework, no build step, matching the setup of the Pack 55 wreath site (static project on Vercel, deployed from GitHub `main`).

## Structure

- `index.html`: home, with the animated "checks on my work" hero
- `work.html`, `work/spark.html`: project list and the Spark case study
- `about.html`, `testimonials.html`, `contact.html`, `404.html`
- `assets/styles.css`, `assets/app.js`
- `vercel.json`: clean URLs and security headers (including a Content Security Policy that allows Google Fonts)

## Run locally

```sh
npx serve .
```

`serve` reads `vercel.json`, so clean URLs like `/work` and `/work/spark` resolve the same way they do on Vercel.

## Before publishing

Every unfinished spot is wrapped in a yellow `class="todo"` highlight. List them with:

```sh
sh scripts/check-todos.sh
```

Still needed: last name for page titles, a photo at `assets/jeremy.jpg` (About page), email, LinkedIn, resume link, job dates and earlier roles, real testimonials, and a check of the Spark step order.

## Testimonials

Quotes come from LinkedIn recommendations. Get each person's OK to publish their words, name, and title before pasting them into `testimonials.html` (the page has three placeholder cards).

## Deploy

1. Create a GitHub repo and push this folder to `main`.
2. In Vercel, import the repo under your personal account. Framework preset: Other. No build command, no output directory.
3. Add a custom domain if you want one. Vercel's default `.vercel.app` URLs can sit behind Vercel login depending on the account's protection settings, which would block recruiters.
