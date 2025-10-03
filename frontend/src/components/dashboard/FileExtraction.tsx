import { useState, useEffect } from 'react';
import { Upload, FileText, Check, X, AlertCircle, Loader2, Download, Eye, Trash2 } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface ExtractedFile {
  file_id: string;
  filename: string;
  file_type: string;
  upload_date: string;
  extraction_status: string;
  confidence_score: number;
}

interface Transaction {
  date: string | null;
  description: string;
  category: string | null;
  amount: number;
  transaction_type: string;
  confidence: number;
  source_location: string;
}

interface ExtractionResult {
  metadata: {
    file_id: string;
    original_filename: string;
    file_type: string;
    confidence_score: number;
    document_classification: string;
  };
  extracted_data: {
    transactions: Transaction[];
  };
  extraction_notes: {
    warnings: string[];
    errors: string[];
  };
  data_quality: {
    completeness_score: number;
    consistency_check: string;
  };
  classification_stats: {
    total_items: number;
    classified: number;
    unmapped: number;
    avg_confidence: number;
  };
}

export function FileExtraction() {
  const { token } = useAuth();
  const [files, setFiles] = useState<ExtractedFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [viewingResult, setViewingResult] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchExtractedFiles();
    const interval = setInterval(fetchExtractedFiles, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchExtractedFiles = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/extraction/list`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFiles(response.data);
    } catch (err) {
      console.error('Error fetching files:', err);
    }
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setUploadProgress(0);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post(`${API_BASE_URL}/extraction/upload`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const progress = progressEvent.total
            ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
            : 0;
          setUploadProgress(progress);
        }
      });

      setSelectedFile(null);
      setUploadProgress(0);
      fetchExtractedFiles();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const viewExtractionResult = async (fileId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/extraction/result/${fileId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setViewingResult(response.data);
    } catch (err) {
      console.error('Error fetching result:', err);
    }
  };

  const deleteFile = async (fileId: string) => {
    if (!confirm('Are you sure you want to delete this file and its extraction results?')) {
      return;
    }

    try {
      await axios.delete(`${API_BASE_URL}/extraction/${fileId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchExtractedFiles();
      if (viewingResult?.metadata.file_id === fileId) {
        setViewingResult(null);
      }
    } catch (err) {
      console.error('Error deleting file:', err);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const getFileTypeIcon = (fileType: string) => {
    return <FileText className="w-5 h-5" />;
  };

  const getStatusBadge = (status: string) => {
    if (status === 'completed') {
      return (
        <span className="flex items-center gap-1 px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
          <Check className="w-3 h-3" />
          Completed
        </span>
      );
    } else if (status === 'processing') {
      return (
        <span className="flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
          <Loader2 className="w-3 h-3 animate-spin" />
          Processing
        </span>
      );
    } else {
      return (
        <span className="flex items-center gap-1 px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
          <X className="w-3 h-3" />
          Failed
        </span>
      );
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">📤 Upload Financial Documents</h2>

        <div className="space-y-4">
          {/* File Input */}
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
            <input
              type="file"
              id="file-upload"
              className="hidden"
              onChange={handleFileSelect}
              accept=".xlsx,.xls,.csv,.pdf,.jpg,.jpeg,.png"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer flex flex-col items-center"
            >
              <Upload className="w-12 h-12 text-gray-400 mb-3" />
              <p className="text-sm font-medium text-gray-700 mb-1">
                {selectedFile ? selectedFile.name : 'Click to upload or drag and drop'}
              </p>
              <p className="text-xs text-gray-500">
                Supports: Excel, CSV, PDF, Images (max 50MB)
              </p>
            </label>
          </div>

          {/* Upload Button */}
          {selectedFile && (
            <div className="flex items-center gap-3">
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {uploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Uploading... {uploadProgress}%
                  </>
                ) : (
                  <>
                    <Upload className="w-4 h-4" />
                    Upload & Extract
                  </>
                )}
              </button>

              <button
                onClick={() => {
                  setSelectedFile(null);
                  setError(null);
                }}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
              <AlertCircle className="w-5 h-5" />
              <span className="text-sm">{error}</span>
            </div>
          )}
        </div>
      </div>

      {/* Files List */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">📁 Extracted Files</h2>
        </div>

        <div className="divide-y divide-gray-200">
          {files.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p>No files uploaded yet</p>
            </div>
          ) : (
            files.map((file) => (
              <div key={file.file_id} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3 flex-1">
                    {getFileTypeIcon(file.file_type)}
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{file.filename}</p>
                      <p className="text-sm text-gray-500">
                        Uploaded: {new Date(file.upload_date).toLocaleString()}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    {file.extraction_status === 'completed' && (
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-700">
                          Confidence: {(file.confidence_score * 100).toFixed(0)}%
                        </p>
                      </div>
                    )}

                    {getStatusBadge(file.extraction_status)}

                    <div className="flex gap-2">
                      {file.extraction_status === 'completed' && (
                        <button
                          onClick={() => viewExtractionResult(file.file_id)}
                          className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="View Results"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                      )}

                      <button
                        onClick={() => deleteFile(file.file_id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Extraction Result Modal */}
      {viewingResult && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-gray-900">{viewingResult.metadata.original_filename}</h3>
                <p className="text-sm text-gray-500">
                  Type: {viewingResult.metadata.document_classification} |
                  Confidence: {(viewingResult.metadata.confidence_score * 100).toFixed(0)}%
                </p>
              </div>
              <button
                onClick={() => setViewingResult(null)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto flex-1">
              {/* Stats */}
              <div className="grid grid-cols-4 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-blue-600 font-medium">Total Items</p>
                  <p className="text-2xl font-bold text-blue-700">{viewingResult.classification_stats.total_items}</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <p className="text-sm text-green-600 font-medium">Classified</p>
                  <p className="text-2xl font-bold text-green-700">{viewingResult.classification_stats.classified}</p>
                </div>
                <div className="bg-yellow-50 p-4 rounded-lg">
                  <p className="text-sm text-yellow-600 font-medium">Unmapped</p>
                  <p className="text-2xl font-bold text-yellow-700">{viewingResult.classification_stats.unmapped}</p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <p className="text-sm text-purple-600 font-medium">Avg Confidence</p>
                  <p className="text-2xl font-bold text-purple-700">
                    {(viewingResult.classification_stats.avg_confidence * 100).toFixed(0)}%
                  </p>
                </div>
              </div>

              {/* Transactions */}
              <h4 className="font-bold text-gray-900 mb-3">Extracted Transactions</h4>
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Date</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Description</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Category</th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">Amount</th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">Confidence</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {viewingResult.extracted_data.transactions.map((txn, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-4 py-2 text-sm text-gray-700">{txn.date || 'N/A'}</td>
                        <td className="px-4 py-2 text-sm text-gray-900">{txn.description}</td>
                        <td className="px-4 py-2 text-sm">
                          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
                            {txn.category || 'Unclassified'}
                          </span>
                        </td>
                        <td className="px-4 py-2 text-sm text-right font-medium">{formatCurrency(txn.amount)}</td>
                        <td className="px-4 py-2 text-sm text-right">
                          <span className={`font-medium ${txn.confidence > 0.8 ? 'text-green-600' : txn.confidence > 0.5 ? 'text-yellow-600' : 'text-red-600'}`}>
                            {(txn.confidence * 100).toFixed(0)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
