import streamlit as st
import requests


st.set_page_config(
    page_title="CarValue AI – Know Your Car's True Worth",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)


if "fuel_type" not in st.session_state:
    st.session_state.fuel_type = "Petrol"
if "transmission" not in st.session_state:
    st.session_state.transmission = "Manual"
if "seller_type" not in st.session_state:
    st.session_state.seller_type = "Individual"


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=Orbitron:wght@400;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #F7F8FC;
    color: #111827;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── ANIMATED GRID BACKGROUND ── */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(255,107,0,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,107,0,0.035) 1px, transparent 1px);
    background-size: 64px 64px;
    animation: gridDrift 18s linear infinite;
    pointer-events: none; z-index: 0;
}
@keyframes gridDrift {
    0%   { background-position: 0 0, 0 0; }
    100% { background-position: 64px 64px, 64px 64px; }
}

/* ── HERO ── */
.hero-wrapper {
    background: linear-gradient(135deg, #04080F 0%, #0A1628 55%, #141A2E 100%);
    padding: 70px 40px 60px;
    position: relative; overflow: hidden;
    display: flex; align-items: center; gap: 48px;
    min-height: 580px;
}
#hero-canvas {
    position: absolute; inset: 0; width: 100%; height: 100%;
    z-index: 1; pointer-events: none;
}

/* speed lines */
.sl {
    position: absolute; left: 0; width: 100%; height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,107,0,0.7) 50%, transparent 100%);
    animation: speedLine linear infinite;
    pointer-events: none; z-index: 2;
}
@keyframes speedLine {
    0%   { transform: translateX(-100%); opacity: 0; }
    15%  { opacity: 1; }
    85%  { opacity: 1; }
    100% { transform: translateX(120%); opacity: 0; }
}
/* floating dots */
.fp {
    position: absolute; border-radius: 50%;
    background: rgba(255,183,3,0.7);
    animation: floatUp linear infinite;
    pointer-events: none; z-index: 2;
}
@keyframes floatUp {
    0%   { transform: translateY(0) scale(0); opacity: 0; }
    10%  { opacity: 0.8; }
    90%  { opacity: 0.6; }
    100% { transform: translateY(-520px) scale(1.5); opacity: 0; }
}

.hero-left  { flex: 1; min-width: 300px; z-index: 3; position: relative; }
.hero-right { flex: 1; display: flex; justify-content: center; align-items: center; z-index: 3; position: relative; }

.hero-right img {
    width: 100%; max-width: 540px; border-radius: 22px; object-fit: cover;
    filter: drop-shadow(0 24px 64px rgba(255,107,0,0.3));
    animation: heroFloat 7s ease-in-out infinite;
    position: relative; z-index: 2;
}
@keyframes heroFloat {
    0%,100% { transform: translateY(0px) rotate(0deg); filter: drop-shadow(0 24px 64px rgba(255,107,0,0.28)); }
    50%      { transform: translateY(-14px) rotate(0.5deg); filter: drop-shadow(0 36px 80px rgba(255,107,0,0.45)); }
}
/* holographic shimmer over image */
.hero-holo {
    position: absolute; inset: 0; border-radius: 22px; pointer-events: none; z-index: 3;
    background: linear-gradient(125deg, transparent 20%, rgba(255,183,3,0.08) 50%, transparent 80%);
    background-size: 200% 200%;
    animation: holoMove 4s ease-in-out infinite;
}
@keyframes holoMove {
    0%,100% { background-position: 0% 0%; }
    50%      { background-position: 100% 100%; }
}

.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,107,0,0.12); border: 1px solid rgba(255,107,0,0.4);
    color: #FF6B00; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    padding: 7px 18px; border-radius: 100px; margin-bottom: 22px;
    animation: badgePulse 3s ease-in-out infinite;
}
.badge-dot {
    width: 6px; height: 6px; background: #FF6B00; border-radius: 50%;
    animation: dotBlink 1.2s ease-in-out infinite;
}
@keyframes badgePulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(255,107,0,0); }
    50%      { box-shadow: 0 0 0 10px rgba(255,107,0,0.08); }
}
@keyframes dotBlink {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.3; transform: scale(0.6); }
}

