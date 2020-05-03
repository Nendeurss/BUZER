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

# dx contient à chaque indice le déplacement en abscisse du joueur en fonction du choix aléatoire
# dy contient à chaque indice le déplacement en ordonnée du joueur en fonction du choix aléatoire
# Pour chaque indice, 0 : sur place, 1: left, 2: Up, 3: Right, 4: Down
dx = np.array([0, -1, 0,  1,  0], dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1], dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)

Debug = False	# Si Debug est activé (True), chaque grilles en parallèles seront affichées dans la console

# Affiche les grilles de jeu exécutées en parallèle de l'application dans la console (MODE DEBUG)
def AffGrilles(G, X, Y):
    nbG, larg, haut = G.shape
    for y in range(haut - 1, -1, -1):
        for i in range(nbG):
            for x in range(larg):
                g = G[i]
                c = ' '
                if G[i, x, y] == 1: c = 'M'  # mur
                if G[i, x, y] == 2: c = 'O'  # trace
                if (X[i], Y[i]) == (x, y): c = 'X'  # joueur
                print(c, sep='', end='')
            print(" ", sep='', end='')  # espace entre les grilles
        print("")  # retour à la ligne

nb = 10000 		# nb de parties en parallèle

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

# La position initiale du joueur est aléatoire, on s'assure que cette position n'est pas un obstacle
randX = 0
randY = 0
while Data[randX][randY] == 1:
    randX = np.random.randint(1, 11)
    randY = np.random.randint(1, 15)

# Création du jeu avec la grille de jeu définit au début
GameInit = Game(GInit, randX, randY)

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
	# La fonction simulant une partie s'arrête que lors d'une instruction break
    while (1):
		# On récupère la liste de position(s) jouable(s)
        possiblePlays = FindpossiblePlays(Game)
		# On récupère le nombre de position(s) jouable(s)
        pPLen = len(possiblePlays)

		# S'il n'y a aucune position jouable, fin de jeu, donc fin de simulation
        if (pPLen == 0):
            return Game.Score
		# Sinon on déplace le joueur dans une des directions possible aléatoirement
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
def NextPlay(Game):
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
        Game2.Grille[Game.PlayerX, Game.PlayerY] = 2
        Game2.PlayerX = i[0]
        Game2.PlayerY = i[1]
        # On ajoute le score retourné de MonteCarlo dans la liste de score
        # averageScore.append(MonteCarlo(Game2, 1000))
        averageScore.append(Simulate(Game2))

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
    possiblePlay = NextPlay(Game)
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


# ---------------------------------------------------------------------------------------------
# Gestion des parties en parallèle
# ---------------------------------------------------------------------------------------------

# Simule les nb parties en parallèle
def Simulate(Game):

    # On copie les datas de départ pour créer plusieurs parties en parallèles
    G      = np.tile(Game.Grille,(nb,1,1))	# G contient la liste des grilles de jeu qui seront jouées en parallèle
    X      = np.tile(Game.PlayerX,nb)		# X contient la liste des positions en abscisse du joueur sur chaque grille
    Y      = np.tile(Game.PlayerY,nb)		# Y contient la liste des positions en ordonnée du joueur sur chaque grille
    S      = np.tile(Game.Score,nb)			# S contient la liste des scores de chaque grille
    I      = np.arange(nb)  				# I est une liste d'indice permettant d'itérer/d'accéder à une grille en particulier

    # VOTRE CODE ICI
	# ---------------------------------------------------------------------------------------------
    if Debug :
        AffGrilles(G,X,Y)

    OldScore = -1

    #On créer des vecteurs pour chaque directions, que l'on set à True, qui vont nous indiquer si une case est jouable
    Vgauche = np.tile(True,nb)
    Vdroite = np.tile(True,nb)
    Vhaut = np.tile(True,nb)
    Vbas = np.tile(True,nb)

    #On transforme les True en 1 et les False en 0
    Vgauche = (Vgauche == 1)*1
    Vdroite = (Vdroite == 1)*1
    Vhaut = (Vhaut == 1)*1
    Vbas = (Vbas == 1)*1

    while(1) :
        if Debug :
            print("X : ",X)
            print("Y : ",Y)
            print("S : ",S)

        # On marque le passage de la moto dans chaque grille
        G[I, X, Y] = 2

        # On crée un tableau de nbx4 remplis de 0 pour stocker les directions possible de chaque joueur sur chaque grille.
        LPossibles = np.zeros((nb,4), dtype=np.int8)

        # On crée un vecteur permmettant de connaître les directions possibles de chaque joueur sur chaque grille
        Indices = np.zeros(nb,dtype=np.int8)

        if Debug :
            print("Indices : ",Indices)

        # Je remplis les vecteurs des valeurs de directions ex: Vgauche = [1,1,1,1,....]; Vhaut = [2,2,2,2,....]; ....
        Vgauche = (G[I,X-1,Y] == 0)*1
        Vhaut = (G[I,X,Y+1] == 0)*2
        Vdroite = (G[I,X+1,Y] == 0)*3
        Vbas = (G[I,X,Y-1] == 0)*4

        if Debug :
            print("Vgauche :",Vgauche)

        # J'incrémente Indices si on a add une direction possible
        # Par exemple si j'ai add 1 dans LPossibles[I,Indices], alors je dois retrouver 1 dans LPossibles[I, Indices]
        LPossibles[I,Indices] = Vgauche
        Indices = Indices + (LPossibles[I,Indices] != 0)
        LPossibles[I,Indices] = Vhaut
        Indices = Indices + (LPossibles[I,Indices] != 0)
        LPossibles[I,Indices] = Vdroite
        Indices = Indices + (LPossibles[I,Indices] != 0)
        LPossibles[I,Indices] = Vbas
        Indices = Indices + (LPossibles[I,Indices] != 0)

        Indices[Indices == 0] = 1

        if Debug :
            print("LPossibles :",LPossibles)
            print("Indices :",Indices)
            print("Vgauche : ",Vgauche)

        R = np.random.randint(12,size=nb)
        if Debug :
            print("R : ",R)

        R = R % Indices
        if Debug :
            print("R : ",R)

        # On récupère le choix de direction : 1 = Left, 2 = Up, 3 = Right, 4 = Down
        Choix = LPossibles[I,R]
		# On récupère le score
        Score = ds[Choix]

        # On modifie la position de chaque joueur sur chaque grille et on incrémente le score de chaque grille
        DX = dx[Choix]
        DY = dy[Choix]
        if Debug :
            print("DX : ", DX)
            print("DY : ", DY)

        X += DX
        Y += DY
        S += Score

        NewScore = np.sum(S)

		# Si l'ancien score correspond au nouveau, c'est que le joueur ne bouge plus, la partie est donc terminée, on sort de la simulation
        if(NewScore == OldScore):
            break
        OldScore = NewScore

        #debug
        if Debug :
            AffGrilles(G,X,Y)
            time.sleep(1)

    return np.mean(S)

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
        Window.after(1, Partie)
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