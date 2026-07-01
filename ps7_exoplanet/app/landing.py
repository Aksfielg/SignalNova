import streamlit as st

def render_landing():
    # --- STICKY HEADER ---
    st.markdown("""
        <style>
        /* Hide default Streamlit header */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        /* Make the main block relative so we can pad it */
        .block-container {
            padding-top: 100px !important; 
            padding-bottom: 0px !important;
        }
        
        /* 1. Float the visual header background and logo */
        .floating-header {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 60%;
            height: 40px;
            background: rgba(15, 20, 35, 0.7);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            z-index: 999998;
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.05);
            border-top: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            display: flex;
            align-items: center;
            padding: 0 25px;
        }
        .header-logo {
            font-family: 'Orbitron', monospace;
            font-size: 16px;
            font-weight: 900;
            color: #fff;
            letter-spacing: 4px;
            margin-top: 2px;
        }
        .header-logo span { color: #a78bfa; }
        
        /* 2. Float the Streamlit button */
        /* Use :has() to target the element-container immediately following the header */
        div.element-container:has(.floating-header) + div.element-container {
            position: fixed !important;
            top: 26px !important;
            right: calc(20% + 15px) !important;
            z-index: 999999 !important;
            width: auto !important;
            display: block !important;
        }
        
        div.element-container:has(.floating-header) + div.element-container button {
            background-color: #378ADD !important;
            color: white !important;
            border-radius: 30px !important;
            border: none !important;
            box-shadow: 0 0 15px rgba(55,138,221,0.4) !important;
            font-family: 'Orbitron', monospace !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            padding: 2px 14px !important;
            transition: all 0.3s ease !important;
            height: 28px !important;
            min-height: 28px !important;
            line-height: 1 !important;
            font-size: 11px !important;
        }
        div.element-container:has(.floating-header) + div.element-container button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 0 25px rgba(55,138,221,0.7) !important;
        }
        
        @media (max-width: 900px) {
            .floating-header { width: 90%; }
            div.element-container:has(.floating-header) + div.element-container { right: calc(5% + 15px) !important; }
        }
        </style>
        
        <div class="floating-header">
            <div class="header-logo">SIGNAL<span>NOVA</span></div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("SKIP INTRO ⏭", key="skip_intro"):
        st.session_state.show_dashboard = True
        st.rerun()

    # Split into parts to avoid triple-quote truncation issues
    part1 = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{background:#000;color:#fff;font-family:'Inter',sans-serif;overflow-x:hidden;}
section{min-height:650px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:60px 40px;position:relative;text-align:center;}

/* STARS */
#star-canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}

/* SECTION 1 - Hero */
.hero{background:radial-gradient(ellipse at center,#0a0a2e 0%,#000 70%);}
.hero-title{font-family:'Orbitron',monospace;font-size:clamp(48px,8vw,120px);
  font-weight:900;letter-spacing:8px;
  background:linear-gradient(135deg,#a8c5ff 0%,#7b9fff 40%,#a78bfa 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:24px;
  text-shadow:none;filter:drop-shadow(0 0 40px rgba(120,150,255,0.5));}
.hero-sub{font-size:20px;color:#a8c5e2;margin-bottom:12px;letter-spacing:1px;}
.hero-desc{font-size:14px;color:#4a6080;letter-spacing:2px;margin-bottom:50px;}
.hero-btn{
  background:linear-gradient(135deg,#667eea,#764ba2);
  border:none;border-radius:50px;padding:18px 50px;
  font-family:'Orbitron',monospace;font-size:14px;letter-spacing:3px;
  color:#fff;cursor:pointer;
  box-shadow:0 0 30px rgba(102,126,234,0.5);
  transition:all 0.3s ease;text-transform:uppercase;}
.hero-btn:hover{transform:scale(1.05);box-shadow:0 0 50px rgba(102,126,234,0.8);}

/* SECTION 2 - Transit */
.transit-section{background:linear-gradient(180deg,#000 0%,#050520 100%);}
.section-title{font-family:'Orbitron',monospace;font-size:clamp(28px,5vw,56px);
  font-weight:700;margin-bottom:24px;color:#fff;
  text-shadow:0 0 40px rgba(100,150,255,0.4);}
.section-desc{font-size:16px;color:#8899bb;max-width:700px;line-height:1.8;margin-bottom:50px;}

/* Light curve animation */
.lc-wrapper{width:min(800px,90vw);height:200px;position:relative;
  background:rgba(10,20,50,0.8);border:1px solid rgba(60,100,200,0.2);
  border-radius:16px;overflow:hidden;}
.lc-scan{position:absolute;top:0;height:100%;width:2px;
  background:rgba(255,255,255,0.8);
  box-shadow:0 0 10px #fff;
  animation:scan 4s linear infinite;}
@keyframes scan{from{left:0;}to{left:100%;}}
.lc-svg{width:100%;height:100%;}
.transit-point{animation:pulse-pt 2s ease-in-out infinite;}
@keyframes pulse-pt{0%,100%{r:4;opacity:1;}50%{r:7;opacity:0.6;}}

/* SECTION 3 - Imposters */
.imposters-section{background:linear-gradient(180deg,#050520 0%,#0a0010 100%);}
.cards-grid{display:flex;gap:24px;flex-wrap:wrap;justify-content:center;max-width:900px;}
.signal-card{width:260px;border-radius:20px;padding:28px;text-align:left;
  border:2px solid transparent;transition:transform 0.3s,box-shadow 0.3s;}
.signal-card:hover{transform:translateY(-8px);}
.card-planet{background:rgba(0,50,20,0.6);border-color:#00ff88;
  box-shadow:0 0 30px rgba(0,255,136,0.1);}
.card-eb{background:rgba(50,30,0,0.6);border-color:#ff8800;
  box-shadow:0 0 30px rgba(255,136,0,0.1);}
.card-noise{background:rgba(20,20,40,0.6);border-color:#4466ff;
  box-shadow:0 0 30px rgba(68,102,255,0.1);}
.card-icon{font-size:32px;margin-bottom:12px;}
.card-title{font-family:'Orbitron',monospace;font-size:16px;font-weight:700;
  margin-bottom:10px;}
.card-planet .card-title{color:#00ff88;}
.card-eb .card-title{color:#ff8800;}
.card-noise .card-title{color:#7788ff;}
.card-body{font-size:13px;color:#8899bb;line-height:1.6;}

/* SECTION 4 - Pipeline */
.pipeline-section{background:linear-gradient(180deg,#0a0010 0%,#000 100%);}
.pipeline-nodes{display:flex;align-items:center;gap:0;flex-wrap:wrap;
  justify-content:center;max-width:900px;margin-top:20px;}
.p-node{display:flex;flex-direction:column;align-items:center;width:140px;}
.p-circle{width:90px;height:90px;border-radius:50%;
  border:2px solid #a78bfa;
  display:flex;align-items:center;justify-content:center;
  font-size:32px;margin-bottom:12px;position:relative;
  background:rgba(20,10,40,0.8);
  box-shadow:0 0 20px rgba(167,139,250,0.2);
  transition:box-shadow 0.3s;}
.p-circle.active{border-color:#00ff88;box-shadow:0 0 30px rgba(0,255,136,0.5);}
.p-label{font-size:11px;color:#a8c5e2;text-align:center;letter-spacing:0.5px;
  font-family:'Orbitron',monospace;}
.p-connector{width:40px;height:2px;background:linear-gradient(90deg,#a78bfa,#667eea);
  position:relative;overflow:hidden;}
.p-connector::after{content:'';position:absolute;top:-1px;left:-100%;
  width:100%;height:4px;background:#fff;opacity:0.8;
  animation:flow 2s linear infinite;}
@keyframes flow{from{left:-100%;}to{left:200%;}}

/* SECTION 5 - Launch */
.launch-section{background:radial-gradient(ellipse at center,#050520 0%,#000 70%);}
.launch-grid{display:flex;gap:40px;align-items:center;flex-wrap:wrap;
  justify-content:center;max-width:900px;}
.code-block{background:#0d1117;border:1px solid #21262d;border-radius:12px;
  padding:28px;width:380px;text-align:left;font-family:'Courier New',monospace;
  font-size:13px;line-height:2;}
.code-import{color:#ff7b72;}
.code-comment{color:#6e7681;}
.code-var{color:#79c0ff;}
.code-string{color:#a5d6ff;}
.code-output{color:#00ff88;}
.system-ready{text-align:left;max-width:320px;}
.system-ready h3{font-family:'Orbitron',monospace;font-size:28px;
  color:#00ff88;letter-spacing:4px;margin-bottom:20px;
  text-shadow:0 0 20px rgba(0,255,136,0.5);}
.system-ready p{font-size:14px;color:#8899bb;line-height:1.7;}

/* Scroll indicator */
.scroll-hint{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);
  color:#333;font-size:12px;letter-spacing:2px;animation:bounce 2s infinite;}
@keyframes bounce{0%,100%{transform:translateX(-50%) translateY(0);}
  50%{transform:translateX(-50%) translateY(8px);}}

/* Floating particles */
.particle{position:fixed;width:2px;height:2px;background:#4466ff;
  border-radius:50%;pointer-events:none;animation:float-up linear infinite;opacity:0;}
@keyframes float-up{
  0%{transform:translateY(100vh) translateX(0);opacity:0;}
  10%{opacity:0.6;}
  90%{opacity:0.6;}
  100%{transform:translateY(-100px) translateX(var(--drift));opacity:0;}}
/* 3D Orbit Animation */
.orbit-container {
  width: 350px;
  height: 350px;
  perspective: 1200px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.star-system {
  position: relative;
  transform-style: preserve-3d;
  transform: rotateX(75deg);
}
.orbit-ring {
  position: absolute;
  width: 320px;
  height: 320px;
  border: 2px dashed rgba(100, 150, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
}
.star-sphere {
  width: 120px;
  height: 120px;
  background: radial-gradient(circle at 30% 30%, #ffffff 0%, #ffcc00 30%, #ff6600 70%, #aa2200 100%);
  border-radius: 50%;
  position: absolute;
  transform: translate(-50%, -50%) rotateX(-75deg);
  box-shadow: 0 0 60px rgba(255,136,0,0.6);
}
.planet-pivot {
  position: absolute;
  transform-style: preserve-3d;
  animation: pivot 4s linear infinite;
}
.planet-translate {
  transform: translateX(160px);
  transform-style: preserve-3d;
}
.planet-anti-pivot {
  transform-style: preserve-3d;
  animation: anti-pivot 4s linear infinite;
}
.planet-sphere {
  width: 24px;
  height: 24px;
  background: radial-gradient(circle at 30% 30%, #a8c5ff 0%, #4466ff 50%, #001144 100%);
  border-radius: 50%;
  position: absolute;
  transform: translate(-50%, -50%) rotateX(-75deg);
  box-shadow: inset -4px -4px 8px rgba(0,0,0,0.7);
}
@keyframes pivot {
  0%   { transform: rotateZ(-207.391deg); }
  100% { transform: rotateZ(1044.782deg); }
}
@keyframes anti-pivot {
  0%   { transform: rotateZ(207.391deg); }
  100% { transform: rotateZ(-1044.782deg); }
}
@media (max-width: 900px) {
  .transit-container { flex-direction: column; text-align: center; }
  .transit-container > div { text-align: center !important; }
  .section-title, .section-desc { text-align: center !important; margin: 0 auto 20px auto; }
}
</style>
</head>
<body>"""

    part2 = """
<canvas id="star-canvas"></canvas>

<!-- SECTION 1: HERO -->
<section class="hero">
  <div style="position:relative;z-index:1">
    <div class="hero-title">SIGNALNOVA</div>
    <div class="hero-sub">AI-Powered Exoplanet Detection Engine</div>
    <div class="hero-desc">Analyzing millions of TESS light curves to find the next Earth.</div>
    <div style="margin-top:20px">
      <div id="counter-display" style="font-family:'Orbitron',monospace;
        font-size:13px;color:#4466ff;letter-spacing:2px;margin-bottom:30px">
        STARS ANALYZED: <span id="counter">0</span>
      </div>
    </div>
  </div>
  <div class="scroll-hint">▼ SCROLL TO EXPLORE ▼</div>
</section>

<!-- SECTION 2: TRANSIT PHENOMENON -->
<section class="transit-section">
  <div class="transit-container" style="display:flex; align-items:center; gap:40px; max-width:1200px; width:100%; margin:0 auto; position:relative; z-index:1;">
    
    <!-- LEFT COLUMN -->
    <div style="flex:1.2; text-align:left;">
      <div class="section-title" style="text-align:left;">The Transit Phenomenon</div>
      <div class="section-desc" style="text-align:left; max-width:100%;">
        When a distant world crosses in front of its host star, it blocks a microscopic
        fraction of light. Our mission is to extract these incredibly faint periodic
        signatures from the intense chaos of stellar noise.
      </div>
      <div class="lc-wrapper" style="margin:0; width:100%; max-width:650px;">
        <div class="lc-scan"></div>
        <svg class="lc-svg" viewBox="0 0 800 200">
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#334466"/>
            </marker>
          </defs>
          <!-- Grid lines -->
          <line x1="0" y1="60" x2="800" y2="60" stroke="rgba(60,100,200,0.15)" stroke-width="1" stroke-dasharray="4"/>
          <line x1="0" y1="100" x2="800" y2="100" stroke="rgba(60,100,200,0.2)" stroke-width="1" stroke-dasharray="4"/>
          <line x1="0" y1="140" x2="800" y2="140" stroke="rgba(60,100,200,0.15)" stroke-width="1" stroke-dasharray="4"/>
          <!-- Light curve path with 3 transits -->
          <path d="M0,100 C20,100 30,98 50,100 C70,102 90,99 110,100 
                   C130,101 145,100 155,100 C165,100 170,112 178,130 
                   C183,140 186,145 190,145 C194,145 197,140 202,130 
                   C210,112 215,100 225,100 C240,100 260,101 280,100
                   C300,99 320,100 340,100 C360,101 375,100 385,100
                   C395,100 400,112 408,130 C413,140 416,145 420,145
                   C424,145 427,140 432,130 C440,112 445,100 455,100
                   C470,100 490,99 510,100 C530,101 560,100 580,100
                   C600,100 620,101 640,100 C645,100 650,112 658,130 
                   C663,140 666,145 670,145 C674,145 677,140 682,130 
                   C690,112 695,100 705,100 C720,100 740,100 800,100"
                fill="none" stroke="#4488ff" stroke-width="2.5" filter="url(#glow)"/>
          <!-- Transit markers -->
          <circle cx="190" cy="145" r="5" fill="#facc15" class="transit-point"/>
          <circle cx="420" cy="145" r="5" fill="#facc15" class="transit-point" style="animation-delay:0.5s"/>
          <circle cx="650" cy="145" r="5" fill="#facc15" class="transit-point" style="animation-delay:1.0s"/>
          <!-- Labels -->
          <text x="190" y="170" fill="#facc15" font-size="10" text-anchor="middle" font-family="monospace">T₁</text>
          <text x="420" y="170" fill="#facc15" font-size="10" text-anchor="middle" font-family="monospace">T₂</text>
          <text x="650" y="170" fill="#facc15" font-size="10" text-anchor="middle" font-family="monospace">T₃</text>
          <text x="535" y="95" fill="#6677aa" font-size="11" font-family="monospace">Period P</text>
          <line x1="420" y1="88" x2="650" y2="88" stroke="#334466" stroke-width="1" stroke-dasharray="3" marker-end="url(#arrow)"/>
        </svg>
      </div>
    </div>
    
    <!-- RIGHT COLUMN -->
    <div style="flex:0.8; display:flex; justify-content:center; align-items:center;">
       <div class="orbit-container">
          <div class="star-system">
             <div class="orbit-ring"></div>
             <div class="star-sphere"></div>
             <div class="planet-pivot">
                 <div class="planet-translate">
                     <div class="planet-anti-pivot">
                         <div class="planet-sphere"></div>
                     </div>
                 </div>
             </div>
          </div>
       </div>
    </div>
    
  </div>
  <div class="scroll-hint">▼</div>
</section>

<!-- SECTION 3: FILTERING IMPOSTERS -->
<section class="imposters-section">
  <div style="position:relative;z-index:1">
    <div class="section-title">Filtering The Imposters</div>
    <div class="section-desc">
      The universe is messy. Eclipsing binaries, background stars, and instrument
      artifacts mimic planetary transits. We use advanced geometric analysis and
      machine learning to find the truth.
    </div>
    <div class="cards-grid">
      <div class="signal-card card-planet">
        <div class="card-icon">🌍</div>
        <div class="card-title">Confirmed Planet</div>
        <div class="card-body">Clean, U-shaped periodic dips with flat bottoms,
          indicating a solid opaque body crossing the stellar disk. SNR &gt; 6σ.
          Odd/even depths consistent. No secondary eclipse.</div>
      </div>
      <div class="signal-card card-eb">
        <div class="card-icon">🔥</div>
        <div class="card-title">Eclipsing Binary</div>
        <div class="card-body">V-shaped alternating primary and secondary eclipses.
          Odd/even depth mismatch flags this class. Secondary eclipse depth
          &gt; 20% of primary. Centroid shifts visible.</div>
      </div>
      <div class="signal-card card-noise">
        <div class="card-icon">📡</div>
        <div class="card-title">Instrumental Noise</div>
        <div class="card-body">Asymmetric artifacts, jitter, and erratic spikes
          generated by the TESS detector. No periodicity. High flux kurtosis.
          Eliminated by sigma-clipping and detrending.</div>
      </div>
    </div>
  </div>
  <div class="scroll-hint">▼</div>
</section>"""

    part3 = """
<!-- SECTION 4: PIPELINE -->
<section class="pipeline-section">
  <div style="position:relative;z-index:1">
    <div class="section-title">Neural Pipeline Architecture</div>
    <div class="section-desc">
      Our end-to-end processing framework seamlessly ingests raw NASA data,
      isolates the signal, performs Box Least Squares frequency searches, and
      predicts exoplanet probability.
    </div>
    <div class="pipeline-nodes">
      <div class="p-node">
        <div class="p-circle" id="pn0">🛰️</div>
        <div class="p-label">Fetch<br>TESS Data</div>
      </div>
      <div class="p-connector"></div>
      <div class="p-node">
        <div class="p-circle" id="pn1">🧹</div>
        <div class="p-label">Flatten &amp;<br>Detrend</div>
      </div>
      <div class="p-connector"></div>
      <div class="p-node">
        <div class="p-circle" id="pn2">📊</div>
        <div class="p-label">BLS<br>Spectrogram</div>
      </div>
      <div class="p-connector"></div>
      <div class="p-node">
        <div class="p-circle" id="pn3">🧠</div>
        <div class="p-label">XGBoost<br>Inference</div>
      </div>
      <div class="p-connector"></div>
      <div class="p-node">
        <div class="p-circle active" id="pn4">🚀</div>
        <div class="p-label">Planet<br>Found</div>
      </div>
    </div>
    <!-- Animated pipeline stats -->
    <div style="margin-top:50px;display:flex;gap:40px;justify-content:center;flex-wrap:wrap">
      <div style="text-align:center">
        <div style="font-family:'Orbitron',monospace;font-size:32px;color:#a78bfa">
          &lt;2s</div>
        <div style="font-size:12px;color:#4a6080;letter-spacing:1px;margin-top:4px">
          PER STAR</div>
      </div>
      <div style="text-align:center">
        <div style="font-family:'Orbitron',monospace;font-size:32px;color:#60a5fa">
          19,440</div>
        <div style="font-size:12px;color:#4a6080;letter-spacing:1px;margin-top:4px">
          DATA POINTS</div>
      </div>
      <div style="font-family:'Orbitron',monospace;font-size:32px;
        text-align:center;color:#4ade80">
        <div>4-CLASS</div>
        <div style="font-size:12px;color:#4a6080;letter-spacing:1px;
          margin-top:4px;font-family:'Inter',sans-serif">ML OUTPUT</div>
      </div>
    </div>
  </div>
  <div class="scroll-hint">▼</div>
</section>

<!-- SECTION 5: LAUNCH -->
<section class="launch-section">
  <div style="position:relative;z-index:1;width:100%">
    <div class="section-title">Enter the Interactive Command Center</div>
    <div class="section-desc">
      Input TIC IDs, dynamically fold phase curves, and run real-time
      inference on the stars.
    </div>
    <div class="launch-grid">
      <div class="code-block">
        <div><span class="code-import">import</span> signalnova</div>
        <div>&nbsp;</div>
        <div><span class="code-comment"># Initialize Target</span></div>
        <div><span class="code-var">star</span> = signalnova.Target(
          tic_id=<span class="code-string">"25155310"</span>)</div>
        <div>&nbsp;</div>
        <div><span class="code-comment"># Execute Pipeline</span></div>
        <div><span class="code-var">result</span> = star.run_pipeline(
          mode=<span class="code-string">'bls+xgb'</span>)</div>
        <div>&nbsp;</div>
        <div><span class="code-comment"># Predict</span></div>
        <div>print(<span class="code-string">f"Probability: 
          {result.prob:.2%}"</span>)</div>
        <div><span class="code-output">&gt; Probability: 99.8% 
          (CONFIRMED PLANET)</span></div>
      </div>
      <div class="system-ready">
        <h3>SYSTEM READY</h3>
        <p>The dashboard is standing by. Click the button below to launch
          the graphical interface and begin your analysis.</p>
      </div>
    </div>
  </div>
</section>"""

    part4 = """
<script>
// Starfield
const canvas = document.getElementById('star-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const stars = [];
for(let i=0;i<200;i++){
  stars.push({
    x:Math.random()*canvas.width,
    y:Math.random()*canvas.height,
    r:Math.random()*1.5+0.3,
    speed:Math.random()*0.3+0.05,
    opacity:Math.random()*0.8+0.2,
    twinkle:Math.random()*Math.PI*2
  });
}
function animateStars(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const t = Date.now()/1000;
  stars.forEach(s=>{
    const op = s.opacity*(0.7+0.3*Math.sin(t*s.speed*3+s.twinkle));
    ctx.beginPath();
    ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
    ctx.fillStyle='rgba(255,255,255,'+op+')';
    ctx.fill();
  });
  requestAnimationFrame(animateStars);
}
animateStars();

// Counter animation
let count = 0;
const target = 847293;
const el = document.getElementById('counter');
const interval = setInterval(()=>{
  count += Math.floor(Math.random()*5000+3000);
  if(count >= target){count=target;clearInterval(interval);}
  el.textContent = count.toLocaleString();
},50);

// Pipeline node animation
let activeNode = 0;
const nodes = document.querySelectorAll('[id^="pn"]');
setInterval(()=>{
  nodes.forEach((n,i)=>{
    if(i===activeNode){
      n.style.borderColor='#00ff88';
      n.style.boxShadow='0 0 30px rgba(0,255,136,0.6)';
    } else {
      n.style.borderColor='#a78bfa';
      n.style.boxShadow='0 0 20px rgba(167,139,250,0.2)';
    }
  });
  activeNode = (activeNode+1)%nodes.length;
},800);

// Floating particles
for(let i=0;i<15;i++){
  const p = document.createElement('div');
  p.className='particle';
  const drift = (Math.random()-0.5)*200;
  p.style.cssText='left:'+Math.random()*100+'%;'+
    'animation-duration:'+(8+Math.random()*12)+'s;'+
    'animation-delay:'+(Math.random()*10)+'s;'+
    '--drift:'+drift+'px;';
  document.body.appendChild(p);
}

window.addEventListener('resize',()=>{
  canvas.width=window.innerWidth;
  canvas.height=window.innerHeight;
});
</script>
</body>
</html>"""

    # Combine all parts
    html_content = part1 + part2 + part3 + part4

    try:
        import streamlit.components.v1 as components
        components.html(html_content, height=3300, scrolling=False)
    except Exception:
        st.markdown(html_content, unsafe_allow_html=True)

    # Launch button smoothly integrated above footer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🚀 INITIATE DASHBOARD",
            type="primary",
            use_container_width=True,
            key="launch_main"
        ):
            st.session_state.show_dashboard = True
            st.rerun()
