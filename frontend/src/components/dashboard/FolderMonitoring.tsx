import { useState, useEffect } from 'react';
import { Folder, Play, Square, Plus, Trash2, Activity, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface WatchConfig {
  path: string;
  project_id?: string;
  patterns: string[];
  recursive: boolean;
  process_existing: boolean;
  process_modifications: boolean;
}

interface FolderMonitoringStatus {
  running: boolean;
  watch_configs: WatchConfig[];
  statistics: {
    total_processed: number;
    total_errors: number;
    success_rate: number;
    by_date: Record<string, { processed: number; errors: number }>;
  };
}

export function FolderMonitoring() {
  const { token } = useAuth();
  const [status, setStatus] = useState<FolderMonitoringStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newFolder, setNewFolder] = useState<WatchConfig>({
    path: '',
    project_id: '',
    patterns: ['*.xlsx', '*.pdf', '*.csv'],
    recursive: true,
    process_existing: false,
    process_modifications: false
  });

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/folder-watch/status`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStatus(response.data);
    } catch (err) {
      console.error('Error fetching folder monitoring status:', err);
    } finally {
      setLoading(false);
    }
  };

  const startMonitoring = async () => {
    try {
      await axios.post(
        `${API_BASE_URL}/folder-watch/start`,
        null,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchStatus();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to start monitoring');
    }
  };

  const stopMonitoring = async () => {
    try {
      await axios.post(
        `${API_BASE_URL}/folder-watch/stop`,
        null,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchStatus();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to stop monitoring');
    }
  };

  const addFolder = async () => {
    try {
      await axios.post(
        `${API_BASE_URL}/folder-watch/add`,
        newFolder,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setShowAddModal(false);
      setNewFolder({
        path: '',
        project_id: '',
        patterns: ['*.xlsx', '*.pdf', '*.csv'],
        recursive: true,
        process_existing: false,
        process_modifications: false
      });
      fetchStatus();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to add folder');
    }
  };

  const removeFolder = async (path: string) => {
    if (!confirm(`Remove monitoring for ${path}?`)) return;

    try {
      await axios.delete(`${API_BASE_URL}/folder-watch/remove/${encodeURIComponent(path)}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchStatus();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to remove folder');
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Control Panel */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Folder className="w-6 h-6 text-blue-600" />
            <div>
              <h2 className="text-xl font-bold text-gray-900">Local Folder Monitoring</h2>
              <p className="text-sm text-gray-600">Auto-process files from local/network folders</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {status?.running ? (
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-green-100 text-green-800">
                <Activity className="w-5 h-5 animate-pulse" />
                <span className="font-medium">Running</span>
              </div>
            ) : (
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-100 text-gray-800">
                <Square className="w-5 h-5" />
                <span className="font-medium">Stopped</span>
              </div>
            )}
          </div>
        </div>

        <div className="flex gap-3">
          {!status?.running ? (
            <button
              onClick={startMonitoring}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
            >
              <Play className="w-4 h-4" />
              Start Monitoring
            </button>
          ) : (
            <button
              onClick={stopMonitoring}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
            >
              <Square className="w-4 h-4" />
              Stop Monitoring
            </button>
          )}

          <button
            onClick={() => setShowAddModal(true)}
            className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Folder
          </button>
        </div>
      </div>

      {/* Statistics */}
      {status?.statistics && (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Processing Statistics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-sm text-blue-600 mb-1">Total Processed</div>
              <div className="text-2xl font-bold text-blue-900">{status.statistics.total_processed}</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-sm text-green-600 mb-1">Success Rate</div>
              <div className="text-2xl font-bold text-green-900">
                {status.statistics?.success_rate?.toFixed(1) || '0'}%
              </div>
            </div>
            <div className="bg-red-50 rounded-lg p-4">
              <div className="text-sm text-red-600 mb-1">Errors</div>
              <div className="text-2xl font-bold text-red-900">{status.statistics.total_errors}</div>
            </div>
          </div>
        </div>
      )}

      {/* Watched Folders */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Watched Folders</h3>

        {!status?.watch_configs || status.watch_configs.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Folder className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No folders configured</p>
            <p className="text-sm">Click "Add Folder" to start monitoring a directory</p>
          </div>
        ) : (
          <div className="space-y-3">
            {status.watch_configs.map((config, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 mb-2">{config.path}</div>
                    <div className="text-sm text-gray-600 space-y-1">
                      <div>Project: {config.project_id || 'Auto-detect'}</div>
                      <div>Patterns: {config.patterns.join(', ')}</div>
                      <div className="flex items-center gap-4">
                        <span className="flex items-center gap-1">
                          {config.recursive ? <CheckCircle className="w-4 h-4 text-green-600" /> : <AlertCircle className="w-4 h-4 text-gray-400" />}
                          Recursive
                        </span>
                        <span className="flex items-center gap-1">
                          {config.process_existing ? <CheckCircle className="w-4 h-4 text-green-600" /> : <AlertCircle className="w-4 h-4 text-gray-400" />}
                          Process Existing
                        </span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => removeFolder(config.path)}
                    className="text-red-600 hover:text-red-700 p-2"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Folder Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Add Folder to Monitor</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Folder Path</label>
                <input
                  type="text"
                  value={newFolder.path}
                  onChange={(e) => setNewFolder({ ...newFolder, path: e.target.value })}
                  placeholder="/path/to/folder"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Project ID (Optional)</label>
                <input
                  type="text"
                  value={newFolder.project_id}
                  onChange={(e) => setNewFolder({ ...newFolder, project_id: e.target.value })}
                  placeholder="PROJ001"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">File Patterns</label>
                <input
                  type="text"
                  value={newFolder.patterns.join(', ')}
                  onChange={(e) => setNewFolder({ ...newFolder, patterns: e.target.value.split(',').map(p => p.trim()) })}
                  placeholder="*.xlsx, *.pdf, *.csv"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="space-y-2">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={newFolder.recursive}
                    onChange={(e) => setNewFolder({ ...newFolder, recursive: e.target.checked })}
                    className="rounded"
                  />
                  <span className="text-sm text-gray-700">Watch subdirectories</span>
                </label>

                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={newFolder.process_existing}
                    onChange={(e) => setNewFolder({ ...newFolder, process_existing: e.target.checked })}
                    className="rounded"
                  />
                  <span className="text-sm text-gray-700">Process existing files on startup</span>
                </label>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={addFolder}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition-colors"
              >
                Add Folder
              </button>
              <button
                onClick={() => setShowAddModal(false)}
                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 rounded-lg transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <h3 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
          <Folder className="w-5 h-5" />
          How Folder Monitoring Works
        </h3>
        <ul className="text-sm text-blue-800 space-y-1 ml-7">
          <li>• Monitors local or network folders for new files</li>
          <li>• Automatically processes files when they appear (Extract → Classify → Validate)</li>
          <li>• Supports multiple folder watches with different configurations</li>
          <li>• Can assign files to specific projects or auto-detect project ID</li>
          <li>• Optionally processes existing files when monitoring starts</li>
        </ul>
      </div>
    </div>
  );
}
