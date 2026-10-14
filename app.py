import html
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("Type a name, customize its look, and add a looping animation.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=100, value=48)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=0.4, max_value=3.0, value=1.4, step=0.1,
                      help="Lower values move more slowly; higher values move faster.")

themes = {
    "Light": ("#f8fafc", "#172033", "#dbeafe"),
    "Dark": ("#0b1020", "#f8fafc", "#1e293b"),
    "Ocean": ("#063b55", "#f0fdff", "#0e7490"),
    "Sunset": ("#4a1942", "#fff7ed", "#ea580c"),
    "Forest": ("#15352a", "#f0fdf4", "#166534"),
    "Lavender": ("#eee7ff", "#35245c", "#c4b5fd"),
    "Midnight": ("#111827", "#fef3c7", "#7c3aed"),
}
bg, text, accent = themes[background]
safe_name = html.escape(name.strip() or "Hello World")
safe_font = json.dumps(font_family)
safe_effect = json.dumps(effect)
safe_mode = json.dumps(name_mode)
safe_name_js = json.dumps(name.strip() or "Hello World")
safe_speed = float(speed)

# The animation runs in the embedded browser with CSS/JavaScript, so it loops
# smoothly without repeatedly rerunning the entire Streamlit script.
html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ font-family: {safe_font}; }}
  .stage {{
    position: relative; width: 100%; height: 590px; overflow: hidden;
    border-radius: 18px; background: {bg}; color: {text};
    border: 1px solid rgba(127,127,127,.25);
    isolation: isolate;
  }}
  .glow {{
    position: absolute; inset: -20%; z-index: -2; opacity: .45;
    background: radial-gradient(circle at 20% 25%, {accent}, transparent 35%),
                radial-gradient(circle at 80% 75%, {accent}, transparent 32%);
    animation: glow 8s ease-in-out infinite alternate;
  }}
  @keyframes glow {{ from {{ transform: scale(1) rotate(0deg); }} to {{ transform: scale(1.2) rotate(8deg); }} }}
  #particles {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }}
  .particle {{ position: absolute; top: -12%; left: var(--x); font-size: var(--size);
    opacity: var(--opacity); animation: fall var(--duration) linear var(--delay) infinite;
    transform: translate3d(0,0,0); will-change: transform; }}
  @keyframes fall {{
    0% {{ transform: translate3d(0,-15%,0) rotate(0deg); }}
    100% {{ transform: translate3d(var(--drift),720px,0) rotate(var(--spin)); }}
  }}
  .name-wrap {{
    position: absolute; z-index: 3; inset: 0; display: flex; align-items: center;
    justify-content: center; padding: 30px; overflow: hidden;
  }}
  #name {{ font-family: {safe_font}; font-size: {font_size}px; font-weight: 800;
    line-height: 1.18; text-align: center; overflow-wrap: anywhere;
    text-shadow: 0 3px 14px rgba(0,0,0,.18); max-width: 100%; }}
  .ticker {{ white-space: nowrap; max-width: none !important; animation: ticker 12s linear infinite; }}
  @keyframes ticker {{ from {{ transform: translateX(110%); }} to {{ transform: translateX(-110%); }} }}
  .repeated {{ display: flex; flex-direction: column; gap: 14px; align-items: center; }}
  .repeat-line {{ opacity: .92; }}
  .label {{ position: absolute; z-index: 4; bottom: 14px; left: 18px; font: 12px/1.4 Arial,sans-serif; opacity: .72; }}
  .wind-line {{ position: absolute; left: -35%; width: 38%; height: 2px; border-radius: 10px;
    background: currentColor; opacity: .45; animation: gust var(--duration) ease-in-out var(--delay) infinite; }}
  @keyframes gust {{ 0% {{ transform: translateX(0) scaleX(.5); opacity: 0; }} 30% {{ opacity: .5; }}
    100% {{ transform: translateX(390%) scaleX(1.5); opacity: 0; }} }}
  .tornado {{ position: absolute; left: 50%; top: 50%; font-size: 130px; opacity: .36;
    animation: spin var(--duration) linear infinite; transform-origin: center; }}
  @keyframes spin {{ from {{ transform: translate(-50%,-50%) rotate(0deg) scale(.85); }}
    to {{ transform: translate(-50%,-50%) rotate(360deg) scale(1.08); }} }}
  @media (prefers-reduced-motion: reduce) {{
    .glow, .particle, .ticker, .wind-line, .tornado {{ animation-duration: 20s !important; }}
  }}
