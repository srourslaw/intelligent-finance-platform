import { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import {
  FileSpreadsheet, FileText, Image as ImageIcon, FileCode,
  Database, Zap, BarChart3, Sparkles,
  RefreshCw, Shield, TrendingUp, PieChart,
  Calculator, BookOpen, FileDigit, Layers, Brain,
  Activity
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

  // Data source definitions (left side - circular purple icons)
  const dataSources = [
    { id: 'excel-source', icon: FileSpreadsheet, label: 'Excel Files', count: '87' },
    { id: 'pdf-source', icon: FileText, label: 'PDF Docs', count: '24' },
    { id: 'image-source', icon: ImageIcon, label: 'Images', count: '12' },
    { id: 'csv-source', icon: FileCode, label: 'CSV Data', count: '8' }
  ];

  // Central processing matrix (big dotted box in center)
  const processingMatrix = {
    topRow: [
      { id: 'raw-data', icon: Database, label: 'Raw Data', description: 'Ingested files' },
      { id: 'ai-extract', icon: Sparkles, label: 'AI Extraction', description: 'OCR & NLP' },
      { id: 'validation', icon: Shield, label: 'Validation', description: 'Data checks' }
    ],
    bottomRow: [
      { id: 'catalog', icon: Layers, label: 'Catalog', description: 'Metadata' },
      { id: 'transform', icon: RefreshCw, label: 'Transform', description: 'Processing' },
      { id: 'enrichment', icon: Zap, label: 'Enrichment', description: 'Enhancement' }
    ]
  };

  // Output groups (right side - grouped in boxes)
  const outputGroups = [
    {
      id: 'financial-statements',
      title: 'Financial Statements',
      items: [
        { id: 'balance-sheet', icon: Calculator, label: 'Balance Sheet' },
        { id: 'income-stmt', icon: TrendingUp, label: 'Income Statement' },
        { id: 'cashflow', icon: BarChart3, label: 'Cash Flow' }
      ]
    },
    {
      id: 'analytics',
      title: 'Analytics & Insights',
      items: [
        { id: 'ratios', icon: PieChart, label: 'Ratios' },
        { id: 'trends', icon: Activity, label: 'Trends' }
      ]
    },
    {
      id: 'documentation',
      title: 'Documentation',
      items: [
        { id: 'assumptions', icon: BookOpen, label: 'Assumptions' },
        { id: 'instructions', icon: FileDigit, label: 'Instructions' }
      ]
    }
  ];

  // Connection paths - comprehensive data flow
  const connections: any[] = [
    // Data Sources to Raw Data
    { from: 'excel-source', to: 'raw-data', color: '#7c3aed' },
    { from: 'pdf-source', to: 'raw-data', color: '#7c3aed' },
    { from: 'image-source', to: 'raw-data', color: '#7c3aed' },
    { from: 'csv-source', to: 'raw-data', color: '#7c3aed' },

    // Top Row Flow: Raw Data -> AI Extraction -> Validation
    { from: 'raw-data', to: 'ai-extract', color: '#3b82f6' },
    { from: 'ai-extract', to: 'validation', color: '#3b82f6' },

    // Bottom Row Flow: Catalog -> Transform -> Enrichment
    { from: 'catalog', to: 'transform', color: '#3b82f6' },
    { from: 'transform', to: 'enrichment', color: '#3b82f6' },

    // Cross connections: Top row to bottom row
    { from: 'raw-data', to: 'catalog', color: '#3b82f6' },
    { from: 'validation', to: 'enrichment', color: '#3b82f6' },

    // Enrichment to Outputs
    { from: 'enrichment', to: 'balance-sheet', color: '#10b981' },
    { from: 'enrichment', to: 'income-stmt', color: '#10b981' },
    { from: 'enrichment', to: 'cashflow', color: '#10b981' },
    { from: 'enrichment', to: 'ratios', color: '#10b981' },
    { from: 'enrichment', to: 'trends', color: '#10b981' },
    { from: 'enrichment', to: 'assumptions', color: '#10b981' },
    { from: 'enrichment', to: 'instructions', color: '#10b981' }
  ];

  // Draw SVG connections using D3
  useEffect(() => {
    if (!svgRef.current || !containerRef.current) return;

    const drawConnections = () => {
      const svg = d3.select(svgRef.current);
      svg.selectAll('*').remove();

      const defs = svg.append('defs');

      // Create glow filter
      const filter = defs.append('filter')
        .attr('id', 'glow')
        .attr('x', '-50%')
        .attr('y', '-50%')
        .attr('width', '200%')
        .attr('height', '200%');

      filter.append('feGaussianBlur')
        .attr('stdDeviation', '3')
        .attr('result', 'coloredBlur');

      const feMerge = filter.append('feMerge');
      feMerge.append('feMergeNode').attr('in', 'coloredBlur');
      feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

      // Draw all connection paths with curved dotted lines
      connections.forEach((conn: any) => {
        const fromEl = document.getElementById(conn.from);
        const toEl = document.getElementById(conn.to);

        if (!fromEl) {
          console.error(`Could not find element with id: ${conn.from}`);
          return;
        }
        if (!toEl) {
          console.error(`Could not find element with id: ${conn.to}`);
          return;
        }

        const svgRect = svgRef.current!.getBoundingClientRect();

        // Get the connection dot positions - these are the ACTUAL dots we added
        // For Excel, we need the element with id='excel-source', then find its dot
        const fromElActual = document.getElementById(conn.from);
        const toElActual = document.getElementById(conn.to);

        if (!fromElActual || !toElActual) {
          return;
        }

        const fromDot = fromElActual.querySelector('.connection-dot') as HTMLElement;
        const toDot = toElActual.querySelector('.connection-dot') as HTMLElement;

        if (!fromDot || !toDot) {
          return;
        }

        // Get the EXACT CENTER of each dot relative to the SVG
        const fromDotRect = fromDot.getBoundingClientRect();
        const toDotRect = toDot.getBoundingClientRect();

        const x1 = fromDotRect.left + fromDotRect.width / 2 - svgRect.left;
        const y1 = fromDotRect.top + fromDotRect.height / 2 - svgRect.top;
        const x2 = toDotRect.left + toDotRect.width / 2 - svgRect.left;
        const y2 = toDotRect.top + toDotRect.height / 2 - svgRect.top;

        // Calculate control points for smooth curve
        const dx = x2 - x1;
        const dy = y2 - y1;

        // Create curved path using quadratic bezier
        const cx = x1 + dx * 0.5;
        const cy = y1 + dy * 0.5 - Math.abs(dy) * 0.2;

        const path = `M ${x1} ${y1} Q ${cx} ${cy}, ${x2} ${y2}`;

        // Draw the curved solid line (static)
        svg.append('path')
          .attr('d', path)
          .attr('class', `connection-path path-${conn.from}-${conn.to}`)
          .attr('stroke', conn.color || '#3b82f6')
          .attr('stroke-width', '2')
          .attr('fill', 'none')
          .attr('opacity', '0.3')
          .attr('stroke-linecap', 'round');
      });
    };

    // Draw immediately and on window resize
    setTimeout(drawConnections, 1000);
    window.addEventListener('resize', drawConnections);

    return () => window.removeEventListener('resize', drawConnections);
  }, []);

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
        {/* SVG Layer */}
        <svg
          ref={svgRef}
          className="connection-svg"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
            zIndex: 1
          }}
        >
        </svg>

        {/* Content Layer */}
        <div className="content-layer">
          {/* LEFT: Data Sources */}
          <div className="data-sources-column">
            <h3 className="column-title">Datasources</h3>
            {dataSources.map(source => {
              const Icon = source.icon;
              return (
                <div key={source.id} id={source.id} className="data-source-item">
                  <div className="source-icon-circle">
                    <Icon size={24} />
                    <div className={`connection-dot ${source.id === 'excel-source' ? 'excel-dot' : ''}`}></div>
                  </div>
                  <div className="source-content">
                    <div className="source-label">{source.label}</div>
                    <div className="source-count">{source.count} files</div>
                  </div>
                </div>
              );
            })}
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
                        <div className="connection-dot"></div>
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
                        <div className="connection-dot"></div>
                      </div>
                      <div className="stage-label">{stage.label}</div>
                      <div className="stage-description">{stage.description}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* RIGHT: Output Groups */}
          <div className="outputs-column">
            <h3 className="column-title">Data Sharing</h3>
            {outputGroups.map(group => (
              <div key={group.id} id={`${group.id}-group`} className="output-group">
                <div className="group-title">{group.title}</div>
                <div className="group-items">
                  {group.items.map(item => {
                    const Icon = item.icon;
                    return (
                      <div key={item.id} id={item.id} className="output-item">
                        <div className="output-icon-wrapper">
                          <Icon size={20} className="output-icon" />
                          <div className="connection-dot"></div>
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
          grid-template-columns: 200px 1fr 280px;
          gap: 60px;
          position: relative;
          z-index: 2;
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
          gap: 16px;
        }

        .data-source-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
          padding: 8px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .data-source-item:hover {
          transform: translateY(-4px);
        }

        .source-icon-circle {
          width: 50px;
          height: 50px;
          border: 2px solid #7c3aed;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #7c3aed;
          flex-shrink: 0;
          transition: all 0.3s ease;
          position: relative;
        }

        .source-icon-circle .connection-dot {
          position: absolute;
          right: -6px;
          top: 50%;
          transform: translateY(-50%);
        }

        .connection-dot {
          width: 8px;
          height: 8px;
          background: #3b82f6;
          border-radius: 50%;
          border: 2px solid white;
        }

        .excel-dot {
          background: #ef4444;
        }

        .data-source-item:hover .source-icon-circle {
          background: #7c3aed;
          color: white;
          transform: scale(1.1);
        }

        .source-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 2px;
          text-align: center;
        }

        .source-label {
          font-size: 0.75rem;
          font-weight: 600;
          color: #1e293b;
        }

        .source-count {
          font-size: 0.65rem;
          color: #64748b;
        }

        /* CENTER: Processing Matrix */
        .processing-matrix {
          padding: 24px;
          background: transparent;
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
        }

        .matrix-title {
          font-size: 1.1rem;
          font-weight: 700;
          color: #1e40af;
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
          background: transparent;
          border: none;
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
        }

        .stage-icon-wrapper {
          position: relative;
          display: inline-block;
          margin-bottom: 4px;
        }

        .stage-icon-wrapper .connection-dot {
          left: -6px;
          right: auto;
        }

        .stage-icon {
          color: #3b82f6;
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
          gap: 20px;
        }

        .output-group {
          border: none;
          background: transparent;
          padding: 0;
        }

        .group-title {
          font-size: 0.75rem;
          font-weight: 700;
          color: #059669;
          margin-bottom: 12px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .group-items {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .output-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
          padding: 8px;
          background: transparent;
          border: none;
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .output-item:hover {
          transform: translateY(-4px);
        }

        .output-icon-wrapper {
          position: relative;
          display: inline-block;
        }

        .output-icon-wrapper .connection-dot {
          left: auto;
          right: -6px;
        }

        .output-icon {
          color: #10b981;
        }

        .output-label {
          font-size: 0.75rem;
          font-weight: 600;
          color: #1e293b;
          text-align: center;
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
