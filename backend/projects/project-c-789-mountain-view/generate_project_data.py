"""
Generate comprehensive realistic dummy data for Project C - Mountain View
A luxury mountain retreat with high-end finishes
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Project details
PROJECT_ID = "project-c-789-mountain-view"
PROJECT_NAME = "789 Mountain View Terrace"
CONTRACT_VALUE = 820000
START_DATE = datetime(2024, 8, 1)
CURRENT_DATE = datetime(2024, 10, 3)

# Base path
BASE_PATH = Path("data")

def random_date(start, end):
    """Generate random date between start and end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def create_land_purchase_documents():
    """01_LAND_PURCHASE"""
    folder = BASE_PATH / "01_LAND_PURCHASE"

    # Land purchase contract
    contract = {
        "document_type": "Land Purchase Contract",
        "date": "2024-06-15",
        "seller": "Blue Mountains Land Trust",
        "buyer": "Michael & Emma Chen",
        "property_address": "789 Mountain View Terrace, Blue Mountains NSW 2780",
        "land_area_sqm": 1200,
        "purchase_price": 385000,
        "deposit_paid": 38500,
        "settlement_date": "2024-07-30",
        "agent": "Mountain Realty Partners",
        "agent_commission": 11550,
        "legal_fees": 3200,
        "stamp_duty": 18465,
        "total_land_cost": 418215
    }

    with open(folder / "land_purchase_contract.json", 'w') as f:
        json.dump(contract, f, indent=2)

    # Land survey
    survey = {
        "document_type": "Land Survey Report",
        "date": "2024-07-10",
        "surveyor": "Alpine Survey Services",
        "surveyor_fee": 2850,
        "lot_number": "LP 789456",
        "street_frontage_m": 25,
        "depth_m": 48,
        "total_area_sqm": 1200,
        "topography": "Sloping with mountain views",
        "access": "Sealed road access",
        "services_available": ["Electricity", "Town Water", "NBN", "Sewerage"]
    }

    with open(folder / "land_survey_report.json", 'w') as f:
        json.dump(survey, f, indent=2)

    # Title deed
    title = {
        "document_type": "Certificate of Title",
        "title_reference": "Vol 12456 Fol 789",
        "registered_owners": ["Michael Chen", "Emma Chen"],
        "date_registered": "2024-07-30",
        "encumbrances": [
            {"type": "Mortgage", "mortgagee": "Mountain View Credit Union", "amount": 308000}
        ]
    }

    with open(folder / "title_deed.json", 'w') as f:
        json.dump(title, f, indent=2)

def create_permits_approvals():
    """02_PERMITS_APPROVALS"""
    folder = BASE_PATH / "02_PERMITS_APPROVALS"

    # DA approval
    da = {
        "document_type": "Development Application Approval",
        "da_number": "DA/2024/0789",
        "council": "Blue Mountains City Council",
        "approval_date": "2024-07-25",
        "applicant": "Alpine Architecture Group",
        "approved_use": "Residential Dwelling - Luxury Mountain Retreat",
        "conditions": 28,
        "application_fee": 4850,
        "section94_contributions": 12400,
        "approved_floor_area_sqm": 380,
        "approved_bedrooms": 5,
        "approved_bathrooms": 4,
        "approved_parking": 3,
        "expiry_date": "2026-07-25"
    }

    with open(folder / "development_approval.json", 'w') as f:
        json.dump(da, f, indent=2)

    # Construction certificate
    cc = {
        "document_type": "Construction Certificate",
        "cc_number": "CC/2024/0789",
        "certifier": "Blue Mountains Certification Services",
        "issue_date": "2024-08-10",
        "fee": 3650,
        "approved_builder": "Mountain Homes Builders",
        "license_number": "LIC 298456",
        "commencement_date": "2024-08-15",
        "estimated_completion": "2025-06-30"
    }

    with open(folder / "construction_certificate.json", 'w') as f:
        json.dump(cc, f, indent=2)

    # Bushfire assessment
    bushfire = {
        "document_type": "Bushfire Attack Level Assessment",
        "assessment_date": "2024-07-05",
        "assessor": "Mountain Fire Safety Consultants",
        "fee": 1850,
        "bal_rating": "BAL-12.5",
        "requirements": [
            "Ember protection mesh on vents",
            "Fire-rated windows and doors",
            "Non-combustible wall cladding",
            "Asset Protection Zone 20m minimum"
        ]
    }

    with open(folder / "bushfire_assessment.json", 'w') as f:
        json.dump(bushfire, f, indent=2)

    # Geotechnical report
    geotech = {
        "document_type": "Geotechnical Investigation Report",
        "date": "2024-06-20",
        "consultant": "Rock Solid Geotechnical",
        "fee": 4200,
        "boreholes": 4,
        "soil_type": "Weathered sandstone over bedrock",
        "bearing_capacity_kpa": 150,
        "foundation_recommendation": "Strip footings with stepped design",
        "drainage_recommendation": "Subsurface drainage and retaining walls",
        "estimated_earthworks": 28500
    }

    with open(folder / "geotechnical_report.json", 'w') as f:
        json.dump(geotech, f, indent=2)

