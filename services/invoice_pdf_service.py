"""
GV Powers ERP - Professional Invoice PDF Generation Service
Generates Owner Copy, Customer Copy, and GST Tax Copy using ReportLab.
Designed for A4 Portrait, print-friendly, commercial-grade invoices.
Brand: GV POWERS - Powering A Better Tomorrow
"""

import os
import io
import qrcode
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    HRFlowable, Image, KeepTogether, PageBreak, Frame, PageTemplate
)
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMPANY = {
    "name": "GV POWERS",
    "tagline": "Powering A Better Tomorrow",
    "services": "Solar Energy | UPS Systems | Inverters | RO Solutions | Electricals",
    "gstin": "29AAAAA0000A1Z5",
    "pan": "AAAAA0000A",
    "state": "Karnataka",
    "state_code": 29,
    "address": "Bangalore, Karnataka, India",
    "phone": "+91-9876543210",
    "email": "gvpowerssalem@gmail.com",
    "website": "https://gvpowers.in",
    "bank_name": "State Bank of India",
    "bank_account": "12345678901234",
    "bank_ifsc": "SBIN0001234",
    "upi_id": "gvpowers@upi",
}

# Brand Colors
PRIMARY_NAVY = colors.HexColor("#081C3A")
PRIMARY_BLUE = colors.HexColor("#2563EB")
PRIMARY_BLUE_HOVER = colors.HexColor("#1D4ED8")
LIGHT_BG = colors.HexColor("#F8FAFC")
BORDER_COLOR = colors.HexColor("#E5E7EB")
TEXT_DARK = colors.HexColor("#111827")
TEXT_SECONDARY = colors.HexColor("#4B5563")
TEXT_MUTED = colors.HexColor("#6B7280")
TEXT_LIGHT = colors.HexColor("#9CA3AF")
WHITE = colors.white
SUCCESS = colors.HexColor("#16A34A")
WARNING = colors.HexColor("#F59E0B")
DANGER = colors.HexColor("#DC2626")

# Legacy aliases
PRIMARY = PRIMARY_NAVY
ACCENT = PRIMARY_BLUE
GREEN = SUCCESS


