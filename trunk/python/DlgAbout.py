# -*- coding: utf-8 -*-

import wx
from wx import xrc
from consts import *


class DlgAbout(wx.Dialog):
    def __init__(self):
        self.res = xrc.XmlResource('ui/dlgAbout.xrc')
	self.dialog = self.res.LoadDialog(None, 'dlgAbout')
	xrc.XRCCTRL(self.dialog, 'lblAppName').SetLabel(APPNAME)
	xrc.XRCCTRL(self.dialog, 'lblDetail').SetLabel('%s: %s\n%s: %s (%s)\n%s: %s\n%s: GPL v2' 
		% (_('Version'), VERSION, _('Author'), AUTHOR, EMAIL, _('Homepage'), HOMEPAGE, _('License')))
	xrc.XRCCTRL(self.dialog, 'btnOK').SetId(wx.ID_OK)
	self.dialog.Bind(wx.EVT_CLOSE, self.OnClose)
	
    def OnClose(self, evt):
	self.dialog.Destroy()
