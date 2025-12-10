import streamlit as st
import random
import time
from datetime import datetime
import os
import json
from pathlib import Path

# Try to import Google GenAI, handle if not installed or key missing
try:
    from google import genai
    from google.genai import types
    HAS_GENAI_LIB = True
except ImportError:
    HAS_GENAI_LIB = False

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Neon Cinema Live", 
    page_icon="🍿", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CONFIGURATION & STATE ---
THEMES = {
    "Neon City": "linear-gradient(-45deg, #FF3CAC, #784BA0, #2B86C5, #23d5ab)",
    "Sunset Strip": "linear-gradient(-45deg, #FF512F, #DD2476, #F09819, #FF512F)",
    "Toxic Jungle": "linear-gradient(-45deg, #11998e, #38ef7d, #00b09b, #96c93d)",
    "Midnight": "linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #000000)",
    "Candy": "linear-gradient(-45deg, #FF9A9E, #FAD0C4, #FAD0C4, #FFD1FF)",
}

if 'queue' not in st.session_state: st.session_state.queue = []
if 'history' not in st.session_state: st.session_state.history = []
if 'ticket_id' not in st.session_state: st.session_state.ticket_id = 101
if 'vip_mode' not in st.session_state: st.session_state.vip_mode = False
if 'current_theme' not in st.session_state: st.session_state.current_theme = "Neon City"
if 'user_api_key' not in st.session_state: st.session_state.user_api_key = None

