"""
Generate ALL missing PDF files with realistic content
"""
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).parent / "dummy_data"

def pdf(file_path, title, lines):
    c = canvas.Canvas(str(file_path), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, title)
    c.setFont("Helvetica", 10)
    y = height - 1.5*inch
    for line in lines:
        c.drawString(1*inch, y, str(line))
        y -= 0.25*inch
        if y < 1*inch: c.showPage(); c.setFont("Helvetica", 10); y = height - 1*inch
    c.save()
    print(f"✓ {file_path.name}")

print("="*70)
print("GENERATING ALL PDF FILES")
print("="*70)

# 01_LAND_PURCHASE
print("\\n[01_LAND_PURCHASE]")
f = BASE_DIR / "01_LAND_PURCHASE"
f.mkdir(parents=True, exist_ok=True)

pdf(f / "Land_Contract_FINAL_v3.pdf", "LAND PURCHASE CONTRACT", [
    "Contract of Sale - Residential Land",
    "Property: 123 Sunset Boulevard, Sydney NSW 2000",
    "", "VENDOR: Previous Owner Pty Ltd", "PURCHASER: John Smith",
    "", "Purchase Price: $250,000.00",
    "Deposit Paid: $25,000.00 (10%)",
    "Balance Due: $225,000.00",
    "", "Settlement Date: 15 June 2024",
    "", "Special Conditions:",
    "1. Subject to finance approval",
    "2. Building & pest inspection satisfactory",
    "3. Clear title transfer",
    "", "Signed: 1 June 2024",
    "Vendor Signature: [signed]",
    "Purchaser Signature: [signed]"
])

pdf(f / "Title_Deed_Scanned.pdf", "CERTIFICATE OF TITLE", [
    "STATE OF NEW SOUTH WALES",
    "LAND AND PROPERTY INFORMATION",
    "", "LOT 15 DP 123456",
    "123 Sunset Boulevard, Sydney NSW 2000",
    "", "FOLIO IDENTIFIER: 15/123456",
    "", "Registered Proprietor: JOHN SMITH",
    "Date Registered: 20 June 2024",
    "", "Estate: Fee Simple",
    "Encumbrances: Mortgage to ANZ Bank",
    "", "Land Dimensions:",
    "Frontage: 15.24 metres",
    "Depth: 30.48 metres",
    "Area: 465 square metres",
    "", "[STAMP: NSW Land Registry Services]",
    "[SEAL]"
])

pdf(f / "Survey_Report_Aug2024.pdf", "LAND SURVEY REPORT", [
    "Survey Report - Residential Land",
    "Property: 123 Sunset Boulevard, Sydney",
    "Date: 22 August 2024",
    "Surveyor: Land Survey Services Pty Ltd",
    "", "FINDINGS:",
    "Lot 15 DP 123456",
    "Total Area: 465.3 square metres",
    "Frontage to Street: 15.24m",
    "Side Boundaries: 30.48m (both sides)",
    "", "Levels:",
    "Front boundary RL: 12.45m AHD",
    "Rear boundary RL: 12.89m AHD",
    "Fall across site: 0.44m (rear higher)",
    "", "Services Located:",
    "- Water main in street",
    "- Sewer connection available",
    "- Power pole at front boundary",
    "", "Surveyor: Mark Johnson, Registered Surveyor #12345"
])

pdf(f / "Legal_Fees_Invoice_JohnsonSolicitors.pdf", "TAX INVOICE", [
    "Johnson & Partners Solicitors",
    "Level 5, 100 George Street, Sydney NSW 2000",
    "ABN: 12 345 678 901",
    "", "INVOICE: JS-2024-0847",
    "Date: 20 June 2024",
    "Client: John Smith",
    "", "RE: Purchase of 123 Sunset Boulevard",
    "", "Professional Services:",
    "Contract review and advice         $1,200.00",
    "Conveyancing services              $1,000.00",
    "Title search and verification        $350.00",
    "Disbursements (searches, etc)        $250.00",
    "                                  -----------",
    "Subtotal                           $2,800.00",
    "GST (10%)                            $280.00",
    "                                  ===========",
    "TOTAL DUE                          $3,080.00",
    "", "Payment Terms: 7 days",
    "Bank Details: BSB 012-345  Acc: 123456789"
])

