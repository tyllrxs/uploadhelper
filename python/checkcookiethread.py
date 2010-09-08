# -*- coding: utf-8 -*-

import wx
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from utilfunc import *

class CheckCookieThread(Thread):
    """Check if cookie is valid."""
 
    #----------------------------------------------------------------------
    def __init__(self, window):
        Thread.__init__(self)
	self.window = window
        self.start()
 
    #----------------------------------------------------------------------
    def run(self):
	self.info = perfect_connect('http://%s/bbs/preupload?board=%s' % (self.window.get_host(), self.window.get_board_name()))
        wx.CallAfter(self.checkCookie)
 
    #----------------------------------------------------------------------
    def checkCookie(self):
	Publisher().sendMessage("update", '%s|%s' % ('Cookie', self.info))
