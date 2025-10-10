import { useState } from 'react';
import { FileText, CheckCircle2, AlertCircle, Eye, Edit2, GitCompare, Clock } from 'lucide-react';
import {
  DEMO_PROJECTS,
  DEMO_EXTRACTED_FILES,
  DEMO_TRANSACTIONS,
  DEMO_CONFLICTS,
  DEMO_BATCH_JOBS
} from '../../services/demoData';

export function DemoFinancialWorkflow() {
  const [selectedProject, setSelectedProject] = useState(DEMO_PROJECTS[0].id);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<'files' | 'transactions' | 'conflicts' | 'jobs'>('files');

  const currentProject = DEMO_PROJECTS.find(p => p.id === selectedProject);
  const fileTransactions = selectedFile
    ? DEMO_TRANSACTIONS.filter(t => t.file_id === selectedFile)
    : DEMO_TRANSACTIONS;

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <div className="space-y-6">
      {/* Demo Mode Banner */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="font-semibold text-blue-900 mb-1">📊 Demo Mode Active</h3>
            <p className="text-sm text-blue-700 mb-3">
              Exploring real construction project data from <strong>{currentProject?.name}</strong>.
              This demonstrates the AI-powered financial extraction and processing workflow without needing a backend API.
            </p>

            {/* Project Selector */}
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium text-blue-900">Select Project:</label>
              <select
                value={selectedProject}
                onChange={(e) => setSelectedProject(e.target.value)}
                className="px-3 py-1.5 border border-blue-300 rounded-lg bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {DEMO_PROJECTS.map(project => (
                  <option key={project.id} value={project.id}>
                    {project.name} - {project.client}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex gap-1 p-2">
            <button
              onClick={() => setSelectedTab('files')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedTab === 'files'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <FileText className="w-4 h-4" />
              Extracted Files ({DEMO_EXTRACTED_FILES.length})
            </button>
            <button
              onClick={() => setSelectedTab('transactions')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedTab === 'transactions'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <Edit2 className="w-4 h-4" />
              Transactions ({DEMO_TRANSACTIONS.length})
            </button>
            <button
              onClick={() => setSelectedTab('conflicts')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedTab === 'conflicts'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <GitCompare className="w-4 h-4" />
              Conflicts ({DEMO_CONFLICTS.length})
            </button>
            <button
              onClick={() => setSelectedTab('jobs')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedTab === 'jobs'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <Clock className="w-4 h-4" />
              Batch Jobs ({DEMO_BATCH_JOBS.filter(j => j.status === 'active').length})
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {selectedTab === 'files' && (
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-4">📁 Extracted Files</h3>
              <p className="text-sm text-gray-600 mb-4">
                Files uploaded from <strong>/{currentProject?.id}/data/</strong>. AI has extracted financial data, classified documents, and assigned confidence scores.
              </p>

              <div className="space-y-3">
                {DEMO_EXTRACTED_FILES.map(file => (
                  <div
                    key={file.file_id}
                    className={`p-4 border rounded-lg cursor-pointer transition-all ${
                      selectedFile === file.file_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                    onClick={() => setSelectedFile(selectedFile === file.file_id ? null : file.file_id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3 flex-1">
                        <FileText className="w-5 h-5 text-gray-400 mt-1" />
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold text-gray-900">{file.filename}</h4>
                            <span className="px-2 py-0.5 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                              <CheckCircle2 className="w-3 h-3 inline mr-1" />
                              Completed
                            </span>
                          </div>
                          <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
                            <div className="text-gray-600">
                              <span className="font-medium">Folder:</span> {file.folder}
                            </div>
                            <div className="text-gray-600">
                              <span className="font-medium">Type:</span> {file.document_classification}
                            </div>
                            <div className="text-gray-600">
                              <span className="font-medium">Uploaded:</span> {formatDate(file.upload_date)}
                            </div>
                            <div className="text-gray-600">
                              <span className="font-medium">Confidence:</span>{' '}
                              <span className={`font-semibold ${file.confidence_score >= 0.9 ? 'text-green-600' : 'text-yellow-600'}`}>
                                {Math.round(file.confidence_score * 100)}%
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      {selectedFile === file.file_id && (
                        <Eye className="w-5 h-5 text-blue-600" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {selectedTab === 'transactions' && (
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-4">✏️ Transaction Editor</h3>
              <p className="text-sm text-gray-600 mb-4">
                AI-extracted transactions from financial documents. Edit descriptions, amounts, or categories as needed.
                {selectedFile && ` Showing transactions from ${DEMO_EXTRACTED_FILES.find(f => f.file_id === selectedFile)?.filename}.`}
              </p>

              {selectedFile && (
                <button
                  onClick={() => setSelectedFile(null)}
                  className="mb-4 text-sm text-blue-600 hover:text-blue-700 font-medium"
                >
                  ← Show all transactions
                </button>
              )}

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200 bg-gray-50">
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Date</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Description</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Category</th>
                      <th className="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase">Amount</th>
                      <th className="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase">Confidence</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">Source</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {fileTransactions.map(txn => (
                      <tr key={txn.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3 text-sm text-gray-900">{formatDate(txn.date)}</td>
                        <td className="px-4 py-3 text-sm text-gray-900 font-medium">{txn.description}</td>
                        <td className="px-4 py-3 text-sm">
                          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                            {txn.category}
                          </span>
                        </td>
                        <td className={`px-4 py-3 text-sm text-right font-semibold ${
                          txn.transaction_type === 'income' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {txn.transaction_type === 'income' ? '+' : '-'}{formatCurrency(txn.amount)}
                        </td>
                        <td className="px-4 py-3 text-sm text-center">
                          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                            txn.confidence >= 0.9 ? 'bg-green-100 text-green-700' :
                            txn.confidence >= 0.8 ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>
                            {Math.round(txn.confidence * 100)}%
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-600">{txn.source_location}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {selectedTab === 'conflicts' && (
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-4">⚖️ Conflict Resolution</h3>
              <p className="text-sm text-gray-600 mb-4">
                Duplicate transactions found across multiple files. The system auto-selects the highest confidence version, but you can override.
              </p>

              <div className="space-y-4">
                {DEMO_CONFLICTS.map(conflict => (
                  <div key={conflict.id} className="border border-yellow-200 bg-yellow-50 rounded-lg p-4">
                    <div className="flex items-start gap-3 mb-3">
                      <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="font-semibold text-gray-900">{conflict.transaction_description}</h4>
                        <p className="text-sm text-gray-600">
                          {formatCurrency(conflict.amount)} on {formatDate(conflict.date)} — Found in {conflict.occurrences.length} files
                        </p>
                      </div>
                    </div>

                    <div className="space-y-2 ml-8">
                      {conflict.occurrences.map((occ, idx) => (
                        <div
                          key={idx}
                          className={`p-3 rounded-lg border-2 ${
                            occ.selected
                              ? 'border-green-500 bg-green-50'
                              : 'border-gray-200 bg-white'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <input
                                type="radio"
                                checked={occ.selected}
                                readOnly
                                className="w-4 h-4 text-green-600"
                              />
                              <div>
                                <div className="font-medium text-gray-900">{occ.filename}</div>
                                <div className="text-sm text-gray-600">
                                  Source: {occ.source_location} • Confidence: {Math.round(occ.confidence * 100)}%
                                </div>
                              </div>
                            </div>
                            {occ.selected && (
                              <span className="px-2 py-1 bg-green-600 text-white rounded-full text-xs font-semibold">
                                Selected
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {selectedTab === 'jobs' && (
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-4">⏰ Scheduled Batch Jobs</h3>
              <p className="text-sm text-gray-600 mb-4">
                Automated tasks that run on a schedule to aggregate data, detect conflicts, and generate reports.
              </p>

              <div className="space-y-3">
                {DEMO_BATCH_JOBS.map(job => (
                  <div key={job.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <Clock className="w-5 h-5 text-gray-400" />
                        <div>
                          <h4 className="font-semibold text-gray-900">{job.name}</h4>
                          <p className="text-sm text-gray-600">{job.description}</p>
                        </div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        job.status === 'active'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-gray-100 text-gray-600'
                      }`}>
                        {job.status.toUpperCase()}
                      </span>
                    </div>

                    <div className="grid grid-cols-4 gap-4 mt-3 text-sm">
                      <div>
                        <div className="text-gray-600 font-medium">Schedule</div>
                        <div className="text-gray-900 font-mono text-xs">{job.schedule}</div>
                      </div>
                      <div>
                        <div className="text-gray-600 font-medium">Last Run</div>
                        <div className="text-gray-900">{job.last_run ? formatDate(job.last_run) : 'Never'}</div>
                      </div>
                      <div>
                        <div className="text-gray-600 font-medium">Next Run</div>
                        <div className="text-gray-900">{job.next_run ? formatDate(job.next_run) : 'N/A'}</div>
                      </div>
                      <div>
                        <div className="text-gray-600 font-medium">Success Rate</div>
                        <div className="text-green-600 font-semibold">{Math.round(job.success_rate * 100)}%</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
