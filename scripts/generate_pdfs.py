#!/usr/bin/env python3
"""
Generate Comprehensive Realistic Construction PDF Documents
Creates invoices, permits, contracts, and reports for Project A - 123 Sunset Boulevard
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import os

# Base directory for output
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICES_DIR = os.path.join(BASE_DIR, "dummy_data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid")
PERMITS_DIR = os.path.join(BASE_DIR, "dummy_data/02_PERMITS_APPROVALS")
CONTRACTS_DIR = os.path.join(BASE_DIR, "dummy_data/07_SUBCONTRACTORS/Subcontractor_Contracts")
REPORTS_DIR = os.path.join(BASE_DIR, "dummy_data/09_SITE_REPORTS_PHOTOS")

def ensure_directories():
    """Create output directories if they don't exist"""
    for directory in [INVOICES_DIR, PERMITS_DIR, CONTRACTS_DIR, REPORTS_DIR]:
        os.makedirs(directory, exist_ok=True)

# =============================================================================
# INVOICE 1: Bob's Hardware - Basic Layout
# =============================================================================
def generate_bobs_hardware_invoice():
    filename = os.path.join(INVOICES_DIR, "BH-2024-0847.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header - Left aligned, simple
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height - 1*inch, "BOB'S HARDWARE & TIMBER")

    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 1.3*inch, "123 Industrial Road, Smithfield NSW 2164")
    c.drawString(1*inch, height - 1.5*inch, "Phone: (02) 9876 5432 | ABN: 51 234 567 890")

    # TAX INVOICE title - right side
    c.setFont("Helvetica-Bold", 16)
    c.drawString(5.5*inch, height - 1*inch, "TAX INVOICE")

    # Invoice details box
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5*inch, height - 1.5*inch, "Invoice #:")
    c.drawString(5*inch, height - 1.7*inch, "Date:")
    c.drawString(5*inch, height - 1.9*inch, "Terms:")

    c.setFont("Helvetica", 10)
    c.drawString(6*inch, height - 1.5*inch, "BH-2024-0847")
    c.drawString(6*inch, height - 1.7*inch, "25 August 2024")
    c.drawString(6*inch, height - 1.9*inch, "30 Days")

    # Bill To
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, height - 2.3*inch, "BILL TO:")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 2.5*inch, "ABC Construction Pty Ltd")
    c.drawString(1*inch, height - 2.7*inch, "Project: House A - 123 Sunset Boulevard")
    c.drawString(1*inch, height - 2.9*inch, "Attention: Site Supervisor")

    # Line items table
    y_position = height - 3.5*inch

    # Table header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y_position, "Item Description")
    c.drawString(4*inch, y_position, "Qty")
    c.drawString(4.8*inch, y_position, "Unit Price")
    c.drawString(6*inch, y_position, "Amount")

    # Line
    c.line(1*inch, y_position - 5, 7*inch, y_position - 5)

    # Items
    c.setFont("Helvetica", 9)
    items = [
        ("H3 Treated Pine 90x45mm", "180 LM", "$12.50", "$2,250.00"),
        ("Galvanised Nails 75mm", "2 Box", "$45.00", "$90.00"),
        ("Screws Batten 10G 65mm", "5 Box", "$28.50", "$142.50"),
        ("Misc Fixings & Hardware", "Various", "-", "$125.00"),
    ]

    y_position -= 25
    for desc, qty, price, amount in items:
        c.drawString(1*inch, y_position, desc)
        c.drawString(4*inch, y_position, qty)
        c.drawString(4.8*inch, y_position, price)
        c.drawString(6*inch, y_position, amount)
        y_position -= 20

    # Totals
    y_position -= 20
    c.line(5.5*inch, y_position, 7*inch, y_position)

    y_position -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5.2*inch, y_position, "Subtotal:")
    c.setFont("Helvetica", 10)
    c.drawString(6*inch, y_position, "$2,607.50")

    y_position -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5.2*inch, y_position, "GST (10%):")
    c.setFont("Helvetica", 10)
    c.drawString(6*inch, y_position, "$260.75")

    y_position -= 20
    c.line(5.5*inch, y_position, 7*inch, y_position)
    y_position -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(5.2*inch, y_position, "TOTAL:")
    c.drawString(6*inch, y_position, "$2,868.25")

    # Payment details
    y_position -= 50
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y_position, "Payment Details:")
    c.setFont("Helvetica", 9)
    y_position -= 15
    c.drawString(1*inch, y_position, "Bank: Commonwealth Bank")
    y_position -= 12
    c.drawString(1*inch, y_position, "BSB: 062-000  Account: 1234 5678")
    y_position -= 12
    c.drawString(1*inch, y_position, "Please use invoice number as reference")

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 0.5*inch, "Thank you for your business!")

    c.save()
    print(f"✓ Generated: {filename}")

