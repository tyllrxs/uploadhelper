# -*- coding: utf-8 -*-

import Image, ImageDraw, ImageChops, ImageEnhance, ImageFont
from consts import *

def get_mark_position(im_size, mark_size, position=0, padding=0):
    if position == 0:
        #lefttop
        position = (padding, padding)
    elif position == 1:
        #righttop
        position = (im_size[0] - mark_size[0] - padding, padding)
    elif position == 2:
        #center
        position = ((im_size[0] - mark_size[0]) / 2, (im_size[1] - mark_size[1]) / 2)
    elif position == 3:
        #left bottom
        position = (padding, im_size[1] - mark_size[1] - padding)
    else:
        #right bottom
        position = (im_size[0] - mark_size[0] - padding, im_size[1] - mark_size[1] - padding)
    return position

def signature(imagefile, text, position=0, padding=0, font=None, size=24, color=(0, 0, 0), opacity=1):
    """Adds text to an image as watermark."""  
    im = Image.open(imagefile)
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    textdraw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(font, size)
    textsize = textdraw.textsize(text, font = font)
    textpos = get_mark_position(im.size, textsize, position, padding)
    textdraw.text(textpos, text, font = font, fill = color)
    del textdraw
    if opacity < 1:
        layer = reduce_opacity(layer, opacity)
    return Image.composite(layer, im, layer)
    
def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(imagefile, markfile, position=0, padding=0, opacity=1):
    """Adds a watermark to an image."""   
    im = Image.open(imagefile)
    mark = Image.open(markfile)   
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    position = get_mark_position(im.size, mark.size, position, padding)
    layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)
    
    
