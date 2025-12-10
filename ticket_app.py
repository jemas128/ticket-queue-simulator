import streamlit as st
import random
import os
from datetime import datetime
from google import genai

# --- 1. ENHANCED PAGE SETUP ---
st.set_page_config(
    page_title="🎬 Neon Cinema AI Queue", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. REFINED THEME SYSTEM ---
THEMES = {
    "neon": { 
        "name": "Neon City", 
        "bg": "linear-gradient(-45deg, #FF3CAC, #784BA0, #2B86C5, #23d5ab)",
        "accent": "#00f2fe",
        "secondary": "#FF3CAC",
        "mood": "🌃 Cyberpunk Night"
    },
    "sunset": { 
        "name": "Sunset Strip", 
        "bg": "linear-gradient(-45deg, #FF512F, #DD2476, #F09819, #FF512F)",
        "accent": "#FF512F",
        "secondary": "#F09819",
        "mood": "🌅 Hollywood Glam"
    },
    "ocean": { 
        "name": "Cyber Ocean", 
        "bg": "linear-gradient(-45deg, #00c6ff, #0072ff, #1cb5e0, #000046)",
        "accent": "#00c6ff",
        "secondary": "#0072ff",
        "mood": "🌊 Digital Waves"
    },
    "forest": { 
        "name": "Toxic Jungle", 
        "bg": "linear-gradient(-45deg, #11998e, #38ef7d, #00b09b, #96c93d)",
        "accent": "#38ef7d",
        "secondary": "#11998e",
        "mood": "🌿 Bio-Luminescent"
    },
    "synthwave": { 
        "name": "Synthwave", 
        "bg": "linear-gradient(-45deg, #FF0080, #FF8C00, #40E0D0, #9370DB)",
        "accent": "#FF0080",
        "secondary": "#40E0D0",
        "mood": "🎵 Retro Future"
    }
}

# Initialize Enhanced Session State
if 'queue' not in st.session_state: 
    st.session_state.queue = []
if 'history' not in st.session_state: 
    st.session_state.history = []
if 'ticket_id' not in st.session_state: 
    st.session_state.ticket_id = 101
if 'current_theme' not in st.session_state: 
    st.session_state.current_theme = "synthwave"
if 'vip_mode' not in st.session_state: 
    st.session_state.vip_mode = False
if 'ai_enabled' not in st.session_state: 
    st.session_state.ai_enabled = True
if 'animations' not in st.session_state: 
    st.session_state.animations = True
if 'total_served' not in st.session_state: 
    st.session_state.total_served = 0
if 'peak_queue' not in st.session_state: 
    st.session_state.peak_queue = 0

# --- 3. ENHANCED CSS WITH MODERN DESIGN ---
current_theme = THEMES[st.session_state.current_theme]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');

    /* MAIN BACKGROUND WITH PARALLAX EFFECT */
    .stApp {{
        background: {current_theme['bg']};
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow-x: hidden;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 50%);
        pointer-events: none;
    }}

    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* GLASS MORPHISM PANELS */
    .glass-panel {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }}

    .glass-panel:hover {{
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }}

    /* HEADER WITH GLOW EFFECT */
    .hero-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        color: white;
        text-shadow: 
            0 0 20px {current_theme['accent']},
            0 0 40px {current_theme['accent']}80,
            0 0 60px {current_theme['accent']}40;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
        animation: textGlow 3s ease-in-out infinite alternate;
    }}

    @keyframes textGlow {{
        from {{ text-shadow: 0 0 20px {current_theme['accent']}; }}
        to {{ text-shadow: 0 0 30px {current_theme['accent']}, 0 0 40px {current_theme['accent']}; }}
    }}

    /* SUBTITLE */
    .hero-subtitle {{
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 40px;
        letter-spacing: 1px;
    }}

    /* ENHANCED BUTTONS WITH GRADIENTS */
    div.stButton > button {{
        width: 100%;
        border-radius: 16px;
        height: 56px;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        background: linear-gradient(135deg, {current_theme['accent']}, {current_theme['secondary']});
        color: white;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }}

    div.stButton > button:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }}

    div.stButton > button:active {{
        transform: translateY(-2px);
    }}

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

    /* SPECIAL VIP BUTTON */
    .vip-button {{
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
    }}

    /* PRIMARY ACTION BUTTON */
    .primary-button {{
        background: linear-gradient(135deg, #00ff88, #00ccff) !important;
        font-size: 1.1rem !important;
        height: 60px !important;
    }}

    /* TICKET CARDS WITH ENHANCED DESIGN */
    .ticket-card {{
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        border-left: 10px solid #e0e0e0;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    .ticket-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
    }}

    @keyframes slideIn {{
        from {{ 
            opacity: 0; 
            transform: translateY(30px) rotateX(-10deg);
        }}
        to {{ 
            opacity: 1; 
            transform: translateY(0) rotateX(0);
        }}
    }}

    .ticket-active {{
        border-left: 10px solid {current_theme['accent']};
        background: linear-gradient(135deg, #ffffff, #f0f9ff);
        box-shadow: 
            0 0 30px {current_theme['accent']}40,
            0 10px 30px rgba(0, 0, 0, 0.1);
        transform: scale(1.02);
        animation: pulseGlow 2s infinite;
    }}

    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 30px {current_theme['accent']}40; }}
        50% {{ box-shadow: 0 0 40px {current_theme['accent']}60; }}
    }}
    
    .ticket-vip {{
        border: 2px solid #FFD700;
        border-left: 10px solid #FFD700;
        background: linear-gradient(135deg, #fffdf0, #fff8e1);
        position: relative;
    }}

    .ticket-vip::after {{
        content: '🌟 VIP';
        position: absolute;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #B8860B;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    .avatar {{
        font-size: 2.8rem;
        margin-right: 20px;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        animation: float 3s ease-in-out infinite;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
    }}

    .ticket-info {{ 
        flex-grow: 1; 
    }}

    .ticket-id {{
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 1.4rem;
        color: #222;
        letter-spacing: 1px;
    }}

    .ticket-meta {{
        font-size: 0.85rem;
        color: #666;
        margin-top: 4px;
        display: flex;
        gap: 12px;
    }}

    /* STATUS BADGES */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    .status-serving {{
        background: linear-gradient(135deg, {current_theme['accent']}, {current_theme['secondary']});
        color: white;
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}

    .status-waiting {{
        background: #f0f0f0;
        color: #666;
    }}

    /* HISTORY SECTION */
    .history-item {{
        background: linear-gradient(135deg, rgba(255,255,255,0.6), rgba(255,255,255,0.4));
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }}

    .history-item:hover {{
        transform: translateX(4px);
        background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.6));
    }}

    .ai-msg {{
        font-style: italic;
        color: #444;
        background: rgba(255,255,255,0.7);
        padding: 10px 15px;
        border-radius: 12px;
        margin-top: 8px;
        border-left: 4px solid {current_theme['accent']};
        font-size: 0.9rem;
        position: relative;
    }}

    .ai-msg::before {{
        content: '🤖 AI: ';
        font-weight: bold;
        color: {current_theme['accent']};
    }}

    /* STATS CARDS */
    .stat-card {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.4);
    }}

    .stat-card:hover {{
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.95);
    }}

    .stat-value {{
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, {current_theme['accent']}, {current_theme['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }}

    .stat-label {{
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }}

    /* THEME SELECTOR */
    .theme-option {{
        padding: 12px;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        background: rgba(255,255,255,0.1);
        margin-bottom: 8px;
    }}

    .theme-option:hover {{
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }}

    .theme-option.active {{
        border-color: white;
        background: rgba(255,255,255,0.3);
    }}

    /* HIDE STREAMLIT DEFAULT ELEMENTS */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    .main > div {{padding-top: 1rem;}}

    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }}

    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.5);
    }}

    /* LOADING STATE */
    .loading-dots {{
        display: inline-block;
    }}

    .loading-dots::after {{
        content: '.';
        animation: dots 1.5s steps(4, end) infinite;
    }}

    @keyframes dots {{
        0%, 20% {{ content: '.'; }}
        40% {{ content: '..'; }}
        60% {{ content: '...'; }}
        80%, 100% {{ content: ''; }}
    }}
