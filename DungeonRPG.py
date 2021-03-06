import random
from tkinter import *

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
def score_bar(data, can, n_lines, size_sprite):
    bar = "HP: {:2d}   GC: {:4d}  Level : {:3d}"
    id  = can.create_text( 4*size_sprite, n_lines+1*size_sprite , text= bar.format(data["hp"], data["gc"], data["level"]))
    data ["id_bar"] = id

def score_bar_update(data, can):
    bar = "HP: {:2d}   GC: {:4d}  Level : {:3d}"
    can.itemconfigure(data["id_bar"], text = bar.format(data["hp"], data["gc"], data["level"]))

#display in-labyrinth lines
def display_labyrinth(lab, window, size_sprite, char_position, data):
    can = Canvas(window, width = 900, height = 680)

    photo_wall      = PhotoImage(file = "sprites/wall.png")
    photo_treasure  = PhotoImage(file = "sprites/chest.gif")
    photo_enemy     = PhotoImage(file = "sprites/enemy.png")
    photo_exit      = PhotoImage(file = "sprites/exit.png")
    photo_hero      = PhotoImage(file = "sprites/hero.gif")

    n_line = 0
    for line in lab:
        n_col = 0
        for car in line:
            #Walls
            if car == "+" or car == "-" or car == "|":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line *size_sprite, anchor = NW, image = photo_wall)
            #treasures
            if car == "1" or car == "2":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line *size_sprite, anchor = NW, image = photo_treasure)
            #fees
            if car == "$":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line *size_sprite, anchor = NW, image = photo_enemy)
            #exit
            if car == "O":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line *size_sprite, anchor = NW, image = photo_exit)

            n_col += 1
        n_line += 1

    #hero's displaying
    sprite_hero = can.create_image(char_position[0] + char_position[0] * size_sprite, char_position[1] + char_position[1] * size_sprite, anchor = NW, image = photo_hero)

    #bar displaying
    score_bar(data, can, len(lab), size_sprite)

    can.pack()
    return (can, sprite_hero, {
    "hero"      : photo_hero,
    "wall"      : photo_wall,
    "treasure"  : photo_treasure,
    "enemy"     : photo_enemy,
    "exit"      : photo_exit })


#keys behavior
def init_keys(window, canvas, lab, char_position, character, data):
    window.bind("<Right>", lambda event, can = canvas, l = lab, pos = char_position, char = character: move(event, can, "right", l, pos, char, data))
    window.bind("<Left>", lambda event, can = canvas, l = lab, pos = char_position, char = character: move(event, can, "left", l, pos, char, data))
    window.bind("<Up>", lambda event, can = canvas, l = lab, pos = char_position, char = character: move(event, can, "up", l, pos, char, data))
    window.bind("<Down>", lambda event, can = canvas, l = lab, pos = char_position, char = character: move(event, can, "down", l, pos, char, data))

    window.bind("<Escape>", lambda event, win = window : destroy(event, win))

#deplacement function
def move(event, can, dep, lab, char_position, character, data):
    #computering lab size
    n_cols   = len(lab[0])
    n_lines  = len(lab)
    pos_col, pos_line,  = [char_position[0], char_position[1]]

    #deplacement
    if dep == "right":
        pos_col += 1
    elif dep == "left":
        pos_col -= 1
    elif dep == "up":
        pos_line -= 1
    elif dep == "down":
        pos_line += 1

    #valid position test
    if pos_line < 0 or pos_col < 0 or pos_line > (n_lines - 1) or pos_col > (n_cols - 1):
        return None

    #if the move is valid, let make it available through the char_position list
    if lab[pos_line][pos_col] == " ":
        can.coords(character, pos_col + pos_col * 31, pos_line + pos_line * 31)
        del char_position[0]
        del char_position[0]
        char_position.append(pos_col)
        char_position.append(pos_line)
    if lab[pos_line][pos_col] == "1" or lab[pos_line][pos_col] == "2":
        treasure_discovery(lab[pos_line][pos_col], data, can)
        del char_position[0]
        del char_position[0]
        char_position.append(pos_col)
        char_position.append(pos_line)
    elif lab[pos_line][pos_col] == "$":
        fight(data, can)
        del char_position[0]
        del char_position[0]
        char_position.append(pos_col)
        char_position.append(pos_line)
    if lab[pos_line][pos_col] == "O":
        win(can, data)

#closing graphic window
def destroy(event, window):
    window.destroy()

#If our character meets a treasure
def treasure_discovery(category, data, can):
    #first shot of treasures:
    #two kinds of them:
    #- 1: between 1 and 20 golds
    #- 2: between 5 and 30 golds
    if category == "1":
        data["gc"] = data["gc"]+ random.randint(1, 20)
    else :
        data["gc"] = data["gc"]+ random.randint(5, 30)
    score_bar_update(data, can)


#If our character meets a monster
def fight(data, can):
    de = random.randint(1, 10)
    if de == 1:
        data["hp"] = data["hp"]-random.randint(5,10)
    elif de >= 2:
        data["hp"] = data["hp"]-random.randint(1,5)
    score_bar_update(data, can)

#the win
def win(can, data):
    can.itemconfigure(data["id_bar"], text = "YOU WON !!")


#main game loop, useless atm
"""def game(level, data, char_position, window):
    while True:
        display_labyrinth(lab, window, size_sprite, char_position)
        score_bar(data, win, coloration)
        if data["hp"] <= 0:
            win.addstr(22, 1, "YOU DIED !", color("RED", coloration))
            win.getch()
            colse_curses()
            exit(0)
        player_choice(level, char_position, data, win)
        if char_position == [-1, -1]:
            win.addstr(22, 1, "You passed this level! ", color("RED", coloration))
            win.addstr(23, 1, "Press a key to continue", color("RED", coloration))
            win.getch()
            win.addstr(1, 20, " ", *50)
            win.addstr(1, 21, " ", *50)
            break
"""
