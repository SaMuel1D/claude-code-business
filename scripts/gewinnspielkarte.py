#!/usr/bin/env python3
"""Gewinnspielkarte Paderkinderleben, DIN A6 quer, zweiseitig, Druck-PDF (CMYK).

Aufruf: python3 scripts/gewinnspielkarte.py [beschnitt_mm] [ausgabe.pdf]
Seite 1 = Vorderseite (Chamäleon + Text), Seite 2 = Rückseite (Ausfüllfelder).
"""
import re, sys, os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BLEED = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
OUT = sys.argv[2] if len(sys.argv) > 2 else "outputs/gewinnspielkarte-a6-druck.pdf"
W, H = 148.0, 105.0  # Endformat in mm

SVG = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-Persönlich/Ladenlokal/Werbung/Taxi/"
    "Finaler Entwurf Swandoo/chameleon_logo/SOURCE.svg")

# ---------- Farben (CMYK) ----------
NAVY = (0.90, 0.78, 0.42, 0.45)
BLAU = (0.95, 0.75, 0.0, 0.0)
GRUEN = (0.50, 0.0, 0.85, 0.0)
GRUEN_D = (0.57, 0.05, 0.95, 0.0)
HELLBLAU = (0.35, 0.12, 0.0, 0.0)
HELLBLAU_BG = (0.08, 0.02, 0.0, 0.0)
HELLGRUEN_BG = (0.10, 0.0, 0.18, 0.0)
WEISS = (0, 0, 0, 0)
# Chamäleon: Originalwerte aus "VECTOR CMYK.eps"
CH = {
    "st0": WEISS,
    "st1": (0, .475, .558, 0),
    "st2": (.771, .200, 1, .052),
    "st3": (.349, .651, .728, .237),
    "st4": (.216, 0, .485, 0),
    "st5": (.064, .609, .737, .001),
    "st6": (.349, .651, .728, .237),
    "st7": (.434, 0, .918, 0),
    "st8": (.814, .480, .948, .598),
}
EVENODD = {"st2", "st3", "st4"}

# ---------- Schriften ----------
pdfmetrics.registerFont(TTFont("Rund", "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"))
pdfmetrics.registerFont(TTFont("Text", "/System/Library/Fonts/Supplemental/Verdana.ttf"))
pdfmetrics.registerFont(TTFont("TextB", "/System/Library/Fonts/Supplemental/Verdana Bold.ttf"))

# ---------- SVG einlesen ----------
NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
TOK = re.compile(r"[MmLlHhVvCcSsZz]|" + NUM.pattern)


def parse_path(d):
    """SVG-Pfad -> Liste absoluter Segmente ('M'|'L'|'C'|'Z', Punkte)."""
    toks = TOK.findall(d)
    segs, i, cmd = [], 0, None
    x = y = sx = sy = 0.0
    lc = None  # letzter Kontrollpunkt
    n = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4}
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]; i += 1
            if cmd in "Zz":
                segs.append(("Z",)); x, y = sx, sy; lc = None
                continue
        up = cmd.upper(); rel = cmd.islower()
        a = [float(t) for t in toks[i:i + n[up]]]; i += n[up]
        if up == "M":
            x, y = (x + a[0], y + a[1]) if rel else a
            sx, sy = x, y; segs.append(("M", x, y)); lc = None
            cmd = "l" if rel else "L"
        elif up == "L":
            x, y = (x + a[0], y + a[1]) if rel else a
            segs.append(("L", x, y)); lc = None
        elif up == "H":
            x = x + a[0] if rel else a[0]; segs.append(("L", x, y)); lc = None
        elif up == "V":
            y = y + a[0] if rel else a[0]; segs.append(("L", x, y)); lc = None
        else:
            if up == "S":
                c1 = (2 * x - lc[0], 2 * y - lc[1]) if lc else (x, y)
                rest = a
            else:
                c1 = (x + a[0], y + a[1]) if rel else (a[0], a[1])
                rest = a[2:]
            if rel:
                rest = [rest[0] + x, rest[1] + y, rest[2] + x, rest[3] + y]
            segs.append(("C", c1[0], c1[1], *rest))
            lc = (rest[0], rest[1]); x, y = rest[2], rest[3]
    return segs