def create_design_drawings():
    """03_DESIGN_DRAWINGS"""
    folder = BASE_PATH / "03_DESIGN_DRAWINGS"

    # Architectural plans
    arch_plans = {
        "document_type": "Architectural Plans Package",
        "architect": "Alpine Architecture Group",
        "project_architect": "Sarah Mitchell",
        "date": "2024-07-15",
        "revision": "Rev D - For Construction",
        "fee": 42000,
        "drawings_included": [
            "Site Plan",
            "Floor Plans - Ground & Upper Levels",
            "Roof Plan",
            "Elevations - All Sides",
            "Sections",
            "Window & Door Schedule",
            "Internal Elevations - Kitchen, Bathrooms",
            "Joinery Details"
        ],
        "key_features": {
            "total_area_sqm": 380,
            "ground_floor_sqm": 220,
            "upper_floor_sqm": 160,
            "outdoor_deck_sqm": 85,
            "garage_bays": 3,
            "bedrooms": 5,
            "bathrooms": 4,
            "living_areas": 3,
            "special_rooms": ["Home Theater", "Wine Cellar", "Study", "Gym"]
        }
    }

    with open(folder / "architectural_plans.json", 'w') as f:
        json.dump(arch_plans, f, indent=2)

    # Engineering plans
    eng_plans = {
        "document_type": "Structural Engineering Plans",
        "engineer": "Mountain Structural Engineers Pty Ltd",
        "date": "2024-07-20",
        "fee": 18500,
        "drawings": [
            "Foundation Plan",
            "Slab Reinforcement",
            "Framing Plans - Timber",
            "Retaining Wall Details",
            "Steel Beam Schedules"
        ]
    }

    with open(folder / "engineering_plans.json", 'w') as f:
        json.dump(eng_plans, f, indent=2)

def create_finance_insurance():
    """04_FINANCE_INSURANCE"""
    folder = BASE_PATH / "04_FINANCE_INSURANCE"

    # Construction loan
    loan = {
        "document_type": "Construction Loan Agreement",
        "lender": "Mountain View Credit Union",
        "loan_number": "CL-2024-789456",
        "approval_date": "2024-07-15",
        "total_approved": 575000,
        "land_component": 308000,
        "construction_component": 267000,
        "interest_rate_percent": 6.85,
        "loan_term_months": 24,
        "drawdown_schedule": [
            {"stage": "Land Purchase", "amount": 308000, "status": "Drawn"},
            {"stage": "Site Prep & Footings", "amount": 85000, "status": "Drawn"},
            {"stage": "Frame & Roof", "amount": 95000, "status": "Pending"},
            {"stage": "Internal Fit-out", "amount": 52000, "status": "Pending"},
            {"stage": "Final Completion", "amount": 35000, "status": "Pending"}
        ],
        "establishment_fee": 2850,
        "monthly_interest_payment": 2750
    }

    with open(folder / "construction_loan.json", 'w') as f:
        json.dump(loan, f, indent=2)

    # Insurance
    insurance = {
        "document_type": "Construction Insurance Policy",
        "insurer": "Alpine Insurance Group",
        "policy_number": "CIP-789-2024",
        "effective_date": "2024-08-01",
        "expiry_date": "2025-08-01",
        "sum_insured": 820000,
        "annual_premium": 4280,
        "coverage": [
            "Contract Works",
            "Public Liability $20M",
            "Professional Indemnity",
            "Delay in Start-up"
        ]
    }

    with open(folder / "construction_insurance.json", 'w') as f:
        json.dump(insurance, f, indent=2)

