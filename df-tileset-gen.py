#!/usr/bin/python
# -*- coding: utf8 -*-

from gimpfu import *
import gimpenums
import gimpcolor

def plugin_main(img, tdrawable, font, size):
    #size = 72
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
    excepts = [0, 32, 254, 255]
    for i in xrange(16):
        for j in xrange(16):
            index = j + 16 * i
            if not index in excepts:
                layer = pdb.gimp_text_layer_new(img, chars[index],
                        font, size * 3/4, gimpenums.UNIT_PIXEL)
                pdb.gimp_image_insert_layer(img, layer, None, -1)
                pdb.gimp_layer_translate(layer, j * size, i * size)
                w = pdb.gimp_drawable_width(layer)
                pdb.gimp_layer_translate(layer, (size - w) / 2, 0)
                pdb.gimp_invert(layer)
    pdb.gimp_image_resize_to_layers(img)
    pdb.gimp_image_grid_set_spacing(img, size, size)

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
            (PF_INT, "size", "Size", 72)
        ],
        [],
        plugin_main)

main()
