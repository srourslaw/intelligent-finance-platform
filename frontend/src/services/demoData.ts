// Demo data service using real backend project data
// This allows the frontend to work without a running backend API

export const DEMO_PROJECTS = [
  {
    id: 'project-a-123-sunset-blvd',
    name: '123 Sunset Boulevard',
    client: 'Mr & Mrs Thompson',
    address: '123 Sunset Boulevard, Riverside Heights, NSW 2155',
    status: 'In Progress - Behind Schedule'
  },
  {
    id: 'project-b-456-ocean-drive',
    name: '456 Ocean Drive',
    client: 'Marine Corp Developments',
    address: '456 Ocean Drive, Coastal Bay, NSW 2100',
    status: 'In Progress'
  },
  {
    id: 'project-c-789-mountain-view',
    name: '789 Mountain View Terrace',
    client: 'Highland Properties Ltd',
    address: '789 Mountain View Terrace, Blue Ridge, NSW 2200',
    status: 'Planning'
  }
];

// Sample extracted files from project-a-123-sunset-blvd
export const DEMO_EXTRACTED_FILES = [
  {
    file_id: 'file_001',
    filename: 'Land_Costs.xlsx',
    file_type: 'excel',
    upload_date: '2024-01-15T10:30:00Z',
    extraction_status: 'completed',
    confidence_score: 0.95,
    folder: '01_LAND_PURCHASE',
    document_classification: 'Financial Summary'
  },
  {
    file_id: 'file_002',
    filename: 'Legal_Fees_Invoice_JohnsonSolicitors.pdf',
    file_type: 'pdf',
    upload_date: '2024-01-16T14:20:00Z',
    extraction_status: 'completed',
    confidence_score: 0.92,
    folder: '01_LAND_PURCHASE',
    document_classification: 'Invoice'
  },
  {
    file_id: 'file_003',
    filename: 'Budget_vs_Actual.xlsx',
    file_type: 'excel',
    upload_date: '2024-03-10T09:15:00Z',
    extraction_status: 'completed',
    confidence_score: 0.98,
    folder: '12_BUDGET_TRACKING',
    document_classification: 'Budget Report'
  },
  {
    file_id: 'file_004',
    filename: 'Subcontractor_Register.xlsx',
    file_type: 'excel',
    upload_date: '2024-02-05T16:45:00Z',
    extraction_status: 'completed',
    confidence_score: 0.88,
    folder: '07_SUBCONTRACTORS',
    document_classification: 'Contractor List'
  },
  {
    file_id: 'file_005',
    filename: 'Balance_Sheet_Sept_2024.xlsx',
    file_type: 'excel',
    upload_date: '2024-09-30T23:59:00Z',
    extraction_status: 'completed',
    confidence_score: 0.96,
    folder: '19_MONTHLY_CLOSE',
    document_classification: 'Financial Statement'
  }
];

// Sample transactions extracted from files
export const DEMO_TRANSACTIONS = [
  {
    id: 'txn_001',
    file_id: 'file_001',
    date: '2024-01-15',
    description: 'Land Purchase - 123 Sunset Blvd',
    category: 'LAND & ACQUISITION',
    amount: 285000.00,
    transaction_type: 'expense',
    confidence: 0.98,
    source_location: 'Sheet1!A5',
    supplier: 'Ray White Riverside',
    invoice_ref: 'RW-2024-0089'
  },
  {
    id: 'txn_002',
    file_id: 'file_001',
    date: '2024-01-15',
    description: 'Stamp Duty',
    category: 'LAND & ACQUISITION',
    amount: 12750.00,
    transaction_type: 'expense',
    confidence: 0.95,
    source_location: 'Sheet1!A6',
    supplier: 'NSW Revenue',
    invoice_ref: ''
  },
  {
    id: 'txn_003',
    file_id: 'file_002',
    date: '2024-01-16',
    description: 'Legal Fees - Conveyancing',
    category: 'LAND & ACQUISITION',
    amount: 1850.50,
    transaction_type: 'expense',
    confidence: 0.92,
    source_location: 'Invoice Total',
    supplier: 'Jenkins & Associates',
    invoice_ref: 'JA-2024-0123'
  },
  {
    id: 'txn_004',
    file_id: 'file_001',
    date: '2024-01-18',
    description: 'Soil Testing & Geotechnical',
    category: 'LAND & ACQUISITION',
    amount: 2650.00,
    transaction_type: 'expense',
    confidence: 0.89,
    source_location: 'Sheet1!A8',
    supplier: 'GeoTech Solutions',
    invoice_ref: 'GEO-2024-0045'
  },
  {
    id: 'txn_005',
    file_id: 'file_003',
    date: '2024-03-05',
    description: 'Framing - Labour & Materials',
    category: 'CONSTRUCTION',
    amount: 45600.00,
    transaction_type: 'expense',
    confidence: 0.94,
    source_location: 'Sheet1!B15',
    supplier: 'BuildRight Framers',
    invoice_ref: 'BRF-2024-0234'
  },
  {
    id: 'txn_006',
    file_id: 'file_004',
    date: '2024-02-10',
    description: 'Plumbing - First Fix',
    category: 'CONSTRUCTION',
    amount: 12400.00,
    transaction_type: 'expense',
    confidence: 0.91,
    source_location: 'Sheet1!C7',
    supplier: 'Aqua Plumbing Services',
    invoice_ref: 'APS-2024-0156'
  },
  {
    id: 'txn_007',
    file_id: 'file_004',
    date: '2024-02-10',
    description: 'Electrical - First Fix',
    category: 'CONSTRUCTION',
    amount: 10800.00,
    transaction_type: 'expense',
    confidence: 0.88,
    source_location: 'Sheet1!C8',
    supplier: 'Spark Electrical Co',
    invoice_ref: 'SEC-2024-0178'
  },
  {
    id: 'txn_008',
    file_id: 'file_005',
    date: '2024-09-01',
    description: 'Client Progress Payment #3',
    category: 'REVENUE',
    amount: 130000.00,
    transaction_type: 'income',
    confidence: 0.97,
    source_location: 'Sheet1!D12',
    supplier: 'Mr & Mrs Thompson',
    invoice_ref: 'INV-2024-003'
  }
];

