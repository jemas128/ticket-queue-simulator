import streamlit as st
import random
import os
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Neon Cinema Queue", 
    page_icon="🍿", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THEMES & STATE ---
THEMES = {
    "neon": { 
        "name": "Neon City", 
        "bg": "linear-gradient(-45deg, #FF3CAC, #784BA0, #2B86C5, #23d5ab)",
        "accent": "#00f2fe",
        "button_bg": "#FF3CAC",
        "button_hover": "#FF0066"
    },
    "sunset": { 
        "name": "Sunset Strip", 
        "bg": "linear-gradient(-45deg, #FF512F, #DD2476, #F09819, #FF512F)",
        "accent": "#FF512F",
        "button_bg": "#FF512F",
        "button_hover": "#DD2476"
    },
    "ocean": { 
        "name": "Cyber Ocean", 
        "bg": "linear-gradient(-45deg, #00c6ff, #0072ff, #1cb5e0, #000046)",
        "accent": "#00c6ff",
        "button_bg": "#0072ff",
        "button_hover": "#1cb5e0"
    },
    "forest": { 
        "name": "Toxic Jungle", 
        "bg": "linear-gradient(-45deg, #11998e, #38ef7d, #00b09b, #96c93d)",
        "accent": "#38ef7d",
        "button_bg": "#11998e",
        "button_hover": "#38ef7d"
    },
}

# Initialize Session State with validation
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "neon"
else:
    # Validate current_theme is a valid key
    if st.session_state.current_theme not in THEMES:
        st.session_state.current_theme = "neon"  # Reset to default

if 'queue' not in st.session_state: 
    st.session_state.queue = []
if 'history' not in st.session_state: 
    st.session_state.history = []
if 'ticket_id' not in st.session_state: 
    st.session_state.ticket_id = 101
if 'vip_mode' not in st.session_state: 
    st.session_state.vip_mode = False

