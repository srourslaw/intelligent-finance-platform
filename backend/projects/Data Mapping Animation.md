<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial AI Data Mapping</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 1400px;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            box-shadow: 0 30px 90px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            position: relative;
            overflow: hidden;
        }

        .header {
            text-align: center;
            margin-bottom: 60px;
        }

        .header h1 {
            font-size: 3em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            font-weight: 800;
        }

        .header p {
            font-size: 1.2em;
            color: #666;
            font-weight: 500;
        }

        .mapping-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 60px;
            position: relative;
            min-height: 600px;
        }

        .source-files, .target-statements {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .section-title {
            font-size: 1.4em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .icon {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            color: white;
            font-size: 1.2em;
        }

        .file-item, .statement-item {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 18px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .file-item:hover, .statement-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
            border-color: #667eea;
        }

        .file-item.active {
            border-color: #667eea;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            transform: scale(1.02);
        }

        .statement-item.active {
            border-color: #10b981;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
            transform: scale(1.02);
        }

        .file-icon {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
            flex-shrink: 0;
        }

        .excel-icon {
            background: linear-gradient(135deg, #107c41 0%, #0e6537 100%);
            color: white;
        }

        .pdf-icon {
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
            color: white;
        }

        .json-icon {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
        }

        .file-details {
            flex: 1;
        }

        .file-name {
            font-weight: 600;
            color: #1f2937;
            font-size: 0.95em;
            margin-bottom: 4px;
        }

        .file-type {
            font-size: 0.8em;
            color: #6b7280;
            font-weight: 500;
        }

        .statement-icon {
            width: 48px;
            height: 48px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            flex-shrink: 0;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }

        .statement-details {
            flex: 1;
        }

        .statement-name {
            font-weight: 700;
            color: #1f2937;
            font-size: 1.05em;
            margin-bottom: 4px;
        }

        .statement-desc {
            font-size: 0.85em;
            color: #6b7280;
        }

        .connector-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }

        .ai-processor {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
            z-index: 10;
            animation: pulse 2s ease-in-out infinite;
        }

        .ai-processor::before {
            content: '';
            position: absolute;
            inset: -3px;
            border-radius: 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            opacity: 0.5;
            filter: blur(10px);
            animation: rotate 3s linear infinite;
        }

        .ai-icon {
            font-size: 3em;
            z-index: 1;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.05); }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .processing-badge {
            position: absolute;
            top: -10px;
            right: -10px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
            animation: bounce 0.5s ease;
        }

        @keyframes bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .confidence-indicator {
            position: absolute;
            bottom: 8px;
            right: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.75em;
            font-weight: 600;
        }

        .confidence-bar {
            width: 60px;
            height: 4px;
            background: #e5e7eb;
            border-radius: 2px;
            overflow: hidden;
        }

        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            transition: width 0.5s ease;
        }

        .stats-panel {
            margin-top: 50px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            border: 2px solid #dee2e6;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .stat-label {
            font-size: 0.9em;
            color: #6b7280;
            font-weight: 600;
        }

        .control-panel {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 20px 30px;
            border-radius: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
            display: flex;
            gap: 15px;
            align-items: center;
            z-index: 100;
        }

        .control-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.95em;
        }

        .control-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .control-btn.secondary {
            background: #e5e7eb;
            color: #4b5563;
        }

        .control-btn.secondary:hover {
            background: #d1d5db;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        @media (max-width: 1024px) {
            .mapping-container {
                flex-direction: column;
                gap: 40px;
            }

            .ai-processor {
                position: relative;
                transform: none;
                margin: 20px auto;
            }

            .stats-panel {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI-Powered Financial Data Mapping</h1>
            <p>Transforming Messy Project Files into Professional Financial Statements</p>
        </div>

        <div class="mapping-container">
            <canvas class="connector-canvas" id="connectorCanvas"></canvas>

            <!-- Source Files -->
            <div class="source-files" id="sourceFiles">
                <div class="section-title">
                    <div class="icon">📂</div>
                    Source Files (Project Data)
                </div>
                <!-- Files will be dynamically added here -->
            </div>

            <!-- AI Processor -->
            <div class="ai-processor">
                <div class="ai-icon">🧠</div>
            </div>

            <!-- Target Statements -->
            <div class="target-statements" id="targetStatements">
                <div class="section-title">
                    <div class="icon">📊</div>
                    Financial Statements
                </div>
                <!-- Statements will be dynamically added here -->
            </div>
        </div>

        <div class="stats-panel">
            <div class="stat-card">
                <div class="stat-value" id="filesProcessed">0</div>
                <div class="stat-label">Files Processed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="dataPoints">0</div>
                <div class="stat-label">Data Points Extracted</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="accuracy">0%</div>
                <div class="stat-label">Classification Accuracy</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="processingTime">0s</div>
                <div class="stat-label">Processing Time</div>
            </div>
        </div>

        <div class="control-panel">
            <button class="control-btn" onclick="startMapping()">▶ Start Mapping</button>
            <button class="control-btn secondary" onclick="resetMapping()">↻ Reset</button>
            <button class="control-btn secondary" onclick="toggleSpeed()">⚡ Speed: <span id="speedLabel">Normal</span></button>
        </div>
    </div>

    <script>
        // Sample project files from the directory structure
        const sourceFiles = [
            { name: 'MASTER_PROJECT_BUDGET.xlsx', type: 'Budget', icon: '📊', category: 'excel', folder: '12_BUDGET_TRACKING' },
            { name: 'Income_Statement_Sept_2024.xlsx', type: 'Financial Statement', icon: '💰', category: 'excel', folder: '19_MONTHLY_CLOSE' },
            { name: 'Balance_Sheet_Sept_2024.xlsx', type: 'Financial Statement', icon: '⚖️', category: 'excel', folder: '19_MONTHLY_CLOSE' },
            { name: 'Cash_Flow_Statement_Sept_2024.xlsx', type: 'Cash Flow', icon: '💵', category: 'excel', folder: '19_MONTHLY_CLOSE' },
            { name: 'Land_Costs.xlsx', type: 'Asset Purchase', icon: '🏗️', category: 'excel', folder: '01_LAND_PURCHASE' },
            { name: 'Materials_Purchases_Summary.xlsx', type: 'Expenses', icon: '🛠️', category: 'excel', folder: '06_PURCHASE_ORDERS_INVOICES' },
            { name: 'Labour_Costs_Summary.xlsx', type: 'Payroll', icon: '👷', category: 'excel', folder: '08_LABOUR_TIMESHEETS' },
            { name: 'Loan_Agreement.pdf', type: 'Liability Document', icon: '🏦', category: 'pdf', folder: '04_FINANCE_INSURANCE' },
            { name: 'Client_Payment_Tracker.xlsx', type: 'Revenue', icon: '💳', category: 'excel', folder: '11_CLIENT_BILLING' },
            { name: 'Bank_Statement_Sept_2024.pdf', type: 'Bank Record', icon: '🏛️', category: 'pdf', folder: '20_BANK_RECONCILIATION' },
        ];

        const targetStatements = [
            { name: 'Balance Sheet', desc: 'Assets, Liabilities & Equity', icon: '⚖️', color: '#10b981' },
            { name: 'Income Statement', desc: 'Revenue & Expenses', icon: '💰', color: '#3b82f6' },
            { name: 'Cash Flow Statement', desc: 'Operating, Investing, Financing', icon: '💵', color: '#8b5cf6' },
            { name: 'Equity Statement', desc: 'Changes in Ownership', icon: '📈', color: '#f59e0b' },
            { name: 'Ratios Dashboard', desc: 'Financial Metrics & KPIs', icon: '📊', color: '#ec4899' },
        ];

        // Mapping rules (which files map to which statements)
        const mappingRules = {
            'MASTER_PROJECT_BUDGET.xlsx': ['Balance Sheet', 'Income Statement'],
            'Income_Statement_Sept_2024.xlsx': ['Income Statement'],
            'Balance_Sheet_Sept_2024.xlsx': ['Balance Sheet', 'Equity Statement'],
            'Cash_Flow_Statement_Sept_2024.xlsx': ['Cash Flow Statement'],
            'Land_Costs.xlsx': ['Balance Sheet'],
            'Materials_Purchases_Summary.xlsx': ['Income Statement', 'Cash Flow Statement'],
            'Labour_Costs_Summary.xlsx': ['Income Statement', 'Cash Flow Statement'],
            'Loan_Agreement.pdf': ['Balance Sheet'],
            'Client_Payment_Tracker.xlsx': ['Income Statement', 'Cash Flow Statement'],
            'Bank_Statement_Sept_2024.pdf': ['Cash Flow Statement', 'Balance Sheet'],
        };

        let animationSpeed = 1000; // milliseconds
        let isAnimating = false;
        let currentFileIndex = 0;

        // Initialize
        function init() {
            renderSourceFiles();
            renderTargetStatements();
            setupCanvas();
        }

        function renderSourceFiles() {
            const container = document.getElementById('sourceFiles');
            sourceFiles.forEach((file, index) => {
                const fileElement = document.createElement('div');
                fileElement.className = 'file-item';
                fileElement.id = `file-${index}`;
                
                const iconClass = file.category === 'excel' ? 'excel-icon' : 
                                 file.category === 'pdf' ? 'pdf-icon' : 'json-icon';
                
                fileElement.innerHTML = `
                    <div class="file-icon ${iconClass}">${file.icon}</div>
                    <div class="file-details">
                        <div class="file-name">${file.name}</div>
                        <div class="file-type">${file.type} • ${file.folder}</div>
                    </div>
                `;
                
                container.appendChild(fileElement);
            });
        }

        function renderTargetStatements() {
            const container = document.getElementById('targetStatements');
            targetStatements.forEach((statement, index) => {
                const statementElement = document.createElement('div');
                statementElement.className = 'statement-item';
                statementElement.id = `statement-${index}`;
                
                statementElement.innerHTML = `
                    <div class="statement-icon">${statement.icon}</div>
                    <div class="statement-details">
                        <div class="statement-name">${statement.name}</div>
                        <div class="statement-desc">${statement.desc}</div>
                    </div>
                    <div class="confidence-indicator">
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: 0%"></div>
                        </div>
                    </div>
                `;
                
                container.appendChild(statementElement);
            });
        }

        function setupCanvas() {
            const canvas = document.getElementById('connectorCanvas');
            const container = document.querySelector('.mapping-container');
            canvas.width = container.offsetWidth;
            canvas.height = container.offsetHeight;
        }

        function drawConnection(fileIndex, statementName, progress = 1, isActive = true) {
            const canvas = document.getElementById('connectorCanvas');
            const ctx = canvas.getContext('2d');
            
            const fileEl = document.getElementById(`file-${fileIndex}`);
            const statementIndex = targetStatements.findIndex(s => s.name === statementName);
            const statementEl = document.getElementById(`statement-${statementIndex}`);
            
            if (!fileEl || !statementEl) return;
            
            const fileRect = fileEl.getBoundingClientRect();
            const statementRect = statementEl.getBoundingClientRect();
            const containerRect = canvas.getBoundingClientRect();
            
            const startX = fileRect.right - containerRect.left;
            const startY = fileRect.top - containerRect.top + fileRect.height / 2;
            const endX = statementRect.left - containerRect.left;
            const endY = statementRect.top - containerRect.top + statementRect.height / 2;
            
            const controlX1 = startX + (endX - startX) * 0.3;
            const controlX2 = startX + (endX - startX) * 0.7;
            
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.bezierCurveTo(controlX1, startY, controlX2, endY, endX, endY);
            
            if (isActive) {
                ctx.strokeStyle = `rgba(102, 126, 234, ${progress})`;
                ctx.lineWidth = 3;
                ctx.shadowColor = 'rgba(102, 126, 234, 0.5)';
                ctx.shadowBlur = 10;
            } else {
                ctx.strokeStyle = 'rgba(16, 185, 129, 0.3)';
                ctx.lineWidth = 2;
                ctx.shadowBlur = 0;
            }
            
            ctx.stroke();
            
            // Draw animated particles along the path
            if (isActive && progress === 1) {
                for (let i = 0; i < 3; i++) {
                    const t = (Date.now() / 1000 + i * 0.3) % 1;
                    const x = Math.pow(1-t, 3) * startX + 3 * Math.pow(1-t, 2) * t * controlX1 + 
                             3 * (1-t) * Math.pow(t, 2) * controlX2 + Math.pow(t, 3) * endX;
                    const y = Math.pow(1-t, 3) * startY + 3 * Math.pow(1-t, 2) * t * startY + 
                             3 * (1-t) * Math.pow(t, 2) * endY + Math.pow(t, 3) * endY;
                    
                    ctx.beginPath();
                    ctx.arc(x, y, 4, 0, Math.PI * 2);
                    ctx.fillStyle = '#667eea';
                    ctx.shadowColor = '#667eea';
                    ctx.shadowBlur = 10;
                    ctx.fill();
                }
            }
        }

        async function startMapping() {
            if (isAnimating) return;
            isAnimating = true;
            
            const startTime = Date.now();
            let totalDataPoints = 0;
            
            for (let i = 0; i < sourceFiles.length; i++) {
                currentFileIndex = i;
                const file = sourceFiles[i];
                const fileEl = document.getElementById(`file-${i}`);
                
                // Highlight current file
                fileEl.classList.add('active');
                
                // Add processing badge
                const badge = document.createElement('div');
                badge.className = 'processing-badge';
                badge.textContent = 'Processing...';
                fileEl.appendChild(badge);
                
                // Update stats
                document.getElementById('filesProcessed').textContent = i + 1;
                totalDataPoints += Math.floor(Math.random() * 50) + 20;
                document.getElementById('dataPoints').textContent = totalDataPoints;
                
                // Get target statements for this file
                const targets = mappingRules[file.name] || [];
                
                // Animate connections to each target
                for (const targetName of targets) {
                    const statementIndex = targetStatements.findIndex(s => s.name === targetName);
                    const statementEl = document.getElementById(`statement-${statementIndex}`);
                    
                    // Animate connection
                    await animateConnection(i, targetName);
                    
                    // Highlight statement
                    statementEl.classList.add('active');
                    
                    // Update confidence
                    const confidence = Math.floor(Math.random() * 15) + 85;
                    const fillEl = statementEl.querySelector('.confidence-fill');
                    fillEl.style.width = `${confidence}%`;
                    
                    await sleep(animationSpeed / 4);
                    
                    statementEl.classList.remove('active');
                }
                
                // Remove badge and deactivate file
                await sleep(animationSpeed / 2);
                badge.remove();
                fileEl.classList.remove('active');
                
                // Update accuracy
                const accuracy = Math.min(95, 75 + (i / sourceFiles.length) * 20);
                document.getElementById('accuracy').textContent = `${Math.floor(accuracy)}%`;
            }
            
            // Final stats
            const endTime = Date.now();
            const totalTime = ((endTime - startTime) / 1000).toFixed(1);
            document.getElementById('processingTime').textContent = `${totalTime}s`;
            
            isAnimating = false;
            
            // Keep animating the connections
            animateLoop();
        }

        function animateConnection(fileIndex, statementName) {
            return new Promise(resolve => {
                let progress = 0;
                const interval = setInterval(() => {
                    progress += 0.05;
                    
                    const canvas = document.getElementById('connectorCanvas');
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    
                    // Redraw all previous connections
                    for (let i = 0; i < fileIndex; i++) {
                        const file = sourceFiles[i];
                        const targets = mappingRules[file.name] || [];
                        targets.forEach(target => drawConnection(i, target, 1, false));
                    }
                    
                    // Draw current connection
                    drawConnection(fileIndex, statementName, progress, true);
                    
                    if (progress >= 1) {
                        clearInterval(interval);
                        resolve();
                    }
                }, 20);
            });
        }

        function animateLoop() {
            const canvas = document.getElementById('connectorCanvas');
            const ctx = canvas.getContext('2d');
            
            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Draw all connections with animated particles
                sourceFiles.forEach((file, i) => {
                    const targets = mappingRules[file.name] || [];
                    targets.forEach(target => drawConnection(i, target, 1, true));
                });
                
                requestAnimationFrame(draw);
            }
            
            draw();
        }

        function resetMapping() {
            const canvas = document.getElementById('connectorCanvas');
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Reset all elements
            document.querySelectorAll('.file-item, .statement-item').forEach(el => {
                el.classList.remove('active');
            });
            
            document.querySelectorAll('.processing-badge').forEach(badge => badge.remove());
            
            document.querySelectorAll('.confidence-fill').forEach(fill => {
                fill.style.width = '0%';
            });
            
            // Reset stats
            document.getElementById('filesProcessed').textContent = '0';
            document.getElementById('dataPoints').textContent = '0';
            document.getElementById('accuracy').textContent = '0%';
            document.getElementById('processingTime').textContent = '0s';
            
            isAnimating = false;
            currentFileIndex = 0;
        }

        function toggleSpeed() {
            const speeds = [1500, 1000, 500, 250];
            const labels = ['Slow', 'Normal', 'Fast', 'Ultra'];
            const currentIndex = speeds.indexOf(animationSpeed);
            const nextIndex = (currentIndex + 1) % speeds.length;
            
            animationSpeed = speeds[nextIndex];
            document.getElementById('speedLabel').textContent = labels[nextIndex];
        }

        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        // Handle window resize
        window.addEventListener('resize', () => {
            setupCanvas();
            if (!isAnimating) {
                const canvas = document.getElementById('connectorCanvas');
                const ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        });

        // Initialize on load
        init();
    </script>
</body>
</html>