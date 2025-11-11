import streamlit as st
import numpy as np

st.title("🎮 Tic Tac Toe - AI vs Human")

if 'board' not in st.session_state:
    st.session_state.board = [" "]*9
    st.session_state.turn = "X"

def check_winner(b, p):
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(b[a]==b[b_]==b[c]==p for a,b_,c in wins)

def best_move(b):
    # Simple AI: first empty spot
    for i in range(9):
        if b[i] == " ":
            return i
    return -1

cols = st.columns(3)
for i in range(9):
    if cols[i % 3].button(st.session_state.board[i] or " ", key=i):
        if st.session_state.board[i] == " ":
            st.session_state.board[i] = "X"
            if not check_winner(st.session_state.board, "X"):
                move = best_move(st.session_state.board)
                if move != -1:
                    st.session_state.board[move] = "O"
            st.rerun()

if check_winner(st.session_state.board, "X"):
    st.success("🎉 You win!")
elif check_winner(st.session_state.board, "O"):
    st.error("💻 Computer wins!")
elif all(cell != " " for cell in st.session_state.board):
    st.info("It's a draw!")
