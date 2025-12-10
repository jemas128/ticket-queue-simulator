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

# --- 2. ENHANCED THEMES WITH COLOR SCHEMES ---
THEMES = {
    "Neon City": {
        "gradient": "linear-gradient(-45deg, #FF3CAC, #784BA0, #2B86C5, #23d5ab)",
        "primary": "#FF3CAC",
        "secondary": "#2B86C5",
        "accent": "#23d5ab",
        "text": "#ffffff",
        "card_bg": "rgba(255, 255, 255, 0.85)"
    },
    "Sunset Strip": {
        "gradient": "linear-gradient(-45deg, #FF512F, #DD2476, #F09819, #FF512F)",
        "primary": "#FF512F",
        "secondary": "#DD2476",
        "accent": "#F09819",
        "text": "#ffffff",
        "card_bg": "rgba(255, 255, 255, 0.9)"
    },
    "Toxic Jungle": {
        "gradient": "linear-gradient(-45deg, #11998e, #38ef7d, #00b09b, #96c93d)",
        "primary": "#38ef7d",
        "secondary": "#11998e",
        "accent": "#96c93d",
        "text": "#ffffff",
        "card_bg": "rgba(255, 255, 255, 0.85)"
    },
    "Midnight Galaxy": {
        "gradient": "linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #000000)",
        "primary": "#8A2BE2",
        "secondary": "#4B0082",
        "accent": "#00CED1",
        "text": "#ffffff",
        "card_bg": "rgba(255, 255, 255, 0.12)"
    },
    "Candy Crush": {
        "gradient": "linear-gradient(-45deg, #FF9A9E, #FAD0C4, #FAD0C4, #FFD1FF)",
        "primary": "#FF9A9E",
        "secondary": "#FAD0C4",
        "accent": "#FFD1FF",
        "text": "#333333",
        "card_bg": "rgba(255, 255, 255, 0.95)"
    },
    "Cyberpunk": {
        "gradient": "linear-gradient(-45deg, #ff0080, #ff8c00, #40e0d0, #00ff00)",
        "primary": "#ff0080",
        "secondary": "#40e0d0",
        "accent": "#00ff00",
        "text": "#ffffff",
        "card_bg": "rgba(0, 0, 0, 0.7)"
    },
    "Ocean Depth": {
        "gradient": "linear-gradient(-45deg, #1a2980, #26d0ce, #1a2980, #26d0ce)",
        "primary": "#1a2980",
        "secondary": "#26d0ce",
        "accent": "#00ffff",
        "text": "#ffffff",
        "card_bg": "rgba(255, 255, 255, 0.85)"
    },
    "Fire Blaze": {
        "gradient": "linear-gradient(-45deg, #ff0000, #ff9900, #ffff00, #ff0000)",
        "primary": "#ff0000",
        "secondary": "#ff9900",
        "accent": "#ffff00",
        "text": "#ffffff",
        "card_bg": "rgba(255, 255, 255, 0.9)"
    }
}

if 'queue' not in st.session_state: st.session_state.queue = []
if 'history' not in st.session_state: st.session_state.history = []
if 'ticket_id' not in st.session_state: st.session_state.ticket_id = 101
if 'vip_mode' not in st.session_state: st.session_state.vip_mode = False
if 'current_theme' not in st.session_state: st.session_state.current_theme = "Neon City"
if 'user_api_key' not in st.session_state: st.session_state.user_api_key = None

# Get current theme colors
current_theme_data = THEMES[st.session_state.current_theme]

