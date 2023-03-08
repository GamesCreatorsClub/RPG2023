import pygame
import levels
import Utils

pygame.init()


WINDOW_WIDTH = 320
WINDOW_HEIGHT = 180


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED)

##########################################################################
# This is where the tilesheet gets loaded, this uses the Utils file
tiny_town_tilesheet = pygame.image.load("tilemap_packed_town.png").convert_alpha()
town_tiles = Utils.unpack_tilemap(tiny_town_tilesheet, tiny_town_tilesheet.get_width(), tiny_town_tilesheet.get_height(), 16)

dungeon_tilesheet = pygame.image.load("tilemap_packed_dungeon.png").convert_alpha()
dungeon_tiles = Utils.unpack_tilemap(dungeon_tilesheet, dungeon_tilesheet.get_width(), dungeon_tilesheet.get_height(), 16)

game_state = "GAME"


def initialise():
    player = {
        "rect": pygame.Rect(32, 32, 16, 16),
        "speed": 2,
        "over_tiles": []
    }

    for level in levels.levels:
        levels.load_level(level)

    current_level = {
        "map_no": 0,
        "player": player,
        "background_layer": levels.levels[0]["background_layer"],
        "main_layer": levels.levels[0]["main_layer"],
        "top_layer": levels.levels[0]["top_layer"],
        "level": levels.levels[0]
    }

    return current_level


def player_tries_to_leave_map():
    for over_tile in over_tiles:
        if "on_leave_map" in over_tile:
            over_tile["on_leave_map"](over_tile, current_level)


current_level = initialise()

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

    ##################################################################################
    # QUIT state, setting the game state to this will close the game window
    if game_state == "QUIT":
        game_running = False
        
    ##################################################################################
    # GAME state, this is where we control the main game
    if game_state == "GAME":
        player = current_level["player"]

        ##################################################################################
        # INPUT CODE
        player_rect = player["rect"]
        targetX = pygame.Rect(player_rect)
        targetY = pygame.Rect(player_rect)

        tried_to_go_off_map = False
        moved_player = False
        if keys[pygame.K_d]:
            targetX.x += player["speed"]
            if targetX.x > WINDOW_WIDTH - player_rect.width:
                targetX.x = WINDOW_WIDTH - player_rect.width
                tried_to_go_off_map = True
        if keys[pygame.K_a]:
            targetX.x -= player["speed"]
            if targetX.x < 0:
                targetX.x = 0
                tried_to_go_off_map = True
        if keys[pygame.K_s]:
            targetY.y += player["speed"]
            if targetY.y > WINDOW_HEIGHT - player_rect.height:
                targetY.y = WINDOW_HEIGHT - player_rect.height
                tried_to_go_off_map = True
        if keys[pygame.K_w]:
            targetY.y -= player["speed"]
            if targetY.y < 0:
                targetY.y = 0
                tried_to_go_off_map = True

        for block in current_level["main_layer"]:
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

        if player_rect.x != targetX.x or player_rect.y != targetY.y:
            player_rect.x = targetX.x
            player_rect.y = targetY.y
            moved_player = True

        if tried_to_go_off_map:
            player_tries_to_leave_map()

        if moved_player:
            over_tiles = player["over_tiles"]
            for block in current_level["main_layer"]:
                block_rect = block["rect"]
                collides = player_rect.colliderect(block_rect)
                if block in over_tiles:
                    if not collides:
                        del over_tiles[over_tiles.index(block)]
                        if "on_leave_tile" in block:
                            block["on_leave_tile"](block, current_level)
                else:
                    if collides:
                        over_tiles.append(block)
                        if "on_enter_tile" in block:
                            block["on_enter_tile"](block, current_level)

        ##################################################################################
        # DRAWING CODE
        # Background fill
        screen.fill((222, 125, 87))

        # Background tiles
        for block in current_level["background_layer"]:
            screen.blit(town_tiles[block["img_tile"]], block["rect"])

        # Main layer            
        for block in current_level["main_layer"]:
            if "img_tile" in block:
                screen.blit(town_tiles[block["img_tile"]], block["rect"])

        # Player layer
        screen.blit(dungeon_tiles[97], player["rect"])
        
        # Top layer
        for block in current_level["top_layer"]:
            if "img_tile" in block:
                screen.blit(town_tiles[block["img_tile"]], block["rect"])

    pygame.display.flip()

pygame.quit()
