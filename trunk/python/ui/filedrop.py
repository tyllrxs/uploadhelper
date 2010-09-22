# -*- coding: utf-8 -*-

import wx

class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
	wx.FileDropTarget.__init__(self)
	self.window = window

    def OnDropFiles(self, x, y, paths):
	self.window.append_files(paths)
