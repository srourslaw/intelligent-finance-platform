"""
Generate ENHANCED realistic PDF files with professional formatting
- Company banners and branding
- Comprehensive tables and line items
- Multi-page documents
- Professional styling
"""
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime, timedelta
import random

BASE_DIR = Path("/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-a-123-sunset-blvd/data")

def draw_professional_header(c, company_name, company_color, abn, address, phone, email):
    """Draw professional company header with banner"""
    width, height = letter

    # Draw colored banner at top
    c.setFillColor(company_color)
    c.rect(0, height - 1.2*inch, width, 1.2*inch, fill=True, stroke=False)

    # Company name in white
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(0.75*inch, height - 0.7*inch, company_name)

    # Company details in white (smaller font)
    c.setFont("Helvetica", 9)
    c.drawString(0.75*inch, height - 0.95*inch, f"ABN: {abn} | {address}")
    c.drawString(0.75*inch, height - 1.1*inch, f"Phone: {phone} | Email: {email}")

    # Draw thin line below header
    c.setStrokeColor(company_color)
    c.setLineWidth(3)
    c.line(0, height - 1.25*inch, width, height - 1.25*inch)

    return height - 1.4*inch  # Return y position after header

def draw_footer(c, page_num):
    """Draw professional footer"""
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(4.25*inch, 0.5*inch, f"Page {page_num}")
    c.drawCentredString(4.25*inch, 0.35*inch, "This is a computer-generated document")

def create_detailed_invoice(filepath, invoice_data):
    """Create a comprehensive multi-page invoice"""
    c = canvas.Canvas(str(filepath), pagesize=letter)
    width, height = letter

    # Header
    y = draw_professional_header(
        c,
        invoice_data['company_name'],
        invoice_data['company_color'],
        invoice_data['abn'],
        invoice_data['address'],
        invoice_data['phone'],
        invoice_data['email']
    )

    # Document title
    c.setFillColor(invoice_data['company_color'])
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.75*inch, y, "TAX INVOICE")

    y -= 0.3*inch
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75*inch, y, f"Invoice No: {invoice_data['invoice_no']}")
    c.drawRightString(width - 0.75*inch, y, f"Date: {invoice_data['date']}")

    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 0.75*inch, y, f"Due Date: {invoice_data['due_date']}")

    y -= 0.4*inch

    # Bill To section with box
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.rect(0.75*inch, y - 0.9*inch, 3*inch, 1*inch, stroke=True, fill=False)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.85*inch, y, "BILL TO:")
    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.drawString(0.85*inch, y, "Sunset Construction Pty Ltd")
    y -= 0.15*inch
    c.drawString(0.85*inch, y, "ABN: 12 345 678 901")
    y -= 0.15*inch
    c.drawString(0.85*inch, y, "123 Sunset Boulevard")
    y -= 0.15*inch
    c.drawString(0.85*inch, y, "Sydney NSW 2000")

    y -= 0.5*inch

    # Line items table
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75*inch, y, "DESCRIPTION OF SERVICES / MATERIALS")
    y -= 0.3*inch

    # Table header
    table_data = [
        ['Item', 'Description', 'Qty', 'Unit Price', 'GST', 'Amount'],
    ]

    # Add line items
    subtotal = 0
    for idx, item in enumerate(invoice_data['items'], 1):
        qty = item.get('qty', 1)
        unit_price = item['unit_price']
        amount = qty * unit_price
        subtotal += amount

        table_data.append([
            str(idx),
            item['description'],
            str(qty),
            f"${unit_price:,.2f}",
            f"${amount * 0.1:,.2f}",
            f"${amount:,.2f}"
        ])

    # Create table
    t = Table(table_data, colWidths=[0.5*inch, 3.5*inch, 0.6*inch, 1*inch, 0.8*inch, 1*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), invoice_data['company_color']),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Draw table
    table_height = len(table_data) * 0.25*inch + 0.4*inch
    t.wrapOn(c, width, height)
    t.drawOn(c, 0.75*inch, y - table_height)

    y -= (table_height + 0.3*inch)

    # Totals section
    gst = subtotal * 0.1
    total = subtotal + gst

    c.setFillColor(colors.lightgrey)
    c.rect(width - 3*inch, y - 1.1*inch, 2.25*inch, 1.1*inch, fill=True, stroke=False)

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    c.drawString(width - 2.9*inch, y - 0.2*inch, "Subtotal:")
    c.drawRightString(width - 0.85*inch, y - 0.2*inch, f"${subtotal:,.2f}")

    y -= 0.3*inch
    c.drawString(width - 2.9*inch, y - 0.2*inch, "GST (10%):")
    c.drawRightString(width - 0.85*inch, y - 0.2*inch, f"${gst:,.2f}")

    y -= 0.35*inch
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(invoice_data['company_color'])
    c.drawString(width - 2.9*inch, y - 0.2*inch, "TOTAL DUE:")
    c.drawRightString(width - 0.85*inch, y - 0.2*inch, f"${total:,.2f}")

    y -= 0.7*inch

    # Payment terms
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.75*inch, y, "PAYMENT TERMS:")
    y -= 0.2*inch
    c.setFont("Helvetica", 9)
    c.drawString(0.75*inch, y, f"Payment due within {invoice_data.get('payment_terms', '30 days')}")
    y -= 0.15*inch
    c.drawString(0.75*inch, y, f"Bank: {invoice_data.get('bank', 'Commonwealth Bank')}")
    y -= 0.15*inch
    c.drawString(0.75*inch, y, f"BSB: {invoice_data.get('bsb', '062-000')}  Account: {invoice_data.get('account', '12345678')}")
    y -= 0.15*inch
    c.drawString(0.75*inch, y, f"Reference: {invoice_data['invoice_no']}")

    # Notes section
    if 'notes' in invoice_data:
        y -= 0.3*inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75*inch, y, "NOTES:")
        y -= 0.15*inch
        c.setFont("Helvetica", 8)
        for note in invoice_data['notes']:
            c.drawString(0.75*inch, y, note)
            y -= 0.12*inch

    draw_footer(c, 1)
    c.save()
    print(f"  ✅ {filepath.name}")