def amount_to_words(amount):
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
            "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
            "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def _chunk(n):
        if n == 0:
            return ""
        if n < 20:
            return ones[n]
        if n < 100:
            return (tens[n // 10] + " " + ones[n % 10]).strip()
        return (ones[n // 100] + " Hundred " + _chunk(n % 100)).strip()

    def _rupees_words(n):
        words = ""
        if n >= 10000000:
            words += _chunk(n // 10000000) + " Crore "
            n %= 10000000
        if n >= 100000:
            words += _chunk(n // 100000) + " Lakh "
            n %= 100000
        if n >= 1000:
            words += _chunk(n // 1000) + " Thousand "
            n %= 1000
        if n > 0:
            words += _chunk(n) + " "
        return words.strip()

    try:
        if isinstance(amount, str):
            amount = Decimal(amount)
        else:
            amount = Decimal(str(amount))
    except Exception:
        return "Rupees Zero Only"

    if amount < 0:
        return "Minus " + amount_to_words(-amount)

    total_paise = int((amount * 100).to_integral_value(rounding=ROUND_HALF_UP))
    rupees, paise = divmod(total_paise, 100)
    if total_paise == 0:
        return "Rupees Zero Only"
    rupee_words = _rupees_words(rupees)
    if paise == 0:
        if rupees == 1:
            return "Rupe One Only"
        return f"Rupees {rupee_words} Only"
    paise_words = _rupees_words(paise)
    if rupees == 0:
        return f"Rupees {paise_words} Paise Only"
    return f"Rupees {rupee_words} and {paise_words} Paise Only"


def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'CompanyName', parent=styles['Normal'], fontSize=14, fontName='Helvetica-Bold',
        textColor=TEXT_DARK, leading=16
    ))
    styles.add(ParagraphStyle(
        'CompanyTagline', parent=styles['Normal'], fontSize=7, fontName='Helvetica-Oblique',
        textColor=PRIMARY_BLUE, leading=9
    ))
    styles.add(ParagraphStyle(
        'CompanyDetail', parent=styles['Normal'], fontSize=7, fontName='Helvetica',
        textColor=TEXT_MUTED, leading=9
    ))
    styles.add(ParagraphStyle(
        'InvoiceTitle', parent=styles['Normal'], fontSize=20, fontName='Helvetica-Bold',
        textColor=PRIMARY_NAVY, alignment=TA_RIGHT, leading=22
    ))
    styles.add(ParagraphStyle(
        'CopyBadge', parent=styles['Normal'], fontSize=8, fontName='Helvetica-Bold',
        textColor=PRIMARY_BLUE, alignment=TA_RIGHT, leading=10, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        'InvoiceNum', parent=styles['Normal'], fontSize=7.5, fontName='Helvetica',
        textColor=TEXT_MUTED, alignment=TA_RIGHT, leading=10
    ))
    styles.add(ParagraphStyle(
        'SectionTitle', parent=styles['Normal'], fontSize=7, fontName='Helvetica-Bold',
        textColor=PRIMARY_BLUE, leading=9
    ))
    styles.add(ParagraphStyle(
        'DetailLabel', parent=styles['Normal'], fontSize=7, fontName='Helvetica',
        textColor=TEXT_MUTED, leading=9
    ))
    styles.add(ParagraphStyle(
        'DetailValue', parent=styles['Normal'], fontSize=8, fontName='Helvetica-Bold',
        textColor=TEXT_DARK, leading=10
    ))
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['Normal'], fontSize=6.5, fontName='Helvetica',
        textColor=TEXT_DARK, leading=8
    ))
    styles.add(ParagraphStyle(
        'TableCellBold', parent=styles['Normal'], fontSize=6.5, fontName='Helvetica-Bold',
        textColor=TEXT_DARK, leading=8
    ))
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['Normal'], fontSize=6, fontName='Helvetica-Bold',
        textColor=WHITE, leading=8
    ))
    styles.add(ParagraphStyle(
        'AmountWords', parent=styles['Normal'], fontSize=7, fontName='Helvetica-Oblique',
        textColor=TEXT_MUTED, leading=9
    ))
    styles.add(ParagraphStyle(
        'FooterText', parent=styles['Normal'], fontSize=6.5, fontName='Helvetica',
        textColor=TEXT_MUTED, leading=8
    ))
    styles.add(ParagraphStyle(
        'Watermark', parent=styles['Normal'], fontSize=50, fontName='Helvetica-Bold',
        textColor=colors.HexColor("#f0f0f0"), alignment=TA_CENTER, leading=55
    ))
    styles.add(ParagraphStyle(
        'SmallText', parent=styles['Normal'], fontSize=6, fontName='Helvetica',
        textColor=TEXT_MUTED, leading=8
    ))
    styles.add(ParagraphStyle(
        'TotalLabel', parent=styles['Normal'], fontSize=7.5, fontName='Helvetica',
        textColor=TEXT_DARK, leading=10
    ))
    styles.add(ParagraphStyle(
        'TotalValue', parent=styles['Normal'], fontSize=7.5, fontName='Helvetica-Bold',
        textColor=TEXT_DARK, alignment=TA_RIGHT, leading=10
    ))
    styles.add(ParagraphStyle(
        'GrandTotal', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold',
        textColor=PRIMARY_BLUE, alignment=TA_RIGHT, leading=12
    ))
    styles.add(ParagraphStyle(
        'Declaration', parent=styles['Normal'], fontSize=6.5, fontName='Helvetica',
        textColor=TEXT_MUTED, leading=9, spaceBefore=4
    ))
    return styles


def _generate_qr_code(data_str, size=50):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=0)
    qr.add_data(data_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


def _draw_watermark(c, text, page_width, page_height):
    c.saveState()
    c.setFillColor(colors.HexColor("#E5E7EB"))
    c.setFont("Helvetica-Bold", 55)
    c.translate(page_width / 2, page_height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def _draw_page_footer(c, company, page_num, page_width):
    c.saveState()
    y = 18
    c.setFont("Helvetica", 5.5)
    c.setFillColor(TEXT_MUTED)
    line1 = f"{company['name']} | GSTIN: {company['gstin']} | {company['phone']} | {company['email']}"
    c.drawCentredString(page_width / 2, y + 10, line1)
    c.drawCentredString(page_width / 2, y + 2, f"This is a computer-generated invoice. | Page {page_num}")
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    c.line(30, y + 18, page_width - 30, y + 18)
    c.restoreState()


def _draw_header(c, company, styles, copy_label, invoice, page_width):
    x_start = 30
    y_top = A4[1] - 25

    # Logo
    logo_path = os.path.join(BASE_DIR, "static", "img", "logo", "btgr.png")
    logo_x = x_start
    logo_y = y_top - 40
    if os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, logo_x, logo_y, width=40, height=40, preserveAspectRatio=True, mask='auto')
        except Exception:
            _draw_fallback_logo(c, logo_x, logo_y)
    else:
        _draw_fallback_logo(c, logo_x, logo_y)

    # Company name
    tx = x_start + 48
    ty = y_top - 10
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(PRIMARY_NAVY)
    c.drawString(tx, ty, company["name"])

    # Tagline
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(tx, ty - 10, company.get("tagline", ""))

    # Services
    c.setFont("Helvetica", 6)
    c.setFillColor(TEXT_MUTED)
    c.drawString(tx, ty - 19, company.get("services", ""))

    # Company details
    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(tx, ty - 29, f"Address: {company['address']}")
    c.drawString(tx, ty - 38, f"GSTIN: {company['gstin']}  |  PAN: {company['pan']}")
    c.drawString(tx, ty - 47, f"Phone: {company['phone']}  |  Email: {company['email']}")
    c.drawString(tx, ty - 56, f"Website: {company['website']}")

    # Right side - Invoice title
    rx = page_width - 30
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(PRIMARY_NAVY)
    c.drawRightString(rx, y_top - 10, "TAX INVOICE")

    # Copy badge
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(PRIMARY_BLUE)
    c.drawRightString(rx, y_top - 22, copy_label)

    # Invoice meta
    c.setFont("Helvetica", 7)
    c.setFillColor(TEXT_MUTED)
    c.drawRightString(rx, y_top - 34, f"Invoice #: {invoice.invoice_number}")
    c.drawRightString(rx, y_top - 43, f"Date: {invoice.invoice_date}")
    if invoice.due_date:
        c.drawRightString(rx, y_top - 52, f"Due Date: {invoice.due_date}")

    # Divider line
    c.setStrokeColor(PRIMARY_BLUE)
    c.setLineWidth(1.2)
    c.line(x_start, y_top - 62, page_width - 30, y_top - 62)

    return y_top - 72


def _draw_fallback_logo(c, x, y):
    c.setFillColor(PRIMARY_BLUE)
    c.roundRect(x, y, 40, 40, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(x + 20, y + 14, "GV")


def _draw_customer_and_info(c, invoice, styles, y, page_width):
    x_left = 30
    x_mid = page_width / 2 + 5
    box_w = page_width / 2 - 35
    box_h = 60

    # Bill To box
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    c.setFillColor(LIGHT_BG)
    c.roundRect(x_left, y - box_h, box_w, box_h, 3, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(x_left + 6, y - 10, "BILL TO")

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(TEXT_DARK)
    c.drawString(x_left + 6, y - 22, invoice.customer_name or "N/A")

    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_MUTED)
    line_y = y - 33
    if invoice.customer_address:
        c.drawString(x_left + 6, line_y, invoice.customer_address[:50])
        line_y -= 8
    if invoice.customer_mobile:
        c.drawString(x_left + 6, line_y, f"Mobile: {invoice.customer_mobile}")
        line_y -= 8
    if invoice.customer_state:
        c.drawString(x_left + 6, line_y, f"State: {invoice.customer_state} ({invoice.customer_state_code})")
        line_y -= 8
    if invoice.customer_gstin:
        c.drawString(x_left + 6, line_y, f"GSTIN: {invoice.customer_gstin}")

    # Invoice Details box
    c.setFillColor(LIGHT_BG)
    c.roundRect(x_mid, y - box_h, box_w, box_h, 3, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(x_mid + 6, y - 10, "INVOICE DETAILS")

    c.setFont("Helvetica", 6.5)
    details = [
        ("Invoice #", invoice.invoice_number),
        ("Date", str(invoice.invoice_date)),
    ]
    if invoice.due_date:
        details.append(("Due Date", str(invoice.due_date)))
    if invoice.payment_method:
        details.append(("Payment", invoice.payment_method.replace("_", " ").title()))
    if hasattr(invoice, 'creator') and invoice.creator:
        details.append(("Sales Person", invoice.creator.full_name if invoice.creator else "System"))
    details.append(("Place of Supply", f"{invoice.customer_state or 'N/A'} ({invoice.customer_state_code})"))

    dy = y - 22
    for label, val in details:
        c.setFillColor(TEXT_MUTED)
        c.drawString(x_mid + 6, dy, f"{label}:")
        c.setFillColor(TEXT_DARK)
        c.drawString(x_mid + 58, dy, str(val)[:35])
        dy -= 9

    return y - box_h - 8


def _draw_product_table(c, invoice, styles, y, page_width, show_internal=False):
    x_start = 30
    col_widths_raw = [16, 75, 35, 22, 22, 22, 22, 22, 22, 22, 22, 28]

    if show_internal:
        col_widths_raw = [16, 65, 30, 20, 20, 20, 20, 20, 20, 20, 20, 26, 26]
        extra_headers = ["Purchase", "Profit"]
    else:
        extra_headers = []

    total_w = sum(col_widths_raw)
    scale = (page_width - 60) / total_w
    col_widths = [w * scale for w in col_widths_raw]

    headers = ["#", "Product Name", "HSN", "Qty", "Rate", "Disc%", "GST%", "Taxable", "CGST", "SGST", "IGST", "Amount"]
    if show_internal:
        headers.extend(["Purchase", "Profit"])

    header_row = [Paragraph(h, styles['TableHeader']) for h in headers]

    data = [header_row]
    for idx, item in enumerate(invoice.items, 1):
        row = [
            Paragraph(str(idx), styles['TableCell']),
            Paragraph(str(item.product_name)[:25], styles['TableCell']),
            Paragraph(str(item.hsn or "-"), styles['TableCell']),
            Paragraph(f"{item.qty} {item.unit}", styles['TableCell']),
            Paragraph(f"{item.price:.2f}", styles['TableCell']),
            Paragraph(f"{item.discount}%", styles['TableCell']),
            Paragraph(f"{item.gst_rate}%", styles['TableCell']),
            Paragraph(f"{item.taxable_value:.2f}", styles['TableCell']),
            Paragraph(f"{item.cgst:.2f}", styles['TableCell']),
            Paragraph(f"{item.sgst:.2f}", styles['TableCell']),
            Paragraph(f"{item.igst:.2f}", styles['TableCell']),
            Paragraph(f"<b>{item.total:.2f}</b>", styles['TableCellBold']),
        ]
        if show_internal:
            purchase = 0
            profit = 0
            if item.product_id:
                try:
                    from app import db, Product as ProductModel
                    prod = db.session.get(ProductModel, item.product_id)
                    if prod:
                        purchase = prod.purchase_price * item.qty
                        profit = item.total - purchase
                except Exception:
                    pass
            row.append(Paragraph(f"{purchase:.2f}", styles['TableCell']))
            profit_style = ParagraphStyle('ProfitCell', parent=styles['TableCell'],
                                          textColor=GREEN if profit > 0 else DANGER)
            row.append(Paragraph(f"{profit:.2f}", profit_style))
        data.append(row)

    table = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 6),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('FONTSIZE', (0, 1), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.3, BORDER_COLOR),
        ('LINEBELOW', (0, 0), (-1, 0), 1, PRIMARY_BLUE),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), LIGHT_BG))
    table.setStyle(TableStyle(style_cmds))

    tw, th = table.wrap(page_width - 60, 0)
    if y - th < 60:
        c.showPage()
        y = A4[1] - 30
    table.drawOn(c, x_start, y - th)
    return y - th


