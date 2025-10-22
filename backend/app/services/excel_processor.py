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

            # Read Budget Summary sheet (headers at row 5, 0-indexed = 4)
            df = pd.read_excel(file_path, sheet_name="Budget Summary", header=4)

            # Clean up data
            df = df.dropna(how='all')  # Remove completely empty rows
            df = df[df['Cost Category'].notna()]  # Remove rows without category

            # Filter out total row
            df = df[df['Cost Category'] != 'TOTAL']

            budget_items = []
            for _, row in df.iterrows():
                try:
                    # Calculate % Complete from % Spent (which has formulas like =C6/B6)
                    budget = float(row['Budget Amount']) if pd.notna(row['Budget Amount']) else 0
                    actual = float(row['Actual Spent']) if pd.notna(row['Actual Spent']) else 0

                    # Calculate percent from actual data
                    percent_complete = 0
                    if budget > 0:
                        percent_complete = int((actual / budget) * 100)

                    budget_items.append({
                        "category": str(row['Cost Category']).strip(),
                        "description": str(row['Notes']) if pd.notna(row['Notes']) else "",
                        "budget": budget,
                        "actual_spent": actual,
                        "committed": 0,  # Not in new structure
                        "forecast": budget,  # Use budget as forecast
                        "variance": float(row['Variance']) if pd.notna(row['Variance']) else (budget - actual),
                        "percent_complete": percent_complete,
                        "notes": str(row['Status']) if pd.notna(row['Status']) else ""
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
            file_path = self.base_dir / "08_LABOUR_TIMESHEETS" / "Timesheets_September_2024.xlsx"

            if not file_path.exists():
                return {"error": "Timesheets file not found", "entries": []}

            # Read Site Supervisor sheet (header at row 4, 0-indexed)
            df_supervisor = pd.read_excel(file_path, sheet_name="Site Supervisor", header=4)
            df_supervisor = df_supervisor.dropna(how='all')

            # Read Labourers sheet (header at row 2, 0-indexed)
            df_labour = pd.read_excel(file_path, sheet_name="Labourers", header=2)
            df_labour = df_labour.dropna(how='all')

            timesheet_entries = []

            # Process supervisor entries
            for _, row in df_supervisor.iterrows():
                if pd.notna(row.get('Date')):
                    timesheet_entries.append({
                        "date": str(row['Date']),
                        "employee": "Tom Richards",  # From sheet title
                        "role": "Site Supervisor",
                        "hours": float(row['Hours']) if pd.notna(row.get('Hours')) else 0,
                        "rate": 75.0,  # From sheet title
                        "cost": float(row['Hours']) * 75.0 if pd.notna(row.get('Hours')) else 0,
                        "task": str(row['Notes']) if pd.notna(row.get('Notes')) else ""
                    })

            # Process labour entries
            for _, row in df_labour.iterrows():
                if pd.notna(row.get('Date')):
                    timesheet_entries.append({
                        "date": str(row['Date']),
                        "employee": str(row['Name']),
                        "role": "Labourer",
                        "hours": float(row['Hours']) if pd.notna(row.get('Hours')) else 0,
                        "rate": float(row['Rate']) if pd.notna(row.get('Rate')) else 0,
                        "cost": float(row['Amount']) if pd.notna(row.get('Amount')) else 0,
                        "task": str(row['Task']) if pd.notna(row.get('Task')) else ""
                    })

            print(f"✓ Timesheets: {len(timesheet_entries)} entries")
            return {"entries": timesheet_entries}

        except Exception as e:
            print(f"Error reading timesheets file: {e}")
            return {"error": str(e), "entries": []}

    def read_purchase_orders(self) -> Dict[str, Any]:
        """Read Purchase_Orders_Master.xlsx"""
        try:
            file_path = self.base_dir / "06_PURCHASE_ORDERS_INVOICES" / "Purchase_Orders_Master.xlsx"

            if not file_path.exists():
                return {"error": "Purchase orders file not found", "orders": []}

            # Read PO Register sheet
            df = pd.read_excel(file_path, sheet_name="PO Register", header=2)
            df = df.dropna(how='all')

            purchase_orders = []
            for _, row in df.iterrows():
                if pd.notna(row.get('PO#')):
                    amount = float(row['Amount']) if pd.notna(row.get('Amount')) else 0
                    gst = amount * 0.1  # Calculate 10% GST
                    total = amount + gst

                    purchase_orders.append({
                        "po_num": str(row['PO#']),
                        "date": str(row['Date']),
                        "supplier": str(row['Supplier']),
                        "description": str(row['Description']),
                        "category": "Materials",  # Default category
                        "amount": amount,
                        "gst": gst,
                        "total": total,
                        "invoice_received": str(row['Invoice Received']) if pd.notna(row.get('Invoice Received')) else "NO",
                        "paid": str(row['Status']) if pd.notna(row.get('Status')) else "PENDING",
                        "notes": str(row['Delivery Date']) if pd.notna(row.get('Delivery Date')) else ""
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
