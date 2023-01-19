import pygame
import random
import Levels
import Utils

pygame.init()

def load_level(level):
    block_list = []
    x = y = 0
    for row in level:
        for col in row:
            if col == "#":
                block = {
                    "rect": pygame.Rect(x, y, 16, 16),
                    "type": "forest",
                    "can_move": False,
                    "rand": random.random()
                    }
            elif col == "H":
                block = {
                    "rect": pygame.Rect(x, y, 16, 16),
                    "type": "house",
                    "can_move": False,
                    "rand": random.random()
                    }
            elif col == "X":
                block = {
                    "rect": pygame.Rect(x, y, 16, 16),
                    "type": "blocker",
                    "can_move": False,
                    "rand": random.random()
                    }
            elif col == "+":
                block = {
                    "rect": pygame.Rect(x, y, 16, 16),
                    "type": "path",
                    "can_move": True,
                    "rand": random.random()
                    }
            else:
                block = {
                    "rect": pygame.Rect(x, y, 16, 16),
                    "type": "grass",
                    "can_move": True,
                    "rand": random.random()
                    }
            block_list.append(block)
            x = x + 16
        y = y + 16
        x = 0
        
    return block_list

screen = pygame.display.set_mode((320,180), pygame.SCALED)

##########################################################################
# This is where the tilesheet gets loaded, this uses the Utils file
tiny_town_tilesheet = pygame.image.load("tilemap_packed_town.png").convert_alpha()
town_tiles = Utils.unpack_tilemap(tiny_town_tilesheet, tiny_town_tilesheet.get_width(), tiny_town_tilesheet.get_height(), 16)

dungeon_tilesheet = pygame.image.load("tilemap_packed_dungeon.png").convert_alpha()
dungeon_tiles = Utils.unpack_tilemap(dungeon_tilesheet, dungeon_tilesheet.get_width(), dungeon_tilesheet.get_height(), 16)

game_state = "GAME"

player = {
    "rect": pygame.Rect(32,32,16,16),
    "speed": 2
    }

blocks = load_level(Levels.level00)

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
        blocks = load_level(Levels.level01)
    if keys[pygame.K_i]:
        blocks = load_level(Levels.level00)

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

        for block in blocks:
            if block["can_move"] == False:
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
        screen.fill((222,125,87))
        # Background tiles        
        for block in blocks:
            if block["type"] == "forest":
                screen.blit(town_tiles[19], block["rect"])
            if block["type"] == "path":
                screen.blit(town_tiles[43], block["rect"])
            if block["type"] == "grass":
                if block["rand"] < 0.7:
                    screen.blit(town_tiles[0], block["rect"])
                elif block["rand"] < 0.9:
                    screen.blit(town_tiles[1], block["rect"])
                else:
                    screen.blit(town_tiles[2], block["rect"])

        # Main layer            
        for block in blocks:
            if block["type"] == "house":
                screen.blit(town_tiles[85], block["rect"])
                screen.blit(town_tiles[72], Utils.adjacent_coord(block["rect"], 16, -2, 0))
                screen.blit(town_tiles[84], Utils.adjacent_coord(block["rect"], 16, -1, 0))
                screen.blit(town_tiles[75], Utils.adjacent_coord(block["rect"], 16, 1, 0))
                
                screen.blit(town_tiles[60], Utils.adjacent_coord(block["rect"], 16, -2, 1))
                screen.blit(town_tiles[61], Utils.adjacent_coord(block["rect"], 16, -1, 1))
                screen.blit(town_tiles[63], Utils.adjacent_coord(block["rect"], 16, 0, 1))
                screen.blit(town_tiles[62], Utils.adjacent_coord(block["rect"], 16, 1, 1))

                screen.blit(town_tiles[48], Utils.adjacent_coord(block["rect"], 16, -2, 2))
                screen.blit(town_tiles[51], Utils.adjacent_coord(block["rect"], 16, -1, 2))
                screen.blit(town_tiles[49], Utils.adjacent_coord(block["rect"], 16, 0, 2))
                screen.blit(town_tiles[50], Utils.adjacent_coord(block["rect"], 16, 1, 2))
        
        # Player layer
        screen.blit(dungeon_tiles[97], player["rect"])
        
        # Top layer
        for block in blocks:
            if block["type"] == "forest":
                if block["rect"].y == 0 and block["rect"].x == 0:
                    screen.blit(town_tiles[32], Utils.adjacent_coord(block["rect"], 16, 1, -1))
                elif block["rect"].y == 10*16 and block["rect"].x == 0:
                    screen.blit(town_tiles[8], Utils.adjacent_coord(block["rect"], 16, 1, 1))
                elif block["rect"].y == 10*16 and block["rect"].x == 19*16:
                    screen.blit(town_tiles[6], Utils.adjacent_coord(block["rect"], 16, -1, 1))
                elif block["rect"].y == 0 and block["rect"].x == 19*16:
                    screen.blit(town_tiles[30], Utils.adjacent_coord(block["rect"], 16, -1, -1))
                elif block["rect"].y == 0:
                    screen.blit(town_tiles[31], Utils.adjacent_coord(block["rect"], 16, 0, -1))
                elif block["rect"].y == 10*16:
                    screen.blit(town_tiles[7], Utils.adjacent_coord(block["rect"], 16, 0, 1))
                elif block["rect"].x == 0:
                    screen.blit(town_tiles[20], Utils.adjacent_coord(block["rect"], 16, 1, 0))
                elif block["rect"].x == 19*16:
                    screen.blit(town_tiles[18], Utils.adjacent_coord(block["rect"], 16, -1, 0))
        
    pygame.display.flip()

pygame.quit()
