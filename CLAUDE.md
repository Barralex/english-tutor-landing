# CLAUDE.md

Working guide for this repository. Read it before making any change.

> **Maintenance rule — non-negotiable.** This file is part of the deliverable, not a
> side note. Any change that touches the vision, the information architecture, the
> design tokens, the copy strategy, the deploy pipeline, or the open work below must
> update this file **in the same commit** as the code. A pull request that changes
> behaviour and leaves `CLAUDE.md` stale is incomplete. When you finish a task, your
> last step is to re-read this file and reconcile it with what you just shipped.

---

## 1. Project

**TeroTalk** — a three-page static marketing site for an independent English
teacher based in Solymar, Ciudad de la Costa, Uruguay.

The site is not a brochure. It is a booking funnel: every page exists to move a
visitor into a WhatsApp conversation with Flor.

### Vision

One umbrella brand, two distinct businesses, kept apart on purpose.

**TeroTalk** is the name on the header, the footer and the domain. Flor Santos is
the person behind it and stays visible everywhere — the brand lockup reads
*TeroTalk · con Flor Santos*, and the home page explains the name once, in her
voice, in the "Quién enseña" section. The brand never replaces the person:
§2 Positioning depends on a named human, so a change that hides Flor is a
regression, not a rebrand.

| | **Teacher Flor** (`/kids/`) | **English at Work** (`/professionals/`) |
|---|---|---|
| Audience | Parents in Ciudad de la Costa | Working professionals across Latin America |
| Service | In-home English lessons for kids | 6-hour one-to-one online program |
| Delivery | Flor drives to the student's house | Video call |
| Emotional hook | Relief — no more driving your kid around | Fear — freezing up in an English meeting |
| Proof | Classroom experience (The British Schools, IB PYP/MYP) | Same credentials, reframed for business |

The home page (`/`) carries the shared brand and acts as a **splitter**: it
establishes who Flor is, then sends each visitor through one of two "doors."
A visitor should reach the right page in one click and never see the other
offer's pricing or objections.

### Positioning

The competitive landscape is anonymous listings on classifieds portals and
institutes selling group courses and exams. The site's answer is threefold, and
every page must reinforce it:

1. **A named person with a history** — you know who enters your house and where she taught.
2. **One-to-one, never a group** — no cohorts, no exam mill.
3. **Zero travel** — she drives to the kids; adults join a call.

### Audience of this repository

The site is shown to prospective clients, and the repository is shown to
prospective employers. Code quality, commit history, and documentation are part
of the product. Hold both to a professional standard.

---

## 2. Architecture

No build step, no package manager, no framework, no dependencies to install.
Edit HTML, commit, push. That constraint is deliberate — it keeps the site fast,
keeps the repo legible, and means the site can never break because of a
dependency update.

```
index.html                     Home: brand, the two doors, who Flor is
kids/index.html                Teacher Flor: in-home lessons, coverage map
professionals/index.html       English at Work: the 6-hour program
assets/css/site.css            Entry: layer order, imports, reset, base, layout, utilities
assets/css/tokens.css          Primitives, semantic aliases, spacing and type scales
assets/css/components.css      Every component block, BEM
assets/brand/favicon.svg       The knot mark
assets/brand/og-cover.png      Link preview image (PLACEHOLDER — see §7)
assets/flor-santos.jpg         Portrait, home page only
robots.txt                     Crawler rules
sitemap.xml                    Three URLs; bump lastmod when copy changes
.github/scripts/check.py       Pre-deploy gate (see §5)
.github/workflows/deploy.yml   GitHub Pages deploy
```

### Conventions that hold across all three pages

- **Everything in the tree is English.** File names, folder names, asset names, URL
  slugs, `id`s, anchor fragments, CSS classes and JavaScript identifiers — English,
  kebab-case, descriptive. The rendered copy is Spanish; the code is not. Dates are the
  one place the US convention does not apply: ISO 8601 `YYYY-MM-DD`, never `MM/DD/YYYY`.
- **Three stylesheets, one cascade.** `site.css` is the only file the pages link. It
  declares the layer order, imports the other two and holds reset, base, layout and
  utilities. Do not add a fourth file and do not introduce a CSS framework. Inline
  `style` attributes are not allowed: there are none left in the markup.
