#!/usr/bin/env python
# -*- coding: utf8 -*-

from gimpfu import *
import gimpcolor
import math

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def draw_shade_char(img, layer, size, density, x, y):
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

def draw_fill_char(img, layer, size, index, x, y):
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

def get_cell_width(img, font, height, square):
    if(square):
        return height
    layer = pdb.gimp_text_layer_new(img, "M",
            font, height * 3/4, UNIT_POINT)
    pdb.gimp_image_insert_layer(img, layer, None, -1)
    width = pdb.gimp_drawable_width(layer)
    pdb.gimp_image_remove_layer(img, layer)
    return width

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

    box_char_base = 206
    box_chars = range(179, 219)

    fill_chars = range(219, 224)

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
            draw_shade_char(img, layer, height, i - shade_chars[0], x, y)
            pdb.gimp_progress_update(i / 255.0)
            continue
        if i in range(179, 219):
            pdb.gimp_progress_update(i / 255.0)
            continue
        if i in fill_chars:
            layer = pdb.gimp_layer_new(img, width, height, GRAYA_IMAGE, chars[i],
                        100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(img, layer, None, -1)
            pdb.gimp_layer_translate(layer, x, y)
            draw_fill_char(img, layer, height, i - fill_chars[0], x, y)
            pdb.gimp_progress_update(i / 255.0)
            continue

        layer = pdb.gimp_text_layer_new(img, chars[i],
                font, height * 3/4, UNIT_POINT)
        pdb.gimp_image_insert_layer(img, layer, None, -1)
        pdb.gimp_layer_translate(layer, x, y)
        w = pdb.gimp_drawable_width(layer)
        pdb.gimp_layer_translate(layer, (width - w) / 2.0, 0)
        pdb.gimp_progress_update(i / 255.0)

        if i == box_char_base:
            char_pixel_height = layer.height

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