</style>
</head>
<body>
<div class="stage" id="stage">
  <div class="glow"></div>
  <div id="particles" aria-hidden="true"></div>
  <div id="wind" aria-hidden="true"></div>
  <div id="tornado" aria-hidden="true"></div>
  <div class="name-wrap"><div id="name">{safe_name}</div></div>
  <div class="label">HELLO WORLD MOTION LAB · {html.escape(effect)} effect</div>
</div>
<script>
(() => {{
  const effect = {safe_effect};
  const mode = {safe_mode};
  const nameText = {safe_name_js};
  const speed = {safe_speed};
  const particles = document.getElementById('particles');
  const nameEl = document.getElementById('name');
  const wind = document.getElementById('wind');
  const tornado = document.getElementById('tornado');
  const symbols = {{
    'Rain': ['💧', '💦'], 'Snow': ['❄️', '❅', '❆'], 'Hail': ['🧊', '●'],
    'Confetti': ['🎉', '🎊', '🟣', '🟡', '🟢', '🔵', '🟥']
  }};
  nameEl.textContent = nameText;
  if (mode === 'Ticker Tape') {{
    nameEl.classList.add('ticker');
    nameEl.style.whiteSpace = 'nowrap';
  }} else if (mode === 'Repeated') {{
    nameEl.textContent = '';
    nameEl.classList.add('repeated');
    for (let i = 0; i < 6; i++) {{
      const line = document.createElement('div');
      line.className = 'repeat-line';
      line.textContent = nameText;
      nameEl.appendChild(line);
    }}
  }}
  if (effect in symbols) {{
    const count = effect === 'Confetti' ? 65 : 45;
    for (let i = 0; i < count; i++) {{
      const p = document.createElement('span');
      p.className = 'particle';
      p.textContent = symbols[effect][Math.floor(Math.random() * symbols[effect].length)];
      p.style.setProperty('--x', Math.random() * 100 + '%');
      p.style.setProperty('--size', (effect === 'Hail' ? 9 + Math.random()*13 : 12 + Math.random()*16) + 'px');
      p.style.setProperty('--opacity', (0.45 + Math.random()*.5).toFixed(2));
      p.style.setProperty('--duration', (Math.max(1.4, 7 + Math.random()*8) / speed) + 's');
      p.style.setProperty('--delay', (-Math.random()*12) + 's');
      p.style.setProperty('--drift', ((Math.random()-.5)*150) + 'px');
      p.style.setProperty('--spin', (Math.random()*900-450) + 'deg');
      particles.appendChild(p);
    }}
  }} else if (effect === 'Wind Gust') {{
    for (let i = 0; i < 14; i++) {{
      const line = document.createElement('span');
      line.className = 'wind-line';
      line.style.top = (8 + Math.random()*82) + '%';
      line.style.setProperty('--duration', (Math.max(1, 4 + Math.random()*4) / speed) + 's');
      line.style.setProperty('--delay', (-Math.random()*6) + 's');
      wind.appendChild(line);
    }}
    nameEl.animate(
      [{{ transform: 'translateX(-8px) rotate(-1deg)' }}, {{ transform: 'translateX(8px) rotate(1deg)' }},
       {{ transform: 'translateX(-8px) rotate(-1deg)' }}],
      {{ duration: 1500 / speed, iterations: Infinity, easing: 'ease-in-out' }}
    );
  }} else if (effect === 'Tornado') {{
    tornado.textContent = '🌪️';
    tornado.className = 'tornado';
    tornado.style.setProperty('--duration', (5 / speed) + 's');
  }}
}})();
</script>
</body>
</html>
"""

components.html(html_doc, height=610, scrolling=False)

st.caption("Tip: change the controls in the sidebar to experiment with fonts, backgrounds, and motion effects.")
