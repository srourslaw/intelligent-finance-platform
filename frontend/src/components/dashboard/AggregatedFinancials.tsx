import { useState, useEffect } from 'react';
import { TrendingUp, AlertCircle, CheckCircle, Info, ChevronDown, ChevronRight, FileText, ExternalLink } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface FinancialLineItem {
  value: number;
  confidence: number;
  source_location: string;
}

interface CurrentAssets {
  [key: string]: FinancialLineItem;
}

interface NonCurrentAssets {
  [key: string]: FinancialLineItem;
}

interface Assets {
  current: CurrentAssets | null;
  non_current: NonCurrentAssets | null;
}

interface CurrentLiabilities {
  [key: string]: FinancialLineItem;
}

interface LongTermLiabilities {
  [key: string]: FinancialLineItem;
}

interface Liabilities {
  current: CurrentLiabilities | null;
  long_term: LongTermLiabilities | null;
}

interface Equity {
  [key: string]: FinancialLineItem;
}

interface BalanceSheet {
  assets: Assets;
  liabilities: Liabilities;
  equity: Equity | null;
}

interface Revenue {
  [key: string]: FinancialLineItem;
}

interface COGS {
  [key: string]: FinancialLineItem;
}

interface OperatingExpenses {
  [key: string]: FinancialLineItem;
}

interface OtherIncomeExpense {
  [key: string]: FinancialLineItem;
}

interface IncomeStatement {
  revenue: Revenue | null;
  cogs: COGS | null;
  operating_expenses: OperatingExpenses | null;
  other_income_expense: OtherIncomeExpense | null;
}

interface OperatingActivities {
  [key: string]: FinancialLineItem;
}

interface InvestingActivities {
  [key: string]: FinancialLineItem;
}

interface FinancingActivities {
  [key: string]: FinancialLineItem;
}

interface CashFlow {
  operating: OperatingActivities | null;
  investing: InvestingActivities | null;
  financing: FinancingActivities | null;
}

interface AggregatedData {
  project_id: string;
  aggregation_date: string;
  source_file_ids: string[];
  balance_sheet: BalanceSheet | null;
  income_statement: IncomeStatement | null;
  cash_flow: CashFlow | null;
  transactions: any[];
  total_files_processed: number;
  conflicts_detected: number;
  conflicts_resolved: number;
}

interface ValidationIssue {
  severity: string;
  message: string;
  field: string | null;
}

interface ValidationResult {
  project_id: string;
  validation_date: string;
  is_valid: boolean;
  errors: ValidationIssue[];
  warnings: ValidationIssue[];
}

interface AggregationSummary {
  project_id: string;
  aggregation_date: string;
  total_files_processed: number;
  transaction_count: number;
  has_balance_sheet: boolean;
  has_income_statement: boolean;
  has_cash_flow: boolean;
  validation: {
    is_valid: boolean;
    error_count: number;
    warning_count: number;
  } | null;
}

