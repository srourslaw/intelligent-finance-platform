
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# --- Data for Sheet 1: Active Subbies ---
subbies_data = {
    'Trade': ['Demolition', 'Partitions & Ceilings', 'Flooring', 'Joinery', 'Mechanical (HVAC)', 'Electrical & Data', 'Hydraulics (Plumbing)', 'Fire Services', 'Painting', 'Glazing', 'Waterproofing', 'Security & Access Control', 'Blinds & Curtains', 'Signage', 'Final Clean'],
    'Company': ['Miami Demo Group', 'Drywall Solutions Inc.', 'Coastal Flooring Co.', 'Millwork Masters', 'ACME Mechanical', 'Spark Electrical Group', 'Hydro Plumbers LLC', 'FireSafe Systems', 'Pro Painters Miami', 'Glass & Glazing Co.', 'Aqua-Tite Waterproofing', 'SecureTech', 'Shade Solutions', 'Ocean Drive Signs', 'Sparkle Cleaners'],
    'Contact Person': ['Juan Perez', 'Mike Brown', 'Carlos Vega', 'David Chen', 'Robert Smith', 'Andrew Wilson', 'Luis Garcia', 'Frank Miller', 'Maria Rodriguez', 'Steven King', 'Paul Allen', 'Kevin Hart', 'Jessica Day', 'Tom Brand', 'Ana Lopez'],
    'Phone': ['305-555-0101', '(305) 555-0102', '305 555 0103', '3055550104', '305-555-0105', '', '(305) 555-0107', '305 555 0108', '3055550109', '305-555-0110', '305-555-0111', '305-555-0112', '305-555-0113', '305-555-0114', '305-555-0115'],
    'Email': ['juan@miamidemo.com', 'mike@drywallsolutions.com', 'carlos.v@coastalfloor.com', 'd.chen@millworkmasters.com', 'bob.s@acme-mech.com', 'awilson@sparkelectrical.com', 'lgarcia@hydroplumbers.net', 'frank.m@firesafe.com', 'maria@propainters.com', 'steven.k@ggc.com', 'paul.a@aquatite.com', 'kevin.h@securetech.com', 'jess.d@shadesolutions.com', 'tom.b@oceandrivesigns.com', 'ana.l@sparklecleaners.com'],
    'ABN': ['12345678901', '23 456 789 012', '34567890123', '45 678 901 234', '56789012345', '67 890 123 456', '78901234567', '89 012 345 678', '90123456789', '123 456 789 01', '234 567 890 12', '345 678 901 23', '456 789 012 34', '567 890 123 45', '678 901 234 56'],
    'Address': ['123 Industrial Rd, Miami', '456 Commerce St, Miami', '789 Trade Ave, Miami', '101 Factory Ln, Miami', '202 Engine Blvd, Miami', '303 Circuit Way, Miami', '404 Pipe Dr, Miami', '505 Safety Ct, Miami', '606 Color St, Miami', '707 Glass Rd, Miami', '808 Sealant Ave, Miami', '909 Lock St, Miami', '1010 Blind Rd, Miami', '1111 Sign St, Miami', '1212 Clean St, Miami'],
    'Contract Value': [48000, 180000, 95000, 220000, 155000, 255000, 75000, 62000, 55000, 35000, 18000, 22000, 16000, 8000, 12000],
    'Contract Date': [datetime(2024, 7, 18), datetime(2024, 7, 25), datetime(2024, 8, 1), datetime(2024, 8, 5), datetime(2024, 8, 10), datetime(2024, 8, 12), datetime(2024, 8, 15), datetime(2024, 8, 20), datetime(2024, 9, 1), datetime(2024, 9, 5), datetime(2024, 9, 10), datetime(2024, 9, 15), datetime(2024, 9, 20), datetime(2024, 10, 1), datetime(2024, 10, 5)],
    'Status': ['Complete', 'In Progress', 'Active', 'Active', 'In Progress', 'ACTIVE', 'In Progress', 'Active', 'Pending Start', 'Pending Start', 'Active', 'Active', 'Pending Start', 'Pending Start', 'Pending Start'],
    'Insurance Expiry': [datetime(2025, 7, 1), datetime(2024, 9, 1), datetime(2025, 8, 15), datetime(2025, 8, 20), datetime(2025, 8, 25), datetime(2025, 8, 28), datetime(2025, 9, 1), datetime(2025, 9, 5), datetime(2025, 9, 10), datetime(2025, 9, 15), datetime(2025, 9, 20), datetime(2025, 10, 1), datetime(2025, 10, 5), datetime(2025, 10, 10), datetime(2025, 10, 15)],
    'License #': [f'LIC-{np.random.randint(10000, 99999)}' for _ in range(15)],
    'Notes': ['', 'Insurance expired!', '', '', '', 'Phone number missing', '', '', '', '', '', '', '', '', '']
}
df_subbies = pd.DataFrame(subbies_data)