def _draw_summary(c, invoice, styles, y, page_width, show_internal=False):
    x_start = 30
    box_w = 220
    box_x = page_width - 30 - box_w

    lines = [
        ("Subtotal", f"{invoice.subtotal:.2f}"),
    ]
    if invoice.total_discount > 0:
        lines.append(("Discount", f"-{invoice.total_discount:.2f}"))
    lines.append(("Taxable Amount", f"{invoice.total_taxable:.2f}"))
    if invoice.is_intra_state:
        lines.append(("CGST", f"{invoice.total_cgst:.2f}"))
        lines.append(("SGST", f"{invoice.total_sgst:.2f}"))
    else:
        lines.append(("IGST", f"{invoice.total_igst:.2f}"))
    if invoice.round_off != 0:
        lines.append(("Round Off", f"{invoice.round_off:.2f}"))

    line_h = 11
    block_h = len(lines) * line_h + 22
    total_h = block_h + 15

    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    c.setFillColor(LIGHT_BG)
    c.roundRect(box_x, y - total_h, box_w, total_h, 3, fill=1, stroke=1)

    ty = y - 12
    for label, val in lines:
        c.setFont("Helvetica", 7)
        c.setFillColor(TEXT_MUTED)
        c.drawString(box_x + 8, ty, label)
        c.setFillColor(TEXT_DARK)
        c.drawRightString(box_x + box_w - 8, ty, f"Rs. {val}")
        ty -= line_h

    c.setStrokeColor(PRIMARY_BLUE)
    c.setLineWidth(0.8)
    c.line(box_x + 8, ty + 2, box_x + box_w - 8, ty + 2)

    ty -= 6
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(box_x + 8, ty, "Grand Total")
    c.drawRightString(box_x + box_w - 8, ty, f"Rs. {invoice.grand_total:.2f}")

    amount_words = amount_to_words(invoice.grand_total)
    ty -= 18
    c.setFont("Helvetica-Oblique", 6.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(box_x + 8, ty, f"Amount in words:")
    ty -= 10
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(TEXT_DARK)
    words = amount_words
    if len(words) > 65:
        c.drawString(box_x + 8, ty, words[:65])
        ty -= 9
        c.drawString(box_x + 8, ty, words[65:])
    else:
        c.drawString(box_x + 8, ty, words)

    return y - total_h - 25


def _draw_payment_info(c, invoice, styles, y, page_width, show_qr=False):
    x_start = 30
    box_w = 200
    payments = list(getattr(invoice, 'payments', []) or [])
    history_rows = []
    if payments:
        try:
            history_rows = sorted(payments, key=lambda p: (p.payment_date or date(1900, 1, 1), p.id or 0), reverse=True)
        except Exception:
            history_rows = payments
        history_rows = history_rows[:5]
    status = getattr(invoice, 'payment_status', '') or ('paid' if (invoice.amount_paid or 0) >= (invoice.grand_total or 0) else 'partial' if (invoice.amount_paid or 0) > 0 else 'due')
    status_label = 'FULLY PAID' if status == 'paid' else 'PARTIALLY PAID' if status == 'partial' else ('CANCELLED' if status == 'cancelled' else 'DUE')
    box_h = 58 + 11 * len(history_rows)

    c.setFillColor(LIGHT_BG)
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    c.roundRect(x_start, y - box_h, box_w, box_h, 3, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(x_start + 6, y - 10, "PAYMENT INFORMATION")

    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_DARK)
    c.drawString(x_start + 6, y - 22, f"Status: {status_label}  |  Method: {(invoice.payment_method or 'N/A').replace('_', ' ').title()}")
    balance = (invoice.balance_due if invoice.balance_due is not None else (invoice.grand_total or 0) - (invoice.amount_paid or 0))
    c.drawString(x_start + 6, y - 33, f"Paid: Rs. {invoice.amount_paid:.2f}  |  Balance: Rs. {balance:.2f}")

    ty = y - 46
    if history_rows:
        c.setFont("Helvetica-Bold", 6.0)
        c.setFillColor(TEXT_DARK)
        c.drawString(x_start + 6, ty, "History:")
        c.setFont("Helvetica", 6.0)
        for p in history_rows:
            ty -= 9
            ref = getattr(p, 'reference_number', None) or getattr(p, 'utr', '') or getattr(p, 'transaction_id', '') or getattr(p, 'cheque_number', '') or ''
            date_s = p.payment_date.strftime('%d-%b-%Y') if getattr(p, 'payment_date', None) else '—'
            method = (p.payment_method or 'cash').replace('_', ' ').title()
            text = f"{date_s}  {method}  Rs.{p.amount:.2f}"
            if ref:
                text += f"  ({ref})"
            if len(text) > 48:
                text = text[:47] + '…'
            c.drawString(x_start + 6, ty, text)

    if show_qr:
        qr_data = f"Invoice:{invoice.invoice_number}|Amount:{invoice.grand_total}|Customer:{invoice.customer_name}"
        qr_buf = _generate_qr_code(qr_data, 45)
        try:
            qr_img = Image(qr_buf, width=38, height=38)
            qr_img.drawOn(c, x_start + box_w + 10, y - 42)
        except Exception:
            pass

    return y - box_h - 8


def _draw_bank_details(c, company, styles, y, page_width):
    x_start = 30
    box_w = 220

    c.setFillColor(LIGHT_BG)
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    c.roundRect(x_start, y - 48, box_w, 48, 3, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(x_start + 6, y - 10, "BANK DETAILS")

    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_DARK)
    c.drawString(x_start + 6, y - 22, f"A/C Name: {company.get('name', '')}")
    c.drawString(x_start + 6, y - 32, f"Bank: {company.get('bank_name', '')}  |  A/C: {company.get('bank_account', '')}")
    c.drawString(x_start + 6, y - 42, f"IFSC: {company.get('bank_ifsc', '')}  |  UPI: {company.get('upi_id', '')}")

    return y - 56


def _draw_declaration_and_signatures(c, invoice, styles, y, page_width, show_customer_sig=True, company=None):
    company = company or COMPANY
    x_start = 30
    col_w = (page_width - 60) / 2

    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(x_start, y - 8, "DECLARATION")
    c.setFont("Helvetica", 6)
    c.setFillColor(TEXT_DARK)
    decl_lines = [
        "1. Goods once sold will not be returned or exchanged.",
        "2. Subject to local jurisdiction.",
        "3. E&OE (Errors and Omissions Excepted).",
        "4. Payment to be made within due date.",
    ]
    dy = y - 18
    for line in decl_lines:
        c.drawString(x_start, dy, line)
        dy -= 8

    sig_y = dy - 8
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)

    sig_x1 = x_start
    sig_x2 = x_start + col_w + 20
    sig_w = col_w - 10

    c.line(sig_x1, sig_y, sig_x1 + sig_w, sig_y)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(sig_x1, sig_y - 10, "Authorized Signature")
    c.drawString(sig_x1, sig_y - 19, company["name"])

    if show_customer_sig:
        c.line(sig_x2, sig_y, sig_x2 + sig_w, sig_y)
        c.drawString(sig_x2, sig_y - 10, "Customer Signature")
        c.drawString(sig_x2, sig_y - 19, "Date: _______________")

    return sig_y - 30