print("="*80)
print("GENERATING ENHANCED PDF FILES WITH PROFESSIONAL FORMATTING")
print("="*80)

# ========== 01_LAND_PURCHASE ==========
print("\n[01_LAND_PURCHASE]")
folder = BASE_DIR / "01_LAND_PURCHASE"
folder.mkdir(parents=True, exist_ok=True)

# Legal Fees Invoice
create_detailed_invoice(folder / "Legal_Fees_Invoice_JohnsonSolicitors.pdf", {
    'company_name': 'JOHNSON & PARTNERS SOLICITORS',
    'company_color': colors.HexColor('#1a237e'),
    'abn': '42 123 456 789',
    'address': 'Level 15, 100 George Street, Sydney NSW 2000',
    'phone': '(02) 9555-1200',
    'email': 'admin@johnsonpartners.com.au',
    'invoice_no': 'JS-2024-0847',
    'date': '20 June 2024',
    'due_date': '27 June 2024',
    'payment_terms': '7 days',
    'bank': 'Commonwealth Bank',
    'bsb': '062-001',
    'account': '10245678',
    'items': [
        {'description': 'Contract Review and Legal Advice - Land Purchase', 'qty': 4.5, 'unit_price': 350.00},
        {'description': 'Conveyancing Services - Full Service', 'qty': 1, 'unit_price': 1200.00},
        {'description': 'Title Search and Verification (Lot 15 DP 123456)', 'qty': 1, 'unit_price': 350.00},
        {'description': 'Section 10.7 Planning Certificate', 'qty': 1, 'unit_price': 180.00},
        {'description': 'Company/Trust Searches', 'qty': 2, 'unit_price': 85.00},
        {'description': 'Document Preparation and Lodgement', 'qty': 1, 'unit_price': 450.00},
        {'description': 'Correspondence and Client Consultations', 'qty': 2.5, 'unit_price': 300.00},
    ],
    'notes': [
        'All disbursements included in itemized charges above',
        'Professional indemnity insurance: $20M',
        'Thank you for choosing Johnson & Partners'
    ]
})

