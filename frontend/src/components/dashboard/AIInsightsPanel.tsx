/**
 * AI Insights Panel Component
 * Displays Databricks-powered predictions, anomalies, and forecasts
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Prediction {
  category: string;
  current_spent: number;
  budget: number;
  predicted_final: number;
  predicted_overrun: number;
  confidence: number;
  risk_level: string;
  weeks_to_overrun: number | null;
  recommendation: string;
}

interface Anomaly {
  id: string;
  transaction_id: string;
  date: string;
  description: string;
  amount: number;
  category: string;
  anomaly_type: string;
  severity: string;
  confidence: number;
  details: string;
  recommendation: string;
}

interface WeeklyForecast {
  week: number;
  start_date: string;
  end_date: string;
  expected_inflow: number;
  expected_outflow: number;
  net_change: number;
  ending_balance: number;
  risk_level: string;
}

interface InsightsSummary {
  high_risk_predictions: number;
  total_predictions: number;
  critical_anomalies: number;
  total_anomalies: number;
  cash_flow_issues: number;
  overall_risk_score: number;
  overall_risk_level: string;
}

interface AIInsightsData {
  summary: InsightsSummary;
  predictions: {
    predictions: Prediction[];
    demo_mode?: boolean;
  };
  anomalies: {
    anomalies: Anomaly[];
    demo_mode?: boolean;
  };
  forecast: {
    weekly_forecast: WeeklyForecast[];
    demo_mode?: boolean;
  };
}

export const AIInsightsPanel: React.FC<{ projectId: string }> = ({ projectId }) => {
  const [insights, setInsights] = useState<AIInsightsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'predictions' | 'anomalies' | 'forecast'>('overview');

  useEffect(() => {
    fetchInsights();
  }, [projectId]);

  const fetchInsights = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('auth_token');
      const response = await axios.get(`${API_URL}/analytics/insights/${projectId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setInsights(response.data);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching AI insights:', err);
      setError(err.response?.data?.detail || 'Failed to load AI insights');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level?.toUpperCase()) {
      case 'HIGH':
      case 'CRITICAL':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'MEDIUM':
      case 'MODERATE':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'LOW':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 0
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-purple-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-purple-100 rounded"></div>
            <div className="h-4 bg-purple-100 rounded w-5/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-600">⚠️ {error}</p>
      </div>
    );
  }

  if (!insights) return null;

  const isDemoMode = insights.predictions.demo_mode || insights.anomalies.demo_mode;

  return (
    <div className="space-y-4">
      {/* Header Card */}
      <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg shadow-lg p-6 text-white">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold flex items-center gap-2">
              🤖 AI Insights
              {isDemoMode && (
                <span className="text-xs bg-yellow-400 text-yellow-900 px-2 py-1 rounded font-normal">
                  DEMO MODE
                </span>
              )}
            </h2>
            <p className="text-purple-100 text-sm mt-1">
              AI-powered predictions and analysis
            </p>
          </div>
          <div className={`text-right ${getRiskColor(insights.summary.overall_risk_level)} px-4 py-2 rounded-lg`}>
            <div className="text-3xl font-bold">{insights.summary.overall_risk_score}</div>
            <div className="text-xs font-semibold">Risk Score</div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-3 gap-4 mt-6">
          <div className="bg-white/10 backdrop-blur rounded-lg p-3">
            <div className="text-2xl font-bold">
              {insights.summary.high_risk_predictions}
            </div>
            <div className="text-xs text-purple-200">High Risk Alerts</div>
          </div>
          <div className="bg-white/10 backdrop-blur rounded-lg p-3">
            <div className="text-2xl font-bold">
              {insights.summary.critical_anomalies}
            </div>
            <div className="text-xs text-purple-200">Critical Anomalies</div>
          </div>
          <div className="bg-white/10 backdrop-blur rounded-lg p-3">
            <div className="text-2xl font-bold">
              {insights.summary.cash_flow_issues}
            </div>
            <div className="text-xs text-purple-200">Cash Flow Issues</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {[
              { key: 'overview', label: '📊 Overview', count: null },
              { key: 'predictions', label: '🔮 Predictions', count: insights.predictions.predictions?.length },
              { key: 'anomalies', label: '🔍 Anomalies', count: insights.anomalies.anomalies?.length },
              { key: 'forecast', label: '📈 Cash Flow', count: insights.forecast.weekly_forecast?.length }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.key
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
                {tab.count !== null && (
                  <span className="ml-2 bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full text-xs">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">AI Analysis Summary</h3>

              {/* Top Risks */}
              {insights.predictions.predictions?.filter(p => p.risk_level === 'HIGH').map(pred => (
                <div key={pred.category} className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <div className="flex items-start">
                    <span className="text-2xl mr-3">⚠️</span>
                    <div className="flex-1">
                      <h4 className="font-semibold text-red-900">{pred.category} - High Risk</h4>
                      <p className="text-sm text-red-700 mt-1">
                        Predicted overrun: {formatCurrency(pred.predicted_overrun)}
                        {pred.weeks_to_overrun && ` in ${pred.weeks_to_overrun} weeks`}
                      </p>
                      <p className="text-sm text-red-600 mt-2">💡 {pred.recommendation}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-semibold text-red-900">
                        {(pred.confidence * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-red-600">Confidence</div>
                    </div>
                  </div>
                </div>
              ))}

              {/* Critical Anomalies */}
              {insights.anomalies.anomalies?.filter(a => a.severity === 'HIGH').map(anomaly => (
                <div key={anomaly.id} className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                  <div className="flex items-start">
                    <span className="text-2xl mr-3">🔍</span>
                    <div className="flex-1">
                      <h4 className="font-semibold text-yellow-900">{anomaly.description}</h4>
                      <p className="text-sm text-yellow-700 mt-1">
                        {formatCurrency(anomaly.amount)} - {anomaly.details}
                      </p>
                      <p className="text-sm text-yellow-600 mt-2">💡 {anomaly.recommendation}</p>
                    </div>
                  </div>
                </div>
              ))}

              {/* Cash Flow Warnings */}
              {insights.forecast.weekly_forecast
                ?.filter(w => w.ending_balance < 0)
                .slice(0, 1)
                .map(week => (
                  <div key={week.week} className="bg-orange-50 border-l-4 border-orange-500 p-4 rounded">
                    <div className="flex items-start">
                      <span className="text-2xl mr-3">💰</span>
                      <div className="flex-1">
                        <h4 className="font-semibold text-orange-900">Cash Flow Alert - Week {week.week}</h4>
                        <p className="text-sm text-orange-700 mt-1">
                          Projected balance: {formatCurrency(week.ending_balance)} (NEGATIVE)
                        </p>
                        <p className="text-sm text-orange-600 mt-2">
                          ⚠️ Immediate action required to avoid cash shortage
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          )}

          {/* Predictions Tab */}
          {activeTab === 'predictions' && (
            <div className="space-y-4">
              {insights.predictions.predictions?.map(pred => (
                <div key={pred.category} className={`border-2 rounded-lg p-4 ${getRiskColor(pred.risk_level)}`}>
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-bold text-lg">{pred.category}</h4>
                      <span className={`inline-block px-2 py-1 rounded text-xs font-semibold mt-1 ${getRiskColor(pred.risk_level)}`}>
                        {pred.risk_level} RISK
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold">
                        {pred.predicted_overrun > 0 ? '+' : ''}{formatCurrency(pred.predicted_overrun)}
                      </div>
                      <div className="text-xs">Predicted Variance</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 mb-3">
                    <div>
                      <div className="text-xs text-gray-600">Budget</div>
                      <div className="font-semibold">{formatCurrency(pred.budget)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-600">Current Spent</div>
                      <div className="font-semibold">{formatCurrency(pred.current_spent)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-600">Predicted Final</div>
                      <div className="font-semibold">{formatCurrency(pred.predicted_final)}</div>
                    </div>
                  </div>

                  <div className="bg-white/50 rounded p-3 mb-2">
                    <div className="text-xs text-gray-600 mb-1">Progress</div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${(pred.current_spent / pred.budget) * 100}%` }}
                      ></div>
                    </div>
                    <div className="text-xs text-gray-600 mt-1">
                      {((pred.current_spent / pred.budget) * 100).toFixed(1)}% of budget used
                    </div>
                  </div>

                  <div className="bg-white/50 rounded p-3">
                    <div className="text-xs font-semibold text-gray-700 mb-1">💡 Recommendation:</div>
                    <div className="text-sm">{pred.recommendation}</div>
                  </div>

                  <div className="mt-2 flex justify-between text-xs text-gray-600">
                    <span>Confidence: {(pred.confidence * 100).toFixed(0)}%</span>
                    {pred.weeks_to_overrun && (
                      <span className="font-semibold">⏱️ {pred.weeks_to_overrun} weeks to overrun</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Anomalies Tab */}
          {activeTab === 'anomalies' && (
            <div className="space-y-4">
              {insights.anomalies.anomalies?.map(anomaly => (
                <div key={anomaly.id} className={`border-2 rounded-lg p-4 ${getRiskColor(anomaly.severity)}`}>
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-bold text-lg">{anomaly.description}</h4>
                      <div className="flex gap-2 mt-1">
                        <span className={`inline-block px-2 py-1 rounded text-xs font-semibold ${getRiskColor(anomaly.severity)}`}>
                          {anomaly.severity}
                        </span>
                        <span className="inline-block px-2 py-1 rounded text-xs font-semibold bg-gray-100 text-gray-700">
                          {anomaly.anomaly_type}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold">{formatCurrency(anomaly.amount)}</div>
                      <div className="text-xs text-gray-600">{anomaly.date}</div>
                    </div>
                  </div>

                  <div className="bg-white/50 rounded p-3 mb-2">
                    <div className="text-sm mb-2">{anomaly.details}</div>
                    <div className="text-xs text-gray-600">
                      Transaction ID: {anomaly.transaction_id} | Category: {anomaly.category}
                    </div>
                  </div>

                  <div className="bg-white/50 rounded p-3">
                    <div className="text-xs font-semibold text-gray-700 mb-1">💡 Recommendation:</div>
                    <div className="text-sm">{anomaly.recommendation}</div>
                  </div>

                  <div className="mt-2 text-xs text-gray-600">
                    Confidence: {(anomaly.confidence * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Forecast Tab */}
          {activeTab === 'forecast' && (
            <div className="space-y-4">
              {insights.forecast.weekly_forecast?.map(week => (
                <div key={week.week} className={`border-2 rounded-lg p-4 ${getRiskColor(week.risk_level)}`}>
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-bold text-lg">Week {week.week}</h4>
                      <div className="text-sm text-gray-600">
                        {week.start_date} to {week.end_date}
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded text-sm font-semibold ${getRiskColor(week.risk_level)}`}>
                      {week.risk_level}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-3">
                    <div className="bg-green-50 rounded p-3">
                      <div className="text-xs text-green-600">Expected Inflow</div>
                      <div className="text-lg font-bold text-green-700">
                        {formatCurrency(week.expected_inflow)}
                      </div>
                    </div>
                    <div className="bg-red-50 rounded p-3">
                      <div className="text-xs text-red-600">Expected Outflow</div>
                      <div className="text-lg font-bold text-red-700">
                        {formatCurrency(week.expected_outflow)}
                      </div>
                    </div>
                  </div>

                  <div className="bg-white/50 rounded p-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold">Net Change:</span>
                      <span className={`text-lg font-bold ${week.net_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {week.net_change >= 0 ? '+' : ''}{formatCurrency(week.net_change)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center mt-2 pt-2 border-t">
                      <span className="text-sm font-semibold">Ending Balance:</span>
                      <span className={`text-xl font-bold ${week.ending_balance >= 0 ? 'text-blue-600' : 'text-red-600'}`}>
                        {formatCurrency(week.ending_balance)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
