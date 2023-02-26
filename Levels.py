import random

import pygame

from houses import finish_house1, finish_house2, finish_house_small1

levels = []


def change_map(block, current_level):
    map_no = block["map"]
    current_map_no = current_level["map_no"]
    player = current_level["player"]
    background_layer, main_layer, top_layer = load_level(levels[map_no])
    # Find block to get us back and place player on that block. Also
    # remove all blocks player is currently over with that block
    for block in main_layer:
        if block["type"] == "load-map" and block["map"] == current_map_no:
            player["over_tiles"] = [block]
            player_rect = player["rect"]
            player_rect.x = block["rect"].x
            player_rect.y = block["rect"].y
            current_level["map_no"] = map_no
            current_level["background_layer"] = background_layer
            current_level["main_layer"] = main_layer
            current_level["top_layer"] = top_layer


def load_level(level):

    level_width = 0
    background_layer = []
    main_layer = []
    top_layer = []
    level["background_layer"] = background_layer
    level["main_layer"] = main_layer
    level["top_layer"] = top_layer

    translations = default_translation.copy()
    translations |= level["map_translations"]

    x = y = 0
    for row in level["map"]:
        level_width = max(level_width, len(row))
        for col in row:
            if col not in translations:
                print("*** cannot find translation for '" + col + "' for level " + (level["name"] if "name" in level else "unknown"))
            else:
                translations[col](level, x, y, col)

            x = x + 16
        y = y + 16
        x = 0

        # Fix for house - add correct images to blockers
        for i, block in enumerate(main_layer):
            if "finish_init" in block:
                block["finish_init"](block, level)

    return background_layer, main_layer, top_layer


def create_block(x, y, block_type, can_move, img_tile):
    block = {
        "rect": pygame.Rect(x, y, 16, 16),
        "type": block_type,
        "can_move": can_move,
        "x": x,
        "y": y
    }
    if img_tile is not None:
        block["img_tile"] = img_tile
    return block


def create_forest(layer_definition, x, y, char):
    def finish_forest(block, layer_definition):
        top_layer = layer_definition["top_layer"]
        if block["rect"].y == 0 and block["rect"].x == 0:
            top_layer.append(create_block(16, 16, "forest", True, 32))
        elif block["rect"].y == 10 * 16 and block["rect"].x == 0:
            top_layer.append(create_block(16, block["rect"].y - 16, "forest", True, 8))
        elif block["rect"].y == 10 * 16 and block["rect"].x == 19 * 16:
            top_layer.append(create_block(block["rect"].x - 16, block["rect"].y - 16, "forest", True, 6))
        elif block["rect"].y == 0 and block["rect"].x == 19 * 16:
            top_layer.append(create_block(block["rect"].x - 16, 16, "forest", True, 30))
        elif block["rect"].y == 0:
            top_layer.append(create_block(block["rect"].x - 16, 16, "forest", True, 31))
        elif block["rect"].y == 10 * 16:
            top_layer.append(create_block(block["rect"].x, block["rect"].y - 16, "forest", True, 7))
        elif block["rect"].x == 0:
            top_layer.append(create_block(16, block["rect"].y, "forest", True, 20))
        elif block["rect"].x == 19 * 16:
            top_layer.append(create_block(block["rect"].x - 16, block["rect"].y, "forest", True, 18))

    block = create_block(x, y, "forest", False, 19)
    layer_definition["main_layer"].append(block)
    block["finish_init"] = finish_forest


def create_blocker(layer_definition, x, y, char):
    layer_definition["main_layer"].append(create_block(x, y, "blocker", False, None))


def create_house1(layer_definition, x, y, char):
    block = create_block(x, y, "house", False, 85)
    block["finish_init"] = finish_house1
    layer_definition["main_layer"].append(block)


def create_house2(layer_definition, x, y, char):
    block = create_block(x, y, "house", False, 89)
    block["finish_init"] = finish_house2
    layer_definition["main_layer"].append(block)


def create_house_small1(layer_definition, x, y, char):
    block = create_block(x, y, "house", False, 89)
    block["finish_init"] = finish_house_small1
    layer_definition["main_layer"].append(block)


def create_path(layer_definition, x, y, char):
    layer_definition["background_layer"].append(create_block(x, y, "path", True, 43))
    layer_definition["main_layer"].append(create_block(x, y, "empty", True, None))


def create_portal(layer_definition, x, y, char):
    block = create_block(x, y, "load-map", True, None)
    block["map"] = int(char)
    block["on_enter_tile"] = change_map
    layer_definition["main_layer"].append(block)


def create_background(layer_definition, x, y, char):
    r = random.random()
    if r < 0.7:
        img_tile = 0
    elif r < 0.9:
        img_tile = 1
    else:
        img_tile = 2

    layer_definition["background_layer"].append(create_block(x, y, "grass", True, img_tile))
    layer_definition["main_layer"].append(create_block(x, y, "empty", True, None))


default_translation = {
    "#": create_forest,
    "+": create_path,
    "X": create_blocker,
    "0": create_portal,
    "1": create_portal,
    "2": create_portal,
    "3": create_portal,
    "4": create_portal,
    "5": create_portal,
    "6": create_portal,
    "7": create_portal,
    "8": create_portal,
    "9": create_portal,
    " ": create_background
}


levels.append({
    "map": [
        "####################",
        "#                  #",
        "#   ++++++++ XXXX  #",
        "#   +      + XXXX  #",
        "1++++      + XXGX  #",
        "#   + XXXX +   +   #",
        "#   + XXXX +++++   #",
        "#   + XXHX     +   #",
        "#   ++++++++++++   #",
        "#                  #",
        "####################"
    ],
    "map_translations": {
        "H": create_house1,
        "G": create_house2,
    }
})

levels.append({
    "map": [
        "####################",
        "#                  #",
        "#            XXXX  #",
        "#            XXXX  #",
        "#+++++++++++ XXHX  #",
        "#          ++++++++0",
        "#          +       #",
        "#          +  XXX  #",
        "#          +  XhX  #",
        "#          +++++   #",
        "####################"
    ],
    "map_translations": {
        "H": create_house2,
        "h": create_house_small1,
    }
})
