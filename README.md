# projet_2048
#########################################
# groupe Bitd 3
# Rami YAMOUT
# Nel RIVART
# Morgan NOIRET
# Bertille LANOIRE
# https://github.com/uvsq22100752/projet_2048
#########################################

import random
import tkinter as tk  
import time

# ---Fonctions---  

def generer_nombre(): #fonction permettant de générer un 2 ou un 4 aléatoirement.
    tmp = random.random()
    if tmp < ratio: 
        return 2 
    return 4

def generate():   #fonction permettant d'ajouter des nombres dans des cases aléatoires du tableau, en fonction de si elles sont vides ou non. 
    alea_case = []    
    for row in range(board_size): 
        for col in range(board_size):
            if board[row][col] is blank:
                alea_case.append([row,col])

    row, col = random.choice(alea_case) 
    board[row][col] = generer_nombre()

def create_board(win): #tableau affiché en cas de victoire
    global score_show

    for i in range(16):
        row = i//4
        col = i%4
        label[i] = tk.Label(win, width=10, height=5, background='#d3d3d3', relief='ridge')
        label[i].grid(row=row+1, column=col)

    tk.Label(win, text="Score").grid(row=0 , column=2)

    score_show = tk.Label(win, text=score)
    score_show.grid(row=0 , column=3)

def update_board(): #création du tableau
    for i in range(16):
        row = i//4
        col = i%4
        text = board[row][col]
        if text == 0:
            text = ''
        label[i]["text"] = text

    score_show["text"] = score

def move_board(direction, update=False): #fonction de conditions de mouvement dans le tableau.
    global score

    if direction == 0: 
        for j in range(board_size):
            for i in range(board_size):
                new_board[i][j] = board[i][j] 

    if direction == 1:
        for i in range(board_size):
            for j in range(board_size):
                new_board[i][j] = board[board_size-1-i][board_size-1-j]

    if direction == 2:
        for i in range(board_size):
            for j in range(board_size):
                new_board[i][j] = board[board_size-1-j][i]

    if direction == 3:
        for j in range(board_size):
            for i in range(board_size):
                new_board[i][j] = board[j][board_size-1-i]

    tmp_board = [[blank for _ in range(board_size)] for _ in range(board_size)]
    tmp_score = 0

    for j in range(board_size):
        top = 0
        for i in range(board_size):
            if new_board[i][j] != blank:
                if tmp_board[top][j] == blank:
                    tmp_board[top][j] = new_board[i][j]
                elif new_board[i][j] == tmp_board[top][j]:
                    tmp_board[top][j] *= 2
                    top += 1
                    tmp_score += tmp_board[top-1][j]
                else:
                    top += 1
                    tmp_board[top][j] = new_board[i][j]

    if update:
        score += tmp_score
        if direction == 0:
            for j in range(board_size):
                for i in range(board_size):
                    board[i][j] = tmp_board[i][j]
        if direction == 1:
            for j in range(board_size):
                for i in range(board_size):
                    board[i][j] = tmp_board[board_size-1-i][board_size-1-j]
        if direction == 3:
            for j in range(board_size):
                for i in range(board_size):
                    board[i][j] = tmp_board[board_size-1-j][i]
        if direction == 2:
            for j in range(board_size):
                for i in range(board_size):
                    board[i][j] = tmp_board[j][board_size-1-i]

    for i in range(board_size):
        for j in range(board_size):
            if tmp_board[i][j] is not new_board[i][j]:
                return True

    return False


def next_turn():
    empty_check = False

    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == blank:
                empty_check = True

    if not empty_check:
        for direct in range(4):
            move_board(direct)

def game_over():
    for direct in range(4):
        if move_board(direct, False):
            return False
    return True

def get_input(event):
    global direction

    key = event.keysym
    print('key:', key)

    if key == "Up":
        direction = 0
    if key == "Down":
        direction = 1
    if key == "Left":
        direction = 2
    if key == "Right":
        direction = 3

def game_loop():
    global direction

    if game_over():
        win.destroy()   # ferme la fenêtre
    else:        
        if direction is not None:        # ne marche que si une touche est pressée
            move_board(direction, True)  # permet le mouvement
            generate()                   # créer un nouveau nombre (2 ou 4)
            update_board()               # met à jour les textes 
            direction = None             # reset les directions
        win.after(250, game_loop)        # ré-enclenchable 0,25 secondes plus tard 

# - variables 

direction = None
label = {}

board_size = 4
blank = 0
board     = [[blank for _ in range(board_size)] for _ in range(board_size)]
new_board = [[blank for _ in range(board_size)] for _ in range(board_size)]
score = 0
ratio = 0.9

direction_move = [[1, 0], [-1, 0], [0, 1], [0, -1]]

# - main

if __name__ == '__main__':

    win = tk.Tk()
    win.title("2048")
    win.geometry("345x430")

    win.bind("<Key>", get_input)  

    create_board(win)  

    generate()         # generate le premier nombre du début
    generate()         # generate le deuxième nombre du début

    update_board()     # change le texte 

    game_loop()        # démarre la boucle

    win.mainloop()      

    print("Votre score est", score)  
