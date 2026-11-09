
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kuvempunagar Bus Run</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: #080d19;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

.game {
    width: 100%;
    height: 100vh;
    position: relative;
    overflow: hidden;
    background: #17243b;
}

canvas {
    width: 100%;
    height: 100%;
    display: block;
}

.header {
    position: absolute;
    top: 20px;
    left: 4%;
    right: 4%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 5;
}

.logo {
    font-size: 23px;
    font-weight: 900;
    letter-spacing: 3px;
}

.logo span {
    color: #ffb34f;
}

.dashboard {
    display: flex;
    gap: 10px;
}

.info {
    background: #08111ddd;
    border: 1px solid #ffffff33;
    padding: 12px 18px;
    border-radius: 12px;
    font-size: 12px;
    letter-spacing: 1px;
}

.info span {
    display: block;
    color: #ffb34f;
    font-size: 19px;
    font-weight: bold;
    margin-top: 5px;
}

.route {
    position: absolute;
    top: 100px;
    left: 4%;
    right: 4%;
    z-index: 5;
    background: #08111dcc;
    border: 1px solid #ffffff33;
    padding: 14px 20px;
    border-radius: 12px;
}

.route-line {
    height: 5px;
    background: #ffffff33;
    margin-top: 12px;
    border-radius: 10px;
    overflow: hidden;
}

.route-progress {
    width: 0%;
    height: 100%;
    background: #ffb34f;
}

.overlay {
    position: absolute;
    inset: 0;
    background: #030817bb;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
    text-align: center;
}

.panel {
    width: min(90%, 470px);
    padding: 38px;
    border-radius: 22px;
    background: #101a2deF;
    border: 1px solid #ffffff33;
    box-shadow: 0 20px 80px #0009;
    backdrop-filter: blur(15px);
}

.panel h1 {
    font-size: 38px;
    letter-spacing: 3px;
    margin-bottom: 15px;
}

.panel h1 span {
    color: #ffb34f;
}

.panel p {
    color: #c6d0e0;
    line-height: 1.8;
    margin-bottom: 20px;
}

button {
    padding: 15px 35px;
    border: none;
    border-radius: 30px;
    background: linear-gradient(120deg,#ffb34f,#ff573d);
    color: white;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
}

button:hover {
    transform: scale(1.05);
}

.hidden {
    display: none;
}

.controls {
    position: absolute;
    bottom: 22px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    gap: 12px;
    z-index: 6;
}

.controls button {
    width: 55px;
    height: 55px;
    padding: 0;
    background: #08111ddd;
    border: 1px solid #ffffff66;
    font-size: 22px;
    touch-action: none;
}

@media(max-width: 650px) {
    .logo { font-size: 15px; }
    .info { padding: 8px; font-size: 9px; }
    .info span { font-size: 14px; }
    .route { top: 75px; font-size: 12px; }
    .panel h1 { font-size: 28px; }
    .panel { padding: 25px; }
}
</style>
</head>

<body>

<div class="game">

    <div class="header">
        <div class="logo">BENGALURU <span>BUS RUN</span></div>

        <div class="dashboard">
            <div class="info">
                SPEED
                <span id="speed">0</span>
            </div>

            <div class="info">
                SCORE
                <span id="score">0</span>
            </div>

            <div class="info">
                TICKETS
                <span id="tickets">0</span>
            </div>
        </div>
    </div>

    <div class="route">
        <div style="display:flex;justify-content:space-between">
            <b>📍 ITPL</b>
            <b id="destination">KUVEMPUNAGAR</b>
        </div>

        <div class="route-line">
            <div class="route-progress" id="progress"></div>
        </div>

        <p id="stopName" style="margin-top:8px;color:#ffb34f">
            Starting point: ITPL Bus Stop
        </p>
    </div>

    <canvas id="gameCanvas"></canvas>

    <div class="overlay" id="startScreen">
        <div class="panel">
            <h1>BENGALURU <span>BUS RUN</span></h1>

            <p>
                YOUR JOURNEY BEGINS AT ITPL.<br>
                DRIVE THROUGH THE CITY.<br>
                REACH KUVEMPUNAGAR BUS STATION.
            </p>

            <p>
                ↑ ACCELERATE<br>
                ↓ BRAKE<br>
                ← → STEER<br>
                SPACE = HORN
            </p>

            <button onclick="startGame()">START JOURNEY</button>
        </div>
    </div>

    <div class="overlay hidden" id="gameOver">
        <div class="panel">
            <h1>JOURNEY <span>ENDED</span></h1>
            <p>You had an accident!</p>
            <p>FINAL SCORE: <b id="finalScore">0</b></p>
            <button onclick="startGame()">TRY AGAIN</button>
        </div>
    </div>

    <div class="overlay hidden" id="winScreen">
        <div class="panel">
            <h1>MISSION <span>COMPLETED!</span></h1>
            <p>You successfully reached Kuvempunagar Bus Station.</p>
            <p>FINAL SCORE: <b id="winScore">0</b></p>
            <button onclick="startGame()">DRIVE AGAIN</button>
        </div>
    </div>

    <div class="controls">
        <button id="leftBtn">←</button>
        <button id="brakeBtn">↓</button>
        <button id="accelerateBtn">↑</button>
        <button id="rightBtn">→</button>
    </div>

</div>

<script>

// ===================================
// 1. CANVAS SETUP
// ===================================

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let W, H, roadTop, roadBottom;

function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;

    roadTop = H * 0.25;
    roadBottom = H * 0.92;

    bus.y = H * 0.70;
}

