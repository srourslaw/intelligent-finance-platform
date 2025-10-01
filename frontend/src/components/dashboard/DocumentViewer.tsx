import { useState, useEffect } from 'react';
import { FileText, Download, FolderOpen, File, Image, FileSpreadsheet } from 'lucide-react';
import { Document, Page, pdfjs } from 'react-pdf';
import * as XLSX from 'xlsx';
import { getDocumentList, getDocumentDownloadUrl } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

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

interface DocumentViewerProps {
  projectId: string;
}

export function DocumentViewer({ projectId }: DocumentViewerProps) {
  const { token } = useAuth();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [documentsByFolder, setDocumentsByFolder] = useState<DocumentsByFolder>({});
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [loading, setLoading] = useState(true);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());

  // PDF state
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);

  // Excel state
  const [excelData, setExcelData] = useState<any>(null);
  const [selectedSheet, setSelectedSheet] = useState<string>('');

  useEffect(() => {
    const fetchDocuments = async () => {
      if (!token || !projectId) return;

      try {
        setLoading(true);
        const response = await getDocumentList(projectId, token);

        if (response.error) {
          setError(response.error);
          return;
        }

        if (response.data) {
          // Filter to only show supported file types (Excel, PDF, Images)
          const supportedDocs = response.data.filter((doc: Document) =>
            doc.type === 'excel' || doc.type === 'pdf' || doc.type === 'image'
          );

          setDocuments(supportedDocs);

          // Group by folder
          const grouped: DocumentsByFolder = {};
          supportedDocs.forEach((doc: Document) => {
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
  }, [token, projectId]);

  const handleDocumentClick = async (doc: Document) => {
    setSelectedDocument(doc);
    setPreviewLoading(true);
    setError(null);
    setExcelData(null);
    setNumPages(0);
    setPageNumber(1);

    try {
      if (doc.type === 'excel') {
        // Fetch and parse Excel file
        const url = getDocumentDownloadUrl(projectId, doc.path);
        const response = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const arrayBuffer = await response.arrayBuffer();
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });

        setExcelData(workbook);
        // Select first non-empty sheet
        const firstNonEmptySheet = workbook.SheetNames.find(name => {
          const sheet = workbook.Sheets[name];
          const data = XLSX.utils.sheet_to_json(sheet);
          return data.length > 0;
        });
        setSelectedSheet(firstNonEmptySheet || workbook.SheetNames[0]);
      }
    } catch (err) {
      console.error('Preview error:', err);
      setError('Failed to preview document');
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

  const renderExcelPreview = () => {
    if (!excelData || !selectedSheet) return null;

    const sheet = excelData.Sheets[selectedSheet];
    const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 }) as any[][];

    if (jsonData.length === 0) {
      return <p className="text-gray-500">Sheet is empty</p>;
    }

    // Get headers (first row)
    const headers = jsonData[0] || [];
    const rows = jsonData.slice(1);

    return (
      <div className="space-y-4">
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Sheet:</label>
          <select
            value={selectedSheet}
            onChange={(e) => setSelectedSheet(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm"
          >
            {excelData.SheetNames.map((name: string) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
        </div>

        <div className="overflow-auto max-h-[500px] border border-gray-300 rounded">
          <table className="min-w-full text-xs border-collapse">
            <thead className="bg-gray-100 sticky top-0">
              <tr>
                {headers.map((header: any, idx: number) => (
                  <th key={idx} className="border border-gray-300 px-3 py-2 text-left font-semibold text-gray-900">
                    {header || `Column ${idx + 1}`}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.slice(0, 100).map((row: any[], rowIdx: number) => (
                <tr key={rowIdx} className={rowIdx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  {headers.map((_, cellIdx: number) => (
                    <td key={cellIdx} className="border border-gray-300 px-3 py-2 text-gray-900">
                      {row[cellIdx] ?? ''}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {rows.length > 100 && (
          <p className="text-sm text-gray-600">
            Showing first 100 of {rows.length} rows
          </p>
        )}
      </div>
    );
  };

  const renderPdfPreview = () => {
    if (!selectedDocument) return null;

    const url = getDocumentDownloadUrl(projectId, selectedDocument.path);

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-600">
            Page {pageNumber} of {numPages}
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}
              disabled={pageNumber <= 1}
              className="px-3 py-1 bg-gray-200 text-gray-700 rounded disabled:opacity-50 text-sm"
            >
              Previous
            </button>
            <button
              onClick={() => setPageNumber(Math.min(numPages, pageNumber + 1))}
              disabled={pageNumber >= numPages}
              className="px-3 py-1 bg-gray-200 text-gray-700 rounded disabled:opacity-50 text-sm"
            >
              Next
            </button>
          </div>
        </div>

        <div className="border border-gray-300 rounded overflow-auto">
          <Document
            file={url}
            onLoadSuccess={({ numPages }) => setNumPages(numPages)}
            loading={
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
              </div>
            }
            error={
              <div className="p-4 text-red-600">
                Failed to load PDF. Please try downloading the file.
              </div>
            }
          >
            <Page
              pageNumber={pageNumber}
              renderTextLayer={true}
              renderAnnotationLayer={true}
              className="mx-auto"
              width={800}
            />
          </Document>
        </div>
      </div>
    );
  };

  const renderImagePreview = () => {
    if (!selectedDocument) return null;

    const url = getDocumentDownloadUrl(projectId, selectedDocument.path);

    return (
      <div>
        <img
          src={url}
          alt={selectedDocument.filename}
          className="max-w-full h-auto rounded border border-gray-300"
        />
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

  if (error && documents.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Project Documents</h2>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-lg p-8 border border-gray-100">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Project Documents</h2>
        <p className="text-sm text-gray-600">
          Browse and preview all project files - Excel spreadsheets, PDFs, and images
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* File Browser */}
        <div className="lg:col-span-1 bg-white border border-gray-200 rounded-xl p-4 max-h-[600px] overflow-y-auto shadow-sm">
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
        <div className="lg:col-span-2 bg-white border border-gray-200 rounded-xl p-6 max-h-[600px] overflow-y-auto shadow-sm">
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
                  href={getDocumentDownloadUrl(projectId, selectedDocument.path)}
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

              {!previewLoading && (
                <div>
                  {selectedDocument.type === 'excel' && renderExcelPreview()}
                  {selectedDocument.type === 'pdf' && renderPdfPreview()}
                  {selectedDocument.type === 'image' && renderImagePreview()}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
