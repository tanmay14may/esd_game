import streamlit as st
import math

st.set_page_config(page_title="Tic Tac Toe - AI vs Human", page_icon="🎮", layout="centered")

# ------------------ Game Logic ------------------

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_moves_left(board):
    return any(board[i][j] == " " for i in range(3) for j in range(3))

def evaluate(board):
    if check_winner(board, "O"):
        return 10
    elif check_winner(board, "X"):
        return -10
    return 0

def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate(board)
    if score == 10 or score == -10:
        return score
    if not is_moves_left(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    value = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    best = max(best, value)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        return best
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    value = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    best = min(best, value)
                    beta = min(beta, best)
                    if beta <= alpha:
                        return best
        return best

def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = " "
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move


# ------------------ Streamlit UI ------------------

st.title("🎮 Tic Tac Toe — Human (X) vs Computer (O)")
st.caption("by Tanmay (2401330120202)")
st.caption("by Ujjwal (2401330120204)")
st.caption("by Vaibhav (2401330120208)")


if "board" not in st.session_state:
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.game_over = False
    st.session_state.winner = None

board = st.session_state.board

def restart():
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.game_over = False
    st.session_state.winner = None

# Display board as buttons
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        if cols[j].button(board[i][j] if board[i][j] != " " else " ", key=f"{i}-{j}", use_container_width=True):
            if not st.session_state.game_over and board[i][j] == " ":
                board[i][j] = "X"
                if check_winner(board, "X"):
                    st.session_state.game_over = True
                    st.session_state.winner = "You (X)"
                elif not is_moves_left(board):
                    st.session_state.game_over = True
                    st.session_state.winner = "Draw"
                else:
                    move = find_best_move(board)
                    if move != (-1, -1):
                        board[move[0]][move[1]] = "O"
                    if check_winner(board, "O"):
                        st.session_state.game_over = True
                        st.session_state.winner = "Computer (O)"
                    elif not is_moves_left(board):
                        st.session_state.game_over = True
                        st.session_state.winner = "Draw"
                st.rerun()

st.write("---")

if st.session_state.winner:
    if st.session_state.winner == "You (X)":
        st.success("🎉 You Win!")
    elif st.session_state.winner == "Computer (O)":
        st.error("💻 Computer Wins!")
    else:
        st.info("🤝 It's a Draw!")

st.button("🔄 Restart Game", on_click=restart)

