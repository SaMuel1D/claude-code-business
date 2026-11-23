"""Erzeugt den Kassenbericht als Excel-Vorlage, die eine DIN-A4-Seite (quer) komplett ausfüllt.
Aufruf: python3 scripts/kassenbericht_a4.py [ausgabe.xlsx]"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.properties import PageSetupProperties

out = sys.argv[1] if len(sys.argv) > 1 else "Kassenbericht Paderkinderleben - DIN A4.xlsx"
NAVY = "1F2A44"
ROWS = 15  # Datenzeilen

wb = Workbook(); ws = wb.active; ws.title = "Kassenbericht"
thin = Side(style="thin", color="808080"); med = Side(style="medium", color=NAVY)
box = Border(left=thin, right=thin, top=thin, bottom=thin)

# Spaltenbreiten: zusammen ca. 27,7 cm (A4 quer minus 2 x 1 cm Rand)
widths = {"A": 17.3, "B": 20.3, "C": 20.3, "D": 20.3, "E": 20.3, "F": 20.3, "G": 26.1}
for col, w in widths.items():
    ws.column_dimensions[col].width = w

ws.merge_cells("A1:G1")
ws["A1"] = "Kassenbericht Paderkinderleben, Borchener Straße 58, 33098 Paderborn"
ws["A1"].font = Font(name="Calibri", size=18, bold=True, color=NAVY)
ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[1].height = 34
ws.row_dimensions[2].height = 8

headers = ["Datum", "Anfangsbestand", "Einnahme Bar", "Einnahme EC", "Entnahme", "Endbestand", "Unterschrift"]
for i, h in enumerate(headers, 1):
    c = ws.cell(row=3, column=i, value=h)
    c.font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = box
ws.row_dimensions[3].height = 32

for r in range(4, 4 + ROWS):
    ws.row_dimensions[r].height = 31
    for col in range(1, 8):
        c = ws.cell(row=r, column=col)
        c.border = box
        c.font = Font(name="Calibri", size=12)
        c.alignment = Alignment(vertical="center", horizontal="center" if col in (1, 7) else "right")
        if col == 1:
            c.number_format = "DD.MM.YYYY"
        elif col <= 6:
            c.number_format = '#,##0.00 "€"'
        else:
            c.number_format = "@"
    # Endbestand = Anfangsbestand + Einnahme Bar - Entnahme (EC landet nicht in der Kasse)
    ws.cell(row=r, column=6, value=f'=IF(B{r}="","",B{r}+C{r}-E{r})')
    if r % 2:
        for col in range(1, 8):
            ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="F2F4F8")

last = 3 + ROWS
ws.print_area = f"A1:G{last}"
ps = ws.page_setup
ps.paperSize = ws.PAPERSIZE_A4
ps.orientation = "landscape"
ps.fitToWidth = 1; ps.fitToHeight = 1
ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
ws.print_options.horizontalCentered = True
ws.print_options.verticalCentered = True
cm = 1 / 2.54
ws.page_margins.left = ws.page_margins.right = 1 * cm
ws.page_margins.top = ws.page_margins.bottom = 1 * cm
ws.page_margins.header = ws.page_margins.footer = 0.3 * cm
ws.freeze_panes = "A4"
wb.save(out)
print("gespeichert:", out)
