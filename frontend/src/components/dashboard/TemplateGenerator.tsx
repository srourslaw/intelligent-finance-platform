import { useState, useEffect } from 'react';
import { FileSpreadsheet, Download, CheckCircle, AlertCircle, Clock, Loader } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface TemplateJob {
  status: string;
  started_at: string;
  completed_at?: string;
  output_path?: string;
  error?: string;
  user: string;
}

interface Template {
  name: string;
  filename: string;
  size_bytes: number;
  modified_at: string;
}

export function TemplateGenerator() {
  const { token } = useAuth();
  const [templates, setTemplates] = useState<Template[]>([]);
  const [jobs, setJobs] = useState<Record<string, TemplateJob>>({});
  const [selectedTemplate, setSelectedTemplate] = useState<string>('default');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTemplates();
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/templates/list`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTemplates(response.data.templates || []);
    } catch (err) {
      console.error('Error fetching templates:', err);
    }
  };

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/templates/jobs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setJobs(response.data.jobs || {});
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  };

  const generateTemplate = async (projectId: string) => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/templates/populate-from-project/${projectId}`,
        null,
        {
          params: { template_name: selectedTemplate },
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      // Start polling for job completion
      pollJobStatus(response.data.job_id);
    } catch (err: any) {
      console.error('Error generating template:', err);
      alert(err.response?.data?.detail || 'Failed to generate template');
    } finally {
      setLoading(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/templates/jobs/${jobId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        const job = response.data;

        if (job.status === 'completed' || job.status === 'failed') {
          clearInterval(interval);
          fetchJobs(); // Refresh job list
        }
      } catch (err) {
        console.error('Error polling job status:', err);
        clearInterval(interval);
      }
    }, 2000);
  };

  const downloadTemplate = async (jobId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/templates/download/${jobId}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `financial_report_${jobId}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading template:', err);
      alert('Failed to download template');
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-600" />;
      case 'processing':
        return <Loader className="w-5 h-5 text-blue-600 animate-spin" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Generate Template Card */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <FileSpreadsheet className="w-6 h-6 text-blue-600" />
          <div>
            <h2 className="text-xl font-bold text-gray-900">Excel Template Generator</h2>
            <p className="text-sm text-gray-600">Generate populated financial reports from aggregated data</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Template
            </label>
            <select
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="default">Default Financial Template</option>
              {templates.map(template => (
                <option key={template.name} value={template.name}>
                  {template.filename}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={() => generateTemplate('PROJ001')}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                Generating Template...
              </>
            ) : (
              <>
                <FileSpreadsheet className="w-5 h-5" />
                Generate Financial Report
              </>
            )}
          </button>

          <p className="text-xs text-gray-500 text-center">
            This will create a populated Excel file with the latest aggregated financial data
          </p>
        </div>
      </div>

      {/* Recent Jobs */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Recent Template Jobs</h3>

        {Object.keys(jobs).length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <FileSpreadsheet className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No template generation jobs yet</p>
            <p className="text-sm">Click "Generate Financial Report" to create your first template</p>
          </div>
        ) : (
          <div className="space-y-3">
            {Object.entries(jobs)
              .sort((a, b) => new Date(b[1].started_at).getTime() - new Date(a[1].started_at).getTime())
              .slice(0, 5)
              .map(([jobId, job]) => (
                <div
                  key={jobId}
                  className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {getStatusIcon(job.status)}
                      <div>
                        <div className="font-medium text-gray-900">{jobId}</div>
                        <div className="text-sm text-gray-600">
                          Started: {new Date(job.started_at).toLocaleString()}
                        </div>
                        {job.completed_at && (
                          <div className="text-sm text-gray-600">
                            Completed: {new Date(job.completed_at).toLocaleString()}
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(job.status)}`}>
                        {job.status}
                      </span>

                      {job.status === 'completed' && (
                        <button
                          onClick={() => downloadTemplate(jobId)}
                          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
                        >
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      )}
                    </div>
                  </div>

                  {job.error && (
                    <div className="mt-3 bg-red-50 border border-red-200 rounded-lg p-3">
                      <p className="text-sm text-red-800">
                        <strong>Error:</strong> {job.error}
                      </p>
                    </div>
                  )}
                </div>
              ))}
          </div>
        )}
      </div>

      {/* Template Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <h3 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
          <FileSpreadsheet className="w-5 h-5" />
          How Template Generation Works
        </h3>
        <ul className="text-sm text-blue-800 space-y-1 ml-7">
          <li>• Loads the latest aggregated financial data for your project</li>
          <li>• Populates the Excel template with Balance Sheet, Income Statement, and Cash Flow data</li>
          <li>• Preserves all formulas and formatting in the template</li>
          <li>• Adds a "Data Lineage" sheet showing data sources and confidence levels</li>
          <li>• Download the populated Excel file for review and sharing</li>
        </ul>
      </div>
    </div>
  );
}