# --- 3. CUSTOM CSS (LIVELY DESIGN) ---
theme_bg = THEMES[st.session_state.current_theme]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Poppins:wght@900&display=swap');

    /* ANIMATED BACKGROUND */
    .stApp {{
        background: {theme_bg};
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Nunito', sans-serif;
        min-height: 100vh;
    }}
    
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* HIDE STREAMLIT ELEMENTS */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}

    /* GLASSMORPHISM PANELS */
    .glass-panel {{
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
    }}

    /* SIDEBAR GLASS */
    .sidebar .sidebar-content {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
    }}

    /* TYPOGRAPHY */
    .hero-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}
    .hero-subtitle {{
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }}

    /* BUTTONS */
    .stButton > button {{
        width: 100%;
        border-radius: 15px;
        height: 55px;
        font-weight: 800;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: white;
        transition: all 0.2s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }}
    
    /* Primary (Serve) - Orange/Gold */
    div[data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button {{
        background: linear-gradient(135deg, #FF9966 0%, #FF5E62 100%);
    }}
    
    /* Secondary (Add) - Blue */
    div[data-testid="stHorizontalBlock"] .stButton > button {{
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }}

    /* Reset Button - Red */
    .reset-button .stButton > button {{
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
    }}

    /* VIP Button Override */
    .vip-active {{
        border: 2px solid #FFD700 !important;
        box-shadow: 0 0 15px #FFD700 !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.02);
        filter: brightness(1.1);
    }}
    .stButton > button:active {{
        transform: translateY(1px);
    }}

    /* QUEUE CARDS */
    .ticket-card {{
        background: white;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 6px solid #e0e0e0;
        animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }}

    @keyframes popIn {{
        from {{ opacity: 0; transform: scale(0.9) translateY(10px); }}
        to {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}

    .ticket-active {{
        border-left: 8px solid #00C9FF;
        background: linear-gradient(to right, #FFFDE4, #FFFFFF);
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 2px solid rgba(0, 201, 255, 0.3);
    }}

    .ticket-vip {{
        border-left: 8px solid #FFD700;
        background: #fffcf0;
        border: 2px solid #FFD700;
    }}

    .t-avatar {{ font-size: 2.5rem; margin-right: 15px; }}
    .t-info {{ flex-grow: 1; }}
    .t-name {{ font-weight: 800; color: #333; font-size: 1.1rem; }}
    .t-meta {{ font-size: 0.8rem; color: #777; display: flex; gap: 10px; }}
    .badge {{ 
        background: #eee; padding: 2px 8px; border-radius: 4px; 
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    }}

    /* HISTORY */
    .history-item {{
        padding: 10px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        font-size: 0.9rem;
    }}
    .ai-msg {{
        font-style: italic;
        color: #555;
        background: rgba(255,255,255,0.5);
        padding: 8px;
        border-radius: 8px;
        margin-top: 5px;
        border-left: 3px solid #8A2387;
    }}

    /* STATS CARDS */
    .stat-card {{
        background: white;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 5px;
    }}
    .stat-number {{
        font-size: 2rem;
        font-weight: 900;
        color: #333;
    }}
    .stat-label {{
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* PROGRESS BAR */
    .progress-container {{
        width: 100%;
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
        margin: 10px 0;
    }}
    .progress-bar {{
        height: 8px;
        border-radius: 10px;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        transition: width 0.3s ease;
    }}
</style>
""", unsafe_allow_html=True)

# --- 4. HELPERS & LOGIC ---

def get_api_key():
    """Get API key from multiple sources in priority order"""
    # 1. User input in session state
    if st.session_state.user_api_key:
        return st.session_state.user_api_key
    
    # 2. Streamlit secrets
    if "API_KEY" in st.secrets:
        return st.secrets["API_KEY"]
    
    # 3. Environment variable
    if "GOOGLE_API_KEY" in os.environ:
        return os.environ["GOOGLE_API_KEY"]
    
    return None

def get_random_data():
    names = ["Kai", "Luna", "Milo", "Nova", "Leo", "Mia", "Zane", "Cleo", "Jax", "Ivy", "Finn"]
    avatars = ["🐼", "🦊", "🦄", "🦁", "🐯", "🐸", "🐙", "🐵", "🐨", "🐷", "🐻"]
    snacks = ["🍿 Popcorn", "🥤 Soda", "🌭 Hotdog", "🥨 Pretzel", "🍫 Candy", "🌮 Nachos"]
    return random.choice(names), random.choice(avatars), random.choice(snacks)

def get_ai_message(name, snack, theme):
    """Generates a message using Gemini, or a fallback if no key is present."""
    
    api_key = get_api_key()
        
    # If no key or no lib, return fallback
    if not api_key or not HAS_GENAI_LIB:
        fallbacks = [
            f"Enjoy your {snack}, {name}!",
            f"Welcome to the movies, {name}!",
            f"Grab a seat, {name}!",
            "Showtime! Enjoy the snacks.",
            f"{name}, your {snack} awaits!",
            f"Roll the film for {name}!",
            f"Dim the lights, {name} is here!"
        ]
        return random.choice(fallbacks)

    # Call Gemini
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"Generate a witty, very short (max 7 words) cinema welcome for {name}. Context: They ordered {snack}. Theme: {theme}. Be creative and fun."
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
        return f"Welcome {name}! Enjoy your movie!"

def enqueue_custom(name, avatar, snack, is_vip):
    """Add a custom guest to the queue"""
    new_ticket = {
        "id": st.session_state.ticket_id,
        "name": name,
        "avatar": avatar,
        "snack": snack,
        "joined": datetime.now().strftime("%I:%M %p"),
        "is_vip": is_vip
    }
    
    st.session_state.ticket_id += 1
    
    # VIP Logic: Insert at index 1 (behind current server) or 0 if empty
    if is_vip and len(st.session_state.queue) > 0:
        st.session_state.queue.insert(1, new_ticket)
    else:
        st.session_state.queue.append(new_ticket)
    
    return new_ticket

def enqueue_random():
    """Add a random guest to the queue"""
    name, avatar, snack = get_random_data()
    return enqueue_custom(name, avatar, snack, st.session_state.vip_mode)

def dequeue():
    if not st.session_state.queue:
        st.toast("⚠️ Queue is empty!")
        return None

    # Pop the first person
    person = st.session_state.queue.pop(0)
    
    # Generate Message
    msg = get_ai_message(person['name'], person['snack'], st.session_state.current_theme)
    person['out_time'] = datetime.now().strftime("%I:%M %p")
    person['message'] = msg
    
    # Add to history
    st.session_state.history.insert(0, person)
    
    # Occasional fun
    if len(st.session_state.history) % 5 == 0:
        st.balloons()
    elif len(st.session_state.history) % 7 == 0:
        st.snow()
    
    return person

def reset():
    st.session_state.queue = []
    st.session_state.history = []
    st.session_state.ticket_id = 101
    st.session_state.vip_mode = False

def save_history():
    """Save history to a JSON file"""
    try:
        history_data = {
            "history": st.session_state.history,
            "total_served": len(st.session_state.history),
            "timestamp": datetime.now().isoformat(),
            "theme": st.session_state.current_theme
        }
        
        # Create data directory if it doesn't exist
        Path("data").mkdir(exist_ok=True)
        
        # Save to file
        with open("data/cinema_history.json", "w") as f:
            json.dump(history_data, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Failed to save history: {e}")
        return False

def load_history():
    """Load history from JSON file"""
    try:
        if Path("data/cinema_history.json").exists():
            with open("data/cinema_history.json", "r") as f:
                data = json.load(f)
                # Optional: You could load the history back
                # st.session_state.history = data.get("history", [])
            return data
    except Exception as e:
        st.error(f"Failed to load history: {e}")
    return None

def get_statistics():
    """Calculate various statistics"""
    total_served = len(st.session_state.history)
    vip_served = len([h for h in st.session_state.history if h.get('is_vip', False)])
    regular_served = total_served - vip_served
    
    # Most popular snack
    snack_counts = {}
    for person in st.session_state.history:
        snack = person.get('snack', 'Unknown')
        snack_counts[snack] = snack_counts.get(snack, 0) + 1
    
    most_popular = max(snack_counts.items(), key=lambda x: x[1]) if snack_counts else ("None", 0)
    
    # Peak time (simplified)
    time_counts = {}
    for person in st.session_state.history:
        time_str = person.get('joined', '')
        hour = time_str.split(':')[0] if ':' in time_str else 'Unknown'
        time_counts[hour] = time_counts.get(hour, 0) + 1
    
    peak_hour = max(time_counts.items(), key=lambda x: x[1]) if time_counts else ("None", 0)
    
    return {
        "total_served": total_served,
        "vip_served": vip_served,
        "regular_served": regular_served,
        "most_popular_snack": most_popular[0],
        "snack_count": most_popular[1],
        "peak_hour": peak_hour[0],
        "current_queue": len(st.session_state.queue),
        "avg_wait_time": max(0, len(st.session_state.queue) - 1) * 2
    }

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API Key Input
    st.markdown("### 🔑 API Settings")
    api_key = get_api_key()
    
    if not api_key:
        st.warning("AI features disabled - no API key found")
        user_key = st.text_input("Enter Google API Key:", type="password", 
                                help="Get your API key from https://makersuite.google.com/app/apikey")
        
        if user_key:
            st.session_state.user_api_key = user_key
            st.success("API key saved! Refresh to enable AI features.")
            st.rerun()
    else:
        st.success("✅ AI features enabled")
        if st.button("Clear API Key"):
            st.session_state.user_api_key = None
            st.rerun()
    
    st.markdown("---")
    
    # Custom Guest Addition
    st.markdown("### 🎭 Add Custom Guest")
    
    with st.expander("Create Custom Ticket", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            custom_name = st.text_input("Guest Name", "Guest")
        with col2:
            custom_avatar = st.selectbox("Avatar", 
                ["🐼", "🦊", "🦄", "🦁", "🐯", "🐸", "🐙", "🐵", "🐨", "🐷", "🐻", "👤", "🎭"])
        
        custom_snack = st.selectbox("Snack Order", 
            ["🍿 Popcorn", "🥤 Soda", "🌭 Hotdog", "🥨 Pretzel", "🍫 Candy", "🌮 Nachos", "🍿🍫 Combo"])
        
        custom_vip = st.checkbox("VIP Guest", value=False)
        
        if st.button("Add Custom Guest", use_container_width=True):
            enqueue_custom(custom_name, custom_avatar, custom_snack, custom_vip)
            st.success(f"Added {custom_name} to the queue!")
            st.rerun()
    
    st.markdown("---")
    
    # History Management
    st.markdown("### 📊 Data Management")
    
    if st.button("💾 Save History", use_container_width=True):
        if save_history():
            st.success("History saved successfully!")
    
    if st.button("📈 View Statistics", use_container_width=True):
        stats = get_statistics()
        st.info(f"""
        **Today's Stats:**
        - Total Served: {stats['total_served']}
        - VIP Guests: {stats['vip_served']}
        - Most Popular: {stats['most_popular_snack']}
        - Current Queue: {stats['current_queue']}
        """)

# --- 6. MAIN LAYOUT ---

st.markdown('<div class="hero-title">🍿 Neon Cinema</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-subtitle">Theme: {st.session_state.current_theme}</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.2, 1], gap="medium")

# --- LEFT: CONTROLS & STATS ---
with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("🎨 Theme Selector")
    
    # Theme Switcher with preview
    selected_theme = st.selectbox("Select Vibe", list(THEMES.keys()), 
                                 index=list(THEMES.keys()).index(st.session_state.current_theme),
                                 label_visibility="collapsed")
    
    if selected_theme != st.session_state.current_theme:
        st.session_state.current_theme = selected_theme
        st.rerun()
    
    st.markdown(f"""
    <div style="text-align:center; margin:10px 0; padding:10px; border-radius:10px; background:rgba(255,255,255,0.5);">
        <small>Current: {selected_theme}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🕹️ Quick Actions")
    
    # VIP Toggle
    vip_label = "🌟 VIP MODE: ON" if st.session_state.vip_mode else "⚪ VIP Mode: Off"
    vip_color = "#FFD700" if st.session_state.vip_mode else "#666"
    
    if st.button(vip_label, use_container_width=True):
        st.session_state.vip_mode = not st.session_state.vip_mode
        st.rerun()
    
    # Add Random Guest Button
    btn_label = "🎭 Add Random VIP" if st.session_state.vip_mode else "➕ Add Random Guest"
    if st.button(btn_label, use_container_width=True):
        enqueue_random()
        st.rerun()
    
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    # Serve Button
    if st.button("🎟️ Serve Next Guest", use_container_width=True):
        served = dequeue()
        if served:
            st.toast(f"Served {served['name']}!")
        st.rerun()
    
    st.markdown("---")
    
    # Statistics
    stats = get_statistics()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['current_queue']}</div>
            <div class="stat-label">In Line</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['vip_served']}</div>
            <div class="stat-label">VIP Served</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['avg_wait_time']}m</div>
            <div class="stat-label">Wait Time</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_served']}</div>
            <div class="stat-label">Total Served</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress Bar for Queue
    if stats['current_queue'] > 0:
        progress = min(100, (stats['current_queue'] / 10) * 100)
        st.markdown(f"""
        <div style="margin-top:15px;">
            <div style="display:flex; justify-content:space-between;">
                <small>Queue Load</small>
                <small>{stats['current_queue']}/10</small>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width:{progress}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Reset Button
    st.markdown('<div class="reset-button">', unsafe_allow_html=True)
    if st.button("🔄 Reset Entire System", use_container_width=True):
        reset()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- CENTER: THE QUEUE ---
with col2:
    if not st.session_state.queue:
        st.markdown("""
        <div class="glass-panel" style="text-align:center; padding:50px;">
            <div style="font-size:4rem; opacity:0.5;">💤</div>
            <h3>Lobby is Empty</h3>
            <p>Add customers to start the movie!</p>
            <div style="margin-top:20px;">
                <small>Use the controls on the left or sidebar to add guests</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, ticket in enumerate(st.session_state.queue):
            is_first = (i == 0)
            is_vip = ticket['is_vip']
            
            # Determine CSS classes
            card_class = "ticket-card"
            if is_first: card_class += " ticket-active"
            if is_vip: card_class += " ticket-vip"
            
            status_badge = "🎬 SERVING NOW" if is_first else f"⏳ WAITING #{i}"
            badge_color = "#00C9FF" if is_first else "#eee"
            text_color = "white" if is_first else "#555"
            
            vip_badge = '<span class="badge" style="background:#FFD700; color:#B8860B; margin-left:5px;">VIP</span>' if is_vip else ""
            
            # Calculate wait time (2 minutes per position)
            wait_time = i * 2
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="t-avatar">{ticket['avatar']}</div>
                <div class="t-info">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span style="font-weight:900; font-size:1.1rem;">#{ticket['id']} {vip_badge}</span>
                        <span class="badge" style="background:{badge_color}; color:{text_color};">{status_badge}</span>
                    </div>
                    <div class="t-name">{ticket['name']}</div>
                    <div class="t-meta">
                        <span>{ticket['snack']}</span> • 
                        <span>Joined: {ticket['joined']}</span> •
                        <span>Wait: {wait_time}min</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- RIGHT: HISTORY & ACTIVITY ---
with col3:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("✅ Recently Served")
    
    if not st.session_state.history:
        st.caption("No customers served yet. Serve your first guest to see history here.")
    
    # Activity filter
    show_all = st.checkbox("Show all history", value=False)
    history_to_show = st.session_state.history[:15] if show_all else st.session_state.history[:5]
    
    for item in history_to_show:
        vip_icon = "🌟" if item['is_vip'] else "👤"
        vip_class = "history-vip" if item['is_vip'] else ""
        
        st.markdown(f"""
        <div class="history-item {vip_class}">
            <div style="font-weight:bold; color:#333; display:flex; justify-content:space-between;">
                <span>#{item['id']} {item['name']} {vip_icon}</span>
                <span style="font-size:0.8rem; color:#999;">{item['out_time']}</span>
            </div>
            <div style="font-size:0.8rem; color:#666;">Ordered: {item['snack']}</div>
            <div class="ai-msg">"{item['message']}"</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.history and len(st.session_state.history) > 5 and not show_all:
        st.caption(f"Showing 5 of {len(st.session_state.history)} records")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional Info Panel
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("ℹ️ Quick Info")
    
    api_status = "✅ Enabled" if get_api_key() and HAS_GENAI_LIB else "❌ Disabled"
    next_ticket = st.session_state.queue[0]['name'] if st.session_state.queue else "None"
    
    st.markdown(f"""
    <div style="font-size:0.9rem;">
        <div style="margin-bottom:8px;">
            <strong>AI Chat:</strong> {api_status}
        </div>
        <div style="margin-bottom:8px;">
            <strong>Next to Serve:</strong> {next_ticket}
        </div>
        <div style="margin-bottom:8px;">
            <strong>Current Theme:</strong> {st.session_state.current_theme}
        </div>
        <div>
            <strong>System Status:</strong> 🟢 Operational
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. FOOTER ---
st.markdown("""
<div style="text-align:center; margin-top:30px; padding:20px; color:rgba(255,255,255,0.7); font-size:0.8rem;">
    <hr style="border-color:rgba(255,255,255,0.2); margin-bottom:15px;">
    <p>🎬 Neon Cinema Live • Streamlit Demo • VIPs skip ahead! • Snacks served with AI charm</p>
    <p><small>Add guests, serve them, and enjoy the AI-powered movie experience!</small></p>
</div>
""", unsafe_allow_html=True)
