#!/usr/bin/env python3
"""
Part 3: Contracts and Site Reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRACTS_DIR = os.path.join(BASE_DIR, "dummy_data/07_SUBCONTRACTORS/Subcontractor_Contracts")
REPORTS_DIR = os.path.join(BASE_DIR, "dummy_data/09_SITE_REPORTS_PHOTOS")

# =============================================================================
# SUBCONTRACTOR CONTRACTS
# =============================================================================
def generate_electrician_contract():
    filename = os.path.join(CONTRACTS_DIR, "Contract_Electrician_SparkElectric.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Page 1
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 1*inch, "SUBCONTRACTOR AGREEMENT")

    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 1.5*inch, "This Agreement made on: 1 July 2024")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, height - 1.9*inch, "BETWEEN:")
    c.setFont("Helvetica", 10)
    c.drawString(1.3*inch, height - 2.1*inch, "ABC Construction Pty Ltd (ABN: 12 345 678 901)")
    c.drawString(1.3*inch, height - 2.25*inch, "123 Builder Street, Sydney NSW 2000")
    c.drawString(1.3*inch, height - 2.4*inch, "(hereinafter 'the Principal')")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, height - 2.8*inch, "AND:")
    c.setFont("Helvetica", 10)
    c.drawString(1.3*inch, height - 3*inch, "Bright Spark Electrical Pty Ltd (ABN: 44 223 445 667)")
    c.drawString(1.3*inch, height - 3.15*inch, "321 Sparky Lane, Auburn NSW 2144")
    c.drawString(1.3*inch, height - 3.3*inch, "Electrical Contractor License: EL-123456")
    c.drawString(1.3*inch, height - 3.45*inch, "(hereinafter 'the Subcontractor')")

    y_pos = height - 4*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "1. SCOPE OF WORKS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "The Subcontractor agrees to supply, install and complete all electrical works for:")
    y_pos -= 0.2*inch
    c.drawString(1.2*inch, y_pos, "Project: New Two-Storey Dwelling - 123 Sunset Boulevard, Sydney NSW 2000")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "Including but not limited to:")
    y_pos -= 0.18*inch
    c.drawString(1.4*inch, y_pos, "• Complete electrical installation as per approved plans dated 15/01/2024")
    y_pos -= 0.16*inch
    c.drawString(1.4*inch, y_pos, "• Main switchboard, distribution boards, circuit protection")
    y_pos -= 0.16*inch
    c.drawString(1.4*inch, y_pos, "• Power and lighting circuits, power points, switches, light fittings")
    y_pos -= 0.16*inch
    c.drawString(1.4*inch, y_pos, "• Hardwired smoke alarms (interconnected)")
    y_pos -= 0.16*inch
    c.drawString(1.4*inch, y_pos, "• Hot water, oven/cooktop circuits")
    y_pos -= 0.16*inch
    c.drawString(1.4*inch, y_pos, "• Testing and certification as per AS/NZS 3000")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "2. CONTRACT PRICE")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "Total Contract Sum: $28,540.00 (including GST)")
    y_pos -= 0.18*inch
    c.drawString(1*inch, y_pos, "Payment to be made in accordance with progress claims submitted monthly.")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "3. PAYMENT TERMS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1.2*inch, y_pos, "• Progress claims submitted on last day of each month")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Payment due within 30 days of approved claim")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• 5% retention held until practical completion and defects rectification")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Final retention released 90 days after practical completion")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "4. TIMEFRAME")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "Commencement Date: 15 July 2024")
    y_pos -= 0.16*inch
    c.drawString(1*inch, y_pos, "Completion Date: 30 September 2024")
    y_pos -= 0.16*inch
    c.drawString(1*inch, y_pos, "Time is of the essence. Liquidated damages of $500/day apply for delay.")

    # Footer
    c.setFont("Helvetica", 7)
    c.drawString(width/2 - 0.5*inch, 0.5*inch, "Page 1 of 3")

    # Page 2
    c.showPage()
    c.setFont("Helvetica-Bold", 12)
    y_pos = height - 1*inch
    c.drawString(1*inch, y_pos, "5. VARIATIONS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "No variation to the works shall be made except by written variation order signed by the Principal.")
    y_pos -= 0.16*inch
    c.drawString(1*inch, y_pos, "Subcontractor must provide written quote for variation works within 48 hours of request.")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "6. INSURANCE REQUIREMENTS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "The Subcontractor must maintain throughout the contract period:")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "• Public Liability Insurance: Minimum $20,000,000")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Workers Compensation Insurance as required by law")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Professional Indemnity Insurance: Minimum $5,000,000")
    y_pos -= 0.16*inch
    c.drawString(1*inch, y_pos, "Copies of insurance certificates must be provided before commencement.")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "7. WARRANTY AND DEFECTS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "The Subcontractor warrants all work will be:")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "• Carried out in a proper and workmanlike manner")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Compliant with all relevant Australian Standards and Building Code")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Free from defects for a period of 12 months from practical completion")
    y_pos -= 0.18*inch
    c.drawString(1*inch, y_pos, "Subcontractor must rectify all defects within 7 days of notification.")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "8. SAFETY AND COMPLIANCE")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "The Subcontractor must:")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "• Comply with all WHS regulations and site safety requirements")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Provide all necessary PPE for workers")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Hold current electrical contractor license")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Provide Certificate of Compliance upon completion")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "9. TERMINATION")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "Either party may terminate this agreement for breach with 14 days written notice.")
    y_pos -= 0.16*inch
    c.drawString(1*inch, y_pos, "Principal may terminate immediately for serious breach, insolvency, or safety violations.")

    c.setFont("Helvetica", 7)
    c.drawString(width/2 - 0.5*inch, 0.5*inch, "Page 2 of 3")

    # Page 3 - Signatures
    c.showPage()
    y_pos = height - 1*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "10. GENERAL PROVISIONS")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1.2*inch, y_pos, "• This agreement is governed by the laws of New South Wales")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Disputes to be resolved by mediation before legal action")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Neither party may assign this agreement without written consent")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• All amendments must be in writing and signed by both parties")

    y_pos -= 0.6*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "SIGNATURES")

    y_pos -= 0.5*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y_pos, "FOR THE PRINCIPAL:")
    c.setFont("Helvetica", 9)
    y_pos -= 0.3*inch
    c.drawString(1*inch, y_pos, "Signed: __Michael Johnson________________")
    y_pos -= 0.25*inch
    c.drawString(1*inch, y_pos, "Name: Michael Johnson")
    y_pos -= 0.18*inch
    c.drawString(1*inch, y_pos, "Position: Director, ABC Construction Pty Ltd")
    y_pos -= 0.18*inch
    c.drawString(1*inch, y_pos, "Date: 1 July 2024")

    y_pos -= 0.6*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y_pos, "FOR THE SUBCONTRACTOR:")
    c.setFont("Helvetica", 9)
    y_pos -= 0.3*inch
    c.drawString(1*inch, y_pos, "Signed: __David Patterson________________")
    y_pos -= 0.25*inch
    c.drawString(1*inch, y_pos, "Name: David Patterson")
    y_pos -= 0.18*inch
    c.drawString(1*inch, y_pos, "Position: Director, Bright Spark Electrical Pty Ltd")
    y_pos -= 0.18*inch
    c.drawString(1*inch, y_pos, "Date: 1 July 2024")

    c.setFont("Helvetica", 7)
    c.drawString(width/2 - 0.5*inch, 0.5*inch, "Page 3 of 3")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_plumber_contract():
    filename = os.path.join(CONTRACTS_DIR, "Contract_Plumber_AquaFlow.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Times-Bold", 20)
    c.drawCentredString(width/2, height - 1*inch, "SUBCONTRACT AGREEMENT")
    c.setFont("Times-Italic", 10)
    c.drawCentredString(width/2, height - 1.3*inch, "Plumbing Works")

    c.setFont("Times-Roman", 10)
    y = height - 1.8*inch
    c.drawString(1*inch, y, "Agreement Date: 5 July 2024")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Project: New Dwelling - 123 Sunset Boulevard, Sydney NSW")

    y -= 0.4*inch
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, y, "Principal Contractor:")
    c.setFont("Times-Roman", 9)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "ABC Construction Pty Ltd | ABN: 12 345 678 901 | License: 123456C")

    y -= 0.3*inch
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, y, "Subcontractor:")
    c.setFont("Times-Roman", 9)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "John's Plumbing Services Pty Ltd | ABN: 55 667 889 001 | License: PL-234567")

    y -= 0.4*inch
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, y, "WORKS TO BE PERFORMED:")
    c.setFont("Times-Roman", 9)
    y -= 0.2*inch
    c.drawString(1*inch, y, "Complete plumbing installation including:")
    items = [
        "• Cold and hot water supply systems (copper and PEX pipe)",
        "• Sanitary drainage (PVC 100mm and 150mm)",
        "• Stormwater drainage and connection to Council system",
        "• Installation of fixtures: toilets, basins, showers, bath, kitchen sink",
        "• Hot water system connection (315L electric storage)",
        "• Backflow prevention devices",
        "• Pressure testing and certification to AS/NZS 3500",
    ]
    for item in items:
        y -= 0.16*inch
        c.drawString(1.2*inch, y, item)

    y -= 0.3*inch
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, y, "CONTRACT SUM: $19,150.00 (inc GST)")

    y -= 0.25*inch
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, y, "PAYMENT SCHEDULE:")
    c.setFont("Times-Roman", 9)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Monthly progress claims based on work completed")
    y -= 0.16*inch
    c.drawString(1.2*inch, y, "• Payment within 30 days of approved claim")
    y -= 0.16*inch
    c.drawString(1.2*inch, y, "• 5% retention until final completion + 90 days")

    y -= 0.3*inch
    c.setFont("Times-Bold", 11)
    c.drawString(1*inch, y, "PROGRAM:")
    c.setFont("Times-Roman", 9)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "Start: 20 July 2024 | Completion: 25 September 2024")

    y -= 0.4*inch
    c.setFont("Times-Bold", 10)
    c.drawString(1*inch, y, "Agreed and Accepted:")

    y -= 0.4*inch
    c.setFont("Times-Roman", 9)
    c.drawString(1*inch, y, "Principal: ___M. Johnson_______________ Date: 5/7/2024")
    y -= 0.3*inch
    c.drawString(1*inch, y, "Subcontractor: ___R. Chen______________ Date: 5/7/2024")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_framer_contract():
    filename = os.path.join(CONTRACTS_DIR, "Contract_Framer_BuildRight.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Courier-Bold", 14)
    c.drawString(1*inch, 10.5*inch, "FRAME AND TRUSS SUBCONTRACT AGREEMENT")

    c.setFont("Courier", 9)
    y = 10*inch
    c.drawString(0.75*inch, y, "=" * 90)
    y -= 0.2*inch
    c.drawString(0.75*inch, y, "Date: 10 July 2024")
    y -= 0.18*inch
    c.drawString(0.75*inch, y, "Project: 123 Sunset Boulevard, Sydney NSW 2000")
    y -= 0.18*inch
    c.drawString(0.75*inch, y, "Contract No: BRF-2024-089")

    y -= 0.3*inch
    c.setFont("Courier-Bold", 10)
    c.drawString(0.75*inch, y, "PARTIES:")
    c.setFont("Courier", 9)
    y -= 0.2*inch
    c.drawString(0.75*inch, y, "Builder: ABC Construction Pty Ltd (ABN: 12 345 678 901)")
    y -= 0.16*inch
    c.drawString(0.75*inch, y, "Framer: BuildRight Framers (ABN: 66 778 889 991 | Lic: 234567C)")

    y -= 0.3*inch
    c.setFont("Courier-Bold", 10)
    c.drawString(0.75*inch, y, "SCOPE:")
    c.setFont("Courier", 8)
    y -= 0.18*inch
    c.drawString(0.75*inch, y, "Supply and install all wall frames (external & internal), roof trusses,")
    y -= 0.14*inch
    c.drawString(0.75*inch, y, "sarking, bracing as per approved plans dated 15/01/2024")

    y -= 0.25*inch
    c.setFont("Courier-Bold", 10)
    c.drawString(0.75*inch, y, "PRICE: $46,500.00 + GST = $51,150.00")

    y -= 0.25*inch
    c.setFont("Courier-Bold", 10)
    c.drawString(0.75*inch, y, "PROGRAM:")
    c.setFont("Courier", 9)
    y -= 0.18*inch
    c.drawString(0.75*inch, y, "Start: 1 August 2024 | Complete: 31 August 2024")

    y -= 0.25*inch
    c.setFont("Courier-Bold", 10)
    c.drawString(0.75*inch, y, "PAYMENT:")
    c.setFont("Courier", 8)
    y -= 0.18*inch
    c.drawString(0.75*inch, y, "Progress claims monthly. 30-day payment terms. 5% retention.")

    y -= 0.25*inch
    c.setFont("Courier-Bold", 10)
    c.drawString(0.75*inch, y, "INSURANCE:")
    c.setFont("Courier", 8)
    y -= 0.18*inch
    c.drawString(0.75*inch, y, "Public Liability $20M, Workers Comp, Contract Works as required")

    y -= 0.4*inch
    c.setFont("Courier", 9)
    c.drawString(0.75*inch, y, "Builder Signature: __M. Johnson__________ Date: 10/07/2024")
    y -= 0.25*inch
    c.drawString(0.75*inch, y, "Framer Signature: __T. Williams_________ Date: 10/07/2024")

    c.save()
    print(f"✓ Generated: {filename}")

# =============================================================================
# SITE REPORTS
# =============================================================================
def generate_weekly_progress_report():
    filename = os.path.join(REPORTS_DIR, "Weekly_Progress_Report_Week_12.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 0.8*inch, "WEEKLY PROGRESS REPORT")

    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 1.1*inch, "Project: 123 Sunset Boulevard - New Dwelling")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, height - 1.5*inch, "Week Number: 12")
    c.drawString(1*inch, height - 1.7*inch, "Report Period: 2-8 September 2024")
    c.drawString(1*inch, height - 1.9*inch, "Prepared by: Tom Richards, Site Supervisor")

    y_pos = height - 2.4*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "WORK COMPLETED THIS WEEK:")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    completed = [
        "• Roof tiling 95% complete - ridge capping underway",
        "• External brickwork completed and cleaned",
        "• Window frames installed and flashed",
        "• Plumbing rough-in first fix inspection passed",
        "• Electrical rough-in first fix inspection passed",
        "• External waterproofing to balcony completed",
        "• Garage slab poured and cured",
    ]
    for item in completed:
        c.drawString(1.2*inch, y_pos, item)
        y_pos -= 0.18*inch

    y_pos -= 0.2*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "WORK PLANNED NEXT WEEK:")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    planned = [
        "• Complete roof tiling and ridge capping",
        "• Install gutters and downpipes",
        "• Commence internal framing partition walls",
        "• Bathroom waterproofing",
        "• External render base coat",
        "• Scaffold adjustment for guttering works",
    ]
    for item in planned:
        c.drawString(1.2*inch, y_pos, item)
        y_pos -= 0.18*inch

    y_pos -= 0.2*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "ISSUES AND RISKS:")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.8, 0, 0)
    c.drawString(1.2*inch, y_pos, "⚠ Weather: 2 days lost to rain this week (Monday, Thursday)")
    y_pos -= 0.18*inch
    c.setFillColorRGB(0, 0, 0)
    c.drawString(1.2*inch, y_pos, "• Tile delivery delayed by 1 day - supplier transport issue (resolved)")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "• Awaiting Council inspection for frame (booked for Wednesday 11/09)")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "• Minor rework required on west wall window flashing - rectified")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "PROJECT STATUS:")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1.2*inch, y_pos, "Overall Completion: 65%")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "Program Status: 12 days behind schedule due to weather delays")
    y_pos -= 0.18*inch
    c.drawString(1.2*inch, y_pos, "Budget Status: Tracking over budget by approx $8,500 (under review)")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "SITE VISITORS THIS WEEK:")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1.2*inch, y_pos, "• Monday: Building Inspector (slab inspection - PASS)")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Tuesday: Client walkthrough with owner")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "• Thursday: Structural engineer (beam inspection)")

    y_pos -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_pos, "SAFETY:")

    y_pos -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(1.2*inch, y_pos, "No incidents or near misses reported this week")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "Toolbox talk conducted: Working at Heights (roof works)")
    y_pos -= 0.16*inch
    c.drawString(1.2*inch, y_pos, "Scaffold inspection completed - compliant")

    # Signature
    y_pos -= 0.5*inch
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y_pos, "Site Supervisor: __T. Richards____________")
    c.drawString(4.5*inch, y_pos, "Date: 8 September 2024")

    c.setFont("Helvetica", 7)
    c.drawString(1*inch, 0.5*inch, "Photos attached (not included in this PDF version)")

    c.save()
    print(f"✓ Generated: {filename}")

def generate_site_meeting_minutes():
    filename = os.path.join(REPORTS_DIR, "Site_Meeting_Minutes_Sept15.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(4.25*inch, 10.5*inch, "SITE MEETING MINUTES")

    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 10*inch, "Project: 123 Sunset Boulevard - New Dwelling Construction")
    c.drawString(1*inch, 9.8*inch, "Meeting Date: 15 September 2024, 9:00 AM")
    c.drawString(1*inch, 9.6*inch, "Location: Site Office")

    y = 9.2*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "ATTENDEES:")
    c.setFont("Helvetica", 9)
    y -= 0.2*inch
    c.drawString(1.2*inch, y, "• Michael Johnson - ABC Construction (Project Manager)")
    y -= 0.16*inch
    c.drawString(1.2*inch, y, "• Tom Richards - ABC Construction (Site Supervisor)")
    y -= 0.16*inch
    c.drawString(1.2*inch, y, "• David Patterson - Bright Spark Electrical")
    y -= 0.16*inch
    c.drawString(1.2*inch, y, "• Robert Chen - John's Plumbing Services")
    y -= 0.16*inch
    c.drawString(1.2*inch, y, "• John Smith - Client (Owner)")

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "ITEMS DISCUSSED:")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "1. Project Progress Update")
    c.setFont("Helvetica", 8)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Overall 65% complete, 12 days behind schedule")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Weather delays impacting timeline (8 days lost to rain)")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Roof tiling completed, gutters being installed this week")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "2. Client Variation Requests")
    c.setFont("Helvetica", 8)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Client requested upgrade to ducted air conditioning (quote: $3,200)")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Quote to be provided by HVAC contractor by 20/09")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Additional 8x power points in living areas approved ($960)")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "3. Electrical Works")
    c.setFont("Helvetica", 8)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• First fix rough-in complete and inspected")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Second fix to commence week of 25/09 after plastering")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Light fitting selection required from client by 20/09")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "4. Plumbing Works")
    c.setFont("Helvetica", 8)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• First fix complete, pressure testing passed")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Hot water system delivered, installation scheduled for 18/09")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Bathroom fixture delivery confirmed for 20/09")

    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1*inch, y, "5. Upcoming Inspections")
    c.setFont("Helvetica", 8)
    y -= 0.18*inch
    c.drawString(1.2*inch, y, "• Frame inspection: Wednesday 18/09")
    y -= 0.14*inch
    c.drawString(1.2*inch, y, "• Waterproofing inspection: Friday 20/09")

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "ACTION ITEMS:")

    y -= 0.2*inch
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, y, "Item")
    c.drawString(4*inch, y, "Responsible")
    c.drawString(5.5*inch, y, "Due Date")
    c.line(1*inch, y - 0.05*inch, 7*inch, y - 0.05*inch)

    actions = [
        ("Provide AC upgrade quote", "HVAC Contractor", "20/09/24"),
        ("Client to select light fittings", "J. Smith", "20/09/24"),
        ("Book frame inspection", "T. Richards", "18/09/24"),
        ("Order additional power points", "D. Patterson", "16/09/24"),
        ("Confirm plaster start date", "M. Johnson", "17/09/24"),
    ]

    y -= 0.18*inch
    for item, responsible, due in actions:
        c.drawString(1*inch, y, item)
        c.drawString(4*inch, y, responsible)
        c.drawString(5.5*inch, y, due)
        y -= 0.16*inch

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "NEXT MEETING:")
    c.setFont("Helvetica", 9)
    y -= 0.2*inch
    c.drawString(1*inch, y, "Date: 22 September 2024, 9:00 AM")
    y -= 0.16*inch
    c.drawString(1*inch, y, "Location: Site Office")

    y -= 0.4*inch
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, y, "Minutes prepared by: T. Richards")
    c.drawString(4.5*inch, y, "Date: 15 September 2024")

    c.save()
    print(f"✓ Generated: {filename}")

if __name__ == "__main__":
    print("\n=== Subcontractor Contracts ===")
    generate_electrician_contract()
    generate_plumber_contract()
    generate_framer_contract()

    print("\n=== Site Reports ===")
    generate_weekly_progress_report()
    generate_site_meeting_minutes()

    print("\n✓ All PDF documents generated successfully!")
