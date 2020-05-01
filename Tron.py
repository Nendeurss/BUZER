import tkinter as tk
import random
import numpy as np
import copy
import time

# ---------------------------------------------------------------------------------------------------------------------
#   Données de partie
# ---------------------------------------------------------------------------------------------------------------------

Data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# Transforme le tableau d'entier ci-dessus en un tableau numpy contenant des entiers codés sur 8 bits
GInit = np.array(Data, dtype=np.int8)
# flip inverse chaque ligne du tableau : la première devient la dernière, la deuxième devient l'avant dernière, etc..
# transpose transforme les colonnes en lignes et les lignes en colonnes : [[1,2],[3,4]] devient [[1,3],[2,4]]
GInit = np.flip(GInit, 0).transpose()

LARGEUR = 13    # nombre de colonnes + 1
HAUTEUR = 17    # nombre de lignes + 1

# La classe Game nous permet de regrouper dans un même objet :
# - la grille,
# - la position du joueur
# - le score de partie
class Game:
    # Constructeur de la classe permet d'initialiser ses différents membres
    # Par défaut le score du joueur est à 0
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX  # Position du joueur en abscisse
        self.PlayerY = PlayerY  # Position du joueur en ordonnée
        self.Score = Score      # Score du joueur sur une partie
        self.Grille = Grille    # Grille de jeu

    # La fonction copy() permet de recopier toutes les données de la partie dans un autre objet.
    def copy(self):
        return copy.deepcopy(self)

# Création du jeu avec la grille de jeu définit au début
GameInit = Game(GInit, 3, 5)

# ---------------------------------------------------------------------------------------------------------------------
#   Création de la fenêtre principale  - NE PAS TOUCHER
# ---------------------------------------------------------------------------------------------------------------------

L = 20                      # L = largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L    # La largeur de la fenêtre correspond au nombre de colonne de la grille de jeu
hauteurPix = HAUTEUR * L    # La hauteur de la fenêtre correspond au nombre de ligne de la grille de jeu

Window = tk.Tk()            # Instanciation d'une fenêtre Tk avec le module tkinter
# La fonction geometry prend en paramètre un string qui définit les dimensions de la fenêtre - ex : 150x150
Window.geometry(str(largeurPix) + "x" + str(hauteurPix))
Window.title("TRON")        # Ajoute un titre à la fenêtre

# Création de la frame principale stockant toutes les pages
F = tk.Frame(Window)

# Les widgets ajouté dans la Frame s'organiseront de haut en bas,
# rempliront les espaces verticialement et horizontalement.
# expand permet d'indiquer que la Frame remplira tout l'espace de son parent (ici, la fenêtre)
F.pack(side="top", fill="both", expand=True)

# rowconfigure et columnconfigure permettent de gérer les dimensions des lignes et colonnes
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# ---------------------------------------------------------------------------------------------------------------------
# Gestion des différentes pages
# ---------------------------------------------------------------------------------------------------------------------

ListePages = {}
PageActive = 0

# Fonction qui crée une page et l'ajoute dans la liste de page, la dimension et renvoie cette page
def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

# Permet de modifier la page affichée avec l'id de la nouvelle page en argument
def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()

# ---------------------------------------------------------------------------------------------------------------------
# Crée la première page
# ---------------------------------------------------------------------------------------------------------------------

Frame0 = CreerUnePage(0)

# Insère la page dans un canvas
canvas = tk.Canvas(Frame0, width=largeurPix, height=hauteurPix, bg="black")
# Positionne le canvas
canvas.place(x=0, y=0)

# ---------------------------------------------------------------------------------------------------------------------
#  Dessine la grille de jeu - ne pas toucher
# ---------------------------------------------------------------------------------------------------------------------

# Affiche la grille de jeu
def Affiche(Game):
    canvas.delete("all")        # Efface la fenêtre de jeu
    H = canvas.winfo_height()   # Récupère la hauteur de la fenêtre de jeu

    # Dessine une case
    def DrawCase(x, y, coul):
        x *= L
        y *= L
        canvas.create_rectangle(x, H - y, x + L, H - y - L, fill=coul)

    # Dessin des murs
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Game.Grille[x, y] == 1: DrawCase(x, y, "#483d8b")   # les obstacles/murs sont en gris
            if Game.Grille[x, y] == 2: DrawCase(x, y, "#4b0082")   # les cases sur lesquels on s'est déplacé sont en bleu

    # dessin de la moto
    DrawCase(Game.PlayerX, Game.PlayerY, "#8a2be2")                 # le personnage est en rouge

# Affiche de score dans la fenêtre de jeu
def AfficheScore(Game):
    info = "SCORE : " + str(Game.Score)
    canvas.create_text(80, 13, font='Helvetica 12 bold', fill="yellow", text=info)

# ---------------------------------------------------------------------------------------------------------------------
# Gestion du joueur IA
# VOTRE CODE ICI
# ---------------------------------------------------------------------------------------------------------------------

