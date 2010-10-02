# -*- coding: utf-8 -*-

import pyexiv2

def read_exif(filename):
	metadata = pyexiv2.ImageMetadata(filename)
	metadata.read()
	print metadata.exif_keys

