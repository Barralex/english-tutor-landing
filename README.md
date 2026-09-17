# TeroTalk

**Clases de inglés · Ciudad de la Costa, Uruguay**

Three pages: a home that splits visitors between two services, in-home lessons for kids, and a six-hour online program for professionals.

***

No build step, no dependencies, nothing to install. Edit the HTML and push.

```
index.html                     home, and the split between the two services
kids/index.html                in-home lessons, coverage map
professionals/index.html       the six-hour online program
assets/css/                    three stylesheets: entry, tokens, components
.github/scripts/check.py       checks every page before it goes out
.github/workflows/deploy.yml   publishes to GitHub Pages
```

Every push to `main` runs `check.py` first: broken markup, a page over the 60 KB budget, a reference to a file that is not in the repo, a base64 image pasted into the HTML, or a bad social preview tag stops the deploy, and the live site stays as it was.

```bash
python .github/scripts/check.py
```

Published at `https://barral.dev/terotalk/`, the URL that `SITE_BASE` in `check.py` validates every page against. A `CNAME` file wins over it, and the move to `terotalk.com` is a one-line change once the DNS points at GitHub Pages.

Conventions, design tokens and what is still open before launch: [CLAUDE.md](CLAUDE.md).

<p align="center"><sub>co-assisted by <b>Claude Opus 4.8</b></sub></p>
