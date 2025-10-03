import { useState, useEffect } from 'react';
import { Mail, RefreshCw, CheckCircle, AlertCircle, Inbox, FileText, Calendar } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface EmailAttachment {
  filename: string;
  saved_as: string;
  filepath: string;
  size: number;
  project_id?: string;
  message_id: string;
  received_at: string;
}

interface EmailStatistics {
  total_processed: number;
  total_files: number;
}

interface EmailStatus {
  configured: boolean;
  email_address?: string;
  imap_server?: string;
  watched_folder?: string;
  message: string;
}

export function EmailIntegration() {
  const { token } = useAuth();
  const [status, setStatus] = useState<EmailStatus | null>(null);
  const [statistics, setStatistics] = useState<EmailStatistics | null>(null);
  const [recentAttachments, setRecentAttachments] = useState<EmailAttachment[]>([]);
  const [checking, setChecking] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatus();
    fetchStatistics();
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/email/status`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStatus(response.data);
    } catch (err) {
      console.error('Error fetching email status:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/email/statistics`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStatistics(response.data);
    } catch (err) {
      console.log('Email statistics not available');
    }
  };

  const checkEmails = async () => {
    if (!status?.configured) {
      alert('Email integration is not configured');
      return;
    }

    setChecking(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/email/check`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });

      const attachments = response.data;
      setRecentAttachments(attachments);

      if (attachments.length > 0) {
        alert(`Found ${attachments.length} new files`);
        fetchStatistics();
      } else {
        alert('No new emails with attachments');
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to check emails');
    } finally {
      setChecking(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatDate = (timestamp: string): string => {
    const year = timestamp.slice(0, 4);
    const month = timestamp.slice(4, 6);
    const day = timestamp.slice(6, 8);
    const hour = timestamp.slice(9, 11);
    const minute = timestamp.slice(11, 13);
    return `${year}-${month}-${day} ${hour}:${minute}`;
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="animate-pulse flex items-center gap-3">
          <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
          <div className="flex-1">
            <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
              <Mail className="w-6 h-6 text-blue-600" />
              Email Integration
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              Automatically receive and process files via email
            </p>
          </div>

          <button
            onClick={checkEmails}
            disabled={checking || !status?.configured}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${checking ? 'animate-spin' : ''}`} />
            {checking ? 'Checking...' : 'Check Now'}
          </button>
        </div>

        <div className={`flex items-center gap-3 p-4 rounded-lg border ${
          status?.configured
            ? 'bg-green-50 border-green-200'
            : 'bg-yellow-50 border-yellow-200'
        }`}>
          {status?.configured ? (
            <CheckCircle className="w-5 h-5 text-green-600" />
          ) : (
            <AlertCircle className="w-5 h-5 text-yellow-600" />
          )}
          <div className="flex-1">
            <p className={`text-sm font-medium ${
              status?.configured ? 'text-green-900' : 'text-yellow-900'
            }`}>
              {status?.message}
            </p>
            {status?.configured && (
              <div className="text-xs text-green-700 mt-1">
                <p>Email: {status.email_address}</p>
                <p>Server: {status.imap_server}</p>
              </div>
            )}
          </div>
        </div>

        {statistics && (
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="text-3xl font-bold text-blue-600">{statistics.total_processed}</div>
              <div className="text-sm text-blue-900 mt-1">Emails Processed</div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="text-3xl font-bold text-green-600">{statistics.total_files}</div>
              <div className="text-sm text-green-900 mt-1">Files Downloaded</div>
            </div>
          </div>
        )}
      </div>

      {recentAttachments.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
              <Inbox className="w-5 h-5 text-blue-600" />
              Recent Downloads ({recentAttachments.length})
            </h3>
          </div>

          <div className="divide-y divide-gray-200">
            {recentAttachments.map((attachment, idx) => (
              <div key={idx} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <FileText className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">{attachment.filename}</p>
                    <div className="flex items-center gap-4 mt-1 text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {formatDate(attachment.received_at)}
                      </span>
                      <span>{formatFileSize(attachment.size)}</span>
                      {attachment.project_id && (
                        <span className="px-2 py-0.5 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                          {attachment.project_id}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div className="flex items-start gap-3">
          <Mail className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-900 mb-2">How to Use</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Send files as email attachments to the configured address</li>
              <li>• Include project ID in subject (e.g., &quot;Invoice - Project Q4_2024&quot;)</li>
              <li>• Supported: PDF, Excel, CSV, Images</li>
              <li>• Files are automatically processed</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