# =============================================================================
# INVOICE 2: ReadyMix Concrete - Professional Layout
# =============================================================================
def generate_readymix_invoice():
    filename = os.path.join(INVOICES_DIR, "RM-2024-8845.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header with border
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.rect(0.5*inch, height - 1.5*inch, width - 1*inch, 1*inch, fill=True, stroke=False)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(0.75*inch, height - 1.2*inch, "READYMIX CONCRETE PTY LTD")

    c.setFont("Helvetica", 10)
    c.drawString(0.75*inch, height - 1.4*inch, "456 Concrete Way, Eastern Creek NSW 2766 | ABN: 22 445 667 889")

    # Reset color
    c.setFillColorRGB(0, 0, 0)

    # Invoice details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.75*inch, height - 2*inch, "TAX INVOICE")

    c.setFont("Helvetica", 10)
    c.drawString(0.75*inch, height - 2.3*inch, "Invoice Number: RM-2024-8845")
    c.drawString(0.75*inch, height - 2.5*inch, "Invoice Date: 15 July 2024")
    c.drawString(0.75*inch, height - 2.7*inch, "Due Date: 14 August 2024")

    c.drawString(4.5*inch, height - 2.3*inch, "Customer Account: ABC-001")
    c.drawString(4.5*inch, height - 2.5*inch, "Delivery Ticket: DT-45632")
    c.drawString(4.5*inch, height - 2.7*inch, "Purchase Order: PO-123")

    # Customer details
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75*inch, height - 3.2*inch, "BILL TO:")
    c.setFont("Helvetica", 10)
    c.drawString(0.75*inch, height - 3.4*inch, "ABC Construction Pty Ltd")
    c.drawString(0.75*inch, height - 3.6*inch, "123 Sunset Boulevard, Sydney NSW 2000")

    # Delivery address
    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.5*inch, height - 3.2*inch, "DELIVERY ADDRESS:")
    c.setFont("Helvetica", 10)
    c.drawString(4.5*inch, height - 3.4*inch, "123 Sunset Boulevard")
    c.drawString(4.5*inch, height - 3.6*inch, "Sydney NSW 2000")

    # Line items
    y_pos = height - 4.2*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.75*inch, y_pos, "Description")
    c.drawString(3.5*inch, y_pos, "Qty")
    c.drawString(4.2*inch, y_pos, "Unit")
    c.drawString(4.8*inch, y_pos, "Rate")
    c.drawString(6*inch, y_pos, "Amount")

    c.line(0.75*inch, y_pos - 5, 7*inch, y_pos - 5)

    c.setFont("Helvetica", 9)
    y_pos -= 25
    c.drawString(0.75*inch, y_pos, "25MPa Concrete - Slab Pour")
    c.drawString(3.5*inch, y_pos, "18.5")
    c.drawString(4.2*inch, y_pos, "m³")
    c.drawString(4.8*inch, y_pos, "$245.00")
    c.drawString(6*inch, y_pos, "$4,532.50")

    y_pos -= 20
    c.drawString(0.75*inch, y_pos, "32MPa Concrete - Column Footings")
    c.drawString(3.5*inch, y_pos, "6.2")
    c.drawString(4.2*inch, y_pos, "m³")
    c.drawString(4.8*inch, y_pos, "$268.00")
    c.drawString(6*inch, y_pos, "$1,661.60")

    y_pos -= 20
    c.drawString(0.75*inch, y_pos, "Concrete Pump - 3 hours")
    c.drawString(3.5*inch, y_pos, "3")
    c.drawString(4.2*inch, y_pos, "hrs")
    c.drawString(4.8*inch, y_pos, "$185.00")
    c.drawString(6*inch, y_pos, "$555.00")

    y_pos -= 20
    c.drawString(0.75*inch, y_pos, "Waiting Time - Traffic Delay")
    c.drawString(3.5*inch, y_pos, "45")
    c.drawString(4.2*inch, y_pos, "mins")
    c.drawString(4.8*inch, y_pos, "$3.50/m")
    c.drawString(6*inch, y_pos, "$157.50")

    y_pos -= 20
    c.drawString(0.75*inch, y_pos, "Saturday Delivery Surcharge")
    c.drawString(3.5*inch, y_pos, "1")
    c.drawString(4.2*inch, y_pos, "load")
    c.drawString(4.8*inch, y_pos, "$250.00")
    c.drawString(6*inch, y_pos, "$250.00")

    # Totals
    y_pos -= 40
    c.line(5.5*inch, y_pos, 7*inch, y_pos)
    y_pos -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5.3*inch, y_pos, "Subtotal:")
    c.drawString(6*inch, y_pos, "$7,156.60")

    y_pos -= 20
    c.drawString(5.3*inch, y_pos, "GST (10%):")
    c.drawString(6*inch, y_pos, "$715.66")

    y_pos -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(5.3*inch, y_pos, "TOTAL DUE:")
    c.drawString(6*inch, y_pos, "$7,872.26")

    # Payment terms
    y_pos -= 60
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75*inch, y_pos, "Payment Terms: 30 Days from Invoice Date")
    c.setFont("Helvetica", 9)
    y_pos -= 15
    c.drawString(0.75*inch, y_pos, "Bank Details: Westpac | BSB: 032-123 | Account: 98765432")

    c.save()
    print(f"✓ Generated: {filename}")

