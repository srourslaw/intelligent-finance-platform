Here's the exact logic for connecting files to the Input Layer (12 nodes) with blue lines:
Connection Logic
function drawAllConnections() {
    // Files to Layer 1 (Blue connections)
    let fileIdx = 0;
    fileStructure.forEach(group => {
        group.files.forEach(file => {
            const nodeIdx = fileIdx % nodesPerLayer;  // nodeIdx cycles 0-11
            const filePos = getPosition(`file-${fileIdx}`);
            if (filePos) {
                drawCurve(filePos, getPosition(`node-1-${nodeIdx}`), '#3b82f6', 0.15, 1);
            }
            fileIdx++;
        });
    });
    // ... rest of network connections ...
}

How It Works:

File Indexing: Each file gets a unique index (0 to 81)

File 0 → file-0
File 1 → file-1
...
File 81 → file-81


Node Distribution: Uses modulo operator % to cycle through 12 nodes
const nodeIdx = fileIdx % 12;
File 0 → Node 0
File 1 → Node 1
...
File 11 → Node 11
File 12 → Node 0 (cycles back)
File 13 → Node 1
etc.


Drawing Blue Lines:
drawCurve(
       getPosition(`file-${fileIdx}`),    // Start point: file position
       getPosition(`node-1-${nodeIdx}`),  // End point: input node position
       '#3b82f6',                         // Color: blue
       0.15,                              // Opacity: 15%
       1                                  // Line width: 1px
   );
   Bezier Curve Drawing:
   function drawCurve(start, end, color, opacity, width) {
       const dx = end.x - start.x;
       const cp1x = start.x + dx * 0.3;  // Control point creates curve
       const cp2x = start.x + dx * 0.7;

       ctx.beginPath();
       ctx.moveTo(start.x, start.y);
       ctx.bezierCurveTo(cp1x, start.y, cp2x, end.y, end.x, end.y);
       ctx.strokeStyle = color + Math.floor(opacity * 255).toString(16).padStart(2, '0');
       ctx.lineWidth = width;
       ctx.stroke();
   }
   Complete Flow:
   82 Files → Distributed → 12 Input Nodes

File 0  (Land_Contract.pdf)      → Node 0
File 1  (Land_Costs.xlsx)        → Node 1
File 2  (Legal_Fees.pdf)         → Node 2
...
File 11                          → Node 11
File 12                          → Node 0  (wraps around)
...
File 81                          → Node 9

Key Point: The modulo % operator ensures even distribution - no matter how many files (82), they're spread across exactly 12 nodes by cycling through.
