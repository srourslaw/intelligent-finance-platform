import { useState } from 'react';
import { Upload, FileText, CheckCircle2, XCircle, Loader2, Database } from 'lucide-react';

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
        </div>
      )}
    </div>
  );
}
