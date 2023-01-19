import pygame
import random
import Levels
import Utils

pygame.init()


def load_level(level, img_tiles):
    def create_block(x, y, block_type, can_move, img_tile):
        block = {
            "rect": pygame.Rect(x, y, 16, 16),
            "type": block_type,
            "can_move": can_move,
        }
        if img_tile is not None:
            block["img_tile"] = img_tiles[img_tile]
        return block

    level_width = 0
    background_layer = []
    main_layer = []
    top_layer = []

    x = y = 0
    for row in level:
        level_width = max(level_width, len(row))
        for col in row:
            if col == "#":
                # background_layer.append(block)
                main_layer.append(create_block(x, y, "forest", False, 19))
            elif col == "H":
                main_layer.append(create_block(x, y, "house", False, 85))
            elif col == "X":
                main_layer.append(create_block(x, y, "blocker", False, None))
            elif col == "+":
                background_layer.append(create_block(x, y, "path", True, 43))
                main_layer.append(create_block(x, y, "empty", True, None))
            else:
                r = random.random()
                if r < 0.7:
                    img_tile = 0
                elif r < 0.9:
                    img_tile = 1
                else:
                    img_tile = 2

                background_layer.append(create_block(x, y, "grass", True, img_tile))
                main_layer.append(create_block(x, y, "empty", True, None))

            x = x + 16
        y = y + 16
        x = 0

        def calculate_index(i, x_offset, y_offset):
            return i + x_offset + y_offset * level_width

        # Fix for house - add correct images to blockers
        for i, block in enumerate(main_layer):
            if block["type"] == "house":
                main_layer[calculate_index(i, -2, 0)]["img_tile"] = img_tiles[72]
                main_layer[calculate_index(i, -1, 0)]["img_tile"] = img_tiles[84]
                main_layer[calculate_index(i, 1, 0)]["img_tile"] = img_tiles[75]

                main_layer[calculate_index(i, -2, -1)]["img_tile"] = img_tiles[60]
                main_layer[calculate_index(i, -1, -1)]["img_tile"] = img_tiles[61]
                main_layer[calculate_index(i, 0, -1)]["img_tile"] = img_tiles[63]
                main_layer[calculate_index(i, 1, -1)]["img_tile"] = img_tiles[62]

                main_layer[calculate_index(i, -2, -2)]["img_tile"] = img_tiles[48]
                main_layer[calculate_index(i, -1, -2)]["img_tile"] = img_tiles[51]
                main_layer[calculate_index(i, 0, -2)]["img_tile"] = img_tiles[49]
                main_layer[calculate_index(i, 1, -2)]["img_tile"] = img_tiles[50]
            elif block["type"] == "forest":
                if block["rect"].y == 0 and block["rect"].x == 0:
                    top_layer.append(create_block(16, 16, "forest", True, 32))
                elif block["rect"].y == 10 * 16 and block["rect"].x == 0:
                    top_layer.append(create_block(16, block["rect"].y - 16, "forest", True, 8))
                elif block["rect"].y == 10 * 16 and block["rect"].x == 19 * 16:
                    top_layer.append(create_block(block["rect"].x - 16, block["rect"].y - 16, "forest", True, 6))
                elif block["rect"].y == 0 and block["rect"].x == 19*16:
                    top_layer.append(create_block(block["rect"].x - 16, 16, "forest", True, 30))
                elif block["rect"].y == 0:
                    top_layer.append(create_block(block["rect"].x - 16, 16, "forest", True, 31))
                elif block["rect"].y == 10 * 16:
                    top_layer.append(create_block(block["rect"].x, block["rect"].y - 16, "forest", True, 7))
                elif block["rect"].x == 0:
                    top_layer.append(create_block(16, block["rect"].y, "forest", True, 20))
                elif block["rect"].x == 19 * 16:
                    top_layer.append(create_block(block["rect"].x - 16, block["rect"].y, "forest", True, 18))

    return background_layer, main_layer, top_layer


screen = pygame.display.set_mode((320, 180), pygame.SCALED)

##########################################################################
# This is where the tilesheet gets loaded, this uses the Utils file
tiny_town_tilesheet = pygame.image.load("tilemap_packed_town.png").convert_alpha()
town_tiles = Utils.unpack_tilemap(tiny_town_tilesheet, tiny_town_tilesheet.get_width(), tiny_town_tilesheet.get_height(), 16)

dungeon_tilesheet = pygame.image.load("tilemap_packed_dungeon.png").convert_alpha()
dungeon_tiles = Utils.unpack_tilemap(dungeon_tilesheet, dungeon_tilesheet.get_width(), dungeon_tilesheet.get_height(), 16)

game_state = "GAME"

player = {
    "rect": pygame.Rect(32, 32, 16, 16),
    "speed": 2
}

background_layer, main_layer, top_layer = load_level(Levels.level00, town_tiles)

clock = pygame.time.Clock()

game_running = True
while game_running:
    ##################################################################################
    # This code runs every frame don't move or change this
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    dt = clock.tick(40)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game_state = "QUIT"

    if keys[pygame.K_j]:
        background_layer, main_layer, top_layer = load_level(Levels.level01, town_tiles)
    if keys[pygame.K_i]:
        background_layer, main_layer, top_layer = load_level(Levels.level00, town_tiles)

    ##################################################################################
    # QUIT state, setting the game state to this will close the game window
    if game_state == "QUIT":
        game_running = False
        
    ##################################################################################
    # GAME state, this is where we control the main game
    if game_state == "GAME":
        
        ##################################################################################
        # INPUT CODE
        targetX = pygame.Rect(player["rect"])
        targetY = pygame.Rect(player["rect"])
        
        if keys[pygame.K_d]:
            targetX.x += player["speed"]
        if keys[pygame.K_a]:
            targetX.x -= player["speed"]
        if keys[pygame.K_s]:
            targetY.y += player["speed"]
        if keys[pygame.K_w]:
            targetY.y -= player["speed"]

        for block in main_layer:
            if not block["can_move"]:
                if targetX.colliderect(block["rect"]):
                    if targetX.x < block["rect"].x:
                        targetX.right = block["rect"].left
                    else:
                        targetX.left = block["rect"].right
                if targetY.colliderect(block["rect"]):
                    if targetY.y < block["rect"].y:
                        targetY.bottom = block["rect"].top
                    else:
                        targetY.top = block["rect"].bottom

        player["rect"].x = targetX.x
        player["rect"].y = targetY.y

        ##################################################################################
        # DRAWING CODE
        # Background fill
        screen.fill((222, 125, 87))

        # Background tiles
        for block in background_layer:
            screen.blit(block["img_tile"], block["rect"])

        # Main layer            
        for block in main_layer:
            if "img_tile" in block:
                screen.blit(block["img_tile"], block["rect"])

        # Player layer
        screen.blit(dungeon_tiles[97], player["rect"])
        
        # Top layer
        for block in top_layer:
            if "img_tile" in block:
                screen.blit(block["img_tile"], block["rect"])

    pygame.display.flip()

pygame.quit()
