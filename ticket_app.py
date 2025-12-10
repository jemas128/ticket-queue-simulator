import streamlit as st
import random
from datetime import datetime
import os

# Try to import Google GenAI, handle if not installed or key missing
try:
    from google import genai
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
}

if 'queue' not in st.session_state: st.session_state.queue = []
if 'history' not in st.session_state: st.session_state.history = []
if 'ticket_id' not in st.session_state: st.session_state.ticket_id = 101
if 'vip_mode' not in st.session_state: st.session_state.vip_mode = False
if 'current_theme' not in st.session_state: st.session_state.current_theme = "Neon City"

# --- 3. COMPACT CUSTOM CSS ---
theme_bg = THEMES[st.session_state.current_theme]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Poppins:wght@900&display=swap');

    /* COMPACT LAYOUT */
    .stApp {{
        background: {theme_bg};
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Nunito', sans-serif;
        overflow: hidden !important;
        min-height: 100vh !important;
    }}
    
    /* Force no scroll */
    .main .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 95% !important;
    }}
    
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* HIDE ALL STREAMLIT ELEMENTS */
    header {{visibility: hidden; height: 0px !important;}}
    footer {{visibility: hidden; height: 0px !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stVerticalBlock"] > div:nth-last-child(1) {{height: 0px !important;}}
    [data-testid="stToolbar"] {{display: none !important;}}

    /* COMPACT GLASS PANELS */
    .glass-panel {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
        border-radius: 16px;
        padding: 16px !important;
        margin-bottom: 12px !important;
        height: fit-content;
        max-height: 300px;
        overflow: hidden;
    }}

    /* COMPACT TYPOGRAPHY */
    .hero-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem !important;
        font-weight: 900;
        color: white;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 2px !important;
        line-height: 1.1 !important;
        padding-top: 0 !important;
    }}
    
    .hero-subtitle {{
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-weight: 700;
        font-size: 0.9rem !important;
        margin-bottom: 15px !important;
    }}

    /* COMPACT BUTTONS */
    .stButton > button {{
        width: 100%;
        border-radius: 12px !important;
        height: 42px !important;
        font-weight: 700 !important;
        border: none;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: white;
        transition: all 0.2s;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
        font-size: 0.85rem !important;
        padding: 0 10px !important;
        margin: 0 !important;
    }}
    
    /* Primary (Serve) - Orange/Gold */
    .serve-button .stButton > button {{
        background: linear-gradient(135deg, #FF9966 0%, #FF5E62 100%);
    }}
    
    /* Secondary (Add) - Blue */
    .add-button .stButton > button {{
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }}

    /* VIP Button */
    .vip-button .stButton > button {{
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        font-size: 0.8rem !important;
    }}

    /* Reset Button - Red */
    .reset-button .stButton > button {{
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        font-size: 0.8rem !important;
    }}

    /* COMPACT QUEUE CARDS */
    .queue-container {{
        max-height: 210px !important;
        overflow-y: auto !important;
        padding-right: 5px !important;
        margin: 0 !important;
    }}
    
    .queue-container::-webkit-scrollbar {{
        width: 4px;
    }}
    
    .queue-container::-webkit-scrollbar-track {{
        background: rgba(255,255,255,0.1);
        border-radius: 2px;
    }}
    
    .queue-container::-webkit-scrollbar-thumb {{
        background: rgba(0,0,0,0.2);
        border-radius: 2px;
    }}

    .ticket-card {{
        background: white;
        border-radius: 12px;
        padding: 10px 12px !important;
        margin-bottom: 8px !important;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #e0e0e0;
        animation: popIn 0.3s ease-out forwards;
        min-height: 60px !important;
    }}

    @keyframes popIn {{
        from {{ opacity: 0; transform: scale(0.95); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}

    .ticket-active {{
        border-left: 5px solid #00C9FF !important;
        background: linear-gradient(to right, #FFFDE4, #FFFFFF);
        box-shadow: 0 5px 12px rgba(0,0,0,0.1);
        border: 1.5px solid rgba(0, 201, 255, 0.3) !important;
    }}

    .ticket-vip {{
        border-left: 5px solid #FFD700 !important;
        background: #fffcf0 !important;
        border: 1.5px solid #FFD700 !important;
    }}

    .t-avatar {{ 
        font-size: 1.8rem !important; 
        margin-right: 10px !important; 
        min-width: 40px !important;
        text-align: center;
    }}
    
    .t-info {{ 
        flex-grow: 1; 
        min-width: 0;
    }}
    
    .t-name {{ 
        font-weight: 800 !important; 
        color: #333; 
        font-size: 0.95rem !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    
    .t-meta {{ 
        font-size: 0.7rem !important; 
        color: #666; 
        display: flex; 
        gap: 8px;
        flex-wrap: wrap;
    }}
    
    .badge {{ 
        background: #eee; 
        padding: 2px 6px !important; 
        border-radius: 4px; 
        font-size: 0.65rem !important; 
        font-weight: 700; 
        text-transform: uppercase;
        white-space: nowrap;
    }}

    /* COMPACT HISTORY */
    .history-container {{
        max-height: 160px !important;
        overflow-y: auto !important;
        padding-right: 5px !important;
        margin: 0 !important;
    }}

    .history-item {{
        padding: 8px 0 !important;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        font-size: 0.8rem !important;
        line-height: 1.2 !important;
    }}
    
    .ai-msg {{
        font-style: italic;
        color: #555;
        background: rgba(255,255,255,0.5);
        padding: 5px 8px !important;
        border-radius: 6px;
        margin-top: 3px !important;
        border-left: 3px solid #8A2387;
        font-size: 0.75rem !important;
        line-height: 1.1 !important;
    }}

    /* COMPACT STATS */
    .stat-card {{
        background: white;
        border-radius: 10px;
        padding: 10px !important;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 3px !important;
        height: 65px !important;
    }}
    
    .stat-number {{
        font-size: 1.5rem !important;
        font-weight: 900;
        color: #333;
        line-height: 1.2 !important;
    }}
    
    .stat-label {{
        font-size: 0.65rem !important;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* TIGHT COLUMNS */
    [data-testid="column"] {{
        padding: 0 8px !important;
    }}
    
    /* SMALL DIVIDERS */
    .compact-divider {{
        margin: 8px 0 !important;
        border-color: rgba(255,255,255,0.2) !important;
    }}

    /* FORM CONTROLS */
    .stSelectbox {{
        margin-bottom: 10px !important;
    }}
    
    .stSelectbox > div > div {{
        padding: 6px 10px !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
    }}

    /* NO EMPTY SPACE */
    .empty-space {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 4. COMPACT HELPERS ---

def get_api_key():
    """Get API key from multiple sources"""
    if "API_KEY" in st.secrets:
        return st.secrets["API_KEY"]
    elif "GOOGLE_API_KEY" in os.environ:
        return os.environ["GOOGLE_API_KEY"]
    return None

def get_random_data():
    names = ["Kai", "Luna", "Milo", "Nova", "Leo", "Mia", "Zane", "Cleo", "Jax", "Ivy"]
    avatars = ["🐼", "🦊", "🦄", "🦁", "🐯", "🐸", "🐙", "🐵", "🐨", "🐷"]
    snacks = ["🍿", "🥤", "🌭", "🥨", "🍫", "🌮"]
    return random.choice(names), random.choice(avatars), random.choice(snacks)

def get_ai_message(name, snack, theme):
    """Generates a message using Gemini or fallback"""
    api_key = get_api_key()
    
    if not api_key or not HAS_GENAI_LIB:
        fallbacks = [
            f"Enjoy {snack}, {name}!",
            f"Welcome {name}!",
            "Showtime!",
            f"{snack} ready!",
            "Enjoy the show!"
        ]
        return random.choice(fallbacks)

    try:
        client = genai.Client(api_key=api_key)
        prompt = f"Very short cinema welcome for {name}. Snack: {snack}. Theme: {theme}. Max 5 words."
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text.strip()[:50]
    except:
        return f"Welcome {name}!"

def enqueue():
    name, avatar, snack = get_random_data()
    is_vip = st.session_state.vip_mode
    
    new_ticket = {
        "id": st.session_state.ticket_id,
        "name": name,
        "avatar": avatar,
        "snack": snack,
        "joined": datetime.now().strftime("%I:%M"),
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
    person['out_time'] = datetime.now().strftime("%I:%M")
    person['message'] = msg
    
    st.session_state.history.insert(0, person)
    
    if len(st.session_state.history) % 5 == 0:
        st.balloons()
    
    return person

def reset():
    st.session_state.queue = []
    st.session_state.history = []
    st.session_state.ticket_id = 101
    st.session_state.vip_mode = False

# --- 5. ULTRA-COMPACT LAYOUT ---

# Header (Very Compact)
col_head1, col_head2, col_head3 = st.columns([1, 2, 1])
with col_head2:
    st.markdown('<div class="hero-title">🎬 NEON CINEMA</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-subtitle">Live Queue System • {st.session_state.current_theme}</div>', unsafe_allow_html=True)

# Main Content in 3 Columns
col1, col2, col3 = st.columns([1.1, 1.4, 1], gap="small")

# --- COLUMN 1: CONTROLS ---
with col1:
    # Theme Selector (Very Compact)
    with st.container():
        st.markdown("**🎨 THEME**")
        selected_theme = st.selectbox(
            "", 
            list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.current_theme),
            label_visibility="collapsed"
        )
        if selected_theme != st.session_state.current_theme:
            st.session_state.current_theme = selected_theme
            st.rerun()
    
    st.markdown('<div class="compact-divider"></div>', unsafe_allow_html=True)
    
    # VIP Toggle
    st.markdown("**🌟 VIP MODE**")
    vip_col1, vip_col2 = st.columns([2, 1])
    with vip_col1:
        vip_status = "ACTIVE" if st.session_state.vip_mode else "OFF"
        vip_color = "#FFD700" if st.session_state.vip_mode else "#666"
        st.markdown(f'<div style="color:{vip_color}; font-weight:bold; font-size:0.9rem;">{vip_status}</div>', unsafe_allow_html=True)
    with vip_col2:
        if st.button("Toggle", use_container_width=True):
            st.session_state.vip_mode = not st.session_state.vip_mode
            st.rerun()
    
    st.markdown('<div class="compact-divider"></div>', unsafe_allow_html=True)
    
    # Action Buttons
    st.markdown("**🕹️ ACTIONS**")
    
    with st.container():
        if st.button("➕ ADD GUEST", use_container_width=True):
            enqueue()
            st.rerun()
    
    with st.container():
        if st.button("🎟️ SERVE NEXT", use_container_width=True):
            dequeue()
            st.rerun()
    
    st.markdown('<div class="compact-divider"></div>', unsafe_allow_html=True)
    
    # Compact Stats
    st.markdown("**📊 LIVE STATS**")
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        queue_len = len(st.session_state.queue)
        wait_time = max(0, queue_len - 1) * 2
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{queue_len}</div>
            <div class="stat-label">In Queue</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(st.session_state.history)}</div>
            <div class="stat-label">Served</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{wait_time}m</div>
            <div class="stat-label">Wait Time</div>
        </div>
        """, unsafe_allow_html=True)
        
        vip_count = len([h for h in st.session_state.history if h.get('is_vip', False)])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{vip_count}</div>
            <div class="stat-label">VIP Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Reset Button (Bottom)
    with st.container():
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("🔄 RESET ALL", use_container_width=True):
            reset()
            st.rerun()

# --- COLUMN 2: QUEUE ---
with col2:
    st.markdown('<div class="glass-panel" style="padding:12px !important;">', unsafe_allow_html=True)
    st.markdown(f"**🎪 LIVE QUEUE ({len(st.session_state.queue)})**")
    
    if not st.session_state.queue:
        st.markdown("""
        <div style="text-align:center; padding:20px 10px;">
            <div style="font-size:2rem; opacity:0.5;">💤</div>
            <div style="font-size:0.9rem; color:#666; margin-top:5px;">Queue is empty</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="queue-container">', unsafe_allow_html=True)
        for i, ticket in enumerate(st.session_state.queue[:6]):  # Show max 6
            is_first = (i == 0)
            is_vip = ticket['is_vip']
            
            card_class = "ticket-card"
            if is_first: card_class += " ticket-active"
            if is_vip: card_class += " ticket-vip"
            
            status_badge = "NOW" if is_first else f"#{i}"
            badge_color = "#00C9FF" if is_first else "#eee"
            text_color = "white" if is_first else "#555"
            
            vip_badge = ' <span class="badge" style="background:#FFD700; color:#B8860B;">VIP</span>' if is_vip else ""
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="t-avatar">{ticket['avatar']}</div>
                <div class="t-info">
                    <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
                        <span style="font-weight:900; font-size:0.9rem;">{ticket['name']}{vip_badge}</span>
                        <span class="badge" style="background:{badge_color}; color:{text_color};">{status_badge}</span>
                    </div>
                    <div class="t-meta">
                        <span>#{ticket['id']}</span> • 
                        <span>{ticket['snack']}</span> • 
                        <span>{ticket['joined']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(st.session_state.queue) > 6:
            st.caption(f"+ {len(st.session_state.queue) - 6} more in queue")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMN 3: HISTORY ---
with col3:
    st.markdown('<div class="glass-panel" style="padding:12px !important;">', unsafe_allow_html=True)
    st.markdown(f"**✅ RECENTLY SERVED ({len(st.session_state.history)})**")
    
    if not st.session_state.history:
        st.caption("No history yet", help="Serve some guests to see history here")
    else:
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        for item in st.session_state.history[:4]:  # Show max 4
            vip_icon = "🌟" if item['is_vip'] else ""
            
            st.markdown(f"""
            <div class="history-item">
                <div style="font-weight:bold; color:#333; display:flex; justify-content:space-between;">
                    <span>{item['name']} {vip_icon}</span>
                    <span style="font-size:0.7rem; color:#999;">{item['out_time']}</span>
                </div>
                <div style="font-size:0.7rem; color:#666;">{item['snack']}</div>
                <div class="ai-msg">{item['message'][:40]}{"..." if len(item['message']) > 40 else ""}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(st.session_state.history) > 4:
            st.caption(f"+ {len(st.session_state.history) - 4} more served")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Status
    api_status = "✅" if get_api_key() and HAS_GENAI_LIB else "❌"
    next_guest = st.session_state.queue[0]['name'] if st.session_state.queue else "None"
    
    st.markdown("""
    <div style="background:rgba(255,255,255,0.7); padding:10px; border-radius:10px; margin-top:8px;">
        <div style="font-size:0.8rem; color:#333; display:flex; justify-content:space-between;">
            <span><strong>AI:</strong> {api_status}</span>
            <span><strong>Next:</strong> {next_guest}</span>
        </div>
    </div>
    """.format(api_status=api_status, next_guest=next_guest), unsafe_allow_html=True)

# Bottom spacer (minimal)
st.markdown('<div style="height:5px"></div>', unsafe_allow_html=True)