pdf(f / "Soil_Test_Report_GeoTech.pdf", "GEOTECHNICAL INVESTIGATION REPORT", [
    "Site: 123 Sunset Boulevard, Sydney NSW",
    "Client: John Smith",
    "Date: 25 June 2024",
    "Report by: GeoTech Surveyors Pty Ltd",
    "", "EXECUTIVE SUMMARY:",
    "A geotechnical investigation was conducted to assess",
    "soil conditions for residential construction.",
    "", "FINDINGS:",
    "Borehole 1 (Front): 0-0.5m topsoil, 0.5-2.5m clay",
    "Borehole 2 (Rear): 0-0.4m topsoil, 0.4-3.0m clay",
    "", "Soil Classification: SC (Slightly Reactive Clay)",
    "Bearing Capacity: 150 kPa",
    "", "RECOMMENDATIONS:",
    "1. Conventional strip footings suitable",
    "2. Minimum footing width: 450mm",
    "3. Minimum footing depth: 600mm below NGL",
    "4. No special foundation treatment required",
    "5. Good drainage essential",
    "", "Report prepared by:",
    "Dr. Sarah Chen, Senior Geotechnical Engineer",
    "GeoTech Surveyors"
])

# 02_PERMITS_APPROVALS
print("\\n[02_PERMITS_APPROVALS]")
f = BASE_DIR / "02_PERMITS_APPROVALS"

pdf(f / "Building_Permit_Application.pdf", "BUILDING PERMIT APPLICATION", [
    "Sydney Council - Building Services",
    "Application No: BP-2024-12345",
    "Date Lodged: 15 July 2024",
    "", "Applicant: John Smith",
    "Builder: Smith Constructions Pty Ltd",
    "License: 123456C",
    "", "Property: 123 Sunset Boulevard, Sydney",
    "Lot 15 DP 123456",
    "", "Proposed Works:",
    "Construction of new two-storey dwelling",
    "", "Development Details:",
    "Building Type: Class 1a Dwelling",
    "Storeys: 2",
    "Floor Area: 245 square metres",
    "Construction Type: Brick veneer timber frame",
    "", "Estimated Cost: $450,000",
    "", "Certifier: BuildCert Australia",
    "Certifier License: C12345",
    "", "Application Fee: $4,200.00 (paid)",
    "", "Applicant Signature: [signed]",
    "Date: 15/07/2024"
])

pdf(f / "DA_Development_Application_Council.pdf", "DEVELOPMENT APPLICATION", [
    "SYDNEY CITY COUNCIL",
    "Development Application",
    "DA Number: DA/2024/0567",
    "", "Property: 123 Sunset Boulevard, Sydney NSW 2000",
    "Applicant: John Smith",
    "", "Proposed Development:",
    "Demolition of existing structures and construction",
    "of new two-storey detached dwelling",
    "", "Site Area: 465 square metres",
    "Proposed GFA: 245 square metres",
    "FSR: 0.53:1 (compliant)",
    "Height: 8.2 metres (compliant)",
    "Setbacks: Front 5.5m, Side 1.2m/1.5m, Rear 6m",
    "", "Car Parking: 2 spaces provided (compliant)",
    "", "Landscaping: 40% of site",
    "", "Public Notification Period: 14 days",
    "Submissions Received: 0",
    "", "RECOMMENDATION: APPROVAL",
    "", "Approved: 10 July 2024",
    "Consent Authority: Council Delegate"
])

