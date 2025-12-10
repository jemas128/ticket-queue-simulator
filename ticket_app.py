import streamlit as st
import time
import random
from datetime import datetime

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Cinema Queue Simulator", page_icon="🎬", layout="wide")

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Custom CSS with gradient, animations, and theme switching
st.markdown(f"""
<style>
    /* Base Theme Variables */
    :root {{
        --primary-color: #ff4b4b;
        --secondary-color: #4CAF50;
        --accent-color: #FFD700;
        --bg-gradient-start: {'#0f0c29' if st.session_state.theme == 'dark' else '#F8F9FA'};
        --bg-gradient-end: {'#302b63' if st.session_state.theme == 'dark' else '#E9ECEF'};
        --card-bg: {'#262730' if st.session_state.theme == 'dark' else '#FFFFFF'};
        --text-color: {'#FFFFFF' if st.session_state.theme == 'dark' else '#000000'};
        --border-color: {'#444' if st.session_state.theme == 'dark' else '#ddd'};
    }}
    
    /* Main Background with Gradient */
    .stApp {{
        background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
        background-attachment: fixed;
        color: var(--text-color);
        transition: all 0.5s ease;
    }}
    
    /* Animated Header */
    @keyframes glow {{
        0%, 100% {{ text-shadow: 0 0 10px var(--primary-color); }}
        50% {{ text-shadow: 0 0 20px var(--primary-color), 0 0 30px var(--primary-color); }}
    }}
    
    .animated-header {{
        animation: glow 2s infinite;
        text-align: center;
        padding: 20px;
        background: linear-gradient(45deg, 
            {'rgba(255, 75, 75, 0.1)' if st.session_state.theme == 'dark' else 'rgba(255, 75, 75, 0.05)'}, 
            {'rgba(76, 175, 80, 0.1)' if st.session_state.theme == 'dark' else 'rgba(76, 175, 80, 0.05)'});
        border-radius: 20px;
        margin-bottom: 30px;
        border: 2px solid {'rgba(255, 75, 75, 0.3)' if st.session_state.theme == 'dark' else 'rgba(255, 75, 75, 0.1)'};
    }}
    
    /* Enhanced Ticket Cards */
    .ticket-card {{
        background: var(--card-bg);
        border: 3px solid var(--primary-color);
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .ticket-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(255, 75, 75, 0.3);
    }}
    
    .ticket-card.vip {{
        background: linear-gradient(45deg, #FFD700, #FFA500);
        border: 3px solid #FFD700;
        color: #000;
    }}
    
    .ticket-card.vip .ticket-number {{
        color: #B8860B;
    }}
    
    .ticket-number {{
        font-size: 24px;
        font-weight: bold;
        color: var(--primary-color);
        margin: 10px 0;
    }}
    
    .ticket-name {{
        font-size: 16px;
        font-weight: 500;
    }}
    
    .vip-badge {{
        position: absolute;
        top: 10px;
        right: 10px;
        background: #FFD700;
        color: #000;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 10px;
        font-weight: bold;
    }}
    
    /* Current Serving Display */
    .current-serving {{
        background: linear-gradient(45deg, 
            {'rgba(209, 255, 189, 0.9)' if st.session_state.theme == 'dark' else 'rgba(209, 255, 189, 0.95)'}, 
            {'rgba(76, 175, 80, 0.9)' if st.session_state.theme == 'dark' else 'rgba(76, 175, 80, 0.95)'});
        color: #1a4a1a;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 3px dashed #4CAF50;
        margin-bottom: 20px;
        font-size: 1.2em;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
    }}
    
    /* Enhanced Buttons */
    .stButton>button {{
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        font-weight: bold;
        font-size: 1.1em;
        margin: 5px 0;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }}
    
    .primary-button {{
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        color: white;
    }}
    
    .vip-button {{
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
        font-weight: bold;
    }}
    
    .secondary-button {{
        background: linear-gradient(45deg, #4CAF50, #66BB6A);
        color: white;
    }}
    
    .theme-button {{
        background: linear-gradient(45deg, #6C63FF, #9A94FF);
        color: white;
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        width: auto !important;
        padding: 10px 20px;
    }}
    
    /* Control Panel Styling */
    .control-panel {{
        background: {'rgba(38, 39, 48, 0.8)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.8)'};
        padding: 25px;
        border-radius: 20px;
        border: 2px solid var(--primary-color);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }}
    
    /* Queue Counter */
    .queue-counter {{
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        font-size: 1.2em;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    /* History Cards */
    .history-card {{
        background: {'rgba(38, 39, 48, 0.6)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.6)'};
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 5px solid var(--secondary-color);
        transition: all 0.3s ease;
    }}
    
    .history-card:hover {{
        transform: translateX(5px);
        background: {'rgba(38, 39, 48, 0.8)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.8)'};
    }}
    
    /* Status Indicator */
    .status-indicator {{
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 10px;
        animation: blink 1s infinite;
    }}
    
    .status-active {{
        background-color: #4CAF50;
    }}
    
    @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (The Memory) ---
if 'queue' not in st.session_state:
    st.session_state.queue = []

if 'history' not in st.session_state:
    st.session_state.history = []

if 'ticket_id' not in st.session_state:
    st.session_state.ticket_id = 100

if 'last_action' not in st.session_state:
    st.session_state.last_action = "Welcome! Queue is empty."

# --- 3. HELPER FUNCTIONS ---

def generate_random_person(is_vip=False):
    names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", 
             "Ian", "Julia", "Kevin", "Luna", "Mike", "Nina", "Oscar", "Paula"]
    emojis = ["👱", "👵", "👮", "🧑‍💻", "🧟", "🧛", "🧙", "🦸", "👨‍🚀", "👩‍🎤", "🕵️", "👩‍🍳", "🧑‍🎨", "👨‍🔬"]
    
    if is_vip:
        names = ["Mr. Smith", "Madame X", "Sir Reginald", "Lady Aurora", "Count Dracula", 
                "Professor X", "Agent 007", "Queen Bee"]
        emojis = ["👑", "🎩", "💎", "🌟", "⭐", "✨", "💼", "🕶️"]
    
    return {
        "name": random.choice(names),
        "avatar": random.choice(emojis),
        "id": st.session_state.ticket_id,
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_vip": is_vip
    }

def enqueue_person(is_vip=False):
    person = generate_random_person(is_vip)
    
    if is_vip:
        # Insert VIP at the front of the queue (after any other VIPs)
        vip_positions = [i for i, p in enumerate(st.session_state.queue) if p.get('is_vip', False)]
        if vip_positions:
            insert_position = vip_positions[-1] + 1
        else:
            insert_position = 0
        st.session_state.queue.insert(insert_position, person)
        st.session_state.last_action = f"⭐ **VIP** Ticket #{person['id']} ({person['name']}) joined with priority!"
    else:
        st.session_state.queue.append(person)
        st.session_state.last_action = f"✅ Ticket #{person['id']} ({person['name']}) joined the line."
    
    st.session_state.ticket_id += 1

def dequeue_person():
    if len(st.session_state.queue) > 0:
        person = st.session_state.queue.pop(0)
        st.session_state.history.insert(0, person)
        status = "⭐ **VIP SERVED**" if person.get('is_vip', False) else "🎟️ Serving"
        st.session_state.last_action = f"{status} Ticket #{person['id']} ({person['name']})..."
    else:
        st.session_state.last_action = "⚠️ The queue is empty!"

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# --- 4. THE ENHANCED UI LAYOUT ---

# Theme Toggle Button (Fixed position)
col_theme = st.columns([5, 1])
with col_theme[1]:
    theme_label = "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle", help="Toggle between dark and light mode"):
        toggle_theme()
        st.rerun()

# Animated Header
st.markdown("""
<div class="animated-header">
    <h1 style="margin:0; color: #ff4b4b;">🎬 Cinema Queue Simulator</h1>
    <p style="margin:0; font-size: 1.2em;">A <strong>vibrant visual demonstration</strong> of the <strong>Queue (FIFO)</strong> algorithm with VIP priority!</p>
</div>
""", unsafe_allow_html=True)

# Layout: 3 Columns
col1, col2, col3 = st.columns([1, 2, 1])

# --- COLUMN 1: ENHANCED CONTROL PANEL ---
with col1:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.subheader("🎮 Control Center")
    
    st.markdown('<div class="queue-counter">Queue: {} people</div>'.format(len(st.session_state.queue)), unsafe_allow_html=True)
    
    # Control Buttons
    col_buttons = st.columns(2)
    with col_buttons[0]:
        if st.button("➕ Join Queue", help="Add a regular customer to the end of the queue"):
            enqueue_person(is_vip=False)
            st.rerun()
    
    with col_buttons[1]:
        if st.button("⭐ VIP Join", help="VIP customers get priority placement!", 
                    key="vip_join"):
            enqueue_person(is_vip=True)
            st.rerun()
    
    if st.button("🎫 Serve Next Customer", type="primary", 
                help="Serve the customer at the front of the queue"):
        dequeue_person()
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🔄 Reset Simulator", help="Clear all queues and history"):
        st.session_state.queue = []
        st.session_state.history = []
        st.session_state.ticket_id = 100
        st.session_state.last_action = "Simulator Reset."
        st.rerun()
    
    if st.button("📊 Quick Stats", help="Generate random queue for demo"):
        for _ in range(random.randint(3, 7)):
            enqueue_person(is_vip=random.choice([True, False]))
        st.rerun()
    
    # Status Panel
    st.markdown("---")
    st.markdown("### 📈 Status Panel")
    st.markdown(f'<span class="status-indicator status-active"></span> **Last Action:**', unsafe_allow_html=True)
    st.info(st.session_state.last_action)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- COLUMN 2: VISUAL QUEUE DISPLAY ---
with col2:
    # Current Serving Display
    if len(st.session_state.queue) > 0:
        next_person = st.session_state.queue[0]
        vip_status = "⭐ **VIP** " if next_person.get('is_vip', False) else ""
        st.markdown(f"""
        <div class="current-serving">
            <h3>🎬 NOW SERVING</h3>
            <div style="font-size: 40px;">{next_person['avatar']}</div>
            <h2>{vip_status}Ticket #{next_person['id']}</h2>
            <p style="font-size: 1.3em;"><strong>{next_person['name']}</strong></p>
            <p>Joined at: {next_person['time']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader(f"👥 Current Queue ({len(st.session_state.queue)})")
    
    if len(st.session_state.queue) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: rgba(255,255,255,0.05); border-radius: 15px;">
            <div style="font-size: 50px;">🎭</div>
            <h3>The lobby is empty</h3>
            <p>No one is waiting. Add some customers to begin!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display the queue flow
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="color: #4CAF50; font-weight: bold;">⬇️ FRONT OF LINE ⬇️</div>
            <div style="font-size: 12px; color: #888;">(Next to be served)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display first 6 people
        people_to_show = st.session_state.queue[:6]
        cols = st.columns(len(people_to_show) if len(people_to_show) > 0 else 1)
        
        for idx, person in enumerate(people_to_show):
            with cols[idx]:
                vip_class = "vip" if person.get('is_vip', False) else ""
                vip_badge = '<div class="vip-badge">VIP</div>' if person.get('is_vip', False) else ""
                
                st.markdown(f"""
                <div class="ticket-card {vip_class}">
                    {vip_badge}
                    <div style="font-size: 40px;">{person['avatar']}</div>
                    <div class="ticket-number">#{person['id']}</div>
                    <div class="ticket-name">{person['name']}</div>
                    <div style="font-size: 12px; margin-top: 5px;">{person['time']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        if len(st.session_state.queue) > 6:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px; margin: 20px 0;">
                <div style="font-size: 30px;">👥</div>
                <p>...and <strong>{len(st.session_state.queue) - 6}</strong> more waiting behind</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="color: #ff4b4b; font-weight: bold;">⬆️ BACK OF LINE ⬆️</div>
            <div style="font-size: 12px; color: #888;">(New people join here)</div>
        </div>
        """, unsafe_allow_html=True)

# --- COLUMN 3: HISTORY & STATS ---
with col3:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.subheader("📜 Service History")
    
    if len(st.session_state.history) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 40px;">📭</div>
            <p><em>No tickets processed yet</em></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_served = len(st.session_state.history)
        vip_served = sum(1 for p in st.session_state.history if p.get('is_vip', False))
        
        # Stats
        st.metric("Total Served", total_served)
        if vip_served > 0:
            st.metric("VIP Served", vip_served)
        
        st.markdown("---")
        
        # Recent history
        st.markdown("**Recent Activity:**")
        for person in st.session_state.history[:5]:
            vip_icon = "⭐ " if person.get('is_vip', False) else ""
            st.markdown(f"""
            <div class="history-card">
                <strong>{vip_icon}#{person['id']} {person['name']}</strong> {person['avatar']}
                <div style="font-size: 12px; color: #666;">Served at {person['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER WITH ALGORITHM EXPLANATION ---
st.divider()

# Algorithm explanation in tabs
tab1, tab2, tab3 = st.tabs(["🧠 How it Works", "⭐ VIP Priority", "🎯 Key Features"])

with tab1:
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.markdown("""
        ### Queue (FIFO) Algorithm
        
        1. **Enqueue** 
           ```python
           queue.append(item)
           ```
           Person enters at the **back**
        
        2. **Dequeue**
           ```python
           queue.pop(0)
           ```
           Person at the **front** leaves
        """)
    
    with col_exp2:
        st.markdown("""
        ### Real-world Examples
        
        • 🎬 Movie ticket lines
        • 🖨️ Printer job queues  
        • 📞 Customer service calls
        • 🚗 Drive-thru orders
        • 🎮 Game matchmaking
        """)

with tab2:
    col_vip1, col_vip2 = st.columns(2)
    with col_vip1:
        st.markdown("""
        ### VIP Priority System
        
        ⭐ **VIP customers** jump ahead of regular customers!
        
        **Implementation:**
        ```python
        if is_vip:
            # Insert after last VIP in queue
            queue.insert(vip_position, person)
        else:
            # Regular customers go to back
            queue.append(person)
        ```
        """)
    
    with col_vip2:
        st.markdown("""
        ### Priority Rules
        
        1. All VIPs go before regular customers
        2. Among VIPs: First-come, first-served
        3. Regular queue maintains FIFO order
        4. VIPs don't displace other VIPs
        """)

with tab3:
    feat_cols = st.columns(3)
    with feat_cols[0]:
        st.markdown("""
        ### 🎨 Visual Design
        • Gradient backgrounds
        • Animated elements
        • Smooth transitions
        • Dark/Light themes
        """)
    
    with feat_cols[1]:
        st.markdown("""
        ### ⚡ Interactive
        • Real-time updates
        • VIP priority system
        • Queue visualization
        • Service history
        """)
    
    with feat_cols[2]:
        st.markdown("""
        ### 📱 Responsive
        • Works on all devices
        • Clean mobile layout
        • Intuitive controls
        • Live status updates
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em;">
    <p>🎬 <strong>Cinema Queue Simulator</strong> | Built with Streamlit | Demonstrating FIFO Queue Algorithm</p>
    <p>Click buttons to interact with the queue!</p>
</div>
""", unsafe_allow_html=True)
