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
the person behind it and stays visible everywhere. The lockup is the logo and the
word *TeroTalk* alone; Flor carries the rest — "Sobre Flor" in the nav, and the home
page explains the name once, in her voice, in the "Quién enseña" section. The brand never replaces the person:
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
establishes who Flor is, then sends each visitor down one of two paths. The
section is a sentence the visitor finishes — *Busco inglés para (mi hijo | mí)*, a segmented
pill whose active option takes the colours of its strip — followed by one full-width strip per service: one headline,
one line of facts, a scene, and an arrow in a ring instead of a button. No eyebrow, no sub-line: the
question is the whole head, kept short. No cards, no bullet lists, no
pitch; the selling happens on the service page. A visitor
should reach the right page in one click and never see the other offer's pricing or
objections.

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
index.html                     Home: brand, the two paths, who Flor is
kids/index.html                Teacher Flor: in-home lessons, coverage map
professionals/index.html       English at Work: the 6-hour program
assets/css/site.css            Entry: layer order, imports, reset, base, layout, utilities
assets/css/tokens.css          Primitives, semantic aliases, spacing and type scales
assets/css/components.css      Every component block, BEM
assets/brand/favicon.svg       The logo on a navy tile
assets/brand/logo.svg          Logo: the chibi mascot nesting in a TT speech bubble (logo-dark.svg for navy)
assets/brand/logo.png          1024px exports of the logo, light and dark, for use outside the site
assets/brand/quality-seal.svg  Quality seal with the mascot standing, not used on the site yet (see §7); PNG exports beside it
assets/brand/og-cover.png      Link preview image (PLACEHOLDER — see §7)
assets/brand/banner.png        README header, repo only
assets/brand/preview.jpg       README screenshot, repo only
assets/brand/signature.svg     README footer credit, repo only
assets/flor-santos.jpg         Portrait, home page only
robots.txt                     Crawler rules
LICENSE                        All rights reserved; brand, copy and photos excluded
sitemap.xml                    Three URLs; bump lastmod when copy changes
.github/scripts/check.py       Pre-deploy gate (see §5)
.github/scripts/stamp.sh       Deploy-time cache busting (see §5)
.github/workflows/deploy.yml   GitHub Pages deploy
design/logo/build.py           Source of the mark: writes every logo SVG, the sprites, seals and canvas marks
design/logo/banner.html        README banner layout (build.py --export renders it)
design/canvas/project/         Source of the design canvas, one .dc.html per board
design/README.md               How the brand source and the canvas are kept
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
  each page (`#logo`, `#knot`, `#arrow`, `#chat`; the home page adds `#flag-uy` and `#globe`) and are used via `<use href="#id">`. Add new
  icons to the sprite; never paste a base64 image into the HTML (`check.py` fails the build).
- **Only two external runtime dependencies**, both from a CDN: Google Fonts in every
  `<head>`, and Leaflet 1.9.4 for the coverage map on the kids page. Adding a third
  needs a real justification.
- **The mark is generated, never hand-edited.** The logo is the mascot: the same chibi tero as
  `.chibi-tero`, nesting in the TT bubble. Its shapes and palettes live in `design/logo/build.py`,
  which rewrites the `#logo` symbol in all three pages, `logo*.svg`, `favicon.svg`, both quality
  seals and every mark on the canvas boards. Change it there and run the script; `--export`
  also renders the PNGs and `banner.png`. The logo appears where the brand signs (header,
  footer, the hero landing, the kids roof, the seam medallion); the full mascot with legs
  appears only where it acts (`.chibi-tero`) and on the seals.
