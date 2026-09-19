"""Builds the TeroTalk mark from one source of truth.

The mark is the chibi mascot nesting in the TT speech bubble. This script writes the
three standalone SVGs in assets/brand/ (light, dark, favicon), the <symbol> the pages
carry in their sprite (colours from the --color-logo-* tokens, never hex) and every mark
on the canvas brand board in design/canvas/. Run it after touching any shape below:

    python design/logo/build.py            # rewrite the SVGs and the page sprites
    python design/logo/build.py --export   # also render the PNG exports and the banner
    python design/logo/build.py --symbol   # print the page sprite symbol

--export needs Chrome or Edge; set CHROME to its path if it is not in the default place.
"""
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
BRAND = ROOT / "assets" / "brand"
PAGES = ["index.html", "kids/index.html", "professionals/index.html"]
CANVAS_BOARD = ROOT / "design" / "canvas" / "project" / "Main.dc.html"
CANVAS_HERO = ROOT / "design" / "canvas" / "project" / "Mezcla.dc.html"

VIEWBOX = "4 22 232 232"

# The chibi is drawn in its own 0-120 space (the same drawing as .chibi-tero on the home
# page) and placed so its body sinks into the top of the bubble.
BIRD = "translate(28 10) scale(1.62)"

# (role, element) — role is the logo token the shape takes.
BIRD_SHAPES = [
    ("wing", '<ellipse cx="58" cy="80" rx="31" ry="25"/>'),
    ("ink", '<ellipse cx="64" cy="88" rx="20" ry="15"/>'),
    ("belly", '<path d="M44 66 C54 74 76 74 86 64 C86 72 80 78 70 80 C58 81 48 76 44 66 Z"/>'),
    ("arm", '<path d="M30 76 C36 64 52 64 58 74 C52 86 38 88 30 76 Z"/>'),
    ("ink", '<path d="M52 26 C44 12 30 8 18 12 C30 14 42 20 48 30 Z"/>'),
    ("ink", '<path d="M54 30 C48 22 38 20 30 22 C38 24 46 28 50 34 Z"/>'),
    ("wing", '<circle cx="62" cy="44" r="24"/>'),
    ("ink", '<path d="M84 40 C82 30 74 24 66 25 C72 32 74 42 73 52 C72 60 68 66 64 70 L78 70 C82 62 86 50 84 40 Z"/>'),
    ("beak", '<path d="M84 42 L98 46 L84 50 Z"/>'),
    ("cheek", '<ellipse cx="58" cy="54" rx="5" ry="3"/>'),
    ("eye", '<circle cx="66" cy="40" r="8"/>'),
    ("belly", '<circle cx="68" cy="41" r="4.5"/>'),
    ("ink", '<circle cx="70" cy="39" r="1.6"/>'),
]

# The legs only show where the whole mascot stands on its own, as on the quality seal.
LEGS = '<path d="M50 98 L48 112 M48 112 H42 M48 112 H55"/><path d="M66 98 L68 112 M68 112 H62 M68 112 H75"/>'
SEALS = {"quality-seal.svg": "dark", "quality-seal-dark.svg": "light"}
SEAL_BIRD = "translate(80.4 54.2) scale(.72)"  # above the TeroTalk line at y 157

BUBBLE = "M40 138 H200 C211 138 218 145 218 156 V208 C218 219 211 226 200 226 H90 L60 248 L66 226 H40 C29 226 22 219 22 208 V156 C22 145 29 138 40 138 Z"
LETTER = "M0 4 C0 1 1 0 4 0 H50 C53 0 54 1 54 4 V17 H50.5 C49.5 12.5 47 11 42 11 H34 V60 C34 64 36 65 41.5 65.5 V70 H12.5 V65.5 C18 65 20 64 20 60 V11 H12 C7 11 4.5 12.5 3.5 17 H0 Z"

