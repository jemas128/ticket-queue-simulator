import streamlit as st
import time
import random
from datetime import datetime

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Cinema Queue Simulator", page_icon="🍿", layout="wide")

# Custom CSS to make the "Tickets" look good
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
    }
    .ticket-card {
        background-color: #262730;
        border: 2px solid #ff4b4b;
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        color: white;
    }
    .ticket-number {
        font-size: 24px;
        font-weight: bold;
        color: #ff4b4b;
    }
    .ticket-name {
        font-size: 16px;
    }
    .current-serving {
        background-color: #d1ffbd;
        color: #1a4a1a;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 2px dashed #4CAF50;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (The Memory) ---
# Streamlit refreshes the script on every click. 
# We use 'session_state' to keep the Queue alive between clicks.

if 'queue' not in st.session_state:
    st.session_state.queue = []  # This is our Queue Data Structure

if 'history' not in st.session_state:
    st.session_state.history = [] # To track served customers

if 'ticket_id' not in st.session_state:
    st.session_state.ticket_id = 100 # Starting ticket number

if 'last_action' not in st.session_state:
    st.session_state.last_action = "Welcome! Queue is empty."

# --- 3. HELPER FUNCTIONS ---

def generate_random_person():
    names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
    emojis = ["👱", "👵", "👮", "🧑‍💻", "🧟", "🧛", "🧙", "🦸"]
    return {
        "name": random.choice(names),
        "avatar": random.choice(emojis),
        "id": st.session_state.ticket_id,
        "time": datetime.now().strftime("%H:%M:%S")
    }

def enqueue_person():
    person = generate_random_person()
    st.session_state.queue.append(person) # Add to end of list
    st.session_state.ticket_id += 1
    st.session_state.last_action = f"✅ Ticket #{person['id']} ({person['name']}) joined the line."

def dequeue_person():
    if len(st.session_state.queue) > 0:
        person = st.session_state.queue.pop(0) # Remove from start of list (FIFO)
        st.session_state.history.insert(0, person) # Add to history
        st.session_state.last_action = f"🎟️ Serving Ticket #{person['id']} ({person['name']})..."
    else:
        st.session_state.last_action = "⚠️ The queue is empty!"

# --- 4. THE UI LAYOUT ---

# Header
st.title("🍿 Cinema Ticket Queue Simulator")
st.markdown("A visual demonstration of the **Queue (FIFO)** algorithm.")
st.divider()

# Layout: 3 Columns (Controls, The Queue, Stats)
col1, col2, col3 = st.columns([1, 2, 1])

# --- COLUMN 1: CONTROLS ---
with col1:
    st.subheader("🎮 Controls")
    
    if st.button("➕ Join Queue (Enqueue)"):
        enqueue_person()
        
    st.write("") # Spacer
    
    if st.button("🎫 Serve Next (Dequeue)", type="primary"):
        dequeue_person()
        
    st.write("") # Spacer

    if st.button("🔄 Reset Simulator"):
        st.session_state.queue = []
        st.session_state.history = []
        st.session_state.ticket_id = 100
        st.session_state.last_action = "Simulator Reset."

    st.info(st.session_state.last_action)

# --- COLUMN 2: THE VISUAL QUEUE ---
with col2:
    st.subheader(f"👥 Current Queue ({len(st.session_state.queue)})")
    
    if len(st.session_state.queue) == 0:
        st.write("The lobby is empty. No one is waiting.")
    else:
        # We display the queue horizontally
        # We start iterating from index 0 (Front of queue)
        
        st.write("**FRONT OF LINE** (Next to be served)")
        
        # Display the first 5 people strictly for visual neatness
        people_to_show = st.session_state.queue[:5]
        
        cols = st.columns(len(people_to_show))
        for idx, person in enumerate(people_to_show):
            with cols[idx]:
                # This HTML block creates the "Ticket Card" look
                st.markdown(f"""
                <div class="ticket-card">
                    <div style="font-size:30px;">{person['avatar']}</div>
                    <div class="ticket-number">#{person['id']}</div>
                    <div class="ticket-name">{person['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
        if len(st.session_state.queue) > 5:
            st.caption(f"...and {len(st.session_state.queue) - 5} others waiting behind.")
            
        st.write("⬆️ **BACK OF LINE** (New people join here)")

# --- COLUMN 3: LOGS & HISTORY ---
with col3:
    st.subheader("📜 Served History")
    
    if len(st.session_state.history) > 0:
        for person in st.session_state.history[:5]: # Show last 5 served
            st.markdown(f"**#{person['id']} {person['name']}** {person['avatar']} served at {person['time']}")
    else:
        st.markdown("*No tickets processed yet.*")

# --- Footer explanation ---
st.divider()
st.markdown("""
### 🧠 How this works (The Algorithm):
1.  **Enqueue:** When you click "Join Queue", we do `list.append(item)`. The person enters at the **back**.
2.  **Dequeue:** When you click "Serve Next", we do `list.pop(0)`. The person at the **front** leaves.
3.  **Visuals:** Streamlit renders the list state instantly.
""")