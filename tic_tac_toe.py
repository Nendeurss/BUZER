import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


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

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu
 
Grille = [ [0,0,1], 
           [2,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille

Winner = 0 #1 Si c'est le joueur, 2 Si c'est l'IA
Score = np.zeros(2,encode=uft-8)

Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
  

###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

def Play(x,y):
    global Winner          
    Grille[x][y] = 1
    if(DetectWin(1)):
        Winner = 1
        print("Winner == 1 : ",Winner == 1)


def DetectWin(Player):
    return DetectHorizontalWin(Player) or DetectVerticalWin(Player) or DetectDiagonalWin(Player)

def DetectVerticalWin(Player):
    nbOfPlayerToken = 0
    for i in range(3):
        for j in range(3):
            if(Grille[i][j] == Player):
                nbOfPlayerToken += 1
        if(nbOfPlayerToken == 3):
            return True
        else:
            nbOfPlayerToken = 0
    return False

def DetectHorizontalWin(Player):
    nbOfPlayerToken = 0
    for i in range(3):
        for j in range(3):
            if(Grille[j][i] == Player):
                nbOfPlayerToken += 1
        if(nbOfPlayerToken == 3):
            return True
        else:
            nbOfPlayerToken = 0
    return False

def DetectDiagonalWin(Player):
    nbOfPlayerToken = 0
    for i in range(3):
        if(Grille[i][i] == Player):
            nbOfPlayerToken += 1
    if(nbOfPlayerToken == 3): 
        return True
    nbOfPlayerToken = 0
    for i in range(2,0,-1):
        if(Grille[i][i] == Player):
            nbOfPlayerToken +=1
    if(nbOfPlayerToken == 3): 
        return True
    
    return False        


################################################################################
#    
# Dessine la grille de jeu

def Dessine(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        print("Partie Gagnee : ",PartieGagnee)
        if(PartieGagnee):
            if(Winner == 1):
                DrawGrille("yellow")
                print("Drawing Yellow")
        else:        
            DrawGrille("blue")
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        
       
def DrawGrille(color):
    for i in range(4):
        canvas.create_line(i*100,0,i*100,300,fill=color, width="4" )
        canvas.create_line(0,i*100,300,i*100,fill=color, width="4" )

  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
   
    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
     
    
    print("clicked at", x,y)
    
    Play(x,y)  # gestion du joueur humain et de l'IA
    print("Winner == 1 : ",Winner == 1)
    Dessine(Winner == True)
    
canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()


  


    
        

      
 