def create_quotes_estimates():
    """05_QUOTES_ESTIMATES"""
    folder = BASE_PATH / "05_QUOTES_ESTIMATES"

    # Main builder quote
    builder_quote = {
        "document_type": "Builder's Quote",
        "quote_number": "Q-2024-0789",
        "builder": "Mountain Homes Builders",
        "date": "2024-07-10",
        "valid_until": "2024-09-10",
        "contact": "David Thompson - Director",
        "breakdown": {
            "site_preparation": 45000,
            "foundations_concrete": 78000,
            "framing_carpentry": 125000,
            "roofing": 52000,
            "external_cladding": 68000,
            "windows_doors": 85000,
            "plumbing_rough_in": 38000,
            "electrical_rough_in": 42000,
            "insulation_sarking": 18000,
            "plasterboard_internal": 45000,
            "tiling": 38000,
            "kitchen_supply_install": 55000,
            "bathroom_fit_out": 48000,
            "flooring": 42000,
            "painting_internal_external": 35000,
            "cabinetry_joinery": 38000,
            "final_fixtures_fittings": 28000,
            "garage_driveway": 32000,
            "landscaping_basic": 25000,
            "preliminaries_margin": 105000
        },
        "total_quoted": 1041000,
        "gst_included": True,
        "payment_schedule": "Progress payments as per contract"
    }

    with open(folder / "main_builder_quote.json", 'w') as f:
        json.dump(builder_quote, f, indent=2)

def create_purchase_orders_invoices():
    """06_PURCHASE_ORDERS_INVOICES"""
    folder = BASE_PATH / "06_PURCHASE_ORDERS_INVOICES"

    # Sample invoices
    invoices = []

    # Site preparation invoice
    inv1 = {
        "invoice_number": "INV-2024-1001",
        "supplier": "Mountain Earthmoving Services",
        "date": "2024-08-20",
        "due_date": "2024-09-10",
        "items": [
            {"description": "Site clearing and vegetation removal", "quantity": 1, "unit_price": 8500, "amount": 8500},
            {"description": "Bulk excavation - 180m3", "quantity": 180, "unit_price": 45, "amount": 8100},
            {"description": "Cut and fill earthworks", "quantity": 1, "unit_price": 12500, "amount": 12500},
            {"description": "Compaction and site preparation", "quantity": 1, "unit_price": 6200, "amount": 6200}
        ],
        "subtotal": 35300,
        "gst": 3530,
        "total": 38830,
        "payment_status": "Paid",
        "payment_date": "2024-09-05"
    }
    invoices.append(inv1)

    # Concrete foundation invoice
    inv2 = {
        "invoice_number": "INV-2024-2089",
        "supplier": "Blue Mountains Concrete Solutions",
        "date": "2024-09-05",
        "due_date": "2024-09-25",
        "items": [
            {"description": "Strip footings - 45m3 N32 concrete", "quantity": 45, "unit_price": 285, "amount": 12825},
            {"description": "Concrete pump hire", "quantity": 1, "unit_price": 850, "amount": 850},
            {"description": "Reinforcement steel mesh & bars", "quantity": 1, "unit_price": 8950, "amount": 8950},
            {"description": "Formwork and boxing", "quantity": 1, "unit_price": 6500, "amount": 6500},
            {"description": "Labour - placement and finishing", "quantity": 1, "unit_price": 12800, "amount": 12800}
        ],
        "subtotal": 41925,
        "gst": 4192.50,
        "total": 46117.50,
        "payment_status": "Paid",
        "payment_date": "2024-09-18"
    }
    invoices.append(inv2)

    # Timber framing materials
    inv3 = {
        "invoice_number": "INV-2024-5678",
        "supplier": "Alpine Timber & Hardware",
        "date": "2024-09-15",
        "due_date": "2024-10-05",
        "items": [
            {"description": "F27 Pine framing timber - wall frames", "quantity": 1, "unit_price": 28500, "amount": 28500},
            {"description": "LVL beams and lintels", "quantity": 1, "unit_price": 12400, "amount": 12400},
            {"description": "Roof trusses - engineered", "quantity": 1, "unit_price": 18900, "amount": 18900},
            {"description": "Treated pine for retaining", "quantity": 1, "unit_price": 5800, "amount": 5800},
            {"description": "Fixings, nails, brackets", "quantity": 1, "unit_price": 3200, "amount": 3200}
        ],
        "subtotal": 68800,
        "gst": 6880,
        "total": 75680,
        "payment_status": "Pending",
        "due_days_remaining": 15
    }
    invoices.append(inv3)

    # Plumbing materials
    inv4 = {
        "invoice_number": "INV-2024-8923",
        "supplier": "Mountain Plumbing Supplies",
        "date": "2024-09-25",
        "due_date": "2024-10-15",
        "items": [
            {"description": "Copper piping and fittings", "quantity": 1, "unit_price": 6800, "amount": 6800},
            {"description": "PVC drainage pipes and fittings", "quantity": 1, "unit_price": 2850, "amount": 2850},
            {"description": "Hot water system - Rheem 315L", "quantity": 1, "unit_price": 2950, "amount": 2950},
            {"description": "Bathroom fixtures - premium range", "quantity": 1, "unit_price": 8500, "amount": 8500},
            {"description": "Kitchen tapware - Grohe", "quantity": 1, "unit_price": 1280, "amount": 1280}
        ],
        "subtotal": 22380,
        "gst": 2238,
        "total": 24618,
        "payment_status": "Pending",
        "due_days_remaining": 12
    }
    invoices.append(inv4)

    for idx, inv in enumerate(invoices, 1):
        with open(folder / f"invoice_{idx:03d}.json", 'w') as f:
            json.dump(inv, f, indent=2)

