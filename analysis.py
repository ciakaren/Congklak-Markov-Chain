import pandas as pd

# ==========================
# STATE TRANSITION
# ==========================

def transition_table(game):

    rows = []

    states = game.turn_states

    for i in range(len(states)-1):

        rows.append({

            "From": states[i]["state"],

            "To": states[i+1]["state"]

        })

    return pd.DataFrame(rows)


# ==========================
# TRANSITION MATRIX
# ==========================

def transition_matrix(game):

    state_list = [
        "S1","S2","S3","S4","S5",
        "W","D","L"
    ]

    matrix = {

        s:{t:0 for t in state_list}

        for s in state_list

    }

    states = game.turn_states

    for i in range(len(states)-1):

        s_from = states[i]["state"]

        s_to = states[i+1]["state"]

        matrix[s_from][s_to] += 1

    return pd.DataFrame(matrix).T


# ==========================
# PROBABILITY MATRIX
# ==========================

def probability_matrix(matrix):

    prob = matrix.copy().astype(float)

    for row in prob.index:

        total = prob.loc[row].sum()

        if total != 0:

            prob.loc[row] = prob.loc[row] / total

    return prob

def game_statistics(game):

    relay = 0
    capture = 0
    extra = 0

    for h in game.history:

        if "Relay" in h:
            relay += 1

        elif "Capture" in h:
            capture += 1

        elif "Extra Turn" in h:
            extra += 1

    return {

        "Steps": max(0, len(game.turn_states)-2),

        "Relay": relay,

        "Capture": capture,

        "Extra Turn": extra,

        "Winner": game.winner,

        "Store A": game.board["STORE_A"],

        "Store B": game.board["STORE_B"]

    }

from engine import *
import pandas as pd

def simulate_games(n):

    state_list = ["S1","S2","S3","S4","S5","W","D","L"]

    # dictionary dulu, bukan DataFrame
    matrix = {

        s: {t:0 for t in state_list}

        for s in state_list

    }

    winner_count = {

        "A":0,

        "B":0,

        "DRAW":0

    }

    for _ in range(n):

        game = new_game()

        while not game.game_over:

            computer_move(game)

        winner_count[game.winner] += 1

        states = game.turn_states

        for i in range(len(states)-1):

            s1 = states[i]["state"]

            s2 = states[i+1]["state"]

            if s1 in state_list and s2 in state_list:

                matrix[s1][s2] += 1

    matrix = pd.DataFrame(matrix).T

    return matrix, winner_count

import pandas as pd

def transition_matrix_simulation(states):

    state_list = ["S1","S2","S3","S4","S5","W","D","L"]

    matrix = {

        s: {t: 0 for t in state_list}

        for s in state_list

    }

    for i in range(len(states)-1):

        s1 = states[i]["state"]

        s2 = states[i+1]["state"]

        if s1 in state_list and s2 in state_list:

            matrix[s1][s2] += 1

    return pd.DataFrame(matrix).T

import numpy as np

def fundamental_matrix(Q):

    I = np.identity(len(Q))

    N = np.linalg.inv(I - Q.values)

    return pd.DataFrame(
        N,
        index=Q.index,
        columns=Q.columns
    )

# ==========================
# Q MATRIX
# ==========================

def q_matrix(prob):

    transient = ["S1","S2","S3","S4","S5"]

    absorbing = ["W","D","L"]

    return prob.loc[transient, transient]

# ==========================
# R MATRIX
# ==========================

def r_matrix(prob):

    transient = ["S1","S2","S3","S4","S5"]

    absorbing = ["W","D","L"]

    return prob.loc[transient, absorbing]

# ==========================
# ABSORPTION MATRIX
# ==========================

def absorption_matrix(N, R):

    B = N.values @ R.values

    return pd.DataFrame(

        B,

        index=N.index,

        columns=R.columns

    )
