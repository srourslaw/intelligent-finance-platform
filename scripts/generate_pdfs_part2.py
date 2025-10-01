#!/usr/bin/env python3
"""
Part 2: Remaining invoices, permits, contracts, and reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICES_DIR = os.path.join(BASE_DIR, "dummy_data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid")
PERMITS_DIR = os.path.join(BASE_DIR, "dummy_data/02_PERMITS_APPROVALS")
CONTRACTS_DIR = os.path.join(BASE_DIR, "dummy_data/07_SUBCONTRACTORS/Subcontractor_Contracts")
REPORTS_DIR = os.path.join(BASE_DIR, "dummy_data/09_SITE_REPORTS_PHOTOS")

# =============================================================================
# INVOICE 6: BuildRight Framers - Progress Claim
# =============================================================================
def generate_buildright_framers_invoice():
    filename = os.path.join(INVOICES_DIR, "BR-PC-003.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height - 1*inch, "BuildRight Framers")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, height - 1.2*inch, "Unit 5, 42 Timber Way, Blacktown NSW 2148")
    c.drawString(1*inch, height - 1.35*inch, "ABN: 66 778 889 991 | Lic: 234567C")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(5*inch, height - 1*inch, "PROGRESS CLAIM #3")

    c.setFont("Helvetica", 9)
    c.drawString(1*inch, height - 1.7*inch, "Claim No: BR-PC-003")
    c.drawString(1*inch, height - 1.85*inch, "Date: 5 September 2024")
    c.drawString(1*inch, height - 2*inch, "For Period: 1-31 August 2024")

    c.drawString(4.5*inch, height - 1.7*inch, "Project: 123 Sunset Boulevard")
    c.drawString(4.5*inch, height - 1.85*inch, "Contract: BRF-2024-089")
    c.drawString(4.5*inch, height - 2*inch, "Client: ABC Construction")

    # Work breakdown
    y_pos = height - 2.5*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y_pos, "Work Completed:")

    y_pos -= 25
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "Description")
    c.drawString(4.5*inch, y_pos, "% Complete")
    c.drawString(5.5*inch, y_pos, "Amount")
    c.line(1*inch, y_pos - 5, 7*inch, y_pos - 5)

    y_pos -= 20
    c.drawString(1*inch, y_pos, "Frame supply and installation")
    c.drawString(4.5*inch, y_pos, "95%")
    c.drawString(5.5*inch, y_pos, "$38,000.00")

    y_pos -= 18
    c.drawString(1*inch, y_pos, "Wall frames - external and internal")
    c.drawString(5.5*inch, y_pos, "$28,500.00")

    y_pos -= 18
    c.drawString(1*inch, y_pos, "Roof trusses supply and install")
    c.drawString(5.5*inch, y_pos, "$12,000.00")

    y_pos -= 18
    c.drawString(1*inch, y_pos, "Sarking and bracing")
    c.drawString(5.5*inch, y_pos, "$6,200.00")

    # Totals
    y_pos -= 40
    c.setFont("Helvetica-Bold", 10)
    c.drawString(4.5*inch, y_pos, "Work This Claim:")
    c.drawString(5.5*inch, y_pos, "$46,500.00")

    y_pos -= 18
    c.setFont("Helvetica", 9)
    c.drawString(4.5*inch, y_pos, "GST (10%):")
    c.drawString(5.5*inch, y_pos, "$4,650.00")

    y_pos -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(4.5*inch, y_pos, "Subtotal:")
    c.drawString(5.5*inch, y_pos, "$51,150.00")

    y_pos -= 20
    c.setFont("Helvetica", 9)
    c.drawString(4.5*inch, y_pos, "Less Previous Claims:")
    c.drawString(5.5*inch, y_pos, "$25,000.00")

    y_pos -= 18
    c.drawString(4.5*inch, y_pos, "Less Retention (5%):")
    c.drawString(5.5*inch, y_pos, "$2,557.50")

    y_pos -= 20
    c.line(5*inch, y_pos, 7*inch, y_pos)
    y_pos -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(4.5*inch, y_pos, "AMOUNT DUE:")
    c.drawString(5.5*inch, y_pos, "$23,592.50")

    y_pos -= 50
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, y_pos, "Payment Details: NAB | BSB: 084-123 | Account: 55667788")
    y_pos -= 15
    c.drawString(1*inch, y_pos, "Retention to be released upon practical completion and defects rectification")

    c.save()
    print(f"✓ Generated: {filename}")

# =============================================================================
# INVOICE 7-10: Remaining Supplier Invoices (Simplified)
# =============================================================================
def generate_timber_supplies_invoice():
    filename = os.path.join(INVOICES_DIR, "TSC-INV-4421.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(4.25*inch, 10*inch, "TIMBER SUPPLIES CO.")
    c.setFont("Helvetica", 9)
    c.drawCentredString(4.25*inch, 9.75*inch, "987 Sawmill Road, Prospect NSW 2148 | ABN: 77 889 990 112")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 9.3*inch, "INVOICE: TSC-INV-4421")
    c.drawString(1*inch, 9.1*inch, "Date: 10 August 2024")
    c.drawString(5*inch, 9.1*inch, "Terms: 7 Days")

    c.setFont("Helvetica", 9)
    c.drawString(1*inch, 8.7*inch, "Bill To: ABC Construction - Sunset Blvd Project")

    y = 8.2*inch
    items = [
        ("F17 Hardwood 90x45 - 5.4m", "85 LM", "$15.50/LM", "$1,317.50"),
        ("MGP10 Pine 90x35 - 4.8m", "120 LM", "$9.80/LM", "$1,176.00"),
        ("Plywood 17mm F/C 2400x1200", "24 Sht", "$68.00", "$1,632.00"),
        ("LVL Beam 240x45 - 7.2m", "6 Ea", "$185.00", "$1,110.00"),
    ]

    for desc, qty, price, amt in items:
        c.drawString(1*inch, y, desc)
        c.drawString(4*inch, y, qty)
        c.drawString(5*inch, y, price)
        c.drawString(6.2*inch, y, amt)
        y -= 0.2*inch

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5.5*inch, y, "Subtotal: $5,235.50")
    y -= 0.2*inch
    c.drawString(5.5*inch, y, "GST: $523.55")
    y -= 0.2*inch
    c.drawString(5.5*inch, y, "TOTAL: $5,759.05")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_top_roof_invoice():
    filename = os.path.join(INVOICES_DIR, "TR-2024-156.pdf")
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, 11*inch, "TOP ROOF TILERS")
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 10.8*inch, "15 Ridge Street, Seven Hills NSW 2147 | ABN: 88 990 112 233 | Lic: 345678C")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, 10.4*inch, "TAX INVOICE: TR-2024-156")
    c.drawString(1*inch, 10.2*inch, "Date: 28 August 2024")

    c.setFont("Helvetica", 9)
    c.drawString(1*inch, 9.8*inch, "To: ABC Construction Pty Ltd")
    c.drawString(1*inch, 9.65*inch, "Project: 123 Sunset Boulevard")

    y = 9.2*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "Description")
    c.drawString(5.5*inch, y, "Amount")

    c.setFont("Helvetica", 9)
    y -= 0.25*inch
    c.drawString(1*inch, y, "Terracotta Roof Tiles - Supply & Install (185m²)")
    c.drawString(5.5*inch, y, "$15,800.00")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Ridge Capping and Flashing")
    c.drawString(5.5*inch, y, "$2,850.00")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Sarking and Battens")
    c.drawString(5.5*inch, y, "$3,200.00")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Colorbond Gutters and Downpipes")
    c.drawString(5.5*inch, y, "$1,800.00")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5*inch, y, "Subtotal:")
    c.drawString(5.5*inch, y, "$23,650.00")
    y -= 0.2*inch
    c.drawString(5*inch, y, "GST:")
    c.drawString(5.5*inch, y, "$2,365.00")
    y -= 0.2*inch
    c.drawString(5*inch, y, "TOTAL:")
    c.drawString(5.5*inch, y, "$26,015.00")

    c.setFont("Helvetica", 7)
    c.drawString(1*inch, 1*inch, "Payment: Bank Transfer | Westpac BSB: 032-456 | Acc: 11223344")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_tonys_brickwork_invoice():
    filename = os.path.join(INVOICES_DIR, "TB-PC-001.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Times-Bold", 18)
    c.drawString(1*inch, 10.5*inch, "Tony's Brickwork & Blocklaying")
    c.setFont("Times-Roman", 9)
    c.drawString(1*inch, 10.3*inch, "Mobile: 0412 345 678 | ABN: 99 112 233 445 | Lic: 456789C")

    c.setFont("Times-Bold", 12)
    c.drawString(1*inch, 9.9*inch, "Payment Claim No. 1")
    c.drawString(1*inch, 9.7*inch, "Claim: TB-PC-001")
    c.drawString(1*inch, 9.5*inch, "Date: 15 August 2024")

    c.setFont("Times-Roman", 9)
    c.drawString(1*inch, 9.1*inch, "Client: ABC Construction Pty Ltd")
    c.drawString(1*inch, 8.95*inch, "Site: 123 Sunset Boulevard, Sydney")

    y = 8.5*inch
    c.setFont("Times-Bold", 9)
    c.drawString(1*inch, y, "Work Item")
    c.drawString(5.5*inch, y, "Amount")
    c.line(1*inch, y - 0.05*inch, 7*inch, y - 0.05*inch)

    c.setFont("Times-Roman", 9)
    y -= 0.25*inch
    c.drawString(1*inch, y, "Face Brickwork - 142m² @ $180/m²")
    c.drawString(5.5*inch, y, "$25,560.00")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Bricks supplied (10,000 @ $1.20)")
    c.drawString(5.5*inch, y, "$12,000.00")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Mortar and materials")
    c.drawString(5.5*inch, y, "$2,400.00")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Scaffolding hire (4 weeks)")
    c.drawString(5.5*inch, y, "$2,540.00")

    y -= 0.4*inch
    c.setFont("Times-Bold", 10)
    c.drawString(5*inch, y, "Subtotal:")
    c.drawString(5.5*inch, y, "$42,500.00")
    y -= 0.2*inch
    c.drawString(5*inch, y, "GST 10%:")
    c.drawString(5.5*inch, y, "$4,250.00")
    y -= 0.25*inch
    c.drawString(5*inch, y, "TOTAL:")
    c.drawString(5.5*inch, y, "$46,750.00")

    y -= 0.5*inch
    c.setFont("Times-Roman", 8)
    c.drawString(1*inch, y, "Bank: CBA | BSB: 062-789 | Account: 9988-7766")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_pacific_paint_invoice():
    filename = os.path.join(INVOICES_DIR, "PPS-8834.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, 10.5*inch, "PACIFIC PAINT SUPPLIES")
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 10.3*inch, "234 Paint Place, St Marys NSW 2760 | Ph: 02 9833 1234 | ABN: 11 223 344 556")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, 9.9*inch, "INVOICE: PPS-8834")
    c.drawString(5*inch, 9.9*inch, "Date: 2 September 2024")
    c.drawString(5*inch, 9.7*inch, "Account: ABC-CONST")

    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 9.5*inch, "Customer: ABC Construction | Project: Sunset Boulevard")

    y = 9*inch
    items = [
        ("Dulux Weathershield Ext White 15L", "8", "$145.00", "$1,160.00"),
        ("Dulux Wash&Wear Int Low Sheen 15L", "12", "$125.00", "$1,500.00"),
        ("Dulux Ceiling White 15L", "6", "$98.00", "$588.00"),
        ("Exterior Primer Sealer 15L", "4", "$110.00", "$440.00"),
        ("Interior Undercoat 15L", "5", "$95.00", "$475.00"),
        ("Gloss Enamel Trim Paint 4L", "8", "$68.00", "$544.00"),
        ("Paint Rollers 270mm", "24", "$8.50", "$204.00"),
        ("Paint Brushes Assorted", "36", "$12.00", "$432.00"),
        ("Masking Tape 48mm", "12", "$5.50", "$66.00"),
        ("Drop Sheets Heavy Duty", "8", "$22.00", "$176.00"),
    ]

    c.setFont("Helvetica-Bold", 8)
    c.drawString(1*inch, y, "Description")
    c.drawString(4*inch, y, "Qty")
    c.drawString(4.8*inch, y, "Unit $")
    c.drawString(6*inch, y, "Total")
    y -= 0.15*inch

    c.setFont("Helvetica", 7)
    for desc, qty, price, total in items:
        c.drawString(1*inch, y, desc)
        c.drawString(4*inch, y, qty)
        c.drawString(4.8*inch, y, price)
        c.drawString(6*inch, y, total)
        y -= 0.15*inch

    y -= 0.2*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(5.3*inch, y, "Subtotal: $5,585.00")
    y -= 0.15*inch
    c.drawString(5.3*inch, y, "GST: $558.50")
    y -= 0.15*inch
    c.drawString(5.3*inch, y, "TOTAL: $6,143.50")

    c.save()
    print(f"✓ Generated: {filename}")

# =============================================================================
# PERMITS AND APPROVALS
# =============================================================================
def generate_building_permit():
    filename = os.path.join(PERMITS_DIR, "Building_Permit_APPROVED.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Official header
    c.setFillColorRGB(0.1, 0.2, 0.5)
    c.rect(0, height - 1.5*inch, width, 1.5*inch, fill=True, stroke=False)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 0.8*inch, "SYDNEY COUNCIL")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 1.1*inch, "Building Certification Services")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, height - 1.3*inch, "123 Council Street, Sydney NSW 2000 | Phone: 02 9999 8888")

    c.setFillColorRGB(0, 0, 0)

    # Permit title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 2*inch, "BUILDING PERMIT - APPROVED")

    # Permit details box
    c.rect(1*inch, height - 3*inch, width - 2*inch, 0.8*inch)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1.2*inch, height - 2.4*inch, "Permit Number:")
    c.drawString(1.2*inch, height - 2.6*inch, "Issue Date:")
    c.drawString(1.2*inch, height - 2.8*inch, "Expiry Date:")

    c.setFont("Helvetica", 11)
    c.drawString(2.5*inch, height - 2.4*inch, "BP-2024-08756")
    c.drawString(2.5*inch, height - 2.6*inch, "15 January 2024")
    c.drawString(2.5*inch, height - 2.8*inch, "15 January 2026")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.5*inch, height - 2.4*inch, "Development Type:")
    c.drawString(4.5*inch, height - 2.6*inch, "Estimated Value:")
    c.drawString(4.5*inch, height - 2.8*inch, "Class of Building:")

    c.setFont("Helvetica", 11)
    c.drawString(6*inch, height - 2.4*inch, "New Dwelling")
    c.drawString(6*inch, height - 2.6*inch, "$650,000")
    c.drawString(6*inch, height - 2.8*inch, "Class 1a")

    # Property details
    y_pos = height - 3.5*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "PROPERTY DETAILS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y_pos, "Address: 123 Sunset Boulevard, Sydney NSW 2000")
    y_pos -= 0.2*inch
    c.drawString(1*inch, y_pos, "Lot/DP: Lot 45 DP 123456")
    y_pos -= 0.2*inch
    c.drawString(1*inch, y_pos, "Owner: John & Mary Smith")
    y_pos -= 0.2*inch
    c.drawString(1*inch, y_pos, "Builder: ABC Construction Pty Ltd (Lic: 123456C)")

    # Approved works
    y_pos -= 0.5*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "APPROVED WORKS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y_pos, "Construction of new two-storey residential dwelling including:")
    y_pos -= 0.2*inch
    c.drawString(1.3*inch, y_pos, "• Total floor area: 245m²")
    y_pos -= 0.18*inch
    c.drawString(1.3*inch, y_pos, "• 4 bedrooms, 2.5 bathrooms, double garage")
    y_pos -= 0.18*inch
    c.drawString(1.3*inch, y_pos, "• Concrete slab on ground foundation")
    y_pos -= 0.18*inch
    c.drawString(1.3*inch, y_pos, "• Timber frame construction with brick veneer")
    y_pos -= 0.18*inch
    c.drawString(1.3*inch, y_pos, "• Terracotta tile roof")

    # Mandatory inspections
    y_pos -= 0.4*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "MANDATORY INSPECTIONS REQUIRED")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    inspections = [
        "1. Excavation and footings before concrete pour",
        "2. Foundation and slab reinforcement before pour",
        "3. Frame inspection before cladding",
        "4. Wet area waterproofing before tiling",
        "5. Stormwater drainage before backfill",
        "6. Final inspection before occupation",
    ]
    for inspection in inspections:
        c.drawString(1.2*inch, y_pos, inspection)
        y_pos -= 0.18*inch

    # Conditions
    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y_pos, "CONDITIONS OF APPROVAL")

    y_pos -= 0.2*inch
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, y_pos, "This permit is valid for 2 years. All work must comply with the Building Code of Australia and approved plans.")
    y_pos -= 0.15*inch
    c.drawString(1*inch, y_pos, "Builder must notify Council 48 hours before each mandatory inspection.")

    # Signature
    y_pos -= 0.5*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "Approved by: ___Sarah Mitchell___")
    c.drawString(4.5*inch, y_pos, "Date: 15 January 2024")
    y_pos -= 0.2*inch
    c.drawString(1*inch, y_pos, "Building Surveyor, Sydney Council")
    c.drawString(4.5*inch, y_pos, "[OFFICIAL SEAL]")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_development_approval():
    filename = os.path.join(PERMITS_DIR, "Development_Approval.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(4.25*inch, 10.5*inch, "SYDNEY COUNCIL")
    c.setFont("Helvetica", 10)
    c.drawCentredString(4.25*inch, 10.25*inch, "Development Assessment")

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(4.25*inch, 9.8*inch, "NOTICE OF DETERMINATION")
    c.drawCentredString(4.25*inch, 9.55*inch, "Development Application APPROVED")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, 9*inch, "DA Number:")
    c.drawString(1*inch, 8.8*inch, "Determination Date:")
    c.drawString(1*inch, 8.6*inch, "Property:")

    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, 9*inch, "DA-2023-3456")
    c.drawString(2.5*inch, 8.8*inch, "20 December 2023")
    c.drawString(2.5*inch, 8.6*inch, "123 Sunset Boulevard, Sydney NSW 2000")

    y = 8.2*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "DEVELOPMENT CONSENT GRANTED")

    y -= 0.3*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y, "Description: Demolition of existing structures and construction of new two-storey dwelling")

    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "CONDITIONS OF CONSENT:")

    y -= 0.25*inch
    c.setFont("Helvetica", 8)
    conditions = [
        "1. Development must be carried out in accordance with approved plans dated 15/12/2023",
        "2. Construction Certificate required before commencement",
        "3. Erosion and sediment control measures to be in place before excavation",
        "4. Construction hours: Monday-Friday 7am-6pm, Saturday 8am-1pm, no work Sundays/Public Holidays",
        "5. Section 94 contribution of $8,500 payable before CC issue",
        "6. Stormwater to be connected to Council system",
        "7. Landscaping to be completed before Occupation Certificate",
    ]
    for condition in conditions:
        c.drawString(1*inch, y, condition)
        y -= 0.18*inch

    y -= 0.3*inch
    c.setFont("Helvetica", 7)
    c.drawString(1*inch, y, "This consent expires 5 years from date of determination if work not commenced.")

    y -= 0.5*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y, "Approved by: James Wilson, Senior Planner")
    c.drawString(1*inch, y - 0.2*inch, "Date: 20 December 2023")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_electrical_certificate():
    filename = os.path.join(PERMITS_DIR, "Electrical_Certificate_of_Compliance.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(4.25*inch, 10.5*inch, "CERTIFICATE OF ELECTRICAL COMPLIANCE")
    c.setFont("Helvetica", 9)
    c.drawCentredString(4.25*inch, 10.25*inch, "AS/NZS 3000:2018 Wiring Rules")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, 9.7*inch, "Certificate No: EC-2024-8945")
    c.drawString(1*inch, 9.5*inch, "Issue Date: 25 September 2024")

    c.setFont("Helvetica", 9)
    c.drawString(1*inch, 9.1*inch, "Property: 123 Sunset Boulevard, Sydney NSW 2000")
    c.drawString(1*inch, 8.95*inch, "Owner: John & Mary Smith")
    c.drawString(1*inch, 8.8*inch, "Builder: ABC Construction Pty Ltd")

    y = 8.4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "ELECTRICAL WORK COMPLETED:")

    c.setFont("Helvetica", 9)
    y -= 0.25*inch
    c.drawString(1*inch, y, "Complete electrical installation for new two-storey dwelling including:")
    y -= 0.2*inch
    c.drawString(1.2*inch, y, "• Main switchboard with RCD protection")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Power circuits (20x), Lighting circuits (12x)")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Power points (45x), Light switches (28x), Light fittings (32x)")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Hardwired smoke alarms interconnected (6x)")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Hot water system connection, Oven/cooktop circuits")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "TEST RESULTS:")

    y -= 0.25*inch
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, y, "Test")
    c.drawString(3.5*inch, y, "Result")
    c.drawString(5*inch, y, "Standard")
    c.line(1*inch, y - 0.05*inch, 7*inch, y - 0.05*inch)

    y -= 0.2*inch
    tests = [
        ("Insulation Resistance", ">100 MΩ", ">1 MΩ"),
        ("Earth Continuity", "<0.5 Ω", "<1 Ω"),
        ("RCD Trip Time (30mA)", "18ms", "<300ms"),
        ("Polarity", "Correct", "Correct"),
    ]
    for test, result, standard in tests:
        c.drawString(1*inch, y, test)
        c.drawString(3.5*inch, y, result)
        c.drawString(5*inch, y, standard)
        y -= 0.18*inch

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "DECLARATION:")
    c.setFont("Helvetica", 8)
    y -= 0.2*inch
    c.drawString(1*inch, y, "I certify that the electrical installation work detailed above has been carried out in accordance")
    y -= 0.15*inch
    c.drawString(1*inch, y, "with AS/NZS 3000:2018 and is safe to connect and use.")

    y -= 0.4*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y, "Licensed Electrician: David Patterson")
    y -= 0.18*inch
    c.drawString(1*inch, y, "License Number: EL-123456")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Company: Bright Spark Electrical Pty Ltd")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Signature: _D. Patterson_")
    c.drawString(4*inch, y, "Date: 25 September 2024")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_plumbing_certificate():
    filename = os.path.join(PERMITS_DIR, "Plumbing_Compliance_Certificate.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(4.25*inch, 10.5*inch, "PLUMBING COMPLIANCE CERTIFICATE")
    c.setFont("Helvetica", 9)
    c.drawCentredString(4.25*inch, 10.25*inch, "AS/NZS 3500 Plumbing and Drainage Standards")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, 9.7*inch, "Certificate No: PC-2024-7823")
    c.drawString(1*inch, 9.5*inch, "Issue Date: 28 September 2024")

    c.setFont("Helvetica", 9)
    c.drawString(1*inch, 9.1*inch, "Property: 123 Sunset Boulevard, Sydney NSW 2000")
    c.drawString(1*inch, 8.95*inch, "Owner: John & Mary Smith")

    y = 8.5*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "PLUMBING WORK COMPLETED:")

    c.setFont("Helvetica", 9)
    y -= 0.25*inch
    c.drawString(1*inch, y, "Complete plumbing installation including:")
    y -= 0.2*inch
    c.drawString(1.2*inch, y, "• Cold water supply system (copper & PEX)")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Hot water system - 315L electric storage")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Sanitary drainage (100mm & 150mm PVC)")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Stormwater drainage connected to Council system")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Fixtures: 3x toilets, 3x basins, 2x showers, 1x bath, 1x kitchen sink")
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Backflow prevention devices installed")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "PRESSURE TEST RESULTS:")

    c.setFont("Helvetica", 9)
    y -= 0.25*inch
    c.drawString(1*inch, y, "Cold water system: Tested 24 hours @ 1500kPa - PASS")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Hot water system: Tested 24 hours @ 1000kPa - PASS")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Drainage system: Water test all fixtures - PASS")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "CERTIFICATION:")
    c.setFont("Helvetica", 8)
    y -= 0.2*inch
    c.drawString(1*inch, y, "I certify that the plumbing work detailed above complies with AS/NZS 3500 and")
    y -= 0.15*inch
    c.drawString(1*inch, y, "has been installed in a safe and workmanlike manner.")

    y -= 0.4*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y, "Licensed Plumber: Robert Chen")
    y -= 0.18*inch
    c.drawString(1*inch, y, "License Number: PL-234567")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Company: John's Plumbing Services Pty Ltd")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Signature: _R. Chen_")
    c.drawString(4*inch, y, "Date: 28 September 2024")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_occupancy_certificate():
    filename = os.path.join(PERMITS_DIR, "Occupancy_Certificate.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    # Header
    c.setFillColorRGB(0.1, 0.3, 0.5)
    c.rect(0, 10.5*inch, 8.5*inch, 0.9*inch, fill=True, stroke=False)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(4.25*inch, 10.85*inch, "SYDNEY COUNCIL")
    c.setFont("Helvetica", 10)
    c.drawCentredString(4.25*inch, 10.65*inch, "Building Certification")

    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(4.25*inch, 10*inch, "OCCUPATION CERTIFICATE")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(4.25*inch, 9.75*inch, "(Final)")

    c.rect(1*inch, 9*inch, 6.5*inch, 0.5*inch)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1.2*inch, 9.3*inch, "OC Number: OC-2024-5623")
    c.drawString(4*inch, 9.3*inch, "Issue Date: 30 September 2024")

    y = 8.6*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "PROPERTY DETAILS:")
    c.setFont("Helvetica", 9)
    y -= 0.2*inch
    c.drawString(1*inch, y, "Address: 123 Sunset Boulevard, Sydney NSW 2000")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Lot/DP: Lot 45 DP 123456")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Owner: John & Mary Smith")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Building Permit: BP-2024-08756")
    y -= 0.18*inch
    c.drawString(1*inch, y, "DA Approval: DA-2023-3456")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "DEVELOPMENT APPROVED FOR OCCUPATION:")
    c.setFont("Helvetica", 9)
    y -= 0.2*inch
    c.drawString(1*inch, y, "New two-storey residential dwelling - Class 1a")
    y -= 0.18*inch
    c.drawString(1*inch, y, "4 bedrooms, 2.5 bathrooms, double garage")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Total floor area: 245m²")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "COMPLIANCE CERTIFICATES SIGHTED:")
    c.setFont("Helvetica", 8)
    y -= 0.2*inch
    c.drawString(1.2*inch, y, "✓ Electrical Compliance Certificate (EC-2024-8945) - 25/09/2024")
    y -= 0.15*inch
    c.drawString(1.2*inch, y, "✓ Plumbing Compliance Certificate (PC-2024-7823) - 28/09/2024")
    y -= 0.15*inch
    c.drawString(1.2*inch, y, "✓ Final Building Inspection - 30/09/2024")
    y -= 0.15*inch
    c.drawString(1.2*inch, y, "✓ Mandatory Fire Safety Measures Certificate")
    y -= 0.15*inch
    c.drawString(1.2*inch, y, "✓ Smoke Alarm Compliance Certificate")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "CERTIFICATION:")
    c.setFont("Helvetica", 8)
    y -= 0.2*inch
    c.drawString(1*inch, y, "I certify that the building work described above:")
    y -= 0.15*inch
    c.drawString(1.2*inch, y, "• Has been completed in accordance with the Building Code of Australia")
    y -= 0.15*inch
    c.drawString(1.2*inch, y, "• Complies with the development consent and building permit")
    y -= 0.15*inch
    c.drawString(1.2*inch, y, "• Is suitable for occupation")

    y -= 0.4*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y, "Building Surveyor: Sarah Mitchell")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Accreditation: BS-45678")
    y -= 0.18*inch
    c.drawString(1*inch, y, "Signature: _S. Mitchell_")
    c.drawString(4*inch, y, "Date: 30 September 2024")
    y -= 0.18*inch
    c.drawString(4*inch, y, "[OFFICIAL SEAL]")

    c.save()
    print(f"✓ Generated: {filename}")

# Continue to part 3 for contracts and reports...

if __name__ == "__main__":
    print("\n=== Part 2: Additional Invoices ===")
    generate_buildright_framers_invoice()
    generate_timber_supplies_invoice()
    generate_top_roof_invoice()
    generate_tonys_brickwork_invoice()
    generate_pacific_paint_invoice()

    print("\n=== Official Permits and Approvals ===")
    generate_building_permit()
    generate_development_approval()
    generate_electrical_certificate()
    generate_plumbing_certificate()
    generate_occupancy_certificate()
