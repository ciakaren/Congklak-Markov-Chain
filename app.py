import streamlit as st
import pandas as pd

from analysis import *
from engine import *
from components.board import draw_board

st.set_page_config(
    page_title="Digital Congklak Simulator",
    page_icon="🎮",
    layout="wide"
)

# ==========================
# CSS
# ==========================

st.markdown("""
<style>

div.stButton > button {
    height: 80px;
    font-size: 24px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SESSION
# ==========================

if "page" not in st.session_state:
    st.session_state.page = "menu"

if "game" not in st.session_state:
    st.session_state.game = new_game()

game = st.session_state.game

# ==========================
# SESSION
# ==========================

if "page" not in st.session_state:

    st.session_state.page = "menu"

if "game" not in st.session_state:

    st.session_state.game = new_game()

game = st.session_state.game

# ==========================
# MENU
# ==========================

if st.session_state.page == "menu":

    st.title("🎮 Digital Congklak Simulator")

    st.write("")

    st.subheader("Selamat Datang!")

    st.write("Pilih mode permainan")

    st.write("")

c1,c2=st.columns(2)

with c1:

    if st.button(

        "👥 Human vs Human",

        use_container_width=True,

    ):

        st.session_state.game=new_game()

        st.session_state.game.mode="Human vs Human"

        st.session_state.page="game"

        st.rerun()

with c2:

    if st.button(

        "🤖 Human vs Computer",

        use_container_width=True,

    ):

        st.session_state.game=new_game()

        st.session_state.game.mode="Human vs Computer"

        st.session_state.page="game"

        st.rerun()

# ==========================
# GAME
# ==========================

if st.session_state.page=="game":

    st.title("🎮 Digital Congklak Simulator")

if st.button("🏠 Kembali ke Menu"):

    st.session_state.page="menu"

    st.rerun()

selected=draw_board(game)

if selected is not None:

    make_move(game,selected)

    st.rerun()

if (

    game.mode=="Human vs Computer"

    and

    game.current_player=="B"

    and

    not game.game_over

):

    computer_move(game)

    st.rerun()

st.divider()

if game.game_over:

    st.success(f"🏆 Winner : Player {game.winner}")

else:

    st.info(f"🎯 Turn : Player {game.current_player}")

st.divider()

st.subheader("📊 Statistics")

st.write("Mode :",game.mode)

st.write("States :",len(game.turn_states))

st.write("Total Seeds :",sum(game.board.values()))

if st.button("🔄 New Game"):

    st.session_state.game=new_game()

    st.session_state.game.mode=game.mode

    st.rerun()

    #STATE ANALYSIS

st.divider()

st.subheader("📊 State Analysis")

la = game.board["STORE_A"]

lb = game.board["STORE_B"]

d = state_difference(game)

st.write(f"Store A : {la}")

st.write(f"Store B : {lb}")

st.latex(r"d=L_A-L_B")

st.write(f"d = {la} - {lb} = {d}")

st.success(

    f"{state_name(game)} — {state_description(game)}"

)

st.divider()

st.subheader("📖 Replay State")

if len(game.turn_states) == 0:

    st.info("Belum ada state.")

else:

    rows = []

    for s in game.turn_states:

        rows.append({

            "Turn": s["turn"],

            "Player": s["player"],

            "Move": s["selected"],

            "Store A": s["store_a"],

            "Store B": s["store_b"],

            "d": s["difference"],

            "State": s["state"]

        })

    df = pd.DataFrame(rows)

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )
    
st.divider()

st.subheader("🔄 State Transition")

transition_df = transition_table(game)

st.dataframe(

        transition_df,

        use_container_width=True,

        hide_index=True

    )

st.divider()

st.subheader("📈 Transition Matrix")

matrix = transition_matrix(game)

st.dataframe(

        matrix,

        use_container_width=True

    )

st.divider()

st.subheader("📊 Transition Probability Matrix")

prob = probability_matrix(matrix)

st.dataframe(

    prob.round(3),

    use_container_width=True

)

st.divider()

st.subheader("📊 Game Statistics")

stats = game_statistics(game)

st.metric("Winner", stats["Winner"])

c1,c2,c3 = st.columns(3)

with c1:
    st.metric("Relay", stats["Relay"])

with c2:
    st.metric("Capture", stats["Capture"])

with c3:
    st.metric("Extra Turn", stats["Extra Turn"])

c4,c5,c6 = st.columns(3)

with c4:
    st.metric("Steps", stats["Steps"])

with c5:
    st.metric("Store A", stats["Store A"])

with c6:
    st.metric("Store B", stats["Store B"])

st.divider()

st.subheader("🤖 Automatic Simulation")

games = st.selectbox(

    "Simulation",

    [10,50,100]

)

if st.button("Run Simulation"):

    matrix,winner=simulate_games(games)

    st.success(f"{games} simulations finished!")

    st.dataframe(matrix)

    st.write("### Winner Statistics")

    st.write(winner)

st.write("### Probability Matrix")

prob=probability_matrix(matrix)

st.dataframe(prob)

st.divider()

st.subheader("🟦 Q Matrix")

Q = q_matrix(prob)

st.dataframe(Q.round(3), use_container_width=True)

st.divider()

st.subheader("🟨 R Matrix")

R = r_matrix(prob)

st.dataframe(R.round(3), use_container_width=True)

st.divider()

st.subheader("🟩 Fundamental Matrix (N)")

N = fundamental_matrix(Q)

st.dataframe(N.round(3), use_container_width=True)

st.divider()

st.subheader("🏆 Absorption Probability Matrix (B)")

B = absorption_matrix(N, R)

st.dataframe(B.round(3), use_container_width=True)