# --- 3. DYNAMIC CSS BASED ON THEME ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Poppins:wght@900&family=Orbitron:wght@400;700&display=swap');
    
    /* ANIMATED BACKGROUND */
    .stApp {{
        background: {current_theme_data['gradient']};
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Nunito', sans-serif;
        min-height: 100vh;
        color: {current_theme_data['text']};
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
        background: {current_theme_data['card_bg']};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        border-top: 5px solid {current_theme_data['primary']};
    }}

    /* SIDEBAR GLASS */
    .sidebar .sidebar-content {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 3px solid {current_theme_data['secondary']};
    }}

    /* TYPOGRAPHY */
    .hero-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(45deg, {current_theme_data['primary']}, {current_theme_data['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }}
    
    .hero-subtitle {{
        text-align: center;
        color: {current_theme_data['text']};
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 30px;
        opacity: 0.9;
        text-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}

    /* THEME BADGE */
    .theme-badge {{
        display: inline-block;
        padding: 4px 12px;
        background: {current_theme_data['primary']};
        color: white;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 10px;
        vertical-align: middle;
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        margin-bottom: 10px;
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::after {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }}
    
    .stButton > button:hover::after {{
        left: 100%;
    }}

    /* Primary (Serve) Button */
    .serve-button .stButton > button {{
        background: linear-gradient(135deg, {current_theme_data['primary']} 0%, {current_theme_data['secondary']} 100%);
        border: 2px solid {current_theme_data['accent']};
    }}

    /* Secondary (Add) Button */
    .add-button .stButton > button {{
        background: linear-gradient(135deg, {current_theme_data['secondary']} 0%, {current_theme_data['accent']} 100%);
    }}

    /* Reset Button */
    .reset-button .stButton > button {{
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        border: 2px solid #FFD700;
    }}

    /* VIP Button */
    .vip-toggle .stButton > button {{
        background: {'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)' if st.session_state.vip_mode else 'linear-gradient(135deg, #666 0%, #333 100%)'};
        border: {'2px solid #FFD700' if st.session_state.vip_mode else 'none'};
        box-shadow: {'0 0 20px #FFD700' if st.session_state.vip_mode else 'none'};
    }}

    .stButton > button:hover {{
        transform: translateY(-5px) scale(1.02);
        filter: brightness(1.1);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    .stButton > button:active {{
        transform: translateY(2px);
    }}

    /* QUEUE CARDS */
    .ticket-card {{
        background: white;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border-left: 8px solid #e0e0e0;
        transition: all 0.3s ease;
        animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        position: relative;
        overflow: hidden;
    }}
    
    .ticket-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {current_theme_data['primary']}, {current_theme_data['secondary']});
    }}

    @keyframes popIn {{
        from {{ opacity: 0; transform: scale(0.9) translateY(20px); }}
        to {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}

    .ticket-active {{
        border-left: 8px solid {current_theme_data['primary']};
        background: linear-gradient(135deg, #FFFDE4 0%, #FFFFFF 100%);
        transform: scale(1.02);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        border: 2px solid {current_theme_data['accent']};
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba({int(current_theme_data['primary'][1:3], 16)}, {int(current_theme_data['primary'][3:5], 16)}, {int(current_theme_data['primary'][5:7], 16)}, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba({int(current_theme_data['primary'][1:3], 16)}, {int(current_theme_data['primary'][3:5], 16)}, {int(current_theme_data['primary'][5:7], 16)}, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba({int(current_theme_data['primary'][1:3], 16)}, {int(current_theme_data['primary'][3:5], 16)}, {int(current_theme_data['primary'][5:7], 16)}, 0); }}
    }}

    .ticket-vip {{
        border-left: 8px solid #FFD700;
        background: linear-gradient(135deg, #fffcf0 0%, #fff8dc 100%);
        border: 2px solid #FFD700;
    }}

    .t-avatar {{ 
        font-size: 3rem; 
        margin-right: 20px; 
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));
    }}
    
    .t-info {{ flex-grow: 1; }}
    .t-name {{ 
        font-weight: 900; 
        color: #333; 
        font-size: 1.3rem;
        font-family: 'Poppins', sans-serif;
    }}
    
    .t-meta {{ 
        font-size: 0.9rem; 
        color: #666; 
        display: flex; 
        gap: 15px;
        margin-top: 5px;
    }}
    
    .badge {{ 
        background: {current_theme_data['secondary']}; 
        color: white;
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 0.75rem; 
        font-weight: 800; 
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .vip-badge {{
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #8B4513;
        box-shadow: 0 2px 5px rgba(255, 165, 0, 0.3);
    }}

    /* HISTORY */
    .history-item {{
        padding: 15px;
        border-bottom: 2px solid rgba(0,0,0,0.05);
        font-size: 0.9rem;
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 4px solid {current_theme_data['secondary']};
    }}
    
    .history-vip {{
        border-left: 4px solid #FFD700;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 255, 255, 0.8) 100%);
    }}
    
    .ai-msg {{
        font-style: italic;
        color: #555;
        background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(240,240,240,0.9) 100%);
        padding: 10px;
        border-radius: 10px;
        margin-top: 8px;
        border-left: 4px solid {current_theme_data['accent']};
        font-size: 0.9rem;
    }}

    /* STATS CARDS */
    .stat-card {{
        background: linear-gradient(135deg, {current_theme_data['card_bg']} 0%, rgba(255,255,255,0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        margin: 8px;
        border: 2px solid {current_theme_data['primary']};
        transition: transform 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-5px);
    }}
    
    .stat-number {{
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(45deg, {current_theme_data['primary']}, {current_theme_data['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Poppins', sans-serif;
    }}
    
    .stat-label {{
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-top: 5px;
    }}

    /* PROGRESS BAR */
    .progress-container {{
        width: 100%;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        margin: 15px 0;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.3);
    }}
    
    .progress-bar {{
        height: 10px;
        border-radius: 10px;
        background: linear-gradient(90deg, {current_theme_data['primary']} 0%, {current_theme_data['accent']} 100%);
        transition: width 0.5s ease;
        box-shadow: 0 0 10px {current_theme_data['primary']};
    }}

    /* THEME PREVIEW */
    .theme-preview {{
        height: 60px;
        border-radius: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: transform 0.3s ease;
        border: 2px solid transparent;
        overflow: hidden;
        position: relative;
    }}
    
    .theme-preview:hover {{
        transform: scale(1.05);
    }}
    
    .theme-preview.active {{
        border: 3px solid white;
        box-shadow: 0 0 15px {current_theme_data['accent']};
    }}
    
    .theme-label {{
        position: absolute;
        bottom: 5px;
        left: 10px;
        color: white;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        font-size: 0.8rem;
    }}

    /* EMPTY STATE */
    .empty-state {{
        text-align: center;
        padding: 60px 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        border: 3px dashed {current_theme_data['primary']};
    }}
    
    .empty-icon {{
        font-size: 5rem;
        opacity: 0.7;
        margin-bottom: 20px;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));
    }}

    /* FOOTER */
    .footer {{
        text-align: center;
        margin-top: 40px;
        padding: 25px;
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        border-top: 2px solid rgba(255,255,255,0.2);
        background: rgba(0,0,0,0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }}
    
    .glow-text {{
        text-shadow: 0 0 10px {current_theme_data['accent']};
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
    
    # Theme Preview Section
    st.markdown("### 🎨 Theme Gallery")
    
    # Create theme preview grid
    cols = st.columns(2)
    for idx, (theme_name, theme_data) in enumerate(THEMES.items()):
        with cols[idx % 2]:
            is_active = theme_name == st.session_state.current_theme
            active_class = "active" if is_active else ""
            
            st.markdown(f"""
            <div class="theme-preview {active_class}" onclick="document.querySelector('input[value=\\'{theme_name}\\']').click();">
                <div style="width:100%; height:100%; background: {theme_data['gradient']};"></div>
                <div class="theme-label">{theme_name}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"", key=f"theme_{idx}", help=f"Switch to {theme_name}", 
                        use_container_width=True, disabled=is_active):
                st.session_state.current_theme = theme_name
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
        
        if st.button("✨ Add Custom Guest", use_container_width=True):
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

st.markdown(f'<div class="hero-title">🎬 NEON CINEMA LIVE</div>', unsafe_allow_html=True)
st.markdown(f'''
    <div class="hero-subtitle">
        Real-time Queue Management • <span class="theme-badge">{st.session_state.current_theme}</span> Theme Active
    </div>
''', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.2, 1], gap="medium")

# --- LEFT: CONTROLS & STATS ---
with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    # VIP Toggle
    st.markdown('<div class="vip-toggle">', unsafe_allow_html=True)
    vip_label = "🌟 VIP MODE ACTIVE" if st.session_state.vip_mode else "⚪ VIP Mode"
    if st.button(vip_label, use_container_width=True):
        st.session_state.vip_mode = not st.session_state.vip_mode
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add Random Guest Button
    st.markdown('<div class="add-button">', unsafe_allow_html=True)
    btn_label = "✨ Add Random VIP Guest" if st.session_state.vip_mode else "➕ Add Random Guest"
    if st.button(btn_label, use_container_width=True):
        enqueue_random()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # Serve Button
    st.markdown('<div class="serve-button">', unsafe_allow_html=True)
    if st.button("🎟️ SERVE NEXT GUEST", use_container_width=True):
        served = dequeue()
        if served:
            st.toast(f"Served {served['name']}!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistics
    st.subheader("📊 Live Stats")
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
        <div style="margin-top:20px;">
            <div style="display:flex; justify-content:space-between;">
                <small>Queue Load</small>
                <small>{stats['current_queue']}/10</small>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width:{progress}%"></div>
            </div>
            <small style="color:#666; display:block
