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
 * Login
 */
export async function login(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  return fetchAPI<{ access_token: string; token_type: string }>('/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });
}

/**
 * Verify token
 */
export async function verifyToken(token: string) {
  return fetchAPI<{ email: string; full_name: string; role: string }>('/auth/verify', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get current user
 */
export async function getCurrentUser(token: string) {
  return fetchAPI<{ email: string; full_name: string; role: string }>('/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Health Check
 */
export async function checkApiHealth(token?: string) {
  return fetchAPI<{ status: string; message: string }>('/projects/health', {
    headers: token ? {
      'Authorization': `Bearer ${token}`,
    } : {},
  });
}

/**
 * Get complete dashboard data
 */
export async function getDashboardData(token: string, projectId: string = 'project-a-123-sunset-blvd') {
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
  }>(`/projects/dashboard?project_id=${projectId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get budget data
 */
export async function getBudgetData(token: string, projectId: string = 'project-a-123-sunset-blvd') {
  return fetchAPI<{
    summary: any;
    items: any[];
  }>(`/projects/budget?project_id=${projectId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get subcontractor data
 */
export async function getSubcontractors(token: string) {
  return fetchAPI<{
    subcontractors: any[];
    payments: any[];
  }>('/projects/subcontractors', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get client payment data
 */
export async function getClientPayments(token: string) {
  return fetchAPI<{
    milestones: any[];
    variations: any[];
  }>('/projects/client-payments', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get defects data
 */
export async function getDefects(token: string) {
  return fetchAPI<{
    defects: any[];
  }>('/projects/defects', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get timesheets data
 */
export async function getTimesheets(token: string) {
  return fetchAPI<{
    entries: any[];
  }>('/projects/timesheets', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get purchase orders data
 */
export async function getPurchaseOrders(token: string) {
  return fetchAPI<{
    orders: any[];
  }>('/projects/purchase-orders', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get cashflow forecast
 */
export async function getCashflowForecast(token: string, weeks: number = 12) {
  return fetchAPI<{
    forecast_weeks: number;
    weekly_burn_rate: number;
    expected_income: number;
    weekly_forecast: any[];
  }>(`/projects/cashflow?weeks=${weeks}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get AI-generated insights
 */
export async function getInsights(token: string) {
  return fetchAPI<{
    insights: any[];
  }>('/projects/insights', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get list of all projects
 */
export async function getProjectsList(token: string) {
  return fetchAPI<any[]>('/projects/list', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Upload budget file
 */
export async function uploadBudgetFile(file: File, token: string) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/budget', {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Upload subcontractor file
 */
export async function uploadSubcontractorFile(file: File, token: string) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/subcontractors', {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Upload client payments file
 */
export async function uploadClientPaymentsFile(file: File, token: string) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/client-payments', {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Upload defects file
 */
export async function uploadDefectsFile(file: File, token: string) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/defects', {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Upload timesheets file
 */
export async function uploadTimesheetsFile(file: File, token: string) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/timesheets', {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Upload purchase orders file
 */
export async function uploadPurchaseOrdersFile(file: File, token: string) {
  const formData = new FormData();
  formData.append('file', file);

  return fetchAPI<{ status: string; message: string; filename: string }>('/uploads/purchase-orders', {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Get list of documents
 */
export async function getDocumentList(projectId: string, token: string) {
  return fetchAPI<any[]>(`/documents/list/${projectId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Preview a document
 */
export async function previewDocument(projectId: string, filePath: string, token: string) {
  return fetchAPI<any>(`/documents/preview/${projectId}/${filePath}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}

/**
 * Download a document
 */
export function getDocumentDownloadUrl(projectId: string, filePath: string): string {
  return `${API_BASE_URL}/documents/download/${projectId}/${filePath}`;
}

export default {
  login,
  verifyToken,
  getCurrentUser,
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
  getProjectsList,
  uploadBudgetFile,
  uploadSubcontractorFile,
  uploadClientPaymentsFile,
  uploadDefectsFile,
  uploadTimesheetsFile,
  uploadPurchaseOrdersFile,
  getDocumentList,
  previewDocument,
  getDocumentDownloadUrl,
};
