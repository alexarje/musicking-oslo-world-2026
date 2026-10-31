"""English figures for the Oslo World musicking deck, as stacked SVG layers for click builds.

All quadrant figures share one canvas, so any of them can be stacked on another. The quadrant
follows Sound Actions (MIT Press, 2022) and the school deck of 30 October 2026
(2026-10-30-Musikk i skolen/presentation/tools/make_quadrant.py): Understand and Experience on
top, Create and Perform below, arrows Create -> Perform -> Experience -> Understand -> Create.
The 4E and social figures are the school deck's make_4e.py and make_sosial.py in English.

Writes images/fig-q-*.svg, fig-4e-*.svg, fig-social-*.svg and fig-process-*.svg.
Run from presentation/reveal/ with .venv/bin/python tools/make_figs.py.
"""
import math
from itertools import combinations
from pathlib import Path

from palette import INK, SKY, CORAL, SUN, MINT

GREY, PALE = "#b8b8c0", "#eeeef2"
# The school deck's colour names, now drawn in the sunrise palette (tools/palette.py).
GREEN, PURPLE, BLUE, PINK = SUN, MINT, SKY, CORAL
FD = "font-family:'Roboto Condensed',Arial,sans-serif;font-weight:700"
FB = "font-family:Inter,Arial,sans-serif"
OUT = Path("images")


def svg(w, h, body, x0=0, y0=0):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}">'
            f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>{body}</svg>')


def text(x, y, lines, size, fill=INK, style=FD, anchor="middle"):
    lines = [lines] if isinstance(lines, str) else lines
    out = ""
    for i, t in enumerate(lines):
        dy = (i - (len(lines) - 1) / 2) * size * 1.15
        out += (f'<text x="{x:.0f}" y="{y + size * 0.35 + dy:.0f}" text-anchor="{anchor}" font-size="{size}" '
                f'fill="{fill}" style="{style}">{t}</text>')
    return out


def write(name, body, size):
    (OUT / name).write_text(svg(*size, body), encoding="utf-8")


# ---- the quadrant -------------------------------------------------------------------------------
QW, QH, R = 1800, 1000, 165
C = {"Understand": (620, 270), "Experience": (1180, 270), "Create": (620, 730), "Perform": (1180, 730)}
FILL = {"Understand": BLUE, "Experience": PINK, "Create": GREEN, "Perform": PURPLE}
CYCLE = [("Create", "Perform"), ("Perform", "Experience"), ("Experience", "Understand"), ("Understand", "Create")]


def edge(p, q, pad=(R + 8, R + 8), dashed=False, arrow=True, width=6, colour=INK, both=False):
    (x1, y1), (x2, y2) = p, q
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    dash = ' stroke-dasharray="14 12"' if dashed else ""
    mk = ' marker-end="url(#a)"' if arrow else ""
    mk += ' marker-start="url(#a)"' if both else ""
    return (f'<line x1="{x1 + ux * pad[0]:.1f}" y1="{y1 + uy * pad[0]:.1f}" x2="{x2 - ux * pad[1]:.1f}" '
            f'y2="{y2 - uy * pad[1]:.1f}" stroke="{colour}" stroke-width="{width}"{dash}{mk}/>')


def node(k, fill=None, grey=False):
    x, y = C[k]
    f, line, col = (PALE, GREY, GREY) if grey else (fill or FILL[k], INK, INK)
    return (f'<circle cx="{x}" cy="{y}" r="{R}" fill="{f}" stroke="{line}" stroke-width="5"/>'
            + text(x, y, k, 50, fill=col))


def full(grey=(), arrows=CYCLE):
    return "".join(edge(C[a], C[b]) for a, b in arrows) + "".join(node(k, grey=k in grey) for k in C)


def qwrite(name, body):
    write(f"fig-q-{name}.svg", body, (QW, QH))


qwrite("0", "")
qwrite("word", text(QW / 2, QH / 2, "Musicking", 58))
for i, (k, prev) in enumerate([("Create", None), ("Perform", "Create"), ("Experience", "Perform"),
                               ("Understand", "Experience")], 1):
    body = (edge(C[prev], C[k]) if prev else "") + (edge(C["Understand"], C["Create"]) if k == "Understand" else "")
    qwrite(f"c{i}", body + node(k))
qwrite("full", full())

