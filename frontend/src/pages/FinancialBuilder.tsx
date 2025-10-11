import { useState } from 'react';
import { FileSpreadsheet, Zap, CheckCircle2, Loader2, AlertCircle, TrendingUp, Database } from 'lucide-react';

interface PipelineStage {
  name: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: number;
  details: string;
  filesProcessed?: number;
  totalFiles?: number;
}

export default function FinancialBuilder() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [stages, setStages] = useState<PipelineStage[]>([
    { name: 'File Extraction', status: 'pending', progress: 0, details: 'Extract data from 144 files (PDFs, Excel)', filesProcessed: 0, totalFiles: 144 },
    { name: 'AI Categorization', status: 'pending', progress: 0, details: 'Map transactions to MASTER template categories' },
    { name: 'Data Aggregation', status: 'pending', progress: 0, details: 'Aggregate and validate all extracted data' },
    { name: 'Excel Population', status: 'pending', progress: 0, details: 'Populate Financial Model spreadsheet' },
  ]);
  const [finalExcelPath, setFinalExcelPath] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startPipeline = async () => {
    setIsProcessing(true);
    setError(null);
    setFinalExcelPath(null);

    try {
      // TODO: Implement API calls
      console.log('Starting full pipeline...');

      // For now, simulate the process
      alert('Full pipeline not yet implemented - backend endpoints needed!');

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Pipeline failed');
    } finally {
      setIsProcessing(false);
    }
  };

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
                AI-powered extraction from 144 files → Automated financial model population
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 py-8 space-y-8">
        {/* Info Card */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-lg">
          <div className="flex items-start gap-4">
            <Database className="w-8 h-8 text-purple-600 flex-shrink-0" />
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">How It Works</h2>
              <div className="text-sm text-gray-600 space-y-2">
                <p>
                  <strong>1. Extract:</strong> Process all PDFs and Excel files in your project folder using MinerU AI
                </p>
                <p>
                  <strong>2. Categorize:</strong> AI maps each transaction to the MASTER Financial Statement Template
                </p>
                <p>
                  <strong>3. Aggregate:</strong> Combine and validate all data with confidence scores
                </p>
                <p>
                  <strong>4. Populate:</strong> Automatically fill your Financial Model Excel with verified data
                </p>
              </div>
              <div className="mt-4 p-3 bg-purple-50 border border-purple-200 rounded-lg">
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-purple-600" />
                  <span className="text-sm font-semibold text-purple-900">
                    Project: project-a-123-sunset-blvd • 144 files ready for processing
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Start Button */}
        {!isProcessing && stages.every(s => s.status === 'pending') && (
          <div className="text-center">
            <button
              onClick={startPipeline}
              className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white py-4 px-8 rounded-xl hover:from-purple-700 hover:to-indigo-800 transition-all duration-200 font-bold text-lg shadow-lg flex items-center gap-3 mx-auto"
            >
              <Zap className="w-6 h-6" />
              Start Full Pipeline Processing
            </button>
          </div>
        )}

        {/* Pipeline Stages */}
        {(isProcessing || stages.some(s => s.status !== 'pending')) && (
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
                    {stage.filesProcessed !== undefined && (
                      <div className="text-sm font-semibold text-gray-900">
                        {stage.filesProcessed} / {stage.totalFiles} files
                      </div>
                    )}
                    <div className="text-sm text-gray-600">
                      {stage.progress}%
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
              <div>
                <h3 className="font-bold text-red-900 mb-1">Pipeline Error</h3>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Success & Download */}
        {finalExcelPath && (
          <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-6 h-6 text-green-600 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="font-bold text-green-900 mb-2">✨ Financial Model Successfully Generated!</h3>
                <p className="text-sm text-green-700 mb-4">
                  All 144 files have been processed and your financial statements are ready.
                </p>
                <div className="bg-white border border-green-300 rounded-lg p-3 mb-4">
                  <div className="text-xs font-medium text-gray-600 mb-1">Generated File:</div>
                  <div className="text-sm font-mono text-gray-900">{finalExcelPath}</div>
                </div>
                <button
                  className="bg-gradient-to-r from-green-600 to-green-700 text-white py-3 px-6 rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-200 font-semibold flex items-center gap-2"
                >
                  <FileSpreadsheet className="w-5 h-5" />
                  Download Financial Model.xlsx
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
