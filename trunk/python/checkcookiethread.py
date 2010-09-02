# -*- coding: utf-8 -*-

import urllib2
import wx
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from utilfunc import *

class CheckCookieThread(Thread):
    """Check if cookie is valid."""
 
    #----------------------------------------------------------------------
    def __init__(self, host, board, cookie):
        Thread.__init__(self)
	self.host = host
	self.board = board
	self.cookie = cookie
        self.start()
 
    #----------------------------------------------------------------------
    def run(self):
	req = urllib2.Request('http://%s/bbs/preupload?board=%s' % (self.host, self.board))
	req.add_header('Cookie', self.cookie)
        try:		    
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError, e:  
		self.info = '%s|%s: %d' % ('Network Error', 'Error code', e.code)
	except:
		self.info = 'Error|Network Error.'
	else:
		the_page = resp.read().decode('gb18030').encode('utf8')
		if the_page.find('发生错误') >= 0:
			k, v = get_html_info(the_page)
			self.info = '|'.join([k, v])
		else:
			self.info = 'OK'
        wx.CallAfter(self.checkCookie)
 
    #----------------------------------------------------------------------
    def checkCookie(self):
	Publisher().sendMessage("update", '%s|%s' % ('Cookie', self.info))
