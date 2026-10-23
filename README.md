# Portfolio site

Plain HTML, CSS, and a little JavaScript. No framework, no build step, matching the setup of the Pack 55 wreath site (static project on Vercel, deployed from GitHub `main`).

## Structure

- `index.html`: home, with the animated "What I've delivered" panel
- `work.html`, `work/agents.html`, `work/wreath.html`: project list (work and passion projects), the AI test agents case study (formerly Spark), and the wreath sale app case study
- `about.html`, `testimonials.html`, `contact.html`, `404.html`
- `assets/styles.css`, `assets/app.js`, `assets/flow.js`, `assets/resume.pdf`
- `vercel.json`: clean URLs and security headers (including a Content Security Policy that allows Google Fonts)

## Run locally

```sh
npx serve .
```

`serve` reads `vercel.json`, so clean URLs like `/work` and `/work/agents` resolve the same way they do on Vercel.

## Before publishing

Every unfinished spot is wrapped in a yellow `class="todo"` highlight. List them with:

```sh
sh scripts/check-todos.sh
```

Still needed: last name for page titles, a photo at `assets/jeremy.jpg` (About page), earlier roles with dates (ESPN, MLB Advanced Media), more passion projects, a short description of each AI agent, wreath sale results after the season, and approved testimonials with photos.

## Testimonials

Quotes come from LinkedIn recommendations. Get each person's OK to publish their words, name, and title before pasting them into `testimonials.html` (the page has three placeholder cards).

## Deploy

1. Create a GitHub repo and push this folder to `main`.
2. In Vercel, import the repo under your personal account. Framework preset: Other. No build command, no output directory.
3. Add a custom domain if you want one. Vercel's default `.vercel.app` URLs can sit behind Vercel login depending on the account's protection settings, which would block recruiters.
