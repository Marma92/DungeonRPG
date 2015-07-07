

#display in-labyrinth lines
def display_labyrinth(lab, character, char_position):
    line = 0
    for line in lab:
        if n_line == character_position:
            print(line[0:char_position[0]] + character + line[char_position[0] + 1:])
        else:
            print(line)
        n_line +=1
        
#will return if a deplacement is allowed or not
def direction_allowed(lab, pos_col, pos_line):
    #compute labyrinth size:
    n_cols  = len(lab[0])
    n_lines = len(lab)
    #simply check if the choosen direction won't conduct character out 
    if pos_line < 0 or pos_col < 0 or pos_line > (n_lines - 1) or pos_col > n_cols -1:
        return None
    elif lab[pos_line][pos_col] != " ":
        return None
    else:
        return[pos_col, pos_line]
            
#all in the title
def display_labyrinth_borders(size):
    print("+{}+".format("-" * (size - 2)))
    for i in range(size-2):
        print("|{}|".format(" " * (size - 2)))
    print("+{}+".format("-" * (size - 2)))

#player's direction choice
def player_choice(lab, char_position):
    choice = input ("Votre déplacement (Haut/Bas/Droite/Gauche/Quitter) ? ")
    if choice == "H" or choice == "Haut" or choice == "haut":
        move = direction_allowed(lab, char_position[0], char_position[1] -1)
    elif choice == "B" or choice == "Bas" or choice == "bas":
        move = direction_allowed(lab, char_position[0], char_position[1] +1)
    elif choice == "D" or choice == "Droite" or choice == "droite":
        move = direction_allowed(lab, char_position[0] + 1, char_position[1])
    elif choice == "G" or choice == "Gauche" or choice == "gauche":
        move = direction_allowed(lab, char_position[0] - 1, char_position[1])
    elif choice == "Q" or choice == "Quitter" or choice == "quitter":
        exit(0)
    if move == None:
        print("Deplacement impossible")
    else:
        char_position[0] = move[0]
        char_position[1] = move[1]
        
        
display_labyrinth_borders(20)
#move = player_choice()
#print(move)