# =============================================================================
# INVOICE 3: Solid Foundations - Progress Claim
# =============================================================================
def generate_solid_foundations_progress_claim():
    filename = os.path.join(INVOICES_DIR, "SF-PC-002.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header - Centered
    c.setFont("Times-Bold", 22)
    c.drawCentredString(width/2, height - 0.8*inch, "SOLID FOUNDATIONS PTY LTD")
    c.setFont("Times-Italic", 10)
    c.drawCentredString(width/2, height - 1.05*inch, "Concrete & Foundation Specialists")
    c.setFont("Times-Roman", 9)
    c.drawCentredString(width/2, height - 1.25*inch, "789 Foundation Street, Penrith NSW 2750")
    c.drawCentredString(width/2, height - 1.4*inch, "ABN: 33 556 778 990 | License: 123456C")

    # Progress Claim Title
    c.setFont("Times-Bold", 16)
    c.drawCentredString(width/2, height - 1.9*inch, "PROGRESS CLAIM No. 2")

    # Box for claim details
    c.rect(1*inch, height - 2.8*inch, width - 2*inch, 0.6*inch)
    c.setFont("Times-Roman", 10)
    c.drawString(1.2*inch, height - 2.3*inch, "Claim Number: SF-PC-002")
    c.drawString(1.2*inch, height - 2.5*inch, "Claim Date: 18 August 2024")
    c.drawString(1.2*inch, height - 2.7*inch, "Payment Due: 17 September 2024")

    c.drawString(4.5*inch, height - 2.3*inch, "Project: House A - 123 Sunset Blvd")
    c.drawString(4.5*inch, height - 2.5*inch, "Contract Date: 1 July 2024")
    c.drawString(4.5*inch, height - 2.7*inch, "Contract Value: $25,000.00")

    # To
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, height - 3.2*inch, "TO:")
    c.setFont("Times-Roman", 10)
    c.drawString(1*inch, height - 3.4*inch, "ABC Construction Pty Ltd")
    c.drawString(1*inch, height - 3.6*inch, "123 Sunset Boulevard, Sydney NSW")

    # Work completed
    y_pos = height - 4.1*inch
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, y_pos, "WORK COMPLETED THIS CLAIM:")

    y_pos -= 30
    c.setFont("Times-Bold", 9)
    c.drawString(1*inch, y_pos, "Item Description")
    c.drawString(5*inch, y_pos, "Amount")
    c.line(1*inch, y_pos - 5, 7*inch, y_pos - 5)

    c.setFont("Times-Roman", 9)
    y_pos -= 25
    c.drawString(1*inch, y_pos, "Concrete slab pour - 180m²")
    c.drawString(5*inch, y_pos, "$12,500.00")

    y_pos -= 20
    c.drawString(1*inch, y_pos, "Steel reinforcement supply and installation")
    c.drawString(5*inch, y_pos, "$3,800.00")

    y_pos -= 20
    c.drawString(1*inch, y_pos, "Waterproofing membrane installation")
    c.drawString(5*inch, y_pos, "$1,200.00")

    y_pos -= 20
    c.drawString(1*inch, y_pos, "Concrete finishing and curing")
    c.drawString(5*inch, y_pos, "$2,000.00")

    # Claim summary
    y_pos -= 50
    c.setFont("Times-Bold", 10)
    c.drawString(4.5*inch, y_pos, "Work This Claim:")
    c.drawString(6*inch, y_pos, "$19,500.00")

    y_pos -= 20
    c.drawString(4.5*inch, y_pos, "GST (10%):")
    c.drawString(6*inch, y_pos, "$1,950.00")

    y_pos -= 20
    c.line(5.5*inch, y_pos, 7*inch, y_pos)
    y_pos -= 25
    c.drawString(4.5*inch, y_pos, "Subtotal This Claim:")
    c.drawString(6*inch, y_pos, "$21,450.00")

    y_pos -= 25
    c.setFont("Times-Roman", 9)
    c.drawString(4.5*inch, y_pos, "Less Previous Claims:")
    c.drawString(6*inch, y_pos, "$10,000.00")

    y_pos -= 20
    c.drawString(4.5*inch, y_pos, "Less Retention (5%):")
    c.drawString(6*inch, y_pos, "$1,072.50")

    y_pos -= 20
    c.line(5.5*inch, y_pos, 7*inch, y_pos)
    y_pos -= 25
    c.setFont("Times-Bold", 12)
    c.drawString(4.5*inch, y_pos, "AMOUNT DUE:")
    c.drawString(6*inch, y_pos, "$10,377.50")

    # Statutory declaration
    y_pos -= 60
    c.setFont("Times-Bold", 9)
    c.drawString(1*inch, y_pos, "STATUTORY DECLARATION:")
    c.setFont("Times-Roman", 8)
    y_pos -= 15
    c.drawString(1*inch, y_pos, "I declare that all work claimed has been completed in accordance with the contract and")
    y_pos -= 12
    c.drawString(1*inch, y_pos, "all suppliers and subcontractors have been paid for work included in previous claims.")

    y_pos -= 30
    c.setFont("Times-Roman", 9)
    c.drawString(1*inch, y_pos, "Signed: _________________________")
    c.drawString(4.5*inch, y_pos, "Date: 18 August 2024")
    y_pos -= 20
    c.drawString(1*inch, y_pos, "Name: Michael Chen, Director")

    # Payment details
    y_pos -= 40
    c.setFont("Times-Bold", 9)
    c.drawString(1*inch, y_pos, "PAYMENT DETAILS:")
    c.setFont("Times-Roman", 8)
    y_pos -= 15
    c.drawString(1*inch, y_pos, "Bank: National Australia Bank | BSB: 084-567 | Account: 12-3456-789")

    c.save()
    print(f"✓ Generated: {filename}")