def load_chameleon():
    src = open(SVG, encoding="utf-8").read()
    shapes = []
    for m in re.finditer(r"<(path|circle|polygon)\s+([^>]*?)/?>", src, re.S):
        kind, attrs = m.group(1), dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(2)))
        cls = attrs["class"]
        if kind == "path":
            shapes.append((cls, "path", parse_path(attrs["d"])))
        elif kind == "circle":
            shapes.append((cls, "circle", (float(attrs["cx"]), float(attrs["cy"]), float(attrs["r"]))))
        else:
            p = [float(v) for v in NUM.findall(attrs["points"])]
            segs = [("M", p[0], p[1])] + [("L", p[k], p[k + 1]) for k in range(2, len(p), 2)] + [("Z",)]
            shapes.append((cls, "path", segs))
    xs, ys = [], []
    for cls, kind, data in shapes:
        if kind == "circle":
            cx, cy, r = data; xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
        else:
            for s in data:
                v = s[1:]; xs += v[0::2]; ys += v[1::2]
    return shapes, (min(xs), min(ys), max(xs), max(ys))


SHAPES, BBOX = load_chameleon()


def draw_chameleon(c, x, y, width, flip=False, rot=0):
    """Zeichnet das Chamäleon; x/y = linke untere Ecke in mm (Endformat-Koordinaten)."""
    x0, y0, x1, y1 = BBOX
    s = width * mm / (x1 - x0)
    c.saveState()
    c.translate(x * mm, y * mm)
    if rot:
        c.rotate(rot)
    if flip:
        c.translate(width * mm, 0); c.scale(-1, 1)
    c.translate(0, (y1 - y0) * s); c.scale(s, -s); c.translate(-x0, -y0)
    for cls, kind, data in SHAPES:
        c.setFillColorCMYK(*CH[cls])
        if kind == "circle":
            c.circle(*data, stroke=0, fill=1)
            continue
        p = c.beginPath()
        for sg in data:
            if sg[0] == "M": p.moveTo(sg[1], sg[2])
            elif sg[0] == "L": p.lineTo(sg[1], sg[2])
            elif sg[0] == "C": p.curveTo(*sg[1:])
            else: p.close()
        c.drawPath(p, stroke=0, fill=1, fillMode=0 if cls in EVENODD else 1)
    c.restoreState()


def ch_height(width):
    x0, y0, x1, y1 = BBOX
    return width * (y1 - y0) / (x1 - x0)


# ---------- Hilfen ----------
def rect(c, x, y, w, h, col, r=0):
    c.setFillColorCMYK(*col)
    if r:
        c.roundRect(x * mm, y * mm, w * mm, h * mm, r * mm, stroke=0, fill=1)
    else:
        c.rect(x * mm, y * mm, w * mm, h * mm, stroke=0, fill=1)


def circ(c, x, y, r, col):
    c.setFillColorCMYK(*col); c.circle(x * mm, y * mm, r * mm, stroke=0, fill=1)


def text(c, x, y, s, font, size, col, align="l", space=0):
    c.setFillColorCMYK(*col); c.setFont(font, size)
    t = c.beginText(); t.setCharSpace(space)
    w = pdfmetrics.stringWidth(s, font, size) + space * (len(s) - 1)
    px = x * mm - (w if align == "r" else w / 2 if align == "c" else 0)
    t.setTextOrigin(px, y * mm); t.textOut(s); c.drawText(t)


# ---------- Vorderseite ----------
def front(c):
    B = BLEED
    rect(c, -B, -B, W + 2 * B, H + 2 * B, HELLBLAU_BG)
    # Deko-Kreise
    circ(c, 112, 60, 44, WEISS)
    circ(c, 14, 98, 15, HELLGRUEN_BG)
    circ(c, 70, 28, 7, HELLGRUEN_BG)
    circ(c, 82, 96, 4, HELLBLAU)
    circ(c, 63, 100, 2.2, GRUEN)
    circ(c, 8, 30, 3, HELLBLAU)
    circ(c, 142, 100, 2.5, GRUEN)
    # Chamäleon
    cw = 68
    draw_chameleon(c, 75, 60 - ch_height(cw) / 2 + 1, cw)
    # Text
    text(c, 9, 77, "Gewinnspiel", "Rund", 37, BLAU)
    rect(c, 9, 61.5, 66, 10, GRUEN)
    text(c, 42, 64.6, "Mitmachen und gewinnen!", "Rund", 12.5, WEISS, "c")
    y = 52
    for line in ("Karte ausfüllen,", "bei uns abgeben", "und Daumen drücken."):
        text(c, 9, y, line, "TextB", 10.5, NAVY); y -= 5.6
    # Fußband
    rect(c, -B, -B, W + 2 * B, 17 + B, BLAU)
    rect(c, -B, 17, W + 2 * B, 1.6, GRUEN)
    text(c, 9, 6.2, "Paderkinderleben", "Rund", 17, WEISS)
    text(c, 139, 6.6, "einfach.sicher.sein.", "Rund", 11.5, GRUEN, "r")