# --- Data for Sheet 2: Payment Schedule ---
payment_data = {
    'Subcontractor': np.random.choice(df_subbies['Company'], 45),
    'Invoice Date': [datetime(2024, 8, 1) + timedelta(days=np.random.randint(0, 60)) for _ in range(45)],
    'Invoice#': [f'INV-{np.random.randint(1000, 9999)}' for _ in range(45)],
    'Description': ['Progress Claim 1', 'Progress Claim 2', 'Deposit', 'Final Claim', 'Materials Deposit'] * 9,
    'Amount Ex GST': [np.random.uniform(5000, 50000) for _ in range(45)],
    'GST': [0]*45,
    'Total': [0]*45,
    'Due Date': [datetime(2024, 8, 31) + timedelta(days=np.random.randint(0, 60)) for _ in range(45)],
    'Paid Date': [d + timedelta(days=np.random.randint(-5, 5)) if np.random.rand() > 0.2 else None for d in [datetime(2024, 8, 31) + timedelta(days=np.random.randint(0, 60)) for _ in range(45)]],
    'Payment Method': np.random.choice(['EFT', 'Check', ''], 45),
    'Retention Held': [0]*45,
    'Notes': [''] * 45
}
df_payments = pd.DataFrame(payment_data)
df_payments['GST'] = df_payments['Amount Ex GST'] * 0.1
df_payments['Total'] = df_payments['Amount Ex GST'] + df_payments['GST']
df_payments['Retention Held'] = df_payments['Total'] * np.random.choice([0.05, 0.1], 45)
df_payments.loc[df_payments['Paid Date'].isnull(), 'Notes'] = 'OVERDUE'

# --- Data for Sheet 3: Contact Log ---
contact_data = {
    'Date': [datetime(2024, 7, 15) + timedelta(days=np.random.randint(0, 90)) for _ in range(35)],
    'Subcontractor': np.random.choice(df_subbies['Company'], 35),
    'Contact Type': np.random.choice(['Call', 'Email', 'Site Meeting'], 35),
    'Summary': ['Discussed schedule', 'Chased up invoice', 'Confirmed material delivery', 'Site instruction given', 'Safety toolbox talk'] * 7,
    'Action Required': ['Send updated drawings', 'Pay invoice', 'Confirm delivery time', 'Issue RFI', ''] * 7,
    'Closed?': np.random.choice(['Yes', 'No'], 35)
}
df_contacts = pd.DataFrame(contact_data)

# --- Create Excel File ---
file_path = "/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-b-456-ocean-drive/data/07_Subcontractors/Subcontractor_Register.xlsx"
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df_subbies.to_excel(writer, sheet_name='Active Subbies', index=False)
    df_payments.to_excel(writer, sheet_name='Payment Schedule', index=False)
    df_contacts.to_excel(writer, sheet_name='Contact Log', index=False)

    # --- Apply Messy Formatting ---
    workbook = writer.book
    subbies_sheet = writer.sheets['Active Subbies']
    from openpyxl.styles import PatternFill
    red_fill = PatternFill(start_color="FFFF0000", end_color="FFFF0000", fill_type="solid")
    subbies_sheet['K3'].fill = red_fill # Expired insurance

print(f"Successfully created {file_path}")
