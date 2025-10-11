import { useState } from 'react';
import { Upload, FileText, CheckCircle2, XCircle, Loader2, Database, ArrowRight, TrendingUp, DollarSign, FileSpreadsheet } from 'lucide-react';

interface ExtractionResult {
  method: 'mineru' | 'pdfplumber';
  confidence: number;
  text_length: number;
  transactions_found: number;
  processing_time: number;
  text_preview: string;
  transactions: Array<{
    description: string;
    amount: number;
    date?: string;
    category?: string;
    confidence: number;
  }>;
  saved_to?: string;
}

interface ComparisonResults {
  mineru: ExtractionResult | null;
  pdfplumber: ExtractionResult | null;
  file_name: string;
}

export function PDFExtractionTest() {
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState<ComparisonResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      setError('Please upload a PDF file');
      return;
    }

    setUploading(true);
    setError(null);
    setResults(null);

    try {
      // Upload and extract with both methods
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/extraction/test-comparison', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <div className="flex items-center gap-3 mb-6">
        <FileText className="w-6 h-6 text-blue-600" />
        <div>
          <h2 className="text-xl font-bold text-gray-900">MinerU PDF Extraction Test</h2>
          <p className="text-sm text-gray-600">
            Upload a PDF to see MinerU vs pdfplumber extraction comparison
          </p>
        </div>
      </div>

      {/* Upload Area */}
      <div className="mb-6">
        <label className="block">
          <div className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            uploading ? 'border-gray-300 bg-gray-50' : 'border-blue-300 bg-blue-50 hover:bg-blue-100'
          }`}>
            <input
              type="file"
              accept="application/pdf"
              onChange={handleFileUpload}
              disabled={uploading}
              className="hidden"
            />
            {uploading ? (
              <div className="flex flex-col items-center gap-3">
                <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
                <p className="text-sm text-gray-600">Extracting with both methods...</p>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-3">
                <Upload className="w-12 h-12 text-blue-600" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Click to upload PDF</p>
                  <p className="text-xs text-gray-500">Invoice, receipt, bank statement, etc.</p>
                </div>
              </div>
            )}
          </div>
        </label>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium text-red-900">Error</p>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <CheckCircle2 className="w-4 h-4 text-green-600" />
            Extracted: <strong>{results.file_name}</strong>
          </div>

          {/* Comparison Grid */}
          <div className="grid grid-cols-2 gap-6">
            {/* MinerU Results */}
            <div className="border border-blue-200 rounded-lg overflow-hidden">
              <div className="bg-blue-50 px-4 py-3 border-b border-blue-200">
                <h3 className="font-bold text-blue-900">🚀 MinerU (Advanced)</h3>
              </div>
              {results.mineru ? (
                <div className="p-4 space-y-3">
                  {/* Stats */}
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <div className="text-gray-600">Confidence</div>
                      <div className="text-lg font-bold text-green-600">
                        {(results.mineru.confidence * 100).toFixed(0)}%
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600">Transactions</div>
                      <div className="text-lg font-bold text-gray-900">
                        {results.mineru.transactions_found}
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600">Text Length</div>
                      <div className="font-semibold text-gray-900">
                        {results.mineru.text_length} chars
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600">Time</div>
                      <div className="font-semibold text-gray-900">
                        {results.mineru.processing_time.toFixed(2)}s
                      </div>
                    </div>
                  </div>

                  {/* Text Preview */}
                  <div>
                    <div className="text-xs font-medium text-gray-600 mb-1">Text Preview:</div>
                    <div className="bg-gray-50 p-3 rounded border border-gray-200 text-xs font-mono whitespace-pre-wrap">
                      {results.mineru.text_preview}
                    </div>
                  </div>

                  {/* Saved Location */}
                  {results.mineru.saved_to && (
                    <div className="flex items-start gap-2 p-3 bg-green-50 border border-green-200 rounded">
                      <Database className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-medium text-green-900">Saved to:</div>
                        <div className="text-xs text-green-700 font-mono truncate">
                          {results.mineru.saved_to}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Transactions */}
                  {results.mineru.transactions.length > 0 && (
                    <div>
                      <div className="text-xs font-medium text-gray-600 mb-2">
                        Extracted Transactions ({results.mineru.transactions.length}):
                      </div>
                      <div className="space-y-2 max-h-64 overflow-y-auto">
                        {results.mineru.transactions.slice(0, 5).map((txn, idx) => (
                          <div key={idx} className="bg-gray-50 p-2 rounded border border-gray-200">
                            <div className="flex justify-between items-start gap-2">
                              <div className="flex-1 min-w-0">
                                <div className="text-xs font-medium text-gray-900 truncate">
                                  {txn.description}
                                </div>
                                {txn.category && (
                                  <div className="text-xs text-gray-500">{txn.category}</div>
                                )}
                              </div>
                              <div className="text-right flex-shrink-0">
                                <div className="text-xs font-bold text-gray-900">
                                  ${txn.amount.toFixed(2)}
                                </div>
                                <div className="text-xs text-gray-500">
                                  {(txn.confidence * 100).toFixed(0)}%
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                        {results.mineru.transactions.length > 5 && (
                          <div className="text-xs text-gray-500 text-center py-2">
                            + {results.mineru.transactions.length - 5} more transactions
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-4 text-sm text-gray-500">No results</div>
              )}
            </div>

            {/* pdfplumber Results */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                <h3 className="font-bold text-gray-900">📄 pdfplumber (Basic)</h3>
              </div>
              {results.pdfplumber ? (
                <div className="p-4 space-y-3">
                  {/* Stats */}
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <div className="text-gray-600">Confidence</div>
                      <div className="text-lg font-bold text-yellow-600">
                        {(results.pdfplumber.confidence * 100).toFixed(0)}%
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600">Transactions</div>
                      <div className="text-lg font-bold text-gray-900">
                        {results.pdfplumber.transactions_found}
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600">Text Length</div>
                      <div className="font-semibold text-gray-900">
                        {results.pdfplumber.text_length} chars
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600">Time</div>
                      <div className="font-semibold text-gray-900">
                        {results.pdfplumber.processing_time.toFixed(2)}s
                      </div>
                    </div>
                  </div>

                  {/* Text Preview */}
                  <div>
                    <div className="text-xs font-medium text-gray-600 mb-1">Text Preview:</div>
                    <div className="bg-gray-50 p-3 rounded border border-gray-200 text-xs font-mono whitespace-pre-wrap">
                      {results.pdfplumber.text_preview || 'No text extracted'}
                    </div>
                  </div>

                  {/* Transactions */}
                  {results.pdfplumber.transactions.length > 0 && (
                    <div>
                      <div className="text-xs font-medium text-gray-600 mb-2">
                        Extracted Transactions ({results.pdfplumber.transactions.length}):
                      </div>
                      <div className="space-y-2 max-h-64 overflow-y-auto">
                        {results.pdfplumber.transactions.slice(0, 5).map((txn, idx) => (
                          <div key={idx} className="bg-gray-50 p-2 rounded border border-gray-200">
                            <div className="flex justify-between items-start gap-2">
                              <div className="flex-1 min-w-0">
                                <div className="text-xs font-medium text-gray-900 truncate">
                                  {txn.description}
                                </div>
                                {txn.category && (
                                  <div className="text-xs text-gray-500">{txn.category}</div>
                                )}
                              </div>
                              <div className="text-right flex-shrink-0">
                                <div className="text-xs font-bold text-gray-900">
                                  ${txn.amount.toFixed(2)}
                                </div>
                                <div className="text-xs text-gray-500">
                                  {(txn.confidence * 100).toFixed(0)}%
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                        {results.pdfplumber.transactions.length > 5 && (
                          <div className="text-xs text-gray-500 text-center py-2">
                            + {results.pdfplumber.transactions.length - 5} more transactions
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-4 text-sm text-gray-500">No results</div>
              )}
            </div>
          </div>

          {/* Winner Badge */}
          {results.mineru && results.pdfplumber && (
            <div className="p-4 bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 rounded-lg">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-6 h-6 text-green-600" />
                <div>
                  <div className="font-bold text-gray-900">
                    {results.mineru.confidence > results.pdfplumber.confidence
                      ? '🏆 MinerU wins with higher confidence!'
                      : results.mineru.transactions_found > results.pdfplumber.transactions_found
                      ? '🏆 MinerU found more transactions!'
                      : '✅ Both methods completed successfully'}
                  </div>
                  <div className="text-sm text-gray-600">
                    Improvement: +{((results.mineru.confidence - results.pdfplumber.confidence) * 100).toFixed(1)}% confidence,
                    +{results.mineru.transactions_found - results.pdfplumber.transactions_found} transactions
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Automated Pipeline Visualization */}
          {results.mineru && results.mineru.transactions_found > 0 && (
            <div className="mt-8 border-t-2 border-gray-300 pt-8">
              <div className="flex items-center gap-3 mb-6">
                <TrendingUp className="w-6 h-6 text-purple-600" />
                <div>
                  <h2 className="text-xl font-bold text-gray-900">Automated Financial Statement Pipeline</h2>
                  <p className="text-sm text-gray-600">
                    Watch as AI categorizes transactions and populates your financial statements
                  </p>
                </div>
              </div>

              {/* Pipeline Flow */}
              <div className="relative">
                {/* Progress Line */}
                <div className="absolute top-12 left-0 right-0 h-1 bg-gradient-to-r from-blue-200 via-purple-200 to-green-200 rounded-full" />
                <div className="absolute top-12 left-0 h-1 bg-gradient-to-r from-blue-600 via-purple-600 to-green-600 rounded-full transition-all duration-1000"
                     style={{ width: '100%' }} />

                {/* Pipeline Stages */}
                <div className="grid grid-cols-3 gap-4 relative z-10">
                  {/* Stage 1: Extracted Data */}
                  <div className="bg-white border-2 border-blue-500 rounded-lg p-4 shadow-lg">
                    <div className="flex items-center gap-2 mb-3">
                      <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">✓</div>
                      <div className="font-bold text-gray-900">1. Extracted Data</div>
                    </div>
                    <div className="text-xs text-gray-600 mb-2">
                      {results.mineru.transactions_found} transactions extracted
                    </div>
                    <div className="space-y-1 max-h-48 overflow-y-auto">
                      {results.mineru.transactions.slice(0, 6).map((txn, idx) => (
                        <div key={idx} className="bg-blue-50 p-2 rounded text-xs">
                          <div className="flex justify-between">
                            <span className="font-medium truncate">{txn.description}</span>
                            <span className="font-bold text-blue-600">${txn.amount.toFixed(2)}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Arrow 1 */}
                  <div className="absolute top-14 left-1/3 transform -translate-x-1/2 z-20">
                    <ArrowRight className="w-6 h-6 text-purple-600 animate-pulse" />
                  </div>

                  {/* Stage 2: AI Categorization */}
                  <div className="bg-white border-2 border-purple-500 rounded-lg p-4 shadow-lg">
                    <div className="flex items-center gap-2 mb-3">
                      <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">✓</div>
                      <div className="font-bold text-gray-900">2. AI Categorization</div>
                    </div>
                    <div className="text-xs text-gray-600 mb-2">
                      Intelligent categorization with confidence scores
                    </div>
                    <div className="space-y-1 max-h-48 overflow-y-auto">
                      {results.mineru.transactions.slice(0, 6).map((txn, idx) => (
                        <div key={idx} className="bg-purple-50 p-2 rounded text-xs">
                          <div className="flex justify-between items-start">
                            <div className="flex-1">
                              <div className="font-medium truncate">{txn.description}</div>
                              <div className="text-purple-700 font-semibold mt-0.5">
                                {txn.category || (txn.amount > 0 ? 'Revenue' : 'Expense')}
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="font-bold">${txn.amount.toFixed(2)}</div>
                              <div className="text-purple-600 text-xs">
                                {(txn.confidence * 100).toFixed(0)}%
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Arrow 2 */}
                  <div className="absolute top-14 left-2/3 transform -translate-x-1/2 z-20">
                    <ArrowRight className="w-6 h-6 text-green-600 animate-pulse" />
                  </div>

                  {/* Stage 3: Financial Statement */}
                  <div className="bg-white border-2 border-green-500 rounded-lg p-4 shadow-lg">
                    <div className="flex items-center gap-2 mb-3">
                      <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">✓</div>
                      <div className="font-bold text-gray-900">3. Income Statement</div>
                    </div>
                    <div className="text-xs text-gray-600 mb-2">
                      Auto-populated financial statement
                    </div>
                    <div className="bg-green-50 p-3 rounded text-xs font-mono space-y-1">
                      <div className="font-bold text-green-900 border-b border-green-300 pb-1 mb-2">
                        Income Statement Preview
                      </div>
                      {(() => {
                        const revenue = results.mineru.transactions
                          .filter(t => t.amount > 0)
                          .reduce((sum, t) => sum + t.amount, 0);
                        const expenses = Math.abs(results.mineru.transactions
                          .filter(t => t.amount < 0)
                          .reduce((sum, t) => sum + t.amount, 0));
                        const netIncome = revenue - expenses;

                        return (
                          <>
                            <div className="flex justify-between">
                              <span>Revenue</span>
                              <span className="font-bold text-green-600">${revenue.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Expenses</span>
                              <span className="font-bold text-red-600">(${expenses.toFixed(2)})</span>
                            </div>
                            <div className="border-t border-green-300 mt-2 pt-2 flex justify-between font-bold">
                              <span>Net Income</span>
                              <span className={netIncome >= 0 ? 'text-green-700' : 'text-red-700'}>
                                ${netIncome.toFixed(2)}
                              </span>
                            </div>
                          </>
                        );
                      })()}
                    </div>

                    {/* Export Button */}
                    <button
                      className="mt-3 w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-2 px-4 rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-200 font-semibold text-sm flex items-center justify-center gap-2"
                    >
                      <FileSpreadsheet className="w-4 h-4" />
                      Export to Excel
                    </button>
                  </div>
                </div>
              </div>

              {/* Info Badge */}
              <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-green-50 border border-purple-200 rounded-lg">
                <div className="flex items-center gap-3">
                  <DollarSign className="w-6 h-6 text-purple-600" />
                  <div>
                    <div className="font-bold text-gray-900">
                      ✨ Fully Automated Process
                    </div>
                    <div className="text-sm text-gray-600">
                      From PDF upload to financial statements in seconds - powered by AI
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
