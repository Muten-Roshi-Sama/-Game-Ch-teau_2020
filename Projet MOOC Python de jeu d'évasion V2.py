"""
Author : F. Vassily (pseudo MOOC : Polyphia)
Date : 15.11.2020

Goal :
This is a simple code that creates an interactive maze/Escape type of Game.
You, the player, moves with the arrow keys, and need to find the exit by collecting clues, which have been
scattered all over the Maze. Using the clues, you will need to answer questions to open up doors on your way.
Good luck !
Input : The four arrows to move around the Maze and all answers to questions typed from a keyboard.
Output : The Interactive Maze itself.


INFO :
The .txt containing the plan : 'plan_chateau.txt'
    value 0 for an empty box,
    value 1 for a wall,
    value 2 for the exit,
    value 3 for a door which will open after answering a question,
    value 4 for a box containing an object to collect, becomes an empty case after.

The game space is (x, y) ; 19x27

The .txt containing the clues : 'dico_objets'
    (x, y), "clue"
    exemple : (12, 3), "un oreiller magique"

The .txt containing the Questions/Answers : 'dico_portes'
    (x, y), ("question", "réponse")
    exemple : (21, 12), ("Capitale de la Belgique ?", "Bruxelles")
"""
# IMPORTS
import turtle as tt
from CONFIGS import *

# CONSTANT VARIABLES
global Hauteur, Largeur  # for readability in next levels.
Hauteur = (abs(ZONE_PLAN_MINI[1]) + abs(ZONE_PLAN_MAXI[1]))
Largeur = (abs(ZONE_PLAN_MINI[0]) + abs(ZONE_PLAN_MAXI[0]))
WRITING_COLOR = 'Black'  # color of turtle when writing something.
PlayerItemList = []
position = POSITION_DEPART
dic_mouv = {'up': (-1, 0), 'down': (1, 0),
            "left": (0, -1), 'right': (0, 1)}
# ----------------------------------------------------LEVEL_1------------------------------------------------------------------------#
"""The first level of the program consist of the creation of the matrix M containing the plan, and the graphic 
representation of it using the Turtle Module. 
"""


def lire_matrice(fichier):
    """Reads the text file and converts it into a matrix."""
    contents = open(fichier).read()
    matrice = [[int(string) for string in elem.split()] for elem in contents.split('\n')[:]]
    print(matrice)
    return matrice


def calculer_pas(matrice):
    """calcule la dimension à donner aux cases"""
    Hauteur_case = Hauteur // len(matrice[0])
    Largeur_case = Largeur // len(matrice)
    return min(Hauteur_case, Largeur_case) + 5  # adjust to screen.


def coordonnees(case, pas):
    """ Calculate the coordinates (left lower part of each box). """
    x, y = case
    bcoord_x = ZONE_PLAN_MINI[0] + y * pas
    bcoord_y = ZONE_PLAN_MAXI[1] - x * pas
    return bcoord_x, bcoord_y


def tracer_carre(dimension):
    """(square : move forward, turn right) *4"""
    tt.pencolor(COULEUR_CASES)  # making the pencolor white
    tt.pendown()  # putting the pen down to start working
    for i in range(4):
        tt.fd(dimension)
        tt.rt(90)


def tracer_case(case, couleur, pas):
    """ Call tracer_carre to draw a square from a certain size, color, position. """
    tt.pu()
    tt.goto(coordonnees(case, pas))
    tt.pd()
    tt.fillcolor(couleur)
    tt.begin_fill()
    tracer_carre(pas)
    tt.end_fill()


def afficher_plan(matrice):
    """ Draws the whole Maze. """
    for x in range(len(matrice)):
        tt.pu()
        for y in range(len(matrice[0])):
            tracer_case((x, y), COULEURS[int(matrice[x][y])], pas)
    tt.pu()
    x, y = coordonnees(POSITION_DEPART, pas)  # Starting box-coordinates of the player.
    MIDDLE = (x + pas // 2, y - pas // 2)  # Centered starting point of the player.
    tt.goto(MIDDLE)
    tt.pd()
    tt.dot(pas * RATIO_PERSONNAGE, COULEUR_PERSONNAGE)


# ----------------------------------------------------LEVEL_2------------------------------------------------------------------------#
""" The second level consist of the code containing the movements of the player.
"""


def deplacer(matrice, position, mouvement, dict_objets, dict_portes):
    """ Function to move the player up, down, left or right in the matrix """
    x, y = position
    new_pos = x + mouvement[0], y + mouvement[1]
    MIN = 0
    MAX_Y = len(matrice[0])
    MAX_X = len(matrice)
    if MIN <= new_pos[0] < MAX_X and MIN <= new_pos[1] < MAX_Y:  # checks if player goes off-limits.
        if matrice[new_pos[0]][new_pos[1]] != 1 and matrice[new_pos[0]][new_pos[1]] != 3:
            # checks for walls and closed-doors.
            position = new_pos
            if (new_pos[0], new_pos[1]) in dict_objets:  # Check if the next box contains a clue.
                ramasser_objet(dict_objets, PlayerItemList, (new_pos[0], new_pos[1]))

        elif (new_pos[0], new_pos[1]) in dict_portes and matrice[new_pos[0]][new_pos[1]] == 3:  # Check for doors.
            temp = poser_question(matrice, (new_pos[0], new_pos[1]), mouvement, dict_portes)
            if temp:
                position = new_pos

        if matrice[new_pos[0]][new_pos[1]] == 2:  # Exit of the Maze.
            if len(PlayerItemList) == len(dict_objets):   # if the Player got all clues.
                writeBanner('Hooray ! You won.')
                mandala()
                tt.exitonclick()
            else:
                writeBanner("You need to find all clues to escape.")

    # print('Position : ', position)  # Prints the position to keep track of your advancement.
    return position


def deplacer_haut():
    """ Player going up """
    global matrice, position, pas, dic_mouv  # AS GIVEN
    temp = deplacer(matrice, position, dic_mouv['up'], dict_objets, dict_portes)
    tt.onkeypress(None, "Up")  # AS GIVEN
    if temp != position:  # if equal, the move sends the player somewhere it shouldn't, so do nothing.
        tracer_case(position, COULEUR_VUE, pas)  # Show where the player already went (=map).
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)  # Make sure the player is centered.
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    tt.onkeypress(deplacer_haut, "Up")  # AS GIVEN


def deplacer_bas():
    """ Player going down """
    global matrice, position, pas, dic_mouv, dict_portes
    temp = deplacer(matrice, position, dic_mouv['down'], dict_objets, dict_portes)
    tt.onkeypress(None, "Down")
    if temp != position:
        tracer_case(position, COULEUR_VUE, pas)
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)

    tt.onkeypress(deplacer_bas, "Down")


def deplacer_gauche():
    """ Player going left """
    global matrice, position, pas, dic_mouv, dict_portes
    temp = deplacer(matrice, position, dic_mouv['left'], dict_objets, dict_portes)
    tt.onkeypress(None, "Left")
    if temp != position:
        tracer_case(position, COULEUR_VUE, pas)
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    tt.onkeypress(deplacer_gauche, "Left")


def deplacer_droite():
    """ Player going right """
    global matrice, position, pas, dic_mouv, dict_portes
    temp = deplacer(matrice, position, dic_mouv['right'], dict_objets, dict_portes)
    tt.onkeypress(None, "Right")
    if temp != position:
        tracer_case(position, COULEUR_VUE, pas)
        position = temp
        tt.penup()
        x, y = coordonnees(position, pas)
        MIDDLE = (x + pas // 2, y - pas // 2)
        tt.goto(MIDDLE)
        tt.pendown()
        tt.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    tt.onkeypress(deplacer_droite, "Right")


# ----------------------------------------------------LEVEL_3------------------------------------------------------------------------#
""" This third level is to manage the clues (objects) scattered around the maze and the display 
when you pick them up.
"""


def creer_dictionnaire_des_objets(file_2):
    """Reads the text file and converts it into a dictionary."""
    Dict = {}
    with open(file_2, encoding="UTF-8") as f:
        for line in f:
            line = line.split(",")
            line[:2] = [eval(','.join(line[:2]))]
            line[1:] = [eval(','.join(line[1:]))]
            Dict[line[0]] = line[1]
    return Dict


def ramasser_objet(dict_objets, PlayerItemList, position):
    """ Delete the clue from the matrix and add it in the menu and PlayerItemList. """
    x, y = position
    if dict_objets[position] not in PlayerItemList:
        PlayerItemList.append(dict_objets[position])
        writeBanner("You found : " + dict_objets[position])
        writeInventory(PlayerItemList)
    matrice[x][y] = 0


def writeInventory(PlayerItemList):
    """ Write the inventory of the Player, based on CONFIGS position."""
    tt.pu()
    x, y = POINT_AFFICHAGE_INVENTAIRE
    tt.goto(x, y)
    tt.pd()
    eraseText(heading=270, color=COULEUR_CASES, rotation=(-90), height=30, width=30)
    # eraseText : seth to 270 to start by turtle going down.
    # width and height based on CONFIGS ZONE to adjust to the window.
    for i in range(len(PlayerItemList)):
        if i == 0:
            tt.pu()
            tt.goto(x, y - (i + 2) * pas)  # First part of the loop to write Inventory : ...
            tt.pd()
            tt.write("Inventory : ", move=False, align='left', font=('Arial', 10, 'normal'))
        tt.pu()
        tt.goto(x + pas, y - (i + 3) * pas)  # Aesthetically : to "indent" items within Inventory.
        tt.pd()
        tt.write(PlayerItemList[i], move=False, align='left', font=('Arial', 8, 'normal'))


def writeBanner(message):
    """ Write at the top of the screen information about the player's most recent actions. """
    tt.pu()
    x, y = POINT_AFFICHAGE_ANNONCES
    x, y = x - 10, y - 30  # to recenter the text.
    tt.goto(x, y)
    tt.pendown()
    eraseText(heading=90, color=COULEUR_CASES, rotation=90, height=30, width=480)
    # eraseText : seth to 90 to start by turtle going up.
    # width and height based on CONFIGS ZONE to adjust to the window.
    tt.pu()
    tt.goto(x + pas, y + pas)
    tt.pd()
    tt.write(message, move=False, align='left', font=('Arial', 8, 'normal'))


