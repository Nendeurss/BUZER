import tkinter as tk
from tkinter import messagebox
import copy
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

DebutPartie = True
nbCoups = 0

def VerifColonnes(GrilleToCheck):
    # Vérification de colonne
    win = list()
    for row in range(3):
        win.append(GrilleToCheck[row][0])
        win.append(GrilleToCheck[row][1])
        win.append(GrilleToCheck[row][2])
        if win.count(1) == 3 or win.count(2) == 3:
            return True
        else:
            win.clear()
    return False

def VerifLignes(GrilleToCheck):
    # Vérification de ligne
    win = list()
    for column in range(3):
        win.append(GrilleToCheck[0][column])
        win.append(GrilleToCheck[1][column])
        win.append(GrilleToCheck[2][column])
        if win.count(1) == 3 or win.count(2) == 3:
            return True
        else:
            win.clear()
    return False

def VerifDiagGD(GrilleToCheck):
    # Vérification de la diagonale gauche-droite
    win = list()
    for i in range(3):
        win.append(GrilleToCheck[i][i])
    if win.count(1) == 3 or win.count(2) == 3:
        return True
    else:
        return False

def VerifDiagDG(GrilleToCheck):
    # Vérification de la diagonale droite-gauche
    win = list()
    for i in range(3):
        win.append(GrilleToCheck[2-i][i])
    if win.count(1) == 3 or win.count(2) == 3:
        return True
    else:
        return False

def VerifDraw(GrilleToCheck):
    n = 0
    for row in range(3):
        for column in range(3):
            if GrilleToCheck[row][column] == 0:
                return False
            if GrilleToCheck[row][column] == 1:
                n += 1
            elif GrilleToCheck[row][column] == 2:
                n -= 1
    if n == 1:
        return True
    else:
        return False

def Play(x,y):
    global nbCoups
    Grille[x][y] = 1
    print("ME | [" + str(x) + "][" + str(y) + "]")
    Dessine()
    nbCoups += 1

def Debug_AfficheGrille(GrilleToPrint):
    for row in range(3):
        print("[" + str(GrilleToPrint[row][0]) + "]" + "[" + str(GrilleToPrint[row][1]) + "]" + "[" + str(GrilleToPrint[row][2]) + "]")
    print("\n")

def bestMove(results = []):
    nbResults = len(results)
    winnerMoves = []

    # Si un coup a permis de gagner, on le stocke dans une liste
    for r in range(nbResults):
        if results[r][0] == "IA":
            winnerMoves.append(results[r])

    bestMove = -1
    bestMoveIndex = -1

    if len(winnerMoves) > 0:
        bestMove = winnerMoves[0][1]
        bestMoveIndex = 0
        nbWinnerMoves = len(winnerMoves)
        for w in range(nbWinnerMoves):
            if winnerMoves[w][1] < bestMove:
                bestMove = winnerMoves[w][1]
                bestMoveIndex = 0
        return winnerMoves[bestMoveIndex]

    # Si un coup permet le match num
    for r in range(nbResults):
        if results[r][0] == "N":
            winnerMoves.append(results[r])

    if len(winnerMoves) > 0:
        bestMove = winnerMoves[0][1]
        bestMoveIndex = 0
        nbWinnerMoves = len(winnerMoves)
        for w in range(nbWinnerMoves):
            if winnerMoves[w][1] < bestMove:
                bestMove = winnerMoves[w][1]
                bestMoveIndex = 0
        return winnerMoves[bestMoveIndex]

    return []

def IaSimulation(GrilleToCopy, nbCoups=0):
    # On vérifie si le jeu est fini
    if VerifColonnes(GrilleToCopy) or VerifLignes(GrilleToCopy) or VerifDiagGD(GrilleToCopy) or VerifDiagDG(GrilleToCopy):
        return "H"
    elif VerifDraw(GrilleToCopy):
        return "N"

    # On recopie la grille passé en paramètre pour ne pas la modifier
    VirtualGrille = []
    for rows in range(3):
        row = []
        for columns in range(3):
            row.append(GrilleToCopy[rows][columns])
        VirtualGrille.append(row)

    # On récupère une liste des coups possibles
    possibleMoves = []
    for row in range(3):
        for column in range(3):
            if VirtualGrille[row][column] == 0:
                possibleMoves.append([row, column])

    # On crée une liste de résultats
    results = []

    # Pour chaque coups possibles
    for m in possibleMoves:
        VirtualGrille[m[0]][m[1]] = 2
        nbCoups += 1
        iaPlayResult = HumanSimulation(VirtualGrille, nbCoups)
        results.append([iaPlayResult, nbCoups, m])
        VirtualGrille[m[0]][m[1]] = 0

    return bestMove(results)

