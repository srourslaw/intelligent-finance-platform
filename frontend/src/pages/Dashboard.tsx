import { useState, useEffect } from 'react';
import { DollarSign, TrendingDown, TrendingUp, AlertTriangle, Calendar, CheckCircle2, LogOut, ArrowLeft } from 'lucide-react';
import { KPICard } from '../components/dashboard/KPICard';
import { BudgetTreemap } from '../components/dashboard/BudgetTreemap';
import { DocumentViewer } from '../components/dashboard/DocumentViewer';
import { useAuth } from '../contexts/AuthContext';
import { getDashboardData } from '../services/api';
import { useNavigate } from 'react-router-dom';

export function Dashboard() {
  const { token, logout, user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [selectedProjectId, setSelectedProjectId] = useState<string>('');

  useEffect(() => {
    // Get selected project from localStorage
    const projectId = localStorage.getItem('selectedProjectId');
    if (!projectId) {
      // No project selected, redirect to projects page
      navigate('/projects');
      return;
    }
    setSelectedProjectId(projectId);
  }, [navigate]);

  useEffect(() => {
    const fetchData = async () => {
      if (!token || !selectedProjectId) {
        return;
      }

      try {
        setLoading(true);
        const response = await getDashboardData(token, selectedProjectId);

        if (response.error) {
          setError(response.error);
        } else if (response.data) {
          setDashboardData(response.data);
        }
      } catch (err) {
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [token, selectedProjectId]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-16 h-16 text-red-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!dashboardData || !dashboardData.kpis) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">No data available</p>
        </div>
      </div>
    );
  }

  const kpis = dashboardData.kpis;
  const projectData = {
    name: kpis.project_name || 'Project A - 123 Sunset Boulevard',
    contractValue: kpis.total_contract_value || 0,
    totalCosts: kpis.total_costs_to_date || 0,
    forecastCost: kpis.forecast_final_cost || 0,
    percentComplete: kpis.percent_complete || 0,
    daysBehind: kpis.days_behind_schedule || 0,
  };

  // Calculated values
  const projectedProfit = projectData.contractValue - projectData.forecastCost;
  const isProfitable = projectedProfit >= 0;
  const profitPercentage = ((projectedProfit / projectData.contractValue) * 100).toFixed(1);

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Executive Dashboard</h1>
              <p className="text-sm text-gray-600 mt-1">Real-time project financial overview</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-600">Welcome, {user?.full_name || 'User'}</p>
                <p className="text-sm font-bold text-gray-900">{projectData.name}</p>
              </div>
              <button
                onClick={() => navigate('/projects')}
                className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                Projects
              </button>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Alert Banner (if project is behind or over budget) */}
        {(!isProfitable || projectData.daysBehind > 0) && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r-lg">
            <div className="flex items-start">
              <AlertTriangle className="w-5 h-5 text-red-600 mr-3 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-red-800">Project Alerts</h3>
                <div className="text-sm text-red-700 mt-1">
                  {!isProfitable && (
                    <p>• Project is forecasted to be over budget by {formatCurrency(Math.abs(projectedProfit))}</p>
                  )}
                  {projectData.daysBehind > 0 && (
                    <p>• Project is {projectData.daysBehind} days behind schedule</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* KPI Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Total Project Value */}
          <KPICard
            title="Total Project Value"
            value={formatCurrency(projectData.contractValue)}
            subtitle="Contract amount"
            icon={DollarSign}
            trend="neutral"
          />

          {/* Total Costs to Date */}
          <KPICard
            title="Total Costs to Date"
            value={formatCurrency(projectData.totalCosts)}
            subtitle={`${((projectData.totalCosts / projectData.contractValue) * 100).toFixed(1)}% of contract value`}
            icon={TrendingDown}
            trend="neutral"
          />

          {/* Forecast Final Cost */}
          <KPICard
            title="Forecast Final Cost"
            value={formatCurrency(projectData.forecastCost)}
            subtitle={projectData.forecastCost > projectData.contractValue ? 'Over budget' : 'Within budget'}
            icon={TrendingUp}
            trend={projectData.forecastCost > projectData.contractValue ? 'negative' : 'positive'}
          />

          {/* Projected Profit */}
          <KPICard
            title="Projected Profit"
            value={formatCurrency(projectedProfit)}
            subtitle={`${profitPercentage}% margin ${isProfitable ? '' : '(LOSS)'}`}
            icon={isProfitable ? TrendingUp : AlertTriangle}
            trend={isProfitable ? 'positive' : 'negative'}
          />

          {/* % Complete */}
          <KPICard
            title="Project Completion"
            value={`${projectData.percentComplete}%`}
            icon={CheckCircle2}
            trend="neutral"
            percentage={projectData.percentComplete}
            showProgressBar
          />

          {/* Days Behind/Ahead Schedule */}
          <KPICard
            title="Schedule Status"
            value={projectData.daysBehind > 0 ? `${projectData.daysBehind} days` : 'On Track'}
            subtitle={projectData.daysBehind > 0 ? 'Behind schedule' : 'Meeting deadlines'}
            icon={Calendar}
            trend={projectData.daysBehind > 0 ? 'negative' : 'positive'}
          />
        </div>

        {/* Budget Treemap Visualization */}
        <BudgetTreemap projectId={selectedProjectId} />

        {/* Document Viewer */}
        <DocumentViewer projectId={selectedProjectId} />

        {/* Additional Info Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Financial Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-3">Budget Breakdown</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Original Contract:</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(projectData.contractValue)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Spent to Date:</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(projectData.totalCosts)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Forecast Remaining:</span>
                  <span className="font-semibold text-gray-900">
                    {formatCurrency(projectData.forecastCost - projectData.totalCosts)}
                  </span>
                </div>
                <div className="border-t pt-2 mt-2">
                  <div className="flex justify-between text-sm font-bold">
                    <span className={isProfitable ? 'text-green-600' : 'text-red-600'}>
                      Projected {isProfitable ? 'Profit' : 'Loss'}:
                    </span>
                    <span className={isProfitable ? 'text-green-600' : 'text-red-600'}>
                      {formatCurrency(Math.abs(projectedProfit))}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-3">Project Status</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Completion:</span>
                  <span className="font-semibold text-gray-900">{projectData.percentComplete}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Schedule Status:</span>
                  <span className={`font-semibold ${projectData.daysBehind > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    {projectData.daysBehind > 0 ? `${projectData.daysBehind} days behind` : 'On schedule'}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Budget Status:</span>
                  <span className={`font-semibold ${isProfitable ? 'text-green-600' : 'text-red-600'}`}>
                    {isProfitable ? 'Within budget' : 'Over budget'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