# Soil Test Report
soil_test = folder / "Soil_Test_Report_GeoTech.pdf"
c = canvas.Canvas(str(soil_test), pagesize=letter)
y = draw_professional_header(c, "GEOTECH AUSTRALIA PTY LTD", colors.HexColor('#d84315'),
                             "78 456 123 789", "Unit 12, 45 Engineering Drive, Macquarie Park NSW 2113",
                             "(02) 9888-5500", "reports@geotechaustralia.com.au")

c.setFillColor(colors.HexColor('#d84315'))
c.setFont("Helvetica-Bold", 18)
c.drawString(0.75*inch, y, "GEOTECHNICAL INVESTIGATION REPORT")

y -= 0.4*inch
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 11)
c.drawString(0.75*inch, y, "Project:")
c.setFont("Helvetica", 11)
c.drawString(2*inch, y, "123 Sunset Boulevard, Sydney NSW 2000")

y -= 0.2*inch
c.setFont("Helvetica-Bold", 11)
c.drawString(0.75*inch, y, "Client:")
c.setFont("Helvetica", 11)
c.drawString(2*inch, y, "Sunset Construction Pty Ltd")

y -= 0.2*inch
c.setFont("Helvetica-Bold", 11)
c.drawString(0.75*inch, y, "Report No:")
c.setFont("Helvetica", 11)
c.drawString(2*inch, y, "GT-2024-1847")

y -= 0.2*inch
c.setFont("Helvetica-Bold", 11)
c.drawString(0.75*inch, y, "Date:")
c.setFont("Helvetica", 11)
c.drawString(2*inch, y, "25 June 2024")

y -= 0.4*inch
c.setFillColor(colors.HexColor('#d84315'))
c.setFont("Helvetica-Bold", 14)
c.drawString(0.75*inch, y, "EXECUTIVE SUMMARY")

y -= 0.3*inch
c.setFillColor(colors.black)
c.setFont("Helvetica", 10)
lines = [
    "A comprehensive geotechnical investigation was conducted comprising three (3) boreholes to",
    "depths ranging from 2.5m to 4.0m below existing ground level. Laboratory testing was performed",
    "on selected samples to determine soil classification and engineering properties.",
    "",
    "SITE CONDITIONS:",
    "• The site is relatively flat with a gentle slope from front to rear (approx. 0.5m over 30m)",
    "• No surface water ponding observed during site visit",
    "• Existing vegetation consists of grass and small shrubs",
    "• One large eucalyptus tree located at rear boundary (12m from proposed dwelling)",
    "",
    "SUBSURFACE CONDITIONS:",
    "• 0.0m - 0.3m: Topsoil (dark brown, loose, organic)",
    "• 0.3m - 1.5m: Silty CLAY (light brown, stiff, low plasticity)",
    "• 1.5m - 4.0m: Sandy CLAY (brown-grey, very stiff, moderately plastic)",
    "• No groundwater encountered to maximum depth of investigation",
    "",
    "SOIL CLASSIFICATION: Class S (Slightly Reactive Clay) per AS 2870-2011",
    "BEARING CAPACITY: 150 kPa for strip footings at 600mm depth",
    "FOOTING DESIGN: Stiffened raft or strip footings on Class S sites",
]

for line in lines:
    if line.startswith("•"):
        c.drawString(1*inch, y, line)
    elif line.isupper() and ":" in line:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.75*inch, y, line)
        c.setFont("Helvetica", 10)
    else:
        c.drawString(0.75*inch, y, line)
    y -= 0.15*inch
    if y < 1.5*inch:
        draw_footer(c, 1)
        c.showPage()
        y = draw_professional_header(c, "GEOTECH AUSTRALIA PTY LTD", colors.HexColor('#d84315'),
                                     "78 456 123 789", "Unit 12, 45 Engineering Drive, Macquarie Park NSW 2113",
                                     "(02) 9888-5500", "reports@geotechaustralia.com.au")