// Potential conflicts (duplicate transactions across files)
export const DEMO_CONFLICTS = [
  {
    id: 'conflict_001',
    transaction_description: 'Legal Fees - Conveyancing',
    amount: 1850.50,
    date: '2024-01-16',
    occurrences: [
      {
        file_id: 'file_001',
        filename: 'Land_Costs.xlsx',
        confidence: 0.89,
        source_location: 'Sheet1!A7',
        selected: false
      },
      {
        file_id: 'file_002',
        filename: 'Legal_Fees_Invoice_JohnsonSolicitors.pdf',
        confidence: 0.92,
        source_location: 'Invoice Total',
        selected: true // Highest confidence
      }
    ]
  },
  {
    id: 'conflict_002',
    transaction_description: 'Soil Testing & Geotechnical',
    amount: 2650.00,
    date: '2024-01-18',
    occurrences: [
      {
        file_id: 'file_001',
        filename: 'Land_Costs.xlsx',
        confidence: 0.89,
        source_location: 'Sheet1!A8',
        selected: true // User selected this one
      },
      {
        file_id: 'file_003',
        filename: 'Budget_vs_Actual.xlsx',
        confidence: 0.85,
        source_location: 'Sheet2!B23',
        selected: false
      }
    ]
  }
];

// Batch jobs configuration
export const DEMO_BATCH_JOBS = [
  {
    id: 'job_001',
    name: 'Daily Financial Aggregation',
    schedule: '0 0 * * *', // Daily at midnight
    status: 'active',
    last_run: '2024-10-09T00:00:00Z',
    next_run: '2024-10-10T00:00:00Z',
    success_rate: 0.98,
    description: 'Aggregates all transactions and updates financial reports'
  },
  {
    id: 'job_002',
    name: 'Weekly Conflict Detection',
    schedule: '0 2 * * 0', // Sundays at 2am
    status: 'active',
    last_run: '2024-10-06T02:00:00Z',
    next_run: '2024-10-13T02:00:00Z',
    success_rate: 1.00,
    description: 'Scans all files for duplicate transactions'
  },
  {
    id: 'job_003',
    name: 'Monthly Report Generation',
    schedule: '0 1 1 * *', // 1st of month at 1am
    status: 'paused',
    last_run: '2024-09-01T01:00:00Z',
    next_run: null,
    success_rate: 0.95,
    description: 'Generates comprehensive monthly financial statements'
  }
];

// Helper functions
export const getDemoFilesByProject = (_projectId: string) => {
  return DEMO_EXTRACTED_FILES;
};

export const getDemoTransactionsByFile = (fileId: string) => {
  return DEMO_TRANSACTIONS.filter(t => t.file_id === fileId);
};

export const getAllDemoTransactions = () => {
  return DEMO_TRANSACTIONS;
};

export const getDemoConflicts = () => {
  return DEMO_CONFLICTS;
};

export const getDemoBatchJobs = () => {
  return DEMO_BATCH_JOBS;
};

// Check if backend is available
export const checkBackendAvailability = async (apiUrl: string): Promise<boolean> => {
  try {
    const response = await fetch(`${apiUrl}/health`, { method: 'GET', signal: AbortSignal.timeout(2000) });
    return response.ok;
  } catch {
    return false;
  }
};