def _draw_gst_summary_table(c, invoice, styles, y, page_width):
    x_start = 30
    headers = ["HSN Code", "Taxable Value", "Rate", "CGST", "SGST", "IGST", "Total Tax"]
    header_row = [Paragraph(h, styles['TableHeader']) for h in headers]
    data = [header_row]

    hsn_data = {}
    for item in invoice.items:
        hsn = item.hsn or "N/A"
        if hsn not in hsn_data:
            hsn_data[hsn] = {"taxable": 0, "rate": item.gst_rate, "cgst": 0, "sgst": 0, "igst": 0}
        hsn_data[hsn]["taxable"] += item.taxable_value
        hsn_data[hsn]["cgst"] += item.cgst
        hsn_data[hsn]["sgst"] += item.sgst
        hsn_data[hsn]["igst"] += item.igst

    for hsn, d in hsn_data.items():
        total_tax = d["cgst"] + d["sgst"] + d["igst"]
        data.append([
            Paragraph(hsn, styles['TableCell']),
            Paragraph(f"{d['taxable']:.2f}", styles['TableCell']),
            Paragraph(f"{d['rate']:.0f}%", styles['TableCell']),
            Paragraph(f"{d['cgst']:.2f}", styles['TableCell']),
            Paragraph(f"{d['sgst']:.2f}", styles['TableCell']),
            Paragraph(f"{d['igst']:.2f}", styles['TableCell']),
            Paragraph(f"{total_tax:.2f}", styles['TableCellBold']),
        ])

    total_tax = invoice.total_cgst + invoice.total_sgst + invoice.total_igst
    data.append([
        Paragraph("<b>Total</b>", styles['TableCellBold']),
        Paragraph(f"<b>{invoice.total_taxable:.2f}</b>", styles['TableCellBold']),
        Paragraph("", styles['TableCell']),
        Paragraph(f"<b>{invoice.total_cgst:.2f}</b>", styles['TableCellBold']),
        Paragraph(f"<b>{invoice.total_sgst:.2f}</b>", styles['TableCellBold']),
        Paragraph(f"<b>{invoice.total_igst:.2f}</b>", styles['TableCellBold']),
        Paragraph(f"<b>{total_tax:.2f}</b>", styles['TableCellBold']),
    ])

    col_w = [(page_width - 60) / 7] * 7
    table = Table(data, colWidths=col_w, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.3, BORDER_COLOR),
        ('LINEBELOW', (0, -1), (-1, -1), 1, PRIMARY_BLUE),
        ('BACKGROUND', (0, -1), (-1, -1), LIGHT_BG),
    ]))

    tw, th = table.wrap(page_width - 60, 0)
    table.drawOn(c, x_start, y - th)
    return y - th


