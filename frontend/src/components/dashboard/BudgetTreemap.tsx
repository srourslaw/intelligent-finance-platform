import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, LineChart, Line, Legend, ComposedChart, Area } from 'recharts';
import { getBudgetData } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { TrendingUp, TrendingDown, DollarSign, AlertTriangle, Target, Zap, Shield, TrendingUpIcon, Activity, Eye } from 'lucide-react';

interface BudgetCategory {
  category: string;
  budget: number;
  actual: number;
  forecast: number;
  variance: number;
  percentComplete: number;
}

interface BudgetTreemapProps {
  projectId: string;
}

export function BudgetTreemap({ projectId }: BudgetTreemapProps) {
  const { token } = useAuth();
  const [categories, setCategories] = useState<BudgetCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBudgetData = async () => {
      if (!token || !projectId) return;

      try {
        setLoading(true);
        const response = await getBudgetData(token, projectId);

        if (response.error) {
          setError(response.error);
          return;
        }

        const items = response.data?.items || [];

        if (items.length > 0) {
          const categoryMap = new Map<string, { budget: number; actual: number; forecast: number; variance: number }>();

          items.forEach((item: any) => {
            const category = item.category || 'Other';
            const existing = categoryMap.get(category) || { budget: 0, actual: 0, forecast: 0, variance: 0 };

            categoryMap.set(category, {
              budget: existing.budget + (item.budget || 0),
              actual: existing.actual + (item.actual_spent || 0),
              forecast: existing.forecast + (item.forecast || 0),
              variance: existing.variance + (item.variance || 0),
            });
          });

          const categoryData: BudgetCategory[] = Array.from(categoryMap.entries()).map(([category, values]) => ({
            category,
            budget: values.budget,
            actual: values.actual,
            forecast: values.forecast,
            variance: values.variance,
            percentComplete: values.budget > 0 ? (values.actual / values.budget) * 100 : 0,
          }));

          categoryData.sort((a, b) => b.budget - a.budget);
          setCategories(categoryData);
        }
      } catch (err) {
        setError('Failed to load budget data');
      } finally {
        setLoading(false);
      }
    };

    fetchBudgetData();
  }, [token, projectId]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatCompact = (value: number) => {
    if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
    return formatCurrency(value);
  };

  const totalBudget = categories.reduce((sum, cat) => sum + cat.budget, 0);
  const totalActual = categories.reduce((sum, cat) => sum + cat.actual, 0);
  const totalForecast = categories.reduce((sum, cat) => sum + cat.forecast, 0);
  const totalVariance = categories.reduce((sum, cat) => sum + cat.variance, 0);
  const remainingBudget = totalBudget - totalActual;
  const budgetUtilization = (totalActual / totalBudget) * 100;
  const forecastOverrun = totalForecast - totalBudget;
  const costPerformanceIndex = totalBudget / totalForecast; // CPI
  const schedulePerformanceIndex = 0.87; // Mock - you can calculate from actual project data

  // Risk categories
  const highRiskCategories = categories.filter(c => c.variance < -5000 || c.percentComplete > 110);
  const mediumRiskCategories = categories.filter(c => (c.variance < -1000 && c.variance >= -5000) || (c.percentComplete > 100 && c.percentComplete <= 110));
  const lowRiskCategories = categories.filter(c => c.variance >= -1000 && c.percentComplete <= 100);

  // Budget burn rate
  const avgBurnRate = totalActual / Math.max(...categories.map(c => c.percentComplete / 100));

  // Top spending categories
  const topSpending = [...categories].sort((a, b) => b.actual - a.actual).slice(0, 3);

  // Most at-risk categories
  const atRiskCategories = [...categories].sort((a, b) => a.variance - b.variance).slice(0, 3);

  // Trend data for forecast vs actual
  const trendData = categories.map(cat => ({
    name: cat.category.substring(0, 8),
    Budget: cat.budget,
    Actual: cat.actual,
    Forecast: cat.forecast,
  }));

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Activity className="w-6 h-6 text-blue-600" />
          Budget & Cost Analytics
        </h2>
        <div className="h-[800px] flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (error || categories.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Activity className="w-6 h-6 text-blue-600" />
          Budget & Cost Analytics
        </h2>
        <div className="h-[800px] flex items-center justify-center">
          <p className="text-gray-600">{error || 'No budget data available'}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-2xl p-8 border border-gray-200">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
          <Activity className="w-8 h-8 text-blue-600" />
          Budget & Cost Analytics
        </h2>
        <p className="text-sm text-gray-600">
          Executive-level financial performance, risk assessment, and strategic insights
        </p>
      </div>

      {/* Executive KPI Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Budget Utilization */}
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white bg-opacity-20 p-3 rounded-lg">
              <Target className="w-6 h-6" />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90">Budget Utilization</p>
              <p className="text-3xl font-bold">{budgetUtilization.toFixed(1)}%</p>
            </div>
          </div>
          <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
            <div
              className="bg-white h-2 rounded-full transition-all"
              style={{ width: `${Math.min(budgetUtilization, 100)}%` }}
            ></div>
          </div>
          <p className="text-xs opacity-75 mt-2">
            {formatCurrency(totalActual)} of {formatCurrency(totalBudget)} spent
          </p>
        </div>

        {/* Cost Performance Index (CPI) */}
        <div className={`bg-gradient-to-br ${costPerformanceIndex >= 1 ? 'from-green-500 to-emerald-600' : 'from-red-500 to-red-600'} rounded-xl p-6 text-white shadow-lg`}>
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white bg-opacity-20 p-3 rounded-lg">
              <Zap className="w-6 h-6" />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90">Cost Performance (CPI)</p>
              <p className="text-3xl font-bold">{costPerformanceIndex.toFixed(2)}</p>
            </div>
          </div>
          <p className="text-xs opacity-75">
            {costPerformanceIndex >= 1 ? '✓ Under budget efficiency' : '⚠ Over budget - action needed'}
          </p>
          <p className="text-xs opacity-90 mt-1">
            Target: &gt;1.0 (Current: {costPerformanceIndex >= 1 ? 'Good' : 'Poor'})
          </p>
        </div>

        {/* Forecast at Completion */}
        <div className={`bg-gradient-to-br ${forecastOverrun <= 0 ? 'from-green-500 to-green-600' : 'from-orange-500 to-red-500'} rounded-xl p-6 text-white shadow-lg`}>
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white bg-opacity-20 p-3 rounded-lg">
              <TrendingUpIcon className="w-6 h-6" />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90">Forecast at Completion</p>
              <p className="text-2xl font-bold">{formatCompact(totalForecast)}</p>
            </div>
          </div>
          <p className="text-xs opacity-75">
            {forecastOverrun > 0 ? `Overrun: ${formatCurrency(forecastOverrun)}` : `Underrun: ${formatCurrency(Math.abs(forecastOverrun))}`}
          </p>
          <p className="text-xs opacity-90 mt-1">
            Budget: {formatCurrency(totalBudget)}
          </p>
        </div>

        {/* Risk Score */}
        <div className={`bg-gradient-to-br ${highRiskCategories.length === 0 ? 'from-green-500 to-green-600' : highRiskCategories.length <= 2 ? 'from-yellow-500 to-orange-500' : 'from-red-500 to-red-600'} rounded-xl p-6 text-white shadow-lg`}>
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white bg-opacity-20 p-3 rounded-lg">
              <Shield className="w-6 h-6" />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90">Budget Risk Level</p>
              <p className="text-3xl font-bold">
                {highRiskCategories.length === 0 ? 'LOW' : highRiskCategories.length <= 2 ? 'MED' : 'HIGH'}
              </p>
            </div>
          </div>
          <p className="text-xs opacity-75">
            {highRiskCategories.length} high risk | {mediumRiskCategories.length} medium | {lowRiskCategories.length} low
          </p>
          <p className="text-xs opacity-90 mt-1">
            Categories requiring attention
          </p>
        </div>
      </div>

      {/* Strategic Insights - Alert Cards */}
      {(highRiskCategories.length > 0 || forecastOverrun > 0) && (
        <div className="bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-500 rounded-r-xl p-6 mb-8">
          <div className="flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-red-600 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h3 className="text-lg font-bold text-red-900 mb-3">⚠️ Executive Alerts - Immediate Action Required</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {forecastOverrun > 0 && (
                  <div className="bg-white p-4 rounded-lg border border-red-200">
                    <p className="font-semibold text-red-800 mb-1">Budget Overrun Forecast</p>
                    <p className="text-sm text-red-700">Projected overrun: {formatCurrency(forecastOverrun)}</p>
                    <p className="text-xs text-gray-600 mt-2">
                      💡 Recommendation: Review cost controls and consider scope adjustments
                    </p>
                  </div>
                )}
                {highRiskCategories.slice(0, 3).map((cat, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-lg border border-orange-200">
                    <p className="font-semibold text-orange-800 mb-1">{cat.category} - Critical Risk</p>
                    <p className="text-sm text-orange-700">Variance: {formatCurrency(cat.variance)}</p>
                    <p className="text-xs text-gray-600 mt-2">
                      💡 {cat.percentComplete > 110 ? 'Severe cost overrun detected' : 'Trending over budget'}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Key Performance Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Top Spending Categories */}
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-blue-600" />
            Top Spending Categories
          </h3>
          <div className="space-y-3">
            {topSpending.map((cat, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-white rounded-lg border border-blue-100">
                <div className="flex items-center gap-3">
                  <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">
                    {idx + 1}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{cat.category}</p>
                    <p className="text-xs text-gray-600">{((cat.actual / totalActual) * 100).toFixed(1)}% of total</p>
                  </div>
                </div>
                <p className="font-bold text-blue-900">{formatCompact(cat.actual)}</p>
              </div>
            ))}
          </div>
        </div>

        {/* At-Risk Categories */}
        <div className="bg-gradient-to-br from-red-50 to-orange-50 rounded-xl p-6 border border-red-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-600" />
            Highest Risk Categories
          </h3>
          <div className="space-y-3">
            {atRiskCategories.map((cat, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-white rounded-lg border border-red-100">
                <div className="flex items-center gap-3">
                  <div className="bg-red-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">
                    !
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{cat.category}</p>
                    <p className="text-xs text-gray-600">{cat.percentComplete.toFixed(0)}% complete</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold text-red-600">{formatCurrency(Math.abs(cat.variance))}</p>
                  <p className="text-xs text-red-500">over</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Financial Health Score */}
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Eye className="w-5 h-5 text-green-600" />
            Financial Health Indicators
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Budget Adherence</span>
                <span className="text-sm font-bold text-gray-900">
                  {((lowRiskCategories.length / categories.length) * 100).toFixed(0)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${(lowRiskCategories.length / categories.length) * 100}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Cost Efficiency</span>
                <span className="text-sm font-bold text-gray-900">
                  {(costPerformanceIndex * 100).toFixed(0)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${costPerformanceIndex >= 1 ? 'bg-green-500' : 'bg-red-500'}`}
                  style={{ width: `${Math.min((costPerformanceIndex * 100), 100)}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Remaining Runway</span>
                <span className="text-sm font-bold text-gray-900">
                  {((remainingBudget / totalBudget) * 100).toFixed(0)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full"
                  style={{ width: `${(remainingBudget / totalBudget) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Advanced Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Budget vs Actual vs Forecast */}
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Budget vs Actual vs Forecast Analysis</h3>
          <ResponsiveContainer width="100%" height={350}>
            <ComposedChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 11 }} tickFormatter={(value) => formatCompact(value)} />
              <Tooltip
                formatter={(value) => formatCurrency(value as number)}
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Legend />
              <Bar dataKey="Budget" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Actual" fill="#10B981" radius={[4, 4, 0, 0]} />
              <Line type="monotone" dataKey="Forecast" stroke="#F59E0B" strokeWidth={3} dot={{ r: 4 }} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* Variance Trend */}
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Variance Trend by Category</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={categories.map(c => ({ name: c.category.substring(0, 10), variance: c.variance }))}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 11 }} tickFormatter={(value) => formatCompact(value)} />
              <Tooltip
                formatter={(value) => formatCurrency(value as number)}
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Bar dataKey="variance" radius={[4, 4, 0, 0]}>
                {categories.map((cat, index) => (
                  <Cell key={`cell-${index}`} fill={cat.variance >= 0 ? '#10B981' : '#EF4444'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Category Breakdown */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Detailed Category Breakdown</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Budget</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actual</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Forecast</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Variance</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">% Complete</th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {categories.map((cat, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="font-semibold text-gray-900">{cat.category}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                    {formatCurrency(cat.budget)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium text-gray-900">
                    {formatCurrency(cat.actual)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-700">
                    {formatCurrency(cat.forecast)}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-right text-sm font-bold ${cat.variance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {cat.variance >= 0 ? '+' : ''}{formatCurrency(cat.variance)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <span className={`font-semibold ${cat.percentComplete > 100 ? 'text-red-600' : 'text-gray-900'}`}>
                      {cat.percentComplete.toFixed(1)}%
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-center">
                    <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      cat.variance < -5000 || cat.percentComplete > 110
                        ? 'bg-red-100 text-red-800'
                        : cat.variance < -1000 || cat.percentComplete > 100
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {cat.variance < -5000 || cat.percentComplete > 110 ? 'High Risk' : cat.variance < -1000 || cat.percentComplete > 100 ? 'Medium Risk' : 'On Track'}
                    </span>
                  </td>
                </tr>
              ))}
              <tr className="bg-gray-100 font-bold">
                <td className="px-6 py-4 whitespace-nowrap text-gray-900">TOTAL</td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-gray-900">{formatCurrency(totalBudget)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-gray-900">{formatCurrency(totalActual)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-gray-900">{formatCurrency(totalForecast)}</td>
                <td className={`px-6 py-4 whitespace-nowrap text-right ${totalVariance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {totalVariance >= 0 ? '+' : ''}{formatCurrency(totalVariance)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-gray-900">
                  {budgetUtilization.toFixed(1)}%
                </td>
                <td className="px-6 py-4"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Executive Summary */}
      <div className="bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 rounded-xl p-6 border border-blue-200">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Target className="w-6 h-6 text-blue-600" />
          Executive Summary & Recommendations
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">📊 Financial Position</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>✓ Total Budget: {formatCurrency(totalBudget)}</li>
              <li>✓ Current Spend: {formatCurrency(totalActual)} ({budgetUtilization.toFixed(1)}% utilized)</li>
              <li>✓ Forecast at Completion: {formatCurrency(totalForecast)}</li>
              <li className={totalVariance >= 0 ? 'text-green-700' : 'text-red-700'}>
                ● Overall Variance: {formatCurrency(totalVariance)} ({((totalVariance / totalBudget) * 100).toFixed(1)}%)
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">💡 Strategic Recommendations</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              {forecastOverrun > 0 && (
                <li>⚠️ Implement immediate cost controls to mitigate {formatCurrency(forecastOverrun)} overrun</li>
              )}
              {highRiskCategories.length > 0 && (
                <li>🔍 Conduct deep-dive review of {highRiskCategories.length} high-risk categories</li>
              )}
              {costPerformanceIndex < 1 && (
                <li>📉 Improve cost efficiency - Current CPI: {costPerformanceIndex.toFixed(2)} (Target: &gt;1.0)</li>
              )}
              {remainingBudget < totalBudget * 0.2 && (
                <li>⏰ Budget runway critical - Only {((remainingBudget / totalBudget) * 100).toFixed(0)}% remaining</li>
              )}
              <li>✅ Maintain strong oversight of top 3 spending categories</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
