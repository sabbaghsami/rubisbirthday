// Canvas setup
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Constants
const COLORS = [
    '#FF0000', '#FFA500', '#FFFF00', '#00FF00',
    '#00BFFF', '#8A2BE2', '#FF1493', '#FFD700'
];

// Audio
const bgMusic = document.getElementById('bgMusic');
let musicStarted = false;

// Particle class for firework explosions
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 7 + 1;
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.lifetime = 255;
        this.gravity = 0.15;
        this.size = Math.random() * 3 + 2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += this.gravity;
        this.lifetime -= 3;
    }

    draw() {
        if (this.lifetime > 0) {
            ctx.save();
            ctx.globalAlpha = this.lifetime / 255;
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }

    isAlive() {
        return this.lifetime > 0;
    }
}

// Firework class
class Firework {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.targetY = Math.random() * 150 + 80; // Higher explosions
        this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
        this.vy = -(Math.random() * 6 + 10); // Faster launch for higher altitude
        this.exploded = false;
        this.particles = [];
    }

    update() {
        if (!this.exploded) {
            this.y += this.vy;
            this.vy += 0.3;
            if (this.y <= this.targetY || this.vy > 0) {
                this.explode();
            }
        } else {
            this.particles = this.particles.filter(p => {
                p.update();
                return p.isAlive();
            });
        }
    }

    explode() {
        this.exploded = true;
        const numParticles = Math.floor(Math.random() * 50) + 50;
        for (let i = 0; i < numParticles; i++) {
            this.particles.push(new Particle(this.x, this.y, this.color));
        }
    }

    draw() {
        if (!this.exploded) {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, 4, 0, Math.PI * 2);
            ctx.fill();
        } else {
            this.particles.forEach(p => p.draw());
        }
    }

    isAlive() {
        return !this.exploded || this.particles.length > 0;
    }
}

// Birthday Cake class
class BirthdayCake {
    constructor(x, y, scale = 1.0) {
        this.x = x;
        this.y = y;
        this.scale = scale;
        this.flameOffset = 0;
        this.flameDirection = 1;
        this.sparkleTimer = 0;
    }

    update() {
        this.flameOffset += 0.2 * this.flameDirection;
        if (Math.abs(this.flameOffset) > 3) {
            this.flameDirection *= -1;
        }
        this.sparkleTimer++;
    }

