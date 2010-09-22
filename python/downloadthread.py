# -*- coding: utf-8 -*-

import os
import urllib, re
from urlparse import urlparse
import wx
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from utilfunc import *

class DownloadThread(Thread):
    """Download Thread."""
    def __init__(self, window, urls):
        Thread.__init__(self)
	self.window = window
	self.urls = urls
	self.start()
 
    def run(self):
	self.filenames = []
	num = 1
    	for url in self.urls:
    		fname = url
    		if not supported_file_type(fname):
    			if supported_file_type(urlparse(fname).path):
    				fname += get_file_type(urlparse(fname).path)
    			else:
    				fname += '.jpg'
    		fname = re.sub(r'[^\w\d\.\{\}\[\]\(\)\+\=\-\_\&\%\#\@\~]', '_', fname)
    		fname = os.path.join(TEMP_DIR, fname)
    		try:
    			urllib.urlretrieve(url, fname)
    		except:
    			fname = ''
    		wx.CallAfter(self.DownloadInfo, num, url, fname)
    		self.filenames.append(fname)
    		num += 1
        wx.CallAfter(self.PostDownloadInfo)
 
    def DownloadInfo(self, num, url, filename):
    	if filename:
		self.window.reshipinfo.AppendText('\n%s ( %d / %d ):\n%s\n%s: %s\n%s\n' 
			% ('Downloading', num, len(self.urls), url, 'Saved To', filename, 'Finished'))
	else:
		self.window.reshipinfo.AppendText('\n%s ( %d / %d ):\n%s\n%s\n' 
			% ('Downloading', num, len(self.urls), url, 'Failed'))
 
    def PostDownloadInfo(self):
    	self.window.reshipinfo.AppendText(SEPARATOR)
	Publisher().sendMessage("update", '%s|%s' % ('Download', '|'.join(self.filenames)))
	
	