def create_subcontractors():
    """07_SUBCONTRACTORS"""
    folder = BASE_PATH / "07_SUBCONTRACTORS"

    subcontractors = [
        {
            "contractor_name": "Elite Framing Solutions",
            "trade": "Carpentry - Framing",
            "contact": "James Robertson",
            "phone": "0428 765 432",
            "abn": "78 945 612 345",
            "license": "LIC 187654",
            "contract_value": 125000,
            "scope": "Wall and roof framing, internal framing",
            "start_date": "2024-09-15",
            "completion_date": "2024-11-05",
            "payment_terms": "Monthly progress claims",
            "insurance_current": True,
            "work_orders": [
                {"date": "2024-09-15", "description": "Mobilization and frame ground floor", "value": 42000, "status": "In Progress"},
                {"date": "2024-10-10", "description": "Upper floor frame", "value": 45000, "status": "Scheduled"},
                {"date": "2024-10-25", "description": "Roof framing and completion", "value": 38000, "status": "Scheduled"}
            ]
        },
        {
            "contractor_name": "Alpine Plumbing Services",
            "trade": "Plumbing",
            "contact": "Robert Chen",
            "phone": "0412 543 876",
            "abn": "45 123 789 456",
            "license": "LIC 234567",
            "contract_value": 68000,
            "scope": "All plumbing - rough-in and final fix",
            "start_date": "2024-10-01",
            "completion_date": "2025-03-15",
            "payment_terms": "Stage payments",
            "insurance_current": True,
            "work_orders": [
                {"date": "2024-10-01", "description": "Underground drainage", "value": 12500, "status": "Scheduled"},
                {"date": "2024-11-15", "description": "Rough-in plumbing", "value": 28000, "status": "Scheduled"},
                {"date": "2025-02-01", "description": "Final fix and commissioning", "value": 27500, "status": "Scheduled"}
            ]
        },
        {
            "contractor_name": "PowerTech Electrical",
            "trade": "Electrical",
            "contact": "Sarah Mitchell",
            "phone": "0421 876 543",
            "abn": "89 456 123 789",
            "license": "LIC 345678",
            "contract_value": 72000,
            "scope": "Full electrical installation including home automation",
            "start_date": "2024-10-15",
            "completion_date": "2025-04-30",
            "payment_terms": "Monthly claims",
            "insurance_current": True,
            "work_orders": [
                {"date": "2024-10-15", "description": "Temporary power and rough-in", "value": 32000, "status": "Scheduled"},
                {"date": "2025-02-15", "description": "Second fix and lighting", "value": 25000, "status": "Scheduled"},
                {"date": "2025-04-15", "description": "Home automation and final", "value": 15000, "status": "Scheduled"}
            ]
        },
        {
            "contractor_name": "Mountain View Roofing",
            "trade": "Roofing",
            "contact": "Tom Wilson",
            "phone": "0438 234 567",
            "abn": "23 789 456 123",
            "license": "LIC 456789",
            "contract_value": 52000,
            "scope": "Colorbond roof with skylights",
            "start_date": "2024-11-01",
            "completion_date": "2024-12-15",
            "payment_terms": "50% on start, 50% on completion",
            "insurance_current": True
        },
        {
            "contractor_name": "Precision Tiling Co",
            "trade": "Tiling",
            "contact": "Maria Santos",
            "phone": "0434 567 890",
            "abn": "67 234 567 890",
            "license": "LIC 567890",
            "contract_value": 48000,
            "scope": "All internal and external tiling",
            "start_date": "2025-01-15",
            "completion_date": "2025-03-30",
            "payment_terms": "Weekly progress claims"
        }
    ]

    for idx, sc in enumerate(subcontractors, 1):
        with open(folder / f"subcontractor_{idx:02d}_{sc['contractor_name'].replace(' ', '_').lower()}.json", 'w') as f:
            json.dump(sc, f, indent=2)

