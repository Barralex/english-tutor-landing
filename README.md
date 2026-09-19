<div align="center">

<img src="assets/brand/banner.png" width="100%" alt="TeroTalk">
<br><br>

[![Live](https://img.shields.io/badge/live-terotalk.com-262940?style=flat-square)](https://terotalk.com/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-deployed-B8323A?style=flat-square&logo=github&logoColor=white)](https://terotalk.com/)
[![Build](https://img.shields.io/badge/build-none-5F6073?style=flat-square)](#requirements)
[![License](https://img.shields.io/badge/license-proprietary-4A4E6D?style=flat-square)](LICENSE)

### Untangle your English.

An IB-trained teacher in Ciudad de la Costa, Uruguay.<br>
In-home lessons for kids, and a six-hour online program for working professionals.

</div>

---

<img src="assets/brand/preview.jpg" width="100%" alt="terotalk.com on desktop and mobile">

---

## The brief

Flor teaches; TeroTalk is only the name over the door, and the site was built so the name never gets in front of the person. The two services stay apart on purpose, because the parent who is tired of driving a kid across town and the professional who freezes in an English meeting are not the same person and cannot be told the same thing. Nothing here asks for a form or a password. Every path ends where the work actually starts: a message to Flor.

## Under the hood

Three static pages, one per audience, with a home that splits between them. HTML and three stylesheets, no build step and no dependencies. Every push to `main` is checked before it ships, and a check that fails leaves the live site exactly as it was.

Design tokens, conventions and open work: [CLAUDE.md](CLAUDE.md). The brand is kept as source in [design/](design/): one script draws the mark and writes every logo, favicon, seal and canvas board from it, so none of them can drift.

## Requirements

- A text editor. There is no build step and nothing to install.
- Python 3, to run `.github/scripts/check.py` before pushing.
- A GitHub account with Pages enabled, to publish.

## License

&copy; 2026 [Luis Barral](https://barral.dev). All rights reserved. The code is public to read, not to reuse: copying or adapting it needs written permission. See [LICENSE](LICENSE).

The brand, the copy and the photography belong to the client and are not covered by it.

<div align="center">

**[Luis Barral](https://barral.dev)** &middot; All rights reserved

<a href="CLAUDE.md"><img src="assets/brand/signature.svg" height="29" alt="co-assisted by Claude Opus 5"></a>

</div>