</style>
""", unsafe_allow_html=True)

# --- 4. ENHANCED LOGIC FUNCTIONS ---
NAMES = ["Kai", "Luna", "Milo", "Nova", "Leo", "Mia", "Zane", "Cleo", "Jax", "Ivy", "Finn"]
AVATARS = ["🐼", "🦊", "🦄", "🦁", "🐯", "🐸", "🐙", "🐵", "🐨", "🤖", "👽"]
SNACKS = ["Popcorn 🍿", "Nachos 🌮", "Soda 🥤", "Candy 🍫", "Hotdog 🌭", "Pretzel 🥨", "Ice Cream 🍦"]
MOVIES = ["Matrix", "Inception", "Blade Runner", "Star Wars", "Avatar", "Interstellar"]

def enqueue():
    name = random.choice(NAMES)
    avatar = random.choice(AVATARS)
    snack = random.choice(SNACKS)
    movie = random.choice(MOVIES)
    is_vip = st.session_state.vip_mode
    
    new_ticket = {
        "id": st.session_state.ticket_id,
        "name": name,
        "avatar": avatar,
        "snack": snack,
        "movie": movie,
        "joined": datetime.now().strftime("%I:%M %p"),
        "joined_full": datetime.now().isoformat(),
        "is_vip": is_vip,
        "waiting_since": datetime.now()
    }
    
    st.session_state.ticket_id += 1
    
    # VIP Logic with visual feedback
    if is_vip:
        if len(st.session_state.queue) > 0:
            # Insert at position 1 (after currently serving)
            st.session_state.queue.insert(1, new_ticket)
        else:
            st.session_state.queue.append(new_ticket)
    else:
        st.session_state.queue.append(new_ticket)
    
    # Update peak queue length
    if len(st.session_state.queue) > st.session_state.peak_queue:
        st.session_state.peak_queue = len(st.session_state.queue)
    
    # Reset VIP mode after adding
    st.session_state.vip_mode = False
    
    # Return the ticket for potential animation
    return new_ticket

def dequeue():
    if not st.session_state.queue:
        return None

    # Pop the first person
    person = st.session_state.queue.pop(0)
    st.session_state.total_served += 1
    
    # Calculate wait time
    wait_time = (datetime.now() - person['waiting_since']).seconds // 60
    
    # AI Message Generation
    ai_message = "Enjoy the movie! 🎬"
    if st.session_state.ai_enabled:
        try:
            api_key = os.environ.get("API_KEY")
            if api_key:
                client = genai.Client(api_key=api_key)
                prompt = f"Create a unique, witty cinema welcome (max 6 words) for {person['name']} who ordered {person['snack']} to watch {person['movie']}. Theme: {current_theme['mood']}."
                response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
                if response.text:
                    ai_message = response.text.strip()
        except Exception:
            ai_message = "The show begins! ✨"

    # Add to history with enhanced data
    person['served_time'] = datetime.now().strftime("%I:%M %p")
    person['ai_msg'] = ai_message
    person['wait_minutes'] = wait_time
    st.session_state.history.insert(0, person)
    
    # Keep history manageable
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]
    
    return person

# --- 5. ENHANCED UI COMPONENTS ---

def theme_selector():
    """Enhanced theme selector component"""
    st.markdown("### 🎨 Vibe Selector")
    cols = st.columns(len(THEMES))
    
    for idx, (theme_key, theme_data) in enumerate(THEMES.items()):
        with cols[idx]:
            is_active = (theme_key == st.session_state.current_theme)
            btn_label = f"• {theme_data['name']}" if is_active else theme_data['name']
            
            if st.button(btn_label, key=f"theme_{theme_key}"):
                st.session_state.current_theme = theme_key
                st.rerun()

def stat_display():
    """Enhanced statistics display"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{len(st.session_state.queue)}</div>
            <div class='stat-label'>In Queue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        wait_time = max(0, (len(st.session_state.queue) - 1) * 2)
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{wait_time}m</div>
            <div class='stat-label'>Avg Wait</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{st.session_state.total_served}</div>
            <div class='stat-label'>Total Served</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{st.session_state.peak_queue}</div>
            <div class='stat-label'>Peak Queue</div>
        </div>
        """, unsafe_allow_html=True)

def empty_state():
    """Beautiful empty state"""
    return st.markdown(f"""
    <div class='glass-panel' style='text-align: center; padding: 60px 20px;'>
        <div style='font-size: 5rem; margin-bottom: 20px; opacity: 0.7;'>🎭</div>
        <h3 style='color: #444; margin-bottom: 10px;'>Theater Lobby is Empty</h3>
        <p style='color: #666; max-width: 300px; margin: 0 auto 30px;'>
            Add customers to start the cinematic experience
        </p>
        <div style='font-size: 2rem; opacity: 0.5;'>
            ↓
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 6. MAIN UI LAYOUT ---

