# Design

Source of the TeroTalk brand. Every file in `assets/brand/` that carries the mark is generated
from here; edit the source, not the output.

## Contents

| Path | What it is |
|---|---|
| [`logo/build.py`](logo/build.py) | The mark, drawn once; writes the logo SVGs, favicon, seals, page sprites and canvas marks |
| [`logo/banner.html`](logo/banner.html) | Layout of the README banner |
| [`canvas/project/`](canvas/project/) | Source of the design canvas, one `.dc.html` per board |
| [`canvas/export.py`](canvas/export.py) | Renders the boards to PDF, SVG and PNG |
| [`canvas/export/`](canvas/export/) | The rendered boards: [PDF](canvas/export/terotalk-canvas.pdf), SVG for Figma or Penpot, PNG |

## Build

```bash
python design/logo/build.py --export   # mark, sprites, seals, PNGs, banner
python design/canvas/export.py         # canvas boards to PDF, SVG, PNG
```

Requires Python 3 with PyMuPDF, and Chrome or Edge (`CHROME` overrides the path).