# The two axes: time across the top, creation to experience up the side.
mid = (C["Understand"][0] + C["Experience"][0]) / 2
qwrite("axis-time",
       text(C["Understand"][0], 45, "Out of time", 44) + text(C["Experience"][0], 45, "Real time", 44)
       + f'<line x1="{mid}" y1="20" x2="{mid}" y2="{QH - 20}" stroke="{INK}" stroke-width="4" stroke-dasharray="14 12"/>')
qwrite("axis-mode",
       f'<line x1="250" y1="{C["Create"][1] + 120}" x2="250" y2="{C["Understand"][1] - 120}" stroke="{INK}" '
       f'stroke-width="7" marker-start="url(#a)" marker-end="url(#a)"/>'
       + text(250, C["Understand"][1] - 170, "Experience", 40) + text(250, C["Create"][1] + 170, "Creation", 40))

# Who musicks: a few roles beside each corner, then the scene in the middle.
ROLES = {"Create": ["composer", "producer", "instrument maker"], "Perform": ["musician", "DJ", "dancer"],
         "Experience": ["audience", "listener", "dancer"], "Understand": ["critic", "researcher", "student"]}
body = ""
for k, who in ROLES.items():
    x, y = C[k]
    left = x < QW / 2
    body += text(x - R - 30 if left else x + R + 30, y, who, 36, style=FB, anchor="end" if left else "start")
qwrite("roles", body)
cx, cy, m = QW / 2, QH / 2, 120
qwrite("scene",
       f'<path d="M{cx} {cy - m} L{cx + m} {cy} L{cx} {cy + m} L{cx - m} {cy} Z" fill="#ffffff" stroke="{INK}" stroke-width="5"/>'
       + text(cx, cy, "Scene", 36)
       + text(cx, QH - 25, "organisers, labels, sound engineers, the people who put up the posters", 32, style=FB))

# Streaming keeps one corner; generative AI skips performing and the scene.
qwrite("streaming", "".join(node(k, grey=k != "Experience") for k in C))
qwrite("genai", edge(C["Understand"], C["Create"]) + edge(C["Create"], C["Experience"])
       + "".join(node(k, grey=k == "Perform") for k in C))


def middle(label, size):
    s = "".join(edge((cx, cy), C[k], pad=(118, R + 6), dashed=True, arrow=False, width=5) for k in C)
    return (s + f'<circle cx="{cx}" cy="{cy}" r="110" fill="{INK}"/>'
            + text(cx, cy, label, size, fill="#ffffff"))


qwrite("ai", middle("AI", 70))
qwrite("tech", middle("Technology", 36))

# Today: every corner connects to every other, sides first, then the diagonals.
qwrite("nodes", "".join(node(k) for k in C))
qwrite("links-sides", "".join(edge(C[a], C[b], both=True) for a, b in CYCLE))
qwrite("links-diag", edge(C["Create"], C["Experience"], both=True) + edge(C["Understand"], C["Perform"], both=True))

# ---- product and process ------------------------------------------------------------------------
PW, PH = 1800, 960
px, py, pr = 1180, 480, 190
write("fig-process-0.svg", "", (PW, PH))
write("fig-process-1.svg",
      f'<rect x="170" y="{py - 150}" width="300" height="300" rx="20" fill="{PALE}" stroke="{INK}" stroke-width="5"/>'
      f'<circle cx="320" cy="{py}" r="105" fill="{INK}"/><circle cx="320" cy="{py}" r="22" fill="{PALE}"/>'
      + text(320, py + 215, "Music as a product", 42), (PW, PH))
write("fig-process-2.svg",
      f'<line x1="520" y1="{py}" x2="{px - pr - 30}" y2="{py}" stroke="{INK}" stroke-width="9" marker-end="url(#a)"/>'
      + f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{GREEN}" stroke="{INK}" stroke-width="5"/>'
      + text(px, py, ["Musicking", "as a process"], 46), (PW, PH))
SAT = [("Embodiment", PURPLE, -135), ("Enaction", BLUE, -45), ("Joint action", PINK, 45), ("Social bonding", PURPLE, 135)]
for i, (t, col, a) in enumerate(SAT, 3):
    a = math.radians(a)
    sx, sy = px + 400 * math.cos(a), py + 330 * math.sin(a)
    body = (edge((px, py), (sx, sy), pad=(pr + 6, 136), arrow=False, width=5)
            + f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="130" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            + text(sx, sy, t.split(" ") if " " in t else t, 38))
    write(f"fig-process-{i}.svg", body, (PW, PH))

