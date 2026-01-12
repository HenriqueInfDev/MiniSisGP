
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def export_to_pdf(filename, data, headers):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    table_data = [headers] + data
    table = Table(table_data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)

from openpyxl import Workbook

def export_to_excel(filename, data, headers):
    workbook = Workbook()
    sheet = workbook.active
    
    sheet.append(headers)
    
    for row in data:
        sheet.append(row)
        
    workbook.save(filename)
