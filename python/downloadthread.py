# -*- coding: utf-8 -*-

import urllib, re
from urlparse import urlparse
import wx
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *

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
    		fname = '/tmp/%s' % urlparse(url).path.replace('/', '_')
    		if not re.search(r'\.[\d\w]{1,4}$', fname):
    			fname = '%s.jpg' % fname
    		urllib.urlretrieve(url, fname)
    		wx.CallAfter(self.DownloadInfo, url, num)
    		self.filenames.append(fname)
    		num += 1
        wx.CallAfter(self.PostDownloadInfo)
 
    def DownloadInfo(self, url, num):
	self.window.reshipinfo.AppendText('\n%s ( %d / %d ):\n%s\n%s\n' % ('Downloading', num, len(self.urls), url, 'Finished'))
 
    def PostDownloadInfo(self):
    	self.window.reshipinfo.AppendText(SEPARATOR)
	Publisher().sendMessage("update", '%s|%s' % ('Download', '|'.join(self.filenames)))
	
	
