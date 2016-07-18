

import DungeonRPG

if __name__ == "__main__":
    #character initialization:
    char            = "X"
    char_position   = [1, 1]
    treasure        = "#"
    n_levels_total  = 20
    data = {
        "gc"    :   0,
        "hp"    :   25,
        "level" :   None
    }

    #game launch
    for n_level in range(1, n_levels_total + 1):
        level = DungeonRPG.load_labyrinth("level_" + str(n_level))
        data["level"] = n_level
        DungeonRPG.game(level, data, char, char_position, treasure)
    print("YOU WIN !!!")