def generate_owner_copy(invoice, company=None):
    company = company or COMPANY
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    styles = _get_styles()
    page_w = A4[0]

    _draw_watermark(c, "OWNER COPY", page_w, A4[1])

    y = _draw_header(c, company, styles, "OWNER COPY", invoice, page_w)
    y = _draw_customer_and_info(c, invoice, styles, y, page_w)
    y = _draw_product_table(c, invoice, styles, y, page_w, show_internal=True)
    y = _draw_summary(c, invoice, styles, y, page_w, show_internal=True)
    y = _draw_payment_info(c, invoice, styles, y, page_w, show_qr=True)
    y = _draw_bank_details(c, company, styles, y, page_w)
    y = _draw_declaration_and_signatures(c, invoice, styles, y, page_w, show_customer_sig=False, company=company)

    _draw_page_footer(c, company, 1, page_w)
    c.save()
    buf.seek(0)
    return buf


def generate_customer_copy(invoice, company=None):
    company = company or COMPANY
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    styles = _get_styles()
    page_w = A4[0]

    _draw_watermark(c, "CUSTOMER COPY", page_w, A4[1])

    y = _draw_header(c, company, styles, "CUSTOMER COPY", invoice, page_w)
    y = _draw_customer_and_info(c, invoice, styles, y, page_w)
    y = _draw_product_table(c, invoice, styles, y, page_w, show_internal=False)
    y = _draw_summary(c, invoice, styles, y, page_w, show_internal=False)
    y = _draw_payment_info(c, invoice, styles, y, page_w, show_qr=True)
    y = _draw_bank_details(c, company, styles, y, page_w)
    y = _draw_declaration_and_signatures(c, invoice, styles, y, page_w, show_customer_sig=True, company=company)

    _draw_page_footer(c, company, 1, page_w)
    c.save()
    buf.seek(0)
    return buf


