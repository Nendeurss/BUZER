import tkinter as tk
import random
import time
import numpy as np


Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,0,0,0,0,0,0,0,0,0,1],
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

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille

    def copy(self):
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

#############################################################
#
#  affichage en mode texte


def AffGrilles(G,X,Y):
    nbG, larg , haut = G.shape
    for y in range(haut-1,-1,-1) :
        for i in range(nbG) :
            for x in range(larg) :
               g = G[i]
               c = ' '
               if G[i,x,y] == 1 : c = 'M'  # mur
               if G[i,x,y] == 2 : c = 'O'  # trace
               if (X[i],Y[i]) == (x,y) : c ='X'  # joueur
               print(c,sep='', end = '')
            print(" ",sep='', end = '') # espace entre les grilles
        print("") # retour à la ligne


###########################################################
#
# simulation en parallèle des parties


# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)

Debug = True
nb = 5 # nb de parties


def Simulate(Game):

    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True
    if Debug : AffGrilles(G,X,Y)

    # VOTRE CODE ICI

    #On créer le vecteur Vgauche, et on met tout à True
    Vgauche = np.tile(True,nb)
    Vdroite = np.tile(True,nb)
    Vhaut = np.tile(True,nb)
    Vbas = np.tile(True,nb)
    #On transforme les True en 1 et les False en 0
    Vgauche = (Vgauche == 1)*1
    Vdroite = (Vdroite == 1)*1
    Vhaut = (Vhaut == 1)*1
    Vbas = (Vbas == 1)*1

    

    while(boucle) :
        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        # marque le passage de la moto
        G[I, X, Y] = 2

        #On créer un vecteur de tableau des coups possibles et on met tout à 0
        LPossibles = np.zeros((nb,4),dtype=np.int8)

        #On créer un vecteur d'indice et on met tout à zero
        Indices = np.zeros(nb,dtype=np.int8)

        print("Indices : ",Indices)

        #Je remplis les vecteurs des valeurs de directions ex: Vgauche = [1,1,1,1,....]; Vhaut = [2,2,2,2,....]; ....
        Vgauche = (G[I,X-1,Y] == 0)*1
        Vdroite = (G[I,X+1,Y] == 0)*3
        Vbas = (G[I,X,Y-1] == 0)*4
        Vhaut = (G[I,X,Y+1] == 0)*2

        print("Vgauche :",Vgauche)

        #J'incrémente Indices si on a add une direction possible
        #Par exemple si j'ai add 1 dans LPossibles[I,Indices], alors je dois retrouver 1 dans LPossibles[I,Indices]
        LPossibles[I,Indices] = Vgauche
        Indices = Indices + (LPossibles[I,Indices] != 0)
        LPossibles[I,Indices] = Vhaut
        Indices = Indices + (LPossibles[I,Indices] != 0)
        LPossibles[I,Indices] = Vdroite
        Indices = Indices + (LPossibles[I,Indices] != 0)
        LPossibles[I,Indices] = Vbas
        Indices = Indices + (LPossibles[I,Indices] != 0)

        print("LPossibles :",LPossibles)
        print("Indices :",Indices)

        if Debug :print("Vgauche : ",Vgauche)

        # Direction : 2 = vers le haut
        Choix = np.ones(nb,dtype=np.uint8) * 2


        #DEPLACEMENT
        DX = dx[Choix]
        DY = dy[Choix]
        if Debug : print("DX : ", DX)
        if Debug : print("DY : ", DY)
        X += DX
        Y += DY


        #debug
        if Debug : AffGrilles(G,X,Y)
        if Debug : time.sleep(2)

    print("Scores : ",np.mean(S))



Simulate(GameInit)

