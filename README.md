# English Tutor Landing

**Private English classes for children · Ciudad de la Costa, Uruguay**

A one-page site for a bilingual teacher. Scaffold only: the structure, the tooling and the deploy pipeline are in place; the name, the copy, the palette and the photography are still open.

***

A single static page: no build step, no dependencies, nothing to install. Edit `index.html` and push.

```
index.html                     the page
assets/                        images
assets/brand/og-cover.png      link preview image (placeholder)
robots.txt                     crawler rules
sitemap.xml                    one URL, update lastmod when the copy changes
.github/scripts/check.py       checks the page before it goes out
.github/workflows/deploy.yml   publishes to GitHub Pages
```

Every push to `main` runs `check.py` first. It stops the deploy on broken markup, a page over the 60 KB budget, a reference to a file that is not in the repo, a base64 image pasted into the HTML, or a social preview tag that is missing, relative, or pointing at the wrong domain. A failure leaves the live site exactly as it was.

To run it by hand:

```bash
python .github/scripts/check.py
```

## Before the first deploy

The scaffold assumes `https://barralex.github.io/english-tutor-landing/`. Four places carry that URL: the canonical link, `og:url`, both image tags, and `sitemap.xml`. If a custom domain arrives, add a `CNAME` file with the bare host and change all four together; `check.py` reads `CNAME` and will fail the build if they disagree.

Also still to replace: every string reading *Nombre del proyecto*, the placeholder copy in each section, the WhatsApp link in the contact section, and `assets/brand/og-cover.png`, which is a flat blue rectangle standing in for the real preview image.

## Conventions

Commits follow `type(scope): short message`, e.g. `feat(landing): add rate card`, `fix(deploy): ...`, `docs(readme): ...`.

Colors live as custom properties in `:root`. The current set is a neutral placeholder — one blue, one ink, two greys — meant to be replaced once the brand is decided, not built on.

<p align="center"><sub>co-assisted by <b>Claude Opus 5</b></sub></p>
