import { useState, useEffect } from 'react';
import { FileText, Download, FolderOpen, File, Image, FileSpreadsheet } from 'lucide-react';
import { getDocumentList, previewDocument, getDocumentDownloadUrl } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

interface Document {
  filename: string;
  path: string;
  type: string;
  size: number;
  modified: number;
  folder: string;
}

interface DocumentsByFolder {
  [folder: string]: Document[];
}

export function DocumentViewer() {
  const { token } = useAuth();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [documentsByFolder, setDocumentsByFolder] = useState<DocumentsByFolder>({});
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [preview, setPreview] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());

  useEffect(() => {
    const fetchDocuments = async () => {
      if (!token) return;

      try {
        setLoading(true);
        const response = await getDocumentList('project-a', token);

        if (response.error) {
          setError(response.error);
          return;
        }

        if (response.data) {
          setDocuments(response.data);

          // Group by folder
          const grouped: DocumentsByFolder = {};
          response.data.forEach((doc: Document) => {
            const folder = doc.folder || 'Root';
            if (!grouped[folder]) {
              grouped[folder] = [];
            }
            grouped[folder].push(doc);
          });

          setDocumentsByFolder(grouped);

          // Expand all folders by default
          setExpandedFolders(new Set(Object.keys(grouped)));
        }
      } catch (err) {
        setError('Failed to load documents');
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, [token]);

  const handleDocumentClick = async (doc: Document) => {
    setSelectedDocument(doc);
    setPreviewLoading(true);
    setPreview(null);

    try {
      const response = await previewDocument('project-a', doc.path, token!);

      if (response.error) {
        setPreview({ error: response.error });
      } else {
        setPreview(response.data);
      }
    } catch (err) {
      setPreview({ error: 'Failed to preview document' });
    } finally {
      setPreviewLoading(false);
    }
  };

  const toggleFolder = (folder: string) => {
    setExpandedFolders((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(folder)) {
        newSet.delete(folder);
      } else {
        newSet.add(folder);
      }
      return newSet;
    });
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'excel':
        return <FileSpreadsheet className="w-4 h-4 text-green-600" />;
      case 'pdf':
        return <FileText className="w-4 h-4 text-red-600" />;
      case 'image':
        return <Image className="w-4 h-4 text-blue-600" />;
      default:
        return <File className="w-4 h-4 text-gray-600" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const renderExcelPreview = (previewData: any) => {
    if (!previewData.sheets) return null;

    const firstSheetName = previewData.sheet_names?.[0];
    const sheet = previewData.sheets[firstSheetName];

    if (!sheet || sheet.error) {
      return <p className="text-red-600">Error loading Excel sheet</p>;
    }

    return (
      <div className="space-y-4">
        <h4 className="font-semibold text-gray-900">Sheet: {firstSheetName}</h4>
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300 text-xs">
            <thead className="bg-gray-50">
              <tr>
                {sheet.columns.map((col: string, idx: number) => (
                  <th key={idx} className="border border-gray-300 px-2 py-1 text-left font-medium text-gray-700">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sheet.data.slice(0, 20).map((row: any[], rowIdx: number) => (
                <tr key={rowIdx} className={rowIdx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  {row.map((cell: any, cellIdx: number) => (
                    <td key={cellIdx} className="border border-gray-300 px-2 py-1 text-gray-900">
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {sheet.total_rows > 20 && (
          <p className="text-sm text-gray-600">
            Showing first 20 of {sheet.total_rows} rows
          </p>
        )}
      </div>
    );
  };

  const renderPdfPreview = (previewData: any) => {
    if (!previewData.pages) return null;

    return (
      <div className="space-y-4">
        <p className="text-sm text-gray-600">
          {previewData.page_count} pages total (showing first 3)
        </p>
        {previewData.pages.slice(0, 3).map((page: any) => (
          <div key={page.page_number} className="border border-gray-300 p-4 rounded">
            <h4 className="font-semibold text-gray-900 mb-2">Page {page.page_number}</h4>
            <pre className="text-xs text-gray-700 whitespace-pre-wrap">{page.text}</pre>
          </div>
        ))}
      </div>
    );
  };

  const renderImagePreview = (previewData: any) => {
    if (!previewData.data) return null;

    return (
      <div>
        <img src={previewData.data} alt={previewData.filename} className="max-w-full h-auto rounded" />
      </div>
    );
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Project Documents</h2>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Project Documents</h2>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Project Documents</h2>
        <p className="text-sm text-gray-600 mt-1">
          Access all project files - Excel sheets, PDFs, and images
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* File Browser */}
        <div className="lg:col-span-1 border border-gray-200 rounded-lg p-4 max-h-[600px] overflow-y-auto">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <FolderOpen className="w-5 h-5" />
            Files ({documents.length})
          </h3>

          {Object.keys(documentsByFolder).sort().map((folder) => (
            <div key={folder} className="mb-2">
              <button
                onClick={() => toggleFolder(folder)}
                className="w-full text-left flex items-center gap-2 px-2 py-1 hover:bg-gray-50 rounded"
              >
                <FolderOpen className="w-4 h-4 text-yellow-600" />
                <span className="text-sm font-medium text-gray-700 truncate">{folder}</span>
                <span className="text-xs text-gray-500">({documentsByFolder[folder].length})</span>
              </button>

              {expandedFolders.has(folder) && (
                <div className="ml-6 mt-1 space-y-1">
                  {documentsByFolder[folder].map((doc) => (
                    <button
                      key={doc.path}
                      onClick={() => handleDocumentClick(doc)}
                      className={`w-full text-left flex items-center gap-2 px-2 py-2 rounded text-sm hover:bg-indigo-50 ${
                        selectedDocument?.path === doc.path ? 'bg-indigo-100' : ''
                      }`}
                    >
                      {getFileIcon(doc.type)}
                      <div className="flex-1 min-w-0">
                        <p className="text-gray-900 truncate">{doc.filename}</p>
                        <p className="text-xs text-gray-500">{formatFileSize(doc.size)}</p>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Preview Panel */}
        <div className="lg:col-span-2 border border-gray-200 rounded-lg p-4 max-h-[600px] overflow-y-auto">
          {!selectedDocument && (
            <div className="flex items-center justify-center h-full text-gray-500">
              <p>Select a document to preview</p>
            </div>
          )}

          {selectedDocument && (
            <div>
              <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-200">
                <div className="flex items-center gap-3">
                  {getFileIcon(selectedDocument.type)}
                  <div>
                    <h3 className="font-semibold text-gray-900">{selectedDocument.filename}</h3>
                    <p className="text-xs text-gray-500">{formatFileSize(selectedDocument.size)}</p>
                  </div>
                </div>
                <a
                  href={getDocumentDownloadUrl('project-a', selectedDocument.path)}
                  download
                  className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 text-sm"
                >
                  <Download className="w-4 h-4" />
                  Download
                </a>
              </div>

              {previewLoading && (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                </div>
              )}

              {!previewLoading && preview && (
                <div>
                  {preview.error && <p className="text-red-600">{preview.error}</p>}
                  {preview.type === 'excel' && renderExcelPreview(preview)}
                  {preview.type === 'pdf' && renderPdfPreview(preview)}
                  {preview.type === 'image' && renderImagePreview(preview)}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
