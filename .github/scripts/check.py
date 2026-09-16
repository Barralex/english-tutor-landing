#!/usr/bin/env python3
"""Pre-deploy checks for the page.

Runs before anything reaches GitHub Pages. A failure here leaves the
published site untouched instead of replacing it with a broken one.
"""

import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

PAGE = "index.html"
MAX_PAGE_BYTES = 60 * 1024

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
    """Where the page will live. A CNAME wins, otherwise the Pages URL."""
    if os.path.exists("CNAME"):
        host = open("CNAME", encoding="utf-8").read().strip()
        if host:
            return "https://%s/" % host
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
    if not os.path.exists(PAGE):
        fail("%s is missing" % PAGE)
        report()
        return

    raw = open(PAGE, "rb").read()
    size = len(raw)
    if size > MAX_PAGE_BYTES:
        fail("%s is %d KB, over the %d KB budget. An image pasted back in as "
             "base64 is the usual cause; move it to assets/ instead."
             % (PAGE, size // 1024, MAX_PAGE_BYTES // 1024))
    else:
        note("%s is %d KB of the %d KB budget" % (PAGE, size // 1024, MAX_PAGE_BYTES // 1024))

    html = raw.decode("utf-8")
    doc = Doc()
    doc.feed(html)
    doc.close()

    for msg in doc.unbalanced:
        fail("Malformed HTML: %s" % msg)
    for tag, line in doc.stack:
        fail("Malformed HTML: <%s> opened on line %d is never closed" % (tag, line))

    base = expected_base()
    if base:
        note("expected base is %s" % base)

    # Local files that the page points at have to exist.
    checked = 0
    for tag, attr, url, line in doc.refs:
        low = url.lower()
        if low.startswith("data:image"):
            fail("Line %d: <%s> carries an inline base64 image. Put the file in "
                 "assets/ and reference it by path." % (line, tag))
            continue
        if low.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#", "//")):
            continue
        target = url.split("?")[0].split("#")[0]
        if not target:
            continue
        if not os.path.exists(target):
            fail("Line %d: <%s %s=\"%s\"> points at a file that is not in the repo"
                 % (line, tag, attr, url))
        else:
            checked += 1
    note("%d local references resolve" % checked)

    # Social preview tags decide what a shared link looks like, and they
    # break silently, so they get checked too.
    for key in ("og:url", "og:image", "og:title", "og:description", "twitter:image"):
        if not doc.meta.get(key):
            fail("Meta tag %s is missing or empty" % key)

    for key in ("og:url", "og:image", "twitter:image"):
        url = doc.meta.get(key, "")
        if not url:
            continue
        if not url.startswith("https://"):
            fail("Meta tag %s is \"%s\". Scrapers need an absolute https URL, "
                 "not a relative path." % (key, url))
            continue
        if base and not url.startswith(base):
            fail("Meta tag %s points at %s but the site is published at %s. "
                 "Update the tag, or add a CNAME if the domain moved."
                 % (key, url, base))

    for key in ("og:image", "twitter:image"):
        url = doc.meta.get(key, "")
        if url.startswith("https://"):
            rel = local_path(url, base)
            if rel and not os.path.exists(rel):
                fail("Meta tag %s points at %s, and %s is not in the repo. "
                     "The link preview would show a broken image." % (key, url, rel))

    report()


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
