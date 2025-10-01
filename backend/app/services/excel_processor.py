"""
Excel file processing service
Reads construction Excel files and extracts structured data
"""
import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Any


class ExcelProcessor:
    """Process construction project Excel files"""

    def __init__(self, project_id: str = "project-a-123-sunset-blvd"):
        # Go up 3 levels from backend/app/services/ to backend/projects/{project_id}/data
        self.project_id = project_id
        self.base_dir = Path(__file__).parent.parent.parent / "projects" / project_id / "data"
        print(f"Excel Processor initialized for project: {project_id}")
        print(f"Base dir: {self.base_dir}")

    def read_budget_file(self) -> Dict[str, Any]:
        """Read MASTER_PROJECT_BUDGET.xlsx and extract data"""
        try:
            file_path = self.base_dir / "12_BUDGET_TRACKING" / "MASTER_PROJECT_BUDGET.xlsx"

            if not file_path.exists():
                print(f"Budget file not found at: {file_path}")
                return {"error": "Budget file not found", "items": []}

            # Read Budget Summary sheet
            df = pd.read_excel(file_path, sheet_name="Budget Summary", header=3)

            # Clean up data
            df = df.dropna(how='all')  # Remove completely empty rows
            df = df[df['Category'].notna()]  # Remove rows without category

            # Filter out total row
            df = df[df['Category'] != 'TOTAL']

            budget_items = []
            for _, row in df.iterrows():
                try:
                    budget_items.append({
                        "category": str(row['Category']).strip(),
                        "description": str(row['Description']).strip(),
                        "budget": float(row['Budget']) if pd.notna(row['Budget']) else 0,
                        "actual_spent": float(row['Actual Spent']) if pd.notna(row['Actual Spent']) else 0,
                        "committed": float(row['Committed']) if pd.notna(row['Committed']) else 0,
                        "forecast": float(row['Forecast']) if pd.notna(row['Forecast']) else 0,
                        "variance": float(row['Variance']) if pd.notna(row['Variance']) else 0,
                        "percent_complete": int(row['% Complete']) if pd.notna(row['% Complete']) else 0,
                        "notes": str(row['Notes']) if pd.notna(row['Notes']) else ""
                    })
                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue

            print(f"✓ Budget file processed: {len(budget_items)} items")
            return {"items": budget_items}

        except Exception as e:
            print(f"Error reading budget file: {e}")
            return {"error": str(e), "items": []}

    def read_subcontractors(self) -> Dict[str, Any]:
        """Read Subcontractor_Register.xlsx"""
        try:
            file_path = self.base_dir / "07_SUBCONTRACTORS" / "Subcontractor_Register.xlsx"

            if not file_path.exists():
                return {"error": "Subcontractor file not found", "subcontractors": [], "payments": []}

            # Read Active Subbies sheet
            df_subbies = pd.read_excel(file_path, sheet_name="Active Subbies", header=2)
            df_subbies = df_subbies.dropna(how='all')

            subcontractors = []
            for _, row in df_subbies.iterrows():
                if pd.notna(row['ID']):
                    subcontractors.append({
                        "id": str(row['ID']),
                        "company_name": str(row['Company Name']),
                        "contact": str(row['Contact']),
                        "phone": str(row['Phone']),
                        "email": str(row['Email']) if pd.notna(row['Email']) else "",
                        "abn": str(row['ABN']),
                        "license": str(row['License']),
                        "insurance_expiry": str(row['Insurance Expiry']),
                        "contract_value": float(row['Contract Value']) if pd.notna(row['Contract Value']) else 0,
                        "status": str(row['Status'])
                    })

            # Read Payment Schedule sheet
            df_payments = pd.read_excel(file_path, sheet_name="Payment Schedule", header=2)
            df_payments = df_payments.dropna(how='all')

            payments = []
            for _, row in df_payments.iterrows():
                if pd.notna(row['Payment ID']):
                    payments.append({
                        "payment_id": str(row['Payment ID']),
                        "subcontractor": str(row['Subcontractor']),
                        "invoice_num": str(row['Invoice #']),
                        "description": str(row['Description']),
                        "amount": float(row['Amount']) if pd.notna(row['Amount']) else 0,
                        "gst": float(row['GST']) if pd.notna(row['GST']) else 0,
                        "total": float(row['Total']) if pd.notna(row['Total']) else 0,
                        "due_date": str(row['Due Date']),
                        "status": str(row['Status'])
                    })

            print(f"✓ Subcontractors: {len(subcontractors)}, Payments: {len(payments)}")
            return {"subcontractors": subcontractors, "payments": payments}

        except Exception as e:
            print(f"Error reading subcontractor file: {e}")
            return {"error": str(e), "subcontractors": [], "payments": []}

    def read_client_payments(self) -> Dict[str, Any]:
        """Read Client_Payment_Tracker.xlsx"""
        try:
            file_path = self.base_dir / "11_CLIENT_BILLING" / "Client_Payment_Tracker.xlsx"

            if not file_path.exists():
                return {"error": "Client payment file not found", "milestones": [], "variations": []}

            # Read Payment Schedule sheet
            df_milestones = pd.read_excel(file_path, sheet_name="Payment Schedule", header=2)
            df_milestones = df_milestones.dropna(how='all')

            milestones = []
            for _, row in df_milestones.iterrows():
                if pd.notna(row['Milestone']):
                    milestones.append({
                        "milestone": str(row['Milestone']),
                        "invoice_num": str(row['Invoice#']),
                        "description": str(row['Description']),
                        "amount": float(row['Amount']) if pd.notna(row['Amount']) else 0,
                        "due_date": str(row['Due Date']),
                        "paid_date": str(row['Paid Date']) if pd.notna(row['Paid Date']) else "",
                        "status": str(row['Status'])
                    })

            # Read Variations sheet
            df_variations = pd.read_excel(file_path, sheet_name="Variations", header=2)
            df_variations = df_variations.dropna(how='all')

            variations = []
            for _, row in df_variations.iterrows():
                if pd.notna(row['VO#']):
                    variations.append({
                        "vo_num": str(row['VO#']),
                        "date": str(row['Date']),
                        "description": str(row['Description']),
                        "cost": float(row['Cost']) if pd.notna(row['Cost']) else 0,
                        "client_price": float(row['Client Price']) if pd.notna(row['Client Price']) else 0,
                        "status": str(row['Status']),
                        "invoiced": str(row['Invoiced'])
                    })

            print(f"✓ Milestones: {len(milestones)}, Variations: {len(variations)}")
            return {"milestones": milestones, "variations": variations}

        except Exception as e:
            print(f"Error reading client payment file: {e}")
            return {"error": str(e), "milestones": [], "variations": []}

    def read_defects(self) -> Dict[str, Any]:
        """Read Defects_And_Snagging.xlsx"""
        try:
            file_path = self.base_dir / "15_DEFECTS_SNAGGING" / "Defects_And_Snagging.xlsx"

            if not file_path.exists():
                return {"error": "Defects file not found", "defects": []}

            df = pd.read_excel(file_path, sheet_name="Defects List", header=2)
            df = df.dropna(how='all')

            defects = []
            for _, row in df.iterrows():
                if pd.notna(row['ID']):
                    defects.append({
                        "id": str(row['ID']),
                        "location": str(row['Location']),
                        "trade": str(row['Trade']),
                        "description": str(row['Description']),
                        "severity": str(row['Severity']),
                        "reported_date": str(row['Reported Date']),
                        "due_date": str(row['Due Date']),
                        "status": str(row['Status']),
                        "notes": str(row['Notes']) if pd.notna(row['Notes']) else ""
                    })

            print(f"✓ Defects: {len(defects)}")
            return {"defects": defects}

        except Exception as e:
            print(f"Error reading defects file: {e}")
            return {"error": str(e), "defects": []}

    def read_timesheets(self) -> Dict[str, Any]:
        """Read Timesheets_September_2024.xlsx"""
        try:
            file_path = self.base_dir / "09_TIMESHEETS" / "Timesheets_September_2024.xlsx"

            if not file_path.exists():
                return {"error": "Timesheets file not found", "entries": []}

            # Read Site Supervisor sheet
            df_supervisor = pd.read_excel(file_path, sheet_name="Site Supervisor", header=2)
            df_supervisor = df_supervisor.dropna(how='all')

            # Read Labour Hours sheet
            df_labour = pd.read_excel(file_path, sheet_name="Labour Hours", header=2)
            df_labour = df_labour.dropna(how='all')

            timesheet_entries = []

            # Process supervisor entries
            for _, row in df_supervisor.iterrows():
                if pd.notna(row['Date']):
                    timesheet_entries.append({
                        "date": str(row['Date']),
                        "employee": str(row['Employee']),
                        "role": "Site Supervisor",
                        "hours": float(row['Hours']) if pd.notna(row['Hours']) else 0,
                        "rate": float(row['Rate']) if pd.notna(row['Rate']) else 0,
                        "cost": float(row['Cost']) if pd.notna(row['Cost']) else 0,
                        "task": str(row['Task']) if pd.notna(row['Task']) else ""
                    })

            # Process labour entries
            for _, row in df_labour.iterrows():
                if pd.notna(row['Date']):
                    timesheet_entries.append({
                        "date": str(row['Date']),
                        "employee": str(row['Worker']),
                        "role": str(row['Role']),
                        "hours": float(row['Hours']) if pd.notna(row['Hours']) else 0,
                        "rate": float(row['Rate']) if pd.notna(row['Rate']) else 0,
                        "cost": float(row['Cost']) if pd.notna(row['Cost']) else 0,
                        "task": str(row['Task']) if pd.notna(row['Task']) else ""
                    })

            print(f"✓ Timesheets: {len(timesheet_entries)} entries")
            return {"entries": timesheet_entries}

        except Exception as e:
            print(f"Error reading timesheets file: {e}")
            return {"error": str(e), "entries": []}

    def read_purchase_orders(self) -> Dict[str, Any]:
        """Read Purchase_Orders_Master.xlsx"""
        try:
            file_path = self.base_dir / "10_PURCHASE_ORDERS" / "Purchase_Orders_Master.xlsx"

            if not file_path.exists():
                return {"error": "Purchase orders file not found", "orders": []}

            # Read PO Register sheet
            df = pd.read_excel(file_path, sheet_name="PO Register", header=2)
            df = df.dropna(how='all')

            purchase_orders = []
            for _, row in df.iterrows():
                if pd.notna(row['PO#']):
                    purchase_orders.append({
                        "po_num": str(row['PO#']),
                        "date": str(row['Date']),
                        "supplier": str(row['Supplier']),
                        "description": str(row['Description']),
                        "category": str(row['Category']),
                        "amount": float(row['Amount']) if pd.notna(row['Amount']) else 0,
                        "gst": float(row['GST']) if pd.notna(row['GST']) else 0,
                        "total": float(row['Total']) if pd.notna(row['Total']) else 0,
                        "invoice_received": str(row['Invoice Received']),
                        "paid": str(row['Paid']),
                        "notes": str(row['Notes']) if pd.notna(row['Notes']) else ""
                    })

            print(f"✓ Purchase Orders: {len(purchase_orders)}")
            return {"orders": purchase_orders}

        except Exception as e:
            print(f"Error reading purchase orders file: {e}")
            return {"error": str(e), "orders": []}

    def check_files_exist(self) -> Dict[str, bool]:
        """Check which Excel files exist"""
        files = {
            "budget": (self.base_dir / "12_BUDGET_TRACKING" / "MASTER_PROJECT_BUDGET.xlsx").exists(),
            "subcontractors": (self.base_dir / "07_SUBCONTRACTORS" / "Subcontractor_Register.xlsx").exists(),
            "client_payments": (self.base_dir / "11_CLIENT_BILLING" / "Client_Payment_Tracker.xlsx").exists(),
            "defects": (self.base_dir / "15_DEFECTS_SNAGGING" / "Defects_And_Snagging.xlsx").exists(),
            "timesheets": (self.base_dir / "09_TIMESHEETS" / "Timesheets_September_2024.xlsx").exists(),
            "purchase_orders": (self.base_dir / "10_PURCHASE_ORDERS" / "Purchase_Orders_Master.xlsx").exists(),
        }
        return files
