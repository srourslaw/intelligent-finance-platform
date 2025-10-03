import { useState, useEffect } from 'react';
import { Cloud, Activity, Link, CheckCircle, XCircle, BarChart3 } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface WebhookEvent {
  timestamp: string;
  provider: string;
  event_type: string;
  data: any;
}

interface WebhookStatistics {
  total_events: number;
  by_provider: Record<string, number>;
  by_event_type: Record<string, number>;
}

interface WebhookHealth {
  status: string;
  service: string;
  configured_providers: {
    dropbox: boolean;
    google_drive: boolean;
    onedrive: boolean;
  };
}

export function CloudWebhooks() {
  const { token } = useAuth();
  const [health, setHealth] = useState<WebhookHealth | null>(null);
  const [statistics, setStatistics] = useState<WebhookStatistics | null>(null);
  const [recentEvents, setRecentEvents] = useState<WebhookEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHealth();
    fetchStatistics();
    fetchEvents();
  }, []);

  const fetchHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/webhooks/health`);
      setHealth(response.data);
    } catch (err) {
      console.error('Error fetching webhook health:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/webhooks/statistics`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStatistics(response.data);
    } catch (err) {
      console.log('Webhook statistics not available');
    }
  };

  const fetchEvents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/webhooks/events?limit=10`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRecentEvents(response.data);
    } catch (err) {
      console.log('Webhook events not available');
    }
  };

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case 'dropbox':
        return '📦';
      case 'google_drive':
        return '📁';
      case 'onedrive':
        return '☁️';
      default:
        return '🔗';
    }
  };

  const getProviderName = (provider: string) => {
    switch (provider) {
      case 'dropbox':
        return 'Dropbox';
      case 'google_drive':
        return 'Google Drive';
      case 'onedrive':
        return 'OneDrive';
      default:
        return provider;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
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
      {/* Header & Status */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2 mb-4">
            <Cloud className="w-6 h-6 text-blue-600" />
            ☁️ Cloud Storage Webhooks
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            Automatic file synchronization from Dropbox, Google Drive, and OneDrive
          </p>
        </div>

        {/* Provider Status */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Dropbox */}
          <div className={`p-4 rounded-lg border ${
            health?.configured_providers.dropbox
              ? 'bg-green-50 border-green-200'
              : 'bg-gray-50 border-gray-200'
          }`}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl">📦</span>
                <span className="font-bold text-gray-900">Dropbox</span>
              </div>
              {health?.configured_providers.dropbox ? (
                <CheckCircle className="w-5 h-5 text-green-600" />
              ) : (
                <XCircle className="w-5 h-5 text-gray-400" />
              )}
            </div>
            <p className="text-xs text-gray-600">
              {health?.configured_providers.dropbox ? 'Connected' : 'Not configured'}
            </p>
            {statistics?.by_provider.dropbox && (
              <p className="text-sm font-bold text-green-600 mt-1">
                {statistics.by_provider.dropbox} events
              </p>
            )}
          </div>

          {/* Google Drive */}
          <div className={`p-4 rounded-lg border ${
            health?.configured_providers.google_drive
              ? 'bg-green-50 border-green-200'
              : 'bg-gray-50 border-gray-200'
          }`}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl">📁</span>
                <span className="font-bold text-gray-900">Google Drive</span>
              </div>
              {health?.configured_providers.google_drive ? (
                <CheckCircle className="w-5 h-5 text-green-600" />
              ) : (
                <XCircle className="w-5 h-5 text-gray-400" />
              )}
            </div>
            <p className="text-xs text-gray-600">
              {health?.configured_providers.google_drive ? 'Connected' : 'Not configured'}
            </p>
            {statistics?.by_provider.google_drive && (
              <p className="text-sm font-bold text-green-600 mt-1">
                {statistics.by_provider.google_drive} events
              </p>
            )}
          </div>

          {/* OneDrive */}
          <div className={`p-4 rounded-lg border ${
            health?.configured_providers.onedrive
              ? 'bg-green-50 border-green-200'
              : 'bg-gray-50 border-gray-200'
          }`}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl">☁️</span>
                <span className="font-bold text-gray-900">OneDrive</span>
              </div>
              {health?.configured_providers.onedrive ? (
                <CheckCircle className="w-5 h-5 text-green-600" />
              ) : (
                <XCircle className="w-5 h-5 text-gray-400" />
              )}
            </div>
            <p className="text-xs text-gray-600">
              {health?.configured_providers.onedrive ? 'Connected' : 'Not configured'}
            </p>
            {statistics?.by_provider.onedrive && (
              <p className="text-sm font-bold text-green-600 mt-1">
                {statistics.by_provider.onedrive} events
              </p>
            )}
          </div>
        </div>

        {/* Overall Statistics */}
        {statistics && statistics.total_events > 0 && (
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <BarChart3 className="w-5 h-5 text-blue-600" />
              <span className="font-bold text-blue-900">Total Events: {statistics.total_events}</span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
              {Object.entries(statistics.by_event_type).map(([type, count]) => (
                <div key={type} className="bg-white p-2 rounded">
                  <div className="font-medium text-gray-900">{type}</div>
                  <div className="text-blue-600">{count}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Recent Events */}
      {recentEvents.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-600" />
              Recent Webhook Events
            </h3>
          </div>

          <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
            {recentEvents.map((event, idx) => (
              <div key={idx} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <div className="text-2xl">{getProviderIcon(event.provider)}</div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-gray-900">{getProviderName(event.provider)}</span>
                        <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                          {event.event_type}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">{formatTimestamp(event.timestamp)}</p>
                      {event.data && Object.keys(event.data).length > 0 && (
                        <pre className="text-xs text-gray-600 mt-2 bg-gray-50 p-2 rounded overflow-x-auto">
                          {JSON.stringify(event.data, null, 2)}
                        </pre>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Setup Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div className="flex items-start gap-3">
          <Link className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-900 mb-2">Webhook Setup Instructions</h4>
            <div className="space-y-4 text-sm text-blue-800">
              <div>
                <p className="font-medium">📦 Dropbox:</p>
                <ul className="ml-4 mt-1 space-y-1">
                  <li>1. Create app at https://www.dropbox.com/developers/apps</li>
                  <li>2. Set webhook URL: https://your-domain.com/api/webhooks/dropbox</li>
                  <li>3. Set DROPBOX_WEBHOOK_SECRET environment variable</li>
                </ul>
              </div>

              <div>
                <p className="font-medium">📁 Google Drive:</p>
                <ul className="ml-4 mt-1 space-y-1">
                  <li>1. Enable Google Drive API in Google Cloud Console</li>
                  <li>2. Create watch channel for monitored folder</li>
                  <li>3. Set webhook URL: https://your-domain.com/api/webhooks/google-drive</li>
                </ul>
              </div>

              <div>
                <p className="font-medium">☁️ OneDrive:</p>
                <ul className="ml-4 mt-1 space-y-1">
                  <li>1. Register app at https://portal.azure.com</li>
                  <li>2. Create subscription for document library</li>
                  <li>3. Set webhook URL: https://your-domain.com/api/webhooks/onedrive</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