# =============================================================================
# INVOICE 4: Spark Electrical Supplies - Detailed Parts List
# =============================================================================
def generate_spark_electrical_invoice():
    filename = os.path.join(INVOICES_DIR, "SES-2024-3421.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header with box
    c.rect(0.5*inch, height - 1.2*inch, width - 1*inch, 0.7*inch)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.75*inch, height - 0.95*inch, "SPARK ELECTRICAL SUPPLIES")
    c.setFont("Helvetica", 8)
    c.drawString(0.75*inch, height - 1.1*inch, "321 Sparky Lane, Auburn NSW 2144 | Ph: (02) 9555 1234 | ABN: 44 223 445 667")

    # Invoice title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.75*inch, height - 1.6*inch, "TAX INVOICE")

    # Details
    c.setFont("Helvetica", 9)
    c.drawString(0.75*inch, height - 1.85*inch, "Invoice: SES-2024-3421")
    c.drawString(0.75*inch, height - 2.0*inch, "Date: 22 August 2024")
    c.drawString(0.75*inch, height - 2.15*inch, "Account: ABC-CONST")

    c.drawString(4.5*inch, height - 1.85*inch, "Customer PO: PO-EL-089")
    c.drawString(4.5*inch, height - 2.0*inch, "Terms: Account - 30 Days")
    c.drawString(4.5*inch, height - 2.15*inch, "Sales Rep: David L.")

    # Customer
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.75*inch, height - 2.5*inch, "BILL TO:")
    c.setFont("Helvetica", 8)
    c.drawString(0.75*inch, height - 2.65*inch, "ABC Construction Pty Ltd")
    c.drawString(0.75*inch, height - 2.8*inch, "Project: 123 Sunset Boulevard")

    # Items table header
    y_pos = height - 3.2*inch
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.75*inch, y_pos, "Code")
    c.drawString(1.3*inch, y_pos, "Description")
    c.drawString(4.2*inch, y_pos, "Qty")
    c.drawString(4.7*inch, y_pos, "Unit")
    c.drawString(5.4*inch, y_pos, "Price")
    c.drawString(6.2*inch, y_pos, "Amount")
    c.line(0.75*inch, y_pos - 5, 7*inch, y_pos - 5)

    # Line items - many items!
    items = [
        ("CW-10", "TPS Cable 2.5mm 100m", "2", "Roll", "$125.50", "$251.00"),
        ("CW-12", "TPS Cable 1.5mm 100m", "3", "Roll", "$98.00", "$294.00"),
        ("CD-20", "20mm Conduit - 3m", "15", "Ea", "$8.50", "$127.50"),
        ("SW-01", "PowerPoint 10A White", "45", "Ea", "$4.20", "$189.00"),
        ("SW-02", "Light Switch 1G White", "28", "Ea", "$3.80", "$106.40"),
        ("SW-04", "Light Switch 2G White", "12", "Ea", "$5.60", "$67.20"),
        ("LF-10", "LED Downlight 90mm", "24", "Ea", "$12.50", "$300.00"),
        ("LF-15", "Batten Holder BC", "8", "Ea", "$4.80", "$38.40"),
        ("CB-15A", "Circuit Breaker 15A", "6", "Ea", "$18.50", "$111.00"),
        ("CB-20A", "Circuit Breaker 20A", "4", "Ea", "$19.20", "$76.80"),
        ("CB-32A", "Circuit Breaker 32A", "2", "Ea", "$24.50", "$49.00"),
        ("RCD-40", "Safety Switch 40A", "2", "Ea", "$85.00", "$170.00"),
        ("JB-STD", "Junction Box Standard", "18", "Ea", "$2.80", "$50.40"),
        ("JB-LG", "Junction Box Large", "6", "Ea", "$4.50", "$27.00"),
        ("MT-10", "Mounting Block", "35", "Ea", "$1.20", "$42.00"),
        ("SC-100", "Self Tap Screws Box", "4", "Bx", "$8.50", "$34.00"),
        ("TP-BLK", "Electrical Tape Black", "12", "Ea", "$2.50", "$30.00"),
        ("WN-50", "Wire Nuts Pack 50", "6", "Pk", "$12.00", "$72.00"),
        ("FX-MIX", "Misc Fittings", "1", "Lot", "$145.00", "$145.00"),
    ]

    c.setFont("Helvetica", 7)
    y_pos -= 18
    for code, desc, qty, unit, price, amount in items:
        c.drawString(0.75*inch, y_pos, code)
        c.drawString(1.3*inch, y_pos, desc)
        c.drawString(4.2*inch, y_pos, qty)
        c.drawString(4.7*inch, y_pos, unit)
        c.drawString(5.4*inch, y_pos, price)
        c.drawString(6.2*inch, y_pos, amount)
        y_pos -= 12

    # Totals
    y_pos -= 20
    c.line(5.8*inch, y_pos, 7*inch, y_pos)
    y_pos -= 18
    c.setFont("Helvetica-Bold", 9)
    c.drawString(5.5*inch, y_pos, "Subtotal:")
    c.drawString(6.2*inch, y_pos, "$2,180.70")

    y_pos -= 15
    c.drawString(5.5*inch, y_pos, "GST (10%):")
    c.drawString(6.2*inch, y_pos, "$218.07")

    y_pos -= 15
    c.line(5.8*inch, y_pos, 7*inch, y_pos)
    y_pos -= 18
    c.setFont("Helvetica-Bold", 11)
    c.drawString(5.5*inch, y_pos, "TOTAL:")
    c.drawString(6.2*inch, y_pos, "$2,398.77")

    # Footer
    c.setFont("Helvetica", 7)
    c.drawString(0.75*inch, 0.6*inch, "Payment: Direct Deposit | CBA | BSB: 062-000 | Account: 1122-3344")
    c.drawString(0.75*inch, 0.5*inch, "All goods remain property of Spark Electrical Supplies until paid in full")

    c.save()
    print(f"✓ Generated: {filename}")

