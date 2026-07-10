import random
import copy
from dataclasses import dataclass, field

# =====================================================
# CONGKLAK ENGINE
# =====================================================
#
# View from Player A
#
#          B7 B6 B5 B4 B3 B2 B1
#
# STORE A                  STORE B
#
#          A1 A2 A3 A4 A5 A6 A7
#
# =====================================================

PATH_A = [
    "A7","A6","A5","A4","A3","A2","A1",
    "STORE_A",
    "B7","B6","B5","B4","B3","B2","B1"
]

PATH_B = [
    "B7","B6","B5","B4","B3","B2","B1",
    "STORE_B",
    "A7","A6","A5","A4","A3","A2","A1"
]

OPPOSITE = {

    "A1": "B7",
    "A2": "B6",
    "A3": "B5",
    "A4": "B4",
    "A5": "B3",
    "A6": "B2",
    "A7": "B1",

    "B1": "A7",
    "B2": "A6",
    "B3": "A5",
    "B4": "A4",
    "B5": "A3",
    "B6": "A2",
    "B7": "A1",
}


@dataclass
class GameState:

    board:dict = field(default_factory=lambda:{

        "A1":7,
        "A2":7,
        "A3":7,
        "A4":7,
        "A5":7,
        "A6":7,
        "A7":7,

        "STORE_A":0,

        "B7":7,
        "B6":7,
        "B5":7,
        "B4":7,
        "B3":7,
        "B2":7,
        "B1":7,

        "STORE_B":0
    })

    current_player:str="A"

    game_over:bool=False

    winner:str=""

    last_hole:str=""

    history:list=field(default_factory=list)

    turn_states: list = field(default_factory=list)

    mode: str = "Human vs Human"


def new_game():

    game = GameState()

    save_initial_state(game)

    return game

# =====================================================
# BASIC HELPERS
# =====================================================

def log(game,text):

    game.history.append(text)


def get_seed(game,hole):

    return game.board[hole]


def set_seed(game,hole,value):

    game.board[hole]=value


def add_seed(game,hole,n=1):

    game.board[hole]+=n


def take_all(game,hole):

    total=game.board[hole]

    game.board[hole]=0

    return total


def is_store(hole):

    return hole.startswith("STORE")


def own_store(player):

    return f"STORE_{player}"


def is_player_hole(player,hole):

    return hole.startswith(player)


def opposite(hole):

    return OPPOSITE[hole]

# =====================================================
# NEXT HOLE
# =====================================================

def next_hole(player,hole):

    path=PATH_A if player=="A" else PATH_B

    i=path.index(hole)

    i+=1

    if i>=len(path):

        i=0

    return path[i]

# =====================================================
# TURN
# =====================================================

def switch_player(game):

    if game.current_player=="A":

        game.current_player="B"

    else:

        game.current_player="A"

# =====================================================
# SIDE HELPERS
# =====================================================

def side_holes(player):

    if player=="A":

        return [
            "A1","A2","A3","A4","A5","A6","A7"
        ]

    return [
        "B1","B2","B3","B4","B5","B6","B7"
    ]


def side_empty(game,player):

    return all(

        get_seed(game,h)==0

        for h in side_holes(player)

    )

def save_state(game, player, selected):

    game.turn_states.append({

        "turn": len(game.turn_states),

        "player": player,

        "selected": selected,

        "store_a": game.board["STORE_A"],

        "store_b": game.board["STORE_B"],

        "difference": state_difference(game),

        "state": state_name(game),

        "board": copy.deepcopy(game.board)
    })

def save_initial_state(game):

    game.turn_states.append({

        "turn":0,

        "player":"-",

        "selected":"START",

        "store_a":0,

        "store_b":0,

        "difference":0,

        "state":"S3",

        "board":copy.deepcopy(game.board)

    })

def collect_remaining(game: GameState):

    # Ambil semua sisa biji Player A
    for hole in ["A1","A2","A3","A4","A5","A6","A7"]:

        seeds = take_all(game, hole)

        add_seed(game, "STORE_A", seeds)

    # Ambil semua sisa biji Player B
    for hole in ["B1","B2","B3","B4","B5","B6","B7"]:

        seeds = take_all(game, hole)

        add_seed(game, "STORE_B", seeds)

