# Design source

The brand is kept as source, not as exported files. Everything under `assets/brand/` that
carries the mark is generated from here, so the site, the README images and the design
canvas can never drift apart.

```
design/logo/build.py          One source for the mark: shapes, palettes, every output
design/logo/banner.html       README header layout, rendered to assets/brand/banner.png
design/canvas/project/        The design canvas, one file per board
  canvas.json                 Board layout: position, size, grid guides
  Main.dc.html                01 · Brand sheet: logo on navy and sand, favicon at 1:1
  Mezcla.dc.html              02 · Hero: the animated thread
```

## The mark

The mark is the site's mascot, a chibi southern lapwing (*tero*), nesting in the TT speech
bubble. It is drawn once, in `build.py`, and written out five ways:

| Output | Where it lives | Colours |
|---|---|---|
| `<symbol id="logo">` | The sprite at the top of every page | `--color-logo-*` tokens, no hex |
| `logo.svg` / `logo-dark.svg` | `assets/brand/`, for use outside the site | Sand and navy palettes |
| `favicon.svg` | `assets/brand/`, 64 px tile, 14 px radius | Navy tile |
| `quality-seal*.svg` | `assets/brand/`, the mascot standing, legs included | Navy and sand |
| Canvas boards | `design/canvas/project/*.dc.html` | Per tile, picked from its background |

```bash
python design/logo/build.py            # SVGs, page sprites, seals, canvas boards
python design/logo/build.py --export   # plus the 1024 px PNGs and the README banner
```

`--export` drives headless Chrome or Edge; set `CHROME` if neither is in its default place.
Change a shape or a colour in `build.py`, run it, and commit what it rewrote in the same commit.

## The canvas

The canvas is a design file on claude.ai, and this folder is its source. The layout follows
a 1440 px board on a 12-column grid (80 px margins, 24 px gutter), an 8 px spacing scale and
numbered sections, each with a title, a one-line purpose and captioned specimens that name
their token or hex. Explorations go in their own boards below the brand sheet, one column,
and are removed once superseded.

Edit the boards here, then publish the folder to the canvas. The repository copy is the one
that is reviewed and versioned; the canvas is where it is looked at.