- **BEM, never the tag.** `.card__title`, `.door--pros`. No `.why div`, no `nth-child`
  on a tag, no styling that breaks when an element changes.
- **Page theming via a body class.** `.t-kids` and `.t-pros` re-skin shared
  components per page. Add a theme override there rather than duplicating a component.
- **Inline SVG sprite.** Icons live in a hidden `<svg>` symbol block at the top of
  each page (`#knot`, `#arrow`, `#chat`) and are used via `<use href="#id">`. Add new
  icons to the sprite; never paste a base64 image into the HTML (`check.py` fails the build).
- **Only two external runtime dependencies**, both from a CDN: Google Fonts in every
  `<head>`, and Leaflet 1.9.4 for the coverage map on the kids page. Adding a third
  needs a real justification.
- **Structured data.** The home page carries a `Person` JSON-LD block. Keep it in
  sync with the visible credentials.

---

## 3. Design system

All tokens live in `:root` of `assets/css/site.css`. **Never hardcode a hex value
in a page or a new rule — add or reuse a token.**

### Palette

The palette lives in two tiers. Primitives carry the only hex values in the codebase;
components consume semantic aliases and never a primitive directly. Renaming a colour is
one line in `tokens.css`.

| Semantic token | Primitive | Role |
|---|---|---|
| `--color-surface` | `--sand-100` `#F3ECE0` | Page background |
| `--color-surface-raised` | `--sand-50` `#FBF8F2` | Cards, chips, raised panels |
| `--color-surface-sunken` | `--sand-200` `#E9DFCE` | Recessed panels |
| `--color-text` | `--navy-900` `#262940` | Body and headings |
| `--color-text-muted` | `--slate-500` `#5F6073` | Secondary text |
| `--color-accent` | `--red-600` `#B8323A` | Emphasis, focus ring, primary CTA |
| `--color-accent-strong` | `--red-700` `#9A2830` | CTA hover only |
| `--color-brand` | `--slate-600` `#4A4E6D` | Eyebrows, handwriting, brand mark |
| `--color-border` | `--sand-300` `#DCD2C0` | Every hairline |
| `--color-map-area` / `--color-map-base` | `--green-700` / `--red-600` | Coverage map only |

**Dark sections never override a component.** `.band--dark`, `.page-hero--dark` and
`.site-footer` rebind the semantic tokens on themselves, so every component inside adapts
without a single descendant selector. Accent discipline: red is the only saturated colour
and it means "act here"; in a dark context the rebinding swaps it for `--blue-300`.

Spacing is a 4px scale, `--space-1` to `--space-24`. No component invents a padding.

### Cascade layers

```
@layer vendor, reset, tokens, base, layout, components, utilities;
```

Specificity stops being a contest: a later layer always wins. One trap to remember —
a stylesheet that arrives as a `<link>` is **unlayered, and unlayered beats every layer**.
That is why the kids page imports Leaflet into `vendor` from a `<style>` block instead of
linking it; as a plain link it silently won over the map styles.

### Typography

| Token | Family | Use |
|---|---|---|
| `--serif` | **Fraunces** (300/400, optical sizing, italic) | All headings. Weight 300, tight tracking, italic `<em>` for the coloured emphasis |
| `--sans` | **Figtree** (400/500/600) | Body, UI, labels |
| `--hand` | **Caveat** (600) | Handwritten notes only — brand sub-line, hero margin notes, portrait caption. Never body copy |

Base size 17px (16px under 640px), line-height 1.6, measure capped at 58–64ch.

### Layout and motion

- `--wrap: 1120px`, gutters via `.wrap`; sections `96px` vertical (72 / 60 at breakpoints).
- `--r: 6px` — one radius everywhere except pills (`999px`).
- Breakpoints: **900px** (grids collapse to one column) and **640px** (type and padding
  step down), plus a 420px tweak. Test every change at all three.
- Motion is restrained: 1–3px lifts, a single draw-on animation for the knot.
  `prefers-reduced-motion` kills all of it — keep that rule intact.

### Accessibility floor

Skip link on every page, visible `:focus-visible` ring, `aria-labelledby` on every
section, `aria-current="page"` in the nav, `aria-hidden` on decorative SVG. These are
not optional extras; a change that drops one is a regression.

---

