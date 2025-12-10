import streamlit as st
import random
from datetime import datetime
import os

# Try to import Google GenAI
try:
    from google import genai
    HAS_GENAI_LIB = True
except ImportError:
    HAS_GENAI_LIB = False

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Neon Cinema Live", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CONFIGURATION & STATE ---
THEMES = {
    "Neon City": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "Sunset Strip": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "Toxic Jungle": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
}

if 'queue' not in st.session_state: st.session_state.queue = []
if 'history' not in st.session_state: st.session_state.history = []
if 'ticket_id' not in st.session_state: st.session_state.ticket_id = 101
if 'vip_mode' not in st.session_state: st.session_state.vip_mode = False
if 'current_theme' not in st.session_state: st.session_state.current_theme = "Neon City"

# --- 3. PROFESSIONAL UI DESIGN CSS ---
theme_bg = THEMES[st.session_state.current_theme]

st.markdown(f"""
<style>
    /* RESET & BASE */
    .stApp {{
        background: {theme_bg};
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        min-height: 100vh;
    }}
    
    /* HIDE DEFAULTS */
    header {{display: none !important;}}
    footer {{display: none !important;}}
    .stDeployButton {{display: none !important;}}
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        max-width: 1200px;
    }}
    
    /* HEADER */
    .cinema-header {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .header-title {{
        font-size: 1.8rem;
        font-weight: 800;
        color: #2D3748;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .header-subtitle {{
        font-size: 0.85rem;
        color: #718096;
        margin: 0.25rem 0 0 0;
        font-weight: 500;
    }}
    
    /* MAIN LAYOUT CONTAINERS */
    .main-grid {{
        display: grid;
        grid-template-columns: 320px 1fr 320px;
        gap: 1rem;
        height: calc(100vh - 140px);
    }}
    
    .panel {{
        background: white;
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    
    .panel-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #F7FAFC;
    }}
    
    .panel-title {{
        font-size: 1rem;
        font-weight: 700;
        color: #2D3748;
        margin: 0;
    }}
    
    .badge {{
        background: #EDF2F7;
        color: #4A5568;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    
    /* LEFT PANEL - CONTROLS */
    .control-section {{
        margin-bottom: 1.25rem;
    }}
    
    .section-title {{
        font-size: 0.875rem;
        font-weight: 600;
        color: #4A5568;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* THEME SELECTOR */
    .theme-option {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem;
        border-radius: 12px;
        background: #F7FAFC;
        border: 2px solid transparent;
        cursor: pointer;
        transition: all 0.2s;
        margin-bottom: 0.5rem;
        width: 100%;
    }}
    
    .theme-option:hover {{
        border-color: #CBD5E0;
    }}
    
    .theme-option.active {{
        border-color: #4299E1;
        background: #EBF8FF;
    }}
    
    .theme-preview {{
        width: 24px;
        height: 24px;
        border-radius: 6px;
        background: var(--theme-color);
    }}
    
    /* TOGGLE SWITCH */
    .toggle-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #F7FAFC;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
    }}
    
    .toggle-label {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #2D3748;
    }}
    
    .toggle-switch {{
        position: relative;
        width: 44px;
        height: 24px;
    }}
    
    .toggle-slider {{
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #CBD5E0;
        transition: .4s;
        border-radius: 24px;
    }}
    
    .toggle-slider:before {{
        position: absolute;
        content: "";
        height: 16px;
        width: 16px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: .4s;
        border-radius: 50%;
    }}
    
    input:checked + .toggle-slider {{
        background-color: #4299E1;
    }}
    
    input:checked + .toggle-slider:before {{
        transform: translateX(20px);
    }}
    
    /* BUTTONS */
    .action-button {{
        width: 100%;
        padding: 0.875rem;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }}
    
    .btn-primary {{
        background: #4299E1;
        color: white;
    }}
    
    .btn-primary:hover {{
        background: #3182CE;
        transform: translateY(-1px);
    }}
    
    .btn-success {{
        background: #38A169;
        color: white;
    }}
    
    .btn-success:hover {{
        background: #2F855A;
        transform: translateY(-1px);
    }}
    
    .btn-warning {{
        background: #ED8936;
        color: white;
    }}
    
    .btn-warning:hover {{
        background: #DD6B20;
        transform: translateY(-1px);
    }}
    
    .btn-danger {{
        background: #F56565;
        color: white;
    }}
    
    .btn-danger:hover {{
        background: #E53E3E;
        transform: translateY(-1px);
    }}
    
    .btn-vip {{
        background: linear-gradient(135deg, #D69E2E, #ECC94B);
        color: #744210;
    }}
    
    .btn-vip:hover {{
        background: linear-gradient(135deg, #B7791F, #D69E2E);
    }}
    
    /* STATS GRID */
    .stats-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-top: auto;
    }}
    
    .stat-card {{
        background: #F7FAFC;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }}
    
    .stat-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #2D3748;
        line-height: 1;
    }}
    
    .stat-label {{
        font-size: 0.75rem;
        color: #718096;
        margin-top: 0.25rem;
    }}
    
    /* CENTER PANEL - QUEUE */
    .queue-container {{
        flex: 1;
        overflow-y: auto;
        padding-right: 0.5rem;
        margin-top: 0.5rem;
    }}
    
    .queue-container::-webkit-scrollbar {{
        width: 6px;
    }}
    
    .queue-container::-webkit-scrollbar-track {{
        background: #F7FAFC;
        border-radius: 3px;
    }}
    
    .queue-container::-webkit-scrollbar-thumb {{
        background: #CBD5E0;
        border-radius: 3px;
    }}
    
    .ticket-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s;
        animation: slideIn 0.3s ease-out;
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-10px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    .ticket-card.active {{
        border-color: #4299E1;
        background: linear-gradient(135deg, #EBF8FF, #FFFFFF);
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.15);
    }}
    
    .ticket-card.vip {{
        border-color: #D69E2E;
        background: linear-gradient(135deg, #FEFCBF, #FFFFFF);
    }}
    
    .ticket-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }}
    
    .ticket-id {{
        font-size: 0.75rem;
        color: #718096;
        font-weight: 600;
    }}
    
    .ticket-status {{
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        background: #E2E8F0;
        color: #4A5568;
    }}
    
    .ticket-status.active {{
        background: #4299E1;
        color: white;
    }}
    
    .ticket-content {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .ticket-avatar {{
        font-size: 2rem;
    }}
    
    .ticket-info {{
        flex: 1;
    }}
    
    .ticket-name {{
        font-weight: 700;
        color: #2D3748;
        margin-bottom: 0.25rem;
    }}
    
    .ticket-details {{
        display: flex;
        gap: 1rem;
        font-size: 0.875rem;
        color: #718096;
    }}
    
    .vip-badge {{
        background: #FEFCBF;
        color: #744210;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }}
    
    .empty-state {{
        text-align: center;
        padding: 3rem 1rem;
        color: #A0AEC0;
    }}
    
    .empty-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }}
    
    /* RIGHT PANEL - HISTORY */
    .history-container {{
        flex: 1;
        overflow-y: auto;
        padding-right: 0.5rem;
    }}
    
    .history-item {{
        padding: 1rem;
        border-bottom: 1px solid #E2E8F0;
    }}
    
    .history-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }}
    
    .history-name {{
        font-weight: 600;
        color: #2D3748;
    }}
    
    .history-time {{
        font-size: 0.75rem;
        color: #718096;
    }}
    
    .history-details {{
        font-size: 0.875rem;
        color: #718096;
        margin-bottom: 0.5rem;
    }}
    
    .history-message {{
        font-style: italic;
        color: #4A5568;
        font-size: 0.875rem;
        padding: 0.5rem;
        background: #F7FAFC;
        border-radius: 8px;
        border-left: 3px solid #4299E1;
    }}
    
    /* STATUS BAR */
    .status-bar {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-top: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.875rem;
    }}
    
    .status-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* HIDE STREAMLIT RADIO/DROPDOWN */
    .stRadio > div {{
        display: none;
    }}
    
    .stSelectbox > div {{
        display: none;
    }}
    
    input[type="checkbox"] {{
        display: none;
    }}
</style>
""", unsafe_allow_html=True)

