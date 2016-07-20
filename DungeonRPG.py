import random
import curses

#curses initialization. Permits to configure the "graphic" interface
def init_curses(lines, cols, pos):
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    window = curses.newwin(lines, cols, pos[0], pos[1])
    window.border(0)
    window.keypad(1)
    return window

#restore graphic parameters
def close_curses():
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()

#initialize coloration, return a list containing the colors
def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    return["RED", "GREEN", "BLUE"]

#color picker, return curses color code
def color(code, l_color):
    return curses.color_pair(l_color.index(code) + 1)


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
def score_bar(data, win, coloration):
    bar = "HP: {:2d}   GC: {:4d}  Level : {:3d}"
    win.addstr(23, 1, bar.format(data["hp"], data["gc"], data["level"]), color("BLUE", coloration))

#display in-labyrinth lines
def display_labyrinth(lab, char, char_position, treasure, win, coloration):
    n_line = 0
    for line in lab:
        for i in range(1, 4):
            line = line.replace(str(i), treasure)
        if n_line == char_position[1]:
            win.addstr(n_line +1, 10, line[0: char_position[0]] + char + line[char_position[0] + 1:])
            #coloring our character
            win.addstr(n_line + 1, 10 + char_position[0], char, color("RED", coloration))
        else:
            win.addstr(n_line + 1, 10, line)
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
    elif lab[pos_line][pos_col] == "O":
        #seems bravely victorious, damn GG son!
        return [-1, -1]
    elif lab[pos_line][pos_col] == "1" or lab[pos_line][pos_col] == "2":
        #discover a treasure
        treasure_discovery(lab[pos_line][pos_col], data)
        lab[pos_line] = lab[pos_line][:pos_col] + " " + lab[pos_line][pos_col + 1:]
        return[pos_col, pos_line]
    elif lab[pos_line][pos_col] == "$":
        #meets a naughty villain
        fight(data)
        lab[pos_line] = lab[pos_line][:pos_col] + " " + lab[pos_line][pos_col + 1:]
        return [pos_col, pos_line]
    elif lab[pos_line][pos_col] != " ":
        return None
    else:
        return[pos_col, pos_line]


#player's direction choice
def player_choice(lab, char_position, data, win):
    move = None
    choice = win.getch()
    if choice == curses.KEY_UP:
        move = direction_allowed(lab, char_position[0], char_position[1] - 1, data)
    elif choice == curses.KEY_DOWN:
        move = direction_allowed(lab, char_position[0], char_position[1] + 1, data)
    elif choice == curses.KEY_LEFT:
        move = direction_allowed(lab, char_position[0] - 1, char_position[1], data)
    elif choice == curses.KEY_RIGHT:
        move = direction_allowed(lab, char_position[0] + 1, char_position[1], data)
    elif choice == 27: #asci code for leave key
        close_curses()
        exit(0)
    if move != None:
        char_position[0] = move[0]
        char_position[1] = move[1]

#main game loop
def game(level, data, char, char_position, treasure, win, coloration):
    while True:
        display_labyrinth(level, char, char_position, treasure, win, coloration)
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
