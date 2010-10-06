# -*- coding: utf-8 -*-

try:
	from PIL import Image, ImageDraw, ImageChops, ImageEnhance, ImageFont
except ImportError:
	print 'No PIL library found. Program may not be fully featured.'	

import os	
from consts import *

def do_resize(imagefile, width, height):
    """Resize image.""" 
    try: 
	    im = Image.open(imagefile)
	    w, h = im.size
	    if w > width:
	    	im = im.resize((width, width * h / w))
	    w, h = im.size
	    if h > height:
	    	im = im.resize((height * w / h, height))
	    newfile = os.path.join(TEMP_DIR, '%s_resize.jpg' % os.path.basename(imagefile))
	    im.save(newfile)
	    return newfile
    except:
	    return ''	    

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

def signature(imagefile, text, position=0, padding=0, font='', size=24, color=(0, 0, 0), savetofile=False):
    """Adds text to an image as watermark."""  
    try:
	    im = Image.open(imagefile)
	    if im.mode != "RGBA":
		im = im.convert("RGBA")
	    textdraw = ImageDraw.Draw(im)
	    font = ImageFont.truetype(font, size)
	    textsize = textdraw.textsize(text, font = font)
	    textpos = get_mark_position(im.size, textsize, position, padding)
	    textdraw.text(textpos, text, font = font, fill = color)
	    del textdraw
	    if savetofile:
	    	newfile = os.path.join(TEMP_DIR, '%s_watertext.jpg' % os.path.basename(imagefile))
	    	im.save(newfile)
	    	return newfile
	    else:
	    	return im
    except:
	    return ''
    
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

def watermark(imagefile, markfile, position=0, padding=0, opacity=1, savetofile=False):
    """Adds a watermark to an image."""   
    try:
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
	    newim = Image.composite(layer, im, layer)
	    if savetofile:
	    	newfile = os.path.join(TEMP_DIR, '%s_waterimage.jpg' % os.path.basename(imagefile))
	    	newim.save(newfile)
	    	return newfile
	    else:
	    	return newim
    except:
	    return ''
    
    