window.addEventListener("resize", resize);


// ===================================
// 2. GAME VARIABLES
// ===================================

let running = false;
let score = 0;
let tickets = 0;
let distance = 0;
let speed = 0;
let frame = 0;
let roadMove = 0;

const destinationDistance = 5000;

let obstacles = [];
let coins = [];

let keys = {
    left: false,
    right: false,
    up: false,
    down: false
};


// ===================================
// 3. BUS OBJECT
// ===================================

const bus = {
    x: 0,
    y: 0,
    width: 85,
    height: 125,
    targetX: 0
};


// ===================================
// 4. BUS POSITION
// ===================================

function resetBus() {
    bus.x = W / 2;
    bus.targetX = W / 2;
    bus.y = H * 0.70;
}


// ===================================
// 5. KEYBOARD CONTROLS
// ===================================

document.addEventListener("keydown", e => {

    if (["ArrowUp", "ArrowDown", "ArrowLeft",
         "ArrowRight", "Space"].includes(e.code)) {
        e.preventDefault();
    }

    if (e.code === "ArrowLeft") keys.left = true;
    if (e.code === "ArrowRight") keys.right = true;
    if (e.code === "ArrowUp") keys.up = true;
    if (e.code === "ArrowDown") keys.down = true;

    if (e.code === "Space" && running) {
        playHorn();
    }
});

document.addEventListener("keyup", e => {

    if (e.code === "ArrowLeft") keys.left = false;
    if (e.code === "ArrowRight") keys.right = false;
    if (e.code === "ArrowUp") keys.up = false;
    if (e.code === "ArrowDown") keys.down = false;

});


// ===================================
// 6. MOBILE CONTROLS
// ===================================

function bindButton(id, key) {

    const button = document.getElementById(id);

    button.addEventListener("pointerdown", e => {
        e.preventDefault();
        keys[key] = true;
    });

    button.addEventListener("pointerup", () => {
        keys[key] = false;
    });

    button.addEventListener("pointerleave", () => {
        keys[key] = false;
    });

    button.addEventListener("pointercancel", () => {
        keys[key] = false;
    });
}

bindButton("leftBtn", "left");
bindButton("rightBtn", "right");
bindButton("accelerateBtn", "up");
bindButton("brakeBtn", "down");


// ===================================
// 7. HORN SOUND
// ===================================

let audioContext;

