import { useState, useEffect, useRef } from 'react';
import { FileText, Download, FolderOpen, File, Image, FileSpreadsheet } from 'lucide-react';
import { Document, Page, pdfjs } from 'react-pdf';
import { SpreadSheets } from '@mescius/spread-sheets-react';
import * as GC from '@mescius/spread-sheets';
import '@mescius/spread-sheets-io';
import { getDocumentList, getDocumentDownloadUrl } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import '@mescius/spread-sheets/styles/gc.spread.sheets.excel2013white.css';

// Configure PDF.js worker - use jsdelivr CDN
pdfjs.GlobalWorkerOptions.workerSrc = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

interface DocumentItem {
  filename: string;
  path: string;
  type: string;
  size: number;
  modified: number;
  folder: string;
}

interface DocumentsByFolder {
  [folder: string]: DocumentItem[];
}

interface DocumentViewerProps {
  projectId: string;
}

export function DocumentViewer({ projectId }: DocumentViewerProps) {
  const { token } = useAuth();
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [documentsByFolder, setDocumentsByFolder] = useState<DocumentsByFolder>({});
  const [selectedDocument, setSelectedDocument] = useState<DocumentItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());

  // PDF state
  const [pdfBlob, setPdfBlob] = useState<string | null>(null);
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);

  // SpreadJS state
  const spreadRef = useRef<GC.Spread.Sheets.Workbook | null>(null);

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
          // Filter to only show supported file types
          const supportedDocs = response.data.filter((doc: DocumentItem) =>
            doc.type === 'excel' || doc.type === 'pdf' || doc.type === 'image'
          );

          setDocuments(supportedDocs);

          // Group by folder
          const grouped: DocumentsByFolder = {};
          supportedDocs.forEach((doc: DocumentItem) => {
            const folder = doc.folder || 'Root';
            if (!grouped[folder]) {
              grouped[folder] = [];
            }
            grouped[folder].push(doc);
          });

          setDocumentsByFolder(grouped);
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

  // Cleanup blob URL on unmount
  useEffect(() => {
    return () => {
      if (pdfBlob) {
        URL.revokeObjectURL(pdfBlob);
      }
    };
  }, [pdfBlob]);

  const handleDocumentClick = async (doc: DocumentItem) => {
    console.log('=== Document clicked ===', doc.filename, 'Type:', doc.type);
    setSelectedDocument(doc);
    setPreviewLoading(true);
    setError(null);
    setPdfBlob(null);
    setNumPages(0);
    setPageNumber(1);

    try {
      const url = getDocumentDownloadUrl(projectId, doc.path);
      console.log('Fetching from URL:', url);

      // Fetch file with authentication
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('Response status:', response.status, response.ok);

      if (!response.ok) {
        throw new Error('Failed to fetch document');
      }

      const arrayBuffer = await response.arrayBuffer();
      console.log('ArrayBuffer received, size:', arrayBuffer.byteLength);

      if (doc.type === 'excel') {
        console.log('Loading Excel file...');
        console.log('spreadRef.current:', spreadRef.current);
        console.log('File info:', doc.filename, 'Size:', arrayBuffer.byteLength);

        // Load Excel file into SpreadJS
        if (!spreadRef.current) {
          console.error('SpreadJS not initialized! spreadRef.current is null');
          setError('SpreadJS viewer not ready. Please try again.');
          setPreviewLoading(false);
          return;
        }

        try {
          // Use SpreadJS built-in import method instead of ExcelIO
          const blob = new Blob([arrayBuffer], {
            type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          });

          console.log('Calling spreadRef.current.import() with blob...');
          (spreadRef.current as any).import(
            blob,
            () => {
              console.log('✅ Excel file imported successfully');
              console.log('Sheet count:', spreadRef.current?.getSheetCount());
              setPreviewLoading(false);
            },
            (error: any) => {
              console.error('❌ Excel import error:', error);
              setError('Failed to import Excel file: ' + (error?.errorMessage || error?.message || 'Unknown error'));
              setPreviewLoading(false);
            },
            {
              fileType: GC.Spread.Sheets.FileType.excel
            }
          );
        } catch (err) {
          console.error('❌ Excel load error:', err);
          setError('Failed to load Excel file: ' + (err instanceof Error ? err.message : 'Unknown error'));
          setPreviewLoading(false);
        }
      } else if (doc.type === 'pdf') {
        console.log('Loading PDF file...');
        // Create blob URL for PDF
        const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
        const blobUrl = URL.createObjectURL(blob);
        console.log('PDF blob URL created:', blobUrl);
        setPdfBlob(blobUrl);
      }
    } catch (err) {
      console.error('❌ Preview error:', err);
      setError('Failed to preview document: ' + (err instanceof Error ? err.message : 'Unknown error'));
      setPreviewLoading(false);
    } finally {
      if (doc.type === 'pdf') {
        setPreviewLoading(false);
      }
    }
  };

  const workbookInit = (spread: GC.Spread.Sheets.Workbook) => {
    console.log('🎯 SpreadJS workbook initializing...', spread);
    spreadRef.current = spread;
    // Configure SpreadJS to be read-only
    spread.options.allowUserEditFormula = false;
    spread.options.tabStripVisible = true;
    spread.options.newTabVisible = false;
    spread.options.tabEditable = false;
    spread.options.allowUserResize = true;
    console.log('✅ SpreadJS workbook initialized and configured');
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

  const renderPdfPreview = () => {
    if (!pdfBlob) return null;

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between bg-gray-50 p-3 rounded border border-gray-200">
          <div className="flex items-center gap-4">
            <span className="text-sm font-semibold text-gray-700">
              Page {pageNumber} of {numPages}
            </span>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}
              disabled={pageNumber <= 1}
              className="px-4 py-2 bg-white border-2 border-gray-300 text-gray-700 rounded-md font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 hover:border-gray-400 transition-colors"
            >
              ← Previous
            </button>
            <button
              onClick={() => setPageNumber(Math.min(numPages, pageNumber + 1))}
              disabled={pageNumber >= numPages}
              className="px-4 py-2 bg-white border-2 border-gray-300 text-gray-700 rounded-md font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 hover:border-gray-400 transition-colors"
            >
              Next →
            </button>
          </div>
        </div>

        <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white p-4 flex justify-center">
          <Document
            file={pdfBlob}
            onLoadSuccess={({ numPages }) => {
              console.log('PDF loaded successfully, pages:', numPages);
              setNumPages(numPages);
            }}
            onLoadError={(error) => {
              console.error('PDF load error:', error);
              setError('Failed to load PDF');
            }}
            loading={
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Loading PDF...</p>
                </div>
              </div>
            }
            error={
              <div className="p-8 text-center">
                <p className="text-red-600 font-semibold mb-2">Failed to load PDF</p>
                <p className="text-sm text-gray-600">Please try downloading the file instead</p>
              </div>
            }
          >
            <Page
              pageNumber={pageNumber}
              renderTextLayer={true}
              renderAnnotationLayer={true}
              className="shadow-xl"
              width={Math.min(window.innerWidth * 0.5, 850)}
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
      <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white p-4 flex justify-center">
        <img
          src={url}
          alt={selectedDocument.filename}
          className="max-w-full h-auto rounded shadow-md"
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
        <div className="lg:col-span-1 bg-white border border-gray-200 rounded-xl p-4 max-h-[750px] overflow-y-auto shadow-sm">
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
                      className={`w-full text-left flex items-center gap-2 px-2 py-2 rounded text-sm hover:bg-indigo-50 transition-colors ${
                        selectedDocument?.path === doc.path ? 'bg-indigo-100 ring-2 ring-indigo-500' : ''
                      }`}
                    >
                      {getFileIcon(doc.type)}
                      <div className="flex-1 min-w-0">
                        <p className="text-gray-900 truncate font-medium">{doc.filename}</p>
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
        <div className="lg:col-span-2 bg-white border border-gray-200 rounded-xl p-6 shadow-sm" style={{ minHeight: '750px', maxHeight: '750px', overflowY: 'auto' }}>
          {/* SpreadJS - Always mounted (hidden off-screen) to keep workbook initialized */}
          <div style={{
            position: selectedDocument?.type === 'excel' && !previewLoading && !error ? 'relative' : 'absolute',
            left: selectedDocument?.type === 'excel' && !previewLoading && !error ? '0' : '-9999px',
            width: selectedDocument?.type === 'excel' && !previewLoading && !error ? '100%' : '1px',
            height: selectedDocument?.type === 'excel' && !previewLoading && !error ? '650px' : '1px',
            overflow: 'hidden'
          }}>
            <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white" style={{ height: '100%', width: '100%' }}>
              <SpreadSheets
                workbookInitialized={workbookInit}
                hostStyle={{ width: '100%', height: '100%' }}
              />
            </div>
          </div>

          {!selectedDocument && (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <FileText className="w-16 h-16 mb-4 text-gray-300" />
              <p className="text-lg font-medium">Select a document to preview</p>
              <p className="text-sm text-gray-400 mt-2">Excel files will show in full SpreadJS viewer</p>
            </div>
          )}

          {selectedDocument && (
            <div>
              <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-gray-200">
                <div className="flex items-center gap-3">
                  {getFileIcon(selectedDocument.type)}
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg">{selectedDocument.filename}</h3>
                    <p className="text-sm text-gray-500">{formatFileSize(selectedDocument.size)}</p>
                  </div>
                </div>
                <a
                  href={getDocumentDownloadUrl(projectId, selectedDocument.path)}
                  download
                  className="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium shadow-md hover:shadow-lg transition-all"
                >
                  <Download className="w-4 h-4" />
                  Download
                </a>
              </div>

              {previewLoading && (
                <div className="flex items-center justify-center py-24">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading {selectedDocument.type} preview...</p>
                  </div>
                </div>
              )}

              {!previewLoading && error && (
                <div className="p-8 text-center">
                  <p className="text-red-600 font-semibold">{error}</p>
                </div>
              )}

              {!previewLoading && !error && (
                <div>
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
