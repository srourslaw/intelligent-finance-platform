import { useState, useEffect, useRef } from 'react';

interface FileNode {
  name: string;
  type: 'folder' | 'excel' | 'pdf' | 'file' | 'json' | 'image' | 'csv' | 'md';
  path: string;
  children?: FileNode[];
  isExpanded?: boolean;
}

interface Project {
  project_id: string;
  project_name: string;
}

interface AIDataMappingAnimationProps {
  projectStructure: FileNode;
  projects: Project[];
  selectedProjectId: string;
  onProjectChange: (projectId: string) => void;
}

export function AIDataMappingAnimation({
  projectStructure,
  projects,
  selectedProjectId,
  onProjectChange
}: AIDataMappingAnimationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [speed, setSpeed] = useState(400);
  const [fileCounter, setFileCounter] = useState('0/0');
  const [outputCounter, setOutputCounter] = useState('0/7');
  const [progress, setProgress] = useState(0);
  const particlesRef = useRef<any[]>([]);
  const isPausedRef = useRef(false);
  const shouldStopRef = useRef(false);
  const speedRef = useRef(400); // Use ref so speed changes take effect immediately during animation
  const activeNodesRef = useRef<Set<string>>(new Set()); // Track active nodes for cleanup

  // Proportional speeds: each level is 2x faster than previous
  const speedLabels: Record<number, string> = { 800: 'Slow', 400: 'Normal', 200: 'Fast', 100: 'Ultra' };

  const outputs = ['Balance Sheet', 'Income Statement', 'Cash Flow Statement', 'Equity Statement', 'Ratios Dashboard', 'Assumptions', 'Instructions'];
  const nodesPerLayer = 12;
  const matrixSize = 10;

  // Build flat file structure from projectStructure
  const buildFileStructure = (node: FileNode): { folder: string; files: string[] }[] => {
    const result: { folder: string; files: string[] }[] = [];

    const traverse = (n: FileNode) => {
      if (n.type === 'folder' && n.children) {
        const files: string[] = [];
        n.children.forEach(child => {
          if (child.type !== 'folder') {
            files.push(child.name);
          } else {
            traverse(child);
          }
        });
        if (files.length > 0) {
          result.push({ folder: n.name, files });
        }
      }
    };

    traverse(node);
    return result;
  };

  const fileStructure = buildFileStructure(projectStructure);
  const totalFiles = fileStructure.reduce((acc, f) => acc + f.files.length, 0);

  // Initialize counter with total files
  useEffect(() => {
    setFileCounter(`0/${totalFiles}`);
  }, [totalFiles]);

  // Sync speedRef with speed state whenever speed changes
  useEffect(() => {
    speedRef.current = speed;
  }, [speed]);

  // Reset animation when project changes
  useEffect(() => {
    if (isRunning) {
      resetAll();
    }
  }, [selectedProjectId]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const updateCanvasSize = () => {
      const viz = document.querySelector('.viz-container');
      if (viz) {
        const rect = viz.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
      }
    };

    setTimeout(updateCanvasSize, 100);
    window.addEventListener('resize', updateCanvasSize);

    const animate = () => {
      if (canvas.width > 0 && canvas.height > 0) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawAllConnections(ctx);
        particlesRef.current = particlesRef.current.filter(p => p.active);
        particlesRef.current.forEach(p => drawParticle(ctx, p));
      }
      requestAnimationFrame(animate);
    };

    const animationId = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('resize', updateCanvasSize);
      cancelAnimationFrame(animationId);
    };
  }, [fileStructure]);

  const getPosition = (id: string) => {
    const el = document.getElementById(id);
    if (!el) return null;
    const rect = el.getBoundingClientRect();
    const vizRect = document.querySelector('.viz-container')?.getBoundingClientRect();
    if (!vizRect) return null;

    if (id.startsWith('file-')) {
      return {
        x: rect.right - vizRect.left,
        y: rect.top - vizRect.top + rect.height / 2
      };
    }

    if (id.startsWith('output-')) {
      return {
        x: rect.left - vizRect.left,
        y: rect.top - vizRect.top + rect.height / 2
      };
    }

    return {
      x: rect.left - vizRect.left + rect.width / 2,
      y: rect.top - vizRect.top + rect.height / 2
    };
  };

  const drawCurve = (ctx: CanvasRenderingContext2D, start: any, end: any, color: string, opacity = 0.2, width = 1) => {
    if (!start || !end) return;
    const dx = end.x - start.x;
    const cp1x = start.x + dx * 0.3;
    const cp2x = start.x + dx * 0.7;
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.bezierCurveTo(cp1x, start.y, cp2x, end.y, end.x, end.y);
    const hexOpacity = Math.floor(opacity * 255).toString(16).padStart(2, '0');
    ctx.strokeStyle = color + hexOpacity;
    ctx.lineWidth = width;
    ctx.stroke();
  };

  const drawAllConnections = (ctx: CanvasRenderingContext2D) => {
    // Files to Layer 1 - draw faint lines for all, will be highlighted when active
    let fileIdx = 0;
    fileStructure.forEach(group => {
      group.files.forEach(() => {
        const nodeIdx = fileIdx % nodesPerLayer;
        const filePos = getPosition(`file-${fileIdx}`);
        const nodePos = getPosition(`node-1-${nodeIdx}`);
        const fileEl = document.getElementById(`file-${fileIdx}`);
        const isActive = fileEl?.classList.contains('active');

        if (filePos && nodePos) {
          drawCurve(ctx, filePos, nodePos, '#3b82f6', isActive ? 0.6 : 0.05, isActive ? 1.2 : 1);
        }
        fileIdx++;
      });
    });

    // Layer 1 to Layer 2 - pulse when both nodes are active
    for (let i = 0; i < nodesPerLayer; i++) {
      const node1Active = document.getElementById(`node-1-${i}`)?.classList.contains('active');

      for (let j = 0; j < nodesPerLayer; j++) {
        const n1 = getPosition(`node-1-${i}`);
        const n2 = getPosition(`node-2-${j}`);
        const node2Active = document.getElementById(`node-2-${j}`)?.classList.contains('active');

        // Only highlight if both connected nodes are active
        const isActive = node1Active && node2Active;

        if (n1 && n2) {
          drawCurve(ctx, n1, n2, '#ef4444', isActive ? 0.6 : 0.08, isActive ? 1.5 : 0.8);
        }
      }
    }

    // Layer 2 to Matrix - only pulse the specific connections being used
    for (let i = 0; i < nodesPerLayer; i++) {
      const node2Active = document.getElementById(`node-2-${i}`)?.classList.contains('active');

      for (let j = 0; j < matrixSize; j++) {
        const cellIdx = Math.floor(j * matrixSize + matrixSize / 2);
        const n2 = getPosition(`node-2-${i}`);
        const cell = getPosition(`cell-${cellIdx}`);
        const cellActive = document.getElementById(`cell-${cellIdx}`)?.classList.contains('active');

        // Only highlight if both connected elements are active
        const isActive = node2Active && cellActive;
        if (n2 && cell) drawCurve(ctx, n2, cell, '#a78bfa', isActive ? 0.5 : 0.08, isActive ? 1.2 : 0.8);
      }
    }

    // Matrix to Layer 3 - only pulse the specific connections being used
    for (let i = 0; i < matrixSize; i++) {
      const cellIdx = Math.floor(i * matrixSize + matrixSize / 2);
      const cellActive = document.getElementById(`cell-${cellIdx}`)?.classList.contains('active');

      for (let j = 0; j < nodesPerLayer; j++) {
        const cell = getPosition(`cell-${cellIdx}`);
        const n3 = getPosition(`node-3-${j}`);
        const node3Active = document.getElementById(`node-3-${j}`)?.classList.contains('active');

        // Only highlight if both connected elements are active
        const isActive = cellActive && node3Active;
        if (cell && n3) drawCurve(ctx, cell, n3, '#8b5cf6', isActive ? 0.5 : 0.08, isActive ? 1.2 : 0.8);
      }
    }

    // Layer 3 to Layer 4 - only pulse the specific connections being used
    for (let i = 0; i < nodesPerLayer; i++) {
      const node3Active = document.getElementById(`node-3-${i}`)?.classList.contains('active');

      for (let j = 0; j < nodesPerLayer; j++) {
        const n3 = getPosition(`node-3-${i}`);
        const n4 = getPosition(`node-4-${j}`);
        const node4Active = document.getElementById(`node-4-${j}`)?.classList.contains('active');

        // Only highlight if both connected nodes are active
        const isActive = node3Active && node4Active;
        if (n3 && n4) drawCurve(ctx, n3, n4, '#10b981', isActive ? 0.5 : 0.08, isActive ? 1.2 : 0.8);
      }
    }

    // Layer 4 to Output Hub - only pulse when both are active
    const hubPos = getPosition('outputHub');
    const hubActive = document.getElementById('outputHub')?.classList.contains('active');
    if (hubPos) {
      for (let i = 0; i < nodesPerLayer; i++) {
        const n4 = getPosition(`node-4-${i}`);
        const node4Active = document.getElementById(`node-4-${i}`)?.classList.contains('active');
        const isActive = node4Active && hubActive;
        if (n4) drawCurve(ctx, n4, hubPos, '#10b981', isActive ? 0.6 : 0.15, isActive ? 1.5 : 1);
      }

      // Output Hub to Outputs - only pulse when both are active
      outputs.forEach((_, i) => {
        const outPos = getPosition(`output-${i}`);
        const outActive = document.getElementById(`output-${i}`)?.classList.contains('active');
        const isActive = hubActive && outActive;
        if (outPos) drawCurve(ctx, hubPos, outPos, '#10b981', isActive ? 0.7 : 0.2, isActive ? 1.5 : 1);
      });
    }
  };

  const createParticle = (startId: string, endId: string, color: string) => ({
    start: startId,
    end: endId,
    progress: 0,
    speed: 0.025,
    color,
    active: true
  });

  const updateParticle = (p: any) => {
    p.progress += p.speed;
    if (p.progress >= 1) { p.active = false; return null; }
    const start = getPosition(p.start);
    const end = getPosition(p.end);
    if (!start || !end) return null;
    const t = p.progress;
    const dx = end.x - start.x;
    const cp1x = start.x + dx * 0.3;
    const cp2x = start.x + dx * 0.7;
    const x = Math.pow(1-t, 3) * start.x + 3 * Math.pow(1-t, 2) * t * cp1x + 3 * (1-t) * t * t * cp2x + Math.pow(t, 3) * end.x;
    const y = Math.pow(1-t, 3) * start.y + 3 * Math.pow(1-t, 2) * t * start.y + 3 * (1-t) * t * t * end.y + Math.pow(t, 3) * end.y;
    return { x, y };
  };

  const drawParticle = (ctx: CanvasRenderingContext2D, p: any) => {
    const pos = updateParticle(p);
    if (!pos) return;
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 5, 0, Math.PI * 2);
    const gradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, 5);
    gradient.addColorStop(0, p.color);
    gradient.addColorStop(1, p.color + '00');
    ctx.fillStyle = gradient;
    ctx.shadowBlur = 20;
    ctx.shadowColor = p.color;
    ctx.fill();
    ctx.shadowBlur = 0;
  };

  const sleep = (ms: number) => new Promise<void>(resolve => {
    const checkPause = () => {
      if (shouldStopRef.current) {
        resolve(); // Exit immediately if stopped
      } else if (!isPausedRef.current) {
        resolve();
      } else {
        setTimeout(checkPause, 50);
      }
    };
    setTimeout(checkPause, ms);
  });

  // Clean up active nodes
  const deactivateNode = (nodeId: string) => {
    document.getElementById(nodeId)?.classList.remove('active');
    activeNodesRef.current.delete(nodeId);
  };

  const activateNode = (nodeId: string) => {
    document.getElementById(nodeId)?.classList.add('active');
    activeNodesRef.current.add(nodeId);
  };

  const startAnimation = async () => {
    if (isRunning) return;

    setIsRunning(true);
    setIsPaused(false);
    isPausedRef.current = false;
    shouldStopRef.current = false;
    activeNodesRef.current.clear();
    let processedFiles = 0;

    for (let folderIdx = 0; folderIdx < fileStructure.length; folderIdx++) {
      if (shouldStopRef.current) break;
      const folder = fileStructure[folderIdx];
      activateNode(`folder-${folderIdx}`);

      for (let fileIdx = 0; fileIdx < folder.files.length; fileIdx++) {
        if (shouldStopRef.current) break;
        const globalFileIdx = processedFiles;
        const nodeIdx = globalFileIdx % nodesPerLayer;
        const node2Idx = (nodeIdx + 2) % nodesPerLayer;
        const node3Idx = (nodeIdx + 1) % nodesPerLayer;
        const cellIndices: number[] = [];

        // Activate file and nodes
        activateNode(`file-${globalFileIdx}`);
        activateNode(`node-1-${nodeIdx}`);

        // Create particles immediately
        for (let p = 0; p < 3; p++) {
          particlesRef.current.push(createParticle(`file-${globalFileIdx}`, `node-1-${nodeIdx}`, '#3b82f6'));
        }
        await sleep(speedRef.current / 6);

        activateNode(`node-2-${node2Idx}`);
        for (let p = 0; p < 2; p++) {
          particlesRef.current.push(createParticle(`node-1-${nodeIdx}`, `node-2-${node2Idx}`, '#ef4444'));
        }
        await sleep(speedRef.current / 6);

        // Activate matrix cells
        for (let j = 0; j < 5; j++) {
          const cellIdx = Math.floor(Math.random() * (matrixSize * matrixSize));
          cellIndices.push(cellIdx);
          activateNode(`cell-${cellIdx}`);
          particlesRef.current.push(createParticle(`node-2-${node2Idx}`, `cell-${cellIdx}`, '#a78bfa'));
          particlesRef.current.push(createParticle(`node-2-${node2Idx}`, `cell-${cellIdx}`, '#a78bfa'));
        }
        await sleep(speedRef.current / 6);

        activateNode(`node-3-${node3Idx}`);
        for (let p = 0; p < 2; p++) {
          particlesRef.current.push(createParticle(`cell-${nodeIdx * matrixSize}`, `node-3-${node3Idx}`, '#8b5cf6'));
        }
        await sleep(speedRef.current / 6);

        activateNode(`node-4-${nodeIdx}`);
        for (let p = 0; p < 2; p++) {
          particlesRef.current.push(createParticle(`node-3-${node3Idx}`, `node-4-${nodeIdx}`, '#10b981'));
        }
        await sleep(speedRef.current / 6);

        activateNode('outputHub');
        for (let p = 0; p < 2; p++) {
          particlesRef.current.push(createParticle(`node-4-${nodeIdx}`, 'outputHub', '#10b981'));
        }
        await sleep(speedRef.current / 6);

        const outputIdx = Math.floor(processedFiles / (totalFiles / outputs.length));
        if (outputIdx < outputs.length) {
          for (let p = 0; p < 2; p++) {
            particlesRef.current.push(createParticle('outputHub', `output-${outputIdx}`, '#10b981'));
          }
          activateNode(`output-${outputIdx}`);
        }

        // Clean up after a brief display
        await sleep(speedRef.current / 3);
        deactivateNode(`file-${globalFileIdx}`);
        deactivateNode(`node-1-${nodeIdx}`);
        deactivateNode(`node-2-${node2Idx}`);
        deactivateNode(`node-3-${node3Idx}`);
        deactivateNode(`node-4-${nodeIdx}`);
        deactivateNode('outputHub');
        cellIndices.forEach(idx => deactivateNode(`cell-${idx}`));

        processedFiles++;
        setFileCounter(`${processedFiles}/${totalFiles}`);
        setProgress(processedFiles / totalFiles * 100);
        await sleep(speedRef.current / 8);
      }
      deactivateNode(`folder-${folderIdx}`);
    }
    if (!shouldStopRef.current) {
      setOutputCounter(`${outputs.length}/${outputs.length}`);
      setIsRunning(false);
    }
  };

  const togglePlayPause = () => {
    if (!isRunning) {
      startAnimation();
    } else {
      isPausedRef.current = !isPausedRef.current;
      setIsPaused(isPausedRef.current);
    }
  };

  const resetAll = () => {
    // Signal animation to stop
    shouldStopRef.current = true;
    isPausedRef.current = false;
    setIsPaused(false);
    setIsRunning(false);

    // Clear all active nodes
    activeNodesRef.current.forEach(nodeId => deactivateNode(nodeId));
    activeNodesRef.current.clear();

    // Clear all visual states
    document.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
    setProgress(0);
    setFileCounter(`0/${totalFiles}`);
    setOutputCounter('0/7');
    particlesRef.current = [];
  };

  const toggleSpeed = () => {
    // Proportional speeds: each level is 2x faster (half the delay)
    const speeds = [800, 400, 200, 100];
    const idx = speeds.indexOf(speed);
    const newSpeed = speeds[(idx + 1) % speeds.length];
    setSpeed(newSpeed);
    // speedRef.current is updated automatically by useEffect
  };

  return (
    <div style={{ background: 'transparent', padding: '0', position: 'relative' }}>
      <div style={{ position: 'fixed', top: 0, left: 0, height: '3px', background: 'linear-gradient(90deg, #3b82f6, #8b5cf6)', width: `${progress}%`, transition: 'width 0.3s', zIndex: 1000 }} />

      <div style={{ width: '100%' }}>
        <div style={{ textAlign: 'center', padding: '20px 0 40px' }}>
          <h1 style={{ fontSize: '2.2em', color: '#1f2937', marginBottom: '8px', fontWeight: 700 }}>AI Data Mapping & Transformation</h1>
          <p style={{ color: '#6b7280', fontSize: '1em' }}>Neural Network Processing • Real-time Data Flow Visualization</p>
        </div>

        <div className="viz-container" style={{ display: 'grid', gridTemplateColumns: '240px 1fr 240px', gap: '60px', position: 'relative', minHeight: '800px', padding: '60px 0' }}>
          <canvas ref={canvasRef} id="mainCanvas" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 1 }} />

          <div style={{ position: 'relative', zIndex: 2, display: 'flex', flexDirection: 'column', gap: '3px', maxHeight: '750px', overflowY: 'auto', paddingRight: '10px', perspective: '1000px' }}>
            <div style={{ fontSize: '0.75em', fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '16px', paddingBottom: '10px', borderBottom: '2px solid #e5e7eb', textAlign: 'center' }}>
              File Processing
              <span style={{ display: 'block', fontSize: '1.1em', color: '#3b82f6', fontWeight: 700, marginTop: '6px' }}>{fileCounter}</span>

              {/* Project Selector */}
              <select
                value={selectedProjectId}
                onChange={(e) => onProjectChange(e.target.value)}
                style={{
                  marginTop: '12px',
                  width: '100%',
                  padding: '8px 12px',
                  fontSize: '0.9em',
                  fontWeight: 600,
                  color: '#374151',
                  background: 'white',
                  border: '2px solid #e5e7eb',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  outline: 'none',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.borderColor = '#3b82f6'}
                onMouseLeave={(e) => e.currentTarget.style.borderColor = '#e5e7eb'}
              >
                {projects.map((project) => (
                  <option key={project.project_id} value={project.project_id}>
                    {project.project_name}
                  </option>
                ))}
              </select>
            </div>
            {fileStructure.map((group, groupIdx) => {
              const startIndex = fileStructure.slice(0, groupIdx).reduce((acc, f) => acc + f.files.length, 0);
              return (
                <div key={groupIdx} style={{ marginBottom: '4px', transformStyle: 'preserve-3d' }}>
                  <div id={`folder-${groupIdx}`} className="folder-header" style={{ fontSize: '0.6em', color: '#ed8936', fontWeight: 600, padding: '3px 6px', cursor: 'pointer', transition: 'all 0.2s', borderRadius: '3px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    📁 {group.folder}
                  </div>
                  <div style={{ marginLeft: '12px', marginTop: '2px', display: 'flex', flexDirection: 'column', gap: '1px', transformStyle: 'preserve-3d' }}>
                    {group.files.map((file, fileIdx) => (
                      <div key={fileIdx} id={`file-${startIndex + fileIdx}`} className="file-item" style={{ fontSize: '0.55em', color: '#6b7280', padding: '2px 6px', cursor: 'pointer', transition: 'all 0.2s', borderRadius: '2px', transform: 'translateZ(0px)', display: 'flex', alignItems: 'center' }}>
                        <span>📄 {file}</span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          <div style={{ position: 'relative', zIndex: 2, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div style={{ display: 'flex', gap: '80px', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
              <div id="layer1" style={{ display: 'flex', flexDirection: 'column', gap: '20px', position: 'relative', marginLeft: '-40px' }}>
                <div style={{ position: 'absolute', top: '-45px', left: '50%', transform: 'translateX(-50%)', fontSize: '0.7em', fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.5px', whiteSpace: 'nowrap', textAlign: 'center' }}>
                  Input Layer<span style={{ display: 'block', color: '#3b82f6', fontSize: '0.95em', marginTop: '2px' }}>12 nodes</span>
                </div>
                {[...Array(nodesPerLayer)].map((_, i) => <div key={i} id={`node-1-${i}`} className="neural-node layer1" style={{ width: '16px', height: '16px', borderRadius: '50%', background: '#3b82f6', transition: 'all 0.3s' }} />)}
              </div>

              <div id="layer2" style={{ display: 'flex', flexDirection: 'column', gap: '20px', position: 'relative' }}>
                <div style={{ position: 'absolute', top: '-45px', left: '50%', transform: 'translateX(-50%)', fontSize: '0.7em', fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.5px', whiteSpace: 'nowrap', textAlign: 'center' }}>
                  Processing Layer<span style={{ display: 'block', color: '#3b82f6', fontSize: '0.95em', marginTop: '2px' }}>12 nodes</span>
                </div>
                {[...Array(nodesPerLayer)].map((_, i) => <div key={i} id={`node-2-${i}`} className="neural-node layer2" style={{ width: '16px', height: '16px', borderRadius: '50%', background: '#ef4444', transition: 'all 0.3s' }} />)}
              </div>

              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', top: '-45px', left: '50%', transform: 'translateX(-50%)', fontSize: '0.7em', fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.5px', whiteSpace: 'nowrap', textAlign: 'center' }}>Mapping Layer</div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(10, 20px)', gap: '3px' }}>
                  {[...Array(matrixSize * matrixSize)].map((_, i) => <div key={i} id={`cell-${i}`} className="matrix-cell" style={{ width: '20px', height: '20px', background: '#f3f4f6', borderRadius: '3px', transition: 'all 0.3s' }} />)}
                </div>
              </div>

              <div id="layer3" style={{ display: 'flex', flexDirection: 'column', gap: '20px', position: 'relative', marginRight: '-40px' }}>
                <div style={{ position: 'absolute', top: '-45px', left: '50%', transform: 'translateX(-50%)', fontSize: '0.7em', fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.5px', whiteSpace: 'nowrap', textAlign: 'center' }}>
                  Processing Layer<span style={{ display: 'block', color: '#3b82f6', fontSize: '0.95em', marginTop: '2px' }}>12 nodes</span>
                </div>
                {[...Array(nodesPerLayer)].map((_, i) => <div key={i} id={`node-3-${i}`} className="neural-node layer3" style={{ width: '16px', height: '16px', borderRadius: '50%', background: '#9ca3af', transition: 'all 0.3s' }} />)}
              </div>

              <div id="layer4" style={{ display: 'flex', flexDirection: 'column', gap: '20px', position: 'relative' }}>
                <div style={{ position: 'absolute', top: '-45px', left: '50%', transform: 'translateX(-50%)', fontSize: '0.7em', fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.5px', whiteSpace: 'nowrap', textAlign: 'center' }}>
                  Output Layer<span style={{ display: 'block', color: '#3b82f6', fontSize: '0.95em', marginTop: '2px' }}>12 nodes</span>
                </div>
                {[...Array(nodesPerLayer)].map((_, i) => <div key={i} id={`node-4-${i}`} className="neural-node layer4" style={{ width: '16px', height: '16px', borderRadius: '50%', background: '#10b981', transition: 'all 0.3s' }} />)}
              </div>
            </div>
          </div>

          <div style={{ position: 'relative', zIndex: 2, display: 'flex', flexDirection: 'column', gap: '6px', alignItems: 'center' }}>
            <div id="outputHub" style={{ width: '20px', height: '20px', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', borderRadius: '50%', position: 'absolute', left: '-50px', top: '50%', transform: 'translateY(-50%)', boxShadow: '0 0 20px rgba(16, 185, 129, 0.4)', zIndex: 3 }} />
            <div style={{ fontSize: '0.75em', fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '16px', paddingBottom: '10px', borderBottom: '2px solid #e5e7eb', textAlign: 'center', width: '100%' }}>
              Financial Analysis
              <span style={{ display: 'block', fontSize: '1.1em', color: '#3b82f6', fontWeight: 700, marginTop: '6px' }}>{outputCounter}</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', width: '100%' }}>
              {outputs.map((item, i) => (
                <div key={i} id={`output-${i}`} className="output-item" style={{ fontSize: '0.8em', color: '#374151', padding: '8px 12px', cursor: 'pointer', transition: 'all 0.3s', borderRadius: '6px', opacity: 0.4, textAlign: 'center', border: '2px solid transparent' }}>
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div style={{ position: 'sticky', bottom: '30px', left: '50%', transform: 'translateX(-50%)', background: 'white', border: '1px solid #e5e7eb', borderRadius: '50px', padding: '12px 25px', display: 'flex', gap: '12px', boxShadow: '0 10px 40px rgba(0,0,0,0.1)', zIndex: 100, marginTop: '30px', width: 'fit-content', marginLeft: 'auto', marginRight: 'auto' }}>
          <button onClick={togglePlayPause} style={{ background: isRunning && !isPaused ? '#f59e0b' : '#3b82f6', color: 'white', border: 'none', padding: '8px 20px', borderRadius: '20px', fontWeight: 600, cursor: 'pointer', transition: 'all 0.3s', fontSize: '0.85em' }}>
            {isRunning && !isPaused ? '⏸ Pause' : '▶ Start'}
          </button>
          <button onClick={resetAll} style={{ background: '#f3f4f6', color: '#374151', border: 'none', padding: '8px 20px', borderRadius: '20px', fontWeight: 600, cursor: 'pointer', transition: 'all 0.3s', fontSize: '0.85em' }}>↻ Reset</button>
          <button onClick={toggleSpeed} style={{ background: '#f3f4f6', color: '#374151', border: 'none', padding: '8px 20px', borderRadius: '20px', fontWeight: 600, cursor: 'pointer', transition: 'all 0.3s', fontSize: '0.85em' }}>⚡ {speedLabels[speed]}</button>
        </div>
      </div>

      <style>{`
        .folder-header:hover { background: #fff7ed; transform: translateZ(5px); }
        .folder-header.active { background: #fed7aa; color: #9a3412; transform: translateZ(10px); }
        .file-item:hover { background: #f3f4f6; color: #374151; transform: translateZ(8px) translateX(2px); }
        .file-item.active { background: #dbeafe; color: #1e40af; font-weight: 600; box-shadow: 0 0 15px rgba(59, 130, 246, 0.3); transform: translateZ(15px) translateX(5px) scale(1.05); }
        .neural-node.active { box-shadow: 0 0 20px rgba(59, 130, 246, 0.6); animation: nodePulse 1s ease-in-out infinite; }
        @keyframes nodePulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.3); } }
        .matrix-cell.active { background: #8b5cf6 !important; box-shadow: 0 0 20px rgba(139, 92, 246, 0.8); animation: matrixGlow 1s ease-in-out infinite; }
        @keyframes matrixGlow { 0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.8); } 50% { box-shadow: 0 0 30px rgba(139, 92, 246, 1); } }
        .output-item.active { opacity: 1; background: #dcfce7; color: #166534; font-weight: 600; transform: translateX(-3px); border: 2px solid #10b981; }
        #outputHub.active { animation: hubPulse 1s ease-in-out infinite; }
        @keyframes hubPulse { 0%, 100% { transform: translateY(-50%) scale(1); box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); } 50% { transform: translateY(-50%) scale(1.2); box-shadow: 0 0 30px rgba(16, 185, 129, 0.8); } }
      `}</style>
    </div>
  );
}
