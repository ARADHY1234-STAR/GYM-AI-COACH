import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    # ── inject CSS ──
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* hide streamlit chrome */
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* full-page background */
    .stApp {
        background:
            linear-gradient(135deg, rgba(0,0,0,0.82) 0%, rgba(10,5,0,0.75) 50%, rgba(0,0,0,0.88) 100%),
            url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1600&q=80') center/cover no-repeat fixed;
        font-family: 'Inter', sans-serif;
    }

    /* ambient glow orbs */
    .stApp::before {
        content: '';
        position: fixed;
        width: 600px; height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(245,120,20,0.18) 0%, transparent 70%);
        top: -150px; left: -100px;
        pointer-events: none;
        z-index: 0;
    }
    .stApp::after {
        content: '';
        position: fixed;
        width: 500px; height: 500px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0,180,255,0.1) 0%, transparent 70%);
        bottom: -100px; right: -80px;
        pointer-events: none;
        z-index: 0;
    }

    /* hero text block */
    .hero-block {
        position: relative;
        z-index: 1;
        padding: 80px 60px 0 60px;
        max-width: 1100px;
        margin: 0 auto;
    }
    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #f5a623;
        border-left: 3px solid #f5a623;
        padding-left: 10px;
        margin-bottom: 20px;
    }
    .hero-headline {
        font-size: clamp(52px, 7vw, 100px);
        font-weight: 900;
        line-height: 0.95;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin: 0 0 12px 0;
    }
    .hero-headline span {
        color: #f5a623;
        display: block;
    }
    .hero-sub {
        font-size: 17px;
        color: rgba(255,255,255,0.55);
        max-width: 440px;
        line-height: 1.7;
        margin-top: 18px;
    }

    /* login card */
    .login-card {
        position: relative;
        z-index: 1;
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(245,166,35,0.2);
        border-radius: 2px;
        padding: 40px 44px 44px;
        max-width: 480px;
        margin: 52px auto 0 auto;
        box-shadow:
            0 0 0 1px rgba(245,166,35,0.06) inset,
            0 32px 80px rgba(0,0,0,0.55),
            0 0 80px rgba(245,120,20,0.06);
    }
    .card-tag {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #f5a623;
        margin-bottom: 8px;
    }
    .card-title {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    .card-desc {
        font-size: 13px;
        color: rgba(255,255,255,0.4);
        margin-bottom: 28px;
        line-height: 1.6;
    }
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(245,166,35,0.25), transparent);
        margin: 0 0 24px 0;
    }

    /* override streamlit input */
    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(245,166,35,0.25) !important;
        border-radius: 2px !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        transition: border-color 0.25s, box-shadow 0.25s !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #f5a623 !important;
        box-shadow: 0 0 0 3px rgba(245,166,35,0.12) !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(255,255,255,0.28) !important;
    }
    div[data-testid="stTextInput"] label {
        color: rgba(255,255,255,0.6) !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* submit button */
    div[data-testid="stForm"] .stFormSubmitButton button,
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #f5a623, #e08a0a) !important;
        color: #000 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 2px !important;
        padding: 14px 0 !important;
        width: 100% !important;
        margin-top: 8px !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        box-shadow: 0 8px 30px rgba(245,166,35,0.3) !important;
        cursor: pointer !important;
    }
    div[data-testid="stForm"] .stFormSubmitButton button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 40px rgba(245,166,35,0.45) !important;
    }

    /* stats strip */
    .stats-strip {
        display: flex;
        justify-content: center;
        gap: 0;
        max-width: 480px;
        margin: 24px auto 0;
        border: 1px solid rgba(255,255,255,0.07);
        overflow: hidden;
    }
    .stat {
        flex: 1;
        text-align: center;
        padding: 16px 12px;
        background: rgba(255,255,255,0.02);
        border-right: 1px solid rgba(255,255,255,0.07);
    }
    .stat:last-child { border-right: none; }
    .stat-val {
        font-size: 22px;
        font-weight: 900;
        color: #f5a623;
        line-height: 1;
    }
    .stat-label {
        font-size: 9px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.35);
        margin-top: 4px;
    }

    /* error override */
    div[data-testid="stAlert"] {
        background: rgba(220,50,50,0.12) !important;
        border: 1px solid rgba(220,50,50,0.3) !important;
        border-radius: 2px !important;
        color: #ff6b6b !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero text ──
    st.markdown("""
    <div class="hero-block">
        <div class="hero-eyebrow">⬡ &nbsp;AI-Powered · Real-time · Computer Vision</div>
        <div class="hero-headline">
            TRAIN<br>
            <span>SMARTER.</span>
        </div>
        <p class="hero-sub">
            Your form. Analyzed. Corrected. In milliseconds.<br>
            Computer vision that watches every rep and tells you exactly what to fix.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Login card wrapper (top) ──
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="card-tag">// Access Portal</div>
        <div class="card-title">Start Your Session</div>
        <p class="card-desc">Enter a unique username to track your reps, sets, and form history.</p>
        <div class="divider"></div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Username",
            placeholder="e.g. Aradhy Shrivastava",
            label_visibility="visible"
        )
        submit_button = st.form_submit_button("→  Begin Training")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Stats strip ──
    st.markdown("""
    <div class="stats-strip">
        <div class="stat">
            <div class="stat-val">100<span style="font-size:13px;color:#f5a623">ms</span></div>
            <div class="stat-label">Latency</div>
        </div>
        <div class="stat">
            <div class="stat-val">5<span style="font-size:13px;color:#f5a623">+</span></div>
            <div class="stat-label">Exercises</div>
        </div>
        <div class="stat">
            <div class="stat-val">95<span style="font-size:13px;color:#f5a623">%</span></div>
            <div class="stat-label">Accuracy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if submit_button:
        if not username:
            st.error("Username cannot be empty.")
            return False

        user = get_or_create_user(username)
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]
        st.rerun()

    return False
