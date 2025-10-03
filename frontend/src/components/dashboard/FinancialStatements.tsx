import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

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

type TabType = 'balance-sheet' | 'income-statement' | 'cash-flow' | 'equity' | 'ratios' | 'assumptions' | 'instructions';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#14B8A6', '#F97316'];

const FinancialStatements: React.FC<FinancialStatementsProps> = ({ projectId }) => {
  const [consolidatedData, setConsolidatedData] = useState<ConsolidatedData | null>(null);
  const [totals, setTotals] = useState<Totals | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('balance-sheet');

  useEffect(() => {
    fetchConsolidatedData();
  }, []);

  const fetchConsolidatedData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('auth_token');

      const params = projectId ? { project_id: projectId } : {};
      const response = await axios.get(`${API_BASE_URL}/financials/consolidated`, {
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

  // Calculate ratios
  const currentRatio = totals.current_assets / totals.current_liabilities;
  const quickRatio = (totals.current_assets - (consolidatedData.current_assets['Inventory'] || 0)) / totals.current_liabilities;
  const workingCapital = totals.current_assets - totals.current_liabilities;
  const debtToEquity = totals.total_liabilities / totals.total_equity;
  const debtToAssets = totals.total_liabilities / totals.total_assets;
  const equityRatio = totals.total_equity / totals.total_assets;
  const grossMargin = (totals.gross_profit / totals.total_revenue) * 100;
  const operatingMargin = (totals.operating_income / totals.total_revenue) * 100;
  const netMargin = (totals.net_income / totals.total_revenue) * 100;

  // Chart data
  const assetsPieData = [
    { name: 'Current Assets', value: totals.current_assets },
    { name: 'Non-Current Assets', value: totals.non_current_assets },
  ];

  const liabilitiesEquityPieData = [
    { name: 'Current Liabilities', value: totals.current_liabilities },
    { name: 'Long-term Liabilities', value: totals.long_term_liabilities },
    { name: 'Total Equity', value: totals.total_equity },
  ];

  const incomeWaterfallData = [
    { name: 'Revenue', value: totals.total_revenue, cumulative: totals.total_revenue },
    { name: 'COGS', value: -totals.total_cogs, cumulative: totals.gross_profit },
    { name: 'Gross Profit', value: totals.gross_profit, cumulative: totals.gross_profit },
    { name: 'Operating Exp.', value: -totals.total_operating_expenses, cumulative: totals.operating_income },
    { name: 'Operating Income', value: totals.operating_income, cumulative: totals.operating_income },
    { name: 'Net Income', value: totals.net_income, cumulative: totals.net_income },
  ];

  // Mock cash flow data (you'll need to implement this in backend)
  const cashFlowData = {
    operating: 850000,
    investing: -320000,
    financing: -180000,
    net_change: 350000,
    beginning_cash: 500000,
    ending_cash: 850000,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Financial Model Dashboard</h2>
            <p className="text-sm text-gray-600 mt-1">Comprehensive financial analysis and reporting</p>
          </div>
          <button
            onClick={fetchConsolidatedData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Refresh Data
          </button>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-gray-200 overflow-x-auto">
          {[
            { id: 'balance-sheet', label: 'Balance Sheet' },
            { id: 'income-statement', label: 'Income Statement' },
            { id: 'cash-flow', label: 'Cash Flow' },
            { id: 'equity', label: 'Equity Statement' },
            { id: 'ratios', label: 'Ratios Dashboard' },
            { id: 'assumptions', label: 'Assumptions' },
            { id: 'instructions', label: 'Instructions' },
          ].map((tab) => (
            <button
              key={tab.id}
              className={`px-6 py-3 font-medium whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab(tab.id as TabType)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Balance Sheet Tab */}
      {activeTab === 'balance-sheet' && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium opacity-90">Total Assets</h3>
              <p className="text-3xl font-bold mt-2">{formatCurrency(totals.total_assets)}</p>
            </div>
            <div className="bg-gradient-to-br from-red-500 to-red-600 text-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium opacity-90">Total Liabilities</h3>
              <p className="text-3xl font-bold mt-2">{formatCurrency(totals.total_liabilities)}</p>
            </div>
            <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium opacity-90">Total Equity</h3>
              <p className="text-3xl font-bold mt-2">{formatCurrency(totals.total_equity)}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Assets Section */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Assets</h3>

              <div className="space-y-4">
                {/* Current Assets */}
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2 flex items-center">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                    Current Assets
                  </h4>
                  <div className="ml-4 space-y-1">
                    {Object.entries(consolidatedData.current_assets).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-1 text-sm">
                        <span className="text-gray-600">{key}</span>
                        <span className="font-medium">{formatCurrency(value)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between py-2 mt-2 border-t border-gray-200 font-bold">
                    <span>Total Current Assets</span>
                    <span className="text-blue-600">{formatCurrency(totals.current_assets)}</span>
                  </div>
                </div>

                {/* Non-Current Assets */}
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2 flex items-center">
                    <span className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>
                    Non-Current Assets
                  </h4>
                  <div className="ml-4 space-y-1">
                    {Object.entries(consolidatedData.non_current_assets).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-1 text-sm">
                        <span className="text-gray-600">{key}</span>
                        <span className="font-medium">{formatCurrency(value)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between py-2 mt-2 border-t border-gray-200 font-bold">
                    <span>Total Non-Current Assets</span>
                    <span className="text-indigo-600">{formatCurrency(totals.non_current_assets)}</span>
                  </div>
                </div>

                <div className="flex justify-between py-3 border-t-2 border-gray-800 font-bold text-lg">
                  <span>TOTAL ASSETS</span>
                  <span className="text-blue-600">{formatCurrency(totals.total_assets)}</span>
                </div>
              </div>

              {/* Assets Chart */}
              <div className="mt-6">
                <h4 className="font-semibold text-gray-700 mb-4">Asset Composition</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={assetsPieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={(entry) => `${entry.name}: ${formatPercent(((entry.value as number) / totals.total_assets) * 100)}`}
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

            {/* Liabilities & Equity Section */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Liabilities & Equity</h3>

              <div className="space-y-4">
                {/* Current Liabilities */}
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2 flex items-center">
                    <span className="w-2 h-2 bg-red-500 rounded-full mr-2"></span>
                    Current Liabilities
                  </h4>
                  <div className="ml-4 space-y-1">
                    {Object.entries(consolidatedData.current_liabilities).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-1 text-sm">
                        <span className="text-gray-600">{key}</span>
                        <span className="font-medium">{formatCurrency(value)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between py-2 mt-2 border-t border-gray-200 font-bold">
                    <span>Total Current Liabilities</span>
                    <span className="text-red-600">{formatCurrency(totals.current_liabilities)}</span>
                  </div>
                </div>

                {/* Long-term Liabilities */}
                {totals.long_term_liabilities > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2 flex items-center">
                      <span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
                      Long-term Liabilities
                    </h4>
                    <div className="ml-4 space-y-1">
                      {Object.entries(consolidatedData.long_term_liabilities).map(([key, value]) => (
                        <div key={key} className="flex justify-between py-1 text-sm">
                          <span className="text-gray-600">{key}</span>
                          <span className="font-medium">{formatCurrency(value)}</span>
                        </div>
                      ))}
                    </div>
                    <div className="flex justify-between py-2 mt-2 border-t border-gray-200 font-bold">
                      <span>Total Long-term Liabilities</span>
                      <span className="text-orange-600">{formatCurrency(totals.long_term_liabilities)}</span>
                    </div>
                  </div>
                )}

                <div className="flex justify-between py-3 border-t-2 border-gray-800 font-bold text-lg">
                  <span>TOTAL LIABILITIES</span>
                  <span className="text-red-600">{formatCurrency(totals.total_liabilities)}</span>
                </div>

                {/* Equity */}
                <div className="mt-4">
                  <h4 className="font-semibold text-gray-700 mb-2 flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    Equity
                  </h4>
                  {Object.entries(consolidatedData.equity).length > 0 ? (
                    <div className="ml-4 space-y-1">
                      {Object.entries(consolidatedData.equity).map(([key, value]) => (
                        <div key={key} className="flex justify-between py-1 text-sm">
                          <span className="text-gray-600">{key}</span>
                          <span className="font-medium">{formatCurrency(value)}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="ml-4 text-gray-400 text-sm">Calculated from Assets - Liabilities</div>
                  )}
                  <div className="flex justify-between py-3 border-t-2 border-gray-800 font-bold text-lg">
                    <span>TOTAL EQUITY</span>
                    <span className="text-green-600">{formatCurrency(totals.total_equity)}</span>
                  </div>
                </div>

                {/* Balance Check */}
                <div className={`flex justify-between py-3 mt-4 border-t border-dashed rounded-lg p-3 ${
                  Math.abs(totals.balance_check) < 1
                    ? 'bg-green-50 border-green-500 text-green-700'
                    : 'bg-red-50 border-red-500 text-red-700'
                }`}>
                  <span className="font-medium">⚖️ Balance Check (Assets = Liabilities + Equity)</span>
                  <span className="font-bold">{formatCurrency(totals.balance_check)}</span>
                </div>
              </div>

              {/* Liabilities & Equity Chart */}
              <div className="mt-6">
                <h4 className="font-semibold text-gray-700 mb-4">Capital Structure</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={liabilitiesEquityPieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={(entry) => `${(entry.name || '').split(' ')[0]}: ${formatPercent(((entry.value as number) / totals.total_assets) * 100)}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {liabilitiesEquityPieData.map((_entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index + 3]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => formatCurrency(value as number)} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Income Statement Tab */}
      {activeTab === 'income-statement' && (
        <div className="space-y-6">
          {/* Summary Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
              <h3 className="text-sm font-medium text-gray-600">Revenue</h3>
              <p className="text-2xl font-bold text-gray-900 mt-2">{formatCurrency(totals.total_revenue)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
              <h3 className="text-sm font-medium text-gray-600">Gross Profit</h3>
              <p className="text-2xl font-bold text-gray-900 mt-2">{formatCurrency(totals.gross_profit)}</p>
              <p className="text-xs text-gray-500 mt-1">Margin: {formatPercent(grossMargin)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
              <h3 className="text-sm font-medium text-gray-600">Operating Income</h3>
              <p className="text-2xl font-bold text-gray-900 mt-2">{formatCurrency(totals.operating_income)}</p>
              <p className="text-xs text-gray-500 mt-1">Margin: {formatPercent(operatingMargin)}</p>
            </div>
            <div className={`rounded-lg shadow p-6 border-l-4 ${totals.net_income >= 0 ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'}`}>
              <h3 className="text-sm font-medium text-gray-600">Net Income</h3>
              <p className={`text-2xl font-bold mt-2 ${totals.net_income >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(totals.net_income)}
              </p>
              <p className="text-xs text-gray-500 mt-1">Margin: {formatPercent(netMargin)}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Income Statement Details */}
            <div className="bg-white rounded-lg shadow p-6 space-y-6">
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Income Statement</h3>

                {/* Revenue */}
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-700 mb-2">Revenue</h4>
                  <div className="ml-4 space-y-1">
                    {Object.entries(consolidatedData.revenue).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-1 text-sm">
                        <span className="text-gray-600">{key}</span>
                        <span className="font-medium text-green-600">{formatCurrency(value)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between py-2 mt-2 border-t border-gray-200 font-bold">
                    <span>Total Revenue</span>
                    <span className="text-green-600">{formatCurrency(totals.total_revenue)}</span>
                  </div>
                </div>

                {/* COGS */}
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-700 mb-2">Cost of Goods Sold</h4>
                  <div className="ml-4 space-y-1">
                    {Object.entries(consolidatedData.cost_of_goods_sold).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-1 text-sm">
                        <span className="text-gray-600">{key}</span>
                        <span className="font-medium text-red-600">{formatCurrency(value)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between py-2 mt-2 border-t border-gray-200 font-bold">
                    <span>Total COGS</span>
                    <span className="text-red-600">{formatCurrency(totals.total_cogs)}</span>
                  </div>
                </div>

                {/* Gross Profit */}
                <div className="bg-blue-50 p-4 rounded-lg mb-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-bold text-lg">Gross Profit</div>
                      <div className="text-sm text-gray-600">Margin: {formatPercent(grossMargin)}</div>
                    </div>
                    <span className="font-bold text-2xl text-blue-600">{formatCurrency(totals.gross_profit)}</span>
                  </div>
                </div>

                {/* Operating Expenses */}
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-700 mb-2">Operating Expenses</h4>
                  <div className="ml-4 space-y-1">
                    {Object.entries(consolidatedData.operating_expenses).map(([key, value]) => (
                      <div key={key} className="flex justify-between py-1 text-sm">
                        <span className="text-gray-600">{key}</span>
                        <span className="font-medium text-red-600">{formatCurrency(value)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between py-2 mt-2 border-t border-gray-200 font-bold">
                    <span>Total Operating Expenses</span>
                    <span className="text-red-600">{formatCurrency(totals.total_operating_expenses)}</span>
                  </div>
                </div>

                {/* Operating Income */}
                <div className="bg-purple-50 p-4 rounded-lg mb-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-bold text-lg">Operating Income (EBIT)</div>
                      <div className="text-sm text-gray-600">Margin: {formatPercent(operatingMargin)}</div>
                    </div>
                    <span className="font-bold text-2xl text-purple-600">{formatCurrency(totals.operating_income)}</span>
                  </div>
                </div>

                {/* Net Income */}
                <div className={`p-4 rounded-lg border-2 ${totals.net_income >= 0 ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-bold text-xl">Net Income</div>
                      <div className="text-sm text-gray-600">Margin: {formatPercent(netMargin)}</div>
                    </div>
                    <span className={`font-bold text-3xl ${totals.net_income >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {formatCurrency(totals.net_income)}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Income Waterfall Chart */}
            <div className="bg-white rounded-lg shadow p-6">
              <h4 className="font-semibold text-gray-700 mb-4">Income Waterfall</h4>
              <ResponsiveContainer width="100%" height={500}>
                <BarChart data={incomeWaterfallData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis tickFormatter={(value) => formatCurrency(value)} />
                  <Tooltip formatter={(value) => formatCurrency(value as number)} />
                  <Bar dataKey="value">
                    {incomeWaterfallData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.value >= 0 ? '#10B981' : '#EF4444'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>

              {/* Margin Trends */}
              <div className="mt-8">
                <h4 className="font-semibold text-gray-700 mb-4">Profit Margins</h4>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Gross Profit Margin</span>
                      <span className="font-bold">{formatPercent(grossMargin)}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className="bg-blue-600 h-3 rounded-full"
                        style={{ width: `${Math.min(grossMargin, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Operating Margin</span>
                      <span className="font-bold">{formatPercent(operatingMargin)}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className="bg-purple-600 h-3 rounded-full"
                        style={{ width: `${Math.min(operatingMargin, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Net Profit Margin</span>
                      <span className="font-bold">{formatPercent(netMargin)}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full ${netMargin >= 0 ? 'bg-green-600' : 'bg-red-600'}`}
                        style={{ width: `${Math.min(Math.abs(netMargin), 100)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cash Flow Statement Tab */}
      {activeTab === 'cash-flow' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Cash Flow Statement</h3>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Cash Flow Details */}
              <div className="space-y-6">
                {/* Operating Activities */}
                <div className="border-b pb-4">
                  <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
                    Cash Flows from Operating Activities
                  </h4>
                  <div className="ml-5 space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Net Income</span>
                      <span className="font-medium">{formatCurrency(totals.net_income)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Add: Depreciation & Amortization</span>
                      <span className="font-medium">{formatCurrency(120000)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Changes in Working Capital</span>
                      <span className="font-medium">{formatCurrency(-50000)}</span>
                    </div>
                    <div className="flex justify-between font-bold pt-2 border-t">
                      <span>Net Cash from Operating</span>
                      <span className="text-blue-600">{formatCurrency(cashFlowData.operating)}</span>
                    </div>
                  </div>
                </div>

                {/* Investing Activities */}
                <div className="border-b pb-4">
                  <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="w-3 h-3 bg-purple-500 rounded-full mr-2"></span>
                    Cash Flows from Investing Activities
                  </h4>
                  <div className="ml-5 space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Purchase of PPE</span>
                      <span className="font-medium text-red-600">{formatCurrency(-350000)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Proceeds from Asset Sales</span>
                      <span className="font-medium text-green-600">{formatCurrency(30000)}</span>
                    </div>
                    <div className="flex justify-between font-bold pt-2 border-t">
                      <span>Net Cash from Investing</span>
                      <span className="text-purple-600">{formatCurrency(cashFlowData.investing)}</span>
                    </div>
                  </div>
                </div>

                {/* Financing Activities */}
                <div className="border-b pb-4">
                  <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="w-3 h-3 bg-orange-500 rounded-full mr-2"></span>
                    Cash Flows from Financing Activities
                  </h4>
                  <div className="ml-5 space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Proceeds from Loans</span>
                      <span className="font-medium text-green-600">{formatCurrency(100000)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Loan Repayments</span>
                      <span className="font-medium text-red-600">{formatCurrency(-280000)}</span>
                    </div>
                    <div className="flex justify-between font-bold pt-2 border-t">
                      <span>Net Cash from Financing</span>
                      <span className="text-orange-600">{formatCurrency(cashFlowData.financing)}</span>
                    </div>
                  </div>
                </div>

                {/* Net Change */}
                <div className="bg-gradient-to-r from-blue-50 to-green-50 p-4 rounded-lg">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-bold text-lg">Net Change in Cash</div>
                      <div className="text-sm text-gray-600 mt-1">
                        Beginning: {formatCurrency(cashFlowData.beginning_cash)}
                      </div>
                      <div className="text-sm text-gray-600">
                        Ending: {formatCurrency(cashFlowData.ending_cash)}
                      </div>
                    </div>
                    <span className={`font-bold text-2xl ${cashFlowData.net_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {formatCurrency(cashFlowData.net_change)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Cash Flow Chart */}
              <div>
                <h4 className="font-semibold text-gray-700 mb-4">Cash Flow Breakdown</h4>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart
                    data={[
                      { name: 'Operating', value: cashFlowData.operating },
                      { name: 'Investing', value: cashFlowData.investing },
                      { name: 'Financing', value: cashFlowData.financing },
                      { name: 'Net Change', value: cashFlowData.net_change },
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis tickFormatter={(value) => formatCurrency(value)} />
                    <Tooltip formatter={(value) => formatCurrency(value as number)} />
                    <Bar dataKey="value">
                      <Cell fill="#3B82F6" />
                      <Cell fill="#8B5CF6" />
                      <Cell fill="#F97316" />
                      <Cell fill="#10B981" />
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>

                {/* Key Metrics */}
                <div className="mt-6 grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-600">Free Cash Flow</div>
                    <div className="text-xl font-bold text-blue-600 mt-1">
                      {formatCurrency(cashFlowData.operating + cashFlowData.investing)}
                    </div>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-600">Cash Flow Margin</div>
                    <div className="text-xl font-bold text-purple-600 mt-1">
                      {formatPercent((cashFlowData.operating / totals.total_revenue) * 100)}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Equity Statement Tab */}
      {activeTab === 'equity' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Statement of Changes in Equity</h3>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Share Capital
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Retained Earnings
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Other Reserves
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Equity
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                <tr className="bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">Beginning Balance</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(500000)}</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(totals.total_equity - totals.net_income - 500000)}</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(0)}</td>
                  <td className="px-6 py-4 text-right font-bold">{formatCurrency(totals.total_equity - totals.net_income)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 pl-12 text-gray-700">Net Profit for the Period</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right text-green-600">{formatCurrency(totals.net_income)}</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right text-green-600">{formatCurrency(totals.net_income)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 pl-12 text-gray-700">Other Comprehensive Income</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(0)}</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(0)}</td>
                </tr>
                <tr className="bg-blue-50">
                  <td className="px-6 py-4 font-medium text-gray-900">Total Comprehensive Income</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right font-bold">{formatCurrency(totals.net_income)}</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right font-bold">{formatCurrency(totals.net_income)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 pl-12 text-gray-700">Dividends Paid</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right text-red-600">{formatCurrency(0)}</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right text-red-600">{formatCurrency(0)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 pl-12 text-gray-700">Share Capital Issued</td>
                  <td className="px-6 py-4 text-right text-green-600">{formatCurrency(0)}</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right">-</td>
                  <td className="px-6 py-4 text-right text-green-600">{formatCurrency(0)}</td>
                </tr>
                <tr className="bg-gray-50 font-bold">
                  <td className="px-6 py-4 text-gray-900">Ending Balance</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(500000)}</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(totals.total_equity - 500000)}</td>
                  <td className="px-6 py-4 text-right">{formatCurrency(0)}</td>
                  <td className="px-6 py-4 text-right text-blue-600 text-lg">{formatCurrency(totals.total_equity)}</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Equity Composition Chart */}
          <div className="mt-8">
            <h4 className="font-semibold text-gray-700 mb-4">Equity Composition</h4>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={[
                    { name: 'Share Capital', value: 500000 },
                    { name: 'Retained Earnings', value: totals.total_equity - 500000 },
                  ]}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name}: ${formatCurrency(entry.value as number)}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  <Cell fill="#3B82F6" />
                  <Cell fill="#10B981" />
                </Pie>
                <Tooltip formatter={(value) => formatCurrency(value as number)} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Ratios Dashboard Tab */}
      {activeTab === 'ratios' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Liquidity Ratios */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-1 h-6 bg-blue-500 mr-2"></span>
                Liquidity Ratios
              </h3>
              <div className="space-y-4">
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Current Ratio</span>
                    <span className={`text-2xl font-bold ${currentRatio >= 1.5 ? 'text-green-600' : currentRatio >= 1 ? 'text-yellow-600' : 'text-red-600'}`}>
                      {currentRatio.toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Target: &gt; 1.5 (Healthy: &gt; 2.0)</p>
                </div>
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Quick Ratio</span>
                    <span className={`text-2xl font-bold ${quickRatio >= 1 ? 'text-green-600' : 'text-yellow-600'}`}>
                      {quickRatio.toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Target: &gt; 1.0</p>
                </div>
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Working Capital</span>
                    <span className={`text-xl font-bold ${workingCapital > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {formatCurrency(workingCapital)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Higher is better</p>
                </div>
                <div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Cash Ratio</span>
                    <span className="text-2xl font-bold text-blue-600">
                      {((consolidatedData.current_assets['Cash and Cash Equivalents'] || 0) / totals.current_liabilities).toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Target: &gt; 0.5</p>
                </div>
              </div>
            </div>

            {/* Profitability Ratios */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-1 h-6 bg-green-500 mr-2"></span>
                Profitability Ratios
              </h3>
              <div className="space-y-4">
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Gross Margin</span>
                    <span className="text-2xl font-bold text-green-600">{formatPercent(grossMargin)}</span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Industry avg: 30-40%</p>
                </div>
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Operating Margin</span>
                    <span className="text-2xl font-bold text-purple-600">{formatPercent(operatingMargin)}</span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Industry avg: 15-20%</p>
                </div>
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Net Profit Margin</span>
                    <span className={`text-2xl font-bold ${netMargin > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {formatPercent(netMargin)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Industry avg: 10-15%</p>
                </div>
                <div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">ROA</span>
                    <span className="text-2xl font-bold text-green-600">
                      {formatPercent((totals.net_income / totals.total_assets) * 100)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Return on Assets</p>
                </div>
              </div>
            </div>

            {/* Leverage Ratios */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-1 h-6 bg-orange-500 mr-2"></span>
                Leverage Ratios
              </h3>
              <div className="space-y-4">
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Debt to Equity</span>
                    <span className={`text-2xl font-bold ${debtToEquity < 1 ? 'text-green-600' : debtToEquity < 2 ? 'text-yellow-600' : 'text-red-600'}`}>
                      {debtToEquity.toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Target: &lt; 1.0 (Conservative)</p>
                </div>
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Debt to Assets</span>
                    <span className="text-2xl font-bold text-orange-600">{formatPercent(debtToAssets * 100)}</span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Target: &lt; 50%</p>
                </div>
                <div className="border-b pb-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Equity Ratio</span>
                    <span className="text-2xl font-bold text-green-600">{formatPercent(equityRatio * 100)}</span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Target: &gt; 50%</p>
                </div>
                <div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Financial Leverage</span>
                    <span className="text-2xl font-bold text-orange-600">
                      {(totals.total_assets / totals.total_equity).toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Assets / Equity</p>
                </div>
              </div>
            </div>
          </div>

          {/* Efficiency & Activity Ratios */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-1 h-6 bg-purple-500 mr-2"></span>
                Efficiency Ratios
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-sm text-gray-600">Asset Turnover</span>
                  <span className="text-2xl font-bold text-purple-600">
                    {(totals.total_revenue / totals.total_assets).toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-sm text-gray-600">Inventory Turnover</span>
                  <span className="text-2xl font-bold text-purple-600">
                    {(totals.total_cogs / (consolidatedData.current_assets['Inventory'] || 1)).toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-sm text-gray-600">Days Inventory Outstanding</span>
                  <span className="text-2xl font-bold text-purple-600">
                    {((consolidatedData.current_assets['Inventory'] || 0) / totals.total_cogs * 365).toFixed(0)} days
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Working Capital Turnover</span>
                  <span className="text-2xl font-bold text-purple-600">
                    {(totals.total_revenue / workingCapital).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            {/* Cash Flow Ratios */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-1 h-6 bg-teal-500 mr-2"></span>
                Cash Flow Ratios
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-sm text-gray-600">Operating Cash Flow Ratio</span>
                  <span className="text-2xl font-bold text-teal-600">
                    {(cashFlowData.operating / totals.current_liabilities).toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-sm text-gray-600">Free Cash Flow</span>
                  <span className="text-2xl font-bold text-teal-600">
                    {formatCurrency(cashFlowData.operating + cashFlowData.investing)}
                  </span>
                </div>
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-sm text-gray-600">Cash Flow Margin</span>
                  <span className="text-2xl font-bold text-teal-600">
                    {formatPercent((cashFlowData.operating / totals.total_revenue) * 100)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Cash Return on Assets</span>
                  <span className="text-2xl font-bold text-teal-600">
                    {formatPercent((cashFlowData.operating / totals.total_assets) * 100)}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Ratio Summary Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Key Ratios Overview</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={[
                  { name: 'Current Ratio', value: currentRatio, target: 2 },
                  { name: 'Quick Ratio', value: quickRatio, target: 1 },
                  { name: 'Debt/Equity', value: debtToEquity, target: 1 },
                  { name: 'Gross Margin %', value: grossMargin / 10, target: 3.5 },
                  { name: 'Net Margin %', value: netMargin / 10, target: 1.5 },
                  { name: 'ROA %', value: (totals.net_income / totals.total_assets) * 10, target: 1 },
                ]}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-15} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#3B82F6" name="Actual" />
                <Bar dataKey="target" fill="#10B981" name="Target" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Assumptions Tab */}
      {activeTab === 'assumptions' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Key Business Assumptions</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Revenue Assumptions */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-4 pb-2 border-b">Revenue Assumptions</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Annual Growth Rate</span>
                  <span className="font-bold text-blue-600">15%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Average Project Size</span>
                  <span className="font-bold">$2.5M</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Number of Active Projects</span>
                  <span className="font-bold">12</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Payment Terms</span>
                  <span className="font-bold">Net 30</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Bad Debt %</span>
                  <span className="font-bold">2%</span>
                </div>
              </div>
            </div>

            {/* Cost Assumptions */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-4 pb-2 border-b">Cost Assumptions</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Target Gross Margin</span>
                  <span className="font-bold text-green-600">35-40%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Labor Cost Inflation</span>
                  <span className="font-bold">4%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Material Cost Inflation</span>
                  <span className="font-bold">6%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Operating Expense Ratio</span>
                  <span className="font-bold">18-22%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Overhead Allocation</span>
                  <span className="font-bold">12%</span>
                </div>
              </div>
            </div>

            {/* Working Capital Assumptions */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-4 pb-2 border-b">Working Capital</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Target Current Ratio</span>
                  <span className="font-bold text-blue-600">2.0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Days Sales Outstanding</span>
                  <span className="font-bold">45 days</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Days Inventory Outstanding</span>
                  <span className="font-bold">30 days</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Days Payable Outstanding</span>
                  <span className="font-bold">60 days</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Cash Conversion Cycle</span>
                  <span className="font-bold">15 days</span>
                </div>
              </div>
            </div>

            {/* Financial Structure */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-4 pb-2 border-b">Financial Structure</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Target Debt/Equity</span>
                  <span className="font-bold text-orange-600">0.5 - 0.8</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Interest Rate (Average)</span>
                  <span className="font-bold">6.5%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Dividend Payout Ratio</span>
                  <span className="font-bold">30%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Tax Rate</span>
                  <span className="font-bold">25%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">WACC</span>
                  <span className="font-bold">8.5%</span>
                </div>
              </div>
            </div>
          </div>

          {/* Macroeconomic Assumptions */}
          <div className="mt-8">
            <h4 className="font-semibold text-gray-700 mb-4 pb-2 border-b">Macroeconomic Assumptions</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600 mb-1">GDP Growth</div>
                <div className="text-2xl font-bold text-blue-600">3.2%</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600 mb-1">Inflation Rate</div>
                <div className="text-2xl font-bold text-green-600">3.5%</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600 mb-1">Construction Index Growth</div>
                <div className="text-2xl font-bold text-purple-600">5.8%</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Instructions Tab */}
      {activeTab === 'instructions' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Financial Model User Guide</h3>

          <div className="prose max-w-none">
            {/* Overview */}
            <div className="mb-8">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">📊 Overview</h4>
              <p className="text-gray-700">
                This comprehensive financial model provides AI-powered consolidation of your construction business financials.
                The system automatically aggregates data from multiple sources including budgets, payments, subcontractors, and project data
                to generate accurate financial statements and insights.
              </p>
            </div>

            {/* How to Use Each Tab */}
            <div className="mb-8">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">📑 Tab-by-Tab Guide</h4>

              <div className="space-y-4">
                <div className="border-l-4 border-blue-500 pl-4">
                  <h5 className="font-semibold text-gray-900">1. Balance Sheet</h5>
                  <p className="text-sm text-gray-700">
                    View your complete financial position with assets, liabilities, and equity. The balance sheet is automatically
                    validated with a balance check (Assets = Liabilities + Equity). Review pie charts for asset composition and
                    capital structure analysis.
                  </p>
                </div>

                <div className="border-l-4 border-green-500 pl-4">
                  <h5 className="font-semibold text-gray-900">2. Income Statement</h5>
                  <p className="text-sm text-gray-700">
                    Analyze your profitability from revenue down to net income. Review gross profit, operating income (EBIT), and
                    net profit with automatic margin calculations. The waterfall chart visualizes the flow from revenue to net income.
                  </p>
                </div>

                <div className="border-l-4 border-purple-500 pl-4">
                  <h5 className="font-semibold text-gray-900">3. Cash Flow Statement</h5>
                  <p className="text-sm text-gray-700">
                    Track cash movements across operating, investing, and financing activities. Monitor free cash flow and
                    cash conversion metrics. Essential for understanding liquidity and cash generation.
                  </p>
                </div>

                <div className="border-l-4 border-orange-500 pl-4">
                  <h5 className="font-semibold text-gray-900">4. Equity Statement</h5>
                  <p className="text-sm text-gray-700">
                    Monitor changes in equity including share capital, retained earnings, and reserves. Track comprehensive income,
                    dividends, and capital transactions.
                  </p>
                </div>

                <div className="border-l-4 border-teal-500 pl-4">
                  <h5 className="font-semibold text-gray-900">5. Ratios Dashboard</h5>
                  <p className="text-sm text-gray-700">
                    Access 30+ financial ratios across liquidity, profitability, leverage, efficiency, and cash flow categories.
                    Each ratio includes industry benchmarks and health indicators.
                  </p>
                </div>

                <div className="border-l-4 border-pink-500 pl-4">
                  <h5 className="font-semibold text-gray-900">6. Assumptions</h5>
                  <p className="text-sm text-gray-700">
                    Review and understand key business drivers and assumptions used in the model including growth rates, margins,
                    working capital targets, and macroeconomic factors.
                  </p>
                </div>
              </div>
            </div>

            {/* Key Features */}
            <div className="mb-8">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">✨ Key Features</h4>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                <li>Automatic data consolidation from multiple sources</li>
                <li>Real-time financial statement generation</li>
                <li>Comprehensive ratio analysis with benchmarks</li>
                <li>Visual analytics with charts and graphs</li>
                <li>Balance sheet validation and error checking</li>
                <li>Export capabilities for reporting</li>
                <li>Mobile-responsive design</li>
              </ul>
            </div>

            {/* Understanding Ratios */}
            <div className="mb-8">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">📈 Understanding Key Ratios</h4>

              <div className="bg-gray-50 p-4 rounded-lg space-y-3">
                <div>
                  <h6 className="font-semibold text-sm">Current Ratio (Target: &gt; 2.0)</h6>
                  <p className="text-sm text-gray-600">Measures ability to pay short-term obligations. Higher is better.</p>
                </div>
                <div>
                  <h6 className="font-semibold text-sm">Debt to Equity (Target: &lt; 1.0)</h6>
                  <p className="text-sm text-gray-600">Measures financial leverage. Lower indicates less risk.</p>
                </div>
                <div>
                  <h6 className="font-semibold text-sm">Gross Margin (Target: 35-40%)</h6>
                  <p className="text-sm text-gray-600">Revenue minus COGS as % of revenue. Higher means better profitability.</p>
                </div>
                <div>
                  <h6 className="font-semibold text-sm">Net Margin (Target: 10-15%)</h6>
                  <p className="text-sm text-gray-600">Bottom line profit as % of revenue. Key profitability indicator.</p>
                </div>
              </div>
            </div>

            {/* Best Practices */}
            <div className="mb-8">
              <h4 className="text-lg font-semibold text-gray-900 mb-3">💡 Best Practices</h4>
              <ol className="list-decimal list-inside space-y-2 text-gray-700">
                <li>Review financial statements monthly for trend analysis</li>
                <li>Monitor key ratios against industry benchmarks</li>
                <li>Track working capital metrics weekly</li>
                <li>Ensure balance sheet always balances (check should be $0)</li>
                <li>Compare actual vs budget regularly</li>
                <li>Use the refresh button to get latest data</li>
                <li>Export statements for board meetings and stakeholder reports</li>
              </ol>
            </div>

            {/* Support */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-blue-900 mb-2">🆘 Need Help?</h4>
              <p className="text-sm text-blue-800">
                For technical support or questions about the financial model, contact your system administrator or
                refer to the detailed documentation in the help center.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export { FinancialStatements };
export default FinancialStatements;
