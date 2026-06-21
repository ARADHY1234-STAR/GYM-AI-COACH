import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    #MainMenu, header, footer { visibility: hidden; }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    .stApp {
        background:
            linear-gradient(160deg, rgba(0,0,0,0.88) 0%, rgba(8,4,0,0.80) 40%, rgba(0,0,0,0.92) 100%),
            url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1600&q=80') center/cover no-repeat fixed;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    /* glow orbs */
    .orb-tl {
        position: fixed; top: -180px; left: -120px;
        width: 500px; height: 500px; border-radius: 50%;
        background: radial-gradient(circle, rgba(245,120,20,0.22) 0%, transparent 68%);
        pointer-events: none; z-index: 0;
    }
    .orb-br {
        position: fixed; bottom: -120px; right: -100px;
        width: 420px; height: 420px; border-radius: 50%;
        background: radial-gradient(circle, rgba(0,180,255,0.13) 0%, transparent 68%);
        pointer-events: none; z-index: 0;
    }

    /* page centering */
    .page-wrap {
        position: relative; z-index: 1;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px 20px;
    }

    /* badge */
    .badge {
        display: inline-flex; align-items: center; gap: 8px;
        font-size: 10px; font-weight: 700; letter-spacing: 0.2em;
        text-transform: uppercase; color: #f5a623;
        border: 1px solid rgba(245,166,35,0.3);
        background: rgba(245,166,35,0.07);
        padding: 6px 16px; margin-bottom: 24px;
    }
    .badge-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #f5a623; box-shadow: 0 0 8px #f5a623;
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

    /* headline */
    .headline-top {
        font-size: 15px; font-weight: 400; letter-spacing: 0.25em;
        text-transform: uppercase; color: rgba(255,255,255,0.4);
        display: block; text-align: center; margin-bottom: 4px;
    }
    .headline-main {
        font-size: clamp(58px, 9vw, 108px); font-weight: 900;
        line-height: 0.9; letter-spacing: -0.03em;
        color: #fff; display: block; text-align: center;
    }
    .headline-accent {
        font-size: clamp(58px, 9vw, 108px); font-weight: 900;
        line-height: 0.9; letter-spacing: -0.03em;
        background: linear-gradient(135deg, #f5a623 30%, #ff6b35 65%, #00d4ff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; display: block; text-align: center;
    }
    .headline-sub {
        font-size: 14px; color: rgba(255,255,255,0.38);
        margin: 14px auto 0; line-height: 1.7; text-align: center;
    }

    /* stats */
    .stats-row {
        display: flex; gap: 0;
        border: 1px solid rgba(255,255,255,0.07);
        margin: 28px 0 32px;
        overflow: hidden; width: 100%; max-width: 420px;
        background: rgba(255,255,255,0.015);
        backdrop-filter: blur(10px);
    }
    .stat { flex:1; text-align:center; padding:13px 8px; border-right:1px solid rgba(255,255,255,0.07); }
    .stat:last-child { border-right:none; }
    .stat-val { font-size:22px; font-weight:900; color:#f5a623; line-height:1; }
    .stat-unit { font-size:11px; color:#f5a623; }
    .stat-label { font-size:8px; letter-spacing:0.14em; text-transform:uppercase; color:rgba(255,255,255,0.28); margin-top:3px; }

    /* card */
    .card {
        width: 100%; max-width: 420px;
        background: rgba(10,8,5,0.75);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border: 1px solid rgba(245,166,35,0.22);
        padding: 32px 36px 12px;
        box-shadow: 0 0 0 1px rgba(245,166,35,0.05) inset, 0 40px 100px rgba(0,0,0,0.6);
        position: relative; overflow: hidden;
    }
    .card::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background: linear-gradient(90deg, transparent, #f5a623, #00d4ff, transparent);
    }
    .card-eyebrow {
        font-size:9px; font-weight:700; letter-spacing:0.2em;
        text-transform:uppercase; color:#f5a623; margin-bottom:5px;
    }
    .card-title { font-size:20px; font-weight:800; color:#fff; margin-bottom:4px; }
    .card-desc { font-size:12px; color:rgba(255,255,255,0.32); margin-bottom:20px; line-height:1.5; }
    .sep {
        height:1px; margin-bottom:20px;
        background: linear-gradient(90deg, transparent, rgba(245,166,35,0.2), transparent);
    }

    /* foot note */
    .foot-note {
        font-size:10px; color:rgba(255,255,255,0.18);
        text-align:center; letter-spacing:0.07em; padding: 14px 0 28px;
    }

    /* ── INPUT — keep it compact and centered ── */
    /* constrain the column that holds the form */
    section[data-testid="stMain"] > div > div > div[data-testid="stVerticalBlock"]
        > div[data-testid="stVerticalBlock"] {
        max-width: 420px !important;
        margin: 0 auto !important;
    }

    div[data-testid="stTextInput"] label {
        color: rgba(255,255,255,0.55) !important;
        font-size: 10px !important; font-weight: 700 !important;
        letter-spacing: 0.14em !important; text-transform: uppercase !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTextInput"] > div {
        max-width: 348px !important;
    }
    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(245,166,35,0.25) !important;
        border-radius: 0 !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        padding: 14px 16px !important;
        height: 52px !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #f5a623 !important;
        box-shadow: 0 0 0 3px rgba(245,166,35,0.1) !important;
        background: rgba(245,166,35,0.04) !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(255,255,255,0.2) !important; font-size: 13px !important;
    }

    /* button — fixed width, centered */
    div[data-testid="stFormSubmitButton"] {
        display: flex !important;
        justify-content: center !important;
        margin-top: 12px !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #f5a623 0%, #e08a0a 100%) !important;
        color: #000 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 11px !important; font-weight: 900 !important;
        letter-spacing: 0.2em !important; text-transform: uppercase !important;
        border: none !important; border-radius: 0 !important;
        height: 50px !important;
        width: 348px !important;
        box-shadow: 0 8px 32px rgba(245,166,35,0.35) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        cursor: pointer !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 16px 48px rgba(245,166,35,0.5) !important;
    }

    /* hide form border */
    div[data-testid="stForm"] {
        border: none !important; padding: 0 !important; background: transparent !important;
    }

    /* error */
    div[data-testid="stAlert"] {
        background: rgba(220,50,50,0.1) !important;
        border: 1px solid rgba(220,50,50,0.28) !important;
        border-radius: 0 !important; color: #ff7070 !important;
        font-family: 'Inter', sans-serif !important; font-size: 12px !important;
        max-width: 420px !important; margin: 8px auto 0 !important;
    }
    </style>

    <div class="orb-tl"></div>
    <div class="orb-br"></div>

    <div class="page-wrap">
      <div class="badge"><span class="badge-dot"></span>AI-Powered · Real-time · Computer Vision</div>

      <span class="headline-top">Real-time AI</span>
      <span class="headline-main">GYM</span>
      <span class="headline-accent">TRAINER.</span>
      <p class="headline-sub">Your form. Analyzed. Corrected. In milliseconds.</p>

      <div class="stats-row">
        <div class="stat"><div class="stat-val">100<span class="stat-unit">ms</span></div><div class="stat-label">Latency</div></div>
        <div class="stat"><div class="stat-val">5<span class="stat-unit">+</span></div><div class="stat-label">Exercises</div></div>
        <div class="stat"><div class="stat-val">95<span class="stat-unit">%</span></div><div class="stat-label">Accuracy</div></div>
      </div>

      <div class="card">
        <div class="card-eyebrow">// Access Portal</div>
        <div class="card-title">Start Your Session</div>
        <p class="card-desc">Enter a unique username to track your reps, sets &amp; form history.</p>
        <div class="sep"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Form rendered AFTER the card HTML so Streamlit places it below —
    # then CSS pulls it up visually with negative margin and centers it.
    st.markdown("""
    <style>
    /* pull the form block up into the card area */
    section[data-testid="stMain"] > div > div > div[data-testid="stVerticalBlock"]
        > div:last-of-type {
        margin-top: -220px !important;
        position: relative; z-index: 10;
        display: flex; flex-direction: column; align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Username",
                placeholder="e.g. Aradhy Shrivastava",
            )
            password = st.text_input("Password / PIN", type="password", placeholder="Choose a password")
            submit_button = st.form_submit_button("⚡  Begin Training")

        st.markdown('<p class="foot-note">No password needed · Progress saved automatically</p>', unsafe_allow_html=True)

    if submit_button:
        if not username.strip() or not password.strip():
            st.error("Username and password cannot be empty.")
            return False
        user, status = get_or_create_user(username.strip(), password.strip())
        
        if status == "wrong_password":
            st.error("Incorrect password. Please try again.")
            return False
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]
        st.rerun()

    return False