y -= 0.2*inch
c.setFillColor(colors.HexColor('#d84315'))
c.setFont("Helvetica-Bold", 14)
c.drawString(0.75*inch, y, "RECOMMENDATIONS")

y -= 0.3*inch
c.setFillColor(colors.black)
c.setFont("Helvetica", 10)
recommendations = [
    "1. Strip footings with minimum width of 450mm and depth of 600mm below natural ground level",
    "2. Concrete strength minimum 25MPa for footings and slabs",
    "3. Reinforced concrete slab-on-ground with F82 mesh minimum",
    "4. Provide edge beams around entire perimeter",
    "5. Install subsurface drainage around footing perimeter",
    "6. Remove tree at rear boundary prior to construction (potential foundation impact)",
    "7. Ensure adequate surface drainage away from building",
    "8. Compact fill beneath slab to 98% Standard Maximum Dry Density",
]

for rec in recommendations:
    c.drawString(0.75*inch, y, rec)
    y -= 0.18*inch

y -= 0.3*inch
c.setFont("Helvetica-Bold", 10)
c.drawString(0.75*inch, y, "Report prepared by:")
y -= 0.2*inch
c.setFont("Helvetica", 10)
c.drawString(0.75*inch, y, "Dr. Sarah Chen, PhD, MIEAust, CPEng")
y -= 0.15*inch
c.drawString(0.75*inch, y, "Principal Geotechnical Engineer")
y -= 0.15*inch
c.drawString(0.75*inch, y, "GeoTech Australia Pty Ltd")

draw_footer(c, 2)
c.save()
print(f"  ✅ {soil_test.name}")

# ========== 03_SITE_ESTABLISHMENT ==========
print("\n[03_SITE_ESTABLISHMENT]")
folder = BASE_DIR / "03_SITE_ESTABLISHMENT"
folder.mkdir(parents=True, exist_ok=True)

# Scaffolding Hire Invoice
create_detailed_invoice(folder / "Scaffolding_Hire_Invoice.pdf", {
    'company_name': 'METRO SCAFFOLDING SERVICES',
    'company_color': colors.HexColor('#f57c00'),
    'abn': '91 234 567 890',
    'address': '88 Industrial Avenue, Silverwater NSW 2128',
    'phone': '1300-SCAF-NOW',
    'email': 'hire@metroscaffolding.com.au',
    'invoice_no': 'MSS-2024-3321',
    'date': '15 July 2024',
    'due_date': '30 July 2024',
    'payment_terms': '15 days',
    'bank': 'Westpac',
    'bsb': '032-156',
    'account': '445566',
    'items': [
        {'description': 'Scaffolding Erection - Two Storey Building (Front & Sides)', 'qty': 1, 'unit_price': 3200.00},
        {'description': 'Weekly Hire - Scaffolding System (Week 1-4)', 'qty': 4, 'unit_price': 450.00},
        {'description': 'Safety Mesh and Edge Protection', 'qty': 85, 'unit_price': 12.50},
        {'description': 'Stair Access Tower', 'qty': 1, 'unit_price': 850.00},
        {'description': 'Weekly Inspection and Compliance Certification', 'qty': 4, 'unit_price': 180.00},
        {'description': 'Delivery and Collection Fee', 'qty': 1, 'unit_price': 450.00},
    ],
    'notes': [
        'All scaffolding compliant with AS/NZS 1576 and 4576',
        'Weekly inspections by licensed scaffolder included',
        'Additional hire weeks charged at $450/week + GST',
        'Dismantling to be quoted separately upon completion'
    ]
})