pdf(f / "Council_Fees_Receipt.pdf", "OFFICIAL RECEIPT", [
    "SYDNEY CITY COUNCIL",
    "Financial Services",
    "", "Receipt No: RCT-2024-8845",
    "Date: 15 July 2024",
    "", "Paid by: John Smith",
    "Property: 123 Sunset Boulevard",
    "", "Description                        Amount",
    "--------------------------------------",
    "DA Application Fee              $2,850.00",
    "                               ==========",
    "TOTAL PAID                      $2,850.00",
    "", "Payment Method: Credit Card",
    "Card: XXXX-XXXX-XXXX-1234",
    "", "This is your official receipt.",
    "Keep for your records.",
    "", "[STAMP: PAID]"
])

pdf(f / "Water_Connection_Approval.pdf", "WATER CONNECTION APPROVAL", [
    "SYDNEY WATER",
    "New Connections",
    "", "Application No: WC-2024-5678",
    "Date: 5 August 2024",
    "", "Property: 123 Sunset Boulevard, Sydney",
    "Owner: John Smith",
    "", "APPROVAL GRANTED",
    "", "Water Connection: Approved",
    "Sewer Connection: Approved",
    "", "Connection Points:",
    "Water: Existing 20mm main in street",
    "Sewer: Existing 150mm sewer main",
    "", "Connection Fee: $1,200.00",
    "Status: PAID",
    "", "Plumber License Required: YES",
    "Licensed Plumber: AquaFlow Plumbing (L123456)",
    "", "Conditions:",
    "1. Water meter to be installed by Sydney Water",
    "2. Backflow prevention device required",
    "3. All work must comply with AS/NZS 3500",
    "", "Approved by: John Williams",
    "Sydney Water - Connections Team"
])

pdf(f / "Electricity_Connection_Quote.pdf", "ELECTRICITY CONNECTION QUOTE", [
    "AUSGRID",
    "New Connections",
    "", "Quote No: EC-2024-9012",
    "Date: 8 August 2024",
    "", "Customer: John Smith",
    "Site: 123 Sunset Boulevard, Sydney",
    "", "Connection Type: New Single Phase Service",
    "Supply: 230V 63A",
    "", "Works Required:",
    "- New service mains from pole",
    "- New meter box installation",
    "- Underground service cable 15 metres",
    "", "Quote Amount:              $2,450.00",
    "GST:                         $245.00",
    "                           ==========",
    "TOTAL:                     $2,695.00",
    "", "Quote valid: 90 days",
    "", "Payment terms: Full payment before connection",
    "", "Electrical contractor required:",
    "Level 2 ASP License needed for connection",
    "", "For queries contact: 13 13 65"
])

pdf(f / "Energy_Rating_Certificate.pdf", "BASIX CERTIFICATE", [
    "Building Sustainability Index (BASIX)",
    "NSW Department of Planning",
    "", "Certificate No: 123456A_01",
    "Issue Date: 12 July 2024",
    "", "Development Address:",
    "123 Sunset Boulevard, Sydney NSW 2000",
    "", "Applicant: John Smith",
    "Assessor: EnergyRate Consultants",
    "", "Dwelling Type: New Detached House",
    "Number of Storeys: 2",
    "Conditioned Floor Area: 180 sqm",
    "", "BASIX COMMITMENTS:",
    "", "Water:",
    "Target: 40 points",
    "Achieved: 42 points - PASS",
    "", "Energy:",
    "Target: 50 points",
    "Achieved: 53 points - PASS",
    "", "Thermal Comfort:",
    "Heating Load: Compliant",
    "Cooling Load: Compliant",
    "", "This certificate must be submitted with",
    "Development Application and Building Permit.",
    "", "Valid for 2 years from issue date"
])

# Continue with more PDF files in next message due to length...
print("\\n[03_DESIGN_DRAWINGS]")
f = BASE_DIR / "03_DESIGN_DRAWINGS/Architectural"
f.mkdir(parents=True, exist_ok=True)