    draw() {
        const w = 140 * this.scale;
        const layer1H = 45 * this.scale;
        const layer2H = 40 * this.scale;
        const layer3H = 35 * this.scale;

        // Plate
        ctx.fillStyle = '#969696';
        ctx.beginPath();
        ctx.ellipse(this.x, this.y - 8, w/2 + 18, 14, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#DCDCDC';
        ctx.beginPath();
        ctx.ellipse(this.x, this.y - 10, w/2 + 15, 12.5, 0, 0, Math.PI * 2);
        ctx.fill();

        // Bottom layer
        ctx.fillStyle = '#654321';
        ctx.fillRect(this.x - w/2, this.y - layer1H, w, layer1H);

        // Frosting bottom
        ctx.fillStyle = '#FFB6C1';
        ctx.beginPath();
        ctx.moveTo(this.x - w/2, this.y - layer1H - 8);
        for (let i = 0; i <= 12; i++) {
            const xPos = this.x - w/2 + (w * i / 12);
            const yPos = this.y - layer1H + 5 * Math.sin(i * 2);
            ctx.lineTo(xPos, yPos);
        }
        ctx.lineTo(this.x + w/2, this.y - layer1H - 8);
        ctx.closePath();
        ctx.fill();

        // Middle layer
        const w2 = w * 0.75;
        const layer2Y = this.y - layer1H;
        ctx.fillStyle = '#8B5A2B';
        ctx.fillRect(this.x - w2/2, layer2Y - layer2H, w2, layer2H);

        ctx.fillStyle = '#FFC0CB';
        ctx.beginPath();
        ctx.moveTo(this.x - w2/2, layer2Y - layer2H - 8);
        for (let i = 0; i <= 12; i++) {
            const xPos = this.x - w2/2 + (w2 * i / 12);
            const yPos = layer2Y - layer2H + 4 * Math.sin(i * 2);
            ctx.lineTo(xPos, yPos);
        }
        ctx.lineTo(this.x + w2/2, layer2Y - layer2H - 8);
        ctx.closePath();
        ctx.fill();

        // Top layer
        const w3 = w * 0.5;
        const layer3Y = layer2Y - layer2H;
        ctx.fillStyle = '#A06432';
        ctx.fillRect(this.x - w3/2, layer3Y - layer3H, w3, layer3H);

        ctx.fillStyle = '#FFC8DC';
        ctx.beginPath();
        ctx.moveTo(this.x - w3/2, layer3Y - layer3H - 8);
        for (let i = 0; i <= 8; i++) {
            const xPos = this.x - w3/2 + (w3 * i / 8);
            const yPos = layer3Y - layer3H + 3 * Math.sin(i * 2.5);
            ctx.lineTo(xPos, yPos);
        }
        ctx.lineTo(this.x + w3/2, layer3Y - layer3H - 8);
        ctx.closePath();
        ctx.fill();

        // Candles
        const numCandles = 7;
        const candleSpacing = w3 / (numCandles + 1);
        const candleColors = ['#FFB6C1', '#ADD8E6', '#FFFFC8', '#FFC8C8', '#C8FFC8'];

        for (let i = 0; i < numCandles; i++) {
            const candleX = this.x - w3/2 + candleSpacing * (i + 1);
            const candleY = layer3Y - layer3H - 5;
            const candleColor = candleColors[i % candleColors.length];

            // Candle body
            ctx.fillStyle = candleColor;
            ctx.fillRect(candleX - 4, candleY, 8, 30);

            // Candle shine
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            ctx.fillRect(candleX - 3, candleY + 2, 2, 26);

            // Wick
            ctx.fillStyle = '#323232';
            ctx.fillRect(candleX - 1, candleY - 5, 2, 5);

            // Flame
            const flameY = candleY + this.flameOffset;

            // Glow
            ctx.save();
            ctx.globalAlpha = 0.3;
            ctx.fillStyle = '#FFC800';
            ctx.beginPath();
            ctx.arc(candleX, flameY - 13, 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Flame shape
            ctx.fillStyle = '#FFC800';
            ctx.beginPath();
            ctx.moveTo(candleX, flameY - 18);
            ctx.lineTo(candleX - 4, flameY - 10);
            ctx.lineTo(candleX - 3, flameY - 6);
            ctx.lineTo(candleX, flameY - 8);
            ctx.lineTo(candleX + 3, flameY - 6);
            ctx.lineTo(candleX + 4, flameY - 10);
            ctx.closePath();
            ctx.fill();

            // Inner flame
            ctx.fillStyle = '#FFFF64';
            ctx.beginPath();
            ctx.moveTo(candleX, flameY - 16);
            ctx.lineTo(candleX - 2, flameY - 10);
            ctx.lineTo(candleX, flameY - 9);
            ctx.lineTo(candleX + 2, flameY - 10);
            ctx.closePath();
            ctx.fill();
        }
    }
}

// Image popup class
class ImagePopup {
    constructor(image) {
        this.image = image;
        this.size = Math.random() * 250 + 350; // Bigger: 350-600px instead of 200-400px

        const aspect = image.width / image.height;
        if (aspect > 1) {
            this.width = this.size;
            this.height = this.size / aspect;
        } else {
            this.height = this.size;
            this.width = this.size * aspect;
        }

        this.x = Math.random() * (canvas.width - this.width - 200) + 100;
        this.y = Math.random() * (canvas.height - this.height - 200) + 100;

        this.lifetime = 180;
        this.maxLifetime = 180;
        this.scale = 0.1;
        this.rotation = 0;
        this.rotationSpeed = (Math.random() - 0.5) * 1.5; // Slower rotation: 1.5 instead of 4
    }

    update() {
        this.lifetime--;
        if (this.scale < 1.0) {
            this.scale += 0.05;
        }
        this.rotation += this.rotationSpeed;
    }

    draw() {
        if (this.lifetime <= 0) return;

        const alpha = this.lifetime < 30 ? this.lifetime / 30 : 1;

        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.translate(this.x + this.width/2, this.y + this.height/2);
        ctx.rotate(this.rotation * Math.PI / 180);
        ctx.scale(this.scale, this.scale);

        // Glow
        ctx.shadowBlur = 20;
        ctx.shadowColor = 'rgba(255, 255, 255, 0.5)';

        ctx.drawImage(this.image, -this.width/2, -this.height/2, this.width, this.height);
        ctx.restore();
    }

    isAlive() {
        return this.lifetime > 0;
    }
}

// Game state
const fireworks = [];
const cakes = [
    new BirthdayCake(canvas.width * 0.25, canvas.height - 150, 1.2),
    new BirthdayCake(canvas.width * 0.75, canvas.height - 150, 1.2)
];

let fireworkTimer = 0;
let fireworkCount = 0;
let imagePopup = null;
let specialImages = [];
let imagesLoaded = 0;
let currentImageIndex = 0; // Track which image to show next

// List of all image files
const imageFiles = [
    '1000028077.jpg',
    'Screenshot_20251110_205756_Snapchat.jpg',
    'Snapchat-1925726483.jpg',
    'Snapchat-517622066.jpg',
    'Snapchat-872040690.jpg'
];

// Load all images
imageFiles.forEach((filename, index) => {
    const img = new Image();
    img.src = filename;
    img.onload = () => {
        specialImages.push(img);
        imagesLoaded++;
        console.log(`Loaded image ${imagesLoaded}/${imageFiles.length}: ${filename}`);
    };
    img.onerror = () => {
        console.error(`Failed to load image: ${filename}`);
    };
});

// Draw background
function drawBackground() {
    // Night sky gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, '#0A0A14');
    gradient.addColorStop(1, '#1E1E3C');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Stars
    ctx.fillStyle = '#FFFFFF';
    for (let i = 0; i < 100; i++) {
        const x = (i * 137.508) % canvas.width; // Pseudo-random but consistent
        const y = (i * 73.219) % (canvas.height / 2);
        const size = (i % 2) + 1;
        ctx.fillRect(x, y, size, size);
    }
}

// Draw text
function drawText() {
    // Title with glow
    ctx.save();
    ctx.shadowBlur = 20;
    ctx.shadowColor = 'rgba(255, 215, 0, 0.8)';
    ctx.fillStyle = '#FFD700';
    ctx.font = 'bold 80px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Happy 22nd Birthday!', canvas.width / 2, 100);
    ctx.restore();

    // Name
    ctx.fillStyle = '#FF69B4';
    ctx.font = 'bold 50px Arial';
    ctx.fillText('RUBI', canvas.width / 2, 170);
}

// Auto-launch fireworks
function autoLaunchFirework() {
    fireworkTimer++;
    if (fireworkTimer >= 15) {
        fireworkTimer = 0;
        const x = Math.random() * (canvas.width - 200) + 100;
        fireworks.push(new Firework(x, canvas.height));
        fireworkCount++;

        // Show image every 15 fireworks
        if (fireworkCount % 15 === 0 && specialImages.length > 0) {
            // Show images in order
            imagePopup = new ImagePopup(specialImages[currentImageIndex]);
            console.log(`Image popup triggered! (Firework #${fireworkCount}) - Image ${currentImageIndex + 1}/${specialImages.length}`);

            // Move to next image, loop back to start when we reach the end
            currentImageIndex = (currentImageIndex + 1) % specialImages.length;
        }
    }
}

// Animation loop
function animate() {
    // Clear and draw background
    drawBackground();

    // Auto-launch fireworks
    autoLaunchFirework();

    // Update and draw fireworks
    for (let i = fireworks.length - 1; i >= 0; i--) {
        fireworks[i].update();
        fireworks[i].draw();
        if (!fireworks[i].isAlive()) {
            fireworks.splice(i, 1);
        }
    }

    // Update and draw cakes
    cakes.forEach(cake => {
        cake.update();
        cake.draw();
    });

    // Draw text
    drawText();

    // Update and draw image popup
    if (imagePopup) {
        imagePopup.update();
        imagePopup.draw();
        if (!imagePopup.isAlive()) {
            imagePopup = null;
        }
    }

    requestAnimationFrame(animate);
}

// Event listeners
canvas.addEventListener('click', (e) => {
    fireworks.push(new Firework(e.clientX, canvas.height));

    // Start music on first interaction
    if (!musicStarted) {
        bgMusic.play().catch(err => console.log('Music autoplay blocked'));
        musicStarted = true;
    }
});

window.addEventListener('keydown', (e) => {
    if (e.key === ' ') {
        const x = Math.random() * (canvas.width - 200) + 100;
        fireworks.push(new Firework(x, canvas.height));
    } else if (e.key === 'm' || e.key === 'M') {
        if (bgMusic.paused) {
            bgMusic.play();
        } else {
            bgMusic.pause();
        }
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Reposition cakes
    cakes[0].x = canvas.width * 0.25;
    cakes[0].y = canvas.height - 150;
    cakes[1].x = canvas.width * 0.75;
    cakes[1].y = canvas.height - 150;
});

// Start animation
animate();
