import os, sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(root)
sys.path.insert(0, os.path.join(root, 'ps7_exoplanet', 'src'))

import streamlit as st
import streamlit.components.v1 as components

def render_landing():
    # Hide Streamlit's default padding and float our launch button as a pill
    st.markdown("""
    <style>
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    header { visibility: hidden; }
    
    /* Target the button container to prevent full width stretching */
    .stButton {
        position: fixed !important;
        bottom: 40px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 99999 !important;
        width: auto !important;
        display: flex;
        justify-content: center;
    }

    .stButton > button {
        background: linear-gradient(90deg, #378ADD, #8b5cf6) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        padding: 20px 80px !important;
        border-radius: 60px !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        box-shadow: 0 15px 50px rgba(55,138,221,0.6), inset 0 0 20px rgba(255,255,255,0.2) !important;
        letter-spacing: 3px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: auto !important;
        min-width: 400px !important;
    }
    .stButton > button:hover {
        transform: scale(1.05) translateY(-5px) !important;
        box-shadow: 0 20px 60px rgba(55,138,221,0.9), inset 0 0 30px rgba(255,255,255,0.4) !important;
        border-color: rgba(255,255,255,1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@300;400;600&display=swap');
        
        :root {
            --bg: #02040a;
            --text: #e2e8f0;
            --primary: #3b82f6;
            --accent: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
        }

        * { box-sizing: border-box; }

        body, html {
            margin: 0; padding: 0;
            width: 100%; height: 100%;
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
            overflow-y: auto;
            scroll-behavior: smooth;
        }

        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

        .bg-layer {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -1;
            background: radial-gradient(circle at center, #0a0f1c 0%, #02040a 100%);
        }
        
        .star {
            position: absolute;
            background: #fff;
            border-radius: 50%;
            animation: twinkle var(--duration) infinite ease-in-out alternate;
            will-change: opacity;
        }
        @keyframes twinkle {
            0% { opacity: 0.1; }
            100% { opacity: 0.9; box-shadow: 0 0 8px #fff; }
        }

        .section {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 60px 5%;
            text-align: center;
            position: relative;
        }

        h1, h2, h3 { font-family: 'Orbitron', sans-serif; margin: 0; }
        
        h1 {
            font-size: clamp(4rem, 8vw, 8rem);
            font-weight: 900;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            background: linear-gradient(135deg, #ffffff 0%, var(--primary) 40%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            opacity: 0; transform: translateY(50px) scale(0.9);
            transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);
            text-shadow: 0 20px 40px rgba(59,130,246,0.3);
        }
        
        h2 {
            font-size: clamp(2.5rem, 5vw, 5rem);
            color: #fff;
            margin-bottom: 40px;
            text-shadow: 0 0 30px rgba(59,130,246,0.5);
            opacity: 0; transform: translateY(50px);
            transition: all 1s ease-out 0.2s;
            max-width: 1200px;
        }

        p.lead {
            font-size: clamp(1.2rem, 1.8vw, 1.8rem);
            color: #94a3b8;
            max-width: 1000px;
            line-height: 1.8;
            opacity: 0; transform: translateY(40px);
            transition: all 1s ease-out 0.4s;
        }

        .graphic {
            margin-top: 80px;
            opacity: 0; transform: translateY(60px) scale(0.9);
            transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1) 0.6s;
            width: 100%; display: flex; justify-content: center;
        }

        .section.visible h1,
        .section.visible h2,
        .section.visible p.lead,
        .section.visible .graphic {
            opacity: 1;
            transform: translateY(0) scale(1);
        }

        /* MASSIVE 3D Planet System */
        .planet-system {
            width: 500px; height: 500px;
            position: relative;
            transform-style: preserve-3d;
            transform: rotateX(75deg) rotateZ(-20deg);
            animation: rotate-sys 20s linear infinite;
        }
        @keyframes rotate-sys {
            100% { transform: rotateX(75deg) rotateZ(340deg); }
        }
        .star-core {
            position: absolute;
            top: 50%; left: 50%;
            width: 180px; height: 180px;
            margin: -90px 0 0 -90px;
            background: radial-gradient(circle, #fff, #fde047 30%, #ea580c 70%, #7c2d12 100%);
            border-radius: 50%;
            box-shadow: 0 0 100px rgba(245,158,11,0.8), 0 0 200px rgba(234,88,12,0.4);
            transform: rotateX(-90deg); /* Counter-rotate */
        }
        .orbit {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            border: 3px solid rgba(255,255,255,0.15); border-radius: 50%;
            box-shadow: inset 0 0 20px rgba(255,255,255,0.05);
        }
        .orbit-2 {
            position: absolute; top: -100px; left: -100px; width: 700px; height: 700px;
            border: 1px dashed rgba(255,255,255,0.1); border-radius: 50%;
            animation: spin-reverse 30s linear infinite;
        }
        @keyframes spin-reverse { 100% { transform: rotateZ(-360deg); } }
        
        .exoplanet {
            position: absolute; top: -20px; left: 50%;
            width: 40px; height: 40px; margin-left: -20px;
            background: radial-gradient(circle at 30% 30%, #60a5fa, #1e3a8a);
            border-radius: 50%;
            box-shadow: inset -5px -5px 15px rgba(0,0,0,0.8), 0 0 30px var(--primary);
        }
        .exoplanet-2 {
            position: absolute; top: 50%; left: -15px;
            width: 30px; height: 30px; margin-top: -15px;
            background: radial-gradient(circle at 30% 30%, #a78bfa, #4c1d95);
            border-radius: 50%;
            box-shadow: inset -5px -5px 10px rgba(0,0,0,0.8), 0 0 20px var(--accent);
        }

        /* GIANT Transit Path */
        .transit-container {
            width: 100%; max-width: 1200px; height: 400px;
            background: rgba(15,23,42,0.4); border: 2px solid rgba(59,130,246,0.3);
            border-radius: 24px; position: relative; overflow: hidden;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6), inset 0 0 50px rgba(59,130,246,0.1);
        }
        .scanner-bar {
            position: absolute; top: 0; left: -10%; width: 8px; height: 100%;
            background: #fff; box-shadow: 0 0 30px #fff, 0 0 60px var(--primary);
            animation: scan 5s ease-in-out infinite;
        }
        @keyframes scan { 
            0% { left: -10%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { left: 110%; opacity: 0; }
        }

        /* GIANT Cards */
        .card-grid {
            display: flex; gap: 40px; flex-wrap: wrap; justify-content: center;
        }
        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 50px 40px;
            width: 400px;
            text-align: left;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }
        .glass-card:hover { transform: translateY(-20px) scale(1.02); background: rgba(30, 41, 59, 0.9); }

        /* GIANT Pipeline */
        .pipeline {
            display: flex; align-items: center; justify-content: center; gap: 30px; flex-wrap: wrap;
            position: relative;
        }
        .pipeline::before {
            content: '';
            position: absolute;
            top: 50%; left: 10%; right: 10%;
            height: 4px;
            background: rgba(255,255,255,0.1);
            z-index: -1;
            transform: translateY(-50%);
        }
        .node {
            background: #0f172a; border: 3px solid var(--accent);
            border-radius: 50%; width: 180px; height: 180px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            font-family: 'Orbitron'; font-size: 1.1rem; letter-spacing: 1px;
            box-shadow: 0 0 30px rgba(139,92,246,0.4), inset 0 0 20px rgba(139,92,246,0.2);
            transition: all 0.4s;
        }
        .node:hover { transform: scale(1.15); box-shadow: 0 0 50px var(--accent), inset 0 0 30px var(--accent); background: #1e1b4b; }
        .node-icon { font-size: 3.5rem; margin-bottom: 15px; }

        .scroll-indicator {
            position: absolute; bottom: 50px; left: 50%; transform: translateX(-50%);
            animation: bounce 2s infinite; color: #94a3b8; font-size: 2.5rem;
            cursor: pointer;
            z-index: 50;
        }
        @keyframes bounce { 0%, 100% { transform: translate(-50%, 0); } 50% { transform: translate(-50%, -20px); } }

        /* Data Visualization Section (New) */
        .data-viz {
            width: 100%; max-width: 1200px;
            display: grid; grid-template-columns: 1fr 1fr; gap: 40px;
            text-align: left;
        }
        .code-block {
            background: #0d1117; border-radius: 16px; padding: 30px;
            font-family: monospace; color: #58a6ff; font-size: 1.2rem;
            border: 1px solid #30363d;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }

    </style>
    </head>
    <body>
        <div class="bg-layer" id="bgLayer"></div>

        <!-- 1. HERO -->
        <div class="section visible" id="sec1">
            <h1>SignalNova</h1>
            <p class="lead" style="font-size: 2rem; color: #fff;">AI-Powered Exoplanet Detection Engine</p>
            <p class="lead" style="margin-top: -20px;">Analyzing millions of TESS light curves to find the next Earth.</p>
            <div class="graphic">
                <div class="planet-system">
                    <div class="orbit"><div class="exoplanet"></div></div>
                    <div class="orbit-2"><div class="exoplanet-2"></div></div>
                    <div class="star-core"></div>
                </div>
            </div>
            <div class="scroll-indicator" onclick="document.getElementById('sec2').scrollIntoView()">↓</div>
        </div>

        <!-- 2. TRANSIT -->
        <div class="section" id="sec2">
            <h2>The Transit Phenomenon</h2>
            <p class="lead">When a distant world crosses in front of its host star, it blocks a microscopic fraction of light. Our mission is to extract these incredibly faint periodic signatures from the intense chaos of stellar noise.</p>
            <div class="graphic">
                <div class="transit-container">
                    <svg viewBox="0 0 1200 400" style="width:100%; height:100%;">
                        <!-- Grid lines -->
                        <line x1="0" y1="100" x2="1200" y2="100" stroke="rgba(255,255,255,0.05)" stroke-dasharray="10,10" stroke-width="2"/>
                        <line x1="0" y1="200" x2="1200" y2="200" stroke="rgba(255,255,255,0.1)" stroke-dasharray="10,10" stroke-width="2"/>
                        <line x1="0" y1="300" x2="1200" y2="300" stroke="rgba(255,255,255,0.05)" stroke-dasharray="10,10" stroke-width="2"/>
                        
                        <!-- Light curve path -->
                        <path d="M 0 100 L 400 100 C 450 100 480 320 520 320 C 560 320 590 100 640 100 L 1200 100" fill="none" stroke="var(--primary)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 15px var(--primary));"/>
                        
                        <!-- Dots on path -->
                        <circle cx="200" cy="100" r="6" fill="#fff"/>
                        <circle cx="520" cy="320" r="10" fill="#fff" style="filter: drop-shadow(0 0 15px #fff);"/>
                        <circle cx="900" cy="100" r="6" fill="#fff"/>
                    </svg>
                    <div class="scanner-bar"></div>
                </div>
            </div>
        </div>

        <!-- 3. CHALLENGE -->
        <div class="section" id="sec3">
            <h2>Filtering The Imposters</h2>
            <p class="lead">The universe is messy. Eclipsing binaries, background stars, and instrument artifacts mimic planetary transits. We use advanced geometric analysis and machine learning to find the truth.</p>
            <div class="graphic card-grid">
                <div class="glass-card" style="border-top: 6px solid var(--success); box-shadow: 0 10px 40px rgba(16,185,129,0.2);">
                    <h3 style="color:var(--success); font-size:2rem; margin-bottom:20px;">🌍 Confirmed Planet</h3>
                    <p style="color:#cbd5e1; line-height:1.8; font-size: 1.2rem;">Clean, U-shaped periodic dips with flat bottoms, indicating a solid spherical world transiting the host star.</p>
                </div>
                <div class="glass-card" style="border-top: 6px solid var(--warning); box-shadow: 0 10px 40px rgba(245,158,11,0.2);">
                    <h3 style="color:var(--warning); font-size:2rem; margin-bottom:20px;">🔥 Eclipsing Binary</h3>
                    <p style="color:#cbd5e1; line-height:1.8; font-size: 1.2rem;">V-shaped, alternating primary and secondary dips caused by twin massive stars orbiting and eclipsing each other.</p>
                </div>
                <div class="glass-card" style="border-top: 6px solid var(--danger); box-shadow: 0 10px 40px rgba(239,68,68,0.2);">
                    <h3 style="color:var(--danger); font-size:2rem; margin-bottom:20px;">📡 Instrumental Noise</h3>
                    <p style="color:#cbd5e1; line-height:1.8; font-size: 1.2rem;">Asymmetric artifacts, jitter, and erratic spikes generated by the spacecraft's thrusters or momentum dumps.</p>
                </div>
            </div>
        </div>

        <!-- 4. PIPELINE -->
        <div class="section" id="sec4">
            <h2>Neural Pipeline Architecture</h2>
            <p class="lead">Our end-to-end processing framework seamlessly ingests raw NASA data, isolates the signal, performs Box Least Squares frequency searches, and predicts exoplanet probability.</p>
            <div class="graphic pipeline">
                <div class="node"><div class="node-icon">🛰️</div>Fetch<br>TESS Data</div>
                <div class="node"><div class="node-icon">🧹</div>Flatten &<br>Detrend</div>
                <div class="node"><div class="node-icon">📉</div>BLS<br>Spectrogram</div>
                <div class="node"><div class="node-icon">🧠</div>XGBoost<br>Inference</div>
                <div class="node" style="border-color:var(--success); box-shadow:0 0 40px rgba(16,185,129,0.5);"><div class="node-icon">🚀</div>Planet<br>Found</div>
            </div>
        </div>

        <!-- 5. CTA -->
        <div class="section" id="sec5">
            <h2>Initialize The Engine</h2>
            <p class="lead" style="margin-bottom: 80px;">Enter the interactive command center. Input TIC IDs, dynamically fold phase curves, and run real-time inference on the stars.</p>
            
            <div class="data-viz graphic">
                <div class="code-block">
                    <span style="color:#ff7b72;">import</span> signalnova<br><br>
                    <span style="color:#8b949e;"># Initialize Target</span><br>
                    star <span style="color:#ff7b72;">=</span> signalnova.Target(tic_id=<span style="color:#a5d6ff;">"25155310"</span>)<br><br>
                    <span style="color:#8b949e;"># Execute Pipeline</span><br>
                    result <span style="color:#ff7b72;">=</span> star.run_pipeline(mode=<span style="color:#a5d6ff;">'bls+xgb'</span>)<br><br>
                    <span style="color:#8b949e;"># Predict</span><br>
                    <span style="color:#79c0ff;">print</span>(f"Probability: {result.prob:.2%}")<br>
                    <span style="color:#a5d6ff;">> Probability: 99.8% (CONFIRMED PLANET)</span>
                </div>
                <div style="display: flex; flex-direction: column; justify-content: center; padding: 0 40px;">
                    <h3 style="font-size: 2.5rem; margin-bottom: 20px; color: var(--primary);">SYSTEM READY</h3>
                    <p style="font-size: 1.4rem; color: #94a3b8; line-height: 1.6;">The dashboard is standing by. Click the button below to launch the graphical interface and begin your analysis.</p>
                </div>
            </div>
            
            <div style="height: 250px;"></div> <!-- Padding for floating button -->
        </div>

        <script>
            // Hardware Accelerated Stars
            const bg = document.getElementById('bgLayer');
            const frag = document.createDocumentFragment();
            for(let i=0; i<250; i++) { // Increased star count
                let s = document.createElement('div');
                s.className = 'star';
                s.style.left = Math.random()*100 + '%';
                s.style.top = Math.random()*100 + '%';
                s.style.width = s.style.height = (Math.random()*2+1)+'px';
                s.style.setProperty('--duration', (Math.random()*4+2)+'s');
                s.style.animationDelay = Math.random()*5+'s';
                frag.appendChild(s);
            }
            bg.appendChild(frag);

            // Intersection Observer
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if(entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, { threshold: 0.15 });

            document.querySelectorAll('.section').forEach(sec => observer.observe(sec));
        </script>
    </body>
    </html>
    """
    
    # Render with scrolling enabled and fixed height for smooth native scroll inside iframe
    components.html(html_content, height=900, scrolling=True)
    
    # Empty container to anchor the button correctly
    st.container()
    
    # Launch button - CSS is handled above
    if st.button("🚀 INITIATE DASHBOARD", key="launch_dashboard"):
        st.session_state.show_dashboard = True
        st.rerun()
