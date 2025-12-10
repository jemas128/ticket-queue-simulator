import streamlit as st
import time
import random
from datetime import datetime

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Cinema Queue Simulator", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Custom CSS with beautiful gradients and animations
st.markdown(f"""
<style>
    /* Modern Color Palette */
    :root {{
        --primary: #FF6B6B;
        --secondary: #4ECDC4;
        --accent: #FFD166;
        --vip: #FFB347;
        --success: #06D6A0;
        --dark-bg: #1A1A2E;
        --dark-card: #16213E;
        --light-bg: #F8F9FF;
        --light-card: #FFFFFF;
        --text-dark: #FFFFFF;
        --text-light: #2D3047;
    }}
    
    /* Main Styling */
    .stApp {{
        background: linear-gradient(135deg, 
            {'#1A1A2E 0%, #16213E 50%, #0F3460 100%' if st.session_state.theme == 'dark' else 
             '#F8F9FF 0%, #E6E9FF 50%, #D6DAFF 100%'});
        background-attachment: fixed;
        min-height: 100vh;
        color: {'var(--text-dark)' if st.session_state.theme == 'dark' else 'var(--text-light)'};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Animated Header */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .main-header {{
        background: linear-gradient(90deg, 
            rgba(255, 107, 107, 0.2) 0%, 
            rgba(78, 205, 196, 0.2) 50%, 
            rgba(255, 209, 102, 0.2) 100%);
        padding: 30px;
        border-radius: 25px;
        margin: 20px 0 40px 0;
        border: 2px solid rgba(255, 107, 107, 0.3);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 107, 107, 0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite linear;
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-50%) translateY(-50%) rotate(0deg); }}
        100% {{ transform: translateX(-50%) translateY(-50%) rotate(360deg); }}
    }}
    
    .cinema-title {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #FFD166);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: float 3s ease-in-out infinite;
    }}
    
    /* Control Panel */
    .control-panel {{
        background: {'rgba(22, 33, 62, 0.9)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.9)'};
        padding: 25px;
        border-radius: 20px;
        border: 2px solid var(--primary);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(15px);
        margin-bottom: 20px;
    }}
    
    /* Queue Display Area */
    .queue-display {{
        background: {'rgba(22, 33, 62, 0.8)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.8)'};
        padding: 30px;
        border-radius: 20px;
        border: 2px solid rgba(78, 205, 196, 0.3);
        backdrop-filter: blur(10px);
        min-height: 400px;
    }}
    
    /* Ticket Cards */
    .ticket-card {{
        background: linear-gradient(135deg, 
            {'rgba(255, 107, 107, 0.15)' if st.session_state.theme == 'dark' else 'rgba(255, 107, 107, 0.1)'}, 
            {'rgba(78, 205, 196, 0.15)' if st.session_state.theme == 'dark' else 'rgba(78, 205, 196, 0.1)'});
        border: 3px solid var(--primary);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }}
    
    .ticket-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
    }}
    
    .ticket-card:hover {{
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 20px 40px rgba(255, 107, 107, 0.3);
    }}
    
    .ticket-card.vip {{
        background: linear-gradient(135deg, rgba(255, 179, 71, 0.3), rgba(255, 209, 102, 0.4));
        border: 3px solid var(--vip);
    }}
    
    .vip-badge {{
        position: absolute;
        top: 10px;
        right: 10px;
        background: linear-gradient(45deg, #FFB347, #FFD166);
        color: #000;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(255, 179, 71, 0.3);
    }}
    
    .ticket-avatar {{
        font-size: 50px;
        margin: 10px 0;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
    }}
    
    .ticket-number {{
        font-size: 22px;
        font-weight: bold;
        color: var(--primary);
        margin: 10px 0;
    }}
    
    .ticket-name {{
        font-size: 16px;
        font-weight: 600;
        color: {'#FFFFFF' if st.session_state.theme == 'dark' else '#2D3047'};
    }}
    
    /* Enhanced Buttons */
    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-weight: bold;
        font-size: 16px;
        margin: 8px 0;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }}
    
    .stButton>button::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
        transform: translateX(-100%);
    }}
    
    .stButton>button:hover::after {{
        transform: translateX(100%);
        transition: transform 0.6s ease;
    }}
    
    /* Theme Toggle */
    .theme-toggle {{
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 1000;
    }}
    
    /* Status Indicators */
    .status-badge {{
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
        animation: pulse 2s infinite;
    }}
    
    .status-serving {{
        background: linear-gradient(45deg, var(--success), #06D6A0);
        color: white;
    }}
    
    .status-waiting {{
        background: linear-gradient(45deg, #FF6B6B, #FF8E8E);
        color: white;
    }}
    
    /* Now Serving Display */
    .now-serving {{
        background: linear-gradient(135deg, rgba(6, 214, 160, 0.2), rgba(78, 205, 196, 0.3));
        border: 3px solid var(--success);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }}
    
    .now-serving::after {{
        content: 'NOW SERVING';
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 12px;
        font-weight: bold;
        color: var(--success);
        opacity: 0.5;
    }}
    
    /* Queue Flow Indicators */
    .queue-flow {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 20px 0;
        padding: 10px 20px;
        background: {'rgba(255,255,255,0.05)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.05)'};
        border-radius: 15px;
        font-weight: bold;
    }}
    
    .front-of-line {{
        color: var(--success);
    }}
    
    .back-of-line {{
        color: var(--primary);
    }}
    
    /* Statistics Cards */
    .stat-card {{
        background: {'rgba(22, 33, 62, 0.7)' if st.session_state.theme == 'dark' else 'rgba(255, 255, 255, 0.7)'};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        border-left: 5px solid var(--secondary);
    }}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {'rgba(255,255,255,0.05)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.05)'};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(var(--primary), var(--secondary));
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(var(--secondary), var(--primary));
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'queue' not in st.session_state:
    st.session_state.queue = []

if 'history' not in st.session_state:
    st.session_state.history = []

if 'ticket_id' not in st.session_state:
    st.session_state.ticket_id = 100

if 'last_action' not in st.session_state:
    st.session_state.last_action = "🎬 Welcome to Cinema Queue Simulator! Add your first customer."

if 'auto_mode' not in st.session_state:
    st.session_state.auto_mode = False

# --- 3. HELPER FUNCTIONS ---
def generate_random_person(is_vip=False):
    """Generate a random person with unique attributes"""
    if is_vip:
        names = ["James Bond", "Cleopatra", "Tony Stark", "Wonder Woman", "Black Panther", 
                "Doctor Strange", "Princess Leia", "The Godfather"]
        emojis = ["👑", "🎩", "💎", "🌟", "⭐", "✨", "🕶️", "🧳"]
    else:
        names = ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Morgan", "Charlie", "Dakota",
                "Skyler", "Quinn", "Parker", "Drew", "Blake", "Avery", "Reese"]
        emojis = ["👱", "👵", "👮", "🧑‍💻", "🧟", "🧛", "🧙", "🦸", "👨‍🚀", "👩‍🎤", "🕵️", "👩‍🍳", "🧑‍🎨", "👨‍🔬", "👷"]
    
    return {
        "name": random.choice(names),
        "avatar": random.choice(emojis),
        "id": st.session_state.ticket_id,
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_vip": is_vip,
        "ticket_color": random.choice(["#FF6B6B", "#4ECDC4", "#FFD166", "#118AB2", "#EF476F"])
    }

def enqueue_person(is_vip=False):
    """Add a person to the queue"""
    person = generate_random_person(is_vip)
    
    if is_vip:
        # Insert VIP after the last VIP in queue (maintaining VIP order)
        vip_positions = [i for i, p in enumerate(st.session_state.queue) if p.get('is_vip', False)]
        if vip_positions:
            insert_position = vip_positions[-1] + 1
        else:
            insert_position = 0
        st.session_state.queue.insert(insert_position, person)
        st.session_state.last_action = f"⭐ **VIP Alert!** {person['avatar']} {person['name']} (Ticket #{person['id']}) entered with priority!"
    else:
        st.session_state.queue.append(person)
        st.session_state.last_action = f"✅ {person['avatar']} {person['name']} (Ticket #{person['id']}) joined the queue."
    
    st.session_state.ticket_id += 1

def dequeue_person():
    """Serve the next person in queue"""
    if st.session_state.queue:
        person = st.session_state.queue.pop(0)
        person['served_time'] = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.insert(0, person)
        
        if person.get('is_vip', False):
            st.session_state.last_action = f"🎉 **VIP SERVED!** {person['avatar']} {person['name']} (Ticket #{person['id']}) has been served."
        else:
            st.session_state.last_action = f"🎟️ {person['avatar']} {person['name']} (Ticket #{person['id']}) has been served."
    else:
        st.session_state.last_action = "⚠️ Queue is empty! Add some customers first."

def toggle_theme():
    """Switch between dark and light mode"""
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    st.rerun()

def clear_queue():
    """Reset the simulator"""
    st.session_state.queue = []
    st.session_state.history = []
    st.session_state.ticket_id = 100
    st.session_state.last_action = "🔄 Simulator has been reset."
    st.rerun()

def populate_queue():
    """Add multiple random customers for demo"""
    for _ in range(random.randint(4, 8)):
        enqueue_person(is_vip=random.choice([True, False]))
    st.session_state.last_action = f"📊 Added {len(st.session_state.queue)} random customers to queue."
    st.rerun()

# --- 4. THEME TOGGLE BUTTON ---
with st.sidebar:
    theme_label = "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle", help="Toggle theme"):
        toggle_theme()

# --- 5. MAIN HEADER ---
st.markdown("""
<div class="main-header">
    <h1 class="cinema-title">🎬 CINEMA QUEUE SIMULATOR</h1>
    <div style="text-align: center; font-size: 1.2rem; opacity: 0.9;">
        A <strong>visual & interactive</strong> demonstration of the <strong>Queue (FIFO)</strong> algorithm
    </div>
</div>
""", unsafe_allow_html=True)

# --- 6. MAIN LAYOUT ---
col1, col2, col3 = st.columns([1, 2, 1])

# --- COLUMN 1: CONTROL PANEL ---
with col1:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
    st.markdown("### 🎮 CONTROL CENTER")
    
    # Queue Counter
    st.markdown(f"""
    <div class="status-badge status-waiting">
        👥 Queue: {len(st.session_state.queue)} people
    </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons
    if st.button("🎫 **ADD CUSTOMER**", type="primary", use_container_width=True):
        enqueue_person(is_vip=False)
        st.rerun()
    
    if st.button("⭐ **ADD VIP**", help="VIPs get priority placement!", use_container_width=True):
        enqueue_person(is_vip=True)
        st.rerun()
    
    if st.button("🚀 **SERVE NEXT**", type="secondary", use_container_width=True):
        dequeue_person()
        st.rerun()
    
    st.markdown("---")
    
    # Utility Buttons
    col_util1, col_util2 = st.columns(2)
    with col_util1:
        if st.button("🔄 Reset", help="Clear all data"):
            clear_queue()
    with col_util2:
        if st.button("🎲 Demo", help="Generate random queue"):
            populate_queue()
    
    # Status Display
    st.markdown("---")
    st.markdown("### 📊 STATUS")
    st.info(st.session_state.last_action)
    
    # Quick Stats
    if st.session_state.history:
        st.metric("Total Served", len(st.session_state.history))
        vip_count = sum(1 for p in st.session_state.history if p.get('is_vip', False))
        if vip_count > 0:
            st.metric("VIPs Served", vip_count)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- COLUMN 2: QUEUE VISUALIZATION ---
with col2:
    st.markdown('<div class="queue-display">', unsafe_allow_html=True)
    
    # Now Serving Section
    if st.session_state.queue:
        next_person = st.session_state.queue[0]
        st.markdown(f"""
        <div class="now-serving">
            <div style="font-size: 50px; margin-bottom: 15px;">{next_person['avatar']}</div>
            <h2 style="margin: 10px 0; color: #06D6A0;">
                {'⭐ ' if next_person.get('is_vip', False) else ''}
                TICKET #{next_person['id']}
            </h2>
            <h3 style="margin: 10px 0;">{next_person['name']}</h3>
            <p style="opacity: 0.8; margin: 5px 0;">Joined: {next_person['time']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Queue Visualization
    st.subheader(f"📋 CURRENT QUEUE ({len(st.session_state.queue)} waiting)")
    
    if not st.session_state.queue:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <div style="font-size: 80px; opacity: 0.3;">🎭</div>
            <h3 style="opacity: 0.7;">Queue is Empty</h3>
            <p>Add customers to start the simulation!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Queue Flow Indicator
        st.markdown("""
        <div class="queue-flow">
            <span class="front-of-line">⬇️ FRONT (Next to Serve)</span>
            <span class="back-of-line">⬆️ BACK (New Entries)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Display queue in rows of 3
        people_to_show = st.session_state.queue[:9]  # Show first 9
        for i in range(0, len(people_to_show), 3):
            cols = st.columns(3)
            row_people = people_to_show[i:i+3]
            for idx, person in enumerate(row_people):
                with cols[idx]:
                    vip_class = "vip" if person.get('is_vip', False) else ""
                    vip_badge = '<div class="vip-badge">VIP</div>' if person.get('is_vip', False) else ""
                    
                    st.markdown(f"""
                    <div class="ticket-card {vip_class}">
                        {vip_badge}
                        <div class="ticket-avatar">{person['avatar']}</div>
                        <div class="ticket-number">#{person['id']}</div>
                        <div class="ticket-name">{person['name']}</div>
                        <div style="font-size: 12px; opacity: 0.7; margin-top: 5px;">
                            {person['time']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Show remaining count
        if len(st.session_state.queue) > 9:
            remaining = len(st.session_state.queue) - 9
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: rgba(255,107,107,0.1); border-radius: 10px; margin-top: 20px;">
                <div style="font-size: 24px;">👥</div>
                <p style="margin: 5px 0;"><strong>+{remaining} more</strong> in queue</p>
                <p style="font-size: 12px; opacity: 0.7;">Total waiting: {len(st.session_state.queue)} people</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- COLUMN 3: HISTORY & STATS ---
with col3:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
    st.markdown("### 📜 SERVICE HISTORY")
    
    if not st.session_state.history:
        st.markdown("""
        <div style="text-align: center; padding: 30px;">
            <div style="font-size: 50px; opacity: 0.3;">📭</div>
            <p style="opacity: 0.7;">No tickets served yet</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Quick Stats
        total_served = len(st.session_state.history)
        vip_served = sum(1 for p in st.session_state.history if p.get('is_vip', False))
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 28px; font-weight: bold;">{total_served}</div>
                <div style="font-size: 12px;">Total Served</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            if vip_served > 0:
                st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size: 28px; font-weight: bold; color: #FFB347;">{vip_served}</div>
                    <div style="font-size: 12px;">VIPs Served</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Recent Activity:**")
        
        # Display recent history
        for person in st.session_state.history[:5]:
            vip_icon = "⭐ " if person.get('is_vip', False) else ""
            served_time = person.get('served_time', person['time'])
            
            st.markdown(f"""
            <div style="background: {'rgba(255,255,255,0.05)' if st.session_state.theme == 'dark' else 'rgba(0,0,0,0.05)'}; 
                        padding: 12px; border-radius: 10px; margin: 8px 0; border-left: 3px solid #4ECDC4;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 24px; margin-right: 10px;">{person['avatar']}</div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: bold;">{vip_icon}#{person['id']} {person['name']}</div>
                        <div style="font-size: 11px; opacity: 0.7;">Served at {served_time}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. FOOTER & ALGORITHM EXPLANATION ---
st.markdown("---")

# Tabs for different explanations
tab1, tab2, tab3 = st.tabs(["🎯 How It Works", "⭐ VIP System", "💡 Queue Applications"])

with tab1:
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.markdown("""
        ### 🔄 Queue Algorithm (FIFO)
        
        **Enqueue Operation:**
        ```python
        def enqueue(person):
            queue.append(person)  # Add to end
        ```
        
        **Dequeue Operation:**
        ```python
        def dequeue():
            if queue:
                return queue.pop(0)  # Remove from front
        ```
        """)
        
        st.markdown("""
        ### 📊 Key Principles:
        1. **First In, First Out (FIFO)**
        2. **Linear Data Structure**
        3. **Two Main Operations:**
           - Enqueue (add to rear)
           - Dequeue (remove from front)
        4. **Constant Time Operations**
        """)
    
    with col_exp2:
        st.markdown("""
        ### 🎨 Visual Elements:
        
        **Ticket Colors:**
        - 🔴 Red: Regular Customers
        - 🟡 Gold: VIP Customers
        - 🟢 Green: Currently Serving
        - 🔵 Blue: Served Customers
        
        **Icons Meaning:**
        - 👑 VIP Priority Access
        - ⭐ Special Treatment
        - 🎟️ Regular Ticket
        - 🚀 Fast Service
        """)

with tab2:
    col_vip1, col_vip2 = st.columns(2)
    with col_vip1:
        st.markdown("""
        ### 🌟 VIP Priority Rules
        
        **Priority Placement:**
        1. All VIPs go before regular customers
        2. Among VIPs: Maintain FIFO order
        3. Regular queue maintains standard FIFO
        
        **Implementation Logic:**
        ```python
        if person.is_vip:
            # Find position after last VIP
            insert_at = last_vip_index + 1
            queue.insert(insert_at, person)
        else:
            # Regular customers go to back
            queue.append(person)
        ```
        """)
    
    with col_vip2:
        st.markdown("""
        ### 🎭 VIP Features:
        
        **Visual Indicators:**
        - Gold gradient background
        - VIP badge on ticket
        - Star icon in display
        - Special notification
        
        **Service Benefits:**
        - Priority queue placement
        - Special announcements
        - Gold-colored tickets
        - Priority service calls
        """)

with tab3:
    col_app1, col_app2, col_app3 = st.columns(3)
    
    with col_app1:
        st.markdown("""
        ### 🎬 Entertainment
        - Movie theater queues
        - Concert ticket lines
        - Amusement park rides
        - Stadium entries
        """)
    
    with col_app2:
        st.markdown("""
        ### 💼 Business
        - Bank teller queues
        - Restaurant waiting
        - Customer service
        - Checkout lines
        """)
    
    with col_app3:
        st.markdown("""
        ### 🖥️ Technology
        - Printer job queues
        - Network packet routing
        - CPU scheduling
        - Message queues
        """)

# Final Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; opacity: 0.8;">
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 10px;">
        <span>🎬 Cinema Queue Simulator</span>
        <span>•</span>
        <span>🔗 Built with Streamlit</span>
        <span>•</span>
        <span>🧠 Demonstrating FIFO Algorithm</span>
    </div>
    <p style="font-size: 0.9rem; margin-top: 10px;">
        Click buttons to interact • Watch the queue flow • Experience VIP priority!
    </p>
</div>
""", unsafe_allow_html=True)

# Add some interactive fun
if st.session_state.queue:
    progress = min(100, (len(st.session_state.history) / max(1, len(st.session_state.history) + len(st.session_state.queue))) * 100)
    st.progress(int(progress))
    st.caption(f"Queue Progress: {len(st.session_state.history)} served • {len(st.session_state.queue)} waiting")