# HEADER SECTION
st.markdown(f'<div class="hero-title">NEON CINEMA AI</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-subtitle">Real-time Queue Management • AI-Powered Welcome Messages • {current_theme["mood"]}</div>', unsafe_allow_html=True)

# MAIN COLUMNS
col_ctrl, col_queue, col_hist = st.columns([1, 1.5, 1])

# --- LEFT COLUMN: CONTROLS & SETTINGS ---
with col_ctrl:
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        
        # Theme Selector
        theme_selector()
        
        st.markdown("---")
        
        # VIP Toggle with better visual feedback
        st.markdown("### ⚡ Quick Actions")
        
        col_vip, col_ai = st.columns(2)
        with col_vip:
            vip_status = "🌟 **VIP MODE ON**" if st.session_state.vip_mode else "⚪ VIP Mode"
            vip_color = "#FFD700" if st.session_state.vip_mode else "#ccc"
            if st.button(vip_status, key="vip_toggle", use_container_width=True):
                st.session_state.vip_mode = not st.session_state.vip_mode
                st.rerun()
        
        with col_ai:
            ai_status = "🤖 **AI ON**" if st.session_state.ai_enabled else "⚡ AI OFF"
            if st.button(ai_status, key="ai_toggle", use_container_width=True):
                st.session_state.ai_enabled = not st.session_state.ai_enabled
                st.rerun()
        
        # Add Customer Button (Dynamic)
        add_label = "✨ ADD VIP CUSTOMER" if st.session_state.vip_mode else "👤 ADD CUSTOMER"
        add_icon = "✨" if st.session_state.vip_mode else "👤"
        
        if st.button(f"{add_icon} {add_label}", key="add_customer", type="primary", use_container_width=True):
            new_ticket = enqueue()
            # Optional: Add success animation/notification here
        
        st.markdown("---")
        
        # Serve Button with Primary Styling
        serve_disabled = len(st.session_state.queue) == 0
        serve_text = "🎟️ SERVE NEXT CUSTOMER" if not serve_disabled else "⏳ QUEUE EMPTY"
        
        if st.button(serve_text, 
                    key="serve_next", 
                    disabled=serve_disabled,
                    use_container_width=True,
                    type="primary" if not serve_disabled else "secondary"):
            served = dequeue()
            if served and st.session_state.animations:
                # Could add toast notification here
                pass
        
        st.markdown("---")
        
        # Real-time Stats
        stat_display()
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- CENTER COLUMN: QUEUE DISPLAY ---
with col_queue:
    if not st.session_state.queue:
        empty_state()
    else:
        # Queue Header
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 0 10px;'>
            <h3 style='color: white; margin: 0;'>🎬 NOW SERVING ({len(st.session_state.queue)} in queue)</h3>
            <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>
                Updated: {datetime.now().strftime("%I:%M %p")}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Ticket Cards
        for index, ticket in enumerate(st.session_state.queue):
            is_first = (index == 0)
            
            # Calculate estimated wait time
            wait_position = index
            est_wait = wait_position * 2  # 2 minutes per person
            
            # Card classes
            card_class = "ticket-card"
            if is_first: 
                card_class += " ticket-active"
            if ticket['is_vip']: 
                card_class += " ticket-vip"
            
            # Status badge
            status_class = "status-serving" if is_first else "status-waiting"
            status_text = "NOW SERVING" if is_first else f"#{wait_position + 1} • {est_wait}min wait"
            
            # Ticket content
            st.markdown(f"""
            <div class="{card_class}">
                <div class="avatar">{ticket['avatar']}</div>
                <div class="ticket-info">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <span class="ticket-id">TICKET #{ticket['id']}</span>
                            <span style="margin-left: 10px; font-size: 0.9rem; color: #666;">
                                for {ticket['movie']}
                            </span>
                        </div>
                        <span class="status-badge {status_class}">{status_text}</span>
                    </div>
                    <div style="font-weight: 700; color: #333; font-size: 1.2rem; margin: 8px 0;">
                        {ticket['name']}
                    </div>
                    <div class="ticket-meta">
                        <span style="background: #f0f0f0; padding: 4px 10px; border-radius: 12px;">
                            {ticket['snack']}
                        </span>
                        <span>Joined: {ticket['joined']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- RIGHT COLUMN: HISTORY & INSIGHTS ---
with col_hist:
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        
        st.markdown("### 📜 RECENTLY SERVED")
        
        if not st.session_state.history:
            st.markdown("""
            <div style='text-align: center; padding: 30px 20px; color: #666;'>
                <div style='font-size: 2rem; opacity: 0.5;'>📝</div>
                <p>No customers served yet</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for idx, item in enumerate(st.session_state.history[:6]):
                time_ago = datetime.now() - datetime.fromisoformat(item['joined_full'])
                minutes_ago = int(time_ago.total_seconds() // 60)
                
                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-weight: 700; color: #333;">
                            {item['avatar']} {item['name']}
                            <span style="font-size: 0.8rem; color: #666; margin-left: 5px;">
                                #{item['id']}
                            </span>
                        </div>
                        <div style="font-size: 0.75rem; color: #888;">
                            {minutes_ago}m ago
                        </div>
                    </div>
                    <div style="font-size: 0.85rem; color: #555; margin-bottom: 6px;">
                        🍿 {item['snack']} • 🎬 {item['movie']}
                        <span style="font-size: 0.75rem; color: #888; margin-left: 8px;">
                            waited {item.get('wait_minutes', 0)}m
                        </span>
                    </div>
                    <div class="ai-msg">{item['ai_msg']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 TODAY'S STATS")
        
        if st.session_state.total_served > 0:
            avg_wait = sum(h.get('wait_minutes', 0) for h in st.session_state.history) / len(st.session_state.history[:5])
            vip_count = sum(1 for h in st.session_state.history if h.get('is_vip', False))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Avg Wait Time", f"{avg_wait:.0f} min")
            with col2:
                st.metric("VIP Served", vip_count)
        else:
            st.info("Stats will appear after serving customers")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. FOOTER ---
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 40px; padding: 20px;'>
    <div>NEON CINEMA AI • Version 2.0 • Built with Streamlit & Gemini AI</div>
    <div style='margin-top: 10px; opacity: 0.5;'>
        Every ticket tells a story • Every welcome is unique
    </div>
</div>
""", unsafe_allow_html=True)