- **The design canvas lives in the repo.** `design/canvas/project/` is the source of the canvas
  (https://claude.ai/artifact/4uaVm4QbSzWGwgbjSvYjDe). Edit the boards there, publish the folder,
  and commit both in the same change. A brand change that leaves the canvas behind is incomplete.
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
| `--color-surface` | `--navy-800` `#2D3049` | Page background (the README banner navy) |
| `--color-surface-raised` | `--navy-700` `#363A58` | Cards, chips, raised panels |
| `--color-surface-sunken` | `--navy-900` `#262940` | Recessed panels |
| `--color-text` | `--sand-100` `#F3ECE0` | Body and headings |
| `--color-text-muted` | `--lilac-200` `#D9D8E5` | Secondary text |
| `--color-accent` | `--red-200` `#F08A90` | Emphasis, focus ring, italic heading turns |
| `--color-accent-strong` | `--red-700` `#9A2830` | CTA hover only |
| `--color-brand` | `--blue-300` `#A9C4DE` | Eyebrows, handwriting, threads |
| `--color-border` | sand at 14% | Every hairline |
| `--color-positive` | `--green-300` `#8FC1A9` | Check icons in lists |
| `--color-flag-*` | `--white`, `--uy-blue`, `--uy-sun` | The Uruguay flag icon only |
| `--color-map-area` / `--color-map-base` | `--green-700` / `--red-600` | Coverage map only |
| `--color-logo-*` | sand, `--blue-300`, `--red-300` `#E0666D` | The `#logo` symbol and the red *Talk* of the wordmark; `--color-logo-gap` is the ring that separates the bird from the bubble and must match the background |

**The site is dark, broken by sand.** The base is `--navy-800`. `.band--soft` is the
counterpoint: it rebinds every semantic token to the light set (`--sand-100` surface,
`--navy-900` text, `--red-600` accent, `--slate-600` brand) so pages alternate navy and sand.
`.band--dark`, `.page-hero--dark` and `.site-footer` sink a section to `--navy-900`. The kids
strip (`.path--kids`, `--blue-300`) stays light blue and the work strip (`.path--work`) sinks to
`--navy-900`, so the two paths read as two businesses. Each strip rebinds the semantic tokens
on itself, like a band. Primary CTAs stay `--red-600` with white text (5.9:1); `--red-200` is
the accent for text because `--red-600` fails contrast on navy. `.btn--solid` is the inverse
button: text colour as background, surface colour as text.

**Dark sections never override a component.** Every section rebinds the semantic tokens on
itself, so every component inside adapts without a single descendant selector. Accent
discipline: red is the only saturated colour and it means "act here". On every navy surface
the accent is `--red-200`; on sand it is `--red-600`. Blue stays in its lane as
`--color-brand` (eyebrows, threads, handwriting) and never carries the italic turn.

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

The wordmark is the one exception to weight 300: *Tero* in Fraunces 650 with `SOFT 100` and
`WONK 1`, *Talk* in italic 500 in the logo red (`.brand__name`, `.brand__talk`). The
Google Fonts link loads Fraunces as a variable range with both axes for that reason.

Base size 17px (16px under 640px), line-height 1.6, measure capped at 58–64ch.

### Layout and motion

- `--wrap: 1120px`, gutters via `.wrap`; sections `96px` vertical (72 / 60 at breakpoints).
- `--r: 6px` — one radius everywhere except pills (`999px`).
- Breakpoints: **900px** (grids collapse to one column) and **640px** (type and padding
  step down), plus a 420px tweak. Test every change at all three.
- Motion is restrained: 1–3px lifts, and one story told once — the home hero.
  `prefers-reduced-motion` kills all of it — keep that rule intact.
- **The home hero animation** (`.hero-anim` in `index.html`, keyframes `hero-*` in
  `components.css`) is one 11 s loop on a shared clock. A thinking figure, doubts escaping the
  tangle, the thread drawing itself, English phrases growing in confidence (*Hi, → I think… →
  let me explain. → here's the plan. → Deal.*) and the tero landing with confetti. Under it, a
  deliberately quieter second layer: one Spanish word at a time (*me trabo, me animo, me sale,
  me suelto, ya casi, me salió*), small, muted, centred under its English partner, entering
  ~110 ms after it and leaving when the next arrives. Keep that hierarchy: the Spanish layer
  never competes with the thread. Under 640px the details (`.hero-anim__detail`) hide; with
  reduced motion the in-between pieces (`.hero-anim__transient`) hide and the final frame
  shows still. The SVG carries no hex and no `style` — colours are `hero-anim__ink--*` /
  `__line--*` token classes. The keyframe percentages were set as one timeline; retime them
  together, never one in isolation, or the two layers drift out of sync.
- **The two paths** (`.paths` in `index.html`, keyframes `path-*`, `ride-*`, `call-*`
  in `components.css`) run on the hero's 11 s clock. The picker never moves on its own — a
  selector that changes by itself reads as broken. It is a segmented control: one option is
  always active — on a thumb in its strip's colours, 10 % larger — and the other sits in grey.
  *mi hijo* is active at rest; hovering or focusing *mí* (or the work strip) slides the thumb
  across and turns it navy, and the matching strip sweeps. The picker drives the strips: the
  active one scales its content to 105 % and the other goes grayscale at 55 % opacity. That
  runs only under `(hover:hover)` — on touch nothing hovers and a grey strip reads as disabled.
  The scenes sit in a 330px column (255px at 900px and 640px). The strips are tall (64px of
  padding, 48 / 40 at the breakpoints) and the seam between them is a wave, not a rule: the work
  strip rides up by twice `--seam` (40px, 20px under 640px) and a CSS mask cuts its top edge to
  the curve, so its background, sweep and grey state follow it. A sand medallion with the logo
  (`.paths__medal`) sits where the wave crosses the old boundary, outside both strips' filters so
  it never goes grey. The two mask layers overlap by 1px; butting them leaves a hairline. The ring arrow nudges forward
  at 45 %, when the tero lands; on hover the ring fills with the accent and the arrow passes
  through and comes back. The kids scene: Flor's car drives to the house (3–38 %) and the tero lands on the roof
  at 42 %, with the hero's tero. The work scene: the call bubble says *Hi,* → *let me explain.* →
  *Deal.* in step with the hero's phrases while the voice bars grow. The CSS base state of every
  piece is the final frame, so reduced motion shows the car parked and *Deal.* on screen. The
  hover sweep on a strip is a `clip-path`, not `scaleX(0)`: a zero-scaled layer leaves a
  hairline at the strip edges in Chrome.
- **Page transitions** are native cross-document View Transitions (`@view-transition` in
  `site.css`), no JavaScript: the header is pinned (`view-transition-name:site-header`), the
  content fades with an 8px drift, ~300 ms. Only same-origin navigations over http(s) animate —
  opening the files straight from disk shows none. Off under reduced motion; unsupported
  browsers simply navigate.
- **The chibi tero** (`.chibi-tero`, next to the home CTAs) runs on the same 11 s clock as the
  hero: it hops forward (squash and stretch, `--chibi-step` per hop) while the thread untangles, and when the tero lands it
  swaps its folded wing for two raised ones and a bubble says *I did it!* — English on purpose,
  it is the student speaking. Logo tokens only, so it matches the header. Blink and crest run
  on their own short loops. Reduced motion leaves it standing still, no bubble.

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

### Cache busting

GitHub Pages serves every file with `max-age=600` and the asset names never change, so
after a deploy a browser that already holds `site.css` keeps rendering the old styles —
exactly what happens on the tablet used to show clients progress. The deploy job runs
`.github/scripts/stamp.sh` before uploading: every local `href`/`src` under `assets/` in
the pages, and the two `@import`s in `site.css`, get `?v=<short commit>` in the published
copy only. The repository keeps clean URLs; nobody bumps a version by hand.

- Link every new asset with a plain relative path under `assets/`; the stamp picks it up.
  A new page goes in the `pages` list of `stamp.sh` as well as `PAGES` in `check.py`.
- A new stylesheet `@import` must keep the `url("name.css")` form or it will not be stamped.
- The script fails the deploy if it stamps fewer than five references, so a markup change
  that breaks the pattern cannot silently switch cache busting off.
- The HTML itself still carries the 10-minute cache. When showing a client a change right
  after a deploy, open the page with any query string (`/?v=2`) to fetch fresh HTML;
  the stamped assets follow from there.

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

- **Subject line only, never a body.** A commit is one `type(scope): short message`
  line and nothing after it. 10 words, 15 at the absolute limit. If the change will not
  fit, split the commit; detail that needs recording belongs in this file, not the history.
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
- [ ] **README images match the live site.** If the home page changed visibly, regenerate
      `assets/brand/preview.jpg` (1860×1050: the desktop page in a browser frame and the
      phone beside it, animations frozen on the final frame). If the logo, wordmark or
      tagline changed, run `python design/logo/build.py --export` for the banner and PNGs.
      Same commit as the change.
- [ ] **Canvas in sync.** A brand change updates `design/canvas/` and is published to the canvas.
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
| Quality seal | `assets/brand/quality-seal.*` | Drawn, not placed. Its SVG text needs Fraunces and Figtree loaded; outline it before using it off-site |
| Testimonials | all pages | None yet — do not invent any |
| Photo of Flor teaching | `assets/` | Only the portrait exists; it stays home-page-only on purpose |
| `terotalk.com` DNS | domain registrar | Not pointed at GitHub Pages; until it is, no `CNAME` file |
| Real personal data in the copy | all pages, JSON-LD, `assets/flor-santos.jpg` | Name, portrait, LinkedIn, schools and zones are still live; they come out and become placeholders in their own commit |

---

<p align="center"><sub>co-assisted by <b>Claude Opus 5</b></sub></p>
