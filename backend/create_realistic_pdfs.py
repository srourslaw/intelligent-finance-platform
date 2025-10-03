#!/usr/bin/env python3
"""
Phase 3: Create Realistic PDF Documents
Generates professional-looking construction finance PDFs matching Excel data
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
from pathlib import Path
import random

def create_letterhead(c, doc_title):
    """Add company letterhead to PDF"""
    # Company logo placeholder (you can add actual logo later)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.drawString(1*inch, 10.5*inch, "SUNSET CONSTRUCTION PTY LTD")

    # Company details
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    c.drawString(1*inch, 10.25*inch, "ABN: 12 345 678 901")
    c.drawString(1*inch, 10.1*inch, "123 Builder Street, Sydney NSW 2000")
    c.drawString(1*inch, 9.95*inch, "Phone: (02) 9555 1234 | Email: info@sunsetconstruction.com.au")

    # Draw line
    c.setStrokeColor(colors.HexColor('#1E3A8A'))
    c.setLineWidth(2)
    c.line(1*inch, 9.8*inch, 7.5*inch, 9.8*inch)

    # Document title
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.drawString(1*inch, 9.4*inch, doc_title)

def create_land_purchase_contract():
    """Create realistic land purchase contract"""
    print("\n📄 Creating Land Purchase Contract...")

    output_dir = Path("/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-a-123-sunset-blvd/data/01_LAND_PURCHASE")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = output_dir / "Land_Purchase_Contract_Signed.pdf"
    c = canvas.Canvas(str(filename), pagesize=letter)

    create_letterhead(c, "CONTRACT FOR SALE OF LAND")

    # Contract details
    y = 9*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "PARTIES")

    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "VENDOR:")
    c.drawString(2*inch, y, "Smith Family Trust")

    y -= 0.2*inch
    c.drawString(2*inch, y, "C/- Sarah Smith (Trustee)")

    y -= 0.2*inch
    c.drawString(2*inch, y, "456 Vendor Avenue, Sydney NSW 2000")

    y -= 0.4*inch
    c.drawString(1*inch, y, "PURCHASER:")
    c.drawString(2*inch, y, "Sunset Construction Pty Ltd")

    y -= 0.2*inch
    c.drawString(2*inch, y, "ABN: 12 345 678 901")

    y -= 0.2*inch
    c.drawString(2*inch, y, "123 Builder Street, Sydney NSW 2000")

    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "PROPERTY DETAILS")

    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Address:")
    c.drawString(2*inch, y, "123 Sunset Boulevard, Sydney NSW 2000")

    y -= 0.2*inch
    c.drawString(1*inch, y, "Lot/Plan:")
    c.drawString(2*inch, y, "Lot 42 in DP 1234567")

    y -= 0.2*inch
    c.drawString(1*inch, y, "Land Area:")
    c.drawString(2*inch, y, "850 square metres")

    y -= 0.2*inch
    c.drawString(1*inch, y, "Zoning:")
    c.drawString(2*inch, y, "R2 Low Density Residential")

    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "PURCHASE PRICE & PAYMENT TERMS")

    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Purchase Price:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*inch, y, "$250,000.00 (GST-Free)")

    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Deposit (10%):")
    c.drawString(2.5*inch, y, "$25,000.00 (Paid on signing)")

    y -= 0.2*inch
    c.drawString(1*inch, y, "Balance:")
    c.drawString(2.5*inch, y, "$225,000.00 (Payable on settlement)")

    y -= 0.2*inch
    c.drawString(1*inch, y, "Settlement Date:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*inch, y, "15 January 2024")

    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "SPECIAL CONDITIONS")

    y -= 0.3*inch
    c.setFont("Helvetica", 9)
    conditions = [
        "1. This contract is subject to purchaser obtaining Development Approval within 90 days.",
        "2. Purchaser to conduct soil testing and environmental assessment at their cost.",
        "3. Property sold with existing easements and encumbrances as per title search.",
        "4. Settlement to occur at purchaser's solicitor's office in Sydney CBD.",
        "5. Vendor warrants clear title and absence of hazardous materials."
    ]

    for condition in conditions:
        c.drawString(1*inch, y, condition)
        y -= 0.2*inch

    # Signatures
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "EXECUTED:")

    y -= 0.4*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y, "VENDOR:")
    c.drawString(1*inch, y-0.3*inch, "_" * 30)
    c.drawString(1*inch, y-0.5*inch, "Sarah Smith (Trustee)")
    c.drawString(1*inch, y-0.7*inch, "Date: 10/01/2024")

    c.drawString(4.5*inch, y, "PURCHASER:")
    c.drawString(4.5*inch, y-0.3*inch, "_" * 30)
    c.drawString(4.5*inch, y-0.5*inch, "Michael Chen (Director)")
    c.drawString(4.5*inch, y-0.7*inch, "Sunset Construction Pty Ltd")
    c.drawString(4.5*inch, y-0.9*inch, "Date: 10/01/2024")

    c.save()
    print(f"  ✅ Created {filename.name}")

def create_bank_statements():
    """Create realistic bank statements for 4 months"""
    print("\n📄 Creating Bank Statements...")

    output_dir = Path("/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-a-123-sunset-blvd/data/20_BANK_RECONCILIATION/Bank_Statements")
    output_dir.mkdir(parents=True, exist_ok=True)

    months = [
        ('June', 2024, 6),
        ('July', 2024, 7),
        ('August', 2024, 8),
        ('September', 2024, 9)
    ]

    opening_balance = 100000

    for month_name, year, month_num in months:
        filename = output_dir / f"Bank_Statement_{month_name}_{year}.pdf"
        c = canvas.Canvas(str(filename), pagesize=letter)

        # Bank logo and header
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor('#C41E3A'))
        c.drawString(1*inch, 10.5*inch, "COMMONWEALTH BANK")

        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawString(1*inch, 10.25*inch, "Business Banking Statement")

        # Account details
        y = 9.8*inch
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y, "SUNSET CONSTRUCTION PTY LTD")

        y -= 0.2*inch
        c.setFont("Helvetica", 9)
        c.drawString(1*inch, y, "123 Builder Street, Sydney NSW 2000")

        y -= 0.3*inch
        c.drawString(1*inch, y, "Account Name: Business Operating Account")

        y -= 0.2*inch
        c.drawString(1*inch, y, "BSB: 062-001")

        y -= 0.2*inch
        c.drawString(1*inch, y, "Account Number: 1234 5678")

        y -= 0.3*inch
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y, f"Statement Period: 1 {month_name} {year} to 30 {month_name} {year}")

        # Statement table
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1*inch, y, "Date")
        c.drawString(1.8*inch, y, "Description")
        c.drawString(4.5*inch, y, "Debit")
        c.drawString(5.5*inch, y, "Credit")
        c.drawString(6.5*inch, y, "Balance")

        y -= 0.05*inch
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.line(1*inch, y, 7.5*inch, y)

        y -= 0.2*inch
        c.setFont("Helvetica", 8)

        # Opening balance
        c.drawString(1*inch, y, "01/" + f"{month_num:02d}/{year}")
        c.drawString(1.8*inch, y, "Opening Balance")
        c.drawString(6.5*inch, y, f"${opening_balance:,.2f}")

        balance = opening_balance

        # Transactions
        transactions = [
            (5, "Deposit - Client Progress Payment", 65000, 'credit'),
            (8, "Transfer - Loan Drawdown", 150000, 'credit'),
            (10, "Payment - BuildMart Supplies", -15400, 'debit'),
            (12, "Payment - Spark Electrical", -22080, 'debit'),
            (15, "Payment - Site Supervisor Wages", -7200, 'debit'),
            (18, "Payment - Premium Plumbing", -18900, 'debit'),
            (20, "Deposit - Client Payment", 32500, 'credit'),
            (22, "Payment - Council Permits", -2850, 'debit'),
            (25, "Payment - Insurance Premium", -1200, 'debit'),
            (28, "Payment - Subcontractor - Excavation", -12120, 'debit'),
            (30, "Bank Fees", -45, 'debit'),
        ]

        for day, desc, amount, type in transactions:
            y -= 0.2*inch
            c.drawString(1*inch, y, f"{day:02d}/{month_num:02d}/{year}")
            c.drawString(1.8*inch, y, desc)

            balance += amount

            if type == 'debit':
                c.drawString(4.5*inch, y, f"${abs(amount):,.2f}")
            else:
                c.drawString(5.5*inch, y, f"${amount:,.2f}")

            c.drawString(6.5*inch, y, f"${balance:,.2f}")

        # Closing balance
        y -= 0.3*inch
        c.setLineWidth(2)
        c.line(1*inch, y, 7.5*inch, y)

        y -= 0.2*inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1*inch, y, "CLOSING BALANCE")
        c.drawString(6.5*inch, y, f"${balance:,.2f}")

        # Summary
        y -= 0.4*inch
        c.setFont("Helvetica", 8)
        c.drawString(1*inch, y, "Total Deposits: $247,500.00")
        c.drawString(3*inch, y, "Total Withdrawals: $79,795.00")

        y -= 0.3*inch
        c.drawString(1*inch, y, "For enquiries: 13 2221 | commbank.com.au")

        opening_balance = balance  # Carry forward to next month

        c.save()
        print(f"  ✅ Created {filename.name}")

def create_tax_invoices():
    """Create realistic tax invoices matching Excel data"""
    print("\n📄 Creating Tax Invoices...")

    output_dir = Path("/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-a-123-sunset-blvd/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid")

    suppliers = [
        {
            'name': 'BuildMart Supplies Pty Ltd',
            'abn': '98 765 432 109',
            'address': '45 Supply Road, Sydney NSW 2000',
            'phone': '(02) 9555 7890',
            'invoice': 'BM-1234',
            'date': '20/09/2024',
            'po': 'PO-2024-1015',
            'items': [
                ('Concrete Mix - 40MPa (20 cubic metres)', 14, 12000, 168000),
                ('Steel Reinforcement Bar (2 tonnes)', 2, 3500, 7000),
                ('Timber Framing (Premium Pine)', 1, 8500, 8500),
            ],
            'subtotal': 14000,
            'gst': 1400,
            'total': 15400
        },
        {
            'name': 'Spark Electrical Services Pty Ltd',
            'abn': '45 678 901 234',
            'address': '78 Voltage Street, Sydney NSW 2000',
            'phone': '(02) 9555 3456',
            'invoice': 'SE-5678',
            'date': '15/09/2024',
            'po': 'PO-2024-1000',
            'items': [
                ('Electrical Rough-In - First Fix', 1, 8500, 8500),
                ('Power Points & Switches (50 units)', 50, 85, 4250),
                ('LED Downlights (30 units)', 30, 65, 1950),
                ('Switchboard & Circuit Breakers', 1, 3200, 3200),
                ('Cable & Conduit Materials', 1, 2180, 2180),
            ],
            'subtotal': 20080,
            'gst': 2008,
            'total': 22088
        },
        {
            'name': 'Premium Plumbing Solutions Pty Ltd',
            'abn': '23 456 789 012',
            'address': '12 Pipe Lane, Sydney NSW 2000',
            'phone': '(02) 9555 6789',
            'invoice': 'PP-9012',
            'date': '25/08/2024',
            'po': 'PO-2024-1008',
            'items': [
                ('Plumbing Rough-In Complete', 1, 12000, 12000),
                ('Hot Water System (315L)', 1, 2800, 2800),
                ('Bathroom Fixtures Set (2 bathrooms)', 2, 1500, 3000),
                ('Kitchen Sink & Tapware', 1, 850, 850),
            ],
            'subtotal': 18650,
            'gst': 1865,
            'total': 20515
        }
    ]

    for supplier in suppliers:
        filename = output_dir / f"Tax_Invoice_{supplier['invoice']}.pdf"
        c = canvas.Canvas(str(filename), pagesize=letter)

        # Supplier letterhead
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor('#1E3A8A'))
        c.drawString(1*inch, 10.5*inch, supplier['name'].upper())

        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawString(1*inch, 10.25*inch, f"ABN: {supplier['abn']}")
        c.drawString(1*inch, 10.1*inch, supplier['address'])
        c.drawString(1*inch, 9.95*inch, f"Phone: {supplier['phone']}")

        # TAX INVOICE watermark
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor('#FF0000'))
        c.drawString(5*inch, 10.3*inch, "TAX INVOICE")

        # Line
        c.setStrokeColor(colors.HexColor('#1E3A8A'))
        c.setLineWidth(2)
        c.line(1*inch, 9.8*inch, 7.5*inch, 9.8*inch)

        # Bill To
        y = 9.4*inch
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)
        c.drawString(1*inch, y, "BILL TO:")

        y -= 0.2*inch
        c.setFont("Helvetica", 9)
        c.drawString(1*inch, y, "Sunset Construction Pty Ltd")
        y -= 0.15*inch
        c.drawString(1*inch, y, "ABN: 12 345 678 901")
        y -= 0.15*inch
        c.drawString(1*inch, y, "123 Builder Street, Sydney NSW 2000")

        # Invoice details box
        y = 9.4*inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(5*inch, y, "Invoice Number:")
        c.drawString(6.3*inch, y, supplier['invoice'])

        y -= 0.2*inch
        c.drawString(5*inch, y, "Invoice Date:")
        c.drawString(6.3*inch, y, supplier['date'])

        y -= 0.2*inch
        c.drawString(5*inch, y, "Purchase Order:")
        c.drawString(6.3*inch, y, supplier['po'])

        y -= 0.2*inch
        c.drawString(5*inch, y, "Payment Terms:")
        c.drawString(6.3*inch, y, "Net 30 Days")

        # Items table
        y = 8.6*inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1*inch, y, "Description")
        c.drawString(4.2*inch, y, "Qty")
        c.drawString(4.8*inch, y, "Unit Price")
        c.drawString(5.8*inch, y, "Amount")

        y -= 0.05*inch
        c.setLineWidth(1)
        c.line(1*inch, y, 7.5*inch, y)

        y -= 0.25*inch
        c.setFont("Helvetica", 8)

        for item_desc, qty, unit_price, amount in supplier['items']:
            c.drawString(1*inch, y, item_desc)
            c.drawString(4.3*inch, y, str(qty))
            c.drawString(4.8*inch, y, f"${unit_price:,.2f}")
            c.drawString(5.8*inch, y, f"${amount:,.2f}")
            y -= 0.2*inch

        # Totals
        y -= 0.2*inch
        c.setLineWidth(1)
        c.line(4.5*inch, y, 7.5*inch, y)

        y -= 0.25*inch
        c.setFont("Helvetica", 9)
        c.drawString(5*inch, y, "Subtotal:")
        c.drawString(6.2*inch, y, f"${supplier['subtotal']:,.2f}")

        y -= 0.2*inch
        c.drawString(5*inch, y, "GST (10%):")
        c.drawString(6.2*inch, y, f"${supplier['gst']:,.2f}")

        y -= 0.25*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(5*inch, y, "TOTAL:")
        c.drawString(6.2*inch, y, f"${supplier['total']:,.2f}")

        # Payment details
        y -= 0.5*inch
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y, "PAYMENT DETAILS")

        y -= 0.2*inch
        c.setFont("Helvetica", 8)
        c.drawString(1*inch, y, "Bank: Commonwealth Bank")
        y -= 0.15*inch
        c.drawString(1*inch, y, "BSB: 062-001")
        y -= 0.15*inch
        c.drawString(1*inch, y, f"Account Number: {supplier['abn'][-9:]}")
        y -= 0.15*inch
        c.drawString(1*inch, y, f"Account Name: {supplier['name']}")
        y -= 0.15*inch
        c.drawString(1*inch, y, f"Reference: {supplier['invoice']}")

        # Footer
        y = 0.8*inch
        c.setFont("Helvetica", 7)
        c.drawString(1*inch, y, "This is a tax invoice for GST purposes. Please retain for your records.")
        y -= 0.12*inch
        c.drawString(1*inch, y, f"Payment due: {supplier['date']} + 30 days | All prices in AUD | E&OE")

        c.save()
        print(f"  ✅ Created {filename.name}")

def create_loan_agreement():
    """Create realistic construction loan agreement"""
    print("\n📄 Creating Loan Agreement...")

    output_dir = Path("/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-a-123-sunset-blvd/data/04_FINANCE_INSURANCE")
    filename = output_dir / "Loan_Agreement_Construction_Finance.pdf"

    c = canvas.Canvas(str(filename), pagesize=letter)

    # Bank header
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#C41E3A'))
    c.drawString(1*inch, 10.5*inch, "COMMONWEALTH BANK")

    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawString(1*inch, 10.2*inch, "Business & Commercial Banking")

    # Document title
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.drawString(1*inch, 9.7*inch, "CONSTRUCTION LOAN FACILITY AGREEMENT")

    y = 9.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "LOAN FACILITY DETAILS")

    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Borrower:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*inch, y, "Sunset Construction Pty Ltd (ABN: 12 345 678 901)")

    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Facility Type:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*inch, y, "Construction Loan - Commercial Development")

    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Facility Limit:")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#C41E3A'))
    c.drawString(2.5*inch, y, "$650,000.00 AUD")

    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(1*inch, y, "Interest Rate:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*inch, y, "6.50% p.a. (variable)")

    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Loan Term:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*inch, y, "12 months construction + 24 months interest-only")

    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Commencement:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5*inch, y, "1 June 2024")

    y -= 0.2*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Facility Fee:")
    c.drawString(2.5*inch, y, "1.5% of facility limit ($9,750)")

    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "DRAWDOWN SCHEDULE")

    y -= 0.25*inch
    c.setFont("Helvetica", 9)
    drawdowns = [
        ("Stage 1", "Land Acquisition", "$265,000", "Completed 15/01/2024"),
        ("Stage 2", "Site Works & Foundation", "$130,000", "Completed 15/03/2024"),
        ("Stage 3", "Framing & Roof", "$100,000", "Available upon completion"),
        ("Stage 4", "Services & Fit-out", "$100,000", "Available upon completion"),
        ("Stage 5", "Final Completion", "$55,000", "Available upon final inspection"),
    ]

    for stage, desc, amount, status in drawdowns:
        y -= 0.2*inch
        c.drawString(1.2*inch, y, f"{stage}: {desc}")
        c.drawString(4.5*inch, y, amount)
        c.drawString(5.5*inch, y, status)

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "SECURITY")

    y -= 0.25*inch
    c.setFont("Helvetica", 9)
    securities = [
        "• First registered mortgage over land at 123 Sunset Boulevard, Sydney NSW 2000",
        "• Fixed and floating charge over all assets of Sunset Construction Pty Ltd",
        "• Personal guarantee from Michael Chen (Director) - $650,000",
        "• Assignment of construction contract proceeds",
    ]

    for security in securities:
        c.drawString(1*inch, y, security)
        y -= 0.18*inch

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "KEY TERMS & CONDITIONS")

    y -= 0.25*inch
    c.setFont("Helvetica", 8)
    terms = [
        "• Interest calculated daily and charged monthly in arrears",
        "• Interest-only repayments during construction (12 months)",
        "• Principal + interest repayments after construction completion",
        "• Loan must be repaid in full by 1 June 2027 (36 months from commencement)",
        "• Borrower to maintain comprehensive insurance over property and works",
        "• Bank approval required for any material variations to construction scope",
        "• Quarterly progress reports and updated costings to be provided to Bank",
        "• Loan subject to satisfactory valuations at each drawdown stage",
        "• Early repayment permitted without penalty after month 6",
    ]

    for term in terms:
        c.drawString(1*inch, y, term)
        y -= 0.16*inch

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "EXECUTED AND AGREED:")

    y -= 0.4*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y, "COMMONWEALTH BANK")
    c.drawString(1*inch, y-0.3*inch, "_" * 30)
    c.drawString(1*inch, y-0.5*inch, "James Patterson")
    c.drawString(1*inch, y-0.65*inch, "Senior Credit Manager")
    c.drawString(1*inch, y-0.8*inch, "Date: 25/05/2024")

    c.drawString(4.5*inch, y, "BORROWER")
    c.drawString(4.5*inch, y-0.3*inch, "_" * 30)
    c.drawString(4.5*inch, y-0.5*inch, "Michael Chen")
    c.drawString(4.5*inch, y-0.65*inch, "Director, Sunset Construction Pty Ltd")
    c.drawString(4.5*inch, y-0.8*inch, "Date: 25/05/2024")

    c.save()
    print(f"  ✅ Created {filename.name}")

def create_insurance_certificates():
    """Create realistic insurance policy certificates"""
    print("\n📄 Creating Insurance Certificates...")

    output_dir = Path("/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-a-123-sunset-blvd/data/04_FINANCE_INSURANCE")

    # Public Liability Insurance
    filename1 = output_dir / "Public_Liability_Insurance_Certificate.pdf"
    c = canvas.Canvas(str(filename1), pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#0066CC'))
    c.drawString(1*inch, 10.5*inch, "QBE INSURANCE")

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(1*inch, 10*inch, "CERTIFICATE OF CURRENCY")
    c.drawString(1*inch, 9.7*inch, "PUBLIC LIABILITY INSURANCE")

    y = 9.2*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Policy Number:")
    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, y, "PL-2024-789456")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Insured:")
    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, y, "Sunset Construction Pty Ltd (ABN: 12 345 678 901)")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Period of Insurance:")
    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, y, "1 June 2024 to 31 May 2025 (both dates inclusive)")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Limit of Liability:")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#0066CC'))
    c.drawString(2.5*inch, y, "$20,000,000 any one occurrence")

    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.black)
    c.drawString(1*inch, y, "COVERAGE:")

    y -= 0.2*inch
    c.setFont("Helvetica", 9)
    coverages = [
        "• Public and Products Liability",
        "• Property damage and personal injury",
        "• Professional indemnity extension",
        "• Worldwide coverage (excluding USA/Canada)",
        "• Annual aggregate limit: $40,000,000",
    ]

    for coverage in coverages:
        c.drawString(1*inch, y, coverage)
        y -= 0.18*inch

    y -= 0.2*inch
    c.setFont("Helvetica", 7)
    c.drawString(1*inch, y, "This certificate is issued as a matter of information only and confers no rights upon the recipient.")

    c.save()
    print(f"  ✅ Created {filename1.name}")

    # Contract Works Insurance
    filename2 = output_dir / "Contract_Works_Insurance_Certificate.pdf"
    c = canvas.Canvas(str(filename2), pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#0066CC'))
    c.drawString(1*inch, 10.5*inch, "QBE INSURANCE")

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawString(1*inch, 10*inch, "CERTIFICATE OF CURRENCY")
    c.drawString(1*inch, 9.7*inch, "CONTRACT WORKS INSURANCE")

    y = 9.2*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Policy Number:")
    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, y, "CW-2024-654321")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Insured:")
    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, y, "Sunset Construction Pty Ltd")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Project:")
    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, y, "Construction of Dwelling at 123 Sunset Boulevard, Sydney NSW 2000")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Period of Insurance:")
    c.setFont("Helvetica", 10)
    c.drawString(2.5*inch, y, "1 June 2024 to 30 June 2025")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Sum Insured:")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#0066CC'))
    c.drawString(2.5*inch, y, "$650,000")

    c.save()
    print(f"  ✅ Created {filename2.name}")

def main():
    print("=" * 80)
    print("PHASE 3: CREATE REALISTIC PDF DOCUMENTS")
    print("=" * 80)

    create_land_purchase_contract()
    create_bank_statements()
    create_tax_invoices()
    create_loan_agreement()
    create_insurance_certificates()

    print("\n" + "=" * 80)
    print("✨ PHASE 3 COMPLETE!")
    print("=" * 80)
    print("\nPDFs Created:")
    print("  ✅ Land_Purchase_Contract_Signed.pdf")
    print("  ✅ Bank_Statement_June_2024.pdf")
    print("  ✅ Bank_Statement_July_2024.pdf")
    print("  ✅ Bank_Statement_August_2024.pdf")
    print("  ✅ Bank_Statement_September_2024.pdf")
    print("  ✅ Tax_Invoice_BM-1234.pdf (BuildMart)")
    print("  ✅ Tax_Invoice_SE-5678.pdf (Spark Electrical)")
    print("  ✅ Tax_Invoice_PP-9012.pdf (Premium Plumbing)")
    print("  ✅ Loan_Agreement_Construction_Finance.pdf")
    print("  ✅ Public_Liability_Insurance_Certificate.pdf")
    print("  ✅ Contract_Works_Insurance_Certificate.pdf")
    print("\nTotal: 11 professional PDF documents")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
