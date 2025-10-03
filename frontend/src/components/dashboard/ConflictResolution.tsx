import { useState, useEffect } from 'react';
import { AlertTriangle, Check, X, ArrowRight, Info } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Transaction {
  date: string | null;
  description: string;
  category: string | null;
  amount: number;
  transaction_type: string;
  confidence: number;
  source_location: string;
  file_id?: string;
  file_name?: string;
}

interface ConflictGroup {
  key: string; // (date, description, amount)
  transactions: Transaction[];
  resolution: 'auto' | 'manual' | 'pending';
  selected_index?: number;
}

export function ConflictResolution() {
  const { token } = useAuth();
  const [files, setFiles] = useState<any[]>([]);
  const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);
  const [conflicts, setConflicts] = useState<ConflictGroup[]>([]);
  const [loading, setLoading] = useState(false);
  const [showOnlyConflicts, setShowOnlyConflicts] = useState(true);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/extraction/list`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFiles(response.data.filter((f: any) => f.extraction_status === 'completed'));
    } catch (err) {
      console.error('Error fetching files:', err);
    }
  };

  const toggleFileSelection = (fileId: string) => {
    setSelectedFileIds(prev =>
      prev.includes(fileId)
        ? prev.filter(id => id !== fileId)
        : [...prev, fileId]
    );
  };

  const detectConflicts = async () => {
    if (selectedFileIds.length < 2) {
      alert('Please select at least 2 files to detect conflicts');
      return;
    }

    setLoading(true);
    try {
      // Load all transactions from selected files
      const allTransactions: Transaction[] = [];

      for (const fileId of selectedFileIds) {
        const response = await axios.get(`${API_BASE_URL}/extraction/result/${fileId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        const fileName = files.find(f => f.file_id === fileId)?.filename || fileId;

        response.data.extracted_data.transactions.forEach((txn: Transaction) => {
          allTransactions.push({
            ...txn,
            file_id: fileId,
            file_name: fileName
          });
        });
      }

      // Group by (date, description, amount)
      const groups: Map<string, Transaction[]> = new Map();

      allTransactions.forEach(txn => {
        const key = `${txn.date}__${txn.description.toLowerCase().trim()}__${txn.amount}`;
        if (!groups.has(key)) {
          groups.set(key, []);
        }
        groups.get(key)!.push(txn);
      });

      // Convert to conflict groups
      const conflictGroups: ConflictGroup[] = [];

      groups.forEach((transactions, key) => {
        if (transactions.length > 1) {
          // Sort by confidence (highest first)
          transactions.sort((a, b) => b.confidence - a.confidence);

          conflictGroups.push({
            key,
            transactions,
            resolution: 'auto',
            selected_index: 0 // Auto-select highest confidence
          });
        }
      });

      setConflicts(conflictGroups);
    } catch (err) {
      console.error('Error detecting conflicts:', err);
    } finally {
      setLoading(false);
    }
  };

  const selectTransaction = (groupIndex: number, transactionIndex: number) => {
    setConflicts(prev => {
      const newConflicts = [...prev];
      newConflicts[groupIndex] = {
        ...newConflicts[groupIndex],
        selected_index: transactionIndex,
        resolution: 'manual'
      };
      return newConflicts;
    });
  };

  const applyResolutions = async () => {
    // In a real implementation, this would save the resolved conflicts
    // and update the aggregation accordingly
    alert(`Applied ${conflicts.length} conflict resolutions. In production, this would update the aggregation.`);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const displayedConflicts = showOnlyConflicts
    ? conflicts
    : conflicts; // In future, could show all transaction groups

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">⚖️ Conflict Resolution</h2>
        <p className="text-sm text-gray-600 mb-4">
          Detect and resolve duplicate transactions across multiple files. The system automatically selects the transaction with the highest confidence, but you can manually override.
        </p>

        {/* File Selection */}
        <div className="mb-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Select Files to Compare</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {files.map((file) => (
              <button
                key={file.file_id}
                onClick={() => toggleFileSelection(file.file_id)}
                className={`p-3 rounded-lg border-2 text-left transition-all ${
                  selectedFileIds.includes(file.file_id)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={selectedFileIds.includes(file.file_id)}
                    onChange={() => {}}
                    className="rounded text-blue-600"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{file.filename}</p>
                    <p className="text-xs text-gray-500">{new Date(file.upload_date).toLocaleDateString()}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={detectConflicts}
            disabled={loading || selectedFileIds.length < 2}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Detecting...' : 'Detect Conflicts'}
          </button>

          {conflicts.length > 0 && (
            <>
              <button
                onClick={applyResolutions}
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Apply Resolutions ({conflicts.length})
              </button>

              <label className="flex items-center gap-2 text-sm text-gray-700">
                <input
                  type="checkbox"
                  checked={showOnlyConflicts}
                  onChange={(e) => setShowOnlyConflicts(e.target.checked)}
                  className="rounded text-blue-600"
                />
                Show only conflicts
              </label>
            </>
          )}
        </div>
      </div>

      {/* Conflicts List */}
      {conflicts.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-gray-900">
              Found {conflicts.length} Conflict{conflicts.length !== 1 ? 's' : ''}
            </h3>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded"></div>
                <span className="text-gray-600">Auto-resolved: {conflicts.filter(c => c.resolution === 'auto').length}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-500 rounded"></div>
                <span className="text-gray-600">Manual: {conflicts.filter(c => c.resolution === 'manual').length}</span>
              </div>
            </div>
          </div>

          {displayedConflicts.map((conflict, groupIndex) => (
            <div key={conflict.key} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="p-4 bg-yellow-50 border-b border-yellow-200 flex items-center gap-3">
                <AlertTriangle className="w-5 h-5 text-yellow-600" />
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">{conflict.transactions[0].description}</h4>
                  <p className="text-sm text-gray-600">
                    {conflict.transactions[0].date} • {formatCurrency(conflict.transactions[0].amount)} •
                    {conflict.transactions.length} duplicate{conflict.transactions.length !== 1 ? 's' : ''} found
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  conflict.resolution === 'auto'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-blue-100 text-blue-700'
                }`}>
                  {conflict.resolution === 'auto' ? 'Auto-resolved' : 'Manual'}
                </span>
              </div>

              <div className="p-4 space-y-3">
                {conflict.transactions.map((txn, txnIndex) => (
                  <div
                    key={txnIndex}
                    className={`relative p-4 rounded-lg border-2 transition-all cursor-pointer ${
                      conflict.selected_index === txnIndex
                        ? 'border-green-500 bg-green-50'
                        : 'border-gray-200 hover:border-green-300'
                    }`}
                    onClick={() => selectTransaction(groupIndex, txnIndex)}
                  >
                    {/* Selection Indicator */}
                    {conflict.selected_index === txnIndex && (
                      <div className="absolute top-2 right-2">
                        <div className="flex items-center gap-1 px-2 py-1 bg-green-600 text-white rounded-full text-xs font-medium">
                          <Check className="w-3 h-3" />
                          Selected
                        </div>
                      </div>
                    )}

                    <div className="grid grid-cols-5 gap-4">
                      <div>
                        <p className="text-xs text-gray-500">Source File</p>
                        <p className="text-sm font-medium text-gray-900 truncate" title={txn.file_name}>
                          {txn.file_name}
                        </p>
                      </div>

                      <div>
                        <p className="text-xs text-gray-500">Category</p>
                        <p className="text-sm font-medium text-gray-900">
                          {txn.category || 'Unclassified'}
                        </p>
                      </div>

                      <div>
                        <p className="text-xs text-gray-500">Type</p>
                        <p className="text-sm">
                          <span className={`px-2 py-1 rounded text-xs ${
                            txn.transaction_type === 'debit'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-green-100 text-green-700'
                          }`}>
                            {txn.transaction_type}
                          </span>
                        </p>
                      </div>

                      <div>
                        <p className="text-xs text-gray-500">Confidence</p>
                        <p className="text-sm">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            txn.confidence > 0.8
                              ? 'bg-green-100 text-green-700'
                              : txn.confidence > 0.5
                              ? 'bg-yellow-100 text-yellow-700'
                              : 'bg-red-100 text-red-700'
                          }`}>
                            {(txn.confidence * 100).toFixed(0)}%
                          </span>
                        </p>
                      </div>

                      <div>
                        <p className="text-xs text-gray-500">Source Location</p>
                        <p className="text-sm font-mono text-gray-600">{txn.source_location}</p>
                      </div>
                    </div>

                    {/* Recommendation Badge */}
                    {txnIndex === 0 && conflict.resolution === 'auto' && (
                      <div className="mt-2 flex items-center gap-2 text-xs text-green-700">
                        <Info className="w-4 h-4" />
                        <span>Recommended: Highest confidence score</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Resolution Summary */}
              <div className="p-4 bg-gray-50 border-t border-gray-200">
                <div className="flex items-center gap-3 text-sm">
                  <span className="text-gray-600">Resolution:</span>
                  <ArrowRight className="w-4 h-4 text-gray-400" />
                  <span className="font-medium text-gray-900">
                    Keep transaction from {conflict.transactions[conflict.selected_index || 0].file_name}
                  </span>
                  <span className="text-gray-500">
                    (Discard {conflict.transactions.length - 1} duplicate{conflict.transactions.length - 1 !== 1 ? 's' : ''})
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {selectedFileIds.length >= 2 && conflicts.length === 0 && !loading && (
        <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
          <Check className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-gray-900 mb-2">No Conflicts Found</h3>
          <p className="text-gray-600">
            All transactions are unique across the selected files. No duplicates detected.
          </p>
        </div>
      )}
    </div>
  );
}