# ---- 4E cognition -------------------------------------------------------------------------------
W4, H4 = 1920, 960
LABELS = ["Embodied", "Enactive", "Embedded", "Extended"]
F4 = [PURPLE, BLUE, PINK, GREEN]
XS = [240 + 480 * i for i in range(4)]
HY, HR, BT, BB, BW = 340, 58, 410, 650, 150


def person(x, fill):
    r = BW / 2
    return (f'<circle cx="{x}" cy="{HY}" r="{HR}" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M{x - r} {BB} L{x - r} {BT + r} A{r} {r} 0 0 1 {x + r} {BT + r} L{x + r} {BB} Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="5"/>')


def arrow2(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="10" '
            f'marker-start="url(#a)" marker-end="url(#a)"/>')


def frame(x):
    return (f'<rect x="{x - 185}" y="{HY - 110}" width="370" height="{BB + 40 - HY + 110}" rx="40" fill="none" '
            f'stroke="{INK}" stroke-width="5"/>')


def panel(i):
    x, kind, f = XS[i], LABELS[i], F4[i]
    if kind == "Embodied":
        art = person(x, f) + arrow2(x, HY - 20, x, BB - 50)
    elif kind == "Embedded":
        art = frame(x) + person(x, f)
    elif kind == "Enactive":
        art = frame(x) + person(x - 30, f) + arrow2(x - 10, 560, x + 250, 560)
    else:
        art = (person(x - 60, f) + f'<rect x="{x + 120}" y="500" width="90" height="120" rx="14" fill="{f}" '
               f'stroke="{INK}" stroke-width="5"/>' + arrow2(x - 40, 560, x + 100, 560))
    return art + text(x, 770, kind, 58)


bar = lambda y, t, dashed: (f'<rect x="60" y="{y}" width="{W4 - 120}" height="96" rx="48" fill="#ffffff" stroke="{INK}" '
                            f'stroke-width="5"{" stroke-dasharray=\"18 12\"" if dashed else ""}/>' + text(W4 / 2, y + 48, t, 60))
for i, body in enumerate([""] + [panel(i) for i in range(4)] + [bar(850, "Musicking", False),
                                                                bar(40, "Technology for body and mind", True)]):
    write(f"fig-4e-{i}.svg", body, (W4, H4))

# ---- embodied and social ------------------------------------------------------------------------
PEOPLE = [(960, 400), (600, 400), (1320, 400), (240, 400), (1680, 400)]
FS = [GREEN, PURPLE, BLUE, PINK, PURPLE]


def phone_at(x, y):
    return x + 105, y - 10


def sperson(x, y, fill):
    r, top, bot = 75, y + 70, y + 310
    ph = phone_at(x, y)
    return (f'<circle cx="{x}" cy="{y}" r="58" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M{x - r} {bot} L{x - r} {top + r} A{r} {r} 0 0 1 {x + r} {top + r} L{x + r} {bot} Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{ph[0] - 22}" y="{ph[1] - 40}" width="44" height="80" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="5"/>')


def arc(a, b):
    (x1, y1), (x2, y2) = phone_at(*a), phone_at(*b)
    lift = 0.22 * abs(x2 - x1)
    return (f'<path d="M{x1} {y1 - 45} Q{(x1 + x2) / 2:.0f} {y1 - 45 - 2 * lift:.0f} {x2} {y2 - 45}" fill="none" '
            f'stroke="{INK}" stroke-width="4" stroke-dasharray="14 12"/>')


x0, y0 = PEOPLE[0]
p0 = phone_at(x0, y0)
one = (sperson(x0, y0, FS[0]) + f'<line x1="{p0[0] + 50}" y1="{p0[1] - 70}" x2="{p0[0] + 50}" y2="{p0[1] + 70}" '
       f'stroke="{INK}" stroke-width="10" marker-start="url(#a)" marker-end="url(#a)"/>' + text(960, 860, "Embodied", 60))
many = "".join(sperson(x, y, f) for (x, y), f in zip(PEOPLE[1:], FS[1:]))
links = "".join(arc(a, b) for a, b in combinations(PEOPLE, 2)) + text(960, 935, "and social", 60)
for i, body in enumerate(["", one, many, links]):
    write(f"fig-social-{i}.svg", body, (1920, 960))

print("wrote images/fig-q-*.svg, fig-process-0..6.svg, fig-4e-0..6.svg and fig-social-0..3.svg")
