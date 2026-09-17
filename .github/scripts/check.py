#!/usr/bin/env python3
"""Pre-deploy checks for every page of the site.

Runs before anything reaches GitHub Pages. A failure here leaves the
published site untouched instead of replacing it with a broken one.
"""

import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

PAGES = ["index.html", "kids/index.html", "professionals/index.html"]
MAX_PAGE_BYTES = 60 * 1024

# The account serves its Pages from a custom domain, so a project site
# lives at barral.dev/<repo>/ and not at <owner>.github.io/<repo>/.
# A CNAME file still wins, for the day this site gets its own domain.
SITE_BASE = "https://barral.dev/english-tutor-landing/"

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

problems = []
notes = []


def fail(msg):
    problems.append(msg)


def note(msg):
    notes.append(msg)


class Doc(HTMLParser):
    """Collects tag nesting, local references and meta tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.refs = []
        self.meta = {}
        self.unbalanced = []

    def handle_startendtag(self, tag, attrs):
        self.collect(tag, attrs)

    def handle_starttag(self, tag, attrs):
        self.collect(tag, attrs)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif any(t == tag for t, _ in self.stack):
            while self.stack and self.stack[-1][0] != tag:
                orphan, line = self.stack.pop()
                self.unbalanced.append("<%s> opened on line %d is never closed" % (orphan, line))
            if self.stack:
                self.stack.pop()
        else:
            self.unbalanced.append("</%s> on line %d closes nothing" % (tag, self.getpos()[0]))

    def collect(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            key = a.get("property") or a.get("name")
            if key:
                self.meta[key] = a.get("content", "")
        for attr in ("src", "href"):
            if a.get(attr):
                self.refs.append((tag, attr, a[attr], self.getpos()[0]))


def expected_base():
    """Where the page will live. A CNAME wins, then SITE_BASE."""
    if os.path.exists("CNAME"):
        host = open("CNAME", encoding="utf-8").read().strip()
        if host:
            return "https://%s/" % host
    if SITE_BASE:
        return SITE_BASE
    slug = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in slug:
        owner, repo = slug.split("/", 1)
        return "https://%s.github.io/%s/" % (owner.lower(), repo)
    return ""


def local_path(url, base):
    """Map a URL that should live in this repo to a path on disk."""
    if url.startswith(base) and base:
        return url[len(base):].split("?")[0].split("#")[0]
    path = urlparse(url).path.lstrip("/")
    parts = [p for p in path.split("/") if p]
    slug = os.environ.get("GITHUB_REPOSITORY", "")
    repo = slug.split("/")[-1] if slug else os.path.basename(os.getcwd())
    if parts and repo and parts[0] == repo:
        parts = parts[1:]
    return "/".join(parts)


def main():
    for page in PAGES:
        check_page(page)
    report()


def check_page(page):
    if not os.path.exists(page):
        fail("%s is missing" % page)
        return

    raw = open(page, "rb").read()
    size = len(raw)
    if size > MAX_PAGE_BYTES:
        fail("%s is %d KB, over the %d KB budget. An image pasted back in as "
             "base64 is the usual cause; move it to assets/ instead."
             % (page, size // 1024, MAX_PAGE_BYTES // 1024))
    else:
        note("%s is %d KB of the %d KB budget" % (page, size // 1024, MAX_PAGE_BYTES // 1024))

    html = raw.decode("utf-8")
    doc = Doc()
    doc.feed(html)
    doc.close()

    for msg in doc.unbalanced:
        fail("%s: malformed HTML: %s" % (page, msg))
    for tag, line in doc.stack:
        fail("%s: malformed HTML: <%s> opened on line %d is never closed" % (page, tag, line))

    base = expected_base()
    folder = os.path.dirname(page)

    # Local files that the page points at have to exist. Paths are
    # relative to the page, and a folder link means its index.html.
    checked = 0
    for tag, attr, url, line in doc.refs:
        low = url.lower()
        if low.startswith("data:image"):
            fail("%s line %d: <%s> carries an inline base64 image. Put the file in "
                 "assets/ and reference it by path." % (page, line, tag))
            continue
        if low.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#", "//")):
            continue
        target = url.split("?")[0].split("#")[0]
        if not target:
            continue
        path = os.path.normpath(os.path.join(folder, target))
        if target.endswith("/") or os.path.isdir(path):
            path = os.path.join(path, "index.html")
        if not os.path.exists(path):
            fail("%s line %d: <%s %s=\"%s\"> points at a file that is not in the repo"
                 % (page, line, tag, attr, url))
        else:
            checked += 1
    note("%s: %d local references resolve" % (page, checked))

    # Social preview tags decide what a shared link looks like, and they
    # break silently, so they get checked too.
    for key in ("og:url", "og:image", "og:title", "og:description", "twitter:image"):
        if not doc.meta.get(key):
            fail("%s: meta tag %s is missing or empty" % (page, key))

    for key in ("og:url", "og:image", "twitter:image"):
        url = doc.meta.get(key, "")
        if not url:
            continue
        if not url.startswith("https://"):
            fail("%s: meta tag %s is \"%s\". Scrapers need an absolute https URL, "
                 "not a relative path." % (page, key, url))
            continue
        if base and not url.startswith(base):
            fail("%s: meta tag %s points at %s but the site is published at %s. "
                 "Update the tag, or add a CNAME if the domain moved."
                 % (page, key, url, base))

    for key in ("og:image", "twitter:image"):
        url = doc.meta.get(key, "")
        if url.startswith("https://"):
            rel = local_path(url, base)
            if rel and not os.path.exists(rel):
                fail("%s: meta tag %s points at %s, and %s is not in the repo. "
                     "The link preview would show a broken image." % (page, key, url, rel))


def report():
    for n in notes:
        print("ok    %s" % n)
    if not problems:
        print("\nAll checks passed. Publishing.")
        return
    print("")
    for p in problems:
        print("FAIL  %s" % p)
    print("\n%d problem(s). The published page was left untouched." % len(problems))
    sys.exit(1)


main()
