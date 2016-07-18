import sys
import os
import random

#Load labyrinth file
def load_labyrinth(filename):
    try:
        file = open(filename + ".txt", "r")
        data = file.readlines()
        file.close()
    except IOError:
        print(" File reading error.")
        exit(1)

    for i in range(len(data)):
        data[i] = data[i].strip()
    return data

#Score bar displaying
def score_bar(data):
    print("HP: (:2d)   GC: (:4d)  Level : (:3d)".format(data["hp"], data["gc"], data["level"]))

#display in-labyrinth lines
def display_labyrinth(lab, char, char_position, treasure):
    n_line = 0
    for line in lab:
        for i in range(1, 4):
            line = line.replace(str(i), treasure)
        if n_line == char_position[1]:
            print(line[0:char_position[0]] + char + line[char_position[0] + 1:])
        else:
            print(line)
        n_line += 1

#clear console screen
def clear_screen():
    if sys.platform.startswith("win"):
        #if windows
        os.system("cls")
    else :
        #if unix based:
        os.system("clear")

#If our character meets a treasure
def treasure_discovery(category, data):
    #first shot of treasures:
    #two kinds of them:
    #- 1: between 1 and 20 golds
    #- 2: between 5 and 30 golds
    if category == "1":
        data["gc"] = data["gc"]+ random.randint(1, 20)
    else :
        data["gc"] = data["gc"]+ random.randint(5, 30)


#If our character meets a monster
def fight(data):
    de = random.randint(1, 10)
    if de == 1:
        data["hp"] = data["hp"]-random.randint(5,10)
    elif de >= 2:
        data["hp"] = data["hp"]-random.randint(1,5)


#will return if a deplacement is allowed or not
def direction_allowed(lab, pos_col, pos_line, data):
    #compute labyrinth size:
    n_cols  = len(lab[0])
    n_lines = len(lab)
    #simply check if the choosen direction won't conduct character out
    if pos_line < 0 or pos_col < 0 or pos_line > (n_lines - 1) or pos_col > (n_cols -1):
        return None
    elif [pos_line][pos_col] == "O":
        #seems bravely victorious, damn GG son!
        return[-1, -1]
    elif lab[pos_line][pos_col] == "1" or lab[pos_line][pos_col] == "2":
        #discover a treasure
        treasure_discovery(lab[pos_line][pos_col], data)
        lab[pos_line] = lab[pos_line][:pos_col] + " " + lab[pos_line][pos_col + 1:]
        return[pos_col, pos_line]
    elif [pos_line][pos_col] == "$":
        #meets a naughty villain
        fight(data)
        lab[pos_line] = lab[pos_line][:pos_col] + " " + lab[pos_line][pos_col + 1:]
        return [pos_col, pos_line]
    elif lab[pos_line][pos_col] != " ":
        return None
    else:
        return[pos_col, pos_line]


#player's direction choice
def player_choice(lab, char_position, data):
    move = None
    choice = input ("Votre déplacement (Haut/Bas/Droite/Gauche/Quitter) ? ")
    if choice == "H" or choice == "h" or choice == "Haut" or choice == "haut":
        move = direction_allowed(lab, char_position[0], char_position[1] -1, data)
    elif choice == "B" or choice == "b" or choice == "Bas" or choice == "bas":
        move = direction_allowed(lab, char_position[0], char_position[1] +1, data)
    elif choice == "D" or choice == "d" or choice == "Droite" or choice == "droite":
        move = direction_allowed(lab, char_position[0] + 1, char_position[1], data)
    elif choice == "G" or choice == "g" or choice == "Gauche" or choice == "gauche":
        move = direction_allowed(lab, char_position[0] - 1, char_position[1], data)
    elif choice == "Q" or choice == "q" or choice == "Quitter" or choice == "quitter":
        exit(0)
    else :
        print ("Choix invalide !")
    if move == None:
        print("Deplacement impossible")
        input("Appuyez sur entrée pour continuer")
    else:
        char_position[0] = move[0]
        char_position[1] = move[1]


#main game loop
def game(level, data, char, char_position, treasure):
    while True:
        clear_screen()
        display_labyrinth(level, char, char_position, treasure)
        score_bar(data)
        if data["hp"] <= 0:
            print("YOU LOSE...")
            exit(0)
        player_choice(level, char_position, data)
        if char_position == [-1, -1]:
            print("You passed this level")
            input("press enter <Return> to continue")
            break
