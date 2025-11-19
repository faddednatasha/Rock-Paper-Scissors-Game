import streamlit as st
import random
import pandas as pd
import requests
from streamlit_lottie import st_lottie

# --- CONFIGURATION ---
st.set_page_config(page_title="RPS Arena", page_icon="🎮", layout="wide")

# --- HELPER FUNCTIONS ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def determine_winner(user, computer):
    if user == computer:
        return "Tie", 0, 0
    elif (user == "Rock" and computer == "Scissors") or \
         (user == "Paper" and computer == "Rock") or \
         (user == "Scissors" and computer == "Paper"):
        return "User", 1, 0
    else:
        return "Computer", 0, 1

# --- LOAD ASSETS ---
# Animation of a robot playing
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ofa3xwo7.json")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    player_name = st.text_input("Enter Player Name", "Player 1")
    st.divider()
    st.write("Developed with Python & Streamlit")

# --- STATE MANAGEMENT ---
if 'history' not in st.session_state:
    st.session_state['history'] = [] # List to store game data

if 'scores' not in st.session_state:
    st.session_state['scores'] = {'User': 0, 'Computer': 0}

# --- MAIN UI ---
col1, col2 = st.columns([1, 2])

with col1:
    st.title("Rock, Paper, Scissors Arena")
    st.write(f"Welcome to the arena, **{player_name}**!")
    if lottie_coding:
        st_lottie(lottie_coding, height=200, key="coding")
    
    # Scoreboard
    st.metric(label=f"{player_name}'s Score", value=st.session_state['scores']['User'])
    st.metric(label="Computer's Score", value=st.session_state['scores']['Computer'])

with col2:
    st.subheader("Choose your weapon!")
    
    # Input
    options = ["Rock", "Paper", "Scissors"]
    # We use a selectbox here for a cleaner look or columns for buttons
    b1, b2, b3 = st.columns(3)
    user_move = None
    
    if b1.button("🪨 Rock", use_container_width=True): user_move = "Rock"
    if b2.button("📄 Paper", use_container_width=True): user_move = "Paper"
    if b3.button("✂️ Scissors", use_container_width=True): user_move = "Scissors"

    # Game Logic
    if user_move:
        computer_move = random.choice(options)
        winner, u_score, c_score = determine_winner(user_move, computer_move)
        
        # Update State
        st.session_state['scores']['User'] += u_score
        st.session_state['scores']['Computer'] += c_score
        
        # Log History
        st.session_state['history'].append({
            "Round": len(st.session_state['history']) + 1,
            "Player": user_move,
            "Computer": computer_move,
            "Winner": winner
        })
        
        # Display Result
        st.success(f"You chose **{user_move}**")
        st.error(f"Computer chose **{computer_move}**")
        
        if winner == "User":
            st.balloons() # Celebration effect!
            st.markdown("### 🏆 YOU WIN!")
        elif winner == "Computer":
            st.markdown("### 🤖 COMPUTER WINS!")
        else:
            st.markdown("### 🤝 IT'S A TIE!")

# --- DATA ANALYTICS SECTION ---
st.divider()
st.subheader("📊 Match History Analytics")

if st.session_state['history']:
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(st.session_state['history'])
    
    # Show the data table
    st.dataframe(df, use_container_width=True)
    
    # Simple Bar Chart of Winners
    winner_counts = df['Winner'].value_counts()
    st.bar_chart(winner_counts)
else:
    st.info("Play a round to see analytics!")