def eraseText(heading, color, rotation, height, width):
    """ Creates a blank frame to 'erase' text by hiding it. """
    tt.seth(heading)
    tt.color(color)
    tt.begin_fill()
    for i in range(4):  # To make a rectangle.
        if i % 2 == 0:
            tt.fd(pas * width)
            tt.rt(rotation)
        else:
            tt.fd(pas * height)
            tt.rt(rotation)
    tt.end_fill()
    tt.color(WRITING_COLOR)
    tt.seth(0)  # Make sure turtle faces the right direction.


# ----------------------------------------------------LEVEL_4------------------------------------------------------------------------#
""" The fourth level is to manage doors and to generate a pop-up window when the player needs to answer an question
 in order to get trough the door. 

"""


def poser_question(matrice, case, mouvement, dict_portes):
    """ When trying to get trough a door, announce it, ask a question, if answered right, opens the door and announce
    it, else announce it. """
    res = False
    answer = tt.textinput("Question", dict_portes[case][0])
    if answer == dict_portes[case][1]:
        matrice[case[0]][case[1]] = 0
        res = True
        writeBanner("Correct, the door opens..")
        dict_portes.pop(case)
        print(dict_portes)
    else:
        writeBanner("The door remains closed.")
    tt.listen()  # Because tt.textinput() interrupts tt.listen()

    return res


