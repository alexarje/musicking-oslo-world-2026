"""Wrap slides.html in the school deck's page (index-school.html) to give index.html.

The head (styles) and tail (scripts, footer) come from the 30 October school deck; only the slides
are this deck's. Edit slides.html, then run .venv/bin/python tools/assemble.py from reveal/.
"""
from pathlib import Path

from palette import MISHMASH

page = Path("index-school.html").read_text(encoding="utf-8")
head, rest = page.split('<div class="slides">', 1)
tail = rest[rest.index('\n</div>\n</div>\n\n<div class="footer">'):]
head = head.replace('<html lang="nb">', '<html lang="en">').replace(
    "<title>Verden i dag og verden i morgen</title>", "<title>Musicking Technology</title>")
# The sunrise palette replaces the MishMash colours in the page styles.
for old, new in MISHMASH.items():
    head = head.replace(old, new)
# Not a MishMash talk: drop the school deck's mishmash.no footer.
tail = tail.replace('<div class="footer">mishmash.no</div>\n', "", 1)
Path("index.html").write_text(head + '<div class="slides">\n' + Path("slides.html").read_text(encoding="utf-8")
                              + tail, encoding="utf-8")
print("wrote index.html")
