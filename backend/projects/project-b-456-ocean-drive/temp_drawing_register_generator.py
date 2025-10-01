
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# --- Data for Architectural Drawings ---
arch_data = {
    'Drawing Number': [f'A-DA-1{i:02d}' for i in range(1, 16)],
    'Drawing Title': [
        'FLOOR PLAN - LEVEL 12 - DEMOLITION', 'FLOOR PLAN - LEVEL 12 - PROPOSED', 'REFLECTED CEILING PLAN',
        'FINISHES PLAN', 'FURNITURE PLAN', 'SECTIONS - SHEET 1', 'SECTIONS - SHEET 2',
        'ELEVATIONS - INTERNAL', 'RECEPTION DESK - DETAILS', 'KITCHEN JOINERY - DETAILS',
        'MEETING ROOM 1 & 2 - DETAILS', 'DOOR & WINDOW SCHEDULE', 'PARTITION TYPES',
        'FLOORING SETOUT', 'BRANDING & SIGNAGE'
    ],
    'Revision': np.random.choice(['A', 'B', 'C', 'D'], 15),
    'Date Issued': [datetime(2024, 7, 10) + timedelta(days=np.random.randint(0, 30)) for _ in range(15)],
    'Status': np.random.choice(['For Construction', 'For Information', 'Superseded', 'For Review'], 15),
    'Notes': ['' for _ in range(15)]
}
df_arch = pd.DataFrame(arch_data)
df_arch.loc[4, 'Status'] = '' # Missing data
df_arch.loc[8, 'Notes'] = 'Clash with structural beam - check'

# --- Data for Structural Drawings ---
struct_data = {
    'Drawing Number': [f'S-0{i}' for i in range(1, 6)],
    'Drawing Title': [
        'STRUCTURAL NOTES & SPECIFICATIONS', 'FLOOR PENETRATION DETAILS',
        'SUSPENDED SLAB SUPPORT DETAILS', 'CEILING SUPPORT FRAMEWORK', 'SERVER ROOM - SLAB STRENGTHENING'
    ],
    'Revision': np.random.choice(['A', 'B'], 5),
    'Date Issued': [datetime(2024, 7, 15) + timedelta(days=np.random.randint(0, 10)) for _ in range(5)],
    'Status': ['For Construction'] * 5,
    'Drawn By': ['J.Doe', 'J.Doe', 'A.Smith', 'A.Smith', 'J.Doe']
}
df_struct = pd.DataFrame(struct_data)

# --- Data for MEP Drawings ---
mep_data = {
    'Drawing Number': [
        'M-01', 'M-02', 'E-01', 'E-02', 'E-03', 'P-01', 'F-01'
    ],
    'Drawing Title': [
        'MECHANICAL - HVAC LAYOUT', 'MECHANICAL - DUCTWORK DETAILS', 'ELECTRICAL - LIGHTING & POWER',
        'ELECTRICAL - COMMS & DATA', 'ELECTRICAL - SINGLE LINE DIAGRAM', 'PLUMBING - FITOUT PLAN',
        'FIRE - SPRINKLER & DETECTOR LAYOUT'
    ],
    'Revision': ['C', 'B', 'D', 'C', 'B', 'A', 'C'],
    'Date Issued': [datetime(2024, 8, 1) + timedelta(days=i*5) for i in range(7)],
    'Status': ['For Construction'] * 7
}
df_mep = pd.DataFrame(mep_data)

# --- Create Excel File ---
file_path = "/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-b-456-ocean-drive/data/03_Design_and_Engineering/Drawing_Register.xlsx"
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df_arch.to_excel(writer, sheet_name='Architectural', index=False)
    df_struct.to_excel(writer, sheet_name='Structural', index=False)
    df_mep.to_excel(writer, sheet_name='MEP', index=False)

    # Add a messy notes sheet
    notes_sheet = writer.book.create_sheet("Coordination Notes")
    notes_sheet['A1'] = "Meeting 28/08/2024"
    notes_sheet['A2'] = "- HVAC unit clashes with ceiling grid in Zone 3. Mech consultant to review."
    notes_sheet['A3'] = "- Final colour for reception desk TBC by client."
    notes_sheet['C5'] = "OLD INFO: ~~Use 2-hour fire rated plasterboard~~"


print(f"Successfully created {file_path}")
