

#display in-labyrinth lines
def display_labyrinth(lab):
    for line in lab:
        print(line)
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
