import pandas as pd
from datetime import datetime, timedelta

# --- Data for Project Schedule ---
schedule_data = {
    'ID': range(1, 26),
    'Task Name': [
        'PROJECT START', 'Lease Finalized', 'Design Development', 'Permit Application', 'Permit Approval',
        'Subcontractor Tenders', 'Award Subcontracts', 'Site Mobilization', 'Demolition',
        'Framing & Partitions', 'HVAC Rough-in', 'Electrical Rough-in', 'Plumbing Rough-in',
        'Ceiling Grid Installation', 'Plasterboard & Finishing', 'Flooring Preparation',
        'Painting', 'Joinery Installation', 'HVAC Fit-off', 'Electrical Fit-off',
        'Plumbing Fit-off', 'Flooring Installation', 'Final Inspections', 'Defects Rectification',
        'PROJECT COMPLETE'
    ],
    'Duration (Days)': [
        0, 5, 30, 5, 20, 15, 10, 5, 10, 25, 15, 15, 10, 10, 20, 5, 15, 20, 10, 10, 5, 10, 5, 10, 0
    ],
    'Start Date': pd.to_datetime('2024-07-15'),
    'Finish Date': pd.to_datetime('2024-07-15'),
    'Predecessors': [
        '', '1', '2', '3', '4', '3', '6', '5,7', '8', '9', '10', '10', '10', '11,12,13', '14',
        '15', '15', '16', '17', '17', '17', '18', '22', '23', '24'
    ],
    'Status': ['Complete'] * 8 + ['In Progress'] * 5 + ['Not Started'] * 12,
    'Notes': ['' for _ in range(25)]
}
df_schedule = pd.DataFrame(schedule_data)

# Calculate start and finish dates based on duration and simple dependency (for realism)
for i in range(1, len(df_schedule)):
    pred_str = str(df_schedule.loc[i, 'Predecessors'])
    if pred_str:
        pred_ids = [int(p.strip()) for p in pred_str.split(',')]
        pred_finish_dates = [df_schedule.loc[p-1, 'Finish Date'] for p in pred_ids]
        start_date = max(pred_finish_dates) + timedelta(days=1)
        df_schedule.loc[i, 'Start Date'] = start_date
        # --- FIX: Convert numpy.int64 to standard int ---
        duration = int(df_schedule.loc[i, 'Duration (Days)'])
        df_schedule.loc[i, 'Finish Date'] = start_date + timedelta(days=duration - 1 if duration > 0 else 0)

df_schedule.loc[8, 'Notes'] = 'Asbestos discovery delayed completion by 3 days'
df_schedule.loc[10, 'Status'] = 'CRITICAL PATH'


# --- Create Excel File ---
file_path = "/Users/husseinsrour/Downloads/intelligent-finance-platform/backend/projects/project-b-456-ocean-drive/data/11_Project_Schedule/Project_Schedule.xlsx"
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df_schedule.to_excel(writer, sheet_name='Gantt View', index=False)

    # Add a messy notes sheet
    notes_sheet = writer.book.create_sheet("Schedule Notes")
    notes_sheet['A1'] = "Schedule Revision Log"
    notes_sheet['A2'] = "Rev A - 15/07/2024 - Baseline schedule"
    notes_sheet['A3'] = "Rev B - 28/07/2024 - Added 3 days to demo due to asbestos"
    notes_sheet['A4'] = "Rev C - 15/08/2024 - Client delay on joinery finish selection (2 day float used)"


print(f"Successfully created {file_path}")