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
    def __init__(self, host, board):
        Thread.__init__(self)
	self.host = host
	self.board = board
        self.start()
 
    #----------------------------------------------------------------------
    def run(self):
	self.info = perfect_connect('http://%s/bbs/preupload?board=%s' % (self.host, self.board))
        wx.CallAfter(self.checkCookie)
 
    #----------------------------------------------------------------------
    def checkCookie(self):
	Publisher().sendMessage("update", '%s|%s' % ('Cookie', self.info))
