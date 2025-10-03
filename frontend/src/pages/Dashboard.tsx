import { useState, useEffect } from 'react';
import {
  DollarSign, TrendingDown, TrendingUp, AlertTriangle, LogOut, ArrowLeft,
  Activity, Target, Clock, Briefcase, PieChart as PieChartIcon, BarChart3, FileText
} from 'lucide-react';
import { BudgetTreemap } from '../components/dashboard/BudgetTreemap';
import { DocumentViewer } from '../components/dashboard/DocumentViewer';
import { FinancialStatements } from '../components/dashboard/FinancialStatements';
import { useAuth } from '../contexts/AuthContext';
import { getDashboardData } from '../services/api';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  PieChart, Pie, Cell, RadarChart, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';

export function Dashboard() {
  const { token, logout, user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [selectedProjectId, setSelectedProjectId] = useState<string>('');

  useEffect(() => {
    const projectId = localStorage.getItem('selectedProjectId');
    if (!projectId) {
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
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-20 w-20 border-b-4 border-blue-600 mx-auto mb-4"></div>
            <div className="absolute inset-0 rounded-full h-20 w-20 border-t-4 border-blue-300 animate-pulse mx-auto"></div>
          </div>
          <p className="text-gray-700 font-medium">Loading Executive Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center bg-white p-8 rounded-xl shadow-2xl">
          <AlertTriangle className="w-20 h-20 text-red-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!dashboardData || !dashboardData.kpis) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center bg-white p-8 rounded-xl shadow-2xl">
          <p className="text-gray-600">No data available</p>
        </div>
      </div>
    );
  }

  const kpis = dashboardData.kpis;
  const budgetSummary = dashboardData.budget_summary;

  const projectData = {
    name: kpis.project_name || 'Project A - 123 Sunset Boulevard',
    contractValue: kpis.total_contract_value || 0,
    totalCosts: kpis.total_costs_to_date || 0,
    forecastCost: kpis.forecast_final_cost || 0,
    percentComplete: kpis.percent_complete || 0,
    daysBehind: kpis.days_behind_schedule || 0,
    revenueLeakage: kpis.revenue_leakage || 0,
  };

  // Calculated values
  const projectedProfit = projectData.contractValue - projectData.forecastCost;
  const isProfitable = projectedProfit >= 0;
  const profitMargin = ((projectedProfit / projectData.contractValue) * 100).toFixed(1);
  const costToDate = ((projectData.totalCosts / projectData.contractValue) * 100).toFixed(1);
  const remainingBudget = projectData.contractValue - projectData.totalCosts;
  const burnRate = projectData.totalCosts / (projectData.percentComplete / 100);
  const forecastVariance = budgetSummary.total_variance || 0;

  // Chart data for budget categories
  const categoryChartData = budgetSummary.categories.map((cat: any) => ({
    name: cat.category,
    Budget: cat.budget,
    Actual: cat.actual,
    Forecast: cat.forecast,
    Variance: cat.variance,
    'Completion %': ((cat.actual / cat.budget) * 100).toFixed(0)
  }));

  // Budget status pie chart
  const budgetStatusData = [
    { name: 'Spent', value: budgetSummary.total_spent, color: '#EF4444' },
    { name: 'Committed', value: budgetSummary.total_committed, color: '#F59E0B' },
    { name: 'Available', value: Math.max(0, budgetSummary.total_budget - budgetSummary.total_spent - budgetSummary.total_committed), color: '#10B981' }
  ];

  // Project health radar
  const healthMetrics = [
    { metric: 'Budget Health', value: isProfitable ? 90 : 45, fullMark: 100 },
    { metric: 'Schedule', value: projectData.daysBehind === 0 ? 100 : Math.max(0, 100 - (projectData.daysBehind * 5)), fullMark: 100 },
    { metric: 'Progress', value: projectData.percentComplete, fullMark: 100 },
    { metric: 'Quality', value: 85, fullMark: 100 },
    { metric: 'Safety', value: 92, fullMark: 100 },
  ];

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100">
      {/* Enhanced Header */}
      <header className="bg-white shadow-xl border-b border-gray-200">
        <div className="max-w-[1600px] mx-auto px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-3 rounded-xl shadow-lg">
                <Briefcase className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                  Executive Dashboard
                </h1>
                <p className="text-sm text-gray-600 mt-1 flex items-center gap-2">
                  <Activity className="w-4 h-4" />
                  Real-time project intelligence & analytics
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right bg-gradient-to-br from-blue-50 to-indigo-50 px-4 py-2 rounded-lg border border-blue-200">
                <p className="text-xs font-medium text-gray-600">Project Manager</p>
                <p className="text-sm font-bold text-gray-900">{user?.full_name || 'User'}</p>
              </div>
              <button
                onClick={() => navigate('/projects')}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all"
              >
                <ArrowLeft className="w-4 h-4" />
                Projects
              </button>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          </div>

          {/* Project Info Banner */}
          <div className="mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-6 text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2">{projectData.name}</h2>
                <div className="flex items-center gap-6 text-sm">
                  <span className="flex items-center gap-2">
                    <DollarSign className="w-4 h-4" />
                    Contract Value: {formatCurrency(projectData.contractValue)}
                  </span>
                  <span className="flex items-center gap-2">
                    <Target className="w-4 h-4" />
                    {projectData.percentComplete}% Complete
                  </span>
                  <span className="flex items-center gap-2">
                    <Clock className="w-4 h-4" />
                    {projectData.daysBehind > 0 ? `${projectData.daysBehind} days behind` : 'On Schedule'}
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold">
                  {isProfitable ? '+' : ''}{formatCurrency(projectedProfit)}
                </div>
                <div className="text-sm opacity-90">Projected {isProfitable ? 'Profit' : 'Loss'}</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-[1600px] mx-auto px-6 lg:px-8 py-8 space-y-8">
        {/* Critical Alerts */}
        {(!isProfitable || projectData.daysBehind > 0 || projectData.revenueLeakage > 0) && (
          <div className="bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-500 p-6 rounded-r-xl shadow-lg">
            <div className="flex items-start">
              <AlertTriangle className="w-6 h-6 text-red-600 mr-4 mt-1" />
              <div className="flex-1">
                <h3 className="text-lg font-bold text-red-900 mb-2">⚠️ Critical Project Alerts</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
                  {!isProfitable && (
                    <div className="bg-white p-3 rounded-lg border border-red-200">
                      <p className="font-semibold text-red-800">Budget Overrun</p>
                      <p className="text-red-700">Forecast loss: {formatCurrency(Math.abs(projectedProfit))}</p>
                    </div>
                  )}
                  {projectData.daysBehind > 0 && (
                    <div className="bg-white p-3 rounded-lg border border-orange-200">
                      <p className="font-semibold text-orange-800">Schedule Delay</p>
                      <p className="text-orange-700">{projectData.daysBehind} days behind schedule</p>
                    </div>
                  )}
                  {projectData.revenueLeakage > 0 && (
                    <div className="bg-white p-3 rounded-lg border border-yellow-200">
                      <p className="font-semibold text-yellow-800">Revenue Leakage</p>
                      <p className="text-yellow-700">{formatCurrency(projectData.revenueLeakage)} at risk</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Enhanced KPI Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Contract Value */}
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-xl hover:shadow-2xl transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <DollarSign className="w-6 h-6" />
              </div>
              <div className="text-right">
                <div className="text-sm opacity-90">Contract Value</div>
                <div className="text-2xl font-bold">{formatCurrency(projectData.contractValue)}</div>
              </div>
            </div>
            <div className="text-xs opacity-75">Total project scope</div>
          </div>

          {/* Costs to Date */}
          <div className="bg-gradient-to-br from-orange-500 to-red-500 rounded-xl p-6 text-white shadow-xl hover:shadow-2xl transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <TrendingDown className="w-6 h-6" />
              </div>
              <div className="text-right">
                <div className="text-sm opacity-90">Costs to Date</div>
                <div className="text-2xl font-bold">{formatCurrency(projectData.totalCosts)}</div>
              </div>
            </div>
            <div className="text-xs opacity-75">{costToDate}% of contract value</div>
          </div>

          {/* Projected Profit/Loss */}
          <div className={`bg-gradient-to-br ${isProfitable ? 'from-green-500 to-emerald-600' : 'from-red-500 to-red-600'} rounded-xl p-6 text-white shadow-xl hover:shadow-2xl transition-all`}>
            <div className="flex items-center justify-between mb-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                {isProfitable ? <TrendingUp className="w-6 h-6" /> : <AlertTriangle className="w-6 h-6" />}
              </div>
              <div className="text-right">
                <div className="text-sm opacity-90">Projected {isProfitable ? 'Profit' : 'Loss'}</div>
                <div className="text-2xl font-bold">{formatCurrency(Math.abs(projectedProfit))}</div>
              </div>
            </div>
            <div className="text-xs opacity-75">{profitMargin}% margin</div>
          </div>

          {/* Project Progress */}
          <div className="bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl p-6 text-white shadow-xl hover:shadow-2xl transition-all">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <Activity className="w-6 h-6" />
              </div>
              <div className="text-right">
                <div className="text-sm opacity-90">Completion</div>
                <div className="text-2xl font-bold">{projectData.percentComplete}%</div>
              </div>
            </div>
            <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
              <div
                className="bg-white h-2 rounded-full transition-all"
                style={{ width: `${projectData.percentComplete}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Secondary KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="bg-white rounded-lg p-4 shadow-md border border-gray-200">
            <div className="text-sm text-gray-600 mb-1">Forecast Cost</div>
            <div className="text-xl font-bold text-gray-900">{formatCurrency(projectData.forecastCost)}</div>
            <div className={`text-xs mt-1 ${forecastVariance < 0 ? 'text-red-600' : 'text-green-600'}`}>
              Variance: {formatCurrency(forecastVariance)}
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-md border border-gray-200">
            <div className="text-sm text-gray-600 mb-1">Remaining Budget</div>
            <div className="text-xl font-bold text-gray-900">{formatCurrency(remainingBudget)}</div>
            <div className="text-xs text-gray-500 mt-1">
              {((remainingBudget / projectData.contractValue) * 100).toFixed(1)}% available
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-md border border-gray-200">
            <div className="text-sm text-gray-600 mb-1">Burn Rate</div>
            <div className="text-xl font-bold text-gray-900">{formatCurrency(burnRate)}</div>
            <div className="text-xs text-gray-500 mt-1">Per 100% completion</div>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-md border border-gray-200">
            <div className="text-sm text-gray-600 mb-1">Schedule Status</div>
            <div className={`text-xl font-bold ${projectData.daysBehind > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {projectData.daysBehind > 0 ? `${projectData.daysBehind} days` : 'On Track'}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {projectData.daysBehind > 0 ? 'Behind schedule' : 'Meeting deadlines'}
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 shadow-md border border-gray-200">
            <div className="text-sm text-gray-600 mb-1">Revenue Leakage</div>
            <div className={`text-xl font-bold ${projectData.revenueLeakage > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {formatCurrency(projectData.revenueLeakage)}
            </div>
            <div className="text-xs text-gray-500 mt-1">At risk revenue</div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Budget by Category Chart */}
          <div className="bg-white rounded-xl p-6 shadow-xl border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-600" />
              Budget Performance by Category
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={categoryChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip
                  formatter={(value) => formatCurrency(value as number)}
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                />
                <Legend />
                <Bar dataKey="Budget" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Actual" fill="#10B981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Forecast" fill="#F59E0B" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Budget Status Pie Chart */}
          <div className="bg-white rounded-xl p-6 shadow-xl border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <PieChartIcon className="w-5 h-5 text-blue-600" />
              Budget Allocation Status
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={budgetStatusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name}: ${formatCurrency(entry.value as number)}`}
                  outerRadius={120}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {budgetStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => formatCurrency(value as number)} />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 grid grid-cols-3 gap-4">
              {budgetStatusData.map((item, idx) => (
                <div key={idx} className="text-center">
                  <div className="text-xs text-gray-600">{item.name}</div>
                  <div className="text-sm font-bold" style={{ color: item.color }}>
                    {formatCurrency(item.value)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Project Health Radar & Variance Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Project Health Radar */}
          <div className="bg-white rounded-xl p-6 shadow-xl border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-600" />
              Project Health Score
            </h3>
            <ResponsiveContainer width="100%" height={350}>
              <RadarChart data={healthMetrics}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="metric" tick={{ fontSize: 12 }} />
                <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fontSize: 11 }} />
                <Radar
                  name="Health Score"
                  dataKey="value"
                  stroke="#3B82F6"
                  fill="#3B82F6"
                  fillOpacity={0.6}
                />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
            <div className="mt-4 grid grid-cols-5 gap-2">
              {healthMetrics.map((metric, idx) => (
                <div key={idx} className="text-center">
                  <div className="text-2xl font-bold" style={{ color: metric.value >= 80 ? '#10B981' : metric.value >= 60 ? '#F59E0B' : '#EF4444' }}>
                    {metric.value}
                  </div>
                  <div className="text-xs text-gray-600">{metric.metric}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Category Variance Analysis */}
          <div className="bg-white rounded-xl p-6 shadow-xl border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-600" />
              Variance Analysis by Category
            </h3>
            <div className="space-y-3 max-h-[350px] overflow-y-auto">
              {categoryChartData.map((cat: any, idx: number) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex-1">
                    <div className="font-semibold text-sm text-gray-900">{cat.name}</div>
                    <div className="text-xs text-gray-600">Budget: {formatCurrency(cat.Budget)}</div>
                  </div>
                  <div className="text-right">
                    <div className={`text-sm font-bold ${cat.Variance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {cat.Variance >= 0 ? '+' : ''}{formatCurrency(cat.Variance)}
                    </div>
                    <div className="text-xs text-gray-500">{cat['Completion %']}% complete</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Budget Treemap */}
        <BudgetTreemap projectId={selectedProjectId} />

        {/* Document Viewer */}
        <DocumentViewer projectId={selectedProjectId} />

        {/* AI-Consolidated Financial Statements */}
        <FinancialStatements projectId={selectedProjectId} />
      </main>
    </div>
  );
}