def generate_gst_copy(invoice, company=None):
    company = company or COMPANY
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    styles = _get_styles()
    page_w = A4[0]

    _draw_watermark(c, "GST TAX COPY", page_w, A4[1])

    y = _draw_header(c, company, styles, "GST TAX COPY", invoice, page_w)

    x_start = 30
    box_w = page_w - 60
    info_h = 28
    c.setFillColor(LIGHT_BG)
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    c.roundRect(x_start, y - info_h, box_w, info_h, 3, fill=1, stroke=1)

    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_DARK)
    col1_x = x_start + 6
    col2_x = x_start + box_w / 3
    col3_x = x_start + 2 * box_w / 3

    c.drawString(col1_x, y - 10, f"Supplier GSTIN: {company['gstin']}")
    c.drawString(col1_x, y - 20, f"Supplier State: {company['state']} ({company['state_code']})")

    c.drawString(col2_x, y - 10, f"Customer GSTIN: {invoice.customer_gstin or 'N/A'}")
    c.drawString(col2_x, y - 20, f"Customer State: {invoice.customer_state or 'N/A'} ({invoice.customer_state_code})")

    c.drawString(col3_x, y - 10, f"Place of Supply: {invoice.customer_state or 'N/A'} ({invoice.customer_state_code})")
    c.drawString(col3_x, y - 20, f"Reverse Charge: No")

    y -= info_h + 8
    y = _draw_product_table(c, invoice, styles, y, page_w, show_internal=False)

    y -= 6
    y = _draw_gst_summary_table(c, invoice, styles, y, page_w)

    y -= 10
    y = _draw_summary(c, invoice, styles, y, page_w, show_internal=False)

    amount_words = amount_to_words(invoice.grand_total)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(TEXT_DARK)
    c.drawString(x_start, y, f"Amount in Words: {amount_words}")
    y -= 14

    sig_y = y
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.3)
    sig_w = 150
    c.line(x_start, sig_y, x_start + sig_w, sig_y)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(x_start, sig_y - 10, "Digital Signature / Authorized Signatory")
    c.drawString(x_start, sig_y - 19, company["name"])

    sig_x2 = page_w - 30 - sig_w
    c.line(sig_x2, sig_y, sig_x2 + sig_w, sig_y)
    c.drawString(sig_x2, sig_y - 10, "Customer Signature & Stamp")
    c.drawString(sig_x2, sig_y - 19, "Date: _______________")

    c.setFont("Helvetica", 6)
    c.setFillColor(TEXT_MUTED)
    decl_y = sig_y - 35
    c.drawString(x_start, decl_y, "Declaration: This invoice is issued for GST return filing purposes.")
    c.drawString(x_start, decl_y - 8, "Subject to local jurisdiction. E&OE.")

    _draw_page_footer(c, company, 1, page_w)
    c.save()
    buf.seek(0)
    return buf


def generate_invoice_pdf(invoice, copy_type="customer", company=None):
    if copy_type == "owner":
        return generate_owner_copy(invoice, company)
    elif copy_type == "gst":
        return generate_gst_copy(invoice, company)
    else:
        return generate_customer_copy(invoice, company)
