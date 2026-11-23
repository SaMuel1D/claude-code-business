"""Druckfertige PDF-Vorlage des Kassenberichts, füllt DIN A4 quer vollständig (1 cm Rand).
Aufruf: python3 scripts/kassenbericht_a4_pdf.py [ausgabe.pdf]"""
import sys
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

out = sys.argv[1] if len(sys.argv) > 1 else "Kassenbericht Paderkinderleben - DIN A4.pdf"
NAVY, GREY, ZEBRA = HexColor("#1F2A44"), HexColor("#808080"), HexColor("#F2F4F8")
W, H = landscape(A4); m = 1 * cm
uw, uh = W - 2 * m, H - 2 * m
ROWS = 15
fr = [12, 14, 14, 14, 14, 14, 18]
cols = [uw * f / sum(fr) for f in fr]
title_h, gap, head_h = 34, 8, 32
row_h = (uh - title_h - gap - head_h) / ROWS

c = canvas.Canvas(out, pagesize=(W, H))
c.setTitle("Kassenbericht Paderkinderleben")
top = H - m
c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 18)
c.drawString(m, top - title_h / 2 - 6, "Kassenbericht Paderkinderleben, Borchener Straße 58, 33098 Paderborn")
y = top - title_h - gap
heads = ["Datum", "Anfangsbestand", "Einnahme Bar", "Einnahme EC", "Entnahme", "Endbestand", "Unterschrift"]
c.setFillColor(NAVY); c.rect(m, y - head_h, uw, head_h, stroke=0, fill=1)
c.setFillColor(white); c.setFont("Helvetica-Bold", 12)
x = m
for w, h in zip(cols, heads):
    c.drawCentredString(x + w / 2, y - head_h / 2 - 4, h); x += w
y -= head_h
for i in range(ROWS):
    if i % 2:
        c.setFillColor(ZEBRA); c.rect(m, y - row_h * (i + 1), uw, row_h, stroke=0, fill=1)
c.setStrokeColor(GREY); c.setLineWidth(0.6)
for i in range(ROWS + 1):
    c.line(m, y - row_h * i, m + uw, y - row_h * i)
x = m
for w in [0] + cols:
    x += w; c.line(x, top - title_h - gap, x, y - row_h * ROWS)
c.showPage(); c.save()
print("gespeichert:", out)