# --- 4. HELPER FUNCTIONS ---

def get_api_key():
    """Get API key from multiple sources"""
    if "API_KEY" in st.secrets:
        return st.secrets["API_KEY"]
    elif "GOOGLE_API_KEY" in os.environ:
        return os.environ["GOOGLE_API_KEY"]
    return None

def get_random_data():
    names = ["Alex Morgan", "Taylor Kim", "Jordan Lee", "Casey Smith", "Riley Jones", "Morgan Chen"]
    avatars = ["👤", "🎭", "🌟", "👑", "🎩", "🕶️"]
    snacks = ["🍿 Popcorn", "🥤 Large Soda", "🍫 Candy Box", "🌭 Hot Dog", "🥨 Pretzel", "🍦 Ice Cream"]
    return random.choice(names), random.choice(avatars), random.choice(snacks)

def get_ai_message(name, snack, theme):
    """Generate welcome message"""
    api_key = get_api_key()
    
    if not api_key or not HAS_GENAI_LIB:
        fallbacks = [
            f"Enjoy the show, {name.split()[0]}!",
            f"Your {snack} is ready!",
            "Lights, camera, action!",
            f"Welcome to Neon Cinema!",
            "Enjoy your movie! 🎬"
        ]
        return random.choice(fallbacks)
    
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"Very brief (max 5 words) cinema welcome for {name}. They ordered {snack}."
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text.strip()
    except:
        return f"Welcome, {name.split()[0]}!"