# ----------------------------------------------------BONUS------------------------------------------------------------------------#
""" This personalized bonus contains the code of the end-game animation.
"""
colors = [
        # red shades
        (1.00, 0.00, 0.00), (1.00, 0.03, 0.00), (1.00, 0.05, 0.00), (1.00, 0.07, 0.00), (1.00, 0.10, 0.00),
        (1.00, 0.12, 0.00), (1.00, 0.15, 0.00), (1.00, 0.17, 0.00), (1.00, 0.20, 0.00), (1.00, 0.23, 0.00),
        (1.00, 0.25, 0.00), (1.00, 0.28, 0.00), (1.00, 0.30, 0.00), (1.00, 0.33, 0.00), (1.00, 0.35, 0.00),
        (1.00, 0.38, 0.00), (1.00, 0.40, 0.00), (1.00, 0.42, 0.00), (1.00, 0.45, 0.00), (1.00, 0.47, 0.00),
        # orange shades
        (1.00, 0.50, 0.00), (1.00, 0.53, 0.00), (1.00, 0.55, 0.00), (1.00, 0.57, 0.00), (1.00, 0.60, 0.00),
        (1.00, 0.62, 0.00), (1.00, 0.65, 0.00), (1.00, 0.68, 0.00), (1.00, 0.70, 0.00), (1.00, 0.72, 0.00),
        (1.00, 0.75, 0.00), (1.00, 0.78, 0.00), (1.00, 0.80, 0.00), (1.00, 0.82, 0.00), (1.00, 0.85, 0.00),
        (1.00, 0.88, 0.00), (1.00, 0.90, 0.00), (1.00, 0.93, 0.00), (1.00, 0.95, 0.00), (1.00, 0.97, 0.00),
        # yellow shades
        (1.00, 1.00, 0.00), (0.95, 1.00, 0.00), (0.90, 1.00, 0.00), (0.85, 1.00, 0.00), (0.80, 1.00, 0.00),
        (0.75, 1.00, 0.00), (0.70, 1.00, 0.00), (0.65, 1.00, 0.00), (0.60, 1.00, 0.00), (0.55, 1.00, 0.00),
        (0.50, 1.00, 0.00), (0.45, 1.00, 0.00), (0.40, 1.00, 0.00), (0.35, 1.00, 0.00), (0.30, 1.00, 0.00),
        (0.25, 1.00, 0.00), (0.20, 1.00, 0.00), (0.15, 1.00, 0.00), (0.10, 1.00, 0.00), (0.05, 1.00, 0.00),
        # green shades
        (0.00, 1.00, 0.00), (0.00, 0.95, 0.05), (0.00, 0.90, 0.10), (0.00, 0.85, 0.15), (0.00, 0.80, 0.20),
        (0.00, 0.75, 0.25), (0.00, 0.70, 0.30), (0.00, 0.65, 0.35), (0.00, 0.60, 0.40), (0.00, 0.55, 0.45),
        (0.00, 0.50, 0.50), (0.00, 0.45, 0.55), (0.00, 0.40, 0.60), (0.00, 0.35, 0.65), (0.00, 0.30, 0.70),
        (0.00, 0.25, 0.75), (0.00, 0.20, 0.80), (0.00, 0.15, 0.85), (0.00, 0.10, 0.90), (0.00, 0.05, 0.95),
        # blue shades
        (0.00, 0.00, 1.00), (0.05, 0.00, 1.00), (0.10, 0.00, 1.00), (0.15, 0.00, 1.00), (0.20, 0.00, 1.00),
        (0.25, 0.00, 1.00), (0.30, 0.00, 1.00), (0.35, 0.00, 1.00), (0.40, 0.00, 1.00), (0.45, 0.00, 1.00),
        (0.50, 0.00, 1.00), (0.55, 0.00, 1.00), (0.60, 0.00, 1.00), (0.65, 0.00, 1.00), (0.70, 0.00, 1.00),
        (0.75, 0.00, 1.00), (0.80, 0.00, 1.00), (0.85, 0.00, 1.00), (0.90, 0.00, 1.00), (0.95, 0.00, 1.00)
    ]

