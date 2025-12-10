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

# --- 2. ADVANCED UI/UX STYLING (Responsive) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&family=Poppins:wght@900&display=swap');

    /* --- ANIMATED BACKGROUND --- */
    .stApp {
        background: linear-gradient(-45deg, #FF3CAC, #784BA0, #2B86C5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
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

    /* --- GLASSMORPHISM CONTAINERS --- */
    .glass-panel {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        height: fit-content;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 { 
        font-family: 'Poppins', sans-serif;
        margin-top: 0 !important;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #FF3CAC, #784BA0, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
        letter-spacing: -1px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #666;
        font-weight: 600;
        margin: 5px 0 15px 0;
        font-size: 1rem;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 0.9rem;
        }
    }

    /* --- BUTTONS --- */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 800;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: white;
        margin: 5px 0;
        font-size: 0.9rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }

    .stButton > button:active {
        transform: translateY(1px);
    }

    /* VIP Button - Royal Purple/Gold */
    button[kind="secondary"]:has(+ div:contains("VIP")) {
        background: linear-gradient(135deg, #8A2BE2 0%, #FFD700 100%);
    }

    /* Regular Add Button - Cool Blue */
    button[kind="secondary"]:not(:has(+ div:contains("VIP"))) {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    /* Serve Button - Sunset Orange */
    button[kind="primary"] {
        background: linear-gradient(135deg, #FF9966 0%, #FF5E62 100%);
    }

    /* Reset Button - Dark */
    .reset-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    /* --- TICKET STYLES --- */
    .ticket-container {
        display: flex;
        align-items: center;
        background: white;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-left: 6px solid #e0e0e0;
    }

    .ticket-vip {
        background: linear-gradient(to right, #FFF8E1, #FFFFFF);
        border-left: 6px solid #FFD700;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }

    /* Golden Ticket Animation */
    @keyframes shine {
        0% { border-color: #FFD700; box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.4); }
        50% { border-color: #FFA500; box-shadow: 0 0 0 8px rgba(255, 215, 0, 0); }
        100% { border-color: #FFD700; box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
    }

    .ticket-active {
        background: linear-gradient(to right, #FFFDE4, #FFFFFF);
        border-left: 6px solid #FFD700;
        animation: shine 2s infinite;
        transform: scale(1.01);
    }

    .t-emoji { 
        font-size: 2rem; 
        margin-right: 12px; 
        filter: drop-shadow(0 2px 2px rgba(0,0,0,0.1));
        min-width: 40px;
        text-align: center;
    }
    .t-details { 
        flex-grow: 1; 
        min-width: 0; /* Prevents overflow */
    }
    .t-id { 
        font-weight: 900; 
        font-size: 1.1rem; 
        color: #333;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .t-name { 
        font-size: 0.95rem; 
        color: #555;
        margin: 2px 0;
    }
    .t-meta { 
        font-size: 0.7rem; 
        font-weight: 700; 
        color: #aaa; 
        text-transform: uppercase; 
        letter-spacing: 0.5px;
    }
    .t-badge {
        background: #f0f0f0; 
        color: #666; 
        padding: 3px 8px; 
        border-radius: 10px; 
        font-size: 0.65rem; 
        font-weight: bold;
        white-space: nowrap;
        display: inline-block;
        margin-left: 5px;
    }
    .badge-live { 
        background: linear-gradient(135deg, #FFD700, #FFA500); 
        color: #8a6d00; 
    }
    .badge-vip {
        background: linear-gradient(135deg, #8A2BE2, #FFD700);
        color: white;
    }

    /* --- STATS BOX --- */
    .stat-box {
        text-align: center;
        padding: 15px;
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        margin: 15px 0;
    }
    .stat-num { 
        font-size: 2.5rem; 
        font-weight: 900; 
        color: #784BA0; 
        line-height: 1;
        margin: 5px 0;
    }
    .stat-label { 
        font-size: 0.8rem; 
        color: #666; 
        font-weight: 700; 
        letter-spacing: 1px;
    }

    /* --- SCROLLABLE CONTAINERS --- */
    .scrollable-container {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 5px;
    }
    
    .scrollable-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .scrollable-container::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb {
        background: rgba(120, 75, 160, 0.5);
        border-radius: 10px;
    }

    /* --- VIP INDICATOR --- */
    .vip-indicator {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #8a6d00;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: bold;
        margin-left: 5px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* --- RESPONSIVE COLUMNS --- */
    @media (max-width: 768px) {
        .st-emotion-cache-1kyxreq {
            flex-direction: column;
        }
        .ticket-container {
            padding: 10px;
        }
        .t-emoji {
            font-size: 1.8rem;
            margin-right: 10px;
        }
        .glass-panel {
            padding: 15px;
        }
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
    else:
        avatar = random.choice(AVATARS)
        vip_badge = ""
    
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
        
        # Celebrate every 3rd customer
        if len(st.session_state.history) % 3 == 0:
            st.balloons()
            st.toast("🎉 Customer served successfully!", icon="✅")
    else:
        st.toast("⚠️ The queue is empty!", icon="📭")

def reset_app():
    """Reset the entire application"""
    st.session_state.queue = []
    st.session_state.history = []
    st.session_state.ticket_id = 101
    st.session_state.vip_count = 0
    st.rerun()

# --- 4. LAYOUT STRUCTURE ---

# Main container for better responsiveness
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title Area
st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 15px 20px; margin-top: 10px;">
        <div class="hero-title">👑 PREMIERE CINEMA</div>
        <div class="hero-subtitle">VIP Queue Management System</div>
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
    st.markdown(f"**📊 Quick Stats**")
    st.markdown(f"""
    - **Total Served:** {served_count}
    - **Next Ticket:** #{st.session_state.ticket_id}
    - **Queue Time:** {(len(st.session_state.queue) * 2)} mins
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMN 2: THE QUEUE ---
with col2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(f"### 🎟️ Live Queue ({len(st.session_state.queue)})")
    
    if not st.session_state.queue:
        st.markdown("""
        <div style="text-align:center; padding: 30px; color: #666;">
            <div style="font-size: 4rem; opacity: 0.5;">💤</div>
            <h3 style="color:#666; margin: 10px 0;">Queue is Empty</h3>
            <p style="color:#888;">Add customers to start managing the queue.</p>
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
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 3px;">
                        <span class="t-id">#{ticket['id']} {ticket['name']} {vip_indicator}</span>
                        {badge_html}
                    </div>
                    <div class="t-meta">Joined: {ticket['joined']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # Close scrollable container
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMN 3: RECENTLY SERVED ---
with col3:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### ✅ Recently Served")
    
    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center; padding: 20px; color: #888;">
            <div style="font-size: 3rem; opacity: 0.3;">🎬</div>
            <p>No customers served yet</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        for item in st.session_state.history[:8]:  # Show last 8 served
            vip_icon = "👑 " if item.get('is_vip', False) else ""
            
            st.markdown(f"""
            <div style="padding: 10px 12px; border-bottom: 1px solid #eee; display:flex; align-items:center; transition: background 0.2s;">
                <span style="font-size:1.4rem; margin-right:10px; opacity:{'0.9' if item.get('is_vip', False) else '0.6'};">{item['avatar']}</span>
                <div style="flex-grow: 1;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-weight:bold; color:#444; font-size: 0.9rem;">{vip_icon}#{item['id']} {item['name']}</div>
                        <div style="font-size:0.7rem; color:#999; background:#f5f5f5; padding:2px 6px; border-radius:8px;">Out</div>
                    </div>
                    <div style="font-size:0.7rem; color:#888; margin-top: 2px;">{item['served']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show more button if there are more served customers
        if len(st.session_state.history) > 8:
            st.caption(f"Showing last 8 of {len(st.session_state.history)} served customers")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 20px; padding: 10px; color: rgba(255,255,255,0.7); font-size: 0.8rem;">
    🎬 Cinema Queue System v2.0 • VIP Priority Enabled • Auto-refresh on action
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container
