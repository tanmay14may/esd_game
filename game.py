import tkinter as tk
from tkinter import messagebox
import math

# Initialize window
root = tk.Tk()
root.title("Tic Tac Toe - Human vs Computer (AI)")

# Global variables
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
player = "X"  # Human
computer = "O"

# ------------------ Game Logic ------------------

def check_winner(b, ch):
    for i in range(3):
        if all(b[i][j] == ch for j in range(3)) or all(b[j][i] == ch for j in range(3)):
            return True
    if all(b[i][i] == ch for i in range(3)) or all(b[i][2 - i] == ch for i in range(3)):
        return True
    return False

def is_moves_left(b):
    return any(b[i][j] == " " for i in range(3) for j in range(3))

def evaluate(b):
    if check_winner(b, computer):
        return 10
    elif check_winner(b, player):
        return -10
    return 0

def minimax(b, depth, is_maximizing, alpha, beta):
    score = evaluate(b)
    if score == 10 or score == -10:
        return score
    if not is_moves_left(b):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = computer
                    val = minimax(b, depth + 1, False, alpha, beta)
                    b[i][j] = " "
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = player
                    val = minimax(b, depth + 1, True, alpha, beta)
                    b[i][j] = " "
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def find_best_move(b):
    best_val = -math.inf
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if b[i][j] == " ":
                b[i][j] = computer
                move_val = minimax(b, 0, False, -math.inf, math.inf)
                b[i][j] = " "
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    return best_move

# ------------------ UI Logic ------------------

def disable_all_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")

def computer_move():
    if not is_moves_left(board):
        return
    move = find_best_move(board)
    if move != (-1, -1):
        i, j = move
        board[i][j] = computer
        buttons[i][j].config(text=computer, state="disabled", disabledforeground="red")

    if check_winner(board, computer):
        messagebox.showinfo("Game Over", "💻 Computer wins!")
        disable_all_buttons()
    elif not is_moves_left(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        disable_all_buttons()

def button_click(i, j):
    if board[i][j] == " ":
        board[i][j] = player
        buttons[i][j].config(text=player, state="disabled", disabledforeground="blue")

        if check_winner(board, player):
            messagebox.showinfo("Game Over", "🎉 You win!")
            disable_all_buttons()
            return
        elif not is_moves_left(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_all_buttons()
            return

        # Computer's turn
        root.after(500, computer_move)

def reset_game():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", state="normal")

# ------------------ GUI Layout ------------------

frame = tk.Frame(root)
frame.pack()

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(
            frame, text=" ", font=("Helvetica", 24), width=5, height=2,
            command=lambda i=i, j=j: button_click(i, j)
        )
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

reset_button = tk.Button(root, text="🔄 Reset Game", font=("Helvetica", 14), command=reset_game)
reset_button.pack(pady=10)

root.mainloop()