# Site Security Fence Invoice
create_detailed_invoice(folder / "Security_Fence_Temp.pdf", {
    'company_name': 'SECURE SITE SOLUTIONS',
    'company_color': colors.HexColor('#2e7d32'),
    'abn': '55 678 901 234',
    'address': '22 Safety Circuit, Wetherill Park NSW 2164',
    'phone': '(02) 9725-8888',
    'email': 'quotes@securesitesolutions.com.au',
    'invoice_no': 'SSS-2024-1245',
    'date': '10 July 2024',
    'due_date': '24 July 2024',
    'payment_terms': '14 days',
    'bank': 'NAB',
    'bsb': '082-401',
    'account': '334455667',
    'items': [
        {'description': 'Temporary Chain Wire Fencing - 2.4m high (45 linear meters)', 'qty': 45, 'unit_price': 35.00},
        {'description': 'Fencing Installation and Stabilization', 'qty': 1, 'unit_price': 680.00},
        {'description': 'Site Access Gate - 4m wide with lock', 'qty': 1, 'unit_price': 420.00},
        {'description': 'Pedestrian Gate - lockable', 'qty': 1, 'unit_price': 280.00},
        {'description': 'Safety Signage Kit (Construction Site Warnings)', 'qty': 1, 'unit_price': 340.00},
        {'description': 'Monthly Hire Fee (3 months prepaid)', 'qty': 3, 'unit_price': 185.00},
    ],
    'notes': [
        'Fencing hire period: July 2024 - October 2024 (renewable)',
        'Removal and final cleanup included in quoted price',
        'All materials comply with WorkCover requirements',
    ]
})

# ========== 05_FOUNDATION ==========
print("\n[05_FOUNDATION]")
folder = BASE_DIR / "05_FOUNDATION"
folder.mkdir(parents=True, exist_ok=True)

# Concrete Supply Invoice
create_detailed_invoice(folder / "Concrete_Supply_Invoice_BetaMix.pdf", {
    'company_name': 'BETAMIX CONCRETE SUPPLIES',
    'company_color': colors.HexColor('#424242'),
    'abn': '33 111 222 333',
    'address': '150 Quarry Road, Erskine Park NSW 2759',
    'phone': '1300-CONCRETE',
    'email': 'orders@betamix.com.au',
    'invoice_no': 'BMX-2024-8821',
    'date': '22 July 2024',
    'due_date': '5 August 2024',
    'payment_terms': '14 days',
    'bank': 'ANZ',
    'bsb': '012-366',
    'account': '998877665',
    'items': [
        {'description': 'Ready-Mix Concrete 25MPa - Footings (12 cubic meters)', 'qty': 12, 'unit_price': 285.00},
        {'description': 'Ready-Mix Concrete 32MPa - Slab (18 cubic meters)', 'qty': 18, 'unit_price': 315.00},
        {'description': 'Concrete Pump Hire - 4 hours', 'qty': 4, 'unit_price': 220.00},
        {'description': 'Fiber Mesh Additive (crack control)', 'qty': 30, 'unit_price': 8.50},
        {'description': 'Concrete Delivery Fee - Multiple pours', 'qty': 3, 'unit_price': 145.00},
        {'description': 'After-hours Pour Surcharge (Saturday)', 'qty': 1, 'unit_price': 550.00},
        {'description': 'Standby Time - 45 minutes @ $150/hr', 'qty': 0.75, 'unit_price': 150.00},
    ],
    'notes': [
        'Pour dates: 22 July 2024 (footings), 24 July 2024 (slab)',
        'All concrete certified to AS 1379 standards',
        'Slump test certificates provided on delivery',
        'Compression test samples taken for lab testing'
    ]
})

