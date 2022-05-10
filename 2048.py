#########################################
# groupe Bitd 3
# Rami YAMOUT
# Nel RIVART
# Morgan NOIRET
# Bertille LANOIRE
# https://github.com/uvsq22007534/tas_de_sable
#########################################




########################### Blibliothèques #######################################"

import tkinter as tk 
import time
import random 

# ---Fonctions---  

def generer_nombre(): #fonction permettant de générer un 2 ou un 4 aléatoirement
    val = random.random()
    if val < rate: 
        return 2 #90% de chance de générer un 2.
    return 4 #10% de chance de générer un 4.

def generation():   #fonction permettant d'ajouter des nombres dans des cases aléatoires du tableau, en fonction de si elles sont vides ou non. 
    case_random = []    
    for row in range(zone_taille): 
        for col in range(zone_taille):
            if zone[row][col] is vide:
                case_random.append([row,col]) 
                
    row, col = random.choice(case_random) 
    zone[row][col] = generer_nombre()

def creer_zone(window): #crée la fenêtre
    global affichage_score
    
    for i in range(16): #nombre de cases (4x4)
        row = i//4
        col = i%4
        label[i] = tk.Label(window, width=10, height=5, background='#d3d3d3', relief='ridge')
        label[i].grid(row=row+1, column=col)

    tk.Label(window, text="Score").grid(row=0 , column=2)
        
    affichage_score = tk.Label(window, text=score)
    affichage_score.grid(row=0 , column=3)

def maj_zone(): #mise à jour du tableau
    for i in range(16): 
        row = i//4
        col = i%4
        text = zone[row][col]
        if text == 0:
            text = ''
        label[i]["text"] = text

    affichage_score["text"] = score

def move_zone(direction, update=False): #fonction de conditions de mouvement dans le tableau.
    global score

    if direction == 0: #déplacement vers le haut
        for j in range(zone_taille):
            for i in range(zone_taille):
                new_zone[i][j] = zone[i][j] 
                
    if direction == 1: #déplacement vers le bas
        for i in range(zone_taille):
            for j in range(zone_taille):
                new_zone[i][j] = zone[zone_taille-1-i][zone_taille-1-j]
                
    if direction == 2: #déplacement vers la gauche
        for i in range(zone_taille):
            for j in range(zone_taille):
                new_zone[i][j] = zone[zone_taille-1-j][i]
                
    if direction == 3: #déplacement vers la droite
        for j in range(zone_taille):
            for i in range(zone_taille):
                new_zone[i][j] = zone[j][zone_taille-1-i]
                
    tempo_zone = [[vide for _ in range(zone_taille)] for _ in range(zone_taille)] #variable temporaire
    tempo_score = 0 #variable temporaire 
    
    for j in range(zone_taille):
        top = 0
        for i in range(zone_taille):
            if new_zone[i][j] != vide:
                if tempo_zone[top][j] == vide:
                    tempo_zone[top][j] = new_zone[i][j]
                elif new_zone[i][j] == tempo_zone[top][j]:
                    tempo_zone[top][j] *= 2
                    top += 1
                    tempo_score += tempo_zone[top-1][j]
                else:
                    top += 1
                    tempo_zone[top][j] = new_zone[i][j]
                    
    if update: 
        score += tempo_score
        # changement de la zone en fonction du déplacement choisi #
        if direction == 0:
            for j in range(zone_taille):
                for i in range(zone_taille):
                    zone[i][j] = tempo_zone[i][j]
        if direction == 1:
            for j in range(zone_taille):
                for i in range(zone_taille):
                    zone[i][j] = tempo_zone[zone_taille-1-i][zone_taille-1-j]
        if direction == 3:
            for j in range(zone_taille):
                for i in range(zone_taille):
                    zone[i][j] = tempo_zone[zone_taille-1-j][i]
        if direction == 2:
            for j in range(zone_taille):
                for i in range(zone_taille):
                    zone[i][j] = tempo_zone[j][zone_taille-1-i]
                    
    for i in range(zone_taille):
        for j in range(zone_taille):
            if tempo_zone[i][j] is not new_zone[i][j]:
                return True
            
    return False

def prochain_tour():
    vide_verif = False #vérification des cases vides.
                         
    for row in range(zone_taille):
        for col in range(zone_taille):
            if zone[row][col] == vide:
                vide_verif = True
                         
    if not vide_verif:
        for direct in range(4):
            move_zone(direct)

def game_over(): #problème
    for direct in range(4):
        if move_zone(direct, False):
            return False 
    return True

def get_input(event): #fonction permettant de faire déplacer la grille avec les touches du clavier
    global direction
    
    touche = event.keysym #synchronisation touche/jeu
    print('Touche :', touche)
    
    if touche == "Up":
        direction = 0
    if touche == "Down":
        direction = 1
    if touche == "Left":
        direction = 2
    if touche == "Right":
        direction = 3
    
def game_loop(): #fonction de la boucle principale du jeu. fonction principale.
    global direction
    
    if game_over():
        window.destroy()   # ferme la fenêtre
    else:        
        if direction is not None:        # ne marche que si une touche est pressée
            move_zone(direction, True)  # permet le mouvement (voir plus haut)
            generation()                   # génère un nouveau nombre (2 ou 4) (voir plus haut)
            maj_zone()               # met-à-jour les nombres dans les zones (voir plus haut)
            direction = None             # reset les directions pour le tour suivant.
        window.after(250, game_loop)        # temps de transition (250 ms)



def close_window():
    window.destroy()
def Exit() :
    window.destroy




        
# - Variables #

direction = None #variable de direction
label = {} #variable de paramétrage du tableau ()

zone_taille = 4 
vide = 0
zone     = [[vide for _ in range(zone_taille)] for _ in range(zone_taille)]
new_zone = [[vide for _ in range(zone_taille)] for _ in range(zone_taille)] 
score = 0 
rate = 0.9 #probabilité de tomber sur une case 2.

direction_move = [[1, 0], [-1, 0], [0, 1], [0, -1]]


# Main - Successions d'exécutions du programme

if __name__ == '__main__':
    # Paramètres de la fenêtre #
    window = tk.Tk() #ouvre Tkinter
    window.title("2048") #titre de la fenêtre
    window.geometry("345x430") #taille et proportions de la fenêtre
    bouton_start = tk.Button(text="Start", command= game_loop)
    bouton_start.place(x = 50, y= 350)
    bouton_exit = tk.Button(text="Exit", command= Exit())
    bouton_exit.place(x= 150, y=350)
    # -------------------------#

    window.bind("<Key>", get_input) 
    

    creer_zone(window)  # crée les labels 
    
    generation()         # génère le premier nombre du début
    generation()         # génère le deuxième nombre du début
    
    maj_zone()     # applique les changements de la zone de jeu
    
    
    
    window.mainloop()     # ouvre la fenêtre tkinter
    
    print("Votre score est", score)   #affichage du score dans le terminal