# ---------- Rückseite ----------
RECHT = ("Ihre Daten sind bei uns sicher und werden nur zur Gewinnermittlung benötigt. "
         "Eine Weiternutzung ist ausgeschlossen. Mit Ihrer Unterschrift bestätigen Sie, dass Sie im "
         "Falle eines Gewinns damit einverstanden sind, dass Ihr Name (Vorname + gekürzter "
         "Nachname) bei uns im Ladengeschäft und auf Facebook bekanntgegeben wird.")
BAR = "Eine Barauszahlung ist ausgeschlossen."


def field(c, x0, x1, y, label):
    c.setStrokeColorCMYK(*NAVY); c.setLineWidth(0.6)
    c.line(x0 * mm, y * mm, x1 * mm, y * mm)
    text(c, x0, y - 3.3, label, "TextB", 6.8, BLAU)


def back(c):
    B = BLEED
    rect(c, -B, -B, W + 2 * B, H + 2 * B, WEISS)
    # Kopfband
    rect(c, -B, 91, W + 2 * B, 14 + B, BLAU)
    rect(c, -B, 89.6, W + 2 * B, 1.4, GRUEN)
    text(c, 8, 95.4, "Gewinnspiel", "Rund", 17, WEISS)
    text(c, 121, 96.0, "Teilnahmekarte", "TextB", 8.5, WEISS, "r", space=0.6)
    circ(c, 132, 93.5, 9.5, WEISS)
    c.setStrokeColorCMYK(*GRUEN); c.setLineWidth(1.6)
    c.circle(132 * mm, 93.5 * mm, 9.5 * mm, stroke=1, fill=0)
    draw_chameleon(c, 124.6, 93.5 - ch_height(15) / 2 + 0.3, 15)
    # Felder
    L, R, M1, M2 = 8, 140, 71.5, 76.5
    field(c, L, M1, 77, "Vorname");                field(c, M2, R, 77, "Nachname")
    field(c, L, M1, 64, "Strasse und Hausnummer"); field(c, M2, R, 64, "PLZ und Ort")
    field(c, L, M1, 51, "Emailadresse");           field(c, M2, R, 51, "Telefonnummer")
    field(c, L, M1, 37, "Ort, Datum");             field(c, M2, R, 37, "Unterschrift")
    # Rechtstext
    rect(c, -B, -B, W + 2 * B, 28 + B, HELLBLAU_BG)
    size, lead = 6.9, 3.3
    y = 22.6
    for line in simpleSplit(RECHT, "Text", size, (R - L) * mm):
        text(c, L, y, line, "Text", size, NAVY); y -= lead
    y -= 1.6
    text(c, L, y, BAR, "TextB", 7.6, BLAU)
    text(c, R, y, "Paderkinderleben", "Rund", 8.5, GRUEN_D, "r")


def main():
    pw, ph = (W + 2 * BLEED) * mm, (H + 2 * BLEED) * mm
    c = canvas.Canvas(OUT, pagesize=(pw, ph), pageCompression=1, initialFontName="Rund")
    c.setTitle("Gewinnspielkarte Paderkinderleben DIN A6 quer")
    c.setAuthor("Paderkinderleben")
    trim = (BLEED * mm, BLEED * mm, (BLEED + W) * mm, (BLEED + H) * mm)
    for side in (front, back):
        c.setTrimBox(trim); c.setBleedBox((0, 0, pw, ph))
        c.saveState(); c.translate(BLEED * mm, BLEED * mm)
        side(c)
        c.restoreState(); c.showPage()
    c.save()
    print(OUT, f"{W + 2 * BLEED:g} x {H + 2 * BLEED:g} mm (Beschnitt {BLEED:g} mm)")


if __name__ == "__main__":
    main()
