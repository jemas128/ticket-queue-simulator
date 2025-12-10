import streamlit as st
import random
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Cinema Queue Live", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED UI/UX STYLING (Gradient Edition) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&family=Poppins:wght@900&display=swap');

    /* --- ANIMATED GRADIENT BACKGROUND --- */
    .stApp {
        background: linear-gradient(-45deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #f5576c 75%, 
            #ff9a9e 100%);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        font-family: 'Nunito', sans-serif;
        min-height: 100vh;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- RESPONSIVE CONTAINERS --- */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 10px;
    }

    @media (max-width: 768px) {
        .main-container {
            padding: 5px;
        }
    }

    /* --- GLASSMORPHISM CONTAINERS WITH GRADIENTS --- */
    .glass-panel {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.88) 100%);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4);
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }

    .glass-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, 
            #667eea 0%, 
            #764ba2 33%, 
            #f093fb 66%, 
            #f5576c 100%);
        z-index: 1;
    }

    /* --- GRADIENT TYPOGRAPHY --- */
    h1, h2, h3 { 
        font-family: 'Poppins', sans-serif;
        margin-top: 0 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #f5576c 75%, 
            #ff9a9e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        text-align: center;
        letter-spacing: -1px;
        line-height: 1.2;
        position: relative;
        padding-bottom: 10px;
    }

    .hero-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 25%;
        width: 50%;
        height: 3px;
        background: linear-gradient(90deg, 
            #667eea 0%, 
            #764ba2 50%, 
            #f093fb 100%);
        border-radius: 2px;
    }
    
    .hero-subtitle {
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin: 10px 0 20px 0;
        font-size: 1.1rem;
        letter-spacing: 1px;
    }

    /* --- GRADIENT BUTTONS --- */
    .stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 55px;
        font-weight: 800;
        border: none;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: white;
        margin: 8px 0;
        font-size: 0.95rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.3), 
            transparent);
        transition: 0.5s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }

    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }

    /* Regular Add Button - Ocean Blue Gradient */
    button[kind="secondary"]:has(+ div:contains("Add")) {
        background: linear-gradient(135deg, 
            #4facfe 0%, 
            #00f2fe 100%);
        border: 2px solid rgba(79, 172, 254, 0.3);
    }

    /* VIP Button - Royal Purple/Gold Gradient */
    button[kind="secondary"]:has(+ div:contains("VIP")) {
        background: linear-gradient(135deg, 
            #8A2BE2 0%, 
            #FFD700 50%, 
            #FF8C00 100%);
        border: 2px solid rgba(255, 215, 0, 0.3);
        animation: vipGlow 2s infinite alternate;
    }

    @keyframes vipGlow {
        0% { box-shadow: 0 8px 25px rgba(138, 43, 226, 0.3); }
        100% { box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5); }
    }

    /* Serve Button - Sunset Gradient */
    button[kind="primary"] {
        background: linear-gradient(135deg, 
            #FF9966 0%, 
            #FF5E62 50%, 
            #FF2E63 100%);
        border: 2px solid rgba(255, 94, 98, 0.3);
        font-size: 1rem;
    }

    /* Reset Button - Deep Purple Gradient */
    button[kind="secondary"]:has(+ div:contains("Reset")) {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 100%);
        border: 2px solid rgba(118, 75, 162, 0.3);
    }

    /* --- GRADIENT TICKET STYLES --- */
    .ticket-container {
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.9) 100%);
        border-radius: 18px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        transition: all 0.4s ease;
        border-left: 8px solid #e0e0e0;
        position: relative;
        overflow: hidden;
    }

    .ticket-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.1) 100%);
        z-index: 0;
    }

    .ticket-vip {
        background: linear-gradient(135deg, 
            rgba(255, 248, 225, 0.95) 0%, 
            rgba(255, 255, 255, 0.9) 100%);
        border-left: 8px solid #FFD700;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.2);
    }

    /* Golden Ticket Animation */
    @keyframes shine {
        0% { 
            border-color: #FFD700; 
            box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.3),
                        inset 0 0 20px rgba(255, 215, 0, 0.1);
        }
        50% { 
            border-color: #FFA500; 
            box-shadow: 0 0 0 10px rgba(255, 215, 0, 0),
                        inset 0 0 30px rgba(255, 215, 0, 0.2);
        }
        100% { 
            border-color: #FFD700; 
            box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.3),
                        inset 0 0 20px rgba(255, 215, 0, 0.1);
        }
    }

    .ticket-active {
        background: linear-gradient(135deg, 
            rgba(255, 253, 228, 0.95) 0%, 
            rgba(255, 255, 255, 0.9) 100%);
        border-left: 8px solid #FFD700;
        animation: shine 2s infinite;
        transform: scale(1.02);
    }

    .t-emoji { 
        font-size: 2.2rem; 
        margin-right: 15px; 
        filter: drop-shadow(0 3px 5px rgba(0,0,0,0.15));
        min-width: 45px;
        text-align: center;
        z-index: 1;
        position: relative;
    }
    
    .t-details { 
        flex-grow: 1; 
        min-width: 0;
        z-index: 1;
        position: relative;
    }
    
    .t-id { 
        font-weight: 900; 
        font-size: 1.15rem; 
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .t-name { 
        font-size: 1rem; 
        color: #555;
        margin: 3px 0;
        font-weight: 600;
    }
    
    .t-meta { 
        font-size: 0.75rem; 
        font-weight: 800; 
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase; 
        letter-spacing: 1px;
    }
    
    .t-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; 
        padding: 5px 12px; 
        border-radius: 20px; 
        font-size: 0.7rem; 
        font-weight: bold;
        white-space: nowrap;
        display: inline-block;
        margin-left: 8px;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .badge-live { 
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #8a6d00; 
        animation: badgePulse 1.5s infinite;
    }

    @keyframes badgePulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .badge-vip {
        background: linear-gradient(135deg, #8A2BE2 0%, #FFD700 100%);
        color: white;
        border: 1px solid rgba(255, 215, 0, 0.5);
    }

    /* --- GRADIENT STATS BOX --- */
    .stat-box {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.9) 0%, 
            rgba(255, 255, 255, 0.7) 100%);
        border-radius: 20px;
        margin: 20px 0;
        border: 2px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }

    .stat-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }

    .stat-num { 
        font-size: 2.8rem; 
        font-weight: 900; 
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin: 10px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stat-label { 
        font-size: 0.85rem; 
        color: #764ba2; 
        font-weight: 800; 
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* --- GRADIENT SCROLLABLE CONTAINERS --- */
    .scrollable-container {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 8px;
        margin-top: 10px;
    }
    
    .scrollable-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .scrollable-container::-webkit-scrollbar-track {
        background: linear-gradient(180deg, 
            rgba(255,255,255,0.1) 0%,
            rgba(255,255,255,0.3) 100%);
        border-radius: 10px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.3);
    }

    /* --- GRADIENT VIP INDICATOR --- */
    .vip-indicator {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #8a6d00;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: bold;
        margin-left: 8px;
        animation: vipPulse 2s infinite;
        border: 1px solid rgba(255, 215, 0, 0.5);
        box-shadow: 0 3px 10px rgba(255, 215, 0, 0.3);
    }

    @keyframes vipPulse {
        0% { transform: scale(1); box-shadow: 0 3px 10px rgba(255, 215, 0, 0.3); }
        50% { transform: scale(1.08); box-shadow: 0 5px 15px rgba(255, 215, 0, 0.5); }
        100% { transform: scale(1); box-shadow: 0 3px 10px rgba(255, 215, 0, 0.3); }
    }

    /* --- GRADIENT SERVED ITEMS --- */
    .served-item {
        padding: 12px 15px;
        border-bottom: 1px solid rgba(255,255,255,0.3);
        display: flex;
        align-items: center;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.9) 0%,
            rgba(255,255,255,0.7) 100%);
        border-radius: 12px;
        margin-bottom: 8px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }

    .served-item:hover {
        transform: translateX(5px);
        background: linear-gradient(135deg, 
            rgba(255,255,255,1) 0%,
            rgba(255,255,255,0.8) 100%);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    /* --- RESPONSIVE COLUMNS --- */
    @media (max-width: 768px) {
        .st-emotion-cache-1kyxreq {
            flex-direction: column;
        }
        .ticket-container {
            padding: 12px;
        }
        .t-emoji {
            font-size: 1.8rem;
            margin-right: 10px;
        }
        .glass-panel {
            padding: 20px;
        }
        .hero-title {
            font-size: 2.2rem;
        }
    }

    /* --- GRADIENT DIVIDERS --- */
    hr {
        height: 3px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #667eea 20%, 
            #764ba2 50%, 
            #f093fb 80%, 
            transparent 100%);
        border: none;
        margin: 25px 0;
        border-radius: 2px;
    }

    /* --- GRADIENT CAPTIONS --- */
    .st-caption {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }

    /* --- GRADIENT FOOTER --- */
    .gradient-footer {
        text-align: center;
        margin-top: 30px;
        padding: 15px;
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.2) 0%,
            rgba(255,255,255,0.1) 100%);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* --- QUICK STATS GRADIENT --- */
    .quick-stats {
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.8) 0%,
            rgba(255,255,255,0.6) 100%);
        padding: 15px;
        border-radius: 15px;
        margin-top: 15px;
        border: 1px solid rgba(255,255,255,0.3);
    }

    .quick-stats strong {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION LOGIC ---
if 'queue' not in st.session_state: 
    st.session_state.queue = []
if 'history' not in st.session_state: 
    st.session_state.history = []
if 'ticket_id' not in st.session_state: 
    st.session_state.ticket_id = 101
if 'vip_count' not in st.session_state:
    st.session_state.vip_count = 0

# Expanded Data
NAMES = ["Kai", "Luna", "Milo", "Nova", "Leo", "Mia", "Zane", "Cleo", "Jax", "Ivy", "Finn", "Ruby"]
AVATARS = ["🐼", "🦊", "🦄", "🦁", "🐯", "🐸", "🐙", "🐵", "🐨", "🐷", "🐻", "🐲"]
VIP_AVATARS = ["👑", "⭐", "🌟", "💎", "🎩", "💍"]

def enqueue(is_vip=False):
    """Add a new customer to the queue"""
    name = random.choice(NAMES)
    
    if is_vip:
        avatar = random.choice(VIP_AVATARS)
        st.session_state.vip_count += 1
        vip_badge = "VIP"
        st.toast("👑 VIP Customer Added!", icon="🌟")
    else:
        avatar = random.choice(AVATARS)
        vip_badge = ""
        st.toast("🎬 Customer Added to Queue", icon="✅")
    
    new_ticket = {
        "id": st.session_state.ticket_id,
        "name": name,
        "avatar": avatar,
        "joined": datetime.now().strftime("%H:%M:%S"),
        "is_vip": is_vip,
        "vip_badge": vip_badge
    }
    
    if is_vip:
        # VIP customers go to the front (after other VIPs)
        vip_position = 0
        for i, ticket in enumerate(st.session_state.queue):
            if not ticket['is_vip']:
                vip_position = i
                break
            else:
                vip_position = i + 1
        st.session_state.queue.insert(vip_position, new_ticket)
    else:
        st.session_state.queue.append(new_ticket)
    
    st.session_state.ticket_id += 1

def dequeue():
    """Serve the next customer in the queue"""
    if st.session_state.queue:
        person = st.session_state.queue.pop(0)
        person['served'] = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.insert(0, person)
        
        if person['is_vip']:
            st.session_state.vip_count -= 1
            st.toast(f"👑 VIP #{person['id']} served!", icon="🎉")
            st.balloons()
        else:
            # Celebrate every 3rd regular customer
            if len(st.session_state.history) % 3 == 0:
                st.toast(f"🎬 #{person['id']} served!", icon="🎬")
                st.balloons()
    else:
        st.toast("⚠️ Queue is empty! Add customers first.", icon="📭")

def reset_app():
    """Reset the entire application"""
    st.session_state.queue = []
    st.session_state.history = []
    st.session_state.ticket_id = 101
    st.session_state.vip_count = 0
    st.toast("🔄 System Reset Complete", icon="🔄")
    st.rerun()

# --- 4. LAYOUT STRUCTURE ---

# Main container for better responsiveness
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title Area
st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 20px; margin-top: 5px;">
        <div class="hero-title">🌈 PREMIERE CINEMA</div>
        <div class="hero-subtitle">Gradient Queue Management System</div>
    </div>
""", unsafe_allow_html=True)

# Create columns with responsive ratios
col1, col2, col3 = st.columns([1, 1.5, 1], gap="medium")

# --- COLUMN 1: CONTROLS ---
with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 🎮 Controls")
    
    # Button Container
    button_col1, button_col2 = st.columns(2, gap="small")
    
    with button_col1:
        if st.button("➕ Add", type="secondary", use_container_width=True):
            enqueue(is_vip=False)
            st.rerun()
    
    with button_col2:
        if st.button("👑 VIP", type="secondary", use_container_width=True):
            enqueue(is_vip=True)
            st.rerun()
    
    # Serve Button
    if st.button("🎬 Serve Next", type="primary", use_container_width=True):
        dequeue()
        st.rerun()
    
    st.markdown("---")
    
    # Reset Button
    if st.button("🔄 Reset System", type="secondary", use_container_width=True):
        reset_app()
    
    # Stats
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        waiting_count = len(st.session_state.queue)
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-num">{waiting_count}</div>
                <div class="stat-label">WAITING</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        vip_count = st.session_state.vip_count
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-num">{vip_count}</div>
                <div class="stat-label">VIP</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("---")
    served_count = len(st.session_state.history)
    st.markdown("""
        <div class="quick-stats">
            <strong>📊 Quick Stats</strong>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding: 10px;">
    - **Total Served:** <strong>{served_count}</strong><br>
    - **Next Ticket:** <strong>#{st.session_state.ticket_id}</strong><br>
    - **Est. Wait:** <strong>{len(st.session_state.queue) * 2} mins</strong>
    </div>
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMN 2: THE QUEUE ---
with col2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(f"### 🎟️ Live Queue ({len(st.session_state.queue)})")
    
    if not st.session_state.queue:
        st.markdown("""
        <div style="text-align:center; padding: 40px; color: #666;">
            <div style="font-size: 4rem; opacity: 0.5; margin-bottom: 20px;">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;">💤</div>
            </div>
            <h3 style="color:#764ba2; margin: 10px 0;">Queue is Empty</h3>
            <p style="color:#888; font-weight: 500;">Add customers to start the magic!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        for i, ticket in enumerate(st.session_state.queue):
            is_first = (i == 0)
            
            # Determine card class
            if is_first:
                card_class = "ticket-container ticket-active"
            elif ticket['is_vip']:
                card_class = "ticket-container ticket-vip"
            else:
                card_class = "ticket-container"
            
            # Determine badge
            if is_first:
                badge_html = '<span class="t-badge badge-live">NOW SERVING</span>'
            elif ticket['is_vip']:
                badge_html = '<span class="t-badge badge-vip">VIP PRIORITY</span>'
            else:
                badge_html = f'<span class="t-badge">#{i+1} IN LINE</span>'
            
            # VIP indicator
            vip_indicator = '<span class="vip-indicator">VIP</span>' if ticket['is_vip'] else ''
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="t-emoji">{ticket['avatar']}</div>
                <div class="t-details">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 5px;">
                        <span class="t-id">#{ticket['id']} {ticket['name']} {vip_indicator}</span>
                        {badge_html}
                    </div>
                    <div class="t-meta">Joined: {ticket['joined']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMN 3: RECENTLY SERVED ---
with col3:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### ✅ Recently Served")
    
    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center; padding: 30px; color: #888;">
            <div style="font-size: 3.5rem; opacity: 0.3; margin-bottom: 15px;">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2);
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;">🎬</div>
            </div>
            <p style="font-weight: 600; color: #764ba2;">No customers served yet</p>
            <p style="font-size: 0.9rem; color: #999;">Serve customers to see history</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        for item in st.session_state.history[:8]:
            vip_icon = "👑 " if item.get('is_vip', False) else ""
            served_style = "background: linear-gradient(90deg, #FFD700, #FFA500);" if item.get('is_vip', False) else "background: linear-gradient(90deg, #667eea, #764ba2);"
            
            st.markdown(f"""
            <div class="served-item">
                <span style="font-size:1.5rem; margin-right:12px; 
                    {'filter: drop-shadow(0 2px 3px rgba(255, 215, 0, 0.5));' if item.get('is_vip', False) else ''}">
                    {item['avatar']}
                </span>
                <div style="flex-grow: 1;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-weight:bold; color:#444; font-size: 0.9rem;">
                            {vip_icon}#{item['id']} {item['name']}
                        </div>
                        <div style="font-size:0.7rem; color:white; padding:3px 8px; border-radius:10px; {served_style}">
                            Served
                        </div>
                    </div>
                    <div style="font-size:0.75rem; color:#888; margin-top: 3px;">
                        {item['served']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if len(st.session_state.history) > 8:
            st.caption(f"Showing last 8 of {len(st.session_state.history)} served customers")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Gradient Footer
st.markdown("""
<div class="gradient-footer">
    <div style="font-size: 1.2rem; font-weight: 800; margin-bottom: 5px;">
        <span style="background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
                     -webkit-background-clip: text;
                     -webkit-text-fill-color: transparent;">
            🎬 Cinema Queue System v3.0
        </span>
    </div>
    <div style="font-size: 0.85rem; color: rgba(255,255,255,0.8);">
        VIP Priority • Gradient UI • Auto-refresh • Live Updates
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