def create_labour_timesheets():
    """08_LABOUR_TIMESHEETS"""
    folder = BASE_PATH / "08_LABOUR_TIMESHEETS"

    # Generate timesheets for September
    workers = [
        {"name": "Jake Morrison", "role": "Site Supervisor", "rate": 65},
        {"name": "Chris Anderson", "role": "Leading Hand", "rate": 55},
        {"name": "Ben Taylor", "role": "Carpenter", "rate": 48},
        {"name": "Luke Davis", "role": "Labourer", "rate": 38},
        {"name": "Ryan Phillips", "role": "Apprentice", "rate": 25}
    ]

    for week in range(1, 5):
        week_start = datetime(2024, 9, 1) + timedelta(weeks=week-1)
        timesheet = {
            "document_type": "Weekly Timesheet",
            "week_commencing": week_start.strftime("%Y-%m-%d"),
            "workers": []
        }

        for worker in workers:
            hours = random.randint(36, 45)
            overtime = random.randint(0, 8) if week > 2 else 0

            timesheet["workers"].append({
                "name": worker["name"],
                "role": worker["role"],
                "hourly_rate": worker["rate"],
                "regular_hours": hours,
                "overtime_hours": overtime,
                "regular_pay": hours * worker["rate"],
                "overtime_pay": overtime * worker["rate"] * 1.5,
                "total_pay": (hours * worker["rate"]) + (overtime * worker["rate"] * 1.5)
            })

        timesheet["week_total"] = sum(w["total_pay"] for w in timesheet["workers"])

        with open(folder / f"timesheet_week_{week}_sep_2024.json", 'w') as f:
            json.dump(timesheet, f, indent=2)

def create_client_billing():
    """11_CLIENT_BILLING"""
    folder = BASE_PATH / "11_CLIENT_BILLING"

    progress_claims = []

    # Claim 1 - Deposit
    claim1 = {
        "claim_number": "PC-001",
        "date": "2024-08-01",
        "claim_type": "Deposit",
        "description": "Initial deposit on contract signing",
        "contract_value": 820000,
        "claim_percentage": 10,
        "claim_amount": 82000,
        "gst": 8200,
        "total_claim": 90200,
        "previous_claims": 0,
        "total_claimed_to_date": 82000,
        "payment_status": "Paid",
        "payment_date": "2024-08-05",
        "payment_method": "Bank Transfer"
    }
    progress_claims.append(claim1)

    # Claim 2 - Site works and foundations
    claim2 = {
        "claim_number": "PC-002",
        "date": "2024-09-15",
        "claim_type": "Progress Payment",
        "description": "Site works, earthworks, and foundation completion",
        "work_completed": [
            {"item": "Site clearing and preparation", "value": 38830, "percentage": 100},
            {"item": "Earthworks and retaining", "value": 28500, "percentage": 100},
            {"item": "Footings and foundation", "value": 46118, "percentage": 100}
        ],
        "total_work_value": 113448,
        "contract_value": 820000,
        "cumulative_percentage": 23.8,
        "claim_amount": 113448,
        "gst": 11344.80,
        "total_claim": 124792.80,
        "less_previous_claims": 82000,
        "net_claim": 42792.80,
        "payment_status": "Paid",
        "payment_date": "2024-09-25"
    }
    progress_claims.append(claim2)

    for idx, claim in enumerate(progress_claims, 1):
        with open(folder / f"progress_claim_{idx:03d}.json", 'w') as f:
            json.dump(claim, f, indent=2)