# --- 3. CSS INJECTION ---
# Get current theme data with fallback
current_theme_data = THEMES.get(
    st.session_state.current_theme, 
    THEMES["neon"]  # Fallback to neon theme
)

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Poppins:wght@900&display=swap');

    /* DYNAMIC THEME BACKGROUND */
    .stApp {{
        background: {current_theme_data['bg']};
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Nunito', sans-serif;
    }}
    
    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* GLASS PANELS */
    .glass-panel {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.6);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}

    /* TITLES */
    .hero-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        color: white;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 0px;
    }}
    
    /* BASE BUTTON STYLES */
    div.stButton > button {{
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 800;
        border: none;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: white !important;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }}

    div.stButton > button:active {{
        transform: translateY(-2px);
    }}

    /* BUTTON HOVER GLOW EFFECT */
    div.stButton > button::after {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }}

    div.stButton > button:hover::after {{
        left: 100%;
    }}

    /* THEME BUTTONS - BLUE/PURPLE */
    .theme-button {{
        background: linear-gradient(135deg, {current_theme_data['button_bg']}, {current_theme_data['accent']}) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }}
    
    .theme-button:hover {{
        background: linear-gradient(135deg, {current_theme_data['button_hover']}, {current_theme_data['button_bg']}) !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 20px {current_theme_data['accent']}80 !important;
    }}

    /* VIP BUTTON - GOLD/YELLOW */
    .vip-button {{
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #8B4513 !important;
        font-weight: 900 !important;
        border: 2px solid #FFD700 !important;
    }}
    
    .vip-button:hover {{
        background: linear-gradient(135deg, #FFA500, #FFD700) !important;
        color: #8B4513 !important;
        box-shadow: 0 0 20px #FFD70080 !important;
        border: 2px solid #FFA500 !important;
    }}

    /* ADD BUTTON - TEAL/BLUE */
    .add-button {{
        background: linear-gradient(135deg, #00C9FF, #92FE9D) !important;
        border: 2px solid #00C9FF !important;
    }}
    
    .add-button:hover {{
        background: linear-gradient(135deg, #92FE9D, #00C9FF) !important;
        box-shadow: 0 0 20px #00C9FF80 !important;
        border: 2px solid #92FE9D !important;
    }}

    /* SERVE BUTTON - GREEN */
    .serve-button {{
        background: linear-gradient(135deg, #00b09b, #96c93d) !important;
        font-size: 1.1rem !important;
        height: 55px !important;
        border: 2px solid #00b09b !important;
    }}
    
    .serve-button:hover {{
        background: linear-gradient(135deg, #96c93d, #00b09b) !important;
        box-shadow: 0 0 20px #96c93d80 !important;
        border: 2px solid #96c93d !important;
    }}

    /* RESET BUTTON - RED/PINK */
    .reset-button {{
        background: linear-gradient(135deg, #FF416C, #FF4B2B) !important;
        margin-top: 10px;
        font-weight: 900 !important;
        border: 2px solid #FF416C !important;
    }}
    
    .reset-button:hover {{
        background: linear-gradient(135deg, #FF4B2B, #FF416C) !important;
        box-shadow: 0 0 20px #FF416C80 !important;
        border: 2px solid #FF4B2B !important;
    }}

    /* TICKET CARDS */
    .ticket-card {{
        background: white;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        border-left: 8px solid #ddd;
        animation: slideIn 0.5s ease;
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .ticket-active {{
        border-left: 8px solid {current_theme_data['accent']};
        background: #fff;
        box-shadow: 0 0 20px {current_theme_data['accent']}40;
        transform: scale(1.02);
    }}
    
    .ticket-vip {{
        border: 2px solid #FFD700;
        border-left: 8px solid #FFD700;
        background: #fffdf0;
    }}

    .avatar {{ font-size: 2.2rem; margin-right: 15px; }}
    .ticket-info {{ flex-grow: 1; }}
    .ticket-id {{ font-weight: 900; font-size: 1.2rem; color: #333; }}
    .ticket-meta {{ font-size: 0.8rem; color: #777; }}
    
    /* HISTORY */
    .history-item {{
        background: rgba(255,255,255,0.5);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }}
    .ai-msg {{
        font-style: italic;
        color: #555;
        background: rgba(255,255,255,0.6);
        padding: 5px 10px;
        border-radius: 8px;
        margin-top: 5px;
        border-left: 3px solid {current_theme_data['accent']};
    }}

    /* HIDE STREAMLIT CHROME */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
</style>
""", unsafe_allow_html=True)

# --- 4. LOGIC FUNCTIONS ---
NAMES = ["Kai", "Luna", "Milo", "Nova", "Leo", "Mia", "Zane", "Cleo", "Jax", "Ivy", "Finn"]
AVATARS = ["🐼", "🦊", "🦄", "🦁", "🐯", "🐸", "🐙", "🐵", "🐨", "🤖", "👽"]
SNACKS = ["Popcorn 🍿", "Nachos 🌮", "Soda 🥤", "Candy 🍫", "Hotdog 🌭"]

# List of predefined cinema messages
CINEMA_MESSAGES = [
    "Enjoy the movie! 🎬",
    "Great choice of snacks! 🍿",
    "Have an awesome time! 😊",
    "The show is about to begin! 🎭",
    "Perfect seats await! 🪑",
    "Movie magic starts now! ✨",
    "Get ready for fun! 🎉",
    "Your cinematic journey begins! 🚀",
    "Lights, camera, action! 📽️",
    "Enjoy the feature! 🍿",
    "Popcorn refills on us! 🆓",
    "Comfort mode: activated! 😎"
]

def enqueue():
    name = random.choice(NAMES)
    avatar = random.choice(AVATARS)
    snack = random.choice(SNACKS)
    is_vip = st.session_state.vip_mode
    
    new_ticket = {
        "id": st.session_state.ticket_id,
        "name": name,
        "avatar": avatar,
        "snack": snack,
        "joined": datetime.now().strftime("%I:%M %p"),
        "is_vip": is_vip
    }
    
    st.session_state.ticket_id += 1
    
    # VIP Logic: Insert behind the person currently being served (index 1)
    if is_vip and len(st.session_state.queue) > 0:
        st.session_state.queue.insert(1, new_ticket)
    else:
        st.session_state.queue.append(new_ticket)
    
    # Reset toggle
    st.session_state.vip_mode = False

def dequeue():
    if not st.session_state.queue:
        return

    # Pop the first person
    person = st.session_state.queue.pop(0)
    
    # Use a random predefined message
    cinema_message = random.choice(CINEMA_MESSAGES)

    # Add to history
    person['served_time'] = datetime.now().strftime("%I:%M %p")
    person['cinema_msg'] = cinema_message
    st.session_state.history.insert(0, person)

def reset_queue():
    """Reset the entire queue and history"""
    st.session_state.queue = []
    st.session_state.history = []
    # Reset ticket ID to start from 101 again
    st.session_state.ticket_id = 101
    # Keep current theme and VIP mode settings
    st.success("Queue and history have been reset!")

# --- 5. UI LAYOUT ---

st.markdown('<div class="hero-title">🍿 POPCORN CINEMA</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:white; margin-bottom:30px; opacity:0.8;">{current_theme_data["name"]} Mode</div>', unsafe_allow_html=True)

col_ctrl, col_queue, col_hist = st.columns([1, 1.5, 1])

# --- LEFT: CONTROLS ---
with col_ctrl:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 🎨 Vibe Check")
    
    # Theme Buttons - BLUE/PURPLE
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌃 Neon City", key="theme_neon", use_container_width=True):
            st.session_state.current_theme = "neon"
            st.rerun()
        if st.button("🌊 Cyber Ocean", key="theme_ocean", use_container_width=True):
            st.session_state.current_theme = "ocean"
            st.rerun()
    with c2:
        if st.button("🌅 Sunset Strip", key="theme_sunset", use_container_width=True):
            st.session_state.current_theme = "sunset"
            st.rerun()
        if st.button("🌿 Toxic Jungle", key="theme_forest", use_container_width=True):
            st.session_state.current_theme = "forest"
            st.rerun()

    st.markdown("---")
    st.markdown("### 🕹️ Actions")
    
    # VIP Toggle - GOLD/YELLOW
    vip_label = "🌟 VIP ON" if st.session_state.vip_mode else "👑 VIP OFF"
    
    # Apply custom styling to VIP button
    st.markdown(f"""
    <style>
        div[data-testid="stButton"] button[kind="secondary"]:first-of-type {{
            background: linear-gradient(135deg, #FFD700, #FFA500) !important;
            color: #8B4513 !important;
            border: 2px solid #FFD700 !important;
        }}
        div[data-testid="stButton"] button[kind="secondary"]:first-of-type:hover {{
            background: linear-gradient(135deg, #FFA500, #FFD700) !important;
            box-shadow: 0 0 20px #FFD70080 !important;
            border: 2px solid #FFA500 !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(vip_label, key="vip_toggle", use_container_width=True):
        st.session_state.vip_mode = not st.session_state.vip_mode
        st.rerun()

    # Add Button - TEAL/BLUE
    add_label = "✨ Add VIP Guest" if st.session_state.vip_mode else "➕ Add Customer"
    
    # Apply custom styling to Add button
    st.markdown(f"""
    <style>
        div[data-testid="stButton"] button[kind="secondary"]:nth-of-type(2) {{
            background: linear-gradient(135deg, #00C9FF, #92FE9D) !important;
            border: 2px solid #00C9FF !important;
        }}
        div[data-testid="stButton"] button[kind="secondary"]:nth-of-type(2):hover {{
            background: linear-gradient(135deg, #92FE9D, #00C9FF) !important;
            box-shadow: 0 0 20px #00C9FF80 !important;
            border: 2px solid #92FE9D !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(add_label, key="add_customer", use_container_width=True):
        enqueue()
        st.rerun()
    
    st.write("")
    
    # Serve Button - GREEN
    serve_disabled = len(st.session_state.queue) == 0
    serve_text = "🎟️ Serve Next Customer" if not serve_disabled else "⏳ Queue Empty"
    
    # Apply custom styling to Serve button
    st.markdown(f"""
    <style>
        div[data-testid="stButton"] button[kind="primary"] {{
            background: linear-gradient(135deg, #00b09b, #96c93d) !important;
            border: 2px solid #00b09b !important;
            height: 55px !important;
        }}
        div[data-testid="stButton"] button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #96c93d, #00b09b) !important;
            box-shadow: 0 0 20px #96c93d80 !important;
            border: 2px solid #96c93d !important;
        }}
        div[data-testid="stButton"] button[kind="primary"]:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(serve_text, key="serve_next", type="primary", disabled=serve_disabled, use_container_width=True):
        dequeue()
        st.rerun()
    
    # Reset Button - RED/PINK
    st.markdown("---")
    
    # Apply custom styling to Reset button
    st.markdown(f"""
    <style>
        div[data-testid="stButton"] button[kind="secondary"]:nth-of-type(3) {{
            background: linear-gradient(135deg, #FF416C, #FF4B2B) !important;
            border: 2px solid #FF416C !important;
            font-weight: 900 !important;
        }}
        div[data-testid="stButton"] button[kind="secondary"]:nth-of-type(3):hover {{
            background: linear-gradient(135deg, #FF4B2B, #FF416C) !important;
            box-shadow: 0 0 20px #FF416C80 !important;
            border: 2px solid #FF4B2B !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Reset Queue & History", key="reset", use_container_width=True):
        reset_queue()
        st.rerun()
        
    st.markdown("---")
    
    # Stats
    wait_time = max(0, (len(st.session_state.queue) - 1) * 2)
    st.markdown(f"""
    <div style="display:flex; justify-content:space-around; text-align:center; color:#333;">
        <div>
            <div style="font-size:1.5rem; font-weight:900;">{len(st.session_state.queue)}</div>
            <div style="font-size:0.8rem;">IN LINE</div>
        </div>
        <div>
            <div style="font-size:1.5rem; font-weight:900;">{wait_time}m</div>
            <div style="font-size:0.8rem;">WAIT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- CENTER: QUEUE ---
with col_queue:
    if not st.session_state.queue:
        st.markdown("""
        <div class="glass-panel" style="text-align:center; padding: 50px;">
            <div style="font-size: 4rem; opacity: 0.5;">💤</div>
            <h3>Lobby is Empty</h3>
            <p>Add customers to start the show!</p>
            <div style="margin-top: 20px; font-size: 2rem; animation: bounce 2s infinite;">
                👇
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<h3 style="color: white; margin-bottom: 15px;">🎬 Active Queue ({len(st.session_state.queue)} waiting)</h3>', unsafe_allow_html=True)
        
        for index, ticket in enumerate(st.session_state.queue):
            is_first = (index == 0)
            status_text = "SERVING NOW" if is_first else f"WAITING #{index}"
            
            # Dynamic Classes
            card_class = "ticket-card"
            if is_first: card_class += " ticket-active"
            if ticket['is_vip']: card_class += " ticket-vip"
            
            vip_badge = '<span style="background:#FFD700; color:#B8860B; padding:2px 6px; border-radius:4px; font-size:0.7rem; margin-left:5px; font-weight:bold;">VIP</span>' if ticket['is_vip'] else ""
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="avatar">{ticket['avatar']}</div>
                <div class="ticket-info">
                    <div style="display:flex; justify-content:space-between;">
                        <span class="ticket-id">#{ticket['id']} {vip_badge}</span>
                        <span style="font-size:0.7rem; font-weight:bold; color:{current_theme_data['accent'] if is_first else '#aaa'}">{status_text}</span>
                    </div>
                    <div style="font-weight:bold; color:#555;">{ticket['name']}</div>
                    <div class="ticket-meta">{ticket['snack']} • {ticket['joined']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- RIGHT: HISTORY ---
with col_hist:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    history_count = len(st.session_state.history)
    st.markdown(f"### ✅ Served ({history_count})")
    
    if not st.session_state.history:
        st.markdown("""
        <div style='text-align: center; padding: 30px; color: #666;'>
            <div style='font-size: 3rem; opacity: 0.5;'>📝</div>
            <p>No customers served yet</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for item in st.session_state.history[:8]:  # Show more history
            st.markdown(f"""
            <div class="history-item">
                <div style="font-weight:bold;">
                    #{item['id']} {item['name']} {item['avatar']}
                </div>
                <div class="ai-msg">"{item.get('cinema_msg', 'Enjoy the show!')}"</div>
            </div>
            """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