def HumanSimulation(GrilleToCopy, nbCoups=0):
    # On vérifie si le jeu est fini
    if VerifColonnes(GrilleToCopy) or VerifLignes(GrilleToCopy) or VerifDiagGD(GrilleToCopy) or VerifDiagDG(GrilleToCopy):
        return "IA"
    elif VerifDraw(GrilleToCopy):
        return "N"

    # On recopie la grille passé en paramètre pour ne pas la modifier
    VirtualGrille = []
    for rows in range(3):
        row = []
        for columns in range(3):
            row.append(GrilleToCopy[rows][columns])
        VirtualGrille.append(row)

    # On récupère une liste des coups possibles
    possibleMoves = []
    for row in range(3):
        for column in range(3):
            if VirtualGrille[row][column] == 0:
                possibleMoves.append([row, column])

    # On crée une liste de résultats
    results = []

    # Pour chaque coups possibles
    for m in possibleMoves:
        VirtualGrille[m[0]][m[1]] = 1
        nbCoups += 1
        iaPlayResult = IaSimulation(VirtualGrille, nbCoups)
        results.append([iaPlayResult, m])
        VirtualGrille[m[0]][m[1]] = 0

    return bestMove(results)

# Fonction jouant contre l'utilisateur
def IA():
    global nbCoups

    moves = IaSimulation(Grille, nbCoups)

    move_x = -1
    move_y = -1

    if moves is not None and len(moves) > 0:
        move_x = moves[2][0]
        move_y = moves[2][1]
    else:
        move_x = np.random.randint(0, 3)
        move_y = np.random.randint(0, 3)
        while Grille[move_x][move_y] != 0:
            move_x = np.random.randint(0, 3)
            move_y = np.random.randint(0, 3)

    Grille[move_x][move_y] = 2
    nbCoups += 1
    print("IA | [" + str(move_x) + "][" + str(move_y) + "]")
    Dessine()

# ----------------------------------------------------------------------------------------------------------------------
# Gestion du dessin de la grille de jeu

def ResetGrille():
    for row in range(3):
        for column in range(3):
            Grille[row][column] = 0
    Dessine()

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
    global DebutPartie

    Window.focus_set()  # La fenêtre principale a le focus

    """
    Si DébutDePartie // lancement d’une nouvelle partie
        Remise à zéro des cases
        Affichage de la grille (bleu par défaut)
        DébutDePartie = Faux
    """
    if DebutPartie:
        for row in range(3):
            for column in range(3):
                Grille[row][column] = 0
        Dessine()
        DebutPartie = False

    """
    Si la case cliquée contient déjà un pion => quittez
    """
    # Conversion d'une coordonée pixel écran en coord grille de jeu
    x = event.x // 100
    y = event.y // 100

    # Si x ou y n'est pas compris entre 0 et deux = > on est en dehors de la grille,
    # Si la case a déjà été joué, on ne considère pas cela comme un coup
    if (0 > x) or (x > 2) or (0 > y) or (y > 2) or Grille[x][y] != 0:
        return

    Play(x,y)   # Gestion du joueur humain et de l'IA
    if VerifColonnes(Grille) or VerifLignes(Grille) or VerifDiagDG(Grille) or VerifDiagGD(Grille):
        print("WINNER")
        DebutPartie = True
        ResetGrille()
    elif VerifDraw(Grille):
        print("DRAW")
        DebutPartie = True
        ResetGrille()
    else:
        IA()
        if VerifColonnes(Grille) or VerifLignes(Grille) or VerifDiagDG(Grille) or VerifDiagGD(Grille):
            DebutPartie = True
            print("LOOSER")
            ResetGrille()
        elif VerifDraw(Grille):
            print("DRAW")
            DebutPartie = True
            ResetGrille()

# On lie le canvas à un événement, celui d'un clic de la souris
canvas.bind('<ButtonPress-1>', MouseClick)

# ----------------------------------------------------------------------------------------------------------------------
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)     # On affiche la fenêtre
Dessine()           # On dessine la grille
Window.mainloop()   # On répète les deux dernières instructions à l'infini