def winner(game: GameState):

    if game.board["STORE_A"] > game.board["STORE_B"]:
        return "A"

    if game.board["STORE_B"] > game.board["STORE_A"]:
        return "B"

    return "DRAW"


# =====================================================
# MOVE
# =====================================================

def make_move(game, selected):

    if game.game_over:
        return False

    player = game.current_player

    # ==========================
    # VALIDASI
    # ==========================

    if not is_player_hole(player, selected):
        log(game, f"Invalid move ({selected})")
        return False

    if get_seed(game, selected) == 0:
        log(game, f"{selected} is empty")
        return False

    log(game, "")
    log(game, f"===== PLAYER {player} =====")
    log(game, f"Choose {selected}")

    hole = selected
    seeds = take_all(game, hole)

    log(game, f"Take {seeds} seed(s)")

    # ==========================
    # RELAY LOOP
    # ==========================

    while True:

        # ---------- SOWING ----------

        while seeds > 0:

            hole = next_hole(player, hole)

            add_seed(game, hole)

            seeds -= 1

            log(game, f"Drop -> {hole}")

        game.last_hole = hole

        # ---------- EXTRA TURN ----------

        if hole == own_store(player):

            log(game, "Extra Turn")

            if side_empty(game, "A") or side_empty(game, "B"):

                collect_remaining(game)

                game.game_over = True

                game.winner = winner(game)

                log(game, "")
                log(game, "===== GAME OVER =====")
                log(game, f"Winner : {game.winner}")

            save_state(game, player, selected)

            return True

        # ---------- RELAY ----------

        if not is_store(hole):

            total = get_seed(game, hole)

            if total > 1:

                log(game, f"Relay from {hole} ({total})")

                seeds = take_all(game, hole)

                continue

        # ---------- CAPTURE ----------

        if is_player_hole(player, hole):

            if get_seed(game, hole) == 1:

                opp = opposite(hole)

                if get_seed(game, opp) > 0:

                    captured = take_all(game, opp)

                    take_all(game, hole)

                    add_seed(
                        game,
                        own_store(player),
                        captured + 1
                    )

                    log(game, f"Capture {captured} seed(s) from {opp}")

        break

    # ==========================
    # SAVE MOVE
    # ==========================

    save_state(game, player, selected)

    # ==========================
    # GAME OVER
    # ==========================

    if side_empty(game, "A") or side_empty(game, "B"):

        collect_remaining(game)

        game.game_over = True

        game.winner = winner(game)

        # ==========================
        # SAVE FINAL STATE
        # ==========================

        if game.winner == "A":
            final_state = "W"

        elif game.winner == "B":
            final_state = "L"

        else:
            final_state = "D"

        game.turn_states.append({

        "turn": len(game.turn_states),

        "player": "-",

        "selected": "END",

        "store_a": game.board["STORE_A"],

        "store_b": game.board["STORE_B"],

        "difference": game.board["STORE_A"] - game.board["STORE_B"],

        "state": final_state,

        "board": copy.deepcopy(game.board)

})
        log(game, "")
        log(game, "===== GAME OVER =====")
        log(game, f"Winner : {game.winner}")

    # ==========================
    # SWITCH PLAYER
    # ==========================

    if not game.game_over:

        switch_player(game)

        log(game, f"Turn -> {game.current_player}")

    return True

def computer_move(game):

    holes = side_holes(game.current_player)

    legal = []

    for h in holes:

        if get_seed(game, h) > 0:

            legal.append(h)

    if len(legal) == 0:

        return

    move = random.choice(legal)

    make_move(game, move)

    

# =====================================================
# STATE
# =====================================================

def state_difference(game):

    return game.board["STORE_A"] - game.board["STORE_B"]

def state_name(game):

    d = state_difference(game)

    if d <= -10:
        return "S1"

    elif -9 <= d <= -1:
        return "S2"

    elif d == 0:
        return "S3"

    elif 1 <= d <= 9:
        return "S4"

    else:
        return "S5"
    
def state_description(game):

        d = state_difference(game)

        if d <= -10:
            return "Tertinggal jauh"

        elif -9 <= d <= -1:
            return "Tertinggal sedikit"

        elif d == 0:
            return "Imbang"

        elif 1 <= d <= 9:
            return "Unggul sedikit"

        else:
            return "Unggul jauh"
    


