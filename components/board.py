import streamlit as st


def draw_board(game):

    st.markdown("## 🎮 Digital Congklak Simulator")

    st.divider()

    # ==========================
    # PLAYER B
    # ==========================

    if game.current_player == "B":
        st.success("🟢 PLAYER B")
    else:
        st.markdown("### 👤 Player B")

    cols = st.columns(7)

    order_b = ["B7", "B6", "B5", "B4", "B3", "B2", "B1"]

    for i, hole in enumerate(order_b):

        if cols[i].button(
            str(game.board[hole]),
            key=hole,
            use_container_width=True
    ):

            return hole

    # ==========================
    # STORES
    # ==========================

    st.write("")

    c1, c2, c3 = st.columns([1, 7, 1])

    with c1:
        st.metric("🏺 Store A", game.board["STORE_A"])

    with c2:
        st.write("")

    with c3:
        st.metric("🏺 Store B", game.board["STORE_B"])

    # ==========================
    # PLAYER A
    # ==========================

    st.write("")

    if game.current_player == "A":
        st.success("🟢 PLAYER A")
    else:
        st.markdown("### 👤 Player A")

    cols = st.columns(7)

    order_a = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]

    for i, hole in enumerate(order_a):

        if cols[i].button(
            str(game.board[hole]),
            key=hole,
            use_container_width=True
    ):

            return hole

    st.divider()

    st.info(f"Current Turn : Player {game.current_player}")

    st.subheader("Move History")

    with st.expander("📜 Move History", expanded=False):

     for h in game.history:
        st.write(h)

    st.write(f"History : {len(game.history)} logs")
    
    return None