def create_budget_tracking():
    """12_BUDGET_TRACKING"""
    folder = BASE_PATH / "12_BUDGET_TRACKING"

    budget = {
        "project_name": PROJECT_NAME,
        "contract_value": 820000,
        "contingency_percentage": 10,
        "contingency_amount": 82000,
        "total_project_budget": 902000,
        "as_of_date": "2024-10-01",
        "categories": [
            {
                "category": "Land Acquisition",
                "budgeted": 418215,
                "committed": 418215,
                "spent": 418215,
                "variance": 0,
                "status": "Complete"
            },
            {
                "category": "Design & Consultants",
                "budgeted": 75000,
                "committed": 73550,
                "spent": 73550,
                "variance": 1450,
                "status": "Complete"
            },
            {
                "category": "Permits & Approvals",
                "budgeted": 28000,
                "committed": 26950,
                "spent": 26950,
                "variance": 1050,
                "status": "Complete"
            },
            {
                "category": "Site Works",
                "budgeted": 73500,
                "committed": 67330,
                "spent": 67330,
                "variance": 6170,
                "status": "Complete"
            },
            {
                "category": "Foundations",
                "budgeted": 78000,
                "committed": 46118,
                "spent": 46118,
                "variance": 31882,
                "status": "Under Budget"
            },
            {
                "category": "Framing & Structure",
                "budgeted": 125000,
                "committed": 75680,
                "spent": 0,
                "variance": 49320,
                "status": "In Progress"
            },
            {
                "category": "Roofing",
                "budgeted": 52000,
                "committed": 0,
                "spent": 0,
                "variance": 52000,
                "status": "Not Started"
            },
            {
                "category": "External Cladding",
                "budgeted": 68000,
                "committed": 0,
                "spent": 0,
                "variance": 68000,
                "status": "Not Started"
            },
            {
                "category": "Windows & Doors",
                "budgeted": 85000,
                "committed": 0,
                "spent": 0,
                "variance": 85000,
                "status": "Not Started"
            },
            {
                "category": "Plumbing",
                "budgeted": 68000,
                "committed": 24618,
                "spent": 0,
                "variance": 43382,
                "status": "Materials Ordered"
            },
            {
                "category": "Electrical",
                "budgeted": 72000,
                "committed": 0,
                "spent": 0,
                "variance": 72000,
                "status": "Not Started"
            },
            {
                "category": "Insulation",
                "budgeted": 18000,
                "committed": 0,
                "spent": 0,
                "variance": 18000,
                "status": "Not Started"
            },
            {
                "category": "Plasterboard",
                "budgeted": 45000,
                "committed": 0,
                "spent": 0,
                "variance": 45000,
                "status": "Not Started"
            },
            {
                "category": "Tiling",
                "budgeted": 48000,
                "committed": 0,
                "spent": 0,
                "variance": 48000,
                "status": "Not Started"
            },
            {
                "category": "Kitchen",
                "budgeted": 55000,
                "committed": 0,
                "spent": 0,
                "variance": 55000,
                "status": "Not Started"
            },
            {
                "category": "Bathrooms",
                "budgeted": 48000,
                "committed": 0,
                "spent": 0,
                "variance": 48000,
                "status": "Not Started"
            },
            {
                "category": "Flooring",
                "budgeted": 42000,
                "committed": 0,
                "spent": 0,
                "variance": 42000,
                "status": "Not Started"
            },
            {
                "category": "Painting",
                "budgeted": 35000,
                "committed": 0,
                "spent": 0,
                "variance": 35000,
                "status": "Not Started"
            },
            {
                "category": "Cabinetry",
                "budgeted": 38000,
                "committed": 0,
                "spent": 0,
                "variance": 38000,
                "status": "Not Started"
            },
            {
                "category": "Fixtures & Fittings",
                "budgeted": 28000,
                "committed": 0,
                "spent": 0,
                "variance": 28000,
                "status": "Not Started"
            }
        ],
        "summary": {
            "total_budgeted": 902000,
            "total_committed": 732461,
            "total_spent": 632163,
            "remaining_budget": 269837,
            "budget_utilization_percent": 70.1,
            "project_completion_percent": 15
        }
    }

    with open(folder / "project_budget_tracker.json", 'w') as f:
        json.dump(budget, f, indent=2)

