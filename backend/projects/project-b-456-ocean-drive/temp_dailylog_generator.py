
import pandas as pd
from datetime import datetime, timedelta

# --- Data for Daily Logs ---
log_data = {
    'Date': [datetime(2024, 9, 1) + timedelta(days=i) for i in range(30)],
    'Weather': ['Sunny, 85F', 'Sunny, 88F', 'Cloudy, 82F', 'Rain, 78F', 'Sunny, 85F'] * 6,
    'Visitors': ['Architect', 'Client', 'Engineer', '', 'Building Inspector'] * 6,
    'Personnel On Site': [f'Coastal: 2, Drywall: 8, HVAC: 4, Elec: 5', f'Coastal: 2, Drywall: 8, HVAC: 4, Elec: 5', f'Coastal: 2, Drywall: 6, HVAC: 5, Elec: 6', f'COASTAL: 1, DRYWALL: 4', f'Coastal: 2, Drywall: 8, HVAC: 6, Elec: 6'] * 6,
    'Work Performed': [
        'Continued partition framing on north side. HVAC rough-in commenced in Zone 1. Electricians pulling cable.',
        'Completed framing. HVAC ductwork installation in Zones 1 & 2. Electrical rough-in ongoing.',
        'Ceiling grid installation started. HVAC team working on main plant connections.',
        'RAINED OFF - No work on site except safety checks.',
        'Ceiling grid continued. Building inspector reviewed framing - PASSED.'
    ] * 6,
    'Issues / Delays': ['', '', 'Wrong ceiling tiles delivered - returned.', 'Site closed due to weather.', ''] * 6
}
df_logs = pd.DataFrame(log_data)

# --- Create Excel File ---
file_path = "/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-b-456-ocean-drive/data/08_Site_Reports_and_Photos/Daily_Logs/Daily_Logs_September_2024.xlsx"
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df_logs.to_excel(writer, sheet_name='Sept 2024', index=False)

print(f"Successfully created {file_path}")
