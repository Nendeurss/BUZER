import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Création de la fenetre principale  - ne pas toucher
# ---------------------------------------------------

# Nombre de pixels en largeur et en longueur
LARG = 300
HAUT = 300

Window = tk.Tk()                            # On instancie la fenêtre principale
Window.geometry(str(LARG)+"x"+str(HAUT))    # On dimensionne la fenêtre
Window.title("ESIEE - Morpion")             # Ajotu d'un titre à la fenpetre


# Création de la frame principale stockant toutes les pages
# ---------------------------------------------------------

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
# Configuration des dimensions des lignes et colonnes
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# Gestion des différentes pages
# -----------------------------

ListePages = {} # Liste de pages
PageActive = 0  # Contient l'ID de la page qui est affiché dans la fenêtre principale

# Renvoie une nouvelle page avec un ID spécifique
def CreerUnePage(id):
    Frame = tk.Frame(F)     # Instancie une nouvelle Frame
    ListePages[id] = Frame  # Ajout de la nouvelle page dans la liste des pages
    Frame.grid(row=0, column=0, sticky="nsew")  # Configuration de la disposition des futures objets fils de la Frame
    return Frame

# On affiche la page portant l'ID spécifié en argument
def AfficherPage(id):
    global PageActive   # On s'apprête à modifier la valeur de PageActive qui est une variable globale
    PageActive = id     # On affecte à PageActive l'ID de la page que l'on souhaite affichée
    ListePages[id].tkraise()    # Permet de faire passer la page devant l'ancienne

#On crée une nouvelle page d'ID 0
Frame0 = CreerUnePage(0)

# On instancie un canvas de la taille de la fenêtre principale avec un fond noir
canvas = tk.Canvas(Frame0, width=LARG, height=HAUT, bg="black")
canvas.place(x=0,y=0)

# ----------------------------------------------------------------------------------------------------------------------
# Paramètres du jeu
# ------------------
 
Grille = [ [0,0,0],
           [0,0,0],
           [0,0,0] ]        # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille, dtype=np.int8)    # On transforme la grille, un tableau 2d, en tableau numpy
Grille = np.flip(Grille, 0).transpose()     # Pour avoir x,y : [0;0] se trouve en bas à gauche

# ----------------------------------------------------------------------------------------------------------------------
# Gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

playerStart = False  # Indique si le joueur commence à jouer en premier
nbCoups = 0
lastPlay_X = []
lastPlay_Y = []

def Play(x,y):             
    Grille[x][y] = 1
    print("ME | x : " + str(x) + " - y : " + str(y))

def IA():
    if playerStart == True:
        return None
    else:
        if nbCoups == 0:
            x, y = 1, 1
            while x == 1 or y == 1 or Grille[x][y] != 0:
                x = np.random.randint(0, 3)
                y = np.random.randint(0, 3)
            print("IA | x : " + str(x) + " - y : " + str(y))
            Grille[x][y] = 2
        


# ----------------------------------------------------------------------------------------------------------------------
# Gestion du dessin de la grille de jeu

# Dessine la grille de jeu
def Dessine(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")    # On efface l'ancien contenu du canvas

        # On dessine la grille
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill="blue", width="4" )
            canvas.create_line(0,i*100,300,i*100,fill="blue", width="4" )

        # On dessine les coups du joueur et de l'IA
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100
                # Si la case [x;y] = 1, on dessine une croix (joueur)
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                # Si la case [x;y] = 2, on dessine un rond (IA)
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        
# Fonction appelée par un clic souris sur la zone de dessin
def MouseClick(event):
   
    Window.focus_set()  # La fenêtre principale a le focus
    # Conversion d'une coordonée pixel écran en coord grille de jeu
    x = event.x // 100
    y = event.y // 100

    # Si x ou y n'est pas compris entre 0 et deux, on est en dehors de la grille, on ne considère pas cela comme un coup
    if (0 > x) or (x > 2) or (0 > y) or (y > 2) or Grille[x][y] != 0:
        return

    # [0;0] est tout en haut à gauche
    print("Joueur joue en [" + str(x) + ';' + str(y) + ']')
    
    Play(x,y)   # Gestion du joueur humain et de l'IA
    IA()
    
    Dessine()   # Redessine la grille de jeu

# On lie le canvas à un événement, celui d'un clic de la souris
canvas.bind('<ButtonPress-1>', MouseClick)

# ----------------------------------------------------------------------------------------------------------------------
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)     # On affiche la fenêtre
Dessine()           # On dessine la grille
Window.mainloop()   # On répète les deux dernières instructions à l'infini


  


    
        

      
 

