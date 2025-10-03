import { useEffect, useRef, useState } from 'react';
import {
  Folder,
  FileSpreadsheet,
  FileText,
  Brain,
  Play,
  Pause,
  RotateCcw,
  ChevronRight,
  ChevronDown,
  FileImage,
  CheckCircle2,
  File
} from 'lucide-react';

interface Particle {
  id: number;
  x: number;
  y: number;
  targetX: number;
  targetY: number;
  progress: number;
  speed: number;
  layer: number;
  color: string;
  size: number;
  matrixCell?: number; // Track which matrix cell to light up
}

interface Neuron {
  x: number;
  y: number;
  activation: number;
  targetActivation: number;
  radius: number;
}

interface FileNode {
  name: string;
  type: 'folder' | 'excel' | 'pdf' | 'file' | 'json' | 'image' | 'csv' | 'md';
  path: string;
  children?: FileNode[];
  isExpanded?: boolean;
  yPosition?: number;
}

interface FinancialOutput {
  name: string;
  color: string;
  requiredFileTypes: string[];
  minFiles: number;
  isActive: boolean;
}

export function AIDataMappingAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [isAnimating, setIsAnimating] = useState(false);
  const [currentPhase, setCurrentPhase] = useState(0);
  const [currentFileIndex, setCurrentFileIndex] = useState(0);
  const [processedFiles, setProcessedFiles] = useState(new Set<string>());
  const particlesRef = useRef<Particle[]>([]);
  const neuronsRef = useRef<Neuron[][]>([]);
  const phaseTimerRef = useRef<number>(0);

  // Complete actual project directory structure with ALL 144 files
  const projectStructure: FileNode = {
    name: 'project-a-123-sunset-blvd',
    type: 'folder',
    path: '/',
    isExpanded: true,
    children: [
      {
        name: 'data',
        type: 'folder',
        path: '/data',
        isExpanded: true,
        children: [
          { name: 'project_a_comprehensive_data.json', type: 'json', path: '/data/project_a_comprehensive_data.json' },
          { name: 'README.md', type: 'md', path: '/data/README.md' },
          {
            name: '01_LAND_PURCHASE',
            type: 'folder',
            path: '/data/01_LAND_PURCHASE',
            isExpanded: true,
            children: [
              { name: 'Land_Contract_FINAL_v3.pdf', type: 'pdf', path: '/data/01_LAND_PURCHASE/Land_Contract_FINAL_v3.pdf' },
              { name: 'Land_Costs.xlsx', type: 'excel', path: '/data/01_LAND_PURCHASE/Land_Costs.xlsx' },
              { name: 'Land_Purchase_Contract_Signed.pdf', type: 'pdf', path: '/data/01_LAND_PURCHASE/Land_Purchase_Contract_Signed.pdf' },
              { name: 'Legal_Fees_Invoice_JohnsonSolicitors.pdf', type: 'pdf', path: '/data/01_LAND_PURCHASE/Legal_Fees_Invoice_JohnsonSolicitors.pdf' },
              { name: 'README.md', type: 'md', path: '/data/01_LAND_PURCHASE/README.md' },
              { name: 'Soil_Test_Report_GeoTech.pdf', type: 'pdf', path: '/data/01_LAND_PURCHASE/Soil_Test_Report_GeoTech.pdf' },
              { name: 'Stamp_Duty_Calculation.xlsx', type: 'excel', path: '/data/01_LAND_PURCHASE/Stamp_Duty_Calculation.xlsx' },
              { name: 'Survey_Report_Aug2024.pdf', type: 'pdf', path: '/data/01_LAND_PURCHASE/Survey_Report_Aug2024.pdf' },
              { name: 'Title_Deed_Scanned.pdf', type: 'pdf', path: '/data/01_LAND_PURCHASE/Title_Deed_Scanned.pdf' },
            ]
          },
          {
            name: '02_PERMITS_APPROVALS',
            type: 'folder',
            path: '/data/02_PERMITS_APPROVALS',
            isExpanded: true,
            children: [
              { name: 'Building_Permit_Application.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Building_Permit_Application.pdf' },
              { name: 'Building_Permit_APPROVED.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Building_Permit_APPROVED.pdf' },
              { name: 'Council_Fees_Receipt.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Council_Fees_Receipt.pdf' },
              { name: 'DA_Development_Application_Council.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/DA_Development_Application_Council.pdf' },
              { name: 'Development_Approval.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Development_Approval.pdf' },
              { name: 'Electrical_Certificate_of_Compliance.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Electrical_Certificate_of_Compliance.pdf' },
              { name: 'Electricity_Connection_Quote.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Electricity_Connection_Quote.pdf' },
              { name: 'Energy_Rating_Certificate.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Energy_Rating_Certificate.pdf' },
              { name: 'Occupancy_Certificate.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Occupancy_Certificate.pdf' },
              { name: 'Permits_Costs_Tracker.xlsx', type: 'excel', path: '/data/02_PERMITS_APPROVALS/Permits_Costs_Tracker.xlsx' },
              { name: 'Plumbing_Compliance_Certificate.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Plumbing_Compliance_Certificate.pdf' },
              { name: 'Water_Connection_Approval.pdf', type: 'pdf', path: '/data/02_PERMITS_APPROVALS/Water_Connection_Approval.pdf' },
            ]
          },
          {
            name: '03_DESIGN_DRAWINGS',
            type: 'folder',
            path: '/data/03_DESIGN_DRAWINGS',
            isExpanded: true,
            children: [
              {
                name: 'Architectural',
                type: 'folder',
                path: '/data/03_DESIGN_DRAWINGS/Architectural',
                isExpanded: true,
                children: [
                  { name: 'Architect_Invoice_1.pdf', type: 'pdf', path: '/data/03_DESIGN_DRAWINGS/Architectural/Architect_Invoice_1.pdf' },
                  { name: 'Architect_Invoice_2_REVISED.pdf', type: 'pdf', path: '/data/03_DESIGN_DRAWINGS/Architectural/Architect_Invoice_2_REVISED.pdf' },
                  { name: 'Architect_Invoice_2.pdf', type: 'pdf', path: '/data/03_DESIGN_DRAWINGS/Architectural/Architect_Invoice_2.pdf' },
                  { name: 'Design_Fees.xlsx', type: 'excel', path: '/data/03_DESIGN_DRAWINGS/Architectural/Design_Fees.xlsx' },
                  { name: 'HOUSE_A_PLANS_FINAL.pdf', type: 'pdf', path: '/data/03_DESIGN_DRAWINGS/Architectural/HOUSE_A_PLANS_FINAL.pdf' },
                  { name: 'HOUSE_A_PLANS_REV_A.pdf', type: 'pdf', path: '/data/03_DESIGN_DRAWINGS/Architectural/HOUSE_A_PLANS_REV_A.pdf' },
                  { name: 'HOUSE_A_PLANS_REV_B.pdf', type: 'pdf', path: '/data/03_DESIGN_DRAWINGS/Architectural/HOUSE_A_PLANS_REV_B.pdf' },
                ]
              },
              {
                name: 'Engineering',
                type: 'folder',
                path: '/data/03_DESIGN_DRAWINGS/Engineering',
                isExpanded: true,
                children: [
                  { name: 'engineering_costs.xlsx', type: 'excel', path: '/data/03_DESIGN_DRAWINGS/Engineering/engineering_costs.xlsx' },
                ]
              }
            ]
          },
          {
            name: '04_FINANCE_INSURANCE',
            type: 'folder',
            path: '/data/04_FINANCE_INSURANCE',
            isExpanded: true,
            children: [
              { name: 'Contract_Works_Insurance_Certificate.pdf', type: 'pdf', path: '/data/04_FINANCE_INSURANCE/Contract_Works_Insurance_Certificate.pdf' },
              { name: 'Financing_Costs_Summary.xlsx', type: 'excel', path: '/data/04_FINANCE_INSURANCE/Financing_Costs_Summary.xlsx' },
              { name: 'Interest_Calculations.xlsx', type: 'excel', path: '/data/04_FINANCE_INSURANCE/Interest_Calculations.xlsx' },
              { name: 'Loan_Agreement_Construction_Finance.pdf', type: 'pdf', path: '/data/04_FINANCE_INSURANCE/Loan_Agreement_Construction_Finance.pdf' },
              { name: 'Loan_Drawdown_Schedule.xlsx', type: 'excel', path: '/data/04_FINANCE_INSURANCE/Loan_Drawdown_Schedule.xlsx' },
              { name: 'Public_Liability_Insurance_Certificate.pdf', type: 'pdf', path: '/data/04_FINANCE_INSURANCE/Public_Liability_Insurance_Certificate.pdf' },
            ]
          },
          {
            name: '05_QUOTES_ESTIMATES',
            type: 'folder',
            path: '/data/05_QUOTES_ESTIMATES',
            isExpanded: true,
            children: [
              { name: 'Initial_Project_Budget_Estimate.xlsx', type: 'excel', path: '/data/05_QUOTES_ESTIMATES/Initial_Project_Budget_Estimate.xlsx' },
              { name: 'Quotes_Comparison.xlsx', type: 'excel', path: '/data/05_QUOTES_ESTIMATES/Quotes_Comparison.xlsx' },
            ]
          },
          {
            name: '06_PURCHASE_ORDERS_INVOICES',
            type: 'folder',
            path: '/data/06_PURCHASE_ORDERS_INVOICES',
            isExpanded: true,
            children: [
              { name: 'AP_Aging_Report.xlsx', type: 'excel', path: '/data/06_PURCHASE_ORDERS_INVOICES/AP_Aging_Report.xlsx' },
              { name: 'Materials_Purchases_Summary.xlsx', type: 'excel', path: '/data/06_PURCHASE_ORDERS_INVOICES/Materials_Purchases_Summary.xlsx' },
              { name: 'Purchase_Orders_Master.xlsx', type: 'excel', path: '/data/06_PURCHASE_ORDERS_INVOICES/Purchase_Orders_Master.xlsx' },
              { name: 'README.md', type: 'md', path: '/data/06_PURCHASE_ORDERS_INVOICES/README.md' },
              {
                name: 'Invoices_Paid',
                type: 'folder',
                path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid',
                isExpanded: true,
                children: [
                  { name: 'APS-2024-8912.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/APS-2024-8912.pdf' },
                  { name: 'BH-2024-0847.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/BH-2024-0847.pdf' },
                  { name: 'BR-PC-003.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/BR-PC-003.pdf' },
                  { name: 'Paid_Invoices_Register.xlsx', type: 'excel', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/Paid_Invoices_Register.xlsx' },
                  { name: 'PPS-8834.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/PPS-8834.pdf' },
                  { name: 'RM-2024-8845.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/RM-2024-8845.pdf' },
                  { name: 'SES-2024-3421.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/SES-2024-3421.pdf' },
                  { name: 'SF-PC-002.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/SF-PC-002.pdf' },
                  { name: 'Tax_Invoice_BM-1234.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/Tax_Invoice_BM-1234.pdf' },
                  { name: 'Tax_Invoice_PP-9012.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/Tax_Invoice_PP-9012.pdf' },
                  { name: 'Tax_Invoice_SE-5678.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/Tax_Invoice_SE-5678.pdf' },
                  { name: 'TB-PC-001.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/TB-PC-001.pdf' },
                  { name: 'TR-2024-156.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/TR-2024-156.pdf' },
                  { name: 'TSC-INV-4421.pdf', type: 'pdf', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/TSC-INV-4421.pdf' },
                ]
              },
              {
                name: 'Invoices_Pending',
                type: 'folder',
                path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Pending',
                isExpanded: true,
                children: [
                  { name: 'Pending_Invoices.xlsx', type: 'excel', path: '/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Pending/Pending_Invoices.xlsx' },
                ]
              }
            ]
          },
          {
            name: '07_SUBCONTRACTORS',
            type: 'folder',
            path: '/data/07_SUBCONTRACTORS',
            isExpanded: true,
            children: [
              { name: 'README.md', type: 'md', path: '/data/07_SUBCONTRACTORS/README.md' },
              { name: 'subcontractor_data.json', type: 'json', path: '/data/07_SUBCONTRACTORS/subcontractor_data.json' },
              { name: 'Subcontractor_Register.xlsx', type: 'excel', path: '/data/07_SUBCONTRACTORS/Subcontractor_Register.xlsx' },
              { name: 'SubcontractorPaymentTracker.xlsx', type: 'excel', path: '/data/07_SUBCONTRACTORS/SubcontractorPaymentTracker.xlsx' },
              {
                name: 'Subcontractor_Contracts',
                type: 'folder',
                path: '/data/07_SUBCONTRACTORS/Subcontractor_Contracts',
                isExpanded: true,
                children: [
                  { name: 'Contract_Electrician_SparkElectric.pdf', type: 'pdf', path: '/data/07_SUBCONTRACTORS/Subcontractor_Contracts/Contract_Electrician_SparkElectric.pdf' },
                  { name: 'Contract_Framer_BuildRight.pdf', type: 'pdf', path: '/data/07_SUBCONTRACTORS/Subcontractor_Contracts/Contract_Framer_BuildRight.pdf' },
                  { name: 'Contract_Plumber_AquaFlow.pdf', type: 'pdf', path: '/data/07_SUBCONTRACTORS/Subcontractor_Contracts/Contract_Plumber_AquaFlow.pdf' },
                ]
              }
            ]
          },
          {
            name: '08_LABOUR_TIMESHEETS',
            type: 'folder',
            path: '/data/08_LABOUR_TIMESHEETS',
            isExpanded: true,
            children: [
              { name: 'Employee_Wage_Rates.xlsx', type: 'excel', path: '/data/08_LABOUR_TIMESHEETS/Employee_Wage_Rates.xlsx' },
              { name: 'Labour_Costs_Summary.xlsx', type: 'excel', path: '/data/08_LABOUR_TIMESHEETS/Labour_Costs_Summary.xlsx' },
              { name: 'Site_Supervisor_Hours.xlsx', type: 'excel', path: '/data/08_LABOUR_TIMESHEETS/Site_Supervisor_Hours.xlsx' },
              { name: 'Timesheets_Aug_2024.xlsx', type: 'excel', path: '/data/08_LABOUR_TIMESHEETS/Timesheets_Aug_2024.xlsx' },
              { name: 'Timesheets_September_2024.xlsx', type: 'excel', path: '/data/08_LABOUR_TIMESHEETS/Timesheets_September_2024.xlsx' },
            ]
          },
          {
            name: '09_SITE_REPORTS_PHOTOS',
            type: 'folder',
            path: '/data/09_SITE_REPORTS_PHOTOS',
            isExpanded: true,
            children: [
              { name: 'Site_Diary_August.xlsx', type: 'excel', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Diary_August.xlsx' },
              { name: 'Site_Diary_September.xlsx', type: 'excel', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Diary_September.xlsx' },
              { name: 'Site_Meeting_Minutes_Sept15.pdf', type: 'pdf', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Meeting_Minutes_Sept15.pdf' },
              { name: 'Weather_Delays_Log.xlsx', type: 'excel', path: '/data/09_SITE_REPORTS_PHOTOS/Weather_Delays_Log.xlsx' },
              { name: 'Weekly_Progress_Report_Week_12.pdf', type: 'pdf', path: '/data/09_SITE_REPORTS_PHOTOS/Weekly_Progress_Report_Week_12.pdf' },
              {
                name: 'Site_Photos',
                type: 'folder',
                path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos',
                isExpanded: true,
                children: [
                  { name: '20240801_Site_Cleared.jpg', type: 'image', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos/20240801_Site_Cleared.jpg' },
                  { name: '20240815_Excavation_Complete.jpg', type: 'image', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos/20240815_Excavation_Complete.jpg' },
                  { name: '20240820_Footings_Poured.jpg', type: 'image', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos/20240820_Footings_Poured.jpg' },
                  { name: '20240825_Slab_Down.jpg', type: 'image', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos/20240825_Slab_Down.jpg' },
                  { name: '20240905_Frame_Started.jpg', type: 'image', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos/20240905_Frame_Started.jpg' },
                  { name: '20240920_Frame_Complete.jpg', type: 'image', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos/20240920_Frame_Complete.jpg' },
                  { name: '20241001_Roof_On.jpg', type: 'image', path: '/data/09_SITE_REPORTS_PHOTOS/Site_Photos/20241001_Roof_On.jpg' },
                ]
              }
            ]
          },
          {
            name: '10_VARIATIONS_CHANGES',
            type: 'folder',
            path: '/data/10_VARIATIONS_CHANGES',
            isExpanded: true,
            children: [
              { name: 'Variation_Order_Register.xlsx', type: 'excel', path: '/data/10_VARIATIONS_CHANGES/Variation_Order_Register.xlsx' },
              { name: 'VO_Impact_on_Budget.xlsx', type: 'excel', path: '/data/10_VARIATIONS_CHANGES/VO_Impact_on_Budget.xlsx' },
            ]
          },
          {
            name: '11_CLIENT_BILLING',
            type: 'folder',
            path: '/data/11_CLIENT_BILLING',
            isExpanded: true,
            children: [
              { name: 'AR_Aging_Report.xlsx', type: 'excel', path: '/data/11_CLIENT_BILLING/AR_Aging_Report.xlsx' },
              { name: 'Client_Payment_Tracker.xlsx', type: 'excel', path: '/data/11_CLIENT_BILLING/Client_Payment_Tracker.xlsx' },
              { name: 'Outstanding_Client_Invoices.xlsx', type: 'excel', path: '/data/11_CLIENT_BILLING/Outstanding_Client_Invoices.xlsx' },
              { name: 'Payment_Schedule.xlsx', type: 'excel', path: '/data/11_CLIENT_BILLING/Payment_Schedule.xlsx' },
              { name: 'README.md', type: 'md', path: '/data/11_CLIENT_BILLING/README.md' },
              { name: 'Revenue_Recognition_Schedule.xlsx', type: 'excel', path: '/data/11_CLIENT_BILLING/Revenue_Recognition_Schedule.xlsx' },
            ]
          },
          {
            name: '12_BUDGET_TRACKING',
            type: 'folder',
            path: '/data/12_BUDGET_TRACKING',
            isExpanded: true,
            children: [
              { name: 'Budget_vs_Actual.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Budget_vs_Actual.xlsx' },
              { name: 'Cashflow_Actual.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Cashflow_Actual.xlsx' },
              { name: 'Cashflow_Forecast.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Cashflow_Forecast.xlsx' },
              { name: 'Cost_Breakdown_by_Phase.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Cost_Breakdown_by_Phase.xlsx' },
              { name: 'MASTER_PROJECT_BUDGET_Sheet1_Budget_Summary.csv', type: 'csv', path: '/data/12_BUDGET_TRACKING/MASTER_PROJECT_BUDGET_Sheet1_Budget_Summary.csv' },
              { name: 'MASTER_PROJECT_BUDGET.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/MASTER_PROJECT_BUDGET.xlsx' },
              { name: 'Monthly_Financial_Summary_Aug.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Monthly_Financial_Summary_Aug.xlsx' },
              { name: 'Monthly_Financial_Summary_Sept.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Monthly_Financial_Summary_Sept.xlsx' },
              { name: 'Profit_Margin_Calculation.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Profit_Margin_Calculation.xlsx' },
              { name: 'Project_A_123_Sunset_Boulevard_Budget.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Project_A_123_Sunset_Boulevard_Budget.xlsx' },
              { name: 'project_budget_data.json', type: 'json', path: '/data/12_BUDGET_TRACKING/project_budget_data.json' },
              { name: 'Project_Budget_v1.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Project_Budget_v1.xlsx' },
              { name: 'Project_Budget_v2_updated.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Project_Budget_v2_updated.xlsx' },
              { name: 'README.md', type: 'md', path: '/data/12_BUDGET_TRACKING/README.md' },
              { name: 'Weekly_Cost_Report.xlsx', type: 'excel', path: '/data/12_BUDGET_TRACKING/Weekly_Cost_Report.xlsx' },
            ]
          },
          {
            name: '13_SCHEDULE_TIMELINE',
            type: 'folder',
            path: '/data/13_SCHEDULE_TIMELINE',
            isExpanded: true,
            children: [
              { name: 'Critical_Path_Analysis.xlsx', type: 'excel', path: '/data/13_SCHEDULE_TIMELINE/Critical_Path_Analysis.xlsx' },
              { name: 'Delays_Log.xlsx', type: 'excel', path: '/data/13_SCHEDULE_TIMELINE/Delays_Log.xlsx' },
              { name: 'Milestone_Tracker.xlsx', type: 'excel', path: '/data/13_SCHEDULE_TIMELINE/Milestone_Tracker.xlsx' },
              { name: 'Project_Schedule_Gantt.xlsx', type: 'excel', path: '/data/13_SCHEDULE_TIMELINE/Project_Schedule_Gantt.xlsx' },
            ]
          },
          {
            name: '14_COMPLIANCE_CERTIFICATES',
            type: 'folder',
            path: '/data/14_COMPLIANCE_CERTIFICATES',
            isExpanded: true,
            children: [
              { name: 'Compliance_Checklist.xlsx', type: 'excel', path: '/data/14_COMPLIANCE_CERTIFICATES/Compliance_Checklist.xlsx' },
            ]
          },
          {
            name: '15_DEFECTS_SNAGGING',
            type: 'folder',
            path: '/data/15_DEFECTS_SNAGGING',
            isExpanded: true,
            children: [
              { name: 'Defect_Rectification_Log.xlsx', type: 'excel', path: '/data/15_DEFECTS_SNAGGING/Defect_Rectification_Log.xlsx' },
              { name: 'Defects_And_Snagging.xlsx', type: 'excel', path: '/data/15_DEFECTS_SNAGGING/Defects_And_Snagging.xlsx' },
              { name: 'Snagging_Items.xlsx', type: 'excel', path: '/data/15_DEFECTS_SNAGGING/Snagging_Items.xlsx' },
              {
                name: 'Defect_Photos',
                type: 'folder',
                path: '/data/15_DEFECTS_SNAGGING/Defect_Photos',
                isExpanded: true,
                children: [
                  { name: 'Defect_01_Paint_Touch_Up.jpg', type: 'image', path: '/data/15_DEFECTS_SNAGGING/Defect_Photos/Defect_01_Paint_Touch_Up.jpg' },
                  { name: 'Defect_02_Door_Alignment.jpg', type: 'image', path: '/data/15_DEFECTS_SNAGGING/Defect_Photos/Defect_02_Door_Alignment.jpg' },
                  { name: 'Defect_03_Tile_Crack.jpg', type: 'image', path: '/data/15_DEFECTS_SNAGGING/Defect_Photos/Defect_03_Tile_Crack.jpg' },
                ]
              }
            ]
          },
          {
            name: '16_HANDOVER',
            type: 'folder',
            path: '/data/16_HANDOVER',
            isExpanded: true,
            children: [
              { name: 'Handover_Checklist.xlsx', type: 'excel', path: '/data/16_HANDOVER/Handover_Checklist.xlsx' },
              { name: 'Keys_Register.xlsx', type: 'excel', path: '/data/16_HANDOVER/Keys_Register.xlsx' },
            ]
          },
          {
            name: '17_GENERAL_LEDGER',
            type: 'folder',
            path: '/data/17_GENERAL_LEDGER',
            isExpanded: true,
            children: [
              { name: 'Chart_of_Accounts.xlsx', type: 'excel', path: '/data/17_GENERAL_LEDGER/Chart_of_Accounts.xlsx' },
              { name: 'Opening_Balances_June_2024.xlsx', type: 'excel', path: '/data/17_GENERAL_LEDGER/Opening_Balances_June_2024.xlsx' },
              { name: 'Trial_Balance_Monthly.xlsx', type: 'excel', path: '/data/17_GENERAL_LEDGER/Trial_Balance_Monthly.xlsx' },
            ]
          },
          {
            name: '18_MISC_RANDOM',
            type: 'folder',
            path: '/data/18_MISC_RANDOM',
            isExpanded: true,
            children: [
              { name: 'Old_Version_Budget_DELETE.xlsx', type: 'excel', path: '/data/18_MISC_RANDOM/Old_Version_Budget_DELETE.xlsx' },
              { name: 'Phone_Numbers_Contacts.xlsx', type: 'excel', path: '/data/18_MISC_RANDOM/Phone_Numbers_Contacts.xlsx' },
              { name: 'Todo_List.xlsx', type: 'excel', path: '/data/18_MISC_RANDOM/Todo_List.xlsx' },
            ]
          },
          {
            name: '19_MONTHLY_CLOSE',
            type: 'folder',
            path: '/data/19_MONTHLY_CLOSE',
            isExpanded: true,
            children: [
              {
                name: '2024-06-Close',
                type: 'folder',
                path: '/data/19_MONTHLY_CLOSE/2024-06-Close',
                isExpanded: true,
                children: [
                  { name: 'Balance_Sheet_June_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-06-Close/Balance_Sheet_June_2024.xlsx' },
                  { name: 'Cash_Flow_Statement_June_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-06-Close/Cash_Flow_Statement_June_2024.xlsx' },
                  { name: 'Income_Statement_June_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-06-Close/Income_Statement_June_2024.xlsx' },
                ]
              },
              {
                name: '2024-07-Close',
                type: 'folder',
                path: '/data/19_MONTHLY_CLOSE/2024-07-Close',
                isExpanded: true,
                children: [
                  { name: 'Balance_Sheet_July_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-07-Close/Balance_Sheet_July_2024.xlsx' },
                  { name: 'Cash_Flow_Statement_July_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-07-Close/Cash_Flow_Statement_July_2024.xlsx' },
                  { name: 'Income_Statement_July_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-07-Close/Income_Statement_July_2024.xlsx' },
                ]
              },
              {
                name: '2024-08-Close',
                type: 'folder',
                path: '/data/19_MONTHLY_CLOSE/2024-08-Close',
                isExpanded: true,
                children: [
                  { name: 'Balance_Sheet_August_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-08-Close/Balance_Sheet_August_2024.xlsx' },
                  { name: 'Cash_Flow_Statement_August_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-08-Close/Cash_Flow_Statement_August_2024.xlsx' },
                  { name: 'Income_Statement_August_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-08-Close/Income_Statement_August_2024.xlsx' },
                ]
              },
              {
                name: '2024-09-Close',
                type: 'folder',
                path: '/data/19_MONTHLY_CLOSE/2024-09-Close',
                isExpanded: true,
                children: [
                  { name: 'Balance_Sheet_September_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-09-Close/Balance_Sheet_September_2024.xlsx' },
                  { name: 'Cash_Flow_Statement_September_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-09-Close/Cash_Flow_Statement_September_2024.xlsx' },
                  { name: 'Income_Statement_September_2024.xlsx', type: 'excel', path: '/data/19_MONTHLY_CLOSE/2024-09-Close/Income_Statement_September_2024.xlsx' },
                ]
              }
            ]
          },
          {
            name: '20_BANK_RECONCILIATION',
            type: 'folder',
            path: '/data/20_BANK_RECONCILIATION',
            isExpanded: true,
            children: [
              { name: 'Bank_Reconciliation_Monthly.xlsx', type: 'excel', path: '/data/20_BANK_RECONCILIATION/Bank_Reconciliation_Monthly.xlsx' },
              {
                name: 'Bank_Statements',
                type: 'folder',
                path: '/data/20_BANK_RECONCILIATION/Bank_Statements',
                isExpanded: true,
                children: [
                  { name: 'Bank_Statement_June_2024.pdf', type: 'pdf', path: '/data/20_BANK_RECONCILIATION/Bank_Statements/Bank_Statement_June_2024.pdf' },
                  { name: 'Bank_Statement_July_2024.pdf', type: 'pdf', path: '/data/20_BANK_RECONCILIATION/Bank_Statements/Bank_Statement_July_2024.pdf' },
                  { name: 'Bank_Statement_August_2024.pdf', type: 'pdf', path: '/data/20_BANK_RECONCILIATION/Bank_Statements/Bank_Statement_August_2024.pdf' },
                  { name: 'Bank_Statement_September_2024.pdf', type: 'pdf', path: '/data/20_BANK_RECONCILIATION/Bank_Statements/Bank_Statement_September_2024.pdf' },
                ]
              }
            ]
          },
          {
            name: '21_FIXED_ASSETS',
            type: 'folder',
            path: '/data/21_FIXED_ASSETS',
            isExpanded: true,
            children: [
              { name: 'Fixed_Assets_Register.xlsx', type: 'excel', path: '/data/21_FIXED_ASSETS/Fixed_Assets_Register.xlsx' },
            ]
          }
        ]
      }
    ]
  };

  // Flatten the tree to get all processable files (exclude folders and .DS_Store)
  const getAllFiles = (node: FileNode, depth: number = 0): Array<FileNode & { depth: number }> => {
    let files: Array<FileNode & { depth: number }> = [];

    if (node.type !== 'folder' && !node.name.startsWith('.')) {
      files.push({ ...node, depth });
    }

    if (node.children) {
      node.children.forEach(child => {
        files = files.concat(getAllFiles(child, depth + 1));
      });
    }

    return files;
  };

  const allFiles = getAllFiles(projectStructure);

  // Financial outputs with intelligent activation logic
  const [outputs, setOutputs] = useState<FinancialOutput[]>([
    {
      name: 'Balance Sheet',
      color: '#6366F1',
      requiredFileTypes: ['excel', 'csv'],
      minFiles: 5,
      isActive: false
    },
    {
      name: 'Income Statement',
      color: '#8B5CF6',
      requiredFileTypes: ['excel', 'csv'],
      minFiles: 5,
      isActive: false
    },
    {
      name: 'Cash Flow Statement',
      color: '#EC4899',
      requiredFileTypes: ['excel', 'csv'],
      minFiles: 5,
      isActive: false
    },
    {
      name: 'Equity Statement',
      color: '#F59E0B',
      requiredFileTypes: ['excel', 'csv'],
      minFiles: 3,
      isActive: false
    },
    {
      name: 'Ratios Dashboard',
      color: '#10B981',
      requiredFileTypes: ['excel', 'csv'],
      minFiles: 8,
      isActive: false
    },
    {
      name: 'Assumptions',
      color: '#3B82F6',
      requiredFileTypes: ['excel', 'pdf', 'csv'],
      minFiles: 10,
      isActive: false
    },
    {
      name: 'Instructions',
      color: '#6B7280',
      requiredFileTypes: ['pdf', 'md'],
      minFiles: 2,
      isActive: false
    },
  ]);

  // Neural network layers configuration (4 layers + matrix in center)
  const layerConfig = [
    { name: 'INPUT LAYER', neurons: 12, color: '#3B82F6' }, // Blue-500
    { name: 'PROCESSING LAYER', neurons: 12, color: '#EF4444' }, // Red-500
    { name: 'OUTPUT LAYER', neurons: 12, color: '#8B5CF6' }, // Violet-500
    { name: 'MAPPING LAYER', neurons: 12, color: '#10B981' }, // Emerald-500
  ];

  const matrixSize = 10; // 10x10 attention matrix
  const [matrixCells, setMatrixCells] = useState<Set<number>>(new Set());
  const outputHubRef = useRef<{ x: number; y: number; activation: number }>({ x: 0, y: 0, activation: 0 });
  const matrixAnimationRef = useRef<Set<number>>(new Set());

  const initializeNeurons = (width: number, height: number) => {
    const layers: Neuron[][] = [];
    const networkStartX = 280;
    const networkEndX = width - 280;
    const networkWidth = networkEndX - networkStartX;

    // Layer positions: Layer1, Layer2, [MATRIX SPACE], Layer3, Layer4
    const matrixWidth = 220; // Space for 10x10 matrix
    const layerSpacing = (networkWidth - matrixWidth) / 3; // 3 gaps between 4 layers

    const layerPositions = [
      networkStartX,                           // Layer 1
      networkStartX + layerSpacing,            // Layer 2
      networkStartX + layerSpacing * 2 + matrixWidth, // Layer 3 (after matrix)
      networkStartX + layerSpacing * 3 + matrixWidth, // Layer 4
    ];

    layerConfig.forEach((config, layerIdx) => {
      const neurons: Neuron[] = [];
      const layerX = layerPositions[layerIdx];
      const neuronSpacing = (height * 0.7) / (config.neurons + 1);
      const startY = height * 0.15;

      for (let i = 0; i < config.neurons; i++) {
        neurons.push({
          x: layerX,
          y: startY + (i + 1) * neuronSpacing,
          activation: 0,
          targetActivation: 0,
          radius: 6, // Smaller cleaner neurons
        });
      }
      layers.push(neurons);
    });

    neuronsRef.current = layers;

    // Initialize output hub position (between Layer 4 and outputs)
    const layer4X = layerPositions[3];
    const outputStartX = width * 0.88;
    outputHubRef.current = {
      x: (layer4X + outputStartX) / 2,
      y: height / 2,
      activation: 0
    };
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'folder': return Folder;
      case 'excel': return FileSpreadsheet;
      case 'pdf': return FileText;
      case 'image': return FileImage;
      case 'json': return File;
      case 'csv': return FileSpreadsheet;
      case 'md': return FileText;
      default: return File;
    }
  };

  const getFileColor = (type: string) => {
    switch (type) {
      case 'excel': return '#10B981';
      case 'pdf': return '#EF4444';
      case 'csv': return '#06B6D4';
      case 'json': return '#F59E0B';
      case 'image': return '#8B5CF6';
      case 'md': return '#6B7280';
      default: return '#6B7280';
    }
  };

  // Update outputs based on processed files
  const updateOutputs = (processedSet: Set<string>) => {
    const processedFilesArray = Array.from(processedSet).map(path =>
      allFiles.find(f => f.path === path)
    ).filter(Boolean);

    setOutputs(prev => prev.map(output => {
      const relevantFiles = processedFilesArray.filter(file =>
        file && output.requiredFileTypes.includes(file.type)
      );

      const shouldActivate = relevantFiles.length >= output.minFiles;

      return {
        ...output,
        isActive: shouldActivate
      };
    }));
  };

  const createParticles = (width: number, height: number, phase: number, fileIndex: number) => {
    const particles: Particle[] = [];

    if (phase === 0 && fileIndex < allFiles.length) {
      // Phase 0: Current file to first layer (Document Parsing)
      const file = allFiles[fileIndex];
      const fileY = file.yPosition || height * 0.5;
      const sourceX = 190; // Match the connection line source
      const targetNeurons = neuronsRef.current[0];
      const fileColor = getFileColor(file.type);

      // Use consistent neuron mapping (same as connection lines)
      const neuronIdx1 = fileIndex % targetNeurons.length;
      const neuronIdx2 = (fileIndex + 1) % targetNeurons.length;

      [neuronIdx1, neuronIdx2].forEach(idx => {
        const neuron = targetNeurons[idx];
        if (neuron) {
          particles.push({
            id: particles.length,
            x: sourceX,
            y: fileY,
            targetX: neuron.x,
            targetY: neuron.y,
            progress: 0,
            speed: 0.025, // Fast continuous speed (matching HTML)
            layer: 0,
            color: fileColor,
            size: 3 + Math.random() * 1.5,
          });
        }
      });
    } else if (phase === 1) {
      // Phase 1: Layer 1 to Layer 2
      const fromLayer = neuronsRef.current[0];
      const toLayer = neuronsRef.current[1];

      fromLayer.forEach((fromNeuron, fromIdx) => {
        const toIdx = (fromIdx + 1) % toLayer.length;
        const toNeuron = toLayer[toIdx];
        particles.push({
          id: particles.length,
          x: fromNeuron.x,
          y: fromNeuron.y,
          targetX: toNeuron.x,
          targetY: toNeuron.y,
          progress: 0,
          speed: 0.025, // Fast continuous speed
          layer: 1,
          color: '#EF4444',
          size: 3 + Math.random() * 1,
        });
      });
    } else if (phase === 2) {
      // Phase 2: Layer 2 to Matrix (activate 5 random matrix cells - matching HTML example)
      const fromLayer = neuronsRef.current[1];
      const layer2 = neuronsRef.current[1];
      const layer3 = neuronsRef.current[2];

      // Calculate matrix position
      const matrixCenterX = (layer2[0].x + layer3[0].x) / 2;
      const matrixCenterY = height / 2;
      const cellSize = 20; // Match HTML example (20px)
      const gap = 3;
      const totalSize = matrixSize * (cellSize + gap) - gap;
      const matrixStartX = matrixCenterX - totalSize / 2;
      const matrixStartY = matrixCenterY - totalSize / 2;

      // Activate 5 random matrix cells (matching HTML example)
      const cellsToActivate = new Set(matrixCells);
      const newActivatedCells: number[] = [];
      for (let i = 0; i < 5; i++) {
        const cellIdx = Math.floor(Math.random() * (matrixSize * matrixSize));
        cellsToActivate.add(cellIdx);
        newActivatedCells.push(cellIdx);
      }
      setMatrixCells(cellsToActivate);

      // Create particles to each activated cell (not just matrix center)
      newActivatedCells.forEach(cellIdx => {
        const col = cellIdx % matrixSize;
        const row = Math.floor(cellIdx / matrixSize);
        const cellX = matrixStartX + col * (cellSize + gap) + cellSize / 2;
        const cellY = matrixStartY + row * (cellSize + gap) + cellSize / 2;

        // Pick a random neuron from Layer 2 to create particle from
        const randomNeuron = fromLayer[Math.floor(Math.random() * fromLayer.length)];
        particles.push({
          id: particles.length,
          x: randomNeuron.x,
          y: randomNeuron.y,
          targetX: cellX,
          targetY: cellY,
          progress: 0,
          speed: 0.025, // Fast continuous speed
          layer: 2,
          color: '#A78BFA',
          size: 3 + Math.random() * 1,
        });
      });
    } else if (phase === 3) {
      // Phase 3: Matrix to Layer 3
      const toLayer = neuronsRef.current[2];
      const layer2 = neuronsRef.current[1];
      const matrixCenterX = (layer2[0].x + neuronsRef.current[2][0].x) / 2;
      const matrixCenterY = height / 2;

      toLayer.forEach((toNeuron) => {
        particles.push({
          id: particles.length,
          x: matrixCenterX,
          y: matrixCenterY,
          targetX: toNeuron.x,
          targetY: toNeuron.y,
          progress: 0,
          speed: 0.025, // Fast continuous speed
          layer: 3,
          color: '#8B5CF6',
          size: 3 + Math.random() * 1,
        });
      });
    } else if (phase === 4) {
      // Phase 4: Layer 3 to Layer 4
      const fromLayer = neuronsRef.current[2];
      const toLayer = neuronsRef.current[3];

      fromLayer.forEach((fromNeuron, fromIdx) => {
        const toIdx = (fromIdx + 1) % toLayer.length;
        const toNeuron = toLayer[toIdx];
        particles.push({
          id: particles.length,
          x: fromNeuron.x,
          y: fromNeuron.y,
          targetX: toNeuron.x,
          targetY: toNeuron.y,
          progress: 0,
          speed: 0.025, // Fast continuous speed
          layer: 4,
          color: '#10B981',
          size: 3 + Math.random() * 1,
        });
      });
    } else if (phase === 5) {
      // Phase 5: Layer 4 to Output Hub
      const lastLayer = neuronsRef.current[3]; // Layer 4 is index 3
      const hub = outputHubRef.current;

      lastLayer.forEach((neuron) => {
        particles.push({
          id: particles.length,
          x: neuron.x,
          y: neuron.y,
          targetX: hub.x,
          targetY: hub.y,
          progress: 0,
          speed: 0.025, // Fast continuous speed
          layer: 5,
          color: '#10B981',
          size: 3 + Math.random() * 1,
        });
      });
    } else if (phase === 6) {
      // Phase 6: Output Hub to Financial Outputs
      const hub = outputHubRef.current;
      const targetX = width * 0.88;

      outputs.forEach((output, idx) => {
        if (output.isActive) {
          const targetY = height * 0.15 + (idx * height * 0.7) / (outputs.length + 1);
          particles.push({
            id: particles.length,
            x: hub.x,
            y: hub.y,
            targetX: targetX,
            targetY: targetY,
            progress: 0,
            speed: 0.025, // Fast continuous speed
            layer: 6,
            color: output.color,
            size: 3 + Math.random() * 1.5,
          });
        }
      });
    }

    particlesRef.current = particles;
  };

  const drawCurvedConnection = (
    ctx: CanvasRenderingContext2D,
    x1: number,
    y1: number,
    x2: number,
    y2: number,
    color: string,
    alpha: number
  ) => {
    const controlX = (x1 + x2) / 2;

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.bezierCurveTo(controlX, y1, controlX, y2, x2, y2);
    ctx.strokeStyle = `${color}${Math.floor(alpha * 255).toString(16).padStart(2, '0')}`;
    ctx.lineWidth = 1.5;
    ctx.stroke();
  };

  const drawFileTree = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    const startX = 10;
    let currentY = 40;
    const lineHeight = 12;
    const maxHeight = height - 60;

    // Draw title
    ctx.fillStyle = '#374151';
    ctx.font = 'bold 10px Inter, system-ui, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`PROJECT DIRECTORY (${allFiles.length} files)`, startX, 25);

    const renderNode = (node: FileNode, depth: number): void => {
      if (currentY > maxHeight) return;

      const indent = depth * 10;
      const x = startX + indent;

      // Update Y position for animation
      if (node.type !== 'folder') {
        const fileIndex = allFiles.findIndex(f => f.path === node.path);
        if (fileIndex >= 0) {
          allFiles[fileIndex].yPosition = currentY;
        }
      }

      const isCurrentFile = node.type !== 'folder' &&
                           currentPhase === 0 &&
                           allFiles[currentFileIndex]?.path === node.path;
      const isProcessed = node.type !== 'folder' && processedFiles.has(node.path);

      // Draw file/folder background if active
      if (isCurrentFile || isProcessed) {
        ctx.fillStyle = isCurrentFile ? '#DBEAFE' : '#ECFDF5';
        ctx.fillRect(x - 3, currentY - 9, 180, 11);
      }

      // Draw icon (simplified)
      const iconColor = isCurrentFile ? '#2563EB' :
                       isProcessed ? '#10B981' :
                       node.type === 'folder' ? '#F59E0B' :
                       node.type === 'excel' ? '#10B981' :
                       node.type === 'pdf' ? '#EF4444' :
                       '#6B7280';

      ctx.fillStyle = iconColor;
      if (node.type === 'folder') {
        ctx.fillRect(x, currentY - 7, 6, 5);
      } else {
        ctx.fillRect(x, currentY - 7, 5, 7);
      }

      // Draw filename
      ctx.fillStyle = isCurrentFile ? '#1E40AF' : isProcessed ? '#047857' : '#374151';
      ctx.font = isCurrentFile ? 'bold 9px Inter, system-ui, sans-serif' : '9px Inter, system-ui, sans-serif';
      const maxTextWidth = 150;
      let displayName = node.name;
      if (ctx.measureText(displayName).width > maxTextWidth) {
        while (ctx.measureText(displayName + '...').width > maxTextWidth && displayName.length > 0) {
          displayName = displayName.slice(0, -1);
        }
        displayName += '...';
      }
      ctx.fillText(displayName, x + 8, currentY);

      // Draw checkmark for processed files
      if (isProcessed && !isCurrentFile) {
        ctx.fillStyle = '#10B981';
        ctx.beginPath();
        ctx.arc(x + 165, currentY - 3, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x + 163.5, currentY - 3);
        ctx.lineTo(x + 164.5, currentY - 1.5);
        ctx.lineTo(x + 166.5, currentY - 4.5);
        ctx.stroke();
      }

      currentY += lineHeight;

      // Recursively render all children (show full tree)
      if (node.children) {
        node.children.forEach(child => {
          if (currentY <= maxHeight) {
            renderNode(child, depth + 1);
          }
        });
      }
    };

    renderNode(projectStructure, 0);
  };

  const drawAttentionMatrix = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    if (neuronsRef.current.length < 2) return;

    const layer2 = neuronsRef.current[1];
    const matrixCenterX = (layer2[0].x + neuronsRef.current[2][0].x) / 2;
    const matrixCenterY = height / 2;

    const cellSize = 20; // Match HTML example (20px)
    const gap = 3;
    const totalSize = matrixSize * (cellSize + gap) - gap;
    const startX = matrixCenterX - totalSize / 2;
    const startY = matrixCenterY - totalSize / 2;

    // VERY FAST random pulsing - cells turn on and off quickly
    if (Math.random() < 0.3) { // 30% chance each frame for rapid flashing
      const randomCell = Math.floor(Math.random() * (matrixSize * matrixSize));
      const currentAnimating = matrixAnimationRef.current;
      if (currentAnimating.has(randomCell)) {
        currentAnimating.delete(randomCell); // Turn OFF
      } else {
        currentAnimating.add(randomCell); // Turn ON
      }
    }

    for (let row = 0; row < matrixSize; row++) {
      for (let col = 0; col < matrixSize; col++) {
        const cellIdx = row * matrixSize + col;
        const x = startX + col * (cellSize + gap);
        const y = startY + row * (cellSize + gap);

        // Cell is active if it's in the permanent set OR animating set
        const isActive = matrixCells.has(cellIdx) || matrixAnimationRef.current.has(cellIdx);

        if (isActive) {
          // Active cell with violet gradient (Violet-400 to Violet-500)
          const gradient = ctx.createLinearGradient(x, y, x + cellSize, y + cellSize);
          gradient.addColorStop(0, '#A78BFA'); // Violet-400
          gradient.addColorStop(1, '#8B5CF6'); // Violet-500
          ctx.fillStyle = gradient;
          ctx.shadowBlur = 10;
          ctx.shadowColor = 'rgba(139, 92, 246, 0.5)';
        } else {
          // Inactive cell - Gray-200
          ctx.fillStyle = '#E5E7EB';
          ctx.shadowBlur = 0;
        }

        ctx.beginPath();
        ctx.roundRect(x, y, cellSize, cellSize, 3);
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }

    // Draw "MAPPING LAYER" label
    ctx.fillStyle = '#6B7280'; // Gray-500
    ctx.font = 'bold 10px Inter, system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('MAPPING LAYER', matrixCenterX, startY - 15);
  };

  const drawStaticConnections = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    if (neuronsRef.current.length < 4) return;

    const layer1 = neuronsRef.current[0];
    const layer2 = neuronsRef.current[1];
    const layer3 = neuronsRef.current[2];
    const layer4 = neuronsRef.current[3];

    // Get matrix center position
    const matrixCenterX = (layer2[0].x + layer3[0].x) / 2;
    const matrixCenterY = height / 2;
    const cellSize = 20; // Match HTML example (20px)
    const gap = 3;
    const totalSize = matrixSize * (cellSize + gap) - gap;
    const matrixStartX = matrixCenterX - totalSize / 2;
    const matrixStartY = matrixCenterY - totalSize / 2;

    // Input files to Layer 1 - Bright blue connections
    allFiles.forEach((file, fileIdx) => {
      if (file.yPosition) {
        const neuronIdx = fileIdx % layer1.length;
        const neuron = layer1[neuronIdx];
        if (neuron) {
          drawCurvedConnection(ctx, 190, file.yPosition, neuron.x, neuron.y, '#93C5FD', 0.4);
        }
      }
    });

    // Layer 1 to Layer 2 - FULLY CONNECTED - RED
    layer1.forEach(fromNeuron => {
      layer2.forEach(toNeuron => {
        drawCurvedConnection(ctx, fromNeuron.x, fromNeuron.y, toNeuron.x, toNeuron.y, '#FCA5A5', 0.3);
      });
    });

    // Layer 2 to Matrix cells - FULLY CONNECTED - LIGHT PURPLE
    layer2.forEach(neuron => {
      for (let row = 0; row < matrixSize; row++) {
        for (let col = 0; col < matrixSize; col++) {
          const cellX = matrixStartX + col * (cellSize + gap) + cellSize / 2;
          const cellY = matrixStartY + row * (cellSize + gap) + cellSize / 2;
          drawCurvedConnection(ctx, neuron.x, neuron.y, cellX, cellY, '#DDD6FE', 0.3);
        }
      }
    });

    // Matrix cells to Layer 3 - FULLY CONNECTED - LIGHT PURPLE
    for (let row = 0; row < matrixSize; row++) {
      for (let col = 0; col < matrixSize; col++) {
        const cellX = matrixStartX + col * (cellSize + gap) + cellSize / 2;
        const cellY = matrixStartY + row * (cellSize + gap) + cellSize / 2;

        layer3.forEach(neuron => {
          drawCurvedConnection(ctx, cellX, cellY, neuron.x, neuron.y, '#DDD6FE', 0.3);
        });
      }
    }

    // Layer 3 to Layer 4 - FULLY CONNECTED - GREEN
    layer3.forEach(fromNeuron => {
      layer4.forEach(toNeuron => {
        drawCurvedConnection(ctx, fromNeuron.x, fromNeuron.y, toNeuron.x, toNeuron.y, '#86EFAC', 0.3);
      });
    });

    // Layer 4 to Output Hub - Bright green connections
    const hub = outputHubRef.current;
    layer4.forEach(neuron => {
      drawCurvedConnection(ctx, neuron.x, neuron.y, hub.x, hub.y, '#86EFAC', 0.4);
    });

    // Output Hub to Outputs - Bright green connections
    outputs.forEach((output, idx) => {
      const outputX = width * 0.88;
      const outputY = height * 0.15 + (idx * height * 0.7) / (outputs.length + 1);
      drawCurvedConnection(ctx, hub.x, hub.y, outputX - 5, outputY, '#86EFAC', 0.4);
    });
  };

  const drawNeuralNetwork = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    // Draw neurons with beat effect when particles hit
    neuronsRef.current.forEach((layer, layerIdx) => {
      layer.forEach((neuron, neuronIdx) => {
        // Smooth activation from particles
        neuron.activation += (neuron.targetActivation - neuron.activation) * 0.2;

        // Calculate pulsing radius based on activation
        const pulseRadius = neuron.radius + (neuron.activation * 4);

        // Draw outer glow when active (beat effect)
        if (neuron.activation > 0.1) {
          const glowGradient = ctx.createRadialGradient(neuron.x, neuron.y, 0, neuron.x, neuron.y, pulseRadius + 8);
          glowGradient.addColorStop(0, layerConfig[layerIdx].color + Math.floor(neuron.activation * 100).toString(16).padStart(2, '0'));
          glowGradient.addColorStop(0.5, layerConfig[layerIdx].color + '20');
          glowGradient.addColorStop(1, 'transparent');
          ctx.fillStyle = glowGradient;
          ctx.beginPath();
          ctx.arc(neuron.x, neuron.y, pulseRadius + 8, 0, Math.PI * 2);
          ctx.fill();
        }

        // Draw main neuron with pulsing size
        ctx.fillStyle = layerConfig[layerIdx].color;
        ctx.shadowBlur = neuron.activation > 0.1 ? 15 : 0;
        ctx.shadowColor = layerConfig[layerIdx].color;
        ctx.beginPath();
        ctx.arc(neuron.x, neuron.y, pulseRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        // Decay activation for next frame
        if (neuron.targetActivation > 0) {
          neuron.targetActivation *= 0.88;
        }
      });
    });

    // Draw layer labels (below each layer)
    neuronsRef.current.forEach((layer, idx) => {
      const avgY = layer.reduce((sum, n) => sum + n.y, 0) / layer.length;

      // Layer name (Gray-500)
      ctx.fillStyle = '#6B7280';
      ctx.font = 'bold 10px Inter, system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(layerConfig[idx].name, layer[0].x, avgY + height * 0.38);

      // Node count (Blue-500)
      ctx.fillStyle = '#3B82F6';
      ctx.font = '9px Inter, system-ui, sans-serif';
      ctx.fillText(`${layerConfig[idx].neurons} NODES`, layer[0].x, avgY + height * 0.38 + 12);
    });
  };

  const drawOutputHub = (ctx: CanvasRenderingContext2D) => {
    const hub = outputHubRef.current;

    // Decay activation
    hub.activation *= 0.9;

    // Draw outer glow when active
    if (hub.activation > 0.1) {
      const gradient = ctx.createRadialGradient(hub.x, hub.y, 0, hub.x, hub.y, 25);
      gradient.addColorStop(0, `#10b981${Math.floor(hub.activation * 150).toString(16).padStart(2, '0')}`);
      gradient.addColorStop(0.5, `#10b98130`);
      gradient.addColorStop(1, 'transparent');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(hub.x, hub.y, 25, 0, Math.PI * 2);
      ctx.fill();
    }

    // Draw core hub (Emerald-500 to Emerald-600 gradient)
    const gradient = ctx.createLinearGradient(hub.x - 10, hub.y - 10, hub.x + 10, hub.y + 10);
    gradient.addColorStop(0, '#10B981'); // Emerald-500
    gradient.addColorStop(1, '#059669'); // Emerald-600
    ctx.fillStyle = gradient;
    ctx.shadowBlur = hub.activation > 0.1 ? 20 : 15;
    ctx.shadowColor = '#10B981';
    ctx.beginPath();
    const hubRadius = 10 + (hub.activation * 2); // Hub pulses when active
    ctx.arc(hub.x, hub.y, hubRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // Inner highlight
    ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.beginPath();
    ctx.arc(hub.x - 3, hub.y - 3, 3, 0, Math.PI * 2);
    ctx.fill();
  };

  const drawParticles = (ctx: CanvasRenderingContext2D) => {
    particlesRef.current.forEach((particle) => {
      // Update particle position (handle negative progress for staggered start)
      particle.progress = Math.min(1, particle.progress + particle.speed);

      // Skip drawing if particle hasn't started yet (negative progress)
      if (particle.progress < 0) return;

      // Cubic Bézier curve (4 control points) - matches example exactly
      const t = particle.progress;
      const dx = particle.targetX - particle.x;
      const cp1x = particle.x + dx * 0.3; // First control point (matching HTML example)
      const cp2x = particle.x + dx * 0.7; // Second control point (matching HTML example)

      // Cubic Bézier formula: P(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
      const currentX = Math.pow(1 - t, 3) * particle.x +
                       3 * Math.pow(1 - t, 2) * t * cp1x +
                       3 * (1 - t) * Math.pow(t, 2) * cp2x +
                       Math.pow(t, 3) * particle.targetX;

      const currentY = Math.pow(1 - t, 3) * particle.y +
                       3 * Math.pow(1 - t, 2) * t * particle.y +
                       3 * (1 - t) * Math.pow(t, 2) * particle.targetY +
                       Math.pow(t, 3) * particle.targetY;

      // Draw particle with glow (like HTML)
      ctx.beginPath();
      ctx.arc(currentX, currentY, 5, 0, Math.PI * 2);

      const gradient = ctx.createRadialGradient(currentX, currentY, 0, currentX, currentY, 5);
      gradient.addColorStop(0, particle.color);
      gradient.addColorStop(1, particle.color + '00');

      ctx.fillStyle = gradient;
      ctx.shadowBlur = 20;
      ctx.shadowColor = particle.color;
      ctx.fill();
      ctx.shadowBlur = 0;

      // Activate target neuron or hub when particle reaches it
      if (particle.progress > 0.75) {
        // Light up matrix cell if particle has one
        if (particle.matrixCell !== undefined) {
          const currentAnimating = matrixAnimationRef.current;
          // Turn cell ON when particle arrives
          currentAnimating.add(particle.matrixCell);

          // Turn OFF after short time (automatic cleanup in draw function)
          setTimeout(() => {
            currentAnimating.delete(particle.matrixCell!);
          }, 100); // Flash for 100ms
        }

        // Check if targeting output hub
        const hub = outputHubRef.current;
        const hubDist = Math.sqrt(
          Math.pow(hub.x - particle.targetX, 2) + Math.pow(hub.y - particle.targetY, 2)
        );
        if (hubDist < 15) {
          hub.activation = Math.min(1, hub.activation + 0.3);
        }

        // Check if targeting neurons
        if (particle.layer < neuronsRef.current.length) {
          const targetLayer = neuronsRef.current[particle.layer];
          targetLayer.forEach((neuron) => {
            const dist = Math.sqrt(
              Math.pow(neuron.x - particle.targetX, 2) + Math.pow(neuron.y - particle.targetY, 2)
            );
            if (dist < 18) {
              neuron.targetActivation = Math.min(1, neuron.targetActivation + 0.5);
            }
          });
        }
      }
    });

    particlesRef.current = particlesRef.current.filter(p => p.progress < 1);
  };

  const drawOutputFiles = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    const x = width * 0.88;

    outputs.forEach((output, idx) => {
      const y = height * 0.15 + (idx * height * 0.7) / (outputs.length + 1);

      // Connection from last layer
      if (currentPhase >= layerConfig.length && output.isActive) {
        const lastLayer = neuronsRef.current[neuronsRef.current.length - 1];
        const lastNeuron = lastLayer?.[idx % lastLayer.length];
        if (lastNeuron) {
          drawCurvedConnection(ctx, lastNeuron.x, lastNeuron.y, x - 5, y, output.color, 0.5);
        }
      }

      // Output card - active when conditions met
      const isFullyActive = output.isActive && currentPhase >= layerConfig.length;
      ctx.fillStyle = isFullyActive ? '#F0F9FF' : '#F9FAFB';
      ctx.strokeStyle = isFullyActive ? output.color : '#D1D5DB';
      ctx.lineWidth = isFullyActive ? 2.5 : 1.5;
      roundRect(ctx, x - 5, y - 14, 145, 28, 6);
      ctx.fill();
      ctx.stroke();

      // Checkmark for active outputs
      if (isFullyActive) {
        ctx.fillStyle = output.color;
        ctx.beginPath();
        ctx.arc(x + 5, y, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(x + 3, y);
        ctx.lineTo(x + 4.5, y + 1.5);
        ctx.lineTo(x + 7, y - 2);
        ctx.stroke();
      }

      // Output name
      ctx.fillStyle = isFullyActive ? '#111827' : '#9CA3AF';
      ctx.font = isFullyActive ? 'bold 10px Inter, system-ui, sans-serif' : '10px Inter, system-ui, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(output.name, x + 15, y + 3);
    });
  };

  const roundRect = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number,
    radius: number
  ) => {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  };

  const animate = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const { width, height } = canvas;

    // Clear with subtle gradient background (Gray-50 to Gray-100)
    const bgGradient = ctx.createLinearGradient(0, 0, width, height);
    bgGradient.addColorStop(0, '#FAFBFC'); // Custom light gray
    bgGradient.addColorStop(0.5, '#F9FAFB'); // Gray-50
    bgGradient.addColorStop(1, '#F3F4F6'); // Gray-100
    ctx.fillStyle = bgGradient;
    ctx.fillRect(0, 0, width, height);

    // Draw file tree on canvas
    drawFileTree(ctx, width, height);

    // Draw all static connections first (always visible)
    drawStaticConnections(ctx, width, height);

    // Draw attention matrix in center
    drawAttentionMatrix(ctx, width, height);

    // Draw neural network
    drawNeuralNetwork(ctx, width, height);

    // Draw output hub
    drawOutputHub(ctx);

    // Draw animated particles on top of static connections
    drawParticles(ctx);

    // Draw output files
    drawOutputFiles(ctx, width, height);

    // Continuous particle creation (like HTML) - no phases, just continuous flow
    phaseTimerRef.current++;

    if (phaseTimerRef.current > 10 && currentFileIndex < allFiles.length) {
      phaseTimerRef.current = 0;

      // Mark file as processed
      const newProcessed = new Set(processedFiles);
      newProcessed.add(allFiles[currentFileIndex].path);
      setProcessedFiles(newProcessed);
      updateOutputs(newProcessed);

      // Create particles for ALL phases at once (continuous flow like HTML)
      const file = allFiles[currentFileIndex];
      const fileY = file.yPosition || height * 0.5;
      const sourceX = 190;
      const fileColor = getFileColor(file.type);
      const nodeIdx = currentFileIndex % neuronsRef.current[0].length;

      // Create complete particle chain immediately (like HTML does)
      const particles: Particle[] = [];

      // Create 3 particles per file - STAGGERED (like HTML)
      for (let p = 0; p < 3; p++) {
        // File to Layer 1
        const node1 = neuronsRef.current[0][nodeIdx];
        particles.push({
          id: Date.now() + Math.random() + p * 0.1,
          x: sourceX,
          y: fileY,
          targetX: node1.x,
          targetY: node1.y,
          progress: -p * 0.15, // STAGGER START (negative progress = delayed start)
          speed: 0.025, // Match HTML speed
          layer: 0,
          color: '#3B82F6', // Blue-500 for input particles
          size: 3,
        });
      }

      // Create 2 particles for layers - STAGGERED (like HTML)
      for (let p = 0; p < 2; p++) {
        // Layer 1 to Layer 2
        const node1 = neuronsRef.current[0][nodeIdx];
        const node2 = neuronsRef.current[1][(nodeIdx + 1) % neuronsRef.current[1].length];
        particles.push({
          id: Date.now() + Math.random() + 10 + p * 0.1,
          x: node1.x,
          y: node1.y,
          targetX: node2.x,
          targetY: node2.y,
          progress: -p * 0.15, // STAGGER START
          speed: 0.025,
          layer: 1,
          color: '#EF4444', // Red-500 for processing particles
          size: 3,
        });
      }

      // Layer 2 to Matrix - particles target RANDOM matrix cells
      const layer2 = neuronsRef.current[1];
      const layer3 = neuronsRef.current[2];
      const matrixCenterX = (layer2[0].x + layer3[0].x) / 2;
      const matrixCenterY = height / 2;
      const cellSize = 20;
      const gap = 3;
      const totalSize = matrixSize * (cellSize + gap) - gap;
      const matrixStartX = matrixCenterX - totalSize / 2;
      const matrixStartY = matrixCenterY - totalSize / 2;

      // Create 2 particles to RANDOM matrix cells - STAGGERED (like HTML)
      const node2 = neuronsRef.current[1][(nodeIdx + 1) % neuronsRef.current[1].length];
      for (let p = 0; p < 2; p++) {
        // Pick random matrix cell
        const randomCellIdx = Math.floor(Math.random() * (matrixSize * matrixSize));
        const col = randomCellIdx % matrixSize;
        const row = Math.floor(randomCellIdx / matrixSize);
        const cellX = matrixStartX + col * (cellSize + gap) + cellSize / 2;
        const cellY = matrixStartY + row * (cellSize + gap) + cellSize / 2;

        particles.push({
          id: Date.now() + Math.random() + 20 + p * 0.1,
          x: node2.x,
          y: node2.y,
          targetX: cellX,
          targetY: cellY,
          progress: -p * 0.15, // STAGGER START
          speed: 0.025,
          layer: 2,
          color: '#A78BFA', // Violet-400 for matrix input particles
          size: 3,
          matrixCell: randomCellIdx, // Track which cell to light up
        });
      }

      // Create 2 particles from Matrix to Layer 3 - STAGGERED (like HTML)
      const node3 = neuronsRef.current[2][nodeIdx];
      for (let p = 0; p < 2; p++) {
        particles.push({
          id: Date.now() + Math.random() + 30 + p * 0.1,
          x: matrixCenterX,
          y: matrixCenterY,
          targetX: node3.x,
          targetY: node3.y,
          progress: -p * 0.15, // STAGGER START
          speed: 0.025,
          layer: 3,
          color: '#8B5CF6', // Violet-500 for matrix output particles
          size: 3,
        });
      }

      // Create 2 particles Layer 3 to Layer 4 - STAGGERED (like HTML)
      const node4 = neuronsRef.current[3][nodeIdx];
      for (let p = 0; p < 2; p++) {
        particles.push({
          id: Date.now() + Math.random() + 40 + p * 0.1,
          x: node3.x,
          y: node3.y,
          targetX: node4.x,
          targetY: node4.y,
          progress: -p * 0.15, // STAGGER START
          speed: 0.025,
          layer: 4,
          color: '#10B981', // Emerald-500 for output particles
          size: 3,
        });
      }

      // Create 2 particles Layer 4 to Hub - STAGGERED (like HTML)
      const hub = outputHubRef.current;
      for (let p = 0; p < 2; p++) {
        particles.push({
          id: Date.now() + Math.random() + 50 + p * 0.1,
          x: node4.x,
          y: node4.y,
          targetX: hub.x,
          targetY: hub.y,
          progress: -p * 0.15, // STAGGER START
          speed: 0.025,
          layer: 5,
          color: '#10B981', // Emerald-500 for output particles
          size: 3,
        });
      }

      // Create 2 particles Hub to Output - STAGGERED (like HTML)
      const outputIdx = Math.floor(currentFileIndex / (allFiles.length / outputs.length));
      if (outputIdx < outputs.length && outputs[outputIdx].isActive) {
        const outputX = width * 0.88;
        const outputY = height * 0.15 + (outputIdx * height * 0.7) / (outputs.length + 1);
        for (let p = 0; p < 2; p++) {
          particles.push({
            id: Date.now() + Math.random() + 60 + p * 0.1,
            x: hub.x,
            y: hub.y,
            targetX: outputX,
            targetY: outputY,
            progress: -p * 0.15, // STAGGER START
            speed: 0.025,
            layer: 6,
            color: '#10B981', // Emerald-500 for output particles
            size: 3,
          });
        }
      }

      particlesRef.current.push(...particles);
      setCurrentFileIndex(currentFileIndex + 1);
    }

    animationRef.current = requestAnimationFrame(animate);
  };

  const handleStart = () => {
    setIsAnimating(true);
  };

  const handlePause = () => {
    setIsAnimating(false);
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
  };

  const handleReset = () => {
    setCurrentPhase(0);
    setCurrentFileIndex(0);
    phaseTimerRef.current = 0;
    particlesRef.current = [];
    setProcessedFiles(new Set());
    setOutputs(prev => prev.map(o => ({ ...o, isActive: false })));

    neuronsRef.current.forEach(layer => {
      layer.forEach(neuron => {
        neuron.activation = 0;
        neuron.targetActivation = 0;
      });
    });
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const updateSize = () => {
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio;
      canvas.height = rect.height * window.devicePixelRatio;

      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      }

      initializeNeurons(rect.width, rect.height);
      createParticles(rect.width, rect.height, currentPhase, currentFileIndex);
    };

    updateSize();
    window.addEventListener('resize', updateSize);

    return () => window.removeEventListener('resize', updateSize);
  }, []);

  useEffect(() => {
    if (isAnimating) {
      animate();
    } else if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isAnimating, currentPhase, currentFileIndex, processedFiles]);


  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-2.5 rounded-lg">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900">AI Financial Data Processing Pipeline</h3>
            <p className="text-sm text-gray-500">
              Neural network visualization • {allFiles.length} files • {processedFiles.size} processed
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {!isAnimating ? (
            <button
              onClick={handleStart}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md"
            >
              <Play className="w-4 h-4" />
              Start Processing
            </button>
          ) : (
            <button
              onClick={handlePause}
              className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              <Pause className="w-4 h-4" />
              Pause
            </button>
          )}
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            Reset
          </button>
        </div>
      </div>

      {/* Full-width Neural Network Canvas with Integrated File Tree */}
      <canvas
        ref={canvasRef}
        className="w-full rounded-lg border border-gray-300 shadow-inner"
        style={{ height: '600px' }}
      />

      {/* Progress indicators */}
      <div className="mt-4 grid grid-cols-6 gap-2 text-center">
        <div className="p-3 rounded-lg border-2 border-gray-300 bg-white shadow-sm">
          <div className="text-xs font-medium text-gray-600">File Processing</div>
          <div className="text-lg font-bold text-gray-900 mt-1">{processedFiles.size}/{allFiles.length}</div>
        </div>
        {layerConfig.map((layer, idx) => (
          <div
            key={idx}
            className={`p-2 rounded-lg text-xs transition-all ${
              currentPhase === idx + 1 ? 'bg-gradient-to-br from-indigo-100 to-purple-100 border-2 border-indigo-600 shadow-md' :
              'bg-gray-100 border border-gray-200'
            }`}
          >
            <div className="font-semibold text-gray-800">{layer.name.replace('\n', ' ')}</div>
            <div className="text-gray-600 mt-0.5">{layer.neurons} nodes</div>
          </div>
        ))}
      </div>

      {/* Output status summary */}
      <div className="mt-4 p-4 bg-white rounded-lg border-2 border-gray-300 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <div className="text-xs font-medium text-gray-600">Financial Analysis</div>
          <div className="text-lg font-bold text-gray-900">{outputs.filter(o => o.isActive).length}/{outputs.length}</div>
        </div>
        <div className="grid grid-cols-7 gap-2">
          {outputs.map((output, idx) => (
            <div
              key={idx}
              className={`p-2 rounded text-center transition-all ${
                output.isActive ? 'bg-white border-2 shadow-sm' : 'bg-gray-100 opacity-60'
              }`}
              style={{ borderColor: output.isActive ? output.color : 'transparent' }}
            >
              <div className={`text-[10px] font-semibold ${
                output.isActive ? 'text-gray-900' : 'text-gray-500'
              }`}>
                {output.name}
              </div>
              {output.isActive && (
                <CheckCircle2 className="w-3 h-3 mx-auto mt-1" style={{ color: output.color }} />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