def create_schedule_timeline():
    """13_SCHEDULE_TIMELINE"""
    folder = BASE_PATH / "13_SCHEDULE_TIMELINE"

    schedule = {
        "project_name": PROJECT_NAME,
        "start_date": "2024-08-01",
        "original_completion": "2025-06-30",
        "revised_completion": "2025-06-30",
        "days_to_completion": 270,
        "current_status": "On Track",
        "phases": [
            {
                "phase": "Pre-Construction",
                "start": "2024-06-01",
                "end": "2024-08-14",
                "duration_days": 75,
                "status": "Complete",
                "completion_percent": 100,
                "tasks": [
                    {"task": "Land purchase", "duration": 15, "status": "Complete"},
                    {"task": "Design development", "duration": 30, "status": "Complete"},
                    {"task": "DA approval", "duration": 45, "status": "Complete"},
                    {"task": "Construction certificate", "duration": 14, "status": "Complete"}
                ]
            },
            {
                "phase": "Site Works & Foundations",
                "start": "2024-08-15",
                "end": "2024-09-30",
                "duration_days": 46,
                "status": "Complete",
                "completion_percent": 100,
                "tasks": [
                    {"task": "Site clearing", "duration": 5, "status": "Complete"},
                    {"task": "Bulk earthworks", "duration": 12, "status": "Complete"},
                    {"task": "Retaining walls", "duration": 15, "status": "Complete"},
                    {"task": "Footings & slab", "duration": 14, "status": "Complete"}
                ]
            },
            {
                "phase": "Frame & Structure",
                "start": "2024-10-01",
                "end": "2024-12-15",
                "duration_days": 76,
                "status": "In Progress",
                "completion_percent": 12,
                "tasks": [
                    {"task": "Ground floor frame", "duration": 20, "status": "In Progress"},
                    {"task": "Upper floor frame", "duration": 18, "status": "Not Started"},
                    {"task": "Roof structure", "duration": 15, "status": "Not Started"},
                    {"task": "Roof covering", "duration": 12, "status": "Not Started"},
                    {"task": "External cladding", "duration": 11, "status": "Not Started"}
                ]
            },
            {
                "phase": "Lock-up",
                "start": "2024-12-16",
                "end": "2025-02-28",
                "duration_days": 74,
                "status": "Not Started",
                "completion_percent": 0,
                "tasks": [
                    {"task": "Windows & doors", "duration": 10, "status": "Not Started"},
                    {"task": "Plumbing rough-in", "duration": 20, "status": "Not Started"},
                    {"task": "Electrical rough-in", "duration": 20, "status": "Not Started"},
                    {"task": "Insulation", "duration": 8, "status": "Not Started"},
                    {"task": "Plasterboard", "duration": 16, "status": "Not Started"}
                ]
            },
            {
                "phase": "Internal Fit-out",
                "start": "2025-03-01",
                "end": "2025-05-31",
                "duration_days": 92,
                "status": "Not Started",
                "completion_percent": 0,
                "tasks": [
                    {"task": "Tiling", "duration": 25, "status": "Not Started"},
                    {"task": "Kitchen installation", "duration": 15, "status": "Not Started"},
                    {"task": "Bathroom fit-out", "duration": 20, "status": "Not Started"},
                    {"task": "Painting", "duration": 18, "status": "Not Started"},
                    {"task": "Flooring", "duration": 14, "status": "Not Started"}
                ]
            },
            {
                "phase": "Final Completion",
                "start": "2025-06-01",
                "end": "2025-06-30",
                "duration_days": 30,
                "status": "Not Started",
                "completion_percent": 0,
                "tasks": [
                    {"task": "Final fix plumbing & electrical", "duration": 10, "status": "Not Started"},
                    {"task": "Final clean", "duration": 3, "status": "Not Started"},
                    {"task": "Landscaping", "duration": 12, "status": "Not Started"},
                    {"task": "Final inspection", "duration": 2, "status": "Not Started"},
                    {"task": "Handover", "duration": 3, "status": "Not Started"}
                ]
            }
        ]
    }

    with open(folder / "construction_schedule.json", 'w') as f:
        json.dump(schedule, f, indent=2)