# =============================================================================
# INVOICE 5: Aqua Plumbing Supplies
# =============================================================================
def generate_aqua_plumbing_invoice():
    filename = os.path.join(INVOICES_DIR, "APS-2024-8912.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Simple header
    c.setFont("Courier-Bold", 16)
    c.drawString(1*inch, height - 0.8*inch, "AQUA PLUMBING SUPPLIES")
    c.setFont("Courier", 9)
    c.drawString(1*inch, height - 1*inch, "654 Water Street, Parramatta NSW 2150")
    c.drawString(1*inch, height - 1.15*inch, "ABN: 55 667 889 001 | Phone: 02 9876 1111")

    c.setFont("Courier-Bold", 12)
    c.drawString(1*inch, height - 1.5*inch, "TAX INVOICE")

    c.setFont("Courier", 9)
    c.drawString(1*inch, height - 1.75*inch, "Invoice#: APS-2024-8912")
    c.drawString(1*inch, height - 1.9*inch, "Date: 20 August 2024")
    c.drawString(1*inch, height - 2.05*inch, "Terms: COD")

    c.drawString(4.5*inch, height - 1.75*inch, "Customer: ABC Construction")
    c.drawString(4.5*inch, height - 1.9*inch, "Job: Sunset Blvd Project")
    c.drawString(4.5*inch, height - 2.05*inch, "Collected By: Site Team")

    # Items
    y_pos = height - 2.5*inch
    c.setFont("Courier-Bold", 9)
    c.drawString(1*inch, y_pos, "ITEM")
    c.drawString(3.5*inch, y_pos, "QTY")
    c.drawString(4.3*inch, y_pos, "UNIT")
    c.drawString(5*inch, y_pos, "PRICE")
    c.drawString(6*inch, y_pos, "TOTAL")
    c.drawString(1*inch, y_pos - 10, "=" * 70)

    c.setFont("Courier", 8)
    items = [
        ("Copper Pipe 15mm x 3m", "12", "Ea", "$18.50", "$222.00"),
        ("Copper Pipe 20mm x 3m", "8", "Ea", "$28.00", "$224.00"),
        ("PEX Pipe 20mm x 50m", "1", "Roll", "$245.00", "$245.00"),
        ("90deg Elbow 15mm Copper", "40", "Ea", "$2.80", "$112.00"),
        ("90deg Elbow 20mm Copper", "25", "Ea", "$4.20", "$105.00"),
        ("T-Piece 15mm Copper", "18", "Ea", "$3.50", "$63.00"),
        ("Basin Mixer Chrome", "3", "Ea", "$125.00", "$375.00"),
        ("Shower Mixer Chrome", "2", "Ea", "$185.00", "$370.00"),
        ("Kitchen Mixer Pull-Out", "1", "Ea", "$245.00", "$245.00"),
        ("Toilet Suite Ceramic", "3", "Ea", "$380.00", "$1,140.00"),
        ("PVC Pipe 100mm x 3m", "6", "Ea", "$32.00", "$192.00"),
        ("PVC Bend 100mm", "8", "Ea", "$12.50", "$100.00"),
        ("Solder 500g", "2", "Ea", "$42.00", "$84.00"),
        ("Flux Paste 500ml", "1", "Ea", "$18.00", "$18.00"),
        ("Teflon Tape", "10", "Roll", "$2.50", "$25.00"),
    ]

    y_pos -= 25
    for desc, qty, unit, price, total in items:
        c.drawString(1*inch, y_pos, desc)
        c.drawString(3.5*inch, y_pos, qty)
        c.drawString(4.3*inch, y_pos, unit)
        c.drawString(5*inch, y_pos, price)
        c.drawString(6*inch, y_pos, total)
        y_pos -= 15

    y_pos -= 10
    c.drawString(1*inch, y_pos, "-" * 70)

    y_pos -= 20
    c.setFont("Courier-Bold", 9)
    c.drawString(5*inch, y_pos, "Subtotal:")
    c.drawString(6*inch, y_pos, "$3,520.00")

    y_pos -= 15
    c.drawString(5*inch, y_pos, "GST 10%:")
    c.drawString(6*inch, y_pos, "$352.00")

    y_pos -= 15
    c.drawString(1*inch, y_pos, "=" * 70)

    y_pos -= 20
    c.setFont("Courier-Bold", 11)
    c.drawString(5*inch, y_pos, "TOTAL:")
    c.drawString(6*inch, y_pos, "$3,872.00")

    y_pos -= 40
    c.setFont("Courier", 8)
    c.drawString(1*inch, y_pos, "PAID - Cash on Delivery - Thank You!")

    c.setFont("Courier", 7)
    c.drawString(1*inch, 0.5*inch, "Goods sold are not returnable without prior authorization")

    c.save()
    print(f"✓ Generated: {filename}")

# Continue in next part...

if __name__ == "__main__":
    ensure_directories()
    print("Generating PDF invoices and documents...")
    print("\n=== Supplier Invoices ===")
    generate_bobs_hardware_invoice()
    generate_readymix_invoice()
    generate_solid_foundations_progress_claim()
    generate_spark_electrical_invoice()
    generate_aqua_plumbing_invoice()
