import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { getBudgetData } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

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
          // Group by category and aggregate
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

          // Convert to array
          const categoryData: BudgetCategory[] = Array.from(categoryMap.entries()).map(([category, values]) => ({
            category,
            budget: values.budget,
            actual: values.actual,
            forecast: values.forecast,
            variance: values.variance,
            percentComplete: values.budget > 0 ? (values.actual / values.budget) * 100 : 0,
          }));

          // Sort by budget descending
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

  const totalBudget = categories.reduce((sum, cat) => sum + cat.budget, 0);
  const totalActual = categories.reduce((sum, cat) => sum + cat.actual, 0);
  const totalVariance = categories.reduce((sum, cat) => sum + cat.variance, 0);

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <DollarSign className="w-6 h-6 text-blue-600" />
          Budget Breakdown by Category
        </h2>
        <div className="h-[600px] flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <DollarSign className="w-6 h-6 text-blue-600" />
          Budget Breakdown by Category
        </h2>
        <div className="h-[600px] flex items-center justify-center">
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  if (categories.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <DollarSign className="w-6 h-6 text-blue-600" />
          Budget Breakdown by Category
        </h2>
        <div className="h-[600px] flex items-center justify-center">
          <p className="text-gray-600">No budget data available</p>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const chartData = categories.map(cat => ({
    name: cat.category,
    Budget: cat.budget,
    Actual: cat.actual,
    Variance: cat.variance,
  }));

  return (
    <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2">
          <DollarSign className="w-6 h-6 text-blue-600" />
          Budget Breakdown by Category
        </h2>
        <p className="text-sm text-gray-600">
          Detailed budget allocation, spending, and variance analysis across all project categories
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-700 font-medium">Total Budget</p>
              <p className="text-2xl font-bold text-blue-900">{formatCurrency(totalBudget)}</p>
            </div>
            <div className="bg-blue-500 p-3 rounded-lg">
              <DollarSign className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-700 font-medium">Total Spent</p>
              <p className="text-2xl font-bold text-green-900">{formatCurrency(totalActual)}</p>
            </div>
            <div className="bg-green-500 p-3 rounded-lg">
              <TrendingDown className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        <div className={`bg-gradient-to-br ${totalVariance >= 0 ? 'from-green-50 to-emerald-100 border-green-200' : 'from-red-50 to-red-100 border-red-200'} rounded-lg p-4 border`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-sm font-medium ${totalVariance >= 0 ? 'text-green-700' : 'text-red-700'}`}>
                Total Variance
              </p>
              <p className={`text-2xl font-bold ${totalVariance >= 0 ? 'text-green-900' : 'text-red-900'}`}>
                {formatCurrency(Math.abs(totalVariance))}
              </p>
            </div>
            <div className={`${totalVariance >= 0 ? 'bg-green-500' : 'bg-red-500'} p-3 rounded-lg`}>
              {totalVariance >= 0 ? (
                <TrendingUp className="w-6 h-6 text-white" />
              ) : (
                <TrendingDown className="w-6 h-6 text-white" />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Budget vs Actual Chart */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Budget vs Actual Spending</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" angle={-45} textAnchor="end" height={120} tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip
              formatter={(value) => formatCurrency(value as number)}
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
            />
            <Bar dataKey="Budget" fill="#3B82F6" radius={[8, 8, 0, 0]} />
            <Bar dataKey="Actual" fill="#10B981" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Category Details Grid */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Category Performance Details</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {categories.map((cat, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-r from-gray-50 to-white rounded-lg p-5 border border-gray-200 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-gray-900">{cat.category}</h4>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    cat.variance >= 0
                      ? 'bg-green-100 text-green-700'
                      : 'bg-red-100 text-red-700'
                  }`}
                >
                  {cat.variance >= 0 ? 'Under Budget' : 'Over Budget'}
                </span>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Budget:</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(cat.budget)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Actual Spent:</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(cat.actual)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Variance:</span>
                  <span className={`font-semibold ${cat.variance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {cat.variance >= 0 ? '+' : ''}{formatCurrency(cat.variance)}
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div>
                <div className="flex justify-between text-xs text-gray-600 mb-1">
                  <span>Completion</span>
                  <span className="font-semibold">{cat.percentComplete.toFixed(0)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all ${
                      cat.percentComplete > 100
                        ? 'bg-gradient-to-r from-red-500 to-red-600'
                        : cat.percentComplete > 80
                        ? 'bg-gradient-to-r from-blue-500 to-blue-600'
                        : 'bg-gradient-to-r from-green-500 to-green-600'
                    }`}
                    style={{ width: `${Math.min(cat.percentComplete, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Summary */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <p className="text-sm text-gray-700 mb-1">Budget Utilization</p>
              <p className="text-3xl font-bold text-blue-900">
                {((totalActual / totalBudget) * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-gray-600 mt-1">Of total budget spent</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-700 mb-1">Variance Rate</p>
              <p className={`text-3xl font-bold ${totalVariance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {((totalVariance / totalBudget) * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-gray-600 mt-1">
                {totalVariance >= 0 ? 'Under' : 'Over'} budget overall
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-700 mb-1">Remaining Budget</p>
              <p className="text-3xl font-bold text-indigo-900">
                {formatCurrency(totalBudget - totalActual)}
              </p>
              <p className="text-xs text-gray-600 mt-1">Available to spend</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
