import { useState, useEffect } from 'react';
import { Clock, Play, Pause, Trash2, Plus, Calendar, AlertCircle, CheckCircle, RefreshCw } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface BatchJob {
  job_id: string;
  job_type: string;
  project_id?: string;
  schedule?: string;
  interval_minutes?: number;
  enabled: boolean;
  created_at: string;
  last_run?: string;
  next_run?: string;
  status: string;
  last_result?: {
    files_processed: number;
    transactions: number;
    is_valid: boolean;
    errors: number;
    warnings: number;
  };
  last_error?: string;
}

export function BatchJobs() {
  const { token } = useAuth();
  const [jobs, setJobs] = useState<BatchJob[]>([]);
  const [loading, setLoading] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newJob, setNewJob] = useState({
    job_id: '',
    project_id: '',
    schedule: '0 2 * * *' // Default: 2am daily
  });

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/batch/jobs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setJobs(response.data);
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  };

  const createJob = async () => {
    if (!newJob.job_id || !newJob.project_id) {
      alert('Please fill in all required fields');
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API_BASE_URL}/batch/jobs/aggregation`, newJob, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setShowCreateForm(false);
      setNewJob({ job_id: '', project_id: '', schedule: '0 2 * * *' });
      fetchJobs();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to create job');
    } finally {
      setLoading(false);
    }
  };

  const pauseJob = async (jobId: string) => {
    try {
      await axios.post(`${API_BASE_URL}/batch/jobs/${jobId}/pause`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchJobs();
    } catch (err) {
      console.error('Error pausing job:', err);
    }
  };

  const resumeJob = async (jobId: string) => {
    try {
      await axios.post(`${API_BASE_URL}/batch/jobs/${jobId}/resume`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchJobs();
    } catch (err) {
      console.error('Error resuming job:', err);
    }
  };

  const deleteJob = async (jobId: string) => {
    if (!confirm(`Are you sure you want to delete job "${jobId}"?`)) return;

    try {
      await axios.delete(`${API_BASE_URL}/batch/jobs/${jobId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchJobs();
    } catch (err) {
      console.error('Error deleting job:', err);
    }
  };

  const runJobNow = async (jobId: string) => {
    try {
      await axios.post(`${API_BASE_URL}/batch/jobs/${jobId}/run`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert(`Job "${jobId}" triggered successfully`);
      setTimeout(fetchJobs, 2000); // Refresh after 2 seconds
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to run job');
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="flex items-center gap-1 px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
            <CheckCircle className="w-3 h-3" />
            Completed
          </span>
        );
      case 'running':
        return (
          <span className="flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
            <RefreshCw className="w-3 h-3 animate-spin" />
            Running
          </span>
        );
      case 'failed':
        return (
          <span className="flex items-center gap-1 px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
            <AlertCircle className="w-3 h-3" />
            Failed
          </span>
        );
      default:
        return (
          <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
            {status}
          </span>
        );
    }
  };

  const parseSchedule = (schedule: string): string => {
    const parts = schedule.split(' ');
    if (parts.length !== 5) return schedule;

    const [minute, hour, day, month, weekday] = parts;

    if (minute === '0' && hour === '2' && day === '*' && month === '*' && weekday === '*') {
      return 'Daily at 2:00 AM';
    }
    if (minute === '0' && hour === '0' && day === '*' && month === '*' && weekday === '0') {
      return 'Weekly on Sunday at midnight';
    }
    if (minute === '0' && hour === '0' && day === '1' && month === '*' && weekday === '*') {
      return 'Monthly on 1st at midnight';
    }
    if (minute === '0' && hour.startsWith('*/')) {
      return `Every ${hour.slice(2)} hours`;
    }

    return schedule;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">⏰ Scheduled Batch Jobs</h2>
            <p className="text-sm text-gray-600 mt-1">
              Automate aggregations and processing tasks with cron-like scheduling
            </p>
          </div>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Job
          </button>
        </div>

        {/* Create Form */}
        {showCreateForm && (
          <div className="border-t border-gray-200 pt-4 mt-4">
            <h3 className="font-medium text-gray-900 mb-3">Create Aggregation Job</h3>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Job ID</label>
                <input
                  type="text"
                  value={newJob.job_id}
                  onChange={(e) => setNewJob({ ...newJob, job_id: e.target.value })}
                  placeholder="daily_aggregation"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Project ID</label>
                <input
                  type="text"
                  value={newJob.project_id}
                  onChange={(e) => setNewJob({ ...newJob, project_id: e.target.value })}
                  placeholder="Q4_2024"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Schedule (Cron)</label>
                <select
                  value={newJob.schedule}
                  onChange={(e) => setNewJob({ ...newJob, schedule: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="0 2 * * *">Daily at 2:00 AM</option>
                  <option value="0 */4 * * *">Every 4 hours</option>
                  <option value="0 0 * * 0">Weekly (Sunday)</option>
                  <option value="0 0 1 * *">Monthly (1st)</option>
                </select>
              </div>
            </div>

            <div className="flex items-center gap-3 mt-4">
              <button
                onClick={createJob}
                disabled={loading}
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition-colors"
              >
                {loading ? 'Creating...' : 'Create Job'}
              </button>
              <button
                onClick={() => setShowCreateForm(false)}
                className="px-6 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Jobs List */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-900">Active Jobs ({jobs.length})</h3>
        </div>

        {jobs.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <Clock className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No scheduled jobs yet</p>
            <p className="text-sm mt-1">Create your first job to automate aggregations</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {jobs.map((job) => (
              <div key={job.job_id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h4 className="font-bold text-gray-900">{job.job_id}</h4>
                      {getStatusBadge(job.status)}
                      {!job.enabled && (
                        <span className="px-2 py-1 bg-gray-200 text-gray-600 rounded-full text-xs font-medium">
                          Paused
                        </span>
                      )}
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Project</p>
                        <p className="font-medium text-gray-900">{job.project_id || 'N/A'}</p>
                      </div>

                      <div>
                        <p className="text-gray-500">Schedule</p>
                        <p className="font-medium text-gray-900">
                          {job.schedule ? parseSchedule(job.schedule) : 'N/A'}
                        </p>
                      </div>

                      <div>
                        <p className="text-gray-500">Last Run</p>
                        <p className="font-medium text-gray-900">
                          {job.last_run
                            ? new Date(job.last_run).toLocaleString()
                            : 'Never'}
                        </p>
                      </div>

                      <div>
                        <p className="text-gray-500">Next Run</p>
                        <p className="font-medium text-gray-900">
                          {job.next_run
                            ? new Date(job.next_run).toLocaleString()
                            : 'Not scheduled'}
                        </p>
                      </div>
                    </div>

                    {/* Last Result */}
                    {job.last_result && (
                      <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                        <p className="text-sm font-medium text-green-900">
                          Last Result: {job.last_result.files_processed} files, {job.last_result.transactions} transactions
                          {!job.last_result.is_valid && (
                            <span className="ml-2 text-red-600">
                              ({job.last_result.errors} errors)
                            </span>
                          )}
                        </p>
                      </div>
                    )}

                    {/* Last Error */}
                    {job.last_error && (
                      <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-sm font-medium text-red-900">Error: {job.last_error}</p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 ml-4">
                    <button
                      onClick={() => runJobNow(job.job_id)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      title="Run Now"
                    >
                      <Play className="w-4 h-4" />
                    </button>

                    {job.enabled ? (
                      <button
                        onClick={() => pauseJob(job.job_id)}
                        className="p-2 text-yellow-600 hover:bg-yellow-50 rounded-lg transition-colors"
                        title="Pause"
                      >
                        <Pause className="w-4 h-4" />
                      </button>
                    ) : (
                      <button
                        onClick={() => resumeJob(job.job_id)}
                        className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        title="Resume"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    )}

                    <button
                      onClick={() => deleteJob(job.job_id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Info Card */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div className="flex items-start gap-3">
          <Calendar className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-900 mb-2">About Scheduled Jobs</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Jobs run automatically based on their schedule</li>
              <li>• Aggregation jobs combine all uploaded files for a project</li>
              <li>• You can trigger any job manually with "Run Now"</li>
              <li>• Pause jobs temporarily or delete them permanently</li>
              <li>• Jobs persist across server restarts</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