# Renvoie un tuple/liste de position(s) jouable(s)
def FindpossiblePlays(Game):
    # On récupère la position du joueur
    x, y = Game.PlayerX, Game.PlayerY
    # On initialise la liste de position(s) jouable(s)
    possiblePlays = list()

    # test de déplacement vers le haut
    if (Game.Grille[x, y + 1] == 0):
        possiblePlays.append((x, y + 1))
    # test de déplacement vers le bas
    if (Game.Grille[x, y - 1] == 0):
        possiblePlays.append((x, y - 1))
    # test de déplacement vers la gauche
    if (Game.Grille[x - 1, y] == 0):
        possiblePlays.append((x - 1, y))
    # test de déplacement vers la droit
    if (Game.Grille[x + 1, y] == 0):
        possiblePlays.append((x + 1, y))

    # On renvoie la liste de position(s) jouable(s)
    return possiblePlays

# Simule une partie entière
def SimulateGame(Game):
    while (1):

        possiblePlays = FindpossiblePlays(Game)

        pPLen = len(possiblePlays)

        if (pPLen == 0):
            return Game.Score
        else:
            index = random.randrange(len(possiblePlays))
            x, y = Game.PlayerX, Game.PlayerY
            Game.Grille[x, y] = 2
            Game.PlayerX, Game.PlayerY = possiblePlays[index][0], possiblePlays[index][1]
            Game.Score += 1

# Exécute l'algorithme de Monté-Carlo sur n parties
def MonteCarlo(Game, nbParties):
    Total = 0
    for i in range(nbParties):
        Game2 = Game.copy()
        Total += SimulateGame(Game2)
    return Total / nbParties

# Renvoie la position du prochain coup
def NextPlay(Game, PlayerX, PlayerY):
    # On récupère les position(s) possible(s)
    possiblePlays = FindpossiblePlays(Game)
    # Si il n'y a aucune position possible, fin de jeu, on retourne une liste vide
    if (len(possiblePlays) == 0):
        return list()

    # On initialise une liste qui contiendra le score moyen de chaque simulation de partie faite par MonteCarlo
    averageScore = list()
    # On copie la partie en cours dans un autre objet pour ne pas le modifier
    Game2 = Game.copy()

    # Pour chaque position possible
    for i in possiblePlays:
        # On place le joueur dans la copie de grille
        Game2.Grille[PlayerX, PlayerY] = 2
        Game2.PlayerX = i[0]
        Game2.PlayerY = i[1]
        # On ajoute le score retourné de MonteCarlo dans la liste de score
        averageScore.append(MonteCarlo(Game2, 1000))

    # On récupère l'indice de la valeur maximale de la liste des scores
    maxScore = averageScore.index(max(averageScore))

    print("\nMeilleure position : " + str(possiblePlays[maxScore]))
    return possiblePlays[maxScore]

# Démarre la partie et renvoyant si la partie est finie ou non
def Play(Game):
    # Tstart récupère le temps auquel on a commencé la partie
    Tstart = time.time()
    # x et y prennent les valeurs d'abscisses et d'ordonnées du joueur
    x, y = Game.PlayerX, Game.PlayerY
    # On affiche les positions du joueur
    print('Position actuelle : (' + str(x) + ', ' + str(y) + ')')

    # La position actuelle du joueur sera une case où il faudra laissé une trace :
    # Pour ça on lui affecte la valeur 2
    Game.Grille[x, y] = 2

    # On récupère les de position(s) possible(s)
    possiblePlay = NextPlay(Game, x, y)
    # Si il n'y a aucune position possible, fin de jeu, on retourne True
    if len(possiblePlay) == 0:
        return True

    # Sinon x et y prennent les valeurs de la nouvelle position du joueur
    x, y = possiblePlay[0], possiblePlay[1]

    # On affecte la position du joueur
    Game.PlayerX = x  # valide le déplacement
    Game.PlayerY = y  # valide le déplacement
    # On augmente le score de 1 car on a parcouru une case
    Game.Score += 1
    # Le temps mis pour un déplacement d'une case est déterminé par la formule suivante
    print("Temps d'exécution du coup : " + str(time.time() - Tstart) + "s")

    # la partie continue, on retourne False
    return False

# ---------------------------------------------------------------------------------------------------------------------

# On crée un objet CurrentGame qui recopie l'objet GameInit
CurrentGame = GameInit.copy()

# Permet de générer une partie
def Partie():
    # Lance un coup et renvoie si le joueur a touché un obstacle
    PartieTermine = Play(CurrentGame)

    if not PartieTermine:
        # Si la partie n'est pas terminé, on (ré)affiche la fenêtre de jeu
        Affiche(CurrentGame)

        # Appelle la fonction Partie après une pause de 1000ms
        Window.after(1000, Partie)
    else:
        # Quand le joueur entre en collision avec un obstacle, la partie est terminée, on affiche le score
        AfficheScore(CurrentGame)

# ---------------------------------------------------------------------------------------------------------------------
#  Mise en place de l'interface - ne pas toucher
# ---------------------------------------------------------------------------------------------------------------------

# On affiche la page 0
AfficherPage(0)
# Appelle la fonction Partie après une pause de 1000ms
Window.after(100, Partie)
# La fonction mainloop permet de stopper l'exécution ici et donc d'effectuer en boucle le programme
Window.mainloop()