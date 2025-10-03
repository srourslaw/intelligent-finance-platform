import { useState, useEffect } from 'react';
import { Save, X, Edit2, Trash2, Plus, AlertCircle, CheckCircle, Search, Filter } from 'lucide-react';
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
}

interface ExtractionResult {
  metadata: {
    file_id: string;
    original_filename: string;
    file_type: string;
    extraction_date: string;
  };
  extracted_data: {
    transactions: Transaction[];
  };
}

export function TransactionEditor() {
  const { token } = useAuth();
  const [files, setFiles] = useState<any[]>([]);
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);
  const [extractionResult, setExtractionResult] = useState<ExtractionResult | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editedTransaction, setEditedTransaction] = useState<Transaction | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [hasChanges, setHasChanges] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  useEffect(() => {
    fetchFiles();
  }, []);

  useEffect(() => {
    if (selectedFileId) {
      loadTransactions(selectedFileId);
    }
  }, [selectedFileId]);

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

  const loadTransactions = async (fileId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/extraction/result/${fileId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setExtractionResult(response.data);
      setTransactions(response.data.extracted_data.transactions);
      setHasChanges(false);
    } catch (err) {
      console.error('Error loading transactions:', err);
    }
  };

  const startEdit = (index: number) => {
    setEditingIndex(index);
    setEditedTransaction({ ...transactions[index] });
  };

  const cancelEdit = () => {
    setEditingIndex(null);
    setEditedTransaction(null);
  };

  const saveEdit = () => {
    if (editingIndex !== null && editedTransaction) {
      const newTransactions = [...transactions];
      newTransactions[editingIndex] = editedTransaction;
      setTransactions(newTransactions);
      setEditingIndex(null);
      setEditedTransaction(null);
      setHasChanges(true);
    }
  };

  const deleteTransaction = (index: number) => {
    if (confirm('Are you sure you want to delete this transaction?')) {
      const newTransactions = transactions.filter((_, i) => i !== index);
      setTransactions(newTransactions);
      setHasChanges(true);
    }
  };

  const addTransaction = () => {
    const newTransaction: Transaction = {
      date: new Date().toISOString().split('T')[0],
      description: 'New Transaction',
      category: null,
      amount: 0,
      transaction_type: 'debit',
      confidence: 1.0,
      source_location: 'manual_entry'
    };
    setTransactions([...transactions, newTransaction]);
    setEditingIndex(transactions.length);
    setEditedTransaction(newTransaction);
    setHasChanges(true);
  };

  const saveAllChanges = async () => {
    if (!selectedFileId || !extractionResult) return;

    setSaving(true);
    setSaveMessage(null);

    try {
      // Create updated extraction result
      const updatedResult = {
        ...extractionResult,
        extracted_data: {
          ...extractionResult.extracted_data,
          transactions: transactions
        }
      };

      // Save to backend
      await axios.put(`${API_BASE_URL}/extraction/result/${selectedFileId}`, updatedResult, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setHasChanges(false);
      setSaveMessage({ type: 'success', text: 'Changes saved successfully!' });
      setTimeout(() => setSaveMessage(null), 3000);
    } catch (err: any) {
      setSaveMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to save changes' });
    } finally {
      setSaving(false);
    }
  };

  const getUniqueCategories = () => {
    const categories = transactions
      .map(t => t.category)
      .filter((c): c is string => c !== null && c !== undefined);
    return Array.from(new Set(categories)).sort();
  };

  const filteredTransactions = transactions.filter(txn => {
    const matchesSearch = searchTerm === '' ||
      txn.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (txn.category && txn.category.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesCategory = filterCategory === 'all' || txn.category === filterCategory;

    return matchesSearch && matchesCategory;
  });

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">✏️ Transaction Editor</h2>
        <p className="text-sm text-gray-600">
          Edit, add, or delete transactions from extracted files. Changes are saved back to the extraction result.
        </p>

        {/* File Selector */}
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Select File</label>
          <select
            value={selectedFileId || ''}
            onChange={(e) => setSelectedFileId(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Choose a file...</option>
            {files.map((file) => (
              <option key={file.file_id} value={file.file_id}>
                {file.filename} - {new Date(file.upload_date).toLocaleDateString()} ({file.extraction_status})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Transaction List */}
      {selectedFileId && extractionResult && (
        <div className="bg-white rounded-xl border border-gray-200">
          {/* Toolbar */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900">
                {extractionResult.metadata.original_filename}
              </h3>
              <div className="flex items-center gap-3">
                <button
                  onClick={addTransaction}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Add Transaction
                </button>
                {hasChanges && (
                  <button
                    onClick={saveAllChanges}
                    disabled={saving}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
                  >
                    <Save className="w-4 h-4" />
                    {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                )}
              </div>
            </div>

            {/* Search and Filter */}
            <div className="grid grid-cols-2 gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search transactions..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div className="relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="all">All Categories</option>
                  {getUniqueCategories().map((cat) => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Save Message */}
            {saveMessage && (
              <div className={`mt-4 flex items-center gap-2 p-3 rounded-lg ${
                saveMessage.type === 'success'
                  ? 'bg-green-50 border border-green-200 text-green-700'
                  : 'bg-red-50 border border-red-200 text-red-700'
              }`}>
                {saveMessage.type === 'success' ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  <AlertCircle className="w-5 h-5" />
                )}
                <span className="text-sm font-medium">{saveMessage.text}</span>
              </div>
            )}
          </div>

          {/* Transaction Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Date</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Description</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Category</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500">Amount</th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500">Type</th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500">Confidence</th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredTransactions.map((txn) => {
                  const originalIndex = transactions.indexOf(txn);
                  const isEditing = editingIndex === originalIndex;

                  return (
                    <tr key={originalIndex} className={isEditing ? 'bg-blue-50' : 'hover:bg-gray-50'}>
                      <td className="px-4 py-3">
                        {isEditing ? (
                          <input
                            type="date"
                            value={editedTransaction?.date || ''}
                            onChange={(e) => setEditedTransaction({ ...editedTransaction!, date: e.target.value })}
                            className="w-full px-2 py-1 border border-gray-300 rounded"
                          />
                        ) : (
                          <span className="text-sm text-gray-700">{txn.date || 'N/A'}</span>
                        )}
                      </td>

                      <td className="px-4 py-3">
                        {isEditing ? (
                          <input
                            type="text"
                            value={editedTransaction?.description || ''}
                            onChange={(e) => setEditedTransaction({ ...editedTransaction!, description: e.target.value })}
                            className="w-full px-2 py-1 border border-gray-300 rounded"
                          />
                        ) : (
                          <span className="text-sm text-gray-900">{txn.description}</span>
                        )}
                      </td>

                      <td className="px-4 py-3">
                        {isEditing ? (
                          <select
                            value={editedTransaction?.category || ''}
                            onChange={(e) => setEditedTransaction({ ...editedTransaction!, category: e.target.value })}
                            className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                          >
                            <option value="">Unclassified</option>
                            {getUniqueCategories().map((cat) => (
                              <option key={cat} value={cat}>{cat}</option>
                            ))}
                          </select>
                        ) : (
                          <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                            {txn.category || 'Unclassified'}
                          </span>
                        )}
                      </td>

                      <td className="px-4 py-3 text-right">
                        {isEditing ? (
                          <input
                            type="number"
                            step="0.01"
                            value={editedTransaction?.amount || 0}
                            onChange={(e) => setEditedTransaction({ ...editedTransaction!, amount: parseFloat(e.target.value) })}
                            className="w-full px-2 py-1 border border-gray-300 rounded text-right"
                          />
                        ) : (
                          <span className="text-sm font-medium text-gray-900">{formatCurrency(txn.amount)}</span>
                        )}
                      </td>

                      <td className="px-4 py-3 text-center">
                        {isEditing ? (
                          <select
                            value={editedTransaction?.transaction_type || 'debit'}
                            onChange={(e) => setEditedTransaction({ ...editedTransaction!, transaction_type: e.target.value })}
                            className="px-2 py-1 border border-gray-300 rounded text-sm"
                          >
                            <option value="debit">Debit</option>
                            <option value="credit">Credit</option>
                          </select>
                        ) : (
                          <span className={`text-xs px-2 py-1 rounded ${
                            txn.transaction_type === 'debit'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-green-100 text-green-700'
                          }`}>
                            {txn.transaction_type}
                          </span>
                        )}
                      </td>

                      <td className="px-4 py-3 text-center">
                        <span className={`text-xs px-2 py-1 rounded ${
                          txn.confidence > 0.8
                            ? 'bg-green-100 text-green-700'
                            : txn.confidence > 0.5
                            ? 'bg-yellow-100 text-yellow-700'
                            : 'bg-red-100 text-red-700'
                        }`}>
                          {(txn.confidence * 100).toFixed(0)}%
                        </span>
                      </td>

                      <td className="px-4 py-3">
                        <div className="flex items-center justify-center gap-2">
                          {isEditing ? (
                            <>
                              <button
                                onClick={saveEdit}
                                className="p-1 text-green-600 hover:bg-green-50 rounded transition-colors"
                                title="Save"
                              >
                                <CheckCircle className="w-4 h-4" />
                              </button>
                              <button
                                onClick={cancelEdit}
                                className="p-1 text-red-600 hover:bg-red-50 rounded transition-colors"
                                title="Cancel"
                              >
                                <X className="w-4 h-4" />
                              </button>
                            </>
                          ) : (
                            <>
                              <button
                                onClick={() => startEdit(originalIndex)}
                                className="p-1 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                                title="Edit"
                              >
                                <Edit2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => deleteTransaction(originalIndex)}
                                className="p-1 text-red-600 hover:bg-red-50 rounded transition-colors"
                                title="Delete"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Summary */}
          <div className="p-6 border-t border-gray-200 bg-gray-50">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-sm text-gray-600">Total Transactions</p>
                <p className="text-2xl font-bold text-gray-900">{filteredTransactions.length}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Amount</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(filteredTransactions.reduce((sum, t) => sum + t.amount, 0))}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Avg Confidence</p>
                <p className="text-2xl font-bold text-gray-900">
                  {filteredTransactions.length > 0
                    ? ((filteredTransactions.reduce((sum, t) => sum + t.confidence, 0) / filteredTransactions.length) * 100).toFixed(0)
                    : 0}%
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