def enqueue():
    name, avatar, snack = get_random_data()
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
    
    if is_vip and len(st.session_state.queue) > 0:
        st.session_state.queue.insert(1, new_ticket)
    else:
        st.session_state.queue.append(new_ticket)
        
    st.session_state.vip_mode = False

def dequeue():
    if not st.session_state.queue:
        return None

    person = st.session_state.queue.pop(0)
    msg = get_ai_message(person['name'], person['snack'], st.session_state.current_theme)
    person['out_time'] = datetime.now().strftime("%I:%M %p")
    person['message'] = msg
    
    st.session_state.history.insert(0, person)
    
    if len(st.session_state.history) % 3 == 0:
        st.balloons()
    
    return person

def reset():
    st.session_state.queue = []
    st.session_state.history = []
    st.session_state.ticket_id = 101
    st.session_state.vip_mode = False

# --- 5. HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="cinema-header">
        <div class="header-title">
            <span>🎬</span>
            <span>Neon Cinema Live</span>
        </div>
        <div class="header-subtitle">
            Real-time Queue Management System
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 6. MAIN GRID LAYOUT ---
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# --- LEFT COLUMN: CONTROLS ---
col_left, col_center, col_right = st.columns([320, 1, 320])

with col_left:
    # Controls Panel
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    # Panel Header
    st.markdown("""
    <div class="panel-header">
        <div class="panel-title">Controls</div>
        <div class="badge">Live</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme Selection
    st.markdown('<div class="control-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Theme</div>', unsafe_allow_html=True)
    
    themes_col1, themes_col2 = st.columns(2)
    for i, (theme_name, theme_gradient) in enumerate(THEMES.items()):
        is_active = theme_name == st.session_state.current_theme
        active_class = "active" if is_active else ""
        
        if i % 2 == 0:
            with themes_col1:
                if st.button(f"🎨 {theme_name}", key=f"theme_{theme_name}", 
                           use_container_width=True, type="primary" if is_active else "secondary"):
                    st.session_state.current_theme = theme_name
                    st.rerun()
        else:
            with themes_col2:
                if st.button(f"🎨 {theme_name}", key=f"theme_{theme_name}", 
                           use_container_width=True, type="primary" if is_active else "secondary"):
                    st.session_state.current_theme = theme_name
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # VIP Toggle
    st.markdown('<div class="control-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">VIP Mode</div>', unsafe_allow_html=True)
    
    vip_col1, vip_col2 = st.columns([3, 1])
    with vip_col1:
        st.markdown(f"""
        <div class="toggle-label">
            <span>🌟</span>
            <span>{'VIP Mode Active' if st.session_state.vip_mode else 'VIP Mode Inactive'}</span>
        </div>
        """, unsafe_allow_html=True)
    with vip_col2:
        if st.button("Toggle", key="vip_toggle", use_container_width=True):
            st.session_state.vip_mode = not st.session_state.vip_mode
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons
    st.markdown('<div class="control-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Actions</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add Guest to Queue", type="primary", use_container_width=True):
        enqueue()
        st.rerun()
    
    if st.button("🎟️ Serve Next Guest", type="secondary", use_container_width=True):
        dequeue()
        st.rerun()
    
    if st.button("🔄 Reset System", type="secondary", use_container_width=True):
        reset()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics
    st.markdown('<div class="control-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Statistics</div>', unsafe_allow_html=True)
    
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        queue_len = len(st.session_state.queue)
        wait_time = max(0, queue_len - 1) * 2
        
        st.markdown(f"""
        <div style="background: #F7FAFC; border-radius: 12px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #2D3748;">{queue_len}</div>
            <div style="font-size: 0.75rem; color: #718096; margin-top: 0.25rem;">In Queue</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: #F7FAFC; border-radius: 12px; padding: 1rem; text-align: center; margin-top: 0.75rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #2D3748;">{len(st.session_state.history)}</div>
            <div style="font-size: 0.75rem; color: #718096; margin-top: 0.25rem;">Served</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown(f"""
        <div style="background: #F7FAFC; border-radius: 12px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #2D3748;">{wait_time}m</div>
            <div style="font-size: 0.75rem; color: #718096; margin-top: 0.25rem;">Wait Time</div>
        </div>
        """, unsafe_allow_html=True)
        
        vip_count = len([h for h in st.session_state.history if h.get('is_vip', False)])
        st.markdown(f"""
        <div style="background: #F7FAFC; border-radius: 12px; padding: 1rem; text-align: center; margin-top: 0.75rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #2D3748;">{vip_count}</div>
            <div style="font-size: 0.75rem; color: #718096; margin-top: 0.25rem;">VIP Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close panel

# --- CENTER COLUMN: QUEUE ---
with col_center:
    # Queue Panel
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    # Panel Header
    queue_count = len(st.session_state.queue)
    st.markdown(f"""
    <div class="panel-header">
        <div class="panel-title">Live Queue</div>
        <div class="badge">{queue_count} waiting</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Queue Content
    st.markdown('<div class="queue-container">', unsafe_allow_html=True)
    
    if not st.session_state.queue:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎭</div>
            <div style="font-weight: 600; color: #4A5568; margin-bottom: 0.5rem;">Queue is Empty</div>
            <div style="font-size: 0.875rem; color: #718096;">Add guests to start serving</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, ticket in enumerate(st.session_state.queue):
            is_active = (i == 0)
            is_vip = ticket['is_vip']
            
            card_class = "ticket-card"
            if is_active:
                card_class += " active"
            if is_vip:
                card_class += " vip"
            
            status_text = "NOW SERVING" if is_active else f"WAITING #{i}"
            status_class = "active" if is_active else ""
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="ticket-header">
                    <div class="ticket-id">#{ticket['id']}</div>
                    <div class="ticket-status {status_class}">{status_text}</div>
                </div>
                <div class="ticket-content">
                    <div class="ticket-avatar">{ticket['avatar']}</div>
                    <div class="ticket-info">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                            <div class="ticket-name">{ticket['name']}</div>
                            {f'<div class="vip-badge">VIP</div>' if is_vip else ''}
                        </div>
                        <div class="ticket-details">
                            <span>{ticket['snack']}</span>
                            <span>•</span>
                            <span>{ticket['joined']}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close queue container
    st.markdown('</div>', unsafe_allow_html=True)  # Close panel

# --- RIGHT COLUMN: HISTORY ---
with col_right:
    # History Panel
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    # Panel Header
    history_count = len(st.session_state.history)
    st.markdown(f"""
    <div class="panel-header">
        <div class="panel-title">Recently Served</div>
        <div class="badge">{history_count} total</div>
    </div>
    """, unsafe_allow_html=True)
    
    # History Content
    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📋</div>
            <div style="font-weight: 600; color: #4A5568; margin-bottom: 0.5rem;">No History Yet</div>
            <div style="font-size: 0.875rem; color: #718096;">Serve some guests to see history</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, item in enumerate(st.session_state.history[:6]):  # Show last 6
            if i > 0:
                st.markdown('<hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #E2E8F0;">', unsafe_allow_html=True)
            
            vip_icon = "🌟 " if item['is_vip'] else ""
            
            st.markdown(f"""
            <div class="history-item">
                <div class="history-header">
                    <div class="history-name">{vip_icon}{item['name']}</div>
                    <div class="history-time">{item['out_time']}</div>
                </div>
                <div class="history-details">
                    #{item['id']} • {item['snack']}
                </div>
                <div class="history-message">
                    "{item['message']}"
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close history container
    st.markdown('</div>', unsafe_allow_html=True)  # Close panel

st.markdown('</div>', unsafe_allow_html=True)  # Close main grid

# --- 7. STATUS BAR ---
st.markdown("""
<div class="status-bar">
    <div class="status-item">
        <span>🎬</span>
        <span>System Status: <strong>Operational</strong></span>
    </div>
    <div class="status-item">
        <span>🤖</span>
        <span>AI: <strong>{ai_status}</strong></span>
    </div>
    <div class="status-item">
        <span>⏱️</span>
        <span>Next: <strong>{next_guest}</strong></span>
    </div>
</div>
""".format(
    ai_status="Active" if get_api_key() and HAS_GENAI_LIB else "Disabled",
    next_guest=st.session_state.queue[0]['name'] if st.session_state.queue else "None"
), unsafe_allow_html=True)