export function AggregatedFinancials() {
  const { token } = useAuth();
  const [aggregations, setAggregations] = useState<AggregationSummary[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);
  const [aggregatedData, setAggregatedData] = useState<AggregatedData | null>(null);
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['balance_sheet']));
  const [expandedLineItems, setExpandedLineItems] = useState<Set<string>>(new Set());
  const [sourceFiles, setSourceFiles] = useState<Map<string, any>>(new Map());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAggregations();
  }, []);

  const fetchAggregations = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/aggregation/list`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAggregations(response.data);
    } catch (err) {
      // Silently ignore - aggregation endpoint not yet implemented
    }
  };

  const loadAggregation = async (projectId: string) => {
    setLoading(true);
    try {
      const [dataResponse, validationResponse] = await Promise.all([
        axios.get(`${API_BASE_URL}/aggregation/result/${projectId}`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API_BASE_URL}/aggregation/validate/${projectId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      const aggData = dataResponse.data;
      setAggregatedData(aggData);
      setValidationResult(validationResponse.data);
      setSelectedProjectId(projectId);

      // Load source file metadata for drill-down
      const fileMap = new Map();
      if (aggData.source_file_ids) {
        for (const fileId of aggData.source_file_ids) {
          try {
            const fileResponse = await axios.get(`${API_BASE_URL}/extraction/result/${fileId}`, {
              headers: { Authorization: `Bearer ${token}` }
            });
            fileMap.set(fileId, fileResponse.data.metadata);
          } catch (err) {
            console.error(`Error loading file ${fileId}:`, err);
          }
        }
      }
      setSourceFiles(fileMap);
    } catch (err) {
      console.error('Error loading aggregation:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  const toggleLineItem = (itemKey: string) => {
    const newExpanded = new Set(expandedLineItems);
    if (newExpanded.has(itemKey)) {
      newExpanded.delete(itemKey);
    } else {
      newExpanded.add(itemKey);
    }
    setExpandedLineItems(newExpanded);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const calculateTotal = (items: any) => {
    if (!items) return 0;
    return Object.values(items).reduce((sum: number, item: any) => {
      if (typeof item === 'object' && item !== null && 'value' in item) {
        return sum + item.value;
      }
      return sum;
    }, 0);
  };

  const renderLineItems = (items: any, title: string, sectionPrefix: string) => {
    if (!items || Object.keys(items).length === 0) return null;

    return (
      <div className="mb-4">
        <h5 className="text-sm font-semibold text-gray-700 mb-2">{title}</h5>
        <div className="space-y-1">
          {Object.entries(items).map(([key, item]: [string, any]) => {
            if (typeof item !== 'object' || item === null || !('value' in item)) return null;

            const lineItem = item as FinancialLineItem;
            const itemKey = `${sectionPrefix}.${key}`;
            const isExpanded = expandedLineItems.has(itemKey);

            return (
              <div key={key} className="border border-gray-100 rounded">
                <button
                  onClick={() => toggleLineItem(itemKey)}
                  className="w-full flex justify-between items-center text-sm hover:bg-gray-50 px-2 py-1 rounded transition-colors"
                >
                  <div className="flex items-center gap-2">
                    {isExpanded ? (
                      <ChevronDown className="w-3 h-3 text-gray-400" />
                    ) : (
                      <ChevronRight className="w-3 h-3 text-gray-400" />
                    )}
                    <span className="text-gray-700 capitalize">{key.replace(/_/g, ' ')}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{formatCurrency(lineItem.value)}</span>
                    <span
                      className={`text-xs px-1.5 py-0.5 rounded ${
                        lineItem.confidence > 0.8
                          ? 'bg-green-100 text-green-700'
                          : lineItem.confidence > 0.5
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-red-100 text-red-700'
                      }`}
                    >
                      {(lineItem.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </button>

                {/* Drill-down details */}
                {isExpanded && (
                  <div className="px-4 py-2 bg-gray-50 border-t border-gray-200 text-xs space-y-1">
                    <div className="flex items-center gap-2 text-gray-600">
                      <ExternalLink className="w-3 h-3" />
                      <span className="font-medium">Source: {lineItem.source_location}</span>
                    </div>
                    {aggregatedData && aggregatedData.source_file_ids && (
                      <div className="mt-2 space-y-1">
                        <p className="text-gray-500 font-medium">Contributing Files:</p>
                        {aggregatedData.source_file_ids.map((fileId) => {
                          const fileMetadata = sourceFiles.get(fileId);
                          return (
                            <div key={fileId} className="flex items-center gap-2 text-gray-600 pl-2">
                              <FileText className="w-3 h-3" />
                              <span>{fileMetadata ? fileMetadata.original_filename : fileId}</span>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderBalanceSheet = (bs: BalanceSheet) => {
    const totalAssets = (bs.assets.current ? calculateTotal(bs.assets.current) : 0) +
                       (bs.assets.non_current ? calculateTotal(bs.assets.non_current) : 0);
    const totalLiabilities = (bs.liabilities.current ? calculateTotal(bs.liabilities.current) : 0) +
                            (bs.liabilities.long_term ? calculateTotal(bs.liabilities.long_term) : 0);
    const totalEquity = bs.equity ? calculateTotal(bs.equity) : 0;

    return (
      <div className="space-y-6">
        {/* Assets */}
        <div>
          <h4 className="font-bold text-gray-900 mb-3">Assets</h4>
          <div className="pl-4 space-y-4">
            {bs.assets.current && renderLineItems(bs.assets.current, 'Current Assets', 'balance_sheet.assets.current')}
            {bs.assets.non_current && renderLineItems(bs.assets.non_current, 'Non-Current Assets', 'balance_sheet.assets.non_current')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-bold text-gray-900">
                <span>Total Assets</span>
                <span>{formatCurrency(totalAssets)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Liabilities */}
        <div>
          <h4 className="font-bold text-gray-900 mb-3">Liabilities</h4>
          <div className="pl-4 space-y-4">
            {bs.liabilities.current && renderLineItems(bs.liabilities.current, 'Current Liabilities', 'balance_sheet.liabilities.current')}
            {bs.liabilities.long_term && renderLineItems(bs.liabilities.long_term, 'Long-Term Liabilities', 'balance_sheet.liabilities.long_term')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-bold text-gray-900">
                <span>Total Liabilities</span>
                <span>{formatCurrency(totalLiabilities)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Equity */}
        {bs.equity && (
          <div>
            <h4 className="font-bold text-gray-900 mb-3">Equity</h4>
            <div className="pl-4 space-y-4">
              {renderLineItems(bs.equity, 'Equity', 'balance_sheet.equity')}
              <div className="border-t pt-2">
                <div className="flex justify-between items-center font-bold text-gray-900">
                  <span>Total Equity</span>
                  <span>{formatCurrency(totalEquity)}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Balance Check */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex justify-between items-center text-sm">
            <span className="font-medium text-blue-900">Total Liabilities + Equity</span>
            <span className="font-bold text-blue-900">{formatCurrency(totalLiabilities + totalEquity)}</span>
          </div>
          <div className="flex justify-between items-center text-sm mt-1">
            <span className="font-medium text-blue-900">Difference</span>
            <span className={`font-bold ${Math.abs(totalAssets - (totalLiabilities + totalEquity)) < 1 ? 'text-green-600' : 'text-red-600'}`}>
              {formatCurrency(totalAssets - (totalLiabilities + totalEquity))}
            </span>
          </div>
        </div>
      </div>
    );
  };

  const renderIncomeStatement = (inc: IncomeStatement) => {
    const totalRevenue = inc.revenue ? calculateTotal(inc.revenue) : 0;
    const totalCOGS = inc.cogs ? calculateTotal(inc.cogs) : 0;
    const totalOpex = inc.operating_expenses ? calculateTotal(inc.operating_expenses) : 0;
    const totalOther = inc.other_income_expense ? calculateTotal(inc.other_income_expense) : 0;

    const grossProfit = totalRevenue - totalCOGS;
    const operatingIncome = grossProfit - totalOpex;
    const netIncome = operatingIncome + totalOther;

    return (
      <div className="space-y-6">
        {inc.revenue && renderLineItems(inc.revenue, 'Revenue', 'income_statement.revenue')}
        <div className="border-t pt-2">
          <div className="flex justify-between items-center font-semibold text-gray-900">
            <span>Total Revenue</span>
            <span>{formatCurrency(totalRevenue)}</span>
          </div>
        </div>

        {inc.cogs && (
          <>
            {renderLineItems(inc.cogs, 'Cost of Goods Sold', 'income_statement.cogs')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-semibold text-gray-900">
                <span>Total COGS</span>
                <span>{formatCurrency(totalCOGS)}</span>
              </div>
            </div>
          </>
        )}

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <div className="flex justify-between items-center font-bold text-blue-900">
            <span>Gross Profit</span>
            <span>{formatCurrency(grossProfit)}</span>
          </div>
          <div className="text-xs text-blue-600 mt-1">
            Margin: {totalRevenue > 0 ? ((grossProfit / totalRevenue) * 100).toFixed(1) : 0}%
          </div>
        </div>

        {inc.operating_expenses && (
          <>
            {renderLineItems(inc.operating_expenses, 'Operating Expenses', 'income_statement.operating_expenses')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-semibold text-gray-900">
                <span>Total Operating Expenses</span>
                <span>{formatCurrency(totalOpex)}</span>
              </div>
            </div>
          </>
        )}

        <div className="bg-green-50 border border-green-200 rounded-lg p-3">
          <div className="flex justify-between items-center font-bold text-green-900">
            <span>Operating Income</span>
            <span>{formatCurrency(operatingIncome)}</span>
          </div>
        </div>

        {inc.other_income_expense && (
          <>
            {renderLineItems(inc.other_income_expense, 'Other Income/Expense', 'income_statement.other_income_expense')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-semibold text-gray-900">
                <span>Total Other Income/Expense</span>
                <span>{formatCurrency(totalOther)}</span>
              </div>
            </div>
          </>
        )}

        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <div className="flex justify-between items-center font-bold text-purple-900 text-lg">
            <span>Net Income</span>
            <span>{formatCurrency(netIncome)}</span>
          </div>
        </div>
      </div>
    );
  };

  const renderCashFlow = (cf: CashFlow) => {
    const totalOperating = cf.operating ? calculateTotal(cf.operating) : 0;
    const totalInvesting = cf.investing ? calculateTotal(cf.investing) : 0;
    const totalFinancing = cf.financing ? calculateTotal(cf.financing) : 0;
    const netCashChange = totalOperating + totalInvesting + totalFinancing;

    return (
      <div className="space-y-6">
        {cf.operating && (
          <>
            {renderLineItems(cf.operating, 'Operating Activities', 'cash_flow.operating')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-semibold text-gray-900">
                <span>Net Cash from Operating</span>
                <span>{formatCurrency(totalOperating)}</span>
              </div>
            </div>
          </>
        )}

        {cf.investing && (
          <>
            {renderLineItems(cf.investing, 'Investing Activities', 'cash_flow.investing')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-semibold text-gray-900">
                <span>Net Cash from Investing</span>
                <span>{formatCurrency(totalInvesting)}</span>
              </div>
            </div>
          </>
        )}

        {cf.financing && (
          <>
            {renderLineItems(cf.financing, 'Financing Activities', 'cash_flow.financing')}
            <div className="border-t pt-2">
              <div className="flex justify-between items-center font-semibold text-gray-900">
                <span>Net Cash from Financing</span>
                <span>{formatCurrency(totalFinancing)}</span>
              </div>
            </div>
          </>
        )}

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex justify-between items-center font-bold text-blue-900 text-lg">
            <span>Net Cash Change</span>
            <span>{formatCurrency(netCashChange)}</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Aggregations List */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">📊 Aggregated Financial Statements</h2>
          <p className="text-sm text-gray-600 mt-1">
            Consolidated financial data from multiple uploaded files
          </p>
        </div>

        <div className="p-6">
          {aggregations.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <TrendingUp className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p>No aggregated data yet</p>
              <p className="text-sm mt-1">Upload files and create an aggregation to get started</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {aggregations.map((agg) => (
                <button
                  key={agg.project_id}
                  onClick={() => loadAggregation(agg.project_id)}
                  className={`text-left p-4 rounded-lg border-2 transition-all hover:shadow-md ${
                    selectedProjectId === agg.project_id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-bold text-gray-900">{agg.project_id}</h3>
                    {agg.validation && (
                      <div>
                        {agg.validation.is_valid ? (
                          <CheckCircle className="w-5 h-5 text-green-500" />
                        ) : (
                          <AlertCircle className="w-5 h-5 text-red-500" />
                        )}
                      </div>
                    )}
                  </div>

                  <div className="space-y-1 text-sm text-gray-600">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4" />
                      <span>{agg.total_files_processed} files</span>
                    </div>
                    <div className="flex gap-2 flex-wrap mt-2">
                      {agg.has_balance_sheet && (
                        <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs">BS</span>
                      )}
                      {agg.has_income_statement && (
                        <span className="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs">IS</span>
                      )}
                      {agg.has_cash_flow && (
                        <span className="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">CF</span>
                      )}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Detailed View */}
      {loading ? (
        <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-gray-600 mt-4">Loading aggregated data...</p>
        </div>
      ) : aggregatedData && validationResult ? (
        <div className="space-y-6">
          {/* Header */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{aggregatedData.project_id}</h2>
                <p className="text-sm text-gray-600 mt-1">
                  Aggregated {new Date(aggregatedData.aggregation_date).toLocaleDateString()} from{' '}
                  {aggregatedData.total_files_processed} files
                </p>
              </div>
              <div className="flex items-center gap-2">
                {validationResult.is_valid ? (
                  <div className="flex items-center gap-2 px-4 py-2 bg-green-50 border border-green-200 rounded-lg">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <span className="font-medium text-green-900">Valid</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 px-4 py-2 bg-red-50 border border-red-200 rounded-lg">
                    <AlertCircle className="w-5 h-5 text-red-600" />
                    <span className="font-medium text-red-900">{validationResult.errors.length} Errors</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Validation Issues */}
          {(validationResult.errors.length > 0 || validationResult.warnings.length > 0) && (
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4">Validation Results</h3>
              <div className="space-y-2">
                {validationResult.errors.map((error, idx) => (
                  <div key={`error-${idx}`} className="flex items-start gap-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                    <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-red-900">{error.message}</p>
                      {error.field && <p className="text-xs text-red-600 mt-1">Field: {error.field}</p>}
                    </div>
                  </div>
                ))}
                {validationResult.warnings.map((warning, idx) => (
                  <div key={`warning-${idx}`} className="flex items-start gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <Info className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-yellow-900">{warning.message}</p>
                      {warning.field && <p className="text-xs text-yellow-600 mt-1">Field: {warning.field}</p>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Financial Statements */}
          <div className="space-y-4">
            {/* Balance Sheet */}
            {aggregatedData.balance_sheet && (
              <div className="bg-white rounded-xl border border-gray-200">
                <button
                  onClick={() => toggleSection('balance_sheet')}
                  className="w-full p-6 flex items-center justify-between hover:bg-gray-50 transition-colors"
                >
                  <h3 className="text-lg font-bold text-gray-900">Balance Sheet</h3>
                  {expandedSections.has('balance_sheet') ? (
                    <ChevronDown className="w-5 h-5 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-500" />
                  )}
                </button>
                {expandedSections.has('balance_sheet') && (
                  <div className="px-6 pb-6">
                    {renderBalanceSheet(aggregatedData.balance_sheet)}
                  </div>
                )}
              </div>
            )}

            {/* Income Statement */}
            {aggregatedData.income_statement && (
              <div className="bg-white rounded-xl border border-gray-200">
                <button
                  onClick={() => toggleSection('income_statement')}
                  className="w-full p-6 flex items-center justify-between hover:bg-gray-50 transition-colors"
                >
                  <h3 className="text-lg font-bold text-gray-900">Income Statement</h3>
                  {expandedSections.has('income_statement') ? (
                    <ChevronDown className="w-5 h-5 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-500" />
                  )}
                </button>
                {expandedSections.has('income_statement') && (
                  <div className="px-6 pb-6">
                    {renderIncomeStatement(aggregatedData.income_statement)}
                  </div>
                )}
              </div>
            )}

            {/* Cash Flow */}
            {aggregatedData.cash_flow && (
              <div className="bg-white rounded-xl border border-gray-200">
                <button
                  onClick={() => toggleSection('cash_flow')}
                  className="w-full p-6 flex items-center justify-between hover:bg-gray-50 transition-colors"
                >
                  <h3 className="text-lg font-bold text-gray-900">Cash Flow Statement</h3>
                  {expandedSections.has('cash_flow') ? (
                    <ChevronDown className="w-5 h-5 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-500" />
                  )}
                </button>
                {expandedSections.has('cash_flow') && (
                  <div className="px-6 pb-6">
                    {renderCashFlow(aggregatedData.cash_flow)}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}
