
def unpack_tilemap(tilesheet, width, height, size):
    list_of_tile_images = []
    x_range = int(width / size)
    y_range = int(height / size)
    for y in range(y_range):
        for x in range(x_range):
            sprite = tilesheet.subsurface(x*size, y*size, size, size)
            list_of_tile_images.append(sprite)
    return list_of_tile_images
