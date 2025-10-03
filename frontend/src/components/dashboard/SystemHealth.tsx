import { useState, useEffect } from 'react';
import { Activity, Server, Cpu, HardDrive, Database, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface SystemHealth {
  status: string;
  timestamp: string;
  environment: string;
  services: Record<string, any>;
  system_resources: {
    cpu: { percent: number; count: number };
    memory: { total_gb: number; available_gb: number; percent: number };
    disk: { total_gb: number; used_gb: number; free_gb: number; percent: number };
  };
  platform: {
    system: string;
    release: string;
    python_version: string;
  };
}

export function SystemHealth() {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(() => {
      fetchHealth();
    }, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/system/health`);
      setHealth(response.data);
      setLastUpdate(new Date());
    } catch (err) {
      console.error('Error fetching system health:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'healthy':
      case 'running':
      case 'configured':
        return 'text-green-600 bg-green-100';
      case 'degraded':
      case 'not_configured':
        return 'text-yellow-600 bg-yellow-100';
      case 'error':
      case 'stopped':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'healthy':
      case 'running':
      case 'configured':
        return <CheckCircle className="w-5 h-5" />;
      case 'degraded':
      case 'not_configured':
        return <AlertCircle className="w-5 h-5" />;
      default:
        return <AlertCircle className="w-5 h-5" />;
    }
  };

  const getResourceStatus = (percent: number) => {
    if (percent < 60) return 'text-green-600';
    if (percent < 80) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!health) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="text-center text-gray-500">
          <AlertCircle className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>Unable to load system health</p>
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
              <Activity className="w-6 h-6 text-blue-600" />
              System Health
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              Real-time system status and resource monitoring
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${getStatusColor(health.status)}`}>
              {getStatusIcon(health.status)}
              <span className="font-medium capitalize">{health.status}</span>
            </div>
            <div className="text-sm text-gray-500 flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {lastUpdate.toLocaleTimeString()}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-600 mb-1">Environment</div>
            <div className="text-xl font-bold text-gray-900 capitalize">{health.environment}</div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-600 mb-1">Platform</div>
            <div className="text-xl font-bold text-gray-900">{health.platform.system}</div>
            <div className="text-xs text-gray-500">{health.platform.python_version}</div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-600 mb-1">Last Updated</div>
            <div className="text-xl font-bold text-gray-900">{new Date(health.timestamp).toLocaleTimeString()}</div>
          </div>
        </div>

        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Server className="w-5 h-5 text-blue-600" />
            Services Status
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(health.services).map(([name, service]: [string, any]) => (
              <div key={name} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-900 capitalize">
                    {name.replace(/_/g, ' ')}
                  </span>
                  <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs ${getStatusColor(service.status)}`}>
                    {getStatusIcon(service.status)}
                    <span className="capitalize">{service.status}</span>
                  </div>
                </div>
                {service.job_count !== undefined && (
                  <div className="text-sm text-gray-600">Jobs: {service.job_count}</div>
                )}
                {service.statistics && (
                  <div className="text-sm text-gray-600">
                    Total: {service.statistics.total_processed || service.statistics.total_events || 0}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Database className="w-5 h-5 text-blue-600" />
          System Resources
        </h3>

        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 text-gray-600" />
                <span className="font-medium text-gray-900">CPU Usage</span>
              </div>
              <span className={`font-bold ${getResourceStatus(health.system_resources.cpu.percent)}`}>
                {health.system_resources.cpu.percent.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${
                  health.system_resources.cpu.percent < 60
                    ? 'bg-green-500'
                    : health.system_resources.cpu.percent < 80
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${health.system_resources.cpu.percent}%` }}
              ></div>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {health.system_resources.cpu.count} cores
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Server className="w-5 h-5 text-gray-600" />
                <span className="font-medium text-gray-900">Memory Usage</span>
              </div>
              <span className={`font-bold ${getResourceStatus(health.system_resources.memory.percent)}`}>
                {health.system_resources.memory.percent.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${
                  health.system_resources.memory.percent < 60
                    ? 'bg-green-500'
                    : health.system_resources.memory.percent < 80
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${health.system_resources.memory.percent}%` }}
              ></div>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {health.system_resources.memory.available_gb.toFixed(1)} GB available of{' '}
              {health.system_resources.memory.total_gb.toFixed(1)} GB
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <HardDrive className="w-5 h-5 text-gray-600" />
                <span className="font-medium text-gray-900">Disk Usage</span>
              </div>
              <span className={`font-bold ${getResourceStatus(health.system_resources.disk.percent)}`}>
                {health.system_resources.disk.percent.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${
                  health.system_resources.disk.percent < 60
                    ? 'bg-green-500'
                    : health.system_resources.disk.percent < 80
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${health.system_resources.disk.percent}%` }}
              ></div>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {health.system_resources.disk.free_gb.toFixed(1)} GB free of{' '}
              {health.system_resources.disk.total_gb.toFixed(1)} GB
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
