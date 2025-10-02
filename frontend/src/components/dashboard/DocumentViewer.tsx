import { useState, useEffect, useRef } from 'react';
import { FileText, Download, FolderOpen, File, Image, FileSpreadsheet } from 'lucide-react';
import * as XLSX from 'xlsx';
import { SpreadSheets } from '@mescius/spread-sheets-react';
import * as GC from '@mescius/spread-sheets';
import '@mescius/spread-sheets/styles/gc.spread.sheets.excel2013white.css';
import '@mescius/spread-sheets-charts';
import '@mescius/spread-sheets-shapes';
import * as ExcelIO from '@mescius/spread-excelio';
import { getDocumentList, getDocumentDownloadUrl } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

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

  // Preview state
  const [pdfBlob, setPdfBlob] = useState<string | null>(null);
  const [imageBlob, setImageBlob] = useState<string | null>(null);
  const [excelSheets, setExcelSheets] = useState<{name: string, data: any[][]}[]>([]);
  const [activeSheetIndex, setActiveSheetIndex] = useState(0);
  const [selectedCell, setSelectedCell] = useState<{row: number, col: number} | null>(null);
  const [selectedColumn, setSelectedColumn] = useState<number | null>(null);
  const [selectedRow, setSelectedRow] = useState<number | null>(null);
  const [formulaInput, setFormulaInput] = useState('');
  const [isEditingFormula, setIsEditingFormula] = useState(false);
  const [calculatedValue, setCalculatedValue] = useState<string | null>(null);
  const [editedCells, setEditedCells] = useState<{[key: string]: string}>({});
  const [editingCell, setEditingCell] = useState<{row: number, col: number} | null>(null);
  const [cellInputValue, setCellInputValue] = useState('');
  const [rangeStart, setRangeStart] = useState<{row: number, col: number} | null>(null);
  const [rangeEnd, setRangeEnd] = useState<{row: number, col: number} | null>(null);
  const [isSelectingRange, setIsSelectingRange] = useState(false);
  const [excelArrayBuffer, setExcelArrayBuffer] = useState<ArrayBuffer | null>(null);
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

  // Cleanup blob URLs on unmount
  useEffect(() => {
    return () => {
      if (pdfBlob) URL.revokeObjectURL(pdfBlob);
      if (imageBlob) URL.revokeObjectURL(imageBlob);
    };
  }, [pdfBlob, imageBlob]);


  const handleDocumentClick = async (doc: DocumentItem) => {
    setSelectedDocument(doc);
    setPreviewLoading(true);
    setError(null);
    setPdfBlob(null);
    setImageBlob(null);
    setExcelSheets([]);
    setActiveSheetIndex(0);
    setSelectedCell(null);
    setSelectedColumn(null);
    setSelectedRow(null);
    setFormulaInput('');
    setIsEditingFormula(false);
    setCalculatedValue(null);
    setEditedCells({});
    setEditingCell(null);
    setCellInputValue('');
    setRangeStart(null);
    setRangeEnd(null);
    setIsSelectingRange(false);
    setExcelArrayBuffer(null);

    try {
      const url = getDocumentDownloadUrl(projectId, doc.path);

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch document');
      }

      const arrayBuffer = await response.arrayBuffer();

      if (doc.type === 'pdf') {
        const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
        const blobUrl = URL.createObjectURL(blob);
        setPdfBlob(blobUrl);
      } else if (doc.type === 'excel') {
        // Store arrayBuffer for SpreadJS import
        setExcelArrayBuffer(arrayBuffer);

        // Also parse sheets for data mode
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        const sheets = workbook.SheetNames.map(name => ({
          name,
          data: XLSX.utils.sheet_to_json(workbook.Sheets[name], { header: 1 }) as any[][]
        }));
        setExcelSheets(sheets);
      } else if (doc.type === 'image') {
        const blob = new Blob([arrayBuffer]);
        const blobUrl = URL.createObjectURL(blob);
        setImageBlob(blobUrl);
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

  // Helper to convert column index to Excel letter (0 -> A, 1 -> B, etc.)
  const getColumnLetter = (index: number): string => {
    let letter = '';
    let num = index;
    while (num >= 0) {
      letter = String.fromCharCode(65 + (num % 26)) + letter;
      num = Math.floor(num / 26) - 1;
    }
    return letter;
  };

  const renderDocumentPreview = () => {
    if (!selectedDocument) return null;

    if (selectedDocument.type === 'pdf' && pdfBlob) {
      return (
        <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white">
          <iframe
            src={pdfBlob}
            className="w-full"
            style={{ height: '700px' }}
            title={selectedDocument.filename}
          />
        </div>
      );
    }

    if (selectedDocument.type === 'excel' && excelArrayBuffer) {
      try {
        const handleSpreadInit = (spread: GC.Spread.Sheets.Workbook) => {
          console.log('SpreadJS workbookInitialized called');

          if (!spread) {
            console.error('SpreadJS workbook not initialized');
            return;
          }

          spreadRef.current = spread;
          console.log('SpreadJS workbook stored in ref');

          try {
            // Configure SpreadJS options
            spread.options.tabStripVisible = true;
            spread.options.newTabVisible = false;
            spread.options.tabEditable = false;
            spread.options.allowUserResize = true;
            spread.options.showHorizontalScrollbar = true;
            spread.options.showVerticalScrollbar = true;
            console.log('SpreadJS options configured');

            // Import Excel file using ExcelIO
            const excelIO = new ExcelIO.IO();
            console.log('ExcelIO instance created');

            // Convert ArrayBuffer to Blob
            const blob = new Blob([excelArrayBuffer], {
              type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            });

            excelIO.open(
              blob,
              (json: any) => {
                console.log('Excel file loaded by ExcelIO');
                spread.fromJSON(json);
                console.log('Excel imported successfully');
                const sheetCount = spread.getSheetCount();
                console.log(`Loaded ${sheetCount} sheets`);

                // Log sheet names
                for (let i = 0; i < sheetCount; i++) {
                  const sheet = spread.getSheet(i);
                  console.log(`Sheet ${i}: ${sheet.name()}`);
                }
              },
              (error: any) => {
                console.error('Error importing Excel:', error);
                alert('Failed to import Excel file: ' + JSON.stringify(error));
              }
            );
          } catch (err) {
            console.error('Error in handleSpreadInit:', err);
            alert('Error initializing SpreadJS: ' + err);
          }
        };

        console.log('Rendering SpreadSheets component');
        return (
          <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white">
            <div className="border-b-2 border-gray-300 bg-gray-50 px-3 py-2">
              <span className="text-sm font-semibold text-gray-700">📊 Excel Viewer</span>
            </div>
            <SpreadSheets
              workbookInitialized={handleSpreadInit}
              hostStyle={{ height: '700px', width: '100%' }}
            />
          </div>
        );
      } catch (err) {
        console.error('Error rendering SpreadJS:', err);
        alert('Critical error: ' + err);
        return (
          <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white p-8">
            <p className="text-red-600">Failed to render Excel viewer: {String(err)}</p>
          </div>
        );
      }
    }

    // Fallback for old data mode (shouldn't reach here anymore)
    if (selectedDocument.type === 'excel' && excelSheets.length > 0) {
        const activeSheet = excelSheets[activeSheetIndex];
        const maxCols = activeSheet.data.length > 0
          ? Math.max(...activeSheet.data.map(r => r.length))
          : 0;

      const handleCellClick = (rowIndex: number, colIndex: number) => {
        // If editing a cell directly and formula mode active
        if (editingCell && cellInputValue.includes('=')) {
          const cellAddr = `${getColumnLetter(colIndex)}${rowIndex + 1}`;
          setCellInputValue(cellInputValue + cellAddr);
          return;
        }

        // If editing in formula bar and formula mode active
        if (isEditingFormula && formulaInput.includes('=')) {
          const cellAddr = `${getColumnLetter(colIndex)}${rowIndex + 1}`;
          setFormulaInput(formulaInput + cellAddr);
          return;
        }

        // Normal click: select cell
        setSelectedCell({ row: rowIndex, col: colIndex });
        setSelectedColumn(null);
        setSelectedRow(null);
        setIsEditingFormula(false);
        setCalculatedValue(null);
        setRangeStart(null);
        setRangeEnd(null);
        setIsSelectingRange(false);

        // Set formula input to current cell value
        const cellValue = getCellValue(rowIndex, colIndex);
        setFormulaInput(cellValue);
      };

      const handleColumnClick = (colIndex: number) => {
        setSelectedColumn(colIndex);
        setSelectedCell(null);
        setSelectedRow(null);
        setIsEditingFormula(false);
        setCalculatedValue(null);
        setFormulaInput('');
      };

      const handleRowClick = (rowIndex: number) => {
        setSelectedRow(rowIndex);
        setSelectedCell(null);
        setSelectedColumn(null);
        setIsEditingFormula(false);
        setCalculatedValue(null);
        setFormulaInput('');
      };

      const getCellKey = (rowIndex: number, colIndex: number): string => {
        return `${activeSheetIndex}-${rowIndex}-${colIndex}`;
      };

      const getCellValue = (rowIndex: number, colIndex: number): string => {
        // Check if cell has been edited
        const cellKey = getCellKey(rowIndex, colIndex);
        if (editedCells[cellKey] !== undefined) {
          return editedCells[cellKey];
        }

        // Otherwise return original value
        const row = activeSheet.data[rowIndex];
        if (!row) return '';
        const cell = row[colIndex];
        return cell !== null && cell !== undefined ? String(cell) : '';
      };

      // Parse cell reference like "A1" to {row: 0, col: 0}
      const parseCellReference = (ref: string): {row: number, col: number} | null => {
        const match = ref.match(/^([A-Z]+)(\d+)$/);
        if (!match) return null;

        const colLetter = match[1];
        const rowNum = parseInt(match[2], 10) - 1;

        // Convert column letter to index
        let colIndex = 0;
        for (let i = 0; i < colLetter.length; i++) {
          colIndex = colIndex * 26 + (colLetter.charCodeAt(i) - 64);
        }
        colIndex -= 1;

        return { row: rowNum, col: colIndex };
      };

      // Evaluate formula
      const evaluateFormula = (formula: string): string => {
        if (!formula.startsWith('=')) {
          return formula;
        }

        try {
          // Remove the = sign
          let expression = formula.substring(1);

          // Replace cell references with their values
          const cellRefRegex = /([A-Z]+\d+)/g;
          expression = expression.replace(cellRefRegex, (match) => {
            const cellPos = parseCellReference(match);
            if (!cellPos) return '0';

            const value = getCellValue(cellPos.row, cellPos.col);
            const numValue = parseFloat(value);
            return isNaN(numValue) ? '0' : String(numValue);
          });

          // Handle SUM function
          if (expression.toUpperCase().includes('SUM')) {
            const sumMatch = expression.match(/SUM\(([A-Z]+\d+):([A-Z]+\d+)\)/i);
            if (sumMatch) {
              const start = parseCellReference(sumMatch[1]);
              const end = parseCellReference(sumMatch[2]);

              if (start && end) {
                let sum = 0;
                for (let r = start.row; r <= end.row; r++) {
                  for (let c = start.col; c <= end.col; c++) {
                    const val = parseFloat(getCellValue(r, c));
                    if (!isNaN(val)) sum += val;
                  }
                }
                return String(sum);
              }
            }
          }

          // Evaluate the mathematical expression
          // eslint-disable-next-line no-eval
          const result = eval(expression);
          return String(result);
        } catch (e) {
          return '#ERROR';
        }
      };

      const handleFormulaChange = (value: string) => {
        setFormulaInput(value);
        setIsEditingFormula(true);

        // Calculate if it's a formula
        if (value.startsWith('=')) {
          const result = evaluateFormula(value);
          setCalculatedValue(result);
        } else {
          setCalculatedValue(null);
        }
      };

      const handleFormulaKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && selectedCell) {
          // Save the formula or value to the selected cell
          const cellKey = getCellKey(selectedCell.row, selectedCell.col);

          if (formulaInput.startsWith('=')) {
            // Evaluate and save the result
            const result = evaluateFormula(formulaInput);
            setEditedCells({...editedCells, [cellKey]: result});
          } else {
            // Save the raw value
            setEditedCells({...editedCells, [cellKey]: formulaInput});
          }

          setIsEditingFormula(false);
          setCalculatedValue(null);
        }
      };

      const handleCellMouseDown = (rowIndex: number, colIndex: number, e: React.MouseEvent) => {
        // If editing a cell with formula or formula bar active
        const inFormulaMode = (editingCell && cellInputValue.includes('=')) || (isEditingFormula && formulaInput.includes('='));

        if (inFormulaMode) {
          setRangeStart({ row: rowIndex, col: colIndex });
          setRangeEnd({ row: rowIndex, col: colIndex });
          setIsSelectingRange(true);
          e.preventDefault();
        }
      };

      const handleCellMouseEnter = (rowIndex: number, colIndex: number) => {
        if (isSelectingRange && rangeStart) {
          setRangeEnd({ row: rowIndex, col: colIndex });
        }
      };

      const handleCellMouseUp = () => {
        if (isSelectingRange && rangeStart && rangeEnd) {
          const startAddr = `${getColumnLetter(rangeStart.col)}${rangeStart.row + 1}`;
          const endAddr = `${getColumnLetter(rangeEnd.col)}${rangeEnd.row + 1}`;

          // Check if it's a single cell or range
          const rangeText = (rangeStart.row === rangeEnd.row && rangeStart.col === rangeEnd.col)
            ? startAddr
            : `${startAddr}:${endAddr}`;

          // Insert into cell input or formula bar
          if (editingCell && cellInputValue.includes('=')) {
            setCellInputValue(cellInputValue + rangeText);
          } else if (isEditingFormula && formulaInput.includes('=')) {
            setFormulaInput(formulaInput + rangeText);
          }

          setIsSelectingRange(false);
          setRangeStart(null);
          setRangeEnd(null);
        }
      };

      const handleCellDoubleClick = (rowIndex: number, colIndex: number) => {
        setEditingCell({ row: rowIndex, col: colIndex });
        setCellInputValue(getCellValue(rowIndex, colIndex));
        setRangeStart(null);
        setRangeEnd(null);
        setIsSelectingRange(false);
      };

      const handleCellInputChange = (value: string) => {
        setCellInputValue(value);

        // Live calculation preview if it's a formula
        if (value.startsWith('=')) {
          const result = evaluateFormula(value);
          setCalculatedValue(result);
        } else {
          setCalculatedValue(null);
        }
      };

      const handleCellInputKeyDown = (e: React.KeyboardEvent, rowIndex: number, colIndex: number) => {
        if (e.key === 'Enter') {
          const cellKey = getCellKey(rowIndex, colIndex);

          if (cellInputValue.startsWith('=')) {
            // Evaluate and save the result
            const result = evaluateFormula(cellInputValue);
            setEditedCells({...editedCells, [cellKey]: result});
          } else {
            // Save the raw value
            setEditedCells({...editedCells, [cellKey]: cellInputValue});
          }

          setEditingCell(null);
          setCellInputValue('');
          setCalculatedValue(null);
        } else if (e.key === 'Escape') {
          setEditingCell(null);
          setCellInputValue('');
          setCalculatedValue(null);
        }
      };

      const handleCellInputBlur = (rowIndex: number, colIndex: number) => {
        const cellKey = getCellKey(rowIndex, colIndex);

        if (cellInputValue.startsWith('=')) {
          const result = evaluateFormula(cellInputValue);
          setEditedCells({...editedCells, [cellKey]: result});
        } else if (cellInputValue !== '') {
          setEditedCells({...editedCells, [cellKey]: cellInputValue});
        }

        setEditingCell(null);
        setCellInputValue('');
        setCalculatedValue(null);
      };

      const getFormulaBarValue = (): string => {
        if (isEditingFormula) {
          return formulaInput;
        }
        if (selectedCell) {
          return getCellValue(selectedCell.row, selectedCell.col);
        }
        return '';
      };

      const getSelectedCellAddress = (): string => {
        if (selectedCell) {
          return `${getColumnLetter(selectedCell.col)}${selectedCell.row + 1}`;
        }
        return '';
      };

      return (
        <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white">
          {/* Formula Bar */}
          <div className="border-b-2 border-gray-300 bg-white px-3 py-2">
            <div className="flex items-center gap-3 mb-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-gray-600 bg-gray-100 px-2 py-1 rounded border border-gray-300" style={{ minWidth: '60px', textAlign: 'center' }}>
                  {getSelectedCellAddress() || 'A1'}
                </span>
              </div>
              <div className="flex-1">
                <input
                  type="text"
                  value={isEditingFormula ? formulaInput : getFormulaBarValue()}
                  onChange={(e) => handleFormulaChange(e.target.value)}
                  onKeyDown={handleFormulaKeyDown}
                  onFocus={() => setIsEditingFormula(true)}
                  placeholder="Enter formula (e.g., =A1+B1 or =SUM(A1:A5)) and press Enter"
                  className="w-full px-3 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>
            {calculatedValue !== null && (
              <div className="text-xs text-gray-600 bg-green-50 px-3 py-1 rounded border border-green-200">
                <span className="font-semibold">Result: </span>
                <span className="text-green-700 font-mono">{calculatedValue}</span>
              </div>
            )}
            <div className="text-xs text-gray-500 mt-1">
              💡 Double-click cell → type <code className="bg-gray-100 px-1 rounded">=</code> → click cells or drag range → type operators (+, -, *, /) → press Enter
            </div>
          </div>

          {/* Sheet tabs */}
          <div className="border-b border-gray-300 bg-gray-50 px-2 py-1 flex gap-2 overflow-x-auto">
            {excelSheets.map((sheet, index) => (
              <button
                key={index}
                onClick={() => {
                  setActiveSheetIndex(index);
                  setSelectedCell(null);
                  setSelectedColumn(null);
                  setSelectedRow(null);
                }}
                className={`px-3 py-1.5 text-sm font-medium rounded transition-colors whitespace-nowrap ${
                  index === activeSheetIndex
                    ? 'bg-white text-indigo-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                {sheet.name}
              </button>
            ))}
          </div>

          {/* Sheet data with horizontal scroll */}
          <div className="overflow-auto" style={{ maxHeight: '550px', width: '100%' }}>
            {activeSheet.data.length > 0 ? (
              <div style={{ overflowX: 'auto', overflowY: 'auto' }}>
                <table className="border-collapse">
                  <thead className="sticky top-0 z-10">
                    <tr>
                      {/* Row number header cell */}
                      <th
                        className="bg-gray-100 border border-gray-300 px-3 py-1 text-xs font-semibold text-gray-600 sticky left-0 z-20"
                        style={{ minWidth: '50px', width: '50px' }}
                      >
                        #
                      </th>
                      {/* Column letter headers (A, B, C...) */}
                      {Array.from({ length: maxCols }).map((_, colIndex) => (
                        <th
                          key={colIndex}
                          onClick={() => handleColumnClick(colIndex)}
                          className={`border border-gray-300 px-3 py-1 text-xs font-semibold text-gray-600 cursor-pointer hover:bg-gray-200 transition-colors ${
                            selectedColumn === colIndex ? 'bg-indigo-200' : 'bg-gray-100'
                          }`}
                          style={{ minWidth: '120px', width: '120px' }}
                        >
                          {getColumnLetter(colIndex)}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white">
                    {activeSheet.data.map((_row, rowIndex) => (
                      <tr key={rowIndex}>
                        {/* Row number */}
                        <td
                          onClick={() => handleRowClick(rowIndex)}
                          className={`border border-gray-300 px-3 py-1 text-xs font-semibold text-gray-600 text-center sticky left-0 z-10 cursor-pointer hover:bg-gray-200 transition-colors ${
                            selectedRow === rowIndex ? 'bg-indigo-200' : 'bg-gray-50'
                          }`}
                          style={{ minWidth: '50px', width: '50px' }}
                        >
                          {rowIndex + 1}
                        </td>
                        {/* Data cells */}
                        {Array.from({ length: maxCols }).map((_, colIndex) => {
                          const isSelected = selectedCell?.row === rowIndex && selectedCell?.col === colIndex;
                          const isInSelectedColumn = selectedColumn === colIndex;
                          const isInSelectedRow = selectedRow === rowIndex;

                          const isEditing = editingCell?.row === rowIndex && editingCell?.col === colIndex;

                          // Check if cell is in selected range
                          const isInRange = rangeStart && rangeEnd &&
                            rowIndex >= Math.min(rangeStart.row, rangeEnd.row) &&
                            rowIndex <= Math.max(rangeStart.row, rangeEnd.row) &&
                            colIndex >= Math.min(rangeStart.col, rangeEnd.col) &&
                            colIndex <= Math.max(rangeStart.col, rangeEnd.col);

                          return (
                            <td
                              key={colIndex}
                              onClick={() => handleCellClick(rowIndex, colIndex)}
                              onMouseDown={(e) => handleCellMouseDown(rowIndex, colIndex, e)}
                              onMouseEnter={() => handleCellMouseEnter(rowIndex, colIndex)}
                              onMouseUp={handleCellMouseUp}
                              onDoubleClick={() => handleCellDoubleClick(rowIndex, colIndex)}
                              className={`border border-gray-300 px-3 py-2 text-sm text-gray-900 cursor-pointer transition-colors select-none ${
                                isSelected
                                  ? 'bg-indigo-100 ring-2 ring-inset ring-indigo-500'
                                  : isInRange
                                    ? 'bg-blue-200'
                                    : isInSelectedColumn || isInSelectedRow
                                      ? 'bg-indigo-50'
                                      : 'hover:bg-gray-100'
                              }`}
                              style={{ minWidth: '120px', width: '120px' }}
                            >
                              {isEditing ? (
                                <input
                                  type="text"
                                  value={cellInputValue}
                                  onChange={(e) => handleCellInputChange(e.target.value)}
                                  onKeyDown={(e) => handleCellInputKeyDown(e, rowIndex, colIndex)}
                                  onBlur={() => handleCellInputBlur(rowIndex, colIndex)}
                                  autoFocus
                                  className="w-full px-1 py-0 text-sm border-0 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded"
                                />
                              ) : (
                                getCellValue(rowIndex, colIndex)
                              )}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="flex items-center justify-center py-12">
                <p className="text-gray-500">This sheet is empty</p>
              </div>
            )}
          </div>
        </div>
      );
    }

    if (selectedDocument.type === 'image' && imageBlob) {
      return (
        <div className="border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg bg-white p-4 flex justify-center items-center" style={{ minHeight: '500px' }}>
          <img
            src={imageBlob}
            alt={selectedDocument.filename}
            className="max-w-full max-h-[650px] h-auto rounded shadow-md object-contain"
          />
        </div>
      );
    }

    return null;
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
          {!selectedDocument && (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <FileText className="w-16 h-16 mb-4 text-gray-300" />
              <p className="text-lg font-medium">Select a document to preview</p>
              <p className="text-sm text-gray-400 mt-2">Excel files will show in full spreadsheet viewer with all sheets</p>
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

              {!previewLoading && !error && renderDocumentPreview()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
