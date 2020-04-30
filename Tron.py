import copy
import random
import tkinter as tk

import numpy as np
import time

#################################################################################
#
#   Données de partie

Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

LARGEUR = 13
HAUTEUR = 17

# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille
    
    def copy(self): 
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix))   # taille de la fenetre
Window.title("TRON")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()
    
    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)
    
    # dessin des murs 
   
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"gray" )
           if Game.Grille[x,y] == 2  : DrawCase(x,y,"cyan" )
   
    
    # dessin de la moto
    DrawCase(Game.PlayerX,Game.PlayerY,"red" )

def AfficheScore(Game):
   info = "SCORE : " + str(Game.Score)
   canvas.create_text(80, 13,   font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI
def FindpossiblePlays(Game):
    x,y = Game.PlayerX, Game.PlayerY
    possiblePlays = list()

    if(Game.Grille[x,y+1] == 0):
        possiblePlays.append((x,y+1))
    if(Game.Grille[x,y-1] == 0):
        possiblePlays.append((x,y-1))
    if(Game.Grille[x-1,y] == 0):
        possiblePlays.append((x-1,y))
    if(Game.Grille[x+1,y] == 0):
        possiblePlays.append((x+1,y))

    return possiblePlays

def SimulateGame(Game):
    while(1):
        possiblePlays = FindpossiblePlays(Game)
        pPLen = len(possiblePlays)

        if(pPLen == 0):
            return Game.Score
        else:
            index = random.randrange(len(possiblePlays))
            x,y = Game.PlayerX, Game.PlayerY
            Game.Grille[x,y] = 2
            Game.PlayerX,Game.PlayerY = possiblePlays[index][0],possiblePlays[index][1]
            Game.Score+=1


def MonteCarlo(Game,nbParties):
    Total = 0
    for i in range(nbParties):
        Game2 = Game.copy()
        Total += SimulateGame(Game2)
    return Total/nbParties

def NextPlay(Game,PlayerX,PlayerY):
    possiblePlays = FindpossiblePlays(Game)
    if(len(possiblePlays) == 0):
      return list()

    averageScore = list()
    Game2 = Game.copy()
    for i in possiblePlays:
        Game2.Grille[PlayerX,PlayerY] = 2
        Game2.PlayerX = i[0]
        Game2.PlayerY = i[1]
        averageScore.append(MonteCarlo(Game2,1000))
    

    maxScore = 0

    for i in range(len(averageScore)):
        print(str(averageScore[i])+" - move : ")
        print(possiblePlays[i])
        if(averageScore[maxScore] < averageScore[i]):
            print("Set maxScore to i")
            maxScore = i
    
    print(" \n play : "+str(possiblePlays[maxScore]))
    return possiblePlays[maxScore]

def Play(Game):   
    
    Tstart = time.time()
    x,y = Game.PlayerX, Game.PlayerY
    print(x,y)

    Game.Grille[x,y] = 2  # laisse la trace de la moto

    # y += 1  # on essaye de bouger vers le haut
    
    # possiblePlays = FindpossiblePlays(Game) #on récupère les coups possibles
    # pPLen = len(possiblePlays)
    # if pPLen == 0:
    #     #Aucun coup possible
    #     return True #partie terminé

    # index = random.randrange(pPLen) #on récupère un coup aléatoire

    # x,y = possiblePlays[index][0],possiblePlays[index][1]

    possiblePlay = NextPlay(Game,x,y)
    x,y = possiblePlay[0],possiblePlay[1]

    v = Game.Grille[x,y]
    
    if v > 0 :
        # collision détectée
        return True # partie terminée
    else :
       Game.PlayerX = x  # valide le déplacement
       Game.PlayerY = y  # valide le déplacement
       Game.Score += 1
       print(time.time() - Tstart)
       return False   # la partie continue
     

################################################################################
     
CurrentGame = GameInit.copy()
 

def Partie():

    PartieTermine = Play(CurrentGame)
    
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(1000,Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