def mandala():
    """ Repeats a shape x-times in a row with around 1 degree rotation using shades of color as to create a mandala."""
    tt.clear()  # Clear the window.
    tt.goto(0, 0)
    tt.hideturtle()
    tt.tracer(5, None)  # Speed of animation.
    tt.bgcolor('Black')
    c = 0
    x = 0
    while x < 800:  # number of shapes to draw.
        idx = int(c) - 50  # Starting color.
        color = colors[idx]
        tt.color(color)
        tt.forward(x)
        tt.right(89)
        x += 1
        c += 0.1
    # Text Message
    tt.pu()
    tt.goto(-250, 200)
    tt.pd()
    eraseText(90, "black", 90, 500, 40)
    tt.pu()
    tt.goto(0, 215)
    tt.pd()
    tt.color("White")
    tt.write("Congratulations ! You bested the Maze. ", move=False, align='center', font=('Arial', 12, 'normal'))


# ----------------------------------------------------MAIN------------------------------------------------------------------------#

if __name__ == "__main__":
    # Main code
    wn = tt.Screen()
    wn.setup(480, 480)  # AS GIVEN
    wn.title("Maze")
    tt.tracer(0)
    tt.hideturtle()
    # ----------------------------------

    matrice = lire_matrice(fichier_plan)  # Matrix containing the Maze plan
    print(matrice)
    pas = calculer_pas(matrice)
    afficher_plan(matrice)  # Draws the whole Maze.
    # window.update()   #only if tt.tracer(0) is not activated.
    # ------------------------------------------------------------
    dict_objets = creer_dictionnaire_des_objets(fichier_objets)
    dict_portes = creer_dictionnaire_des_objets(fichier_questions)
    # ------------------------------------------------------------
    tt.listen()
    tt.onkeypress(deplacer_haut, 'w')
    tt.onkeypress(deplacer_bas, 's')
    tt.onkeypress(deplacer_gauche, 'a')
    tt.onkeypress(deplacer_droite, 'd')
    # ---------------------------------
    tt.mainloop()
    # ---------------------------------
mandala()