# Steel Reinforcement Invoice
create_detailed_invoice(folder / "Steel_Reinforcement_AceSteel.pdf", {
    'company_name': 'ACE STEEL REINFORCING',
    'company_color': colors.HexColor('#b71c1c'),
    'abn': '44 555 666 777',
    'address': '12 Steel Way, Smithfield NSW 2164',
    'phone': '(02) 9725-4400',
    'email': 'sales@acesteel.com.au',
    'invoice_no': 'ACE-2024-5589',
    'date': '18 July 2024',
    'due_date': '1 August 2024',
    'payment_terms': '14 days',
    'bank': 'Westpac',
    'bsb': '032-089',
    'account': '112233445',
    'items': [
        {'description': 'N12 Deformed Bar - Footing Reinforcement (650kg)', 'qty': 650, 'unit_price': 1.85},
        {'description': 'N16 Deformed Bar - Edge Beams (420kg)', 'qty': 420, 'unit_price': 1.95},
        {'description': 'F82 Reinforcing Mesh - Slab (180 sqm)', 'qty': 180, 'unit_price': 8.50},
        {'description': 'L12 Ligatures and Ties (Bundle)', 'qty': 8, 'unit_price': 45.00},
        {'description': 'Bar Chairs and Spacers - Mixed Sizes', 'qty': 320, 'unit_price': 0.95},
        {'description': 'Cutting and Bending Service', 'qty': 1, 'unit_price': 385.00},
        {'description': 'Delivery - Hiab Truck', 'qty': 1, 'unit_price': 295.00},
    ],
    'notes': [
        'All steel certified to AS/NZS 4671:2001',
        'Mill test certificates available upon request',
        'Installation guide and fixing details provided',
    ]
})

# ========== 06_FRAME ==========
print("\n[06_FRAME]")
folder = BASE_DIR / "06_FRAME"
folder.mkdir(parents=True, exist_ok=True)

# Timber Frame Supply
create_detailed_invoice(folder / "Timber_Frame_Supply_Invoice.pdf", {
    'company_name': 'TIMBERLAND FRAMES & TRUSSES',
    'company_color': colors.HexColor('#5d4037'),
    'abn': '22 333 444 555',
    'address': '88 Sawmill Drive, Riverstone NSW 2765',
    'phone': '(02) 9627-3300',
    'email': 'frames@timberlandframes.com.au',
    'invoice_no': 'TFT-2024-2914',
    'date': '1 August 2024',
    'due_date': '15 August 2024',
    'payment_terms': '14 days',
    'bank': 'Commonwealth Bank',
    'bsb': '062-000',
    'account': '55667788',
    'items': [
        {'description': 'Roof Truss Package - Engineered (Custom Design)', 'qty': 1, 'unit_price': 8850.00},
        {'description': '90x45 F7 Pine Framing - Wall Studs (4.8m linear meters)', 'qty': 285, 'unit_price': 12.80},
        {'description': '90x45 F7 Pine - Top/Bottom Plates', 'qty': 180, 'unit_price': 12.80},
        {'description': '140x45 F17 Hardwood - Bearers and Joists', 'qty': 95, 'unit_price': 28.50},
        {'description': 'LVL Beams 300x45mm (structural)', 'qty': 24, 'unit_price': 85.00},
        {'description': 'Glulam Posts 150x150mm', 'qty': 8, 'unit_price': 125.00},
        {'description': 'Truss Engineering Certification', 'qty': 1, 'unit_price': 680.00},
        {'description': 'Delivery - Crane Truck (Two loads)', 'qty': 2, 'unit_price': 420.00},
    ],
    'notes': [
        'All timber F7/F17 graded per AS 1720',
        'Structural engineer certification included for trusses',
        'Installation manual and bracing guide provided',
        'Treated pine for bottom plates (H3 rated)',
    ]
})