function playHorn() {
    try {
        audioContext = audioContext ||
            new AudioContext();

        const oscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();

        oscillator.connect(gain);
        gain.connect(audioContext.destination);

        oscillator.type = "sawtooth";
        oscillator.frequency.value = 350;

        gain.gain.setValueAtTime(
            0.08, audioContext.currentTime
        );

        gain.gain.exponentialRampToValueAtTime(
            0.001, audioContext.currentTime + 0.3
        );

        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.3);

    } catch (error) {
        console.log("Audio unavailable");
    }
}


// ===================================
// 8. DRAW SKY AND CITY
// ===================================

function drawBackground() {

    let sky = ctx.createLinearGradient(0, 0, 0, H);

    sky.addColorStop(0, "#101e3a");
    sky.addColorStop(0.45, "#9c5969");
    sky.addColorStop(1, "#f3a45c");

    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    // Sun

    ctx.beginPath();

    ctx.arc(
        W * 0.75,
        H * 0.27,
        48,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#ffcc83";
    ctx.shadowBlur = 45;
    ctx.shadowColor = "#ff8b42";
    ctx.fill();

    ctx.shadowBlur = 0;

    // City buildings

    const buildingColors = [
        "#263448",
        "#344359",
        "#202d43",
        "#41465c"
    ];

    for (let i = 0; i < 14; i++) {

        let x = i * W / 13;
        let bh = 70 + (i * 37 % 100);

        ctx.fillStyle =
            buildingColors[i % buildingColors.length];

        ctx.fillRect(
            x,
            roadTop - bh,
            65,
            bh
        );

        // Building windows

        ctx.fillStyle = "#ffc77788";

        for (let wx = x + 10; wx < x + 55; wx += 17) {
            for (let wy = roadTop - bh + 12;
                 wy < roadTop - 10; wy += 22) {

                ctx.fillRect(wx, wy, 6, 8);
            }
        }
    }

    // Road surroundings

    ctx.fillStyle = "#24302d";
    ctx.fillRect(0, roadTop, W, H - roadTop);

    // Road

    const left = W * 0.16;
    const right = W * 0.84;

    ctx.fillStyle = "#242a35";
    ctx.fillRect(
        left,
        roadTop,
        right - left,
        H - roadTop
    );

    // Road edges

    ctx.fillStyle = "#ffb34f";

    ctx.fillRect(left, roadTop, 5, H - roadTop);
    ctx.fillRect(right - 5, roadTop, 5, H - roadTop);

    // Moving road lines

    ctx.fillStyle = "#f5f0d5";

    for (
        let y = roadTop + (roadMove % 90);
        y < H;
        y += 90
    ) {

        ctx.fillRect(W / 2 - 4, y, 8, 42);
    }

    // Side road trees

    for (let i = 0; i < 8; i++) {

        let y = roadTop + (i * 105 + roadMove) %
                (H - roadTop);

        drawTree(W * 0.08, y);
        drawTree(W * 0.92, y);
    }

}


// ===================================
// 9. DRAW TREES
// ===================================

function drawTree(x, y) {

    ctx.fillStyle = "#49392e";
    ctx.fillRect(x - 5, y, 10, 35);

    ctx.fillStyle = "#183e35";

    ctx.beginPath();
    ctx.arc(x, y - 8, 22, 0, Math.PI * 2);
    ctx.fill();

}


// ===================================
// 10. DRAW PLAYER BUS
// ===================================

function drawBus() {

    const x = bus.x;
    const y = bus.y;
    const w = bus.width;
    const h = bus.height;

    // Bus shadow

    ctx.fillStyle = "#0007";
    ctx.fillRect(x - w / 2 + 5, y + h - 5, w, 15);

    // Main body

    ctx.fillStyle = "#e5a91d";

    ctx.beginPath();

    ctx.roundRect(
        x - w / 2,
        y,
        w,
        h,
        12
    );

    ctx.fill();

    // Upper bus body

    ctx.fillStyle = "#f5c342";

    ctx.fillRect(
        x - w / 2 + 5,
        y + 8,
        w - 10,
        38
    );

    // Front windshield

    ctx.fillStyle = "#172c40";

    ctx.beginPath();

    ctx.roundRect(
        x - w / 2 + 10,
        y + 12,
        w - 20,
        31,
        5
    );

    ctx.fill();

    // Destination board

    ctx.fillStyle = "#17202c";
    ctx.fillRect(x - 25, y + 49, 50, 13);

    ctx.fillStyle = "#ffe6a2";
    ctx.font = "bold 8px Arial";
    ctx.textAlign = "center";

    ctx.fillText("KUVEMPUNAGAR", x, y + 58);

    // Body lower section

    ctx.fillStyle = "#e6aa21";

    ctx.fillRect(
        x - w / 2 + 5,
        y + 65,
        w - 10,
        42
    );

    // Wheels

    ctx.fillStyle = "#10141b";

    ctx.fillRect(x - w / 2 - 4, y + 25, 9, 24);
    ctx.fillRect(x + w / 2 - 5, y + 25, 9, 24);

    ctx.fillRect(x - w / 2 - 4, y + 83, 9, 24);
    ctx.fillRect(x + w / 2 - 5, y + 83, 9, 24);

    // Headlights

    ctx.fillStyle = "#fff1b5";
    ctx.shadowBlur = 18;
    ctx.shadowColor = "#fff0b0";

    ctx.fillRect(x - 31, y + 109, 14, 7);
    ctx.fillRect(x + 17, y + 109, 14, 7);

    ctx.shadowBlur = 0;

    // Front bumper

    ctx.fillStyle = "#c1c8d0";
    ctx.fillRect(x - 35, y + 119, 70, 5);

}


// ===================================
// 11. CREATE TRAFFIC
// ===================================

function createObstacle() {

    const types = ["car", "truck", "bike"];

    const type = types[
        Math.floor(Math.random() * types.length)
    ];

    const roadLeft = W * 0.20;
    const roadRight = W * 0.80;

    obstacles.push({

        x: roadLeft + 25 +
           Math.random() * (roadRight - roadLeft - 50),

        y: -150,

        width: type === "truck" ? 65 : 48,
        height: type === "truck" ? 110 : 85,

        type: type
    });

}


// ===================================
// 12. DRAW TRAFFIC
// ===================================

function drawObstacles() {

    obstacles.forEach(ob => {

        if (ob.type === "truck") {
            ctx.fillStyle = "#477d92";
        } else if (ob.type === "bike") {
            ctx.fillStyle = "#d94d3e";
        } else {
            ctx.fillStyle = "#4366a1";
        }

        ctx.beginPath();

        ctx.roundRect(
            ob.x - ob.width / 2,
            ob.y,
            ob.width,
            ob.height,
            8
        );

        ctx.fill();

        // Windows

        ctx.fillStyle = "#142c43";

        ctx.fillRect(
            ob.x - ob.width / 2 + 6,
            ob.y + 10,
            ob.width - 12,
            25
        );

        // Rear lights

        ctx.fillStyle = "#ff5144";

        ctx.fillRect(
            ob.x - ob.width / 2 + 5,
            ob.y + ob.height - 12,
            8,
            6
        );

        ctx.fillRect(
            ob.x + ob.width / 2 - 13,
            ob.y + ob.height - 12,
            8,
            6
        );

    });

}


// ===================================
// 13. CREATE TICKETS
// ===================================

function createCoin() {

    coins.push({

        x: W * 0.20 +
           Math.random() * W * 0.60,

        y: -30,

        radius: 12

    });

}


// ===================================
// 14. DRAW TICKETS
// ===================================

function drawCoins() {

    coins.forEach(coin => {

        ctx.beginPath();

        ctx.arc(
            coin.x,
            coin.y,
            coin.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#ffcb43";
        ctx.fill();

        ctx.strokeStyle = "#fff2a3";
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.fillStyle = "#47300a";
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "center";

        ctx.fillText("₹", coin.x, coin.y + 4);

    });

}


// ===================================
// 15. COLLISION DETECTION
// ===================================

function collision(a, b) {

    return (

        Math.abs(a.x - b.x) <
        (a.width + b.width) / 2 - 8

        &&

        Math.abs(a.y + a.height / 2 -
                 (b.y + b.height / 2)) <
        (a.height + b.height) / 2 - 12

    );

}


// ===================================
// 16. UPDATE GAME
// ===================================

function update() {

    if (!running) return;

    frame++;

    // Accelerate and brake

    if (keys.up) {
        speed += 0.12;
    }

    if (keys.down) {
        speed -= 0.20;
    }

    speed = Math.max(0, Math.min(speed, 12));

    // Move bus

    if (keys.left) {
        bus.targetX -= 5;
    }

    if (keys.right) {
        bus.targetX += 5;
    }

    bus.targetX = Math.max(
        W * 0.22,
        Math.min(W * 0.78, bus.targetX)
    );

    bus.x += (bus.targetX - bus.x) * 0.18;

    // Distance and score

    distance += speed * 0.15;

    score += Math.floor(speed * 0.1);

    roadMove += speed * 1.8;

    // Create traffic

    if (frame % 65 === 0) {
        createObstacle();
    }

    // Create tickets

    if (frame % 95 === 0) {
        createCoin();
    }

    // Move traffic

    obstacles.forEach(ob => {

        ob.y += speed * 1.5 + 2;

        if (collision(bus, ob)) {
            endGame();
        }

    });

    obstacles = obstacles.filter(
        ob => ob.y < H + 150
    );

    // Move tickets

    coins.forEach(coin => {

        coin.y += speed * 1.5 + 2;

        if (
            Math.abs(bus.x - coin.x) < 48 &&
            Math.abs(bus.y + 60 - coin.y) < 75
        ) {

            coin.collected = true;

            tickets++;
            score += 50;

        }

    });

    coins = coins.filter(
        coin => !coin.collected && coin.y < H + 30
    );

    // Update dashboard

    document.getElementById("score").textContent = score;

    document.getElementById("tickets").textContent = tickets;

    document.getElementById("speed").textContent =
        Math.round(speed * 10) + " km/h";

    // Route progress

    const progress = Math.min(
        100,
        distance / destinationDistance * 100
    );

    document.getElementById("progress").style.width =
        progress + "%";

    // Intermediate stops

    if (distance < 1600) {
        document.getElementById("stopName").textContent =
            "Next: Whitefield City Road";
    }
    else if (distance < 3200) {
        document.getElementById("stopName").textContent =
            "Next: Bengaluru City Bus Stop";
    }
    else {
        document.getElementById("stopName").textContent =
            "Next: Kuvempunagar Bus Station";
    }

    // Destination reached

    if (distance >= destinationDistance) {
        winGame();
    }

}


// ===================================
// 17. MAIN GAME LOOP
// ===================================

function loop() {

    drawBackground();

    if (running) {
        update();
    }

    drawObstacles();
    drawCoins();
    drawBus();

    if (running) {
        requestAnimationFrame(loop);
    }

}


// ===================================
// 18. START GAME
// ===================================

function startGame() {

    score = 0;
    tickets = 0;
    distance = 0;
    speed = 0;
    frame = 0;
    roadMove = 0;

    obstacles = [];
    coins = [];

    keys = {
        left: false,
        right: false,
        up: false,
        down: false
    };

    resetBus();

    running = true;

    document.getElementById("startScreen")
        .classList.add("hidden");

    document.getElementById("gameOver")
        .classList.add("hidden");

    document.getElementById("winScreen")
        .classList.add("hidden");

    loop();

}


// ===================================
// 19. GAME OVER
// ===================================

function endGame() {

    if (!running) return;

    running = false;

    document.getElementById("finalScore").textContent =
        score;

    document.getElementById("gameOver")
        .classList.remove("hidden");

}


// ===================================
// 20. MISSION COMPLETED
// ===================================

function winGame() {

    if (!running) return;

    running = false;

    document.getElementById("winScore").textContent =
        score;

    document.getElementById("winScreen")
        .classList.remove("hidden");

}


// ===================================
// 21. INITIAL GAME SCREEN
// ===================================

resize();
resetBus();

drawBackground();
drawBus();

</script>

</body>
</html>
"""


# ===================================
# FLASK BACKEND
# ===================================

@app.route("/")
def home():
    return render_template_string(HTML)


# ===================================
# RUN APPLICATION
# ===================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