.hero-headline {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 3.6vw, 3.3rem);
    font-weight: 800; color: #FFFFFF; line-height: 1.12; margin-bottom: 18px;
}
.shimmer-text {
    background: linear-gradient(90deg, #FF6B00 0%, #FFB703 40%, #FF6B00 80%, #FFB703 100%);
    background-size: 300% 100%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: shimmerFlow 3.5s linear infinite;
    display: inline-block;
}
@keyframes shimmerFlow {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
.hero-sub {
    font-size: 1rem; color: rgba(255,255,255,0.57);
    max-width: 470px; line-height: 1.75; margin-bottom: 34px;
}

/* STAT COUNTERS */
.hero-stats { display: flex; gap: 34px; flex-wrap: wrap; }
.stat-item { position: relative; }
.stat-item::after {
    content: '';
    position: absolute; bottom: -4px; left: 0; width: 0; height: 2px;
    background: linear-gradient(90deg, #FF6B00, #FFB703);
    animation: statUnderline 3s ease-in-out infinite;
}
@keyframes statUnderline {
    0%,100% { width: 0%; left: 0%; }
    40%,60%  { width: 100%; left: 0%; }
}
.hero-stat-num {
    font-family: 'Orbitron', sans-serif; font-size: 1.75rem;
    font-weight: 900; color: #FF6B00; line-height: 1; display: block;
    text-shadow: 0 0 24px rgba(255,107,0,0.55);
}
.hero-stat-label {
    font-size: 0.73rem; color: rgba(255,255,255,0.42);
    text-transform: uppercase; letter-spacing: 1.2px;
}

/* ── HOW IT WORKS ── */
.how-strip {
    background: #FFFFFF; border-bottom: 1px solid #E5E7EB;
    padding: 28px 40px; display: flex; align-items: center;
    gap: 0; justify-content: center; flex-wrap: wrap;
    position: relative; overflow: hidden; z-index: 1;
}
.how-strip::after {
    content: '';
    position: absolute; bottom: 0; left: -100%; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #FF6B00, #FFB703, transparent);
    animation: scanLine 3.5s ease-in-out infinite;
}
@keyframes scanLine { 0% { left: -100%; } 100% { left: 100%; } }

.how-step  { display: flex; align-items: center; gap: 12px; }
.how-num   {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #FF6B00, #FFB703); border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 0.9rem; color: #fff;
    animation: numRing 2.2s ease-out infinite;
}
.how-step:nth-child(3) .how-num { animation-delay: 0.6s; }
.how-step:nth-child(5) .how-num { animation-delay: 1.2s; }
@keyframes numRing {
    0%,100% { box-shadow: 0 0 0 0 rgba(255,107,0,0); }
    40%      { box-shadow: 0 0 0 10px rgba(255,107,0,0.08); }
    70%      { box-shadow: 0 0 0 14px rgba(255,107,0,0); }
}
.how-text  { font-size: 0.86rem; font-weight: 600; color: #374151; line-height: 1.3; }
.how-text small { display: block; font-weight: 400; color: #9CA3AF; font-size: 0.74rem; }
.how-arrow {
    font-size: 1rem; color: #D1D5DB; margin: 0 22px;
    animation: arrowBounce 1.4s ease-in-out infinite;
}
@keyframes arrowBounce {
    0%,100% { transform: translateX(0); color: #D1D5DB; }
    50%      { transform: translateX(6px); color: #FF6B00; }
}

/* ── FORM SECTION ── */
.form-section { background: #F7F8FC; padding: 56px 40px; position: relative; z-index: 1; }
.section-label { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700; color: #111827; margin-bottom: 4px; }
.section-sub   { font-size: 0.90rem; color: #6B7280; margin-bottom: 28px; }

/* ── CARDS — SPOTLIGHT ── */
.input-card {
    background: #FFFFFF; border-radius: 18px; padding: 26px 24px 22px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 14px rgba(0,0,0,0.05);
    margin-bottom: 18px;
    will-change: transform;
    transition: box-shadow 0.35s ease, border-color 0.35s ease;
    position: relative; overflow: hidden;
}
/* spotlight on card */
.input-card::before {
    content: '';
    position: absolute; inset: 0; border-radius: 18px;
    background: radial-gradient(400px circle at var(--mx,50%) var(--my,50%), rgba(255,107,0,0.06) 0%, transparent 55%);
    opacity: 0; transition: opacity 0.3s;
    pointer-events: none; z-index: 0;
}
.input-card:hover::before { opacity: 1; }
.input-card:hover {
    border-color: rgba(255,107,0,0.28);
    box-shadow: 0 10px 40px rgba(255,107,0,0.13), 0 2px 14px rgba(0,0,0,0.05);
}
/* bottom circuit trace */
.input-card::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #FF6B00, #FFB703, transparent);
    transform: scaleX(0); transform-origin: left; transition: transform 0.5s ease;
}
.input-card:hover::after { transform: scaleX(1); }

.card-title {
    font-family: 'Syne', sans-serif; font-size: 0.82rem; font-weight: 700;
    color: #6B7280; text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 18px; display: flex; align-items: center; gap: 8px; position: relative; z-index: 1;
}
.card-icon {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #FF6B00, #FFB703); border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center; font-size: 0.88rem;
}

.toggle-label {
    font-size: 0.80rem; font-weight: 600; color: #6B7280;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; margin-top: 4px;
    position: relative; z-index: 1;
}
.tip-text { font-size: 0.74rem; color: #9CA3AF; margin-top: 3px; font-style: italic; position: relative; z-index: 1; }

/* Streamlit overrides */
.stSelectbox label, .stNumberInput label, .stTextInput label, .stSlider label {
    font-family: 'DM Sans', sans-serif !important; font-size: 0.80rem !important;
    font-weight: 600 !important; color: #6B7280 !important;
    text-transform: uppercase !important; letter-spacing: 1px !important;
    position: relative; z-index: 1;
}
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #F9FAFB !important; border: 1.5px solid #E5E7EB !important;
    border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important; color: #111827 !important; font-weight: 500 !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #FF6B00 !important;
    box-shadow: 0 0 0 3px rgba(255,107,0,0.12) !important;
}
.stSlider > div > div > div > div { background: linear-gradient(90deg, #FF6B00, #FFB703) !important; }
.stSlider > div > div > div > div > div {
    background: #FF6B00 !important; border: 2px solid #fff !important;
    box-shadow: 0 2px 8px rgba(255,107,0,0.45) !important;
}

/* Toggle buttons */
div[data-testid="column"] .stButton > button {
    font-family: 'DM Sans', sans-serif !important; font-size: 0.86rem !important;
    font-weight: 600 !important; border-radius: 100px !important; padding: 9px 18px !important;
    border: 1.5px solid #E5E7EB !important; background: #F9FAFB !important;
    color: #374151 !important; transition: all 0.18s ease !important;
    box-shadow: none !important; width: 100% !important;
    position: relative !important; overflow: hidden !important;
}
div[data-testid="column"] .stButton > button:hover {
    border-color: #FF6B00 !important; color: #FF6B00 !important;
    background: rgba(255,107,0,0.06) !important;
    box-shadow: 0 0 0 4px rgba(255,107,0,0.08) !important;
}

/* CTA */
.cta-wrap .stButton > button {
    font-family: 'Syne', sans-serif !important; font-size: 1.08rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #FF6B00 0%, #FF8C42 50%, #FF6B00 100%) !important;
    background-size: 200% 100% !important;
    color: #fff !important; border: none !important; border-radius: 14px !important;
    padding: 18px 40px !important; width: 100% !important;
    box-shadow: 0 8px 28px rgba(255,107,0,0.40) !important;
    transition: all 0.25s ease !important;
    position: relative !important; overflow: hidden !important;
    animation: ctaBreath 3s ease-in-out infinite !important;
}
@keyframes ctaBreath {
    0%,100% { box-shadow: 0 8px 28px rgba(255,107,0,0.38); }
    50%      { box-shadow: 0 8px 44px rgba(255,107,0,0.65), 0 0 0 10px rgba(255,107,0,0.08); }
}
.cta-wrap .stButton > button:hover {
    background-position: 100% 0 !important;
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 16px 44px rgba(255,107,0,0.55) !important;
}

/* ── RESULT ── */
.res-card {
    background: linear-gradient(135deg, #06090F 0%, #0C1629 100%);
    border-radius: 22px; padding: 42px 34px;
    border: 1px solid rgba(255,107,0,0.22);
    box-shadow: 0 24px 64px rgba(0,0,0,0.35), 0 0 50px rgba(255,107,0,0.1), inset 0 1px 0 rgba(255,255,255,0.05);
    margin-top: 26px; text-align: center;
    animation: resultPop 0.85s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    position: relative; overflow: hidden;
}
@keyframes resultPop {
    from { opacity: 0; transform: scale(0.88) translateY(24px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}
/* scanline overlay */
.res-card::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(255,107,0,0.012) 3px, rgba(255,107,0,0.012) 4px);
    animation: scanlines 10s linear infinite;
    pointer-events: none;
}
@keyframes scanlines { 0% { background-position: 0 0; } 100% { background-position: 0 -100px; } }
/* corner glows */
.res-card::after {
    content: '';
    position: absolute; inset: 0; border-radius: 22px;
    background:
        radial-gradient(80px at 0% 0%, rgba(255,107,0,0.14), transparent),
        radial-gradient(80px at 100% 100%, rgba(255,183,3,0.09), transparent);
    pointer-events: none;
}

.res-tag {
    display: inline-block; background: rgba(255,107,0,0.15);
    border: 1px solid rgba(255,107,0,0.35); color: #FF8C42;
    font-size: 0.70rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; padding: 5px 14px; border-radius: 100px; margin-bottom: 18px;
    animation: tagPing 2s ease-in-out infinite;
    position: relative; z-index: 1;
}
@keyframes tagPing {
    0%,100% { box-shadow: 0 0 0 0 rgba(255,107,0,0); }
    50%      { box-shadow: 0 0 0 8px rgba(255,107,0,0.08); }
}
.res-label {
    font-size: 0.85rem; font-weight: 500; color: rgba(255,255,255,0.48);
    text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;
    position: relative; z-index: 1;
}
.res-price {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(2.8rem, 5vw, 4rem); font-weight: 900;
    background: linear-gradient(90deg, #FF6B00, #FFB703, #FF6B00);
    background-size: 200% 100%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1; margin-bottom: 8px;
    animation: priceShimmer 2.5s linear infinite, pricePop 0.7s cubic-bezier(0.34,1.56,0.64,1) 0.3s both;
    position: relative; z-index: 1;
}
@keyframes priceShimmer { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
@keyframes pricePop {
    from { opacity: 0; transform: scale(0.7); }
    to   { opacity: 1; transform: scale(1); }
}
.res-rupees { font-size: 0.95rem; color: rgba(255,255,255,0.38); margin-bottom: 28px; position: relative; z-index: 1; }

.range-box {
    background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 18px 22px; margin-bottom: 28px;
    position: relative; z-index: 1;
}
.range-title {
    font-size: 0.72rem; font-weight: 600; color: rgba(255,255,255,0.32);
    text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;
}
.range-row { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.range-low, .range-high {
    font-family: 'Orbitron', sans-serif; font-size: 1rem;
    font-weight: 700; color: rgba(255,255,255,0.82); white-space: nowrap;
}
.range-bar { flex: 1; height: 7px; background: rgba(255,255,255,0.08); border-radius: 6px; overflow: hidden; }
.range-fill {
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #FF6B00, #FFB703); border-radius: 6px;
    animation: rangeFill 1.6s cubic-bezier(0.4,0,0.2,1) 0.7s forwards;
    box-shadow: 0 0 10px rgba(255,107,0,0.5);
}
@keyframes rangeFill { from { width: 0%; } to { width: 100%; } }

.metrics-row {
    display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;
    border-top: 1px solid rgba(255,255,255,0.055); padding-top: 22px;
    position: relative; z-index: 1;
}
.m-box { text-align: center; }
.m-val { font-family: 'Orbitron', sans-serif; font-size: 0.95rem; font-weight: 700; color: #FFFFFF; display: block; }
.m-key { font-size: 0.67rem; color: rgba(255,255,255,0.32); text-transform: uppercase; letter-spacing: 1px; }

/* CHIPS */
.chip-row { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 20px; }
.chip {
    flex: 1; min-width: 130px; border-radius: 15px; padding: 18px 18px; text-align: center;
    opacity: 0; animation: chipRise 0.65s cubic-bezier(0.34,1.56,0.64,1) forwards;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.chip:hover { transform: translateY(-4px); }
.chip:nth-child(1) { animation-delay: 0.25s; }
.chip:nth-child(2) { animation-delay: 0.38s; }
.chip:nth-child(3) { animation-delay: 0.51s; }
.chip:nth-child(4) { animation-delay: 0.64s; }
@keyframes chipRise {
    from { opacity: 0; transform: translateY(24px) scale(0.88); }
    to   { opacity: 1; transform: translateY(0)  scale(1); }
}
.chip-v { font-family: 'Orbitron', sans-serif; font-size: 1.3rem; font-weight: 900; display: block; }
.chip-k { font-size: 0.70rem; text-transform: uppercase; letter-spacing: 1px; }

/* TRUST */
.trust-section { background: #FFFFFF; padding: 44px 40px; border-top: 1px solid #E5E7EB; position: relative; z-index: 1; }
.trust-h { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #111827; text-align: center; margin-bottom: 28px; }
.trust-grid { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
.trust-card {
    display: flex; align-items: flex-start; gap: 14px; background: #F9FAFB;
    border: 1px solid #E5E7EB; border-radius: 14px; padding: 18px 20px; max-width: 270px;
    transition: all 0.3s ease;
}
.trust-card:hover {
    border-color: rgba(255,107,0,0.3);
    box-shadow: 0 10px 36px rgba(255,107,0,0.11);
    transform: translateY(-5px);
}
.t-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #FF6B00, #FFB703); border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; flex-shrink: 0;
    transition: transform 0.3s ease;
}
.trust-card:hover .t-icon { transform: rotate(12deg) scale(1.1); }
.t-title { font-family: 'Syne', sans-serif; font-size: 0.88rem; font-weight: 700; color: #111827; margin-bottom: 4px; }
.t-desc  { font-size: 0.78rem; color: #6B7280; line-height: 1.55; }

/* FOOTER */
.footer-bar { background: #06090F; padding: 24px 40px; text-align: center; position: relative; overflow: hidden; z-index: 1; }
.footer-bar::before {
    content: '';
    position: absolute; top: 0; left: -100%; right: 0; height: 1.5px;
    background: linear-gradient(90deg, transparent, #FF6B00, #FFB703, transparent);
    animation: scanLine 5s ease-in-out infinite;
}
.footer-bar p { font-size: 0.78rem; color: rgba(255,255,255,0.28); }
.footer-bar span { color: #FF6B00; }

hr { border: none; border-top: 1px solid #E5E7EB; margin: 0; }

/* page entrance */
.stApp > div { animation: pageIn 0.7s ease-out both; }
@keyframes pageIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero-wrapper" id="heroWrap">
  <canvas id="hero-canvas"></canvas>

  <!-- speed lines -->
  <div class="sl" style="top:18%; animation-duration:2.2s; animation-delay:0s;"></div>
  <div class="sl" style="top:35%; animation-duration:3.1s; animation-delay:0.7s;"></div>
  <div class="sl" style="top:52%; animation-duration:2.6s; animation-delay:1.4s;"></div>
  <div class="sl" style="top:71%; animation-duration:3.4s; animation-delay:0.3s;"></div>
  <div class="sl" style="top:86%; animation-duration:2.0s; animation-delay:1.1s;"></div>

  <!-- floating particles -->
  <div class="fp" style="left:8%;  width:4px; height:4px; bottom:10%; animation-duration:6s; animation-delay:0s;"></div>
  <div class="fp" style="left:18%; width:3px; height:3px; bottom:5%;  animation-duration:8s; animation-delay:1.5s;"></div>
  <div class="fp" style="left:28%; width:5px; height:5px; bottom:15%; animation-duration:7s; animation-delay:0.8s;"></div>
  <div class="fp" style="left:45%; width:3px; height:3px; bottom:8%;  animation-duration:9s; animation-delay:2.2s;"></div>
  <div class="fp" style="left:62%; width:4px; height:4px; bottom:12%; animation-duration:6.5s;animation-delay:0.4s;"></div>
  <div class="fp" style="left:75%; width:3px; height:3px; bottom:6%;  animation-duration:7.5s;animation-delay:1.8s;"></div>
  <div class="fp" style="left:88%; width:5px; height:5px; bottom:18%; animation-duration:8.5s;animation-delay:0.9s;"></div>

  <div class="hero-left">
    <div class="hero-badge"><span class="badge-dot"></span>&#129504; AI-Powered Valuation Engine</div>
    <h1 class="hero-headline">
      Know Your Car's<br>
      <span class="shimmer-text">True Resale Value</span><br>
      in Seconds.
    </h1>
    <p class="hero-sub">
      Our XGBoost ML model, trained on thousands of real transactions,
      gives you an instant data-backed estimate — no guesswork, no haggling.
    </p>
    <div class="hero-stats">
      <div class="stat-item">
        <span class="hero-stat-num" data-count="82" data-suffix="%">82%</span>
        <span class="hero-stat-label">Accuracy</span>
      </div>
      <div class="stat-item">
        <span class="hero-stat-num">&lt;2 sec</span>
        <span class="hero-stat-label">Response Time</span>
      </div>
      <div class="stat-item">
        <span class="hero-stat-num" data-count="50000" data-suffix="K+">50K+</span>
        <span class="hero-stat-label">Valuations Done</span>
      </div>
    </div>
  </div>

  <div class="hero-right">
    <div style="position:relative; display:inline-block;">
      <img
        src="https://images.unsplash.com/photo-1617469767053-d3b523a0b982?w=800&q=80&auto=format&fit=crop"
        alt="Luxury Car"
        onerror="this.src='https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80&auto=format&fit=crop'"
      />
      <div class="hero-holo"></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HOW IT WORKS
# ============================================================
st.markdown("""
<div class="how-strip">
  <div class="  "><div class="how-num">1</div>
    <div class="how-text">Enter Details <small>Fill in your car specs</small></div></div>
  <span class="how-arrow">&#8594;</span>
  <div class="how-step"><div class="how-num">2</div>
    <div class="how-text">AI Analyzes Market <small>XGBoost runs instantly</small></div></div>
  <span class="how-arrow">&#8594;</span>
  <div class="how-step"><div class="how-num">3</div>
    <div class="how-text">Get Instant Price <small>With realistic range</small></div></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FORM SECTION
# ============================================================
st.markdown('<div class="form-section">', unsafe_allow_html=True)
_, center_col, _ = st.columns([1, 2.8, 1])

with center_col:

    st.markdown('<p class="section-label">Vehicle Details</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Fill in the details below for an accurate AI-powered valuation.</p>', unsafe_allow_html=True)

    # Card 1
    st.markdown('<div class="input-card"><div class="card-title"><span class="card-icon">&#128663;</span>&nbsp;Vehicle Identity</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        car_name = st.text_input("CAR MODEL", placeholder="e.g., Swift, Nexon, i20")
    with cb:
        year = st.selectbox("MANUFACTURING YEAR", options=list(range(2026, 1999, -1)), index=8)
    present_price = st.number_input(
        "CURRENT SHOWROOM PRICE (₹ Lakhs)",
        min_value=0.5, max_value=500.0, value=7.5, step=0.5,
        help="Price of this exact model if bought brand new from showroom today"
    )
    st.markdown('<p class="tip-text">💡 Check manufacturer website for latest ex-showroom price</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Card 2
    st.markdown('<div class="input-card"><div class="card-title"><span class="card-icon">&#9881;&#65039;</span>&nbsp;Engine & Powertrain</div>', unsafe_allow_html=True)
    st.markdown('<p class="toggle-label">Fuel Type</p>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        if st.button(("✅ " if st.session_state.fuel_type == "Petrol" else "") + "⛽ Petrol", key="bp", use_container_width=True):
            st.session_state.fuel_type = "Petrol"; st.rerun()
    with f2:
        if st.button(("✅ " if st.session_state.fuel_type == "Diesel" else "") + "🛢️ Diesel", key="bd", use_container_width=True):
            st.session_state.fuel_type = "Diesel"; st.rerun()
    with f3:
        if st.button(("✅ " if st.session_state.fuel_type == "CNG" else "") + "🌿 CNG", key="bc", use_container_width=True):
            st.session_state.fuel_type = "CNG"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="toggle-label">Transmission</p>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1:
        if st.button(("✅ " if st.session_state.transmission == "Manual" else "") + "🔧 Manual", key="bm", use_container_width=True):
            st.session_state.transmission = "Manual"; st.rerun()
    with t2:
        if st.button(("✅ " if st.session_state.transmission == "Automatic" else "") + "🤖 Automatic", key="ba", use_container_width=True):
            st.session_state.transmission = "Automatic"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="toggle-label">Seller Type</p>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        if st.button(("✅ " if st.session_state.seller_type == "Individual" else "") + "👤 Individual", key="bi", use_container_width=True):
            st.session_state.seller_type = "Individual"; st.rerun()
    with s2:
        if st.button(("✅ " if st.session_state.seller_type == "Dealer" else "") + "🏢 Dealer", key="bde", use_container_width=True):
            st.session_state.seller_type = "Dealer"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Card 3
    st.markdown('<div class="input-card"><div class="card-title"><span class="card-icon">&#128202;</span>&nbsp;Usage & Condition</div>', unsafe_allow_html=True)
    kms_driven = st.slider("KILOMETERS DRIVEN", min_value=0, max_value=300000, value=45000, step=1000, format="%d km")
    st.markdown(f'<p class="tip-text">📍 Selected: <strong>{kms_driven:,} km</strong></p>', unsafe_allow_html=True)
    owner = st.selectbox(
        "PREVIOUS OWNERS",
        options=[0, 1, 2, 3],
        format_func=lambda x: ["0 — First Owner", "1 — Second Owner", "2 — Third Owner", "3 — Fourth Owner+"][x]
    )
    st.markdown('</div>', unsafe_allow_html=True)

    car_age = 2026 - int(year)
    st.markdown(f"""
    <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;
                padding:13px 18px;margin-bottom:18px;display:flex;align-items:center;gap:12px;">
        <span style="font-size:1.1rem;">📅</span>
        <span style="font-family:'DM Sans',sans-serif;font-size:0.86rem;color:#15803D;font-weight:500;">
            Vehicle is <strong>{car_age} year{'s' if car_age != 1 else ''} old</strong>
            — auto-factored into the AI model.
        </span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
    predict_btn = st.button("🔍  Calculate Selling Price", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── RESULT ──────────────────────────────────────────────
    if predict_btn:
        if not car_name.strip():
            st.warning("⚠️ Please enter your car model name first.")
        else:
            payload = {
                "Car_name": car_name.strip().lower(),
                "Year": int(year),
                "Present_Price": float(present_price),
                "Kms_Driven": int(kms_driven),
                "Fuel_Type": st.session_state.fuel_type,
                "Seller_Type": st.session_state.seller_type,
                "Transmission": st.session_state.transmission,
                "Owner": int(owner)
            }
            with st.spinner("🧠 AI is analyzing your vehicle..."):
                try:
                    resp = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=30)
                    if resp.status_code == 200:
                        predicted = float(resp.json()["prediction_price"])
                        low  = predicted * 0.91
                        high = predicted * 1.09

                        def fmt(v):
                            return f"₹{v/100:.2f} Cr" if v >= 100 else f"₹{v:.2f} L"

                        def full_rs(v):
                            r = v * 100_000
                            return f"₹{r/1_00_00_000:.2f} Crore" if r >= 1_00_00_000 else f"₹{r/1_00_000:.2f} Lakh"

                        dep = round(((present_price - predicted) / present_price) * 100, 1) if present_price > 0 else 0

                        st.markdown(f"""
                        <div class="res-card">
                          <div class="res-tag">✨ AI Valuation Complete</div>
                          <p class="res-label">Estimated Resale Value</p>
                          <div class="res-price">{fmt(predicted)}</div>
                          <p class="res-rupees">{full_rs(predicted)}</p>
                          <div class="range-box">
                            <p class="range-title">Realistic Market Range (±9%)</p>
                            <div class="range-row">
                              <span class="range-low">{fmt(low)}</span>
                              <div class="range-bar"><div class="range-fill"></div></div>
                              <span class="range-high">{fmt(high)}</span>
                            </div>
                          </div>
                          <div class="metrics-row">
                            <div class="m-box"><span class="m-val">{car_name.title()}</span><span class="m-key">Model</span></div>
                            <div class="m-box"><span class="m-val">{year}</span><span class="m-key">Year</span></div>
                            <div class="m-box"><span class="m-val">{kms_driven:,} km</span><span class="m-key">Odometer</span></div>
                            <div class="m-box"><span class="m-val">{st.session_state.fuel_type}</span><span class="m-key">Fuel</span></div>
                            <div class="m-box"><span class="m-val">{st.session_state.transmission}</span><span class="m-key">Gearbox</span></div>
                          </div>
                        </div>
                        <div class="chip-row">
                          <div class="chip" style="background:#FFF7ED;border:1px solid #FED7AA;">
                            <span class="chip-v" style="color:#EA580C;">{dep}%</span>
                            <span class="chip-k" style="color:#9A3412;">Depreciation</span>
                          </div>
                          <div class="chip" style="background:#F0FDF4;border:1px solid #BBF7D0;">
                            <span class="chip-v" style="color:#16A34A;">{car_age} yr</span>
                            <span class="chip-k" style="color:#166534;">Vehicle Age</span>
                          </div>
                          <div class="chip" style="background:#EFF6FF;border:1px solid #BFDBFE;">
                            <span class="chip-v" style="color:#2563EB;">{owner}</span>
                            <span class="chip-k" style="color:#1E40AF;">Prev Owners</span>
                          </div>
                          <div class="chip" style="background:#FDF4FF;border:1px solid #E9D5FF;">
                            <span class="chip-v" style="color:#9333EA;">{st.session_state.seller_type}</span>
                            <span class="chip-k" style="color:#6B21A8;">Seller</span>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"Server error {resp.status_code}. Is FastAPI running?")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to the valuation engine.")
                    st.code("uvicorn main:app --reload", language="bash")
                    st.info("Run this in Terminal 1, then try again.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TRUST
# ============================================================
st.markdown("""
<div class="trust-section">
  <p class="trust-h">Why Trust CarValue AI?</p>
  <div class="trust-grid">
    <div class="trust-card">
      <div class="t-icon">🧠</div>
      <div><div class="t-title">XGBoost ML Model</div>
      <div class="t-desc">Trained on thousands of real listings with gradient boosting for maximum accuracy.</div></div>
    </div>
    <div class="trust-card">
      <div class="t-icon">📊</div>
      <div><div class="t-title">Realistic Price Range</div>
      <div class="t-desc">We show a ±9% band — because real markets have variance, not a single rigid number.</div></div>
    </div>
    <div class="trust-card">
      <div class="t-icon">⚡</div>
      <div><div class="t-title">Instant Results</div>
      <div class="t-desc">No sign-up. No waiting. Get your valuation under 2 seconds, completely free.</div></div>
    </div>
    <div class="trust-card">
      <div class="t-icon">🔒</div>
      <div><div class="t-title">Privacy First</div>
      <div class="t-desc">We don't store your data. All computations are server-side and discarded immediately.</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer-bar">
  <p>Built with <span>♥</span> using Python &middot; FastAPI &middot; XGBoost &middot; Streamlit
  &nbsp;|&nbsp; CarValue AI &mdash; <span>Not affiliated with Cars24, CarDekho or Spinny</span></p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# JAVASCRIPT — injected LAST so DOM is ready
# ============================================================
st.markdown("""
<script>
(function() {
  if (window.__cvInitialized) { _reAttach(); return; }
  window.__cvInitialized = true;

  /* ── 1. CARD SPOTLIGHT + 3D TILT ─────────────────── */
  function initCards() {
    document.querySelectorAll('.input-card').forEach(function(card) {
      card.addEventListener('mousemove', function(e) {
        var r   = card.getBoundingClientRect();
        var x   = e.clientX - r.left;
        var y   = e.clientY - r.top;
        var cx  = r.width  / 2;
        var cy  = r.height / 2;
        var rotX = ((y - cy) / cy) * -6;
        var rotY = ((x - cx) / cx) *  6;
        card.style.transform      = 'perspective(900px) rotateX('+rotX+'deg) rotateY('+rotY+'deg) scale(1.012)';
        card.style.setProperty('--mx', x + 'px');
        card.style.setProperty('--my', y + 'px');
      });
      card.addEventListener('mouseleave', function() {
        card.style.transform = 'perspective(900px) rotateX(0) rotateY(0) scale(1)';
      });
    });
  }
  initCards();

  /* ── 2. MAGNETIC CTA BUTTON ──────────────────────── */
  function initMagnetic() {
    var btns = document.querySelectorAll('.cta-wrap button');
    btns.forEach(function(btn) {
      btn.addEventListener('mousemove', function(e) {
        var r  = btn.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width  / 2);
        var dy = e.clientY - (r.top  + r.height / 2);
        btn.style.transform = 'translateY(-3px) translate('+dx*0.18+'px,'+dy*0.18+'px) scale(1.01)';
      });
      btn.addEventListener('mouseleave', function() {
        btn.style.transform = '';
      });
      /* ripple */
      btn.addEventListener('click', function(e) {
        var rip = document.createElement('span');
        var r   = btn.getBoundingClientRect();
        rip.style.cssText = 'position:absolute;border-radius:50%;background:rgba(255,255,255,0.28);'
          + 'width:0;height:0;left:'+(e.clientX-r.left)+'px;top:'+(e.clientY-r.top)+'px;'
          + 'transform:translate(-50%,-50%);pointer-events:none;animation:ripOut 0.7s ease-out forwards;';
        btn.appendChild(rip);
        setTimeout(function() { rip.remove(); }, 700);
      });
    });
  }
  initMagnetic();

  /* ripple keyframe */
  if (!document.getElementById('ripStyle')) {
    var s = document.createElement('style');
    s.id = 'ripStyle';
    s.textContent = '@keyframes ripOut{to{width:320px;height:320px;opacity:0}}';
    document.head.appendChild(s);
  }

  /* ── 3. THREE.JS HERO CANVAS ─────────────────────── */
  function loadThree() {
    if (window.THREE) { initThree(); return; }
    var sc = document.createElement('script');
    sc.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
    sc.onload = initThree;
    document.head.appendChild(sc);
  }

  function initThree() {
    var canvas = document.getElementById('hero-canvas');
    if (!canvas) return;
    if (canvas._threeInit) {
      canvas._threeRenderer && canvas._threeRenderer.dispose();
    }
    canvas._threeInit = true;

    var W = canvas.offsetWidth  || canvas.parentElement.offsetWidth  || 800;
    var H = canvas.offsetHeight || canvas.parentElement.offsetHeight || 560;

    var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(W, H);
    canvas._threeRenderer = renderer;

    var scene  = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(60, W / H, 0.1, 100);
    camera.position.set(0, 0, 5.5);

    var knotGeo  = new THREE.TorusKnotGeometry(1.1, 0.34, 160, 22, 2, 3);
    var knotMat  = new THREE.MeshBasicMaterial({ color: 0xFF6B00, wireframe: true, transparent: true, opacity: 0.18 });
    var knotMesh = new THREE.Mesh(knotGeo, knotMat);
    knotMesh.position.set(2.8, 0.2, -1.2);
    scene.add(knotMesh);

    var ringGeo  = new THREE.TorusGeometry(2.2, 0.012, 8, 80);
    var ringMat  = new THREE.MeshBasicMaterial({ color: 0xFFB703, transparent: true, opacity: 0.25 });
    var ringMesh = new THREE.Mesh(ringGeo, ringMat);
    ringMesh.rotation.x = Math.PI / 4;
    ringMesh.position.set(2.8, 0, -1.5);
    scene.add(ringMesh);

    var N    = 340;
    var pos  = new Float32Array(N * 3);
    var vel  = [];
    for (var i = 0; i < N; i++) {
      pos[i*3]   = (Math.random() - 0.5) * 14;
      pos[i*3+1] = (Math.random() - 0.5) * 8;
      pos[i*3+2] = (Math.random() - 0.5) * 5 - 2;
      vel.push({ x: (Math.random()-0.5)*0.003, y: (Math.random()-0.5)*0.003 });
    }
    var ptGeo  = new THREE.BufferGeometry();
    ptGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    var ptMat  = new THREE.PointsMaterial({ color: 0xFF8C42, size: 0.055, transparent: true, opacity: 0.7 });
    var points = new THREE.Points(ptGeo, ptMat);
    scene.add(points);

    var linePos  = [];
    var maxDist  = 1.8;
    for (var i = 0; i < N; i++) {
      for (var j = i+1; j < N; j++) {
        var dx = pos[i*3]   - pos[j*3];
        var dy = pos[i*3+1] - pos[j*3+1];
        var dz = pos[i*3+2] - pos[j*3+2];
        if (Math.sqrt(dx*dx + dy*dy + dz*dz) < maxDist) {
          linePos.push(pos[i*3], pos[i*3+1], pos[i*3+2]);
          linePos.push(pos[j*3], pos[j*3+1], pos[j*3+2]);
        }
      }
    }
    var lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(linePos), 3));
    var lineMat = new THREE.LineBasicMaterial({ color: 0xFF6B00, transparent: true, opacity: 0.07 });
    scene.add(new THREE.LineSegments(lineGeo, lineMat));

    var targetRotX = 0, targetRotY = 0;
    var wrap = canvas.parentElement;
    wrap.addEventListener('mousemove', function(e) {
      var r  = wrap.getBoundingClientRect();
      targetRotY = ((e.clientX - r.left) / r.width  - 0.5) * 0.5;
      targetRotX = ((e.clientY - r.top)  / r.height - 0.5) * 0.3;
    });

    var t = 0;
    var alive = true;
    canvas._threeStop = function() { alive = false; renderer.dispose(); };

    (function animate() {
      if (!alive) return;
      requestAnimationFrame(animate);
      t += 0.006;

      knotMesh.rotation.x += 0.003;
      knotMesh.rotation.y += 0.005;
      ringMesh.rotation.z += 0.004;
      ringMesh.rotation.x  = Math.PI/4 + Math.sin(t*0.4)*0.2;

      for (var i = 0; i < N; i++) {
        pos[i*3]   += vel[i].x;
        pos[i*3+1] += vel[i].y;
        if (Math.abs(pos[i*3])   > 7) vel[i].x *= -1;
        if (Math.abs(pos[i*3+1]) > 4) vel[i].y *= -1;
      }
      ptGeo.attributes.position.needsUpdate = true;

      scene.rotation.y += (targetRotY - scene.rotation.y) * 0.04;
      scene.rotation.x += (targetRotX - scene.rotation.x) * 0.04;

      var sc = 1 + Math.sin(t * 0.8) * 0.035;
      knotMesh.scale.set(sc, sc, sc);

      renderer.render(scene, camera);
    })();

    var resObs = new ResizeObserver(function() {
      var nW = canvas.offsetWidth  || W;
      var nH = canvas.offsetHeight || H;
      camera.aspect = nW / nH;
      camera.updateProjectionMatrix();
      renderer.setSize(nW, nH);
    });
    resObs.observe(canvas.parentElement);
  }

  loadThree();

  /* ── 4. RE-ATTACH after Streamlit rerun ──────────── */
  function _reAttach() {
    setTimeout(function() { initCards(); initMagnetic(); }, 200);
  }

})();
</script>
""", unsafe_allow_html=True)