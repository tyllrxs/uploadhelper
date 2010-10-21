# -*- coding: utf-8 -*-

import urllib2
import wx
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from utilfunc import *

class LogoutThread(Thread):
    """Logout current BBS ID."""
 
    #----------------------------------------------------------------------
    def __init__(self, window, quiet=False):
        Thread.__init__(self)
        self.window = window
	self.host = self.window.get_host()
	self.cookie = self.window.get_cookie()
	self.proxy = self.window.get_proxy()
	self.quiet = quiet
        self.start()
 
    #----------------------------------------------------------------------
    def run(self):
	req = urllib2.Request('http://%s/bbs/logout' % self.host)
	req.add_header('Cookie', self.cookie)
	if self.proxy:
		opener = urllib2.build_opener(urllib2.ProxyHandler({'http': self.proxy}))
		urllib2.install_opener(opener)
        try:		    
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError, e:  
		self.info = '%s|%s. %s: %d' % (MSG_LOGOUT, MSG_NETWORK_ERROR, MSG_ERROR_CODE, e.code)
	except:
		self.info = '%s|%s' % (MSG_LOGOUT, MSG_NETWORK_ERROR)
	else:
		the_page = resp.read().decode('gb18030')
		if the_page.find(u'发生错误') >= 0:
			k, v = get_html_info(the_page)
			self.info = '%s|%s: %s' % (MSG_LOGOUT, k, v)
		else:
			self.info = 'OK'
        wx.CallAfter(self.sendInfo)
 
    #----------------------------------------------------------------------
    def sendInfo(self):
	if not self.quiet:
		Publisher().sendMessage("update", '%s|%s' % ('Logout', self.info))
	
