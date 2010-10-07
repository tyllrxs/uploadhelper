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
    def __init__(self, window, urls, source_url = ''):
        Thread.__init__(self)
	self.window = window
	self.urls = urls
	self.source_url = source_url
	self.host = get_url_host(source_url)
	self.path = get_url_path(source_url)
	self.start()
 
    def run(self):
	self.filenames = []
	num = 1
    	for url in self.urls:
    		if self.window.ignore and url.lower().endswith('.gif'):
    			fname = '-'
    		else:
	    		fname = url
	    		if not supported_file_type(fname):
	    			if supported_file_type(urlparse(fname).path):
	    				fname += get_file_type(urlparse(fname).path)
	    			else:
	    				fname += '.jpg'
	    		fname = re.sub(r'[^\w\d\.\{\}\[\]\(\)\+\=\-\_\&\%\#\@\~]', '_', fname)
	    		fname = os.path.join(TEMP_DIR, fname)
	    		if self.source_url and not url.startswith('http://'):
	    			if url.startswith('/'):
	    				url = self.host + url
	    			else:
	    				url = self.path + url
	    		try:
	    			urllib.urlretrieve(url, fname)
	    		except:
	    			fname = ''
    		wx.CallAfter(self.DownloadInfo, num, url, fname)
    		self.filenames.append(fname)
    		num += 1
        wx.CallAfter(self.PostDownloadInfo)
 
    def DownloadInfo(self, num, url, filename):
    	self.window.txtReship.AppendText('\n%s ( %d / %d ):\n%s\n' % (_('Downloading'), num, len(self.urls), url))
    	if filename:
    		if filename != '-':
			self.window.txtReship.AppendText('%s: %s\n%s\n' % (_('Saved to'), filename, _('Finished')))
		else:
			self.window.txtReship.AppendText('%s\n' % _('Skip'))
	else:
		self.window.txtReship.AppendText('%s\n' % _('Failed'))

    def PostDownloadInfo(self):
    	self.window.txtReship.AppendText(SEPARATOR)
	Publisher().sendMessage("update", '%s|%s' % ('Download', '|'.join(self.filenames)))
	
	
