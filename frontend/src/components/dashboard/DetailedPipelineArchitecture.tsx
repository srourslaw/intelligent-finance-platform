import { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import {
  FileSpreadsheet, FileText, Image as ImageIcon, FileCode,
  Database, Zap, BarChart3, Sparkles,
  RefreshCw, Shield, TrendingUp, PieChart,
  Calculator, BookOpen, FileDigit, Layers, Brain,
  Activity, FileSearch, Users, CheckCircle, DollarSign,
  Building2, ClipboardCheck, TrendingDown
} from 'lucide-react';

interface DetailedPipelineArchitectureProps {
  isAnimating?: boolean;
  onToggleAnimation?: () => void;
}

export function DetailedPipelineArchitecture({
  isAnimating = false,
  onToggleAnimation
}: DetailedPipelineArchitectureProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [stats, setStats] = useState({
    filesProcessed: 0,
    extracted: 0,
    validated: 0,
    transformed: 0,
    outputs: 0
  });

  // Data source definitions (left side - Real construction financial documents)
  const dataSources = [
    { id: 'invoices', icon: FileText, label: 'Vendor Invoices', count: '45', description: 'Materials, Equipment, Services' },
    { id: 'pos', icon: FileSpreadsheet, label: 'Purchase Orders', count: '38', description: 'PO #1001-1250' },
    { id: 'timesheets', icon: FileCode, label: 'Timesheets', count: '24', description: 'Direct Labor & Overtime' },
    { id: 'subcontracts', icon: FileDigit, label: 'Sub Contracts', count: '18', description: 'Trade Subs & Consultants' },
    { id: 'bank-statements', icon: Calculator, label: 'Bank Statements', count: '6', description: 'Monthly Bank Reconciliation' }
  ];

  // Central processing matrix - Real construction financial processing stages
  const processingMatrix = {
    topRow: [
      { id: 'ai-classification', icon: Sparkles, label: 'AI Classification', description: 'Document Type Detection' },
      { id: 'ocr-extraction', icon: FileSearch, label: 'OCR Extraction', description: 'Line Items & Amounts' },
      { id: 'vendor-matching', icon: Users, label: 'Vendor Matching', description: 'Entity Recognition' }
    ],
    bottomRow: [
      { id: 'cost-coding', icon: Layers, label: 'Cost Coding', description: 'WBS Assignment' },
      { id: 'duplicate-check', icon: Shield, label: 'Duplicate Check', description: 'De-duplication' },
      { id: 'validation', icon: CheckCircle, label: 'Validation', description: 'Business Rules' }
    ]
  };

  // Output groups - Real construction financial reports
  const outputGroups = [
    {
      id: 'project-financials',
      title: 'Project Financials',
      items: [
        { id: 'wip-report', icon: Building2, label: 'WIP Report' },
        { id: 'cost-breakdown', icon: PieChart, label: 'Cost by Trade' },
        { id: 'budget-actual', icon: TrendingUp, label: 'Budget vs Actual' }
      ]
    },
    {
      id: 'cash-management',
      title: 'Cash Management',
      items: [
        { id: 'cashflow-forecast', icon: BarChart3, label: 'Cash Flow Forecast' },
        { id: 'aging-payables', icon: TrendingDown, label: 'Aging Payables' }
      ]
    },
    {
      id: 'compliance',
      title: 'Compliance & Audit',
      items: [
        { id: 'sub-reconciliation', icon: ClipboardCheck, label: 'Sub Reconciliation' },
        { id: 'audit-trail', icon: BookOpen, label: 'Audit Trail' }
      ]
    }
  ];

  // Connection paths - Logical construction financial data flow
  const connections: any[] = [
    // Data Sources to AI Classification (all documents flow to AI first)
    { from: 'invoices', to: 'ai-classification', color: '#7c3aed' },
    { from: 'pos', to: 'ai-classification', color: '#7c3aed' },
    { from: 'timesheets', to: 'ai-classification', color: '#7c3aed' },
    { from: 'subcontracts', to: 'ai-classification', color: '#7c3aed' },
    { from: 'bank-statements', to: 'ai-classification', color: '#7c3aed' },

    // Top Row Processing Flow: AI Classification -> OCR Extraction -> Vendor Matching
    { from: 'ai-classification', to: 'ocr-extraction', color: '#3b82f6' },
    { from: 'ocr-extraction', to: 'vendor-matching', color: '#3b82f6' },

    // Bottom Row Processing Flow: Cost Coding -> Duplicate Check -> Validation
    { from: 'cost-coding', to: 'duplicate-check', color: '#3b82f6' },
    { from: 'duplicate-check', to: 'validation', color: '#3b82f6' },

    // Cross connections: Top row feeds bottom row
    { from: 'ai-classification', to: 'cost-coding', color: '#3b82f6' },
    { from: 'vendor-matching', to: 'validation', color: '#3b82f6' },

    // Validation to Project Financial Outputs
    { from: 'validation', to: 'wip-report', color: '#10b981' },
    { from: 'validation', to: 'cost-breakdown', color: '#10b981' },
    { from: 'validation', to: 'budget-actual', color: '#10b981' },

    // Validation to Cash Management Outputs
    { from: 'validation', to: 'cashflow-forecast', color: '#10b981' },
    { from: 'validation', to: 'aging-payables', color: '#10b981' },

    // Validation to Compliance Outputs
    { from: 'validation', to: 'sub-reconciliation', color: '#10b981' },
    { from: 'validation', to: 'audit-trail', color: '#10b981' }
  ];

  // No SVG connections - using visual flow indicators instead

  // Particles removed

  // Update stats
  useEffect(() => {
    if (!isAnimating) {
      setStats({ filesProcessed: 0, extracted: 0, validated: 0, transformed: 0, outputs: 0 });
      return;
    }

    const interval = setInterval(() => {
      setStats(prev => {
        const newProcessed = Math.min(prev.filesProcessed + 3, 131);
        return {
          filesProcessed: newProcessed,
          extracted: Math.min(Math.floor(newProcessed * 0.9), 131),
          validated: Math.min(Math.floor(newProcessed * 0.8), 131),
          transformed: Math.min(Math.floor(newProcessed * 0.7), 131),
          outputs: Math.min(Math.floor(newProcessed * 0.6), 131)
        };
      });
    }, 200);

    return () => clearInterval(interval);
  }, [isAnimating]);


  return (
    <div className="pipeline-architecture" ref={containerRef}>
      {/* Stats Bar */}
      <div className="stats-bar">
        <div className="stat-item">
          <span className="stat-value">{stats.filesProcessed}</span>
          <span className="stat-label">Files Processed</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.extracted}</span>
          <span className="stat-label">Extracted</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.validated}</span>
          <span className="stat-label">Validated</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.transformed}</span>
          <span className="stat-label">Transformed</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.outputs}</span>
          <span className="stat-label">Outputs Generated</span>
        </div>
      </div>

      {/* Main Diagram */}
      <div className="diagram-container">
        {/* Content Layer */}
        <div className="content-layer">
          {/* LEFT: Data Sources */}
          <div className="data-sources-column">
            <h3 className="column-title">Source Documents</h3>
            {dataSources.map(source => {
              const Icon = source.icon;
              return (
                <div key={source.id} id={source.id} className="data-source-item">
                  <div className="source-card">
                    <div className="source-icon-circle">
                      <Icon size={20} />
                    </div>
                    <div className="source-content">
                      <div className="source-label">{source.label}</div>
                      <div className="source-description">{source.description}</div>
                      <div className="source-count">{source.count} docs</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Flow Arrow: Sources to Processing */}
          <div className={`flow-arrow arrow-purple ${isAnimating ? 'animating' : ''}`}>
            <div className="arrow-line"></div>
            <div className="arrow-head">→</div>
            {isAnimating && (
              <>
                <div className="flow-particle" style={{ animationDelay: '0s' }}></div>
                <div className="flow-particle" style={{ animationDelay: '0.5s' }}></div>
                <div className="flow-particle" style={{ animationDelay: '1s' }}></div>
              </>
            )}
          </div>

          {/* CENTER: Processing Matrix */}
          <div id="matrix-container" className="processing-matrix">
            <div className="matrix-header">
              <Brain size={24} className="matrix-icon" />
              <span className="matrix-title">AI-Powered Financial Data Pipeline</span>
            </div>

            <div className="matrix-content">
              {/* Top Row */}
              <div className="matrix-row">
                {processingMatrix.topRow.map(stage => {
                  const Icon = stage.icon;
                  return (
                    <div key={stage.id} id={stage.id} className="matrix-stage">
                      <div className="stage-icon-wrapper">
                        <Icon size={32} className="stage-icon" />
                      </div>
                      <div className="stage-label">{stage.label}</div>
                      <div className="stage-description">{stage.description}</div>
                    </div>
                  );
                })}
              </div>

              {/* Bottom Row */}
              <div className="matrix-row">
                {processingMatrix.bottomRow.map(stage => {
                  const Icon = stage.icon;
                  return (
                    <div key={stage.id} id={stage.id} className="matrix-stage">
                      <div className="stage-icon-wrapper">
                        <Icon size={32} className="stage-icon" />
                      </div>
                      <div className="stage-label">{stage.label}</div>
                      <div className="stage-description">{stage.description}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Flow Arrow: Processing to Outputs */}
          <div className={`flow-arrow arrow-green ${isAnimating ? 'animating' : ''}`}>
            <div className="arrow-line"></div>
            <div className="arrow-head">→</div>
            {isAnimating && (
              <>
                <div className="flow-particle" style={{ animationDelay: '0.2s' }}></div>
                <div className="flow-particle" style={{ animationDelay: '0.7s' }}></div>
                <div className="flow-particle" style={{ animationDelay: '1.2s' }}></div>
              </>
            )}
          </div>

          {/* RIGHT: Output Groups */}
          <div className="outputs-column">
            <h3 className="column-title">Financial Reports</h3>
            {outputGroups.map(group => (
              <div key={group.id} id={`${group.id}-group`} className="output-group">
                <div className="group-header">
                  <div className="group-title">{group.title}</div>
                </div>
                <div className="group-items">
                  {group.items.map(item => {
                    const Icon = item.icon;
                    return (
                      <div key={item.id} id={item.id} className="output-item">
                        <div className="output-icon-wrapper">
                          <Icon size={18} className="output-icon" />
                        </div>
                        <span className="output-label">{item.label}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Control Button */}
      <div className="control-panel">
        <button className={`control-btn ${isAnimating ? 'active' : ''}`} onClick={onToggleAnimation}>
          {isAnimating ? '⏸ Pause Animation' : '▶ Start Animation'}
        </button>
      </div>

      <style>{`
        @keyframes dash-flow {
          0% {
            stroke-dashoffset: 0;
          }
          100% {
            stroke-dashoffset: 100;
          }
        }

        .pipeline-architecture {
          width: 100%;
          background: #f8fafc;
          padding: 24px;
          position: relative;
          min-height: 800px;
        }

        .stats-bar {
          display: flex;
          gap: 24px;
          margin-bottom: 40px;
          padding: 24px;
          background: white;
          border-radius: 12px;
          border: 1px solid #e2e8f0;
          justify-content: space-around;
        }

        .stat-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 6px;
        }

        .stat-value {
          font-size: 2rem;
          font-weight: 700;
          color: #1e293b;
          line-height: 1;
        }

        .stat-label {
          font-size: 0.75rem;
          color: #64748b;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .diagram-container {
          position: relative;
          min-height: 600px;
          background: white;
          border-radius: 12px;
          padding: 40px;
        }

        .content-layer {
          display: grid;
          grid-template-columns: 220px 50px 1fr 50px 300px;
          gap: 0;
          position: relative;
          z-index: 2;
          align-items: start;
        }

        /* Flow Arrows */
        .flow-arrow {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          position: relative;
        }

        .arrow-line {
          width: 3px;
          height: 100%;
          background: linear-gradient(to bottom, transparent 10%, currentColor 50%, transparent 90%);
          opacity: 0.3;
        }

        .arrow-head {
          font-size: 2.5rem;
          font-weight: 300;
          color: currentColor;
          animation: pulse-arrow 2s ease-in-out infinite;
          margin-top: -20px;
        }

        .arrow-purple {
          color: #7c3aed;
        }

        .arrow-green {
          color: #10b981;
        }

        @keyframes pulse-arrow {
          0%, 100% {
            opacity: 0.4;
            transform: translateX(0);
          }
          50% {
            opacity: 1;
            transform: translateX(4px);
          }
        }

        .flow-arrow.animating .arrow-head {
          animation: pulse-arrow 1s ease-in-out infinite;
        }

        .flow-arrow.animating .arrow-line {
          opacity: 0.6;
        }

        .flow-particle {
          position: absolute;
          width: 8px;
          height: 8px;
          background: currentColor;
          border-radius: 50%;
          top: 50%;
          left: 0;
          animation: flow-particle 1.5s ease-in-out infinite;
          box-shadow: 0 0 10px currentColor;
        }

        @keyframes flow-particle {
          0% {
            left: 0;
            opacity: 0;
            transform: translateY(-50%) scale(0.5);
          }
          20% {
            opacity: 1;
            transform: translateY(-50%) scale(1);
          }
          80% {
            opacity: 1;
            transform: translateY(-50%) scale(1);
          }
          100% {
            left: 100%;
            opacity: 0;
            transform: translateY(-50%) scale(0.5);
          }
        }

        .column-title {
          font-size: 0.9rem;
          font-weight: 700;
          color: #7c3aed;
          margin-bottom: 24px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        /* LEFT: Data Sources */
        .data-sources-column {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .data-source-item {
          transition: all 0.3s ease;
        }

        .data-source-item:hover {
          transform: translateX(4px);
        }

        .source-card {
          display: flex;
          gap: 12px;
          padding: 12px;
          background: linear-gradient(135deg, #7c3aed05 0%, #7c3aed15 100%);
          border: 1px solid #7c3aed30;
          border-radius: 8px;
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .source-card:hover {
          background: linear-gradient(135deg, #7c3aed10 0%, #7c3aed25 100%);
          border-color: #7c3aed;
          box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
        }

        .source-icon-circle {
          width: 40px;
          height: 40px;
          background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          flex-shrink: 0;
          transition: all 0.3s ease;
          position: relative;
        }

        .source-card:hover .source-icon-circle {
          transform: scale(1.1);
          box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
        }

        .source-content {
          display: flex;
          flex-direction: column;
          gap: 2px;
          flex: 1;
        }

        .source-label {
          font-size: 0.8rem;
          font-weight: 700;
          color: #1e293b;
        }

        .source-description {
          font-size: 0.65rem;
          color: #64748b;
          line-height: 1.3;
        }

        .source-count {
          font-size: 0.7rem;
          color: #7c3aed;
          font-weight: 600;
          margin-top: 2px;
        }

        /* CENTER: Processing Matrix */
        .processing-matrix {
          padding: 28px;
          background: linear-gradient(135deg, #3b82f610 0%, #3b82f605 100%);
          border: 2px solid #3b82f630;
          border-radius: 16px;
          box-shadow: 0 8px 24px rgba(59, 130, 246, 0.08);
        }

        .matrix-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 24px;
          padding-bottom: 16px;
          border-bottom: 2px solid #3b82f6;
        }

        .matrix-icon {
          color: #3b82f6;
          filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.3));
        }

        .matrix-title {
          font-size: 1.1rem;
          font-weight: 700;
          background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .matrix-content {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .matrix-row {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 16px;
        }

        .matrix-stage {
          background: white;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          padding: 20px;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
          text-align: center;
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .matrix-stage:hover {
          transform: translateY(-4px);
          border-color: #3b82f6;
          box-shadow: 0 8px 20px rgba(59, 130, 246, 0.2);
          background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
        }

        .stage-icon-wrapper {
          position: relative;
          display: inline-block;
          margin-bottom: 4px;
          background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
          padding: 12px;
          border-radius: 10px;
        }

        .stage-icon {
          color: white;
        }

        .matrix-stage:hover .stage-icon-wrapper {
          transform: scale(1.1);
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }

        .stage-label {
          font-size: 0.85rem;
          font-weight: 700;
          color: #1e293b;
        }

        .stage-description {
          font-size: 0.7rem;
          color: #64748b;
        }

        /* RIGHT: Output Groups */
        .outputs-column {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .output-group {
          background: linear-gradient(135deg, #10b98105 0%, #10b98115 100%);
          border: 1px solid #10b98130;
          border-radius: 12px;
          padding: 16px;
          transition: all 0.3s ease;
        }

        .output-group:hover {
          border-color: #10b981;
          box-shadow: 0 6px 16px rgba(16, 185, 129, 0.15);
        }

        .group-header {
          margin-bottom: 12px;
          padding-bottom: 8px;
          border-bottom: 2px solid #10b98120;
        }

        .group-title {
          font-size: 0.75rem;
          font-weight: 700;
          color: #059669;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .group-items {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .output-item {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 10px;
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .output-item:hover {
          transform: translateX(-4px);
          border-color: #10b981;
          box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
          background: linear-gradient(135deg, #ffffff 0%, #ecfdf5 100%);
        }

        .output-icon-wrapper {
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          width: 36px;
          height: 36px;
          border-radius: 8px;
          flex-shrink: 0;
        }

        .output-icon {
          color: white;
        }

        .output-item:hover .output-icon-wrapper {
          transform: scale(1.1);
          box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }

        .output-label {
          font-size: 0.75rem;
          font-weight: 600;
          color: #1e293b;
          flex: 1;
        }

        .control-panel {
          display: flex;
          justify-content: center;
          margin-top: 32px;
        }

        .control-btn {
          padding: 16px 48px;
          background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
          color: white;
          border: none;
          border-radius: 12px;
          font-weight: 700;
          font-size: 1rem;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        }

        .control-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 24px rgba(59, 130, 246, 0.4);
        }

        .control-btn.active {
          background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
          box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
        }
      `}</style>
    </div>
  );
}