# Hex values per standalone file. The pages never see these: they use the tokens.
PALETTES = {
    "light": {"ink": "#262940", "wing": "#4A4E6D", "belly": "#FBF8F2", "beak": "#B8323A",
              "bubble": "#262940", "letters": "#F3ECE0", "gap": "#F3ECE0"},
    "dark": {"ink": "#F3ECE0", "wing": "#A9C4DE", "belly": "#262940", "beak": "#E0666D",
             "bubble": "#F3ECE0", "letters": "#262940", "gap": "#262940"},
    "favicon": {"ink": "#F3ECE0", "wing": "#A9C4DE", "belly": "#262940", "beak": "#E0666D",
                "bubble": "#F3ECE0", "letters": "#262940", "gap": "#2D3049"},
}


def paint(role, p):
    """Presentation attributes for a role in a standalone file."""
    if role == "arm":
        return f'fill="{p["belly"]}" stroke="{p["ink"]}" stroke-width="1.5"'
    if role == "eye":
        return f'fill="{p["ink"]}" stroke="{p["beak"]}" stroke-width="1.5"'
    if role == "cheek":
        return f'fill="{p["beak"]}" fill-opacity=".5"'
    return f'fill="{p[role]}"'


def with_attrs(element, attrs):
    return element.replace(" ", f" {attrs} ", 1)


def mark(p=None):
    """The mark's inner markup: classes when p is None, hex attributes otherwise."""
    def attrs(role):
        return f'class="logo__{role}"' if p is None else paint(role, p)

    bird = "".join(with_attrs(el, attrs(role)) for role, el in BIRD_SHAPES)
    if p is None:
        bubble = f'<path class="logo__bubble" stroke-width="7" stroke-linejoin="round" d="{BUBBLE}"/>'
        letters = "".join(
            f'<path class="logo__letters" transform="translate({x} 148)" d="{LETTER}"/>' for x in (56, 130))
    else:
        bubble = (f'<path fill="{p["bubble"]}" stroke="{p["gap"]}" stroke-width="7" '
                  f'stroke-linejoin="round" d="{BUBBLE}"/>')
        letters = "".join(
            f'<path fill="{p["letters"]}" transform="translate({x} 148)" d="{LETTER}"/>' for x in (56, 130))
    return f'<g transform="{BIRD}">{bird}</g>{bubble}{letters}'


def bird(p):
    return "".join(with_attrs(el, paint(role, p)) for role, el in BIRD_SHAPES)


def standing(p):
    """The whole mascot on its feet, legs behind the body."""
    legs = (f'<g fill="none" stroke="{p["beak"]}" stroke-width="3" stroke-linecap="round" '
            f'stroke-linejoin="round">{LEGS}</g>')
    return legs + bird(p)


def symbol():
    return f'<symbol id="logo" viewBox="{VIEWBOX}">{mark()}</symbol>'


def write_files():
    ns = 'xmlns="http://www.w3.org/2000/svg"'
    for name, key in (("logo.svg", "light"), ("logo-dark.svg", "dark")):
        (BRAND / name).write_text(f'<svg {ns} viewBox="{VIEWBOX}">{mark(PALETTES[key])}</svg>\n', encoding="utf-8")
    fav = PALETTES["favicon"]
    (BRAND / "favicon.svg").write_text(
        f'<svg {ns} viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{fav["gap"]}"/>'
        f'<g transform="translate(3 -3.5) scale(.25)">{mark(fav)}</g></svg>\n', encoding="utf-8")
    for page in PAGES:
        path = ROOT / page
        html = path.read_text(encoding="utf-8")
        html, n = re.subn(r'<symbol id="logo".*?</symbol>', lambda _: symbol(), html, flags=re.S)
        assert n == 1, page
        path.write_text(html, encoding="utf-8", newline="")
    sync_seals()
    sync_canvas()