## 4. Voice and copy

**Site copy is Spanish (Rioplatense, `voseo`) — `lang="es-UY"`. This file and all
repository documentation are English.** Do not mix the two.

- Write the way Flor speaks: direct, warm, no institutional register, no exclamation marks.
- Headings carry the idea; the italic `<em>` fragment carries the turn.
- Name the customer's real problem before offering the service.
- No invented claims. Credentials, years, and institutions must match §1 and the JSON-LD.
- **TeroTalk is one word, two capitals.** Never "Tero Talk" or "Terotalk" in rendered copy;
  the all-lowercase form belongs to the domain and the repo slug only.
- Every CTA is a WhatsApp link with a **pre-filled, context-specific message** — the
  text differs per section so Flor knows what the person was reading.

---

## 5. Quality gate and deploy

Every push to `main` runs `.github/scripts/check.py` before anything is published.
A failure leaves the live site untouched. Run it locally before committing:

```bash
python .github/scripts/check.py
```

It fails the build on:

1. Malformed or unbalanced HTML on any page in `PAGES`.
2. A page over the **60 KB** budget.
3. A local `src`/`href` pointing at a file that is not in the repo.
4. A base64 image inlined into the HTML.
5. A missing, relative, or wrong-domain `og:`/`twitter:` tag.

Add every new page to `PAGES` in that script **and** to `sitemap.xml`.

### Canonical URL

The site is published at `https://barral.dev/terotalk/`. The account serves its Pages
from a custom domain, so a project site lives under that domain instead of at
`barralex.github.io`. The URL appears in **five** places on every page — the canonical
link, `og:url`, `og:image`, `twitter:image` and the JSON-LD `url` — plus `sitemap.xml`
and `robots.txt`. `check.py` compares them against `SITE_BASE` and fails on a mismatch.

`terotalk.com` is the brand's own domain and the site's destination. Moving there is
one commit: add a `CNAME` file holding the bare host, which takes priority over
`SITE_BASE`, and rewrite the URL in all seven places above. Do it only once the DNS
already points at GitHub Pages — a `CNAME` ahead of the records takes the live site
down.

### Commits

`type(scope): short message` — e.g. `feat(kids): add coverage polygon`,
`fix(deploy): pin pages action`, `docs(claude): record palette change`.
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `chore`.

- **Subject line: 10 words, 15 at the absolute limit.** Detail goes in the body.
- **No co-author trailers.** The history stays in one name.
- **Releases are semver tags** — `vMAJOR.MINOR.PATCH`. `feat` moves the minor, `fix`
  moves the patch, a breaking change to the URL structure or the published domain
  moves the major. Tag when a release is worth pointing someone at, not every push.

---

## 6. Definition of done

A change is finished when all of the following are true:

- [ ] `python .github/scripts/check.py` passes.
- [ ] Checked at 1440px, 900px, and 375px.
- [ ] No new hardcoded colour, font, or radius — tokens only.
- [ ] Accessibility floor intact (§3).
- [ ] `sitemap.xml` `lastmod` bumped if copy changed.
- [ ] **`CLAUDE.md` updated if anything in §1–§5 or §7 moved.**
- [ ] Commit message follows the convention.

---

## 7. Open items before launch

Tracked here because they block the site being useful, not because they are bugs.

| Item | Where | Status |
|---|---|---|
| Flor's WhatsApp number | every `wa.me/` link on all three pages | **Blank — highest priority** |
| Price of the English at Work program | `professionals/index.html`, `.amount.tbd` | Placeholder text |
| Real coverage polygon | `kids/index.html`, `zona` array in the map script | Approximated by hand |
| Real `og-cover.png` | `assets/brand/` | Placeholder |
| Testimonials | all pages | None yet — do not invent any |
| Photo of Flor teaching | `assets/` | Only the portrait exists; it stays home-page-only on purpose |
| `terotalk.com` DNS | domain registrar | Not pointed at GitHub Pages; until it is, no `CNAME` file |
| Real personal data in the copy | all pages, JSON-LD, `assets/flor-santos.jpg` | Name, portrait, LinkedIn, schools and zones are still live; they come out and become placeholders in their own commit |

---

<p align="center"><sub>co-assisted by <b>Claude Opus 4.8</b></sub></p>
