# -*- coding: utf-8 -*-

import wx

class ddTaskBarIcon(wx.TaskBarIcon):

    ID_Restore = wx.NewId()

    def __init__(self, icon, tooltip, frame):
        wx.TaskBarIcon.__init__(self)
        self.SetIcon(icon, tooltip)
        self.frame = frame
	self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.on_left_dclick)
	self.Bind(wx.EVT_MENU, self.OnRestore, id = self.ID_Restore)
	self.Bind(wx.EVT_MENU, self.OnExit, id = wx.ID_EXIT)

    def on_left_dclick(self, e):
        if self.frame.IsIconized():
        	self.frame.Iconize(False)
        	self.frame.Raise()
        else:
        	self.frame.Iconize(True)

    # override
    def CreatePopupMenu(self):
        menu = wx.Menu()
	menu.Append(self.ID_Restore, _('Restore Window'))
	menu.AppendSeparator()
	menu.Append(wx.ID_EXIT, _('Exit'))
	return menu

    def OnRestore(self, evt):
	wx.MessageBox('Hello From TaskBarIcon!', 'Prompt')
	
    def OnExit(self, evt):
	self.frame.Close()
	