pdf(f / "HOUSE_A_PLANS_REV_A.pdf", "ARCHITECTURAL PLANS - REVISION A", [
    "Project: NEW DWELLING",
    "Address: 123 Sunset Boulevard, Sydney",
    "Client: John Smith",
    "", "Drawing Set: Architectural Plans",
    "Revision: A",
    "Date: 25 June 2024",
    "Architect: Smith & Associates Architecture",
    "", "SHEET INDEX:",
    "A01 - Site Plan",
    "A02 - Ground Floor Plan",
    "A03 - First Floor Plan",
    "A04 - Elevations North & South",
    "A05 - Elevations East & West",
    "A06 - Sections",
    "", "KEY FEATURES:",
    "- 4 Bedroom, 2.5 Bathroom",
    "- Double garage",
    "- Open plan living/dining/kitchen",
    "- Alfresco area",
    "", "Total Floor Area: 245 sqm",
    "Site Coverage: 52%",
    "", "Architect: David Smith",
    "Reg. Architect: NSW 12345"
])

pdf(f / "HOUSE_A_PLANS_REV_B.pdf", "ARCHITECTURAL PLANS - REVISION B", [
    "Project: NEW DWELLING",
    "Address: 123 Sunset Boulevard, Sydney",
    "", "Drawing Set: Architectural Plans",
    "Revision: B (Council Comments Addressed)",
    "Date: 5 July 2024",
    "", "REVISIONS FROM REV A:",
    "- Increased front setback to 5.5m",
    "- Reduced eastern side setback to 1.2m",
    "- Revised window locations for privacy",
    "- Added additional landscaping",
    "- Updated carport to enclosed garage",
    "", "All revisions comply with DCP requirements",
    "", "Architect: David Smith",
    "Approved for Construction: YES"
])

pdf(f / "HOUSE_A_PLANS_FINAL.pdf", "ARCHITECTURAL PLANS - FINAL", [
    "Project: NEW DWELLING",
    "123 Sunset Boulevard, Sydney NSW",
    "", "Drawing Set: CONSTRUCTION DOCUMENTATION",
    "Status: FINAL FOR CONSTRUCTION",
    "Date: 20 July 2024",
    "", "APPROVED PLANS",
    "DA Approval: DA/2024/0567",
    "Building Permit: BP-2024-12345",
    "", "This drawing set is approved for construction",
    "No changes without architect approval",
    "", "Total Sheets: 15",
    "", "Architect:",
    "Smith & Associates Architecture",
    "David Smith - Registered Architect NSW 12345",
    "", "[STAMP: APPROVED FOR CONSTRUCTION]"
])

pdf(f / "Architect_Invoice_1.pdf", "TAX INVOICE", [
    "Smith & Associates Architecture",
    "ABN: 23 456 789 012",
    "", "Invoice: ARCH-001",
    "Date: 30 June 2024",
    "Client: John Smith",
    "", "RE: New Dwelling - 123 Sunset Boulevard",
    "", "Design Services - Stage 1",
    "Concept Design                     $4,000.00",
    "Design Development                 $3,500.00",
    "DA Documentation                   $2,500.00",
    "                                  ----------",
    "Subtotal                          $10,000.00",
    "GST                                $1,000.00",
    "                                  ==========",
    "TOTAL                             $11,000.00",
    "", "Payment Terms: 14 days",
    "Status: PAID"
])

pdf(f / "Architect_Invoice_2_REVISED.pdf", "TAX INVOICE - REVISED", [
    "Smith & Associates Architecture",
    "", "Invoice: ARCH-002-REV",
    "Date: 15 August 2024",
    "Client: John Smith",
    "", "Construction Documentation",
    "Working Drawings                   $5,000.00",
    "Specifications                     $1,500.00",
    "Council Liaison                    $1,200.00",
    "Extra Revisions (3 rounds)         $2,400.00",
    "                                  ----------",
    "Subtotal                           $10,100.00",
    "GST                                 $1,010.00",
    "                                  ==========",
    "TOTAL                              $11,110.00",
    "", "NOTE: Additional $2,400 for extra revisions",
    "due to client changes after DA approval"
])

print("\\n>>> PDF Generation: Phase 1 Complete (Folders 01-03)")
print(">>> Total PDFs created so far...")
