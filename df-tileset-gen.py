#!/usr/bin/env python
# -*- coding: utf8 -*-

from gimpfu import *
import gimpcolor
import math

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def draw_shade_char(img, layer, density, x, y):
    size = layer.height
    for j in xrange(4):
        for k in xrange(j % 4, size, 4):
            pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                    x + k, y + j, 1, 1)
            pdb.gimp_edit_bucket_fill_full(layer, FG_BUCKET_FILL, NORMAL_MODE, 100,
                    255, False, True, SELECT_CRITERION_COMPOSITE, 0, 0)

    for j in map(lambda x: 4 * 2**x,
            xrange(int(math.ceil(math.log(size, 2))))):
        copy = pdb.gimp_layer_copy(layer, False)
        pdb.gimp_image_insert_layer(img, copy, None, -1)
        pdb.gimp_layer_translate(copy, 0, j)
        layer = pdb.gimp_image_merge_down(img, copy, CLIP_TO_BOTTOM_LAYER)

    if density == 1:
        copy1 = pdb.gimp_layer_copy(layer, False)
        copy2 = pdb.gimp_layer_copy(layer, False)
        pdb.gimp_image_insert_layer(img, copy1, None, -1)
        pdb.gimp_image_insert_layer(img, copy2, None, -1)
        pdb.gimp_layer_translate(copy1, 2, 0)
        pdb.gimp_layer_translate(copy2, -2, 0)
        layer = pdb.gimp_image_merge_down(img, copy1, CLIP_TO_BOTTOM_LAYER)
        layer = pdb.gimp_image_merge_down(img, copy2, CLIP_TO_BOTTOM_LAYER)
    if density == 2:
        copy1 = pdb.gimp_layer_copy(layer, False)
        copy2 = pdb.gimp_layer_copy(layer, False)
        copy3 = pdb.gimp_layer_copy(layer, False)
        copy4 = pdb.gimp_layer_copy(layer, False)
        pdb.gimp_image_insert_layer(img, copy1, None, -1)
        pdb.gimp_image_insert_layer(img, copy2, None, -1)
        pdb.gimp_image_insert_layer(img, copy3, None, -1)
        pdb.gimp_image_insert_layer(img, copy4, None, -1)
        pdb.gimp_layer_translate(copy1, 1, 0)
        pdb.gimp_layer_translate(copy2, -1, 0)
        pdb.gimp_layer_translate(copy3, 3, 0)
        pdb.gimp_layer_translate(copy4, -3, 0)
        layer = pdb.gimp_image_merge_down(img, copy1, CLIP_TO_BOTTOM_LAYER)
        layer = pdb.gimp_image_merge_down(img, copy2, CLIP_TO_BOTTOM_LAYER)
        layer = pdb.gimp_image_merge_down(img, copy3, CLIP_TO_BOTTOM_LAYER)
        layer = pdb.gimp_image_merge_down(img, copy4, CLIP_TO_BOTTOM_LAYER)
    pdb.gimp_selection_none(img)

def draw_fill_char(img, layer, index, x, y):
    size = layer.height
    if index == 0:
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                x, y, size, size)
    elif index == 1:
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                x, y + size / 2, size, size / 2)
    elif index == 2:
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                x, y, size / 2, size)
    elif index == 3:
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                x + size / 2, y, size / 2, size)
    elif index == 4:
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                x, y, size, size / 2)
    pdb.gimp_edit_bucket_fill_full(layer, FG_BUCKET_FILL, NORMAL_MODE, 100,
                255, False, True, SELECT_CRITERION_COMPOSITE, 0, 0)
    pdb.gimp_selection_none(img)

def draw_box_char(img, layer, char, x, y):
    width = 4
    def draw_vert_line(top, length, hollow):
        cx = layer.width / 2
        cy = layer.height / 2
        if (hollow):
            pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                    x + cx - 3 * width / 2, top, 3 * width, length)
            pdb.gimp_edit_bucket_fill_full(layer, FG_BUCKET_FILL, NORMAL_MODE, 
                    100, 255, False, True, SELECT_CRITERION_COMPOSITE, 0, 0)
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                x + cx - width / 2, top, width, length)
        if (hollow):
            pdb.gimp_edit_clear(layer)
        else:
            pdb.gimp_edit_bucket_fill_full(layer, FG_BUCKET_FILL, NORMAL_MODE, 
                    100, 255, False, True, SELECT_CRITERION_COMPOSITE, 0, 0)
        pdb.gimp_selection_none(img)

    def draw_horiz_line(left, length, hollow):
        cx = layer.width / 2
        cy = layer.height / 2
        if (hollow):
            pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                    left, y + cy - 3 * width / 2, length, 3 * width)
            pdb.gimp_edit_bucket_fill_full(layer, FG_BUCKET_FILL, NORMAL_MODE, 
                    100, 255, False, True, SELECT_CRITERION_COMPOSITE, 0, 0)
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                left, y + cy - width / 2, length, width)
        if (hollow):
            pdb.gimp_edit_clear(layer)
        else:
            pdb.gimp_edit_bucket_fill_full(layer, FG_BUCKET_FILL, NORMAL_MODE, 
                    100, 255, False, True, SELECT_CRITERION_COMPOSITE, 0, 0)
        pdb.gimp_selection_none(img)

    def clear_vert_line(top, length):
        cx = layer.width / 2
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                x + cx - width / 2, top, width, length)
        pdb.gimp_edit_clear(layer)
        pdb.gimp_selection_none(img)

    def clear_horiz_line(top, length):
        cy = layer.height / 2
        pdb.gimp_image_select_rectangle(img, CHANNEL_OP_REPLACE,
                left, y + cy - width / 2, length, width)
        pdb.gimp_edit_clear(layer)
        pdb.gimp_selection_none(img)

    size = layer.height
    temp_layer = pdb.gimp_layer_copy(layer, False)
    pdb.gimp_image_insert_layer(img, temp_layer, None, -1)
    pdb.gimp_layer_resize(temp_layer, size, size, 0, 0)