def sync_seals():
    """Stand the mascot inside the dashed ring of both quality seals."""
    for name, key in SEALS.items():
        path = BRAND / name
        svg = path.read_text(encoding="utf-8")
        svg, n = re.subn(r'<g transform="[^"]*"( data-mascot="")?>.*</g>(\s*<text x="120" y="157")',
                         lambda m: f'<g transform="{SEAL_BIRD}" data-mascot="">{standing(PALETTES[key])}</g>{m.group(2)}',
                         svg, flags=re.S)
        assert n == 1, name
        path.write_text(svg, encoding="utf-8", newline="")


def sync_canvas():
    """Redraw every mark on the canvas brand board with the palette of the tile it sits on."""
    board = CANVAS_BOARD.read_text(encoding="utf-8")

    def redraw(m):
        on_sand = "#F3ECE0" in board[max(0, m.start() - 200):m.start()]
        return m.group(1) + mark(PALETTES["light" if on_sand else "favicon"]) + "</svg>"

    board, n = re.subn(r'(<svg viewBox="4 22 232 232"[^>]*>).*?</svg>', redraw, board, flags=re.S)
    assert n, "no marks found on the canvas board"
    CANVAS_BOARD.write_text(board, encoding="utf-8", newline="")

    # The hero board lands the mark at the end of the thread, on navy.
    hero = CANVAS_HERO.read_text(encoding="utf-8")
    hero, n = re.subn(r'(<g transform="translate\(1238 128\) scale\(\.56\)">).*?(</g></g>)',
                      lambda m: m.group(1) + mark(PALETTES["favicon"]) + m.group(2), hero, flags=re.S)
    assert n == 1, "no mark found on the hero board"
    CANVAS_HERO.write_text(hero, encoding="utf-8", newline="")


CHROMES = [os.environ.get("CHROME", ""),
           r"C:\Program Files\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "google-chrome", "chromium"]


def shoot(url, out, width, height, transparent=False):
    chrome = next(c for c in CHROMES if c and (os.path.exists(c) or "/" not in c and "\\" not in c))
    args = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
            f"--window-size={width},{height}", "--virtual-time-budget=3000", f"--screenshot={out}", url]
    if transparent:
        args.insert(-1, "--default-background-color=00000000")
    subprocess.run(args, check=True, capture_output=True)


def export():
    """1024 px PNGs of both logos and both seals on transparent, and the README banner."""
    with tempfile.TemporaryDirectory() as tmp:
        for svg in ("logo", "logo-dark"):
            page = pathlib.Path(tmp) / f"{svg}.html"
            page.write_text(f'<style>html,body{{margin:0;background:transparent}}img{{display:block;width:1024px;'
                            f'height:1024px}}</style><img src="{(BRAND / (svg + ".svg")).as_uri()}">', encoding="utf-8")
            shoot(page.as_uri(), str(BRAND / f"{svg}.png"), 1024, 1024, transparent=True)
    with tempfile.TemporaryDirectory() as tmp:
        for svg in ("quality-seal", "quality-seal-dark"):
            page = pathlib.Path(tmp) / f"{svg}.html"
            page.write_text(f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@600'
                            f'&display=swap"><style>html,body{{margin:0;background:transparent}}svg{{display:block;'
                            f'width:1024px;height:1024px}}</style>{(BRAND / (svg + ".svg")).read_text(encoding="utf-8")}',
                            encoding="utf-8")
            shoot(page.as_uri(), str(BRAND / f"{svg}.png"), 1024, 1024, transparent=True)
    shoot((ROOT / "design" / "logo" / "banner.html").as_uri(), str(BRAND / "banner.png"), 1800, 450)


if __name__ == "__main__":
    if "--symbol" in sys.argv:
        print(symbol())
    else:
        write_files()
        if "--export" in sys.argv:
            export()
        print("wrote the brand SVGs and the sprite in", len(PAGES), "pages" + (", plus PNGs" if "--export" in sys.argv else ""))
