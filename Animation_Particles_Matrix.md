1. Particle Creation & Speed
function createParticle(startId, endId, color) {
    return {
        start: startId,
        end: endId,
        progress: 0,
        speed: 0.025,  // Controls how fast dots move (higher = faster)
        color,
        active: true
    };
}
2. Particle Animation (Bezier Curve Movement)
function updateParticle(p) {
    p.progress += p.speed;
    if (p.progress >= 1) {
        p.active = false;
        return null;
    }

    const start = getPosition(p.start);
    const end = getPosition(p.end);
    if (!start || !end) return null;

    const t = p.progress;
    const dx = end.x - start.x;
    const cp1x = start.x + dx * 0.3;  // Control point 1
    const cp2x = start.x + dx * 0.7;  // Control point 2

    // Bezier curve calculation
    const x = Math.pow(1-t, 3) * start.x + 
             3 * Math.pow(1-t, 2) * t * cp1x + 
             3 * (1-t) * t * t * cp2x + 
             Math.pow(t, 3) * end.x;
    const y = Math.pow(1-t, 3) * start.y + 
             3 * Math.pow(1-t, 2) * t * start.y + 
             3 * (1-t) * t * t * end.y + 
             Math.pow(t, 3) * end.y;

    return { x, y };
}3. Matrix Cell Activation (Random Squares Light Up)
// Layer 2 to Matrix - Random cells activate
const cellsToActivate = [];
for (let j = 0; j < 5; j++) {  // Activate 5 random cells
    const randomCellIdx = Math.floor(Math.random() * (matrixSize * matrixSize));
    cellsToActivate.push(randomCellIdx);
}

cellsToActivate.forEach((cellIdx, idx) => {
    const cell = document.getElementById(`cell-${cellIdx}`);
    cell.classList.add('active');  // Lights up the square
    setTimeout(() => {
        particles.push(createParticle(`node-2-${node2Idx}`, `cell-${cellIdx}`, '#a78bfa'));
        particles.push(createParticle(`node-2-${node2Idx}`, `cell-${cellIdx}`, '#a78bfa'));
    }, idx * 30);  // Stagger the particles
});
4. Drawing Particles on Canvas
function drawParticle(p) {
    const pos = updateParticle(p);
    if (!pos) return;

    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 5, 0, Math.PI * 2);  // 5 = particle size
    
    const gradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, 5);
    gradient.addColorStop(0, p.color);
    gradient.addColorStop(1, p.color + '00');
    
    ctx.fillStyle = gradient;
    ctx.shadowBlur = 20;  // Glow effect
    ctx.shadowColor = p.color;
    ctx.fill();
    ctx.shadowBlur = 0;
}
5. Animation Loop
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawAllConnections();  // Draw lines
    
    particles = particles.filter(p => p.active);  // Remove dead particles
    particles.forEach(p => drawParticle(p));  // Draw each particle
    
    requestAnimationFrame(animate);  // 60fps loop
}
Key Points for Claude Code Max:

speed: 0.025 controls particle velocity
Math.floor(Math.random() * 100) picks random matrix cells
Particles die when progress >= 1
Bezier curves create smooth curved paths
requestAnimationFrame runs at 60fps
Multiple particles created with setTimeout stagger for parallel effect