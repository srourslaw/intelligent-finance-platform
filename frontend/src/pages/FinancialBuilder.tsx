import { useState, useEffect } from 'react';
import { FileSpreadsheet, Zap, CheckCircle2, Loader2, AlertCircle, TrendingUp, Database, BarChart3, Download } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { ConceptFlowAnimation } from '../components/dashboard/ConceptFlowAnimation';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface PipelineStage {
  name: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: number;
  details: string;
  filesProcessed?: number;
  totalFiles?: number;
}

interface FinancialResults {
  total_transactions: number;
  categorized: number;
  uncategorized_count: number;
  average_confidence: number;
  excel_path: string;
  categories?: {
    [key: string]: {
      count: number;
      total_amount: number;
      avg_confidence: number;
    };
  };
}

export default function FinancialBuilder() {
  const { } = useAuth();
  const currentProject = 'project-a-123-sunset-blvd'; // TODO: Make project-aware
  const [isProcessing, setIsProcessing] = useState(false);
  const [isLoadingResults, setIsLoadingResults] = useState(false);
  const [stages, setStages] = useState<PipelineStage[]>([
    { name: 'File Extraction', status: 'pending', progress: 0, details: 'Extract data from project files (PDFs, Excel)', filesProcessed: 0, totalFiles: 0 },
    { name: 'Data Normalization', status: 'pending', progress: 0, details: 'Parse into normalized data points with lineage' },
    { name: 'Deduplication & Validation', status: 'pending', progress: 0, details: 'Detect conflicts and validate data' },
    { name: 'AI Categorization', status: 'pending', progress: 0, details: 'Map transactions to financial categories' },
    { name: 'Excel Generation', status: 'pending', progress: 0, details: 'Generate financial model spreadsheet' },
  ]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [results, setResults] = useState<FinancialResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startPipeline = async () => {
    if (!currentProject) {
      setError('No project selected');
      return;
    }

    setIsProcessing(true);
    setIsLoadingResults(false);
    setError(null);
    setResults(null);
    setJobId(null);

    // Reset stages
    setStages(stages.map(s => ({ ...s, status: 'pending', progress: 0 })));

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/financial-builder/${currentProject}/run-full-pipeline`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      setJobId(data.job_id);

      // Update first stage to processing
      setStages(prev => prev.map((s, idx) =>
        idx === 0 ? { ...s, status: 'processing', totalFiles: data.total_files } : s
      ));

    } catch (err: any) {
      console.error('Pipeline start failed:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to start pipeline');
      setIsProcessing(false);
    }
  };

  // Poll for pipeline status
  useEffect(() => {
    if (!jobId || !isProcessing) return;

    const pollInterval = setInterval(async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/financial-builder/jobs/${jobId}/status`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const status = await response.json();

        // Update stages based on progress
        const progressPercent = status.progress_percent;

        setStages(prev => {
          const newStages = [...prev];

          // Extraction (0-30%)
          if (progressPercent >= 0) {
            newStages[0] = {
              ...newStages[0],
              status: progressPercent >= 30 ? 'completed' : 'processing',
              progress: Math.min(100, (progressPercent / 30) * 100),
              filesProcessed: status.processed_files,
              totalFiles: status.total_files
            };
          }

          // Normalization (30-50%)
          if (progressPercent >= 30) {
            newStages[1] = {
              ...newStages[1],
              status: progressPercent >= 50 ? 'completed' : 'processing',
              progress: Math.min(100, ((progressPercent - 30) / 20) * 100)
            };
          }

          // Deduplication (50-70%)
          if (progressPercent >= 50) {
            newStages[2] = {
              ...newStages[2],
              status: progressPercent >= 70 ? 'completed' : 'processing',
              progress: Math.min(100, ((progressPercent - 50) / 20) * 100)
            };
          }

          // Categorization (70-90%)
          if (progressPercent >= 70) {
            newStages[3] = {
              ...newStages[3],
              status: progressPercent >= 90 ? 'completed' : 'processing',
              progress: Math.min(100, ((progressPercent - 70) / 20) * 100)
            };
          }

          // Excel Generation (90-100%)
          if (progressPercent >= 90) {
            newStages[4] = {
              ...newStages[4],
              status: progressPercent >= 100 ? 'completed' : 'processing',
              progress: Math.min(100, ((progressPercent - 90) / 10) * 100)
            };
          }

          return newStages;
        });

        // Check if completed
        if (status.status === 'completed') {
          clearInterval(pollInterval);
          setIsProcessing(false);

          // Show loading state for results
          setIsLoadingResults(true);

          // Mark all stages complete
          setStages(prev => prev.map(s => ({ ...s, status: 'completed', progress: 100 })));

          // Parse metadata for results with slight delay to show loading
          setTimeout(() => {
            if (status.metadata) {
              try {
                const metadata = typeof status.metadata === 'string'
                  ? JSON.parse(status.metadata)
                  : status.metadata;
                setResults(metadata);
                setIsLoadingResults(false);
              } catch (e) {
                console.error('Failed to parse metadata:', e);
                setIsLoadingResults(false);
              }
            } else {
              setIsLoadingResults(false);
            }
          }, 500); // Small delay to ensure smooth transition
        }

        // Check if failed
        if (status.status === 'failed') {
          clearInterval(pollInterval);
          setIsProcessing(false);
          setError(status.error_message || 'Pipeline failed');

          // Mark current stage as error
          setStages(prev => prev.map(s =>
            s.status === 'processing' ? { ...s, status: 'error' } : s
          ));
        }

      } catch (err) {
        console.error('Status poll failed:', err);
        clearInterval(pollInterval);
        setIsProcessing(false);
        setError('Failed to check pipeline status');
      }
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(pollInterval);
  }, [jobId, isProcessing]);

  const getStageIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-6 h-6 text-green-600" />;
      case 'processing':
        return <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />;
      case 'error':
        return <AlertCircle className="w-6 h-6 text-red-600" />;
      default:
        return <div className="w-6 h-6 rounded-full border-2 border-gray-300" />;
    }
  };

  const getStageColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'border-green-500 bg-green-50';
      case 'processing':
        return 'border-blue-500 bg-blue-50';
      case 'error':
        return 'border-red-500 bg-red-50';
      default:
        return 'border-gray-300 bg-gray-50';
    }
  };


  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white py-8 px-8 shadow-xl">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-4">
            <FileSpreadsheet className="w-12 h-12" />
            <div>
              <h1 className="text-4xl font-bold mb-2">Financial Statement Builder</h1>
              <p className="text-purple-100">
                AI-powered extraction → Normalized data layer → Automated financial model
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 py-8 space-y-8">
        {/* Concept Flow Animation */}
        <ConceptFlowAnimation isAnimating={isProcessing} />

        {/* Info Card */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-lg">
          <div className="flex items-start gap-4">
            <Database className="w-8 h-8 text-purple-600 flex-shrink-0" />
            <div className="flex-1">
              <h2 className="text-xl font-bold text-gray-900 mb-2">How It Works</h2>
              <div className="text-sm text-gray-600 space-y-2">
                <p>
                  <strong>1. Extract:</strong> Process all PDFs and Excel files using MinerU AI and pandas
                </p>
                <p>
                  <strong>2. Normalize:</strong> Parse into structured data points with full lineage tracking
                </p>
                <p>
                  <strong>3. Validate:</strong> Detect duplicates, conflicts, and validate against business rules
                </p>
                <p>
                  <strong>4. Categorize:</strong> AI maps each transaction to financial statement categories
                </p>
                <p>
                  <strong>5. Generate:</strong> Create professional financial model Excel with 5 sheets
                </p>
              </div>
              {currentProject && (
                <div className="mt-4 p-3 bg-purple-50 border border-purple-200 rounded-lg">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-purple-600" />
                    <span className="text-sm font-semibold text-purple-900">
                      Project: {currentProject} • Ready for processing
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Start Button */}
        {!isProcessing && !results && (
          <div className="text-center">
            <button
              onClick={startPipeline}
              disabled={!currentProject}
              className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white py-4 px-8 rounded-xl hover:from-purple-700 hover:to-indigo-800 transition-all duration-200 font-bold text-lg shadow-lg flex items-center gap-3 mx-auto disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Zap className="w-6 h-6" />
              Start Full Pipeline Processing
            </button>
            {!currentProject && (
              <p className="mt-2 text-sm text-gray-500">Please select a project first</p>
            )}
          </div>
        )}

        {/* Pipeline Stages */}
        {(isProcessing || stages.some(s => s.status !== 'pending')) && !results && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Pipeline Progress</h2>

            {stages.map((stage, idx) => (
              <div key={idx} className={`border-2 rounded-xl p-6 transition-all duration-300 ${getStageColor(stage.status)}`}>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    {getStageIcon(stage.status)}
                    <div>
                      <h3 className="font-bold text-lg text-gray-900">{stage.name}</h3>
                      <p className="text-sm text-gray-600">{stage.details}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    {stage.filesProcessed !== undefined && stage.totalFiles !== undefined && (
                      <div className="text-sm font-semibold text-gray-900">
                        {stage.filesProcessed} / {stage.totalFiles} files
                      </div>
                    )}
                    <div className="text-sm text-gray-600">
                      {Math.round(stage.progress)}%
                    </div>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all duration-500 ${
                      stage.status === 'completed' ? 'bg-green-600' :
                      stage.status === 'processing' ? 'bg-blue-600' :
                      stage.status === 'error' ? 'bg-red-600' :
                      'bg-gray-400'
                    }`}
                    style={{ width: `${stage.progress}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="font-bold text-red-900 mb-1">Pipeline Error</h3>
                <p className="text-sm text-red-700">{error}</p>
                <button
                  onClick={() => {
                    setError(null);
                    setStages(stages.map(s => ({ ...s, status: 'pending', progress: 0 })));
                  }}
                  className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Try Again
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Loading Results State */}
        {!isProcessing && isLoadingResults && (
          <div className="bg-gradient-to-br from-purple-50 to-indigo-50 border-2 border-purple-200 rounded-xl p-8">
            <div className="flex flex-col items-center gap-4">
              <div className="relative">
                <Loader2 className="w-12 h-12 text-purple-600 animate-spin" />
                <div className="absolute inset-0 animate-ping">
                  <div className="w-12 h-12 bg-purple-400 rounded-full opacity-20"></div>
                </div>
              </div>
              <div className="text-center">
                <h3 className="text-xl font-bold text-purple-900 mb-2">
                  🎨 Preparing Your Financial Dashboard...
                </h3>
                <p className="text-sm text-purple-700">
                  Organizing {stages[0].totalFiles} files worth of financial data
                </p>
                <div className="mt-4 flex items-center gap-2 text-xs text-purple-600">
                  <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Success & Results Dashboard */}
        {results && !isLoadingResults && (
          <div className="space-y-6">
            {/* Success Banner */}
            <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6">
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-6 h-6 text-green-600 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="font-bold text-green-900 mb-2">✨ Financial Model Successfully Generated!</h3>
                  <p className="text-sm text-green-700">
                    All files have been processed and your financial statements are ready.
                  </p>
                </div>
              </div>
            </div>

            {/* Financial Summary Metrics */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">📊 Financial Summary</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Total Transactions */}
                <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
                  <div className="flex items-center justify-between mb-2">
                    <BarChart3 className="w-8 h-8 opacity-80" />
                    <span className="text-2xl font-bold">{results.total_transactions}</span>
                  </div>
                  <h3 className="text-sm font-semibold opacity-90">Total Transactions</h3>
                  <p className="text-xs opacity-75 mt-1">From all source files</p>
                </div>

                {/* Categorized */}
                <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
                  <div className="flex items-center justify-between mb-2">
                    <CheckCircle2 className="w-8 h-8 opacity-80" />
                    <span className="text-2xl font-bold">{results.categorized}</span>
                  </div>
                  <h3 className="text-sm font-semibold opacity-90">Successfully Categorized</h3>
                  <p className="text-xs opacity-75 mt-1">
                    {Math.round((results.categorized / results.total_transactions) * 100)}% success rate
                  </p>
                </div>

                {/* Uncategorized */}
                <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white shadow-lg">
                  <div className="flex items-center justify-between mb-2">
                    <AlertCircle className="w-8 h-8 opacity-80" />
                    <span className="text-2xl font-bold">{results.uncategorized_count}</span>
                  </div>
                  <h3 className="text-sm font-semibold opacity-90">Needs Review</h3>
                  <p className="text-xs opacity-75 mt-1">Manual categorization needed</p>
                </div>

                {/* Average Confidence */}
                <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-lg">
                  <div className="flex items-center justify-between mb-2">
                    <TrendingUp className="w-8 h-8 opacity-80" />
                    <span className="text-2xl font-bold">
                      {Math.round(results.average_confidence * 100)}%
                    </span>
                  </div>
                  <h3 className="text-sm font-semibold opacity-90">Avg Confidence</h3>
                  <p className="text-xs opacity-75 mt-1">AI categorization accuracy</p>
                </div>
              </div>
            </div>

            {/* Generated Excel Sheets */}
            <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-lg">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                <FileSpreadsheet className="w-5 h-5 text-purple-600" />
                Generated Excel Sheets
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="font-semibold text-gray-900">Summary</div>
                  <div className="text-xs text-gray-600 mt-1">Key financial metrics & KPIs</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="font-semibold text-gray-900">Revenue</div>
                  <div className="text-xs text-gray-600 mt-1">Revenue breakdown by category</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="font-semibold text-gray-900">Direct Costs</div>
                  <div className="text-xs text-gray-600 mt-1">Direct cost categorization</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="font-semibold text-gray-900">Indirect Costs</div>
                  <div className="text-xs text-gray-600 mt-1">Overhead & operating expenses</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="font-semibold text-gray-900">Transactions</div>
                  <div className="text-xs text-gray-600 mt-1">Complete transaction history</div>
                </div>
              </div>

              <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-4">
                <div className="text-xs font-medium text-gray-600 mb-1">Generated File:</div>
                <div className="text-sm font-mono text-gray-900 break-all">{results.excel_path}</div>
              </div>

              <button
                type="button"
                onClick={async (e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  console.log('Download button clicked');
                  console.log('Current project:', currentProject);

                  try {
                    const token = localStorage.getItem('token');
                    console.log('Token exists:', !!token);

                    const downloadUrl = `/api/financial-builder/${currentProject}/download`;
                    console.log('Download URL:', downloadUrl);

                    console.log('Starting fetch...');
                    const response = await fetch(downloadUrl, {
                      headers: {
                        'Authorization': `Bearer ${token}`
                      }
                    });

                    console.log('Response status:', response.status);
                    console.log('Response ok:', response.ok);

                    if (!response.ok) {
                      const errorText = await response.text();
                      console.error('Error response:', errorText);
                      throw new Error(`Download failed: ${response.status} - ${errorText}`);
                    }

                    console.log('Creating blob...');
                    const blob = await response.blob();
                    console.log('Blob size:', blob.size, 'type:', blob.type);

                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `Financial_Model_${currentProject}.xlsx`;
                    document.body.appendChild(a);
                    console.log('Triggering download...');
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    console.log('Download complete!');
                  } catch (error) {
                    console.error('Download error:', error);
                    alert(`Failed to download file: ${error instanceof Error ? error.message : 'Unknown error'}`);
                  }
                }}
                className="w-full bg-gradient-to-r from-purple-600 to-indigo-700 text-white py-3 px-6 rounded-lg hover:from-purple-700 hover:to-indigo-800 transition-all duration-200 font-semibold flex items-center justify-center gap-2"
              >
                <Download className="w-5 h-5" />
                Download Financial Model.xlsx
              </button>
            </div>

            {/* Process Another Button */}
            <div className="text-center">
              <button
                onClick={() => {
                  setResults(null);
                  setJobId(null);
                  setStages(stages.map(s => ({ ...s, status: 'pending', progress: 0 })));
                }}
                className="px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
              >
                Process Another Project
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