def create_general_ledger():
    """17_GENERAL_LEDGER"""
    folder = BASE_PATH / "17_GENERAL_LEDGER"

    # Generate ledger entries
    transactions = []

    # Land purchase transactions
    transactions.append({
        "date": "2024-07-30",
        "reference": "LP-001",
        "description": "Land purchase - 789 Mountain View Terrace",
        "category": "Land Acquisition",
        "debit": 385000,
        "credit": 0,
        "balance": -385000,
        "payment_method": "Bank Transfer"
    })

    transactions.append({
        "date": "2024-07-30",
        "reference": "LP-002",
        "description": "Stamp duty on land purchase",
        "category": "Land Acquisition",
        "debit": 18465,
        "credit": 0,
        "balance": -403465,
        "payment_method": "Bank Transfer"
    })

    transactions.append({
        "date": "2024-07-30",
        "reference": "LP-003",
        "description": "Legal fees - conveyancing",
        "category": "Professional Fees",
        "debit": 3200,
        "credit": 0,
        "balance": -406665,
        "payment_method": "Bank Transfer"
    })

    # Construction loan drawdowns
    transactions.append({
        "date": "2024-07-30",
        "reference": "LOAN-001",
        "description": "Construction loan drawdown - Land",
        "category": "Financing",
        "debit": 0,
        "credit": 308000,
        "balance": -98665,
        "payment_method": "Loan Drawdown"
    })

    transactions.append({
        "date": "2024-09-01",
        "reference": "LOAN-002",
        "description": "Construction loan drawdown - Siteworks",
        "category": "Financing",
        "debit": 0,
        "credit": 85000,
        "balance": -13665,
        "payment_method": "Loan Drawdown"
    })

    # Client payments
    transactions.append({
        "date": "2024-08-05",
        "reference": "CP-001",
        "description": "Client payment - Deposit",
        "category": "Client Payments",
        "debit": 0,
        "credit": 90200,
        "balance": 76535,
        "payment_method": "Bank Transfer"
    })

    transactions.append({
        "date": "2024-09-25",
        "reference": "CP-002",
        "description": "Client payment - Progress Claim 2",
        "category": "Client Payments",
        "debit": 0,
        "credit": 42792.80,
        "balance": 119327.80,
        "payment_method": "Bank Transfer"
    })

    # Expenses
    transactions.append({
        "date": "2024-08-20",
        "reference": "INV-1001",
        "description": "Site preparation - Mountain Earthmoving",
        "category": "Site Works",
        "debit": 38830,
        "credit": 0,
        "balance": 80497.80,
        "payment_method": "Bank Transfer"
    })

    transactions.append({
        "date": "2024-09-05",
        "reference": "INV-2089",
        "description": "Concrete foundation - Blue Mountains Concrete",
        "category": "Foundations",
        "debit": 46117.50,
        "credit": 0,
        "balance": 34380.30,
        "payment_method": "Bank Transfer"
    })

    ledger = {
        "project_name": PROJECT_NAME,
        "as_of_date": "2024-10-01",
        "transactions": transactions,
        "summary": {
            "total_debits": 491612.50,
            "total_credits": 526992.80,
            "net_position": 34380.30,
            "transaction_count": len(transactions)
        }
    }

    with open(folder / "general_ledger.json", 'w') as f:
        json.dump(ledger, f, indent=2)

# Main execution
if __name__ == "__main__":
    print("🏗️ Generating comprehensive data for Mountain View Terrace project...")

    create_land_purchase_documents()
    print("✅ Created land purchase documents")

    create_permits_approvals()
    print("✅ Created permits and approvals")

    create_design_drawings()
    print("✅ Created design documents")

    create_finance_insurance()
    print("✅ Created finance and insurance documents")

    create_quotes_estimates()
    print("✅ Created quotes and estimates")

    create_purchase_orders_invoices()
    print("✅ Created purchase orders and invoices")

    create_subcontractors()
    print("✅ Created subcontractor records")

    create_labour_timesheets()
    print("✅ Created labour timesheets")

    create_client_billing()
    print("✅ Created client billing documents")

    create_budget_tracking()
    print("✅ Created budget tracking")

    create_schedule_timeline()
    print("✅ Created schedule and timeline")

    create_general_ledger()
    print("✅ Created general ledger")

    print("\n🎉 All data generated successfully!")
    print(f"Project: {PROJECT_NAME}")
    print(f"Contract Value: ${CONTRACT_VALUE:,}")
    print(f"Current Status: 15% Complete - Early Construction Phase")
