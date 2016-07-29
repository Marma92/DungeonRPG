#!/usr/bin/python3
import DungeonRPG
from tkinter import *

if __name__ == "__main__":
    #character initialization:
    char            = "X"
    char_position   = [1, 1]
    treasure        = "#"
    n_levels_total  = 20
    data = {
        "gc"    :   0,
        "hp"    :   25,
        "level" :   1
    }

    size_sprite = 31

    #graphic environment initialization
    window = Tk()
    window.title("DungeonRPG Game")

    #game launch
    level = DungeonRPG.load_labyrinth("level_1")
    (canvas, sprite_hero, photos) = DungeonRPG.display_labyrinth(level, window, size_sprite, char_position)
    DungeonRPG.init_keys(window, canvas, level, char_position, sprite_hero)

    #events loop
    window.mainloop()