#    "│","┤","╡","╢","╖","╕","╣","║","╗","╝","╜","╛","┐",
#    "└","┴","┬","├","─","┼","╞","╟","╚","╔","╩","╦","╠","═","╬","╧",
#    "╨","╤","╥","╙","╘","╒","╓","╫","╪","┘","┌"

    # Single vert line
    if (char == "│" or char == "┤" or char == "╡" or char == "├" or
            char == "┼" or char == "╞" or char == "╪"):
        draw_vert_line(y, layer.height, False)

    # Double vert line
    if (char == "╢" or char == "╣" or char == "║" or char == "╟" or
            char == "╠" or char == "╬" or char == "╫"):
        draw_vert_line(y, layer.height, True)

    # Single vert top half
    if (char == "╛" or char == "└" or char == "┴" or char == "╧" or
            char == "╘" or char == "┘"):
        draw_vert_line(y, layer.height / 2, False)

    # Double vert top half
    if (char == "╝" or char == "╜" or char == "╚" or char == "╩" or
            char == "╨" or char == "╙"):
        draw_vert_line(y, layer.height / 2, True)

    # Single vert bottom half
    if (char == "╕" or char == "┐" or char == "┬" or char == "╤" or
            char == "╒" or char == "┌"):
        draw_vert_line(y + layer.height / 2, layer.height, False)

    # Double vert bottom half
    if (char == "╖" or char == "╗" or char == "╔" or char == "╦" or
            char == "╥" or char == "╓"):
        draw_vert_line(y + layer.height / 2, layer.height, True)

    # Single horiz line
    if (char == "┴" or char == "┬" or char == "─" or char == "┼" or
            char == "╨" or char == "╥" or char == "╫"):
        draw_horiz_line(x, layer.width, False)

    # Double horiz line
    if (char == "╩" or char == "╦" or char == "═" or char == "╬" or
            char == "╧" or char == "╤" or char == "╪"):
        draw_horiz_line(x, layer.width, True)

    # Single horiz left half
    if (char == "┤" or char == "╢" or char == "╖" or char == "╜" or
            char == "┐" or char == "┘"):
        draw_horiz_line(x, layer.width / 2, False)

    # Double horiz left half
    if (char == "╡" or char == "╕" or char == "╣" or char == "╗" or
            char == "╝" or char == "╛"):
        draw_horiz_line(x, layer.width / 2, True)

    # Single horiz right half
    if (char == "└" or char == "├" or char == "╟" or char == "╙" or
            char == "╓" or char == "┌"):
        draw_horiz_line(x + layer.width / 2, layer.width, False)

    # Double horiz right half
    if (char == "╞" or char == "╚" or char == "╔" or char == "╠" or
            char == "╘" or char == "╒"):
        draw_horiz_line(x + layer.width / 2, layer.width, True)


    layer = pdb.gimp_image_merge_down(img, temp_layer, CLIP_TO_BOTTOM_LAYER)

def get_cell_width(img, font, height, square):
    if(square):
        return height
    layer = pdb.gimp_text_layer_new(img, "M",
            font, height * 3/4, UNIT_POINT)
    return layer.width + 2

