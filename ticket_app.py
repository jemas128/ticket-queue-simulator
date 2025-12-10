import streamlit as st
import random
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Cinema Queue Live", 
    page_icon="🍿", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED UI/UX STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&family=Poppins:wght@900&display=swap');

    /* --- ANIMATED BACKGROUND --- */
    .stApp {
        background: linear-gradient(-45deg, #FF3CAC, #784BA0, #2B86C5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Nunito', sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- GLASSMORPHISM CONTAINERS --- */
    .glass-panel {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 { font-family: 'Poppins', sans-serif; }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(#FF3CAC, #784BA0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        text-align: center;
        color: #666;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /* --- BUTTONS --- */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-weight: 800;
        border: none;
        transition: transform 0.2s, box-shadow 0.2s;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: white;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        color: white;
    }

    div.stButton > button:active {
        transform: translateY(1px);
    }

    /* Secondary Button (Add) - Cool Blue */
    button[kind="secondary"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    /* Primary Button (Serve) - Sunset Orange */
    button[kind="primary"] {
        background: linear-gradient(135deg, #FF9966 0%, #FF5E62 100%);
        font-size: 1.1rem;
    }

    /* Reset Button override (Targeting the specific button label via Streamlit is hard, 
       so we leave the standard style or rely on secondary) */

    /* --- TICKET STYLES --- */
    .ticket-container {
        display: flex;
        align-items: center;
        background: white;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border-left: 6px solid #e0e0e0;
    }

    /* Golden Ticket Animation */
    @keyframes shine {
        0% { border-color: #FFD700; box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.4); }
        50% { border-color: #FFA500; box-shadow: 0 0 0 10px rgba(255, 215, 0, 0); }
        100% { border-color: #FFD700; box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
    }

    .ticket-active {
        background: linear-gradient(to right, #FFFDE4, #FFFFFF);
        border-left: 8px solid #FFD700;
        animation: shine 2s infinite;
        transform: scale(1.02);
    }

    .t-emoji { font-size: 2.5rem; margin-right: 15px; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.1)); }
    .t-details { flex-grow: 1; }
    .t-id { font-weight: 900; font-size: 1.2rem; color: #333; }
    .t-name { font-size: 1rem; color: #555; }
    .t-meta { font-size: 0.75rem; font-weight: 700; color: #aaa; text-transform: uppercase; letter-spacing: 0.5px; }
    .t-badge {
        background: #eee; color: #555; padding: 4px 8px; 
        border-radius: 6px; font-size: 0.7rem; font-weight: bold;
    }
    .badge-live { background: #FFD700; color: #8a6d00; }

    /* --- STATS BOX --- */
    .stat-box {
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.5);
        border-radius: 15px;
        margin-top: 20px;
    }
    .stat-num { font-size: 3rem; font-weight: 900; color: #784BA0; line-height: 1; }
    .stat-label { font-size: 0.9rem; color: #666; font-weight: 700; letter-spacing: 1px; }

</style>
""", unsafe_allow_html=True)

# --- 3. SESSION LOGIC ---
if 'queue' not in st.session_state: st.session_state.queue = []
if 'history' not in st.session_state: st.session_state.history = []
if 'ticket_id' not in st.session_state: st.session_state.ticket_id = 101

# Expanded Data
NAMES = ["Kai", "Luna", "Milo", "Nova", "Leo", "Mia", "Zane", "Cleo", "Jax", "Ivy", "Finn", "Ruby"]
AVATARS = ["🐼", "🦊", "🦄", "🦁", "🐯", "🐸", "🐙", "🐵", "🐨", "🐷", "🐻", "🐲"]

def enqueue():
    """Add a new customer to the queue"""
    name = random.choice(NAMES)
    new_ticket = {
        "id": st.session_state.ticket_id,
        "name": name,
        "avatar": random.choice(AVATARS),
        "joined": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.queue.append(new_ticket)
    st.session_state.ticket_id += 1

def dequeue():
    """Serve the next customer in the queue"""
    if st.session_state.queue:
        person = st.session_state.queue.pop(0)
        person['served'] = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.insert(0, person)
        if len(st.session_state.history) % 5 == 0:
            st.balloons()
    else:
        st.toast("⚠️ The queue is empty!", icon="📭")

def reset_app():
    """Reset the entire application"""
    st.session_state.queue = []
    st.session_state.history = []
    st.session_state.ticket_id = 101
    st.rerun()

# --- 4. LAYOUT STRUCTURE ---

# Title Area
st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 30px;">
        <div class="hero-title">NEON CINEMA</div>
        <div class="hero-subtitle">Smart Queue Management System</div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.8, 1], gap="large")

# --- COLUMN 1: CONTROLS ---
with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 🎮 Controls")
    
    if st.button("➕ Add Customer", type="secondary"):
        enqueue()
        st.rerun()

    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)  # Spacer

    if st.button("🔥 Serve Next", type="primary"):
        dequeue()
        st.rerun()
    
    st.markdown("---")
    if st.button("↻ Reset System"):
        reset_app()

    # Live Stat
    count = len(st.session_state.queue)
    st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{count}</div>
            <div class="stat-label">WAITING</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMN 2: THE QUEUE ---
with col2:
    if not st.session_state.queue:
        st.markdown("""
        <div class="glass-panel" style="text-align:center; padding: 50px;">
            <div style="font-size: 5rem; opacity: 0.5;">💤</div>
            <h3 style="color:#666;">No one is waiting.</h3>
            <p style="color:#888;">Add a customer to start the queue.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, ticket in enumerate(st.session_state.queue):
            is_first = (i == 0)
            card_class = "ticket-container ticket-active" if is_first else "ticket-container"
            badge_html = '<span class="t-badge badge-live">SERVING NOW</span>' if is_first else f'<span class="t-badge">#{i+1} IN LINE</span>'
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="t-emoji">{ticket['avatar']}</div>
                <div class="t-details">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="t-id">#{ticket['id']}</span>
                        {badge_html}
                    </div>
                    <div class="t-name">{ticket['name']}</div>
                    <div class="t-meta">Joined: {ticket['joined']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- COLUMN 3: RECENTLY SERVED ---
with col3:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### ✅ Served")
    
    if not st.session_state.history:
        st.caption("No customers served yet.")
    
    for item in st.session_state.history[:6]:
        st.markdown(f"""
        <div style="padding: 10px; border-bottom: 1px solid #eee; display:flex; align-items:center;">
            <span style="font-size:1.5rem; margin-right:10px; opacity:0.6;">{item['avatar']}</span>
            <div>
                <div style="font-weight:bold; color:#444;">#{item['id']} {item['name']}</div>
                <div style="font-size:0.7rem; color:#888;">Out: {item['served']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
