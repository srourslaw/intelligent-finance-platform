1. File Structure Data (The Complete Tree)
const fileStructure = [
    { 
        folder: '01_LAND_PURCHASE', 
        files: ['Land_Contract_FINAL_v3.pdf', 'Land_Costs.xlsx', 'Legal_Fees_Invoice.pdf', 
                'Soil_Test_Report.pdf', 'Survey_Report_Aug2024.pdf', 'Title_Deed.pdf']
    },
    { 
        folder: '02_PERMITS_APPROVALS', 
        files: ['Building_Permit_Application.pdf', 'Building_Permit_APPROVED.pdf', 
                'Council_Fees_Receipt.pdf', 'Development_Approval.pdf', 'Energy_Rating_Certificate.pdf']
    },
    // ... 21 folders total with 82 files
];

let totalFiles = 0;
fileStructure.forEach(f => totalFiles += f.files.length);  // Counts all files = 82
2. Rendering the Sidebar (Building the Tree)
function renderInputs() {
    const list = document.getElementById('inputList');
    let fileIndex = 0;  // Global file counter
    
    fileStructure.forEach((group, groupIdx) => {
        // Create folder container
        const folderDiv = document.createElement('div');
        folderDiv.className = 'folder-group';
        
        // Create folder header
        const header = document.createElement('div');
        header.className = 'folder-header';
        header.id = `folder-${groupIdx}`;
        header.innerHTML = `📁 ${group.folder}`;
        
        // Create files container
        const filesContainer = document.createElement('div');
        filesContainer.className = 'folder-files';
        
        // Add each file
        group.files.forEach((file, fileIdx) => {
            const fileDiv = document.createElement('div');
            fileDiv.className = 'file-item';
            fileDiv.id = `file-${fileIndex}`;  // Unique ID for each file
            fileDiv.textContent = `📄 ${file}`;
            filesContainer.appendChild(fileDiv);
            fileIndex++;  // Increment global counter
        });
        
        folderDiv.appendChild(header);
        folderDiv.appendChild(filesContainer);
        list.appendChild(folderDiv);
    });
}
3. Processing Files (Animation Logic)
async function startAnimation() {
    let processedFiles = 0;
    
    // Loop through each folder
    for (let folderIdx = 0; folderIdx < fileStructure.length; folderIdx++) {
        const folder = fileStructure[folderIdx];
        const folderEl = document.getElementById(`folder-${folderIdx}`);
        folderEl.classList.add('active');  // Highlight folder
        
        // Loop through each file in folder
        for (let fileIdx = 0; fileIdx < folder.files.length; fileIdx++) {
            const globalFileIdx = processedFiles;
            const fileEl = document.getElementById(`file-${globalFileIdx}`);
            fileEl.classList.add('active');  // Highlight file
            
            // Create particles from this file
            const nodeIdx = globalFileIdx % nodesPerLayer;
            for (let p = 0; p < 3; p++) {
                setTimeout(() => {
                    particles.push(createParticle(`file-${globalFileIdx}`, `node-1-${nodeIdx}`, '#3b82f6'));
                }, p * 50);
            }
            
            // ... process through network ...
            
            // Update counter
            processedFiles++;
            document.getElementById('fileCounter').textContent = `${processedFiles}/${totalFiles}`;
            
            await sleep(speed / 8);  // Wait before next file
        }
        
        folderEl.classList.remove('active');  // Deactivate folder
    }
}
4. Connecting Files to Network
function drawAllConnections() {
    // Draw lines from each file to neural network
    let fileIdx = 0;
    fileStructure.forEach(group => {
        group.files.forEach(file => {
            const nodeIdx = fileIdx % nodesPerLayer;  // Distribute across 12 nodes
            const filePos = getPosition(`file-${fileIdx}`);
            if (filePos) {
                drawCurve(filePos, getPosition(`node-1-${nodeIdx}`), '#3b82f6', 0.15, 1);
            }
            fileIdx++;
        });
    });
    // ... rest of connections ...
}
5. CSS for 3D Effect
.input-section {
    perspective: 1000px;  /* Enables 3D space */
    transform-style: preserve-3d;
}

.file-item.active {
    transform: translateZ(15px) translateX(5px) scale(1.05);  /* Pop out effect */
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
}
Key Logic Summary:

Data Structure: 21 folders → 82 files stored in fileStructure array
Rendering: Nested loops create folder headers + file items with unique IDs
Animation: Outer loop = folders, Inner loop = files, each file creates 3 particles
Connection: Each file connects to Input Layer node based on fileIdx % 12
Counter: processedFiles tracks progress → updates ${processedFiles}/${totalFiles}
3D Effect: CSS translateZ() makes active files "lift" from background