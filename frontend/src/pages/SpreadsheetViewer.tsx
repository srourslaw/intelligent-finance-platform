import React, { useEffect, useRef, useState } from 'react';
import Spreadsheet from 'x-data-spreadsheet';
import 'x-data-spreadsheet/dist/xspreadsheet.css';
import * as XLSX from 'xlsx';

import { Upload, FileSpreadsheet, Download } from 'lucide-react';

const SpreadsheetViewer: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const spreadsheetRef = useRef<any>(null);
  const [fileName, setFileName] = useState<string>('');
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!containerRef.current || spreadsheetRef.current) return;

    // Initialize x-spreadsheet with empty data
    const xs = new Spreadsheet(containerRef.current, {
      mode: 'edit',
      showToolbar: true,
      showGrid: true,
      showContextmenu: true,
      view: {
        height: () => 600,
        width: () => containerRef.current?.clientWidth || 1200,
      },
      row: {
        len: 100,
        height: 25,
      },
      col: {
        len: 26,
        width: 100,
        indexWidth: 60,
        minWidth: 60,
      },
    }).loadData({
      name: 'Sheet1',
      rows: {},
    });

    spreadsheetRef.current = xs;
    setIsReady(true);

    return () => {
      spreadsheetRef.current = null;
    };
  }, []);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !spreadsheetRef.current) return;

    setFileName(file.name);

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const data = new Uint8Array(e.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });

        // Convert first sheet to x-spreadsheet format
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' }) as any[][];

        // Convert to x-spreadsheet rows format
        const rows: any = {};
        jsonData.forEach((row, rowIndex) => {
          const cells: any = {};
          row.forEach((cell, colIndex) => {
            if (cell !== '') {
              cells[colIndex] = { text: cell?.toString() || '' };
            }
          });
          if (Object.keys(cells).length > 0) {
            rows[rowIndex] = { cells };
          }
        });

        // Load data into spreadsheet
        spreadsheetRef.current.loadData({
          name: firstSheetName,
          rows: rows,
        });

        console.log('Excel file loaded successfully:', file.name);
      } catch (error) {
        console.error('Error loading Excel file:', error);
        alert('Error loading Excel file. Please try another file.');
      }
    };
    reader.readAsArrayBuffer(file);
  };

  const handleDownload = () => {
    if (!spreadsheetRef.current) {
      alert('No data to download');
      return;
    }

    try {
      // Get data from x-spreadsheet
      const data = spreadsheetRef.current.getData();

      // Convert to array of arrays
      const rows: any[][] = [];
      const rowKeys = Object.keys(data.rows || {}).map(Number).sort((a, b) => a - b);

      rowKeys.forEach(rowIndex => {
        const row = data.rows[rowIndex];
        const cells = row.cells || {};
        const cellKeys = Object.keys(cells).map(Number).sort((a, b) => a - b);
        const maxCol = Math.max(...cellKeys, 0);

        const rowData: any[] = [];
        for (let i = 0; i <= maxCol; i++) {
          rowData.push(cells[i]?.text || '');
        }
        rows[rowIndex] = rowData;
      });

      // Fill empty rows
      const maxRow = Math.max(...rowKeys, 0);
      for (let i = 0; i <= maxRow; i++) {
        if (!rows[i]) rows[i] = [];
      }

      // Create workbook
      const ws = XLSX.utils.aoa_to_sheet(rows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, data.name || 'Sheet1');

      // Download
      XLSX.writeFile(wb, fileName || 'spreadsheet.xlsx');
    } catch (error) {
      console.error('Error downloading file:', error);
      alert('Error downloading file. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-full mx-auto px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-3 rounded-xl">
                <FileSpreadsheet className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Excel Spreadsheet Viewer
                </h1>
                <p className="text-sm text-gray-600">
                  View and edit Excel files with formulas, formatting & multiple sheets
                </p>
              </div>
            </div>

            <div className="flex gap-3">
              <label className="px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all cursor-pointer flex items-center gap-2 shadow-md">
                <Upload className="w-4 h-4" />
                Upload Excel
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>

              <button
                onClick={handleDownload}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all flex items-center gap-2 shadow-md"
              >
                <Download className="w-4 h-4" />
                Download
              </button>
            </div>
          </div>

          {fileName && (
            <div className="mt-3 px-4 py-2 bg-blue-50 border border-blue-200 rounded-lg flex items-center gap-2">
              <FileSpreadsheet className="w-4 h-4 text-blue-600" />
              <span className="text-sm font-medium text-blue-900">{fileName}</span>
            </div>
          )}
        </div>
      </div>

      {/* Spreadsheet Container */}
      <div className="max-w-full mx-auto px-8 py-8">
        <div className="bg-white rounded-xl shadow-2xl overflow-hidden">
          <div ref={containerRef} />
        </div>
      </div>
    </div>
  );
};

export default SpreadsheetViewer;
