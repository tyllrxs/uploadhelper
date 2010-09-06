# -*- coding: utf-8 -*-

import wx
from wx import xrc

from consts import *

class DlgAbout(wx.Dialog):
    def __init__(self):
        self.res = xrc.XmlResource(PATH + '/ui/dlgAbout.xrc')
	self.dialog = self.res.LoadDialog(None, 'dlgAbout')
	xrc.XRCCTRL(self.dialog, 'lblAppName').SetLabel(APPNAME)
	xrc.XRCCTRL(self.dialog, 'lblDetail').SetLabel('Version: %s\nAuthor: %s (%s)\nHomepage: %s\nLicense: GPL v2' % (VERSION, AUTHOR, EMAIL, HOMEPAGE))
	xrc.XRCCTRL(self.dialog, 'btnOK').SetId(wx.ID_OK)