# Frame Carpentry Labour
create_detailed_invoice(folder / "Carpentry_Labour_Invoice.pdf", {
    'company_name': 'PRECISION CARPENTRY CONTRACTORS',
    'company_color': colors.HexColor('#ff6f00'),
    'abn': '66 777 888 999',
    'address': '45 Tradesman Lane, Blacktown NSW 2148',
    'phone': '0412-345-678',
    'email': 'admin@precisioncarpentry.com.au',
    'invoice_no': 'PCC-2024-1156',
    'date': '15 August 2024',
    'due_date': '29 August 2024',
    'payment_terms': '14 days',
    'bank': 'NAB',
    'bsb': '082-192',
    'account': '223344556',
    'items': [
        {'description': 'Frame Construction - Ground Floor (6 days @ $850/day)', 'qty': 6, 'unit_price': 850.00},
        {'description': 'Frame Construction - First Floor (5 days @ $850/day)', 'qty': 5, 'unit_price': 850.00},
        {'description': 'Roof Truss Installation & Bracing (3 days @ $950/day)', 'qty': 3, 'unit_price': 950.00},
        {'description': 'Window & Door Frame Installation (2 days)', 'qty': 2, 'unit_price': 750.00},
        {'description': 'Temporary Bracing and Support', 'qty': 1, 'unit_price': 480.00},
        {'description': 'Waste Removal and Site Cleanup', 'qty': 1, 'unit_price': 380.00},
    ],
    'notes': [
        'Licensed builder: NSW 123456C',
        'All work complies with Building Code of Australia',
        'Public liability insurance: $20M',
        'Frame inspection certificate provided upon completion',
    ]
})

# ========== 07_WINDOWS_DOORS ==========
print("\n[07_WINDOWS_DOORS]")
folder = BASE_DIR / "07_WINDOWS_DOORS"
folder.mkdir(parents=True, exist_ok=True)

# Windows & Doors Supply
create_detailed_invoice(folder / "Windows_Doors_Supply_Invoice.pdf", {
    'company_name': 'PREMIUM WINDOWS & DOORS',
    'company_color': colors.HexColor('#0277bd'),
    'abn': '88 999 000 111',
    'address': '200 Glazier Street, Homebush NSW 2140',
    'phone': '(02) 9764-5000',
    'email': 'sales@premiumwindowsdoors.com.au',
    'invoice_no': 'PWD-2024-7733',
    'date': '20 August 2024',
    'due_date': '3 September 2024',
    'payment_terms': '14 days',
    'bank': 'ANZ',
    'bsb': '012-003',
    'account': '667788990',
    'items': [
        {'description': 'Aluminum Sliding Windows 1800x1200mm (Low-E glass)', 'qty': 8, 'unit_price': 685.00},
        {'description': 'Aluminum Awning Windows 900x600mm', 'qty': 4, 'unit_price': 425.00},
        {'description': 'Double Glazed Fixed Window 3000x2100mm (Feature)', 'qty': 1, 'unit_price': 3200.00},
        {'description': 'Hinged Entry Door - Pivot 2400x1200mm (Timber)', 'qty': 1, 'unit_price': 2850.00},
        {'description': 'Sliding Patio Doors 3600x2100mm (Double glazed)', 'qty': 1, 'unit_price': 4200.00},
        {'description': 'Internal Hollow Core Doors 2040x820mm', 'qty': 8, 'unit_price': 180.00},
        {'description': 'Door Furniture - Handles, Locks, Hinges (Complete set)', 'qty': 1, 'unit_price': 1250.00},
        {'description': 'Flyscreens - Sliding doors and windows', 'qty': 9, 'unit_price': 145.00},
        {'description': 'Installation Service - Complete Package', 'qty': 1, 'unit_price': 3800.00},
        {'description': 'WERS Certification (Window Energy Rating)', 'qty': 1, 'unit_price': 285.00},
    ],
    'notes': [
        'All windows comply with AS 2047 and WERS 5-star rated',
        'Double glazed units: 6mm/12mm air gap/6mm Low-E',
        'Powder coated aluminum - Surfmist color',
        '10-year warranty on glass seals and hardware',
        'Installation includes flashing and waterproofing',
    ]
})

print("\n" + "="*80)
print("✅ ENHANCED PDF GENERATION COMPLETE!")
print("="*80)
print("\nSample PDFs created with professional features:")
print("  ✓ Company banners and branding")
print("  ✓ Comprehensive itemized tables")
print("  ✓ Multi-page documents with headers/footers")
print("  ✓ Professional color schemes")
print("  ✓ Detailed line items and subtotals")
print("  ✓ Realistic company names and details")
print("  ✓ Terms & conditions sections")
print("\nRun this script to generate enhanced PDFs for remaining categories")
print("="*80 + "\n")
