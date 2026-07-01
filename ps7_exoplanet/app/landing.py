def render_landing():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
    background: #0a0e1a;
    font-family: 'Segoe UI', sans-serif;
    color: #e8f4fd;
    height: 860px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
}
/* Starfield */
.stars { position:absolute; width:100%; height:100%; top:0; left:0; }
.star {
    position:absolute;
    background:#ffffff;
    border-radius:50%;
    animation: twinkle 3s infinite alternate;
}
@keyframes twinkle {
    0% { opacity:0.2; transform:scale(1); }
    100% { opacity:1; transform:scale(1.3); }
}
/* Orbiting planet */
.solar-system {
    position:relative;
    width:200px; height:200px;
    margin-bottom:40px;
}
.star-center {
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    width:70px; height:70px;
    background:radial-gradient(circle, #facc15, #f59e0b, #d97706);
    border-radius:50%;
    box-shadow: 0 0 40px #facc15, 0 0 80px rgba(250,204,21,0.4);
    animation: pulse-star 2s ease-in-out infinite alternate;
}
@keyframes pulse-star {
    0% { box-shadow:0 0 30px #facc15, 0 0 60px rgba(250,204,21,0.3); }
    100% { box-shadow:0 0 50px #facc15, 0 0 100px rgba(250,204,21,0.5); }
}
.orbit-ring {
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    width:180px; height:180px;
    border:1px solid rgba(96,165,250,0.2);
    border-radius:50%;
}
.planet {
    position:absolute;
    top:50%; left:50%;
    width:18px; height:18px;
    margin-top:-9px; margin-left:-9px;
    animation: orbit 5s linear infinite;
}
.planet-body {
    width:18px; height:18px;
    background:radial-gradient(circle, #60a5fa, #1e40af);
    border-radius:50%;
    box-shadow:0 0 10px rgba(96,165,250,0.6);
}
@keyframes orbit {
    from { transform:rotate(0deg) translateX(90px) rotate(0deg); }
    to   { transform:rotate(360deg) translateX(90px) rotate(-360deg); }
}
/* Light curve */
.lc-container {
    width:400px; height:80px;
    margin-bottom:30px;
    position:relative;
}
/* Text */
.main-title {
    font-size:36px; font-weight:800;
    color:#e8f4fd;
    text-shadow: 0 0 30px rgba(55,138,221,0.8);
    text-align:center; margin-bottom:8px;
    letter-spacing:-0.5px;
}
.subtitle {
    font-size:16px; color:#a8c5e2;
    text-align:center; margin-bottom:6px;
}
.badge {
    display:inline-block;
    border:1px solid #1e3a5f;
    border-radius:20px;
    padding:4px 14px;
    font-size:12px; color:#6b8bb5;
    margin-bottom:30px;
}
.features {
    display:flex; gap:30px;
    margin-top:10px;
}
.feature-pill {
    background:rgba(30,58,95,0.4);
    border:1px solid #1e3a5f;
    border-radius:8px;
    padding:8px 16px;
    font-size:12px;
    color:#a8c5e2;
    text-align:center;
}
.feature-pill span {
    display:block;
    font-size:18px;
    margin-bottom:4px;
}
/* Nebula glow */
.nebula {
    position:absolute;
    border-radius:50%;
    filter:blur(80px);
    pointer-events:none;
}
.nebula-1 {
    width:400px; height:400px;
    background:radial-gradient(circle, rgba(167,139,250,0.08), transparent);
    top:-100px; right:-100px;
    animation:drift1 20s ease-in-out infinite alternate;
}
.nebula-2 {
    width:300px; height:300px;
    background:radial-gradient(circle, rgba(55,138,221,0.08), transparent);
    bottom:-50px; left:-50px;
    animation:drift2 25s ease-in-out infinite alternate;
}
@keyframes drift1 {
    0%{transform:translate(0,0);} 100%{transform:translate(30px,20px);}
}
@keyframes drift2 {
    0%{transform:translate(0,0);} 100%{transform:translate(-20px,30px);}
}
</style>
</head>
<body>
<div class="nebula nebula-1"></div>
<div class="nebula nebula-2"></div>
<div class="stars" id="stars"></div>

<div class="solar-system">
    <div class="orbit-ring"></div>
    <div class="star-center"></div>
    <div class="planet"><div class="planet-body"></div></div>
</div>

<h1 class="main-title">🔭 Exoplanet Transit Detection</h1>
<p class="subtitle">AI-powered discovery from noisy TESS starlight</p>
<span class="badge">ISRO Bharatiya Antariksh Hackathon 2026 — PS7</span>

<svg class="lc-container" viewBox="0 0 400 80" id="lc-svg">
  <polyline id="lc-line" 
    points="0,20 50,20 80,20 100,20 120,20 130,45 140,55 150,45 160,20 180,20 210,20 230,20 250,20 270,20 280,45 290,55 300,45 310,20 340,20 380,20 400,20"
    fill="none" stroke="#60a5fa" stroke-width="2"
    stroke-dasharray="600" stroke-dashoffset="600">
    <animate attributeName="stroke-dashoffset" 
      from="600" to="0" dur="2s" fill="freeze"/>
  </animate>
  </polyline>
  <circle r="4" fill="#facc15" opacity="0">
    <animateMotion dur="2s" fill="freeze"
      path="M0,20 L50,20 L80,20 L100,20 L120,20 L130,45 L140,55 L150,45 L160,20 L180,20 L210,20 L230,20 L250,20 L270,20 L280,45 L290,55 L300,45 L310,20 L340,20 L380,20 L400,20"/>
    <animate attributeName="opacity" from="0" to="1" 
      begin="0.1s" dur="0.1s" fill="freeze"/>
  </circle>
  <text x="135" y="75" fill="#facc15" font-size="10" 
    text-anchor="middle" opacity="0">
    Transit detected
    <animate attributeName="opacity" from="0" to="1" 
      begin="2s" dur="0.5s" fill="freeze"/>
  </text>
</svg>

<div class="features">
    <div class="feature-pill"><span>📡</span>BLS Detection</div>
    <div class="feature-pill"><span>🤖</span>ML Classification</div>
    <div class="feature-pill"><span>✅</span>Auto Vetting</div>
    <div class="feature-pill"><span>📊</span>Live Dashboard</div>
</div>

<script>
// Generate starfield
const container = document.getElementById('stars');
for (let i = 0; i < 150; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    const size = Math.random() * 2 + 1;
    star.style.cssText = `
        width:${size}px; height:${size}px;
        top:${Math.random()*100}%;
        left:${Math.random()*100}%;
        animation-delay:${Math.random()*3}s;
        animation-duration:${2+Math.random()*3}s;
        opacity:${Math.random()*0.7+0.2};
    `;
    container.appendChild(star);
}
</script>
</body>
</html>
"""
    try:
        import streamlit.components.v1 as components
        components.html(html_content, height=880, scrolling=False)
    except Exception:
        pass
    
    import streamlit as st
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🚀 Launch Dashboard",
            type="primary",
            use_container_width=True,
            key="launch_btn"
        ):
            st.session_state.show_dashboard = True
            st.rerun()
    
    st.markdown(
        "<p style='text-align:center;color:#6b8bb5;"
        "font-size:12px;margin-top:8px'>"
        "Or press the button above to enter the detection pipeline</p>",
        unsafe_allow_html=True
    )
