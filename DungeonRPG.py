

#display in-labyrinth lines
def display_labyrinth(lab, character, character_position):
    line = 0
    for line in lab:
        if n_line == character_position:
            print(line[0:character_position[0]] + character + line[character_position[0] + 1:])
        else:
            print(line)
        n_line +=1
        
#will return if a deplacement is allowed or not
def direction_allowed(lab, pos_col, pos_line):
    #compute labyrinth size:
    n_cols  = len(lab[0])
    n_lines = len(lab)
    #simply check if the choosen direction won't conduct character out 
    if pos_line < 0 or pos_col < 0 or pos_line > (n_lines - 1) or pos_col > n_cols -1):
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
def player_choice():
    return input ("Votre déplacement (Haut/Bas/Droite/Gauche) ? ")


display_labyrinth_borders(20)
dep = player_choice()
print(dep)
