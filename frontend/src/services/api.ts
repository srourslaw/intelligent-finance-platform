/**
 * API Service Layer
 * Handles all HTTP requests to FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      return {
        error: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
      };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    console.error('API fetch error:', error);
    return {
      error: error instanceof Error ? error.message : 'Network error',
    };
  }
}

/**
 * Health Check
 */
export async function checkApiHealth() {
  return fetchAPI<{ status: string; message: string }>('/projects/health');
}

/**
 * Get complete dashboard data
 */
export async function getDashboardData() {
  return fetchAPI<{
    kpis: any;
    budget_summary: any;
    budget_items: any[];
    subcontractors: any[];
    payments: any[];
    milestones: any[];
    variations: any[];
    defects: any[];
    critical_issues: any[];
    cashflow: any;
    insights: any[];
  }>('/projects/dashboard');
}

/**
 * Get budget data
 */
export async function getBudgetData() {
  return fetchAPI<{
    summary: any;
    items: any[];
  }>('/projects/budget');
}

/**
 * Get subcontractor data
 */
export async function getSubcontractors() {
  return fetchAPI<{
    subcontractors: any[];
    payments: any[];
  }>('/projects/subcontractors');
}

/**
 * Get client payment data
 */
export async function getClientPayments() {
  return fetchAPI<{
    milestones: any[];
    variations: any[];
  }>('/projects/client-payments');
}

/**
 * Get defects data
 */
export async function getDefects() {
  return fetchAPI<{
    defects: any[];
  }>('/projects/defects');
}

/**
 * Get timesheets data
 */
export async function getTimesheets() {
  return fetchAPI<{
    entries: any[];
  }>('/projects/timesheets');
}

/**
 * Get purchase orders data
 */
export async function getPurchaseOrders() {
  return fetchAPI<{
    orders: any[];
  }>('/projects/purchase-orders');
}

/**
 * Get cashflow forecast
 */
export async function getCashflowForecast(weeks: number = 12) {
  return fetchAPI<{
    forecast_weeks: number;
    weekly_burn_rate: number;
    expected_income: number;
    weekly_forecast: any[];
  }>(`/projects/cashflow?weeks=${weeks}`);
}

/**
 * Get AI-generated insights
 */
export async function getInsights() {
  return fetchAPI<{
    insights: any[];
  }>('/projects/insights');
}

/**
 * Upload budget file
 */
export async function uploadBudgetFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/budget', {
    method: 'POST',
    body: formData,
    headers: {}, // Let browser set Content-Type for FormData
  });
}

/**
 * Upload subcontractor file
 */
export async function uploadSubcontractorFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/subcontractors', {
    method: 'POST',
    body: formData,
    headers: {},
  });
}

/**
 * Upload client payments file
 */
export async function uploadClientPaymentsFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/client-payments', {
    method: 'POST',
    body: formData,
    headers: {},
  });
}

/**
 * Upload defects file
 */
export async function uploadDefectsFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/defects', {
    method: 'POST',
    body: formData,
    headers: {},
  });
}

/**
 * Upload timesheets file
 */
export async function uploadTimesheetsFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/timesheets', {
    method: 'POST',
    body: formData,
    headers: {},
  });
}

/**
 * Upload purchase orders file
 */
export async function uploadPurchaseOrdersFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/purchase-orders', {
    method: 'POST',
    body: formData,
    headers: {},
  });
}

export default {
  checkApiHealth,
  getDashboardData,
  getBudgetData,
  getSubcontractors,
  getClientPayments,
  getDefects,
  getTimesheets,
  getPurchaseOrders,
  getCashflowForecast,
  getInsights,
  uploadBudgetFile,
  uploadSubcontractorFile,
  uploadClientPaymentsFile,
  uploadDefectsFile,
  uploadTimesheetsFile,
  uploadPurchaseOrdersFile,
};
