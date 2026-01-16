
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
from openpyxl import Workbook

def _footer_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    # Watermark
    watermark_text = f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - MiniSis - Gestão de Produção"
    canvas.setFillColor(colors.lightgrey)
    canvas.drawString(inch, 0.75 * inch, watermark_text)
    # Page Number
    page_number_text = f"Página {doc.page}"
    canvas.drawRightString(letter[0] - inch, letter[1] - 0.75 * inch, page_number_text)
    canvas.restoreState()

def export_to_pdf(filename, data, headers):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    table_data = [headers] + data
    # Calculate column widths to span the page width
    page_width = letter[0] - 2 * inch # Page width minus margins
    num_columns = len(headers)
    col_width = page_width / num_columns
    table = Table(table_data, colWidths=[col_width] * num_columns)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ])

    table.setStyle(style)
    elements.append(table)
    
    doc.build(elements, onFirstPage=_footer_canvas, onLaterPages=_footer_canvas)

def export_to_excel(filename, data, headers):
    workbook = Workbook()
    sheet = workbook.active
    
    sheet.append(headers)
    
    for row in data:
        sheet.append(row)
        
    workbook.save(filename)
