# -*- coding: utf-8 -*-

import os, sys
import urllib, urllib2, cookielib
import wx
from consts import *
from utilfunc import *
from httpredirect import *


class MyLoginDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        self.imgTitle = wx.StaticBitmap(self, -1, wx.Bitmap("icon/title.png"))
        self.label_1 = wx.StaticText(self, -1, _("BBS host"), style=wx.ALIGN_CENTRE)
        self.cmbHost = wx.Choice(self, -1, choices=BBS_HOSTS)
        self.label_2 = wx.StaticText(self, -1, _("User"), style=wx.ALIGN_CENTRE)
        self.txtUser = wx.TextCtrl(self, -1, "")
        self.label_3 = wx.StaticText(self, -1, _("Password"), style=wx.ALIGN_CENTRE)
        self.txtPwd = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.lnkHelp = wx.HyperlinkCtrl(self, -1, _("How to Use"), '%s%s' % (HOMEPAGE, 'faq.htm'))
        self.chkAutoLogin = wx.CheckBox(self, -1, _("Auto Login"))
        self.btnLogin = wx.Button(self, -1, _("Login"))
        
        self.__set_properties()
        self.__do_layout()
        
	self.Bind(wx.EVT_BUTTON, self.OnbtnLoginClick, self.btnLogin)
	self.Bind(wx.EVT_CLOSE, self.OnClose)
	
    def __set_properties(self):
        self.SetTitle(_("Login"))
        self.cmbHost.SetSelection(read_config_int('Login', 'Host', 0))
        self.txtUser.SetValue(read_config('Login', 'UserID'))
	self.txtPwd.SetValue(read_config('Login', 'Password'))
	self.chkAutoLogin.SetValue(read_config_bool('Login', 'AutoLogin', True))
	self.btnLogin.SetDefault()

    def __do_layout(self):
        object_1 = wx.BoxSizer(wx.VERTICAL)
        object_5 = wx.BoxSizer(wx.HORIZONTAL)
        object_4 = wx.BoxSizer(wx.HORIZONTAL)
        object_3 = wx.BoxSizer(wx.HORIZONTAL)
        object_2 = wx.BoxSizer(wx.HORIZONTAL)
        object_1.Add(self.imgTitle, 0, wx.BOTTOM, 5)
        object_2.Add(self.label_1, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_2.Add(self.cmbHost, 3, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_1.Add(object_2, 1, wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        object_3.Add(self.label_2, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_3.Add(self.txtUser, 3, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_1.Add(object_3, 1, wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        object_4.Add(self.label_3, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_4.Add(self.txtPwd, 3, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_1.Add(object_4, 1, wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        object_5.Add(self.lnkHelp, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_5.Add((20, 20), 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        object_5.Add(self.chkAutoLogin, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_1.Add(object_5, 1, wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        object_1.Add(self.btnLogin, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(object_1)
        object_1.Fit(self)
        self.Layout()
        self.Centre()

    def OnbtnLoginClick(self, evt):
	host = self.cmbHost.GetSelection()
	userid = self.txtUser.GetValue().strip()
	pwd = self.txtPwd.GetValue().strip()
	autologin = self.chkAutoLogin.IsChecked()
	if userid == '' or pwd == '':
		wx.MessageBox(MSG_FILL_BLANKS)
		return
	opener = urllib2.build_opener(SmartRedirectHandler())  
	urllib2.install_opener(opener)  
	req = urllib2.Request('http://%s/bbs/login' % BBS_HOSTS[host], urllib.urlencode({'id': userid, 'pw': pwd}))  
	try:
		resp = urllib2.urlopen(req)  
	except urllib2.HTTPError, e:  
		wx.MessageBox('%s: %d' % (MSG_ERROR_CODE, e.code), MSG_NETWORK_ERROR) 
		return
	except:
		wx.MessageBox(MSG_NETWORK_ERROR)
		return
	else:
		if resp.code != 302:			
			the_page = resp.read().decode('gb18030').encode('utf8')
			head, body = get_html_info(the_page)
			wx.MessageBox(body, head)
			return
		else:
			cookie = ';'.join(resp.headers['set-cookie'].split(','))
			write_config('Login', {'UserID': userid, 'Password': pwd, 'Cookie': cookie, 'Host': host, 'AutoLogin': autologin})
			wx.MessageBox(_('Login OK. Prepare to upload files.'))
			update_title()
			self.Close()
	
    def OnClose(self, evt):
	self.Destroy()

# end of class MyLoginDialog


class MyAboutDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):    
        wx.Dialog.__init__(self, *args, **kwargs)
        self.imgLogo = wx.StaticBitmap(self, -1, wx.Bitmap('icon/logo.png'))
        self.txtAppName = wx.StaticText(self, label = APPNAME)
        font1 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        self.txtAppName.SetFont(font1)
        self.txtInfo = wx.StaticText(self)
        self.txtInfo.SetLabel('%s: %s\n%s: %s (%s)\n%s: %s\n%s: GPL v2' 
		% (_('Version'), VERSION, _('Author'), AUTHOR, EMAIL, _('Homepage'), HOMEPAGE, _('License')))
        self.txtLink = wx.HyperlinkCtrl(self, -1, _('Visit Homepage'), HOMEPAGE, style = wx.HL_ALIGN_LEFT)
        self.btnOK = wx.Button(self, wx.ID_OK)

        self.__set_properties()
        self.__do_layout()

	self.Bind(wx.EVT_CLOSE, self.OnClose)
	
    def __set_properties(self):
        self.SetTitle(_("About"))

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.imgLogo, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(self.txtAppName, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.txtInfo, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(wx.StaticLine(self), 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer.Add(self.txtLink, 1, wx.ALIGN_CENTRE_VERTICAL)
        subsizer.Add(self.btnOK, 0, wx.ALIGN_CENTRE_VERTICAL)
        sizer.Add(subsizer, 0, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        self.Centre()
		
    def OnClose(self, evt):
	self.Destroy()
	
# end of class MyAboutDialog
