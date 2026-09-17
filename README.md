# Flor Santos · Bilingual Educator

**Clases de inglés · Solymar, Ciudad de la Costa, Uruguay**

A three-page static site for Flor Santos: a home page that splits visitors between two services, each with its own page and voice.

***

No build step, no dependencies, nothing to install. Edit the HTML and push.

```
index.html                     home: brand, the two services, who Flor is
kids/index.html                Teacher Flor: home visits for kids, coverage map
professionals/index.html       English at Work: 6-hour online program for adults
assets/css/site.css            shared styles and palette tokens
assets/brand/favicon.svg       the thread mark
assets/brand/og-cover.png      link preview image (placeholder)
robots.txt                     crawler rules
sitemap.xml                    three URLs, update lastmod when the copy changes
.github/scripts/check.py       checks every page before it goes out
.github/workflows/deploy.yml   publishes to GitHub Pages
```

Every push to `main` runs `check.py` first. It checks every page in `PAGES` and stops the deploy on broken markup, a page over the 60 KB budget, a reference to a file that is not in the repo, a base64 image pasted into the HTML, or a social preview tag that is missing, relative, or pointing at the wrong domain. A failure leaves the live site exactly as it was.

To run it by hand:

```bash
python .github/scripts/check.py
```

## Before the first deploy

The site is published at `https://barral.dev/english-tutor-landing/`, under the account's own domain rather than at `barralex.github.io`. Five places on every page carry that URL: the canonical link, `og:url`, both image tags and the JSON-LD `url`, plus `sitemap.xml` and `robots.txt`. `check.py` compares them against `SITE_BASE` and will fail the build if they disagree. If a client domain arrives, add a `CNAME` file with the bare host; it wins over `SITE_BASE`.

Still pending before launch: Flor's WhatsApp number (every `wa.me/` link is blank), a photo of her teaching (`assets/flor-santos.jpg` is the portrait, and it appears on the home page only — on purpose, so it does not lose its effect), the price of the English at Work program, the real coverage polygon in `kids/index.html`, testimonials, and a real `og-cover.png`.

## Conventions

Commits follow `type(scope): short message`, e.g. `feat(landing): add rate card`, `fix(deploy): ...`, `docs(readme): ...`.

Colors live as custom properties in `:root` of `assets/css/site.css`: pizarra `#4A4E6D` (from her LinkedIn banner), noche `#262940`, arena `#F3ECE0`, ceibo `#B8323A` (accent, used sparingly), celeste `#A9C4DE`, pino `#355E52` (map only). Type: Fraunces for headings, Figtree for text, Caveat only for handwritten notes. Copy is Rioplatense voseo.

<p align="center"><sub>co-assisted by <b>Claude Opus 5</b></sub></p>
