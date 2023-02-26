def finish_house1(block, layer_definition):
    line_width = max(len(line) for line in layer_definition["map"])

    def calculate_index(i, x_offset, y_offset):
        return i + x_offset + y_offset * line_width

    main_layer = layer_definition["main_layer"]
    i = main_layer.index(block)
    main_layer[calculate_index(i, -2, 0)]["img_tile"] = 72
    main_layer[calculate_index(i, -1, 0)]["img_tile"] = 84
    main_layer[calculate_index(i, 1, 0)]["img_tile"] = 75

    main_layer[calculate_index(i, -2, -1)]["img_tile"] = 60
    main_layer[calculate_index(i, -1, -1)]["img_tile"] = 61
    main_layer[calculate_index(i, 0, -1)]["img_tile"] = 63
    main_layer[calculate_index(i, 1, -1)]["img_tile"] = 62

    main_layer[calculate_index(i, -2, -2)]["img_tile"] = 48
    main_layer[calculate_index(i, -1, -2)]["img_tile"] = 51
    main_layer[calculate_index(i, 0, -2)]["img_tile"] = 49
    main_layer[calculate_index(i, 1, -2)]["img_tile"] = 50


def finish_house_small1(block, layer_definition):
    line_width = max(len(line) for line in layer_definition["map"])

    def calculate_index(i, x_offset, y_offset):
        return i + x_offset + y_offset * line_width

    main_layer = layer_definition["main_layer"]
    i = main_layer.index(block)
    main_layer[calculate_index(i, -1, 0)]["img_tile"] = 72
    main_layer[calculate_index(i, 1, 0)]["img_tile"] = 75

    main_layer[calculate_index(i, -1, -1)]["img_tile"] = 48
    main_layer[calculate_index(i, 0, -1)]["img_tile"] = 51
    main_layer[calculate_index(i, 1, -1)]["img_tile"] = 50


def finish_house2(block, layer_definition):
    line_width = max(len(line) for line in layer_definition["map"])

    def calculate_index(i, x_offset, y_offset):
        return i + x_offset + y_offset * line_width

    main_layer = layer_definition["main_layer"]
    i = main_layer.index(block)
    main_layer[calculate_index(i, -2, 0)]["img_tile"] = 76
    main_layer[calculate_index(i, -1, 0)]["img_tile"] = 88
    main_layer[calculate_index(i, 1, 0)]["img_tile"] = 79

    main_layer[calculate_index(i, -2, -1)]["img_tile"] = 64
    main_layer[calculate_index(i, -1, -1)]["img_tile"] = 65
    main_layer[calculate_index(i, 0, -1)]["img_tile"] = 67
    main_layer[calculate_index(i, 1, -1)]["img_tile"] = 66

    main_layer[calculate_index(i, -2, -2)]["img_tile"] = 52
    main_layer[calculate_index(i, -1, -2)]["img_tile"] = 55
    main_layer[calculate_index(i, 0, -2)]["img_tile"] = 53
    main_layer[calculate_index(i, 1, -2)]["img_tile"] = 54
