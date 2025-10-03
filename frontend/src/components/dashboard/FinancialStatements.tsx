import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface FinancialStatementsProps {
  projectId?: string;
}

interface ConsolidatedData {
  current_assets: Record<string, number>;
  non_current_assets: Record<string, number>;
  current_liabilities: Record<string, number>;
  long_term_liabilities: Record<string, number>;
  equity: Record<string, number>;
  revenue: Record<string, number>;
  cost_of_goods_sold: Record<string, number>;
  operating_expenses: Record<string, number>;
  other_income: Record<string, number>;
  other_expenses: Record<string, number>;
}

interface Totals {
  current_assets: number;
  non_current_assets: number;
  total_assets: number;
  current_liabilities: number;
  long_term_liabilities: number;
  total_liabilities: number;
  total_equity: number;
  total_revenue: number;
  total_cogs: number;
  gross_profit: number;
  total_operating_expenses: number;
  operating_income: number;
  net_income: number;
  balance_check: number;
}

const FinancialStatements: React.FC<FinancialStatementsProps> = ({ projectId }) => {
  const [consolidatedData, setConsolidatedData] = useState<ConsolidatedData | null>(null);
  const [totals, setTotals] = useState<Totals | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'balance-sheet' | 'income-statement' | 'ratios'>('balance-sheet');

  useEffect(() => {
    fetchConsolidatedData();
  }, []);

  const fetchConsolidatedData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');

      const params = projectId ? { project_id: projectId } : {};
      const response = await axios.get(`${API_BASE_URL}/api/financials/consolidated`, {
        headers: { Authorization: `Bearer ${token}` },
        params
      });

      setConsolidatedData(response.data.consolidated_data);
      setTotals(response.data.totals);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load financial data');
      console.error('Error fetching financial data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
        <button
          onClick={fetchConsolidatedData}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!consolidatedData || !totals) {
    return <div>No data available</div>;
  }

  // Prepare chart data
  const assetsPieData = [
    { name: 'Current Assets', value: totals.current_assets },
    { name: 'Non-Current Assets', value: totals.non_current_assets },
  ];

  const incomeData = [
    { name: 'Revenue', value: totals.total_revenue },
    { name: 'COGS', value: -totals.total_cogs },
    { name: 'Gross Profit', value: totals.gross_profit },
    { name: 'Operating Expenses', value: -totals.total_operating_expenses },
    { name: 'Operating Income', value: totals.operating_income },
    { name: 'Net Income', value: totals.net_income },
  ];

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-900">AI-Consolidated Financial Statements</h2>
          <button
            onClick={fetchConsolidatedData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Refresh Data
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-200">
          <button
            className={`px-6 py-3 font-medium ${
              activeTab === 'balance-sheet'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('balance-sheet')}
          >
            Balance Sheet
          </button>
          <button
            className={`px-6 py-3 font-medium ${
              activeTab === 'income-statement'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('income-statement')}
          >
            Income Statement
          </button>
          <button
            className={`px-6 py-3 font-medium ${
              activeTab === 'ratios'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('ratios')}
          >
            Ratios & Metrics
          </button>
        </div>
      </div>

      {/* Balance Sheet Tab */}
      {activeTab === 'balance-sheet' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Assets */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Assets</h3>

            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Current Assets</h4>
                {Object.entries(consolidatedData.current_assets).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-1">
                    <span className="text-gray-600">{key}</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
                <div className="flex justify-between py-2 border-t border-gray-200 font-bold">
                  <span>Total Current Assets</span>
                  <span>{formatCurrency(totals.current_assets)}</span>
                </div>
              </div>

              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Non-Current Assets</h4>
                {Object.entries(consolidatedData.non_current_assets).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-1">
                    <span className="text-gray-600">{key}</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
                <div className="flex justify-between py-2 border-t border-gray-200 font-bold">
                  <span>Total Non-Current Assets</span>
                  <span>{formatCurrency(totals.non_current_assets)}</span>
                </div>
              </div>

              <div className="flex justify-between py-3 border-t-2 border-gray-800 font-bold text-lg">
                <span>TOTAL ASSETS</span>
                <span className="text-blue-600">{formatCurrency(totals.total_assets)}</span>
              </div>
            </div>

            {/* Assets Pie Chart */}
            <div className="mt-6">
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={assetsPieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(props: any) => {
                      const { name, percent } = props;
                      return `${name}: ${(percent * 100).toFixed(0)}%`;
                    }}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {assetsPieData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => formatCurrency(value as number)} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Liabilities & Equity */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Liabilities & Equity</h3>

            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Current Liabilities</h4>
                {Object.entries(consolidatedData.current_liabilities).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-1">
                    <span className="text-gray-600">{key}</span>
                    <span className="font-medium">{formatCurrency(value)}</span>
                  </div>
                ))}
                <div className="flex justify-between py-2 border-t border-gray-200 font-bold">
                  <span>Total Current Liabilities</span>
                  <span>{formatCurrency(totals.current_liabilities)}</span>
                </div>
              </div>

              {totals.long_term_liabilities > 0 && (
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Long-term Liabilities</h4>
                  {Object.entries(consolidatedData.long_term_liabilities).map(([key, value]) => (
                    <div key={key} className="flex justify-between py-1">
                      <span className="text-gray-600">{key}</span>
                      <span className="font-medium">{formatCurrency(value)}</span>
                    </div>
                  ))}
                  <div className="flex justify-between py-2 border-t border-gray-200 font-bold">
                    <span>Total Long-term Liabilities</span>
                    <span>{formatCurrency(totals.long_term_liabilities)}</span>
                  </div>
                </div>
              )}

              <div className="flex justify-between py-3 border-t-2 border-gray-800 font-bold text-lg">
                <span>TOTAL LIABILITIES</span>
                <span className="text-red-600">{formatCurrency(totals.total_liabilities)}</span>
              </div>

              <div className="mt-4">
                <h4 className="font-semibold text-gray-700 mb-2">Equity</h4>
                {Object.entries(consolidatedData.equity).length > 0 ? (
                  Object.entries(consolidatedData.equity).map(([key, value]) => (
                    <div key={key} className="flex justify-between py-1">
                      <span className="text-gray-600">{key}</span>
                      <span className="font-medium">{formatCurrency(value)}</span>
                    </div>
                  ))
                ) : (
                  <div className="text-gray-400 text-sm">No equity items found</div>
                )}
                <div className="flex justify-between py-3 border-t-2 border-gray-800 font-bold text-lg">
                  <span>TOTAL EQUITY</span>
                  <span className="text-green-600">{formatCurrency(totals.total_equity)}</span>
                </div>
              </div>

              {/* Balance Check */}
              <div className={`flex justify-between py-3 border-t border-dashed ${
                Math.abs(totals.balance_check) < 1 ? 'border-green-500 text-green-700' : 'border-red-500 text-red-700'
              }`}>
                <span className="font-medium">Balance Check (should be $0)</span>
                <span className="font-bold">{formatCurrency(totals.balance_check)}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Income Statement Tab */}
      {activeTab === 'income-statement' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Income Statement</h3>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left: Details */}
            <div className="space-y-6">
              {/* Revenue */}
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Revenue</h4>
                {Object.entries(consolidatedData.revenue).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-1">
                    <span className="text-gray-600">{key}</span>
                    <span className="font-medium text-green-600">{formatCurrency(value)}</span>
                  </div>
                ))}
                <div className="flex justify-between py-2 border-t border-gray-200 font-bold">
                  <span>Total Revenue</span>
                  <span className="text-green-600">{formatCurrency(totals.total_revenue)}</span>
                </div>
              </div>

              {/* COGS */}
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Cost of Goods Sold</h4>
                {Object.entries(consolidatedData.cost_of_goods_sold).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-1">
                    <span className="text-gray-600">{key}</span>
                    <span className="font-medium text-red-600">{formatCurrency(value)}</span>
                  </div>
                ))}
                <div className="flex justify-between py-2 border-t border-gray-200 font-bold">
                  <span>Total COGS</span>
                  <span className="text-red-600">{formatCurrency(totals.total_cogs)}</span>
                </div>
              </div>

              {/* Gross Profit */}
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-bold text-lg">Gross Profit</div>
                    <div className="text-sm text-gray-600">
                      Margin: {formatPercent((totals.gross_profit / totals.total_revenue) * 100)}
                    </div>
                  </div>
                  <span className={`font-bold text-2xl ${totals.gross_profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {formatCurrency(totals.gross_profit)}
                  </span>
                </div>
              </div>

              {/* Operating Expenses */}
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">Operating Expenses</h4>
                {Object.entries(consolidatedData.operating_expenses).map(([key, value]) => (
                  <div key={key} className="flex justify-between py-1">
                    <span className="text-gray-600">{key}</span>
                    <span className="font-medium text-red-600">{formatCurrency(value)}</span>
                  </div>
                ))}
                <div className="flex justify-between py-2 border-t border-gray-200 font-bold">
                  <span>Total Operating Expenses</span>
                  <span className="text-red-600">{formatCurrency(totals.total_operating_expenses)}</span>
                </div>
              </div>

              {/* Operating Income */}
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-bold text-lg">Operating Income (EBIT)</div>
                    <div className="text-sm text-gray-600">
                      Margin: {formatPercent((totals.operating_income / totals.total_revenue) * 100)}
                    </div>
                  </div>
                  <span className={`font-bold text-2xl ${totals.operating_income >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {formatCurrency(totals.operating_income)}
                  </span>
                </div>
              </div>

              {/* Net Income */}
              <div className="bg-gradient-to-r from-blue-50 to-green-50 p-4 rounded-lg border-2 border-blue-200">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-bold text-xl">Net Income</div>
                    <div className="text-sm text-gray-600">
                      Margin: {formatPercent((totals.net_income / totals.total_revenue) * 100)}
                    </div>
                  </div>
                  <span className={`font-bold text-3xl ${totals.net_income >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {formatCurrency(totals.net_income)}
                  </span>
                </div>
              </div>
            </div>

            {/* Right: Chart */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-4">Income Waterfall</h4>
              <ResponsiveContainer width="100%" height={500}>
                <BarChart data={incomeData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis tickFormatter={(value) => formatCurrency(value)} />
                  <Tooltip formatter={(value) => formatCurrency(value as number)} />
                  <Bar dataKey="value">
                    {incomeData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.value >= 0 ? '#10B981' : '#EF4444'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {/* Ratios Tab */}
      {activeTab === 'ratios' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Profitability</h3>
            <div className="space-y-3">
              <div>
                <div className="text-sm text-gray-600">Gross Profit Margin</div>
                <div className="text-2xl font-bold text-blue-600">
                  {formatPercent((totals.gross_profit / totals.total_revenue) * 100)}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Operating Margin</div>
                <div className="text-2xl font-bold text-purple-600">
                  {formatPercent((totals.operating_income / totals.total_revenue) * 100)}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Net Profit Margin</div>
                <div className="text-2xl font-bold text-green-600">
                  {formatPercent((totals.net_income / totals.total_revenue) * 100)}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Liquidity</h3>
            <div className="space-y-3">
              <div>
                <div className="text-sm text-gray-600">Current Ratio</div>
                <div className="text-2xl font-bold text-blue-600">
                  {(totals.current_assets / totals.current_liabilities).toFixed(2)}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Working Capital</div>
                <div className="text-2xl font-bold text-green-600">
                  {formatCurrency(totals.current_assets - totals.current_liabilities)}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Leverage</h3>
            <div className="space-y-3">
              <div>
                <div className="text-sm text-gray-600">Debt to Assets</div>
                <div className="text-2xl font-bold text-orange-600">
                  {formatPercent((totals.total_liabilities / totals.total_assets) * 100)}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export { FinancialStatements };
export default FinancialStatements;