def generate_tileset(cur_img, drawable, font, height, softening, square):

    gimp.context_push()
    width = get_cell_width(cur_img, font, height, square)
    img = pdb.gimp_image_new(16 * width, 16 * height, GRAY)
    img.undo_group_start()
    pdb.gimp_progress_init("Generating tileset...", None);

    chars = [" ","☺","☻","♥","♦","♣","♠","•","◘","○","◙","♂","♀","♪","♫","☼",
            "►","◄","↕","‼","¶","§","▬","↨","↑","↓","→","←","∟","↔","▲","▼",
            " ","!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/",
            "0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?",
            "@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
            "P","Q","R","S","T","U","V","W","X","Y","Z","[","\\","]","^","_",
            "`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o",
            "p","q","r","s","t","u","v","w","x","y","z","{","|","}","~","⌂",
            "Ç","ü","é","â","ä","à","å","ç","ê","ë","è","ï","î","ì","Ä","Å",
            "É","æ","Æ","ô","ö","ò","û","ù","ÿ","Ö","Ü","¢","£","¥","₧","ƒ",
            "á","í","ó","ú","ñ","Ñ","ª","º","¿","⌐","¬","½","¼","¡","«","»",
            "░","▒","▓","│","┤","╡","╢","╖","╕","╣","║","╗","╝","╜","╛","┐",
            "└","┴","┬","├","─","┼","╞","╟","╚","╔","╩","╦","╠","═","╬","╧",
            "╨","╤","╥","╙","╘","╒","╓","╫","╪","┘","┌","█","▄","▌","▐","▀",
            "α","ß","Γ","π","Σ","σ","τ","Φ","Θ","Ω","δ","∞","φ","ε","∩","≡",
            "±","≥","≤","⌠","⌡","÷","≈","°","∙","·","√","ⁿ","²","■"," "," "]

    # Skip blank cells, as Gimp errors on drawing these
    excepts = [0, 32, 254, 255]

    # Characters requiring special treatment
    # TODO: implement
    shade_chars = range(176,179)
    box_chars = range(179, 219)
    fill_chars = range(219, 224)
    bottom_aligns = [243]

    pdb.gimp_context_set_foreground(gimpcolor.RGB(1.0, 1.0, 1.0, 1.0))

    layer = pdb.gimp_layer_new(img, pdb.gimp_image_width(img),
                pdb.gimp_image_height(img), GRAYA_IMAGE, "Background",
                softening, NORMAL_MODE)
    pdb.gimp_image_insert_layer(img, layer, None, -1)
    pdb.gimp_edit_bucket_fill_full(layer, FG_BUCKET_FILL, NORMAL_MODE, 100,
            255, False, True, SELECT_CRITERION_COMPOSITE, 0, 0)


    for i in xrange(256):
        if i in excepts:
            pdb.gimp_progress_update(i / 255.0)
            continue
        x = (i % 16) * width
        y = math.floor(i / 16.0) * height
        if i in shade_chars:
            layer = pdb.gimp_layer_new(img, width, height, GRAYA_IMAGE, chars[i],
                        100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(img, layer, None, -1)
            pdb.gimp_layer_translate(layer, x, y)
            draw_shade_char(img, layer, i - shade_chars[0], x, y)
            pdb.gimp_progress_update(i / 255.0)
            continue
        if i in range(179, 219):
            layer = pdb.gimp_layer_new(img, width, height, GRAYA_IMAGE, chars[i],
                        100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(img, layer, None, -1)
            pdb.gimp_layer_translate(layer, x, y)
            draw_box_char(img, layer, chars[i], x, y)
            continue
        if i in fill_chars:
            layer = pdb.gimp_layer_new(img, width, height, GRAYA_IMAGE, chars[i],
                        100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(img, layer, None, -1)
            pdb.gimp_layer_translate(layer, x, y)
            draw_fill_char(img, layer, i - fill_chars[0], x, y)
            pdb.gimp_progress_update(i / 255.0)
            continue

        layer = pdb.gimp_text_layer_new(img, chars[i],
                font, height * 3.0/4.0, UNIT_PIXEL)
        pdb.gimp_image_insert_layer(img, layer, None, -1)
        if (layer.width > width):
            new_height = height * width / layer.width
            pdb.gimp_text_layer_set_font_size(layer, new_height * 3.0/4.0,
                    UNIT_PIXEL)
            pdb.gimp_layer_translate(layer, 0, (height - new_height) / 2)
        pdb.gimp_layer_translate(layer, x, y)
        pdb.gimp_layer_translate(layer, (width - layer.width) / 2.0, 0)
        if i in bottom_aligns:
            pdb.gimp_layer_translate(layer, 0, height - layer.height)
        pdb.gimp_progress_update(i / 255.0)

    pdb.gimp_image_grid_set_spacing(img, width, height)

    img.undo_group_end()
    pdb.gimp_display_new(img)
    gimp.context_pop()


register(
        "python_fu_df_tileset",
        "Generate a Dwarf Fortress tileset from the specified font.",
        "Generate a Dwarf Fortress tileset from the specified font.",
        "Philip Jones",
        "Philip Jones",
        "2017",
        "<Image>/Filters/Render/DF tileset generator...",
        "RGB*, GRAY*",
        [
            (PF_FONT, "font", "Font", "DejaVu Sans Mono"),
            (PF_INT, "height", "Tile height (px)", 96),
            (PF_SLIDER, "softening", "Background opacity", 20, (0.0, 100.0,
                1.0)),
            (PF_BOOL, "square", "Square", False)
            ],
        [],
        generate_tileset)

main()
