# -*- coding: utf-8 -*-

import urllib2
import wx
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from utilfunc import *

class CheckUpdateThread(Thread):
    """Check for Updates Thread."""
 
    #----------------------------------------------------------------------
    def __init__(self):
        Thread.__init__(self)
        self.start()
 
    #----------------------------------------------------------------------
    def run(self):
	req = urllib2.Request('%s%s' % (HOMEPAGE, 'version.txt'))   
        try:		    
		resp = urllib2.urlopen(req)       
	except:
		self.info = ''
	else:
		the_page = resp.read()
		self.info = get_update_info(the_page, 'Version')
        wx.CallAfter(self.checkNewRelease)
 
    #----------------------------------------------------------------------
    def checkNewRelease(self):
	Publisher().sendMessage("update", 'Update|%s' % self.info)

