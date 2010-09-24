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
        object_1.Add(self.imgTitle, 0, wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 5)
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
			the_page = resp.read().decode('gb18030')
			head, body = get_html_info(the_page)
			wx.MessageBox(body, head)
			return
		else:
			cookie = ';'.join(resp.headers['set-cookie'].split(','))
			write_config('Login', {'UserID': userid, 'Password': pwd, 'Cookie': cookie, 'Host': host, 'AutoLogin': autologin})
			wx.MessageBox(_('Login OK. Prepare to upload files.'))
			update_title()
			if self.Parent.to_upload:
				evt = wx.CommandEvent()
				self.Parent.OnbtnUploadClick(evt)
			if self.Parent.to_post:
				evt = wx.CommandEvent()
				self.Parent.OnbtnPostClick(evt)
			self.Close()
	
    def OnClose(self, evt):
	self.Destroy()

# end of class MyLoginDialog

class MySettingDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.sizer_12_staticbox = wx.StaticBox(self.notebook_1_pane_2, -1, _("Search Files"))
        self.sizer_11_staticbox = wx.StaticBox(self.notebook_1_pane_3, -1, _("Template to Post Article"))
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.label_1 = wx.StaticText(self.notebook_1_pane_1, -1, _("Threads to Upload"))
        self.spin_ctrl_1 = wx.SpinCtrl(self.notebook_1_pane_1, -1, "", min=1, max=10)
        self.checkbox_1 = wx.CheckBox(self.notebook_1_pane_1, -1, _("Minimize to Tray"))
        self.label_2 = wx.StaticText(self.notebook_1_pane_2, -1, _("Size Range (KB)"))
        self.spin_ctrl_2 = wx.SpinCtrl(self.notebook_1_pane_2, -1, "", min=0, max=9999)
        self.label_3 = wx.StaticText(self.notebook_1_pane_2, -1, _("-"))
        self.spin_ctrl_3 = wx.SpinCtrl(self.notebook_1_pane_2, -1, "", min=0, max=9999)
        self.checkbox_2 = wx.CheckBox(self.notebook_1_pane_2, -1, _("Search for Subfolders"))
        self.checkbox_3 = wx.CheckBox(self.notebook_1_pane_2, -1, _("Alarm when file size (KB) is larger than"))
        self.spin_ctrl_4 = wx.SpinCtrl(self.notebook_1_pane_2, -1, "", min=0, max=9999)
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_1_pane_3, -1, "")
        self.label_6 = wx.StaticText(self.notebook_1_pane_3, -1, _("Description"))
        self.label_4 = wx.StaticText(self.notebook_1_pane_3, -1, _("Post-upload URL"))
        self.choice_1 = wx.Choice(self.notebook_1_pane_3, -1, choices=[])
        self.checkbox_4 = wx.CheckBox(self.notebook_1_pane_3, -1, _("Automatic Update"))
        self.button_1 = wx.Button(self, wx.ID_OK)
        self.button_2 = wx.Button(self, wx.ID_CANCEL)

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def __set_properties(self):
        self.SetTitle(_("Preferences"))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.StaticBoxSizer(self.sizer_11_staticbox, wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(self.sizer_12_staticbox, wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_5.Add(self.spin_ctrl_1, 0, wx.ALL, 5)
        sizer_4.Add(sizer_5, 1, wx.EXPAND|wx.ALL, 5)
        sizer_4.Add(self.checkbox_1, 0, wx.ALL, 5)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_3)
        sizer_7.Add(self.label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_7.Add(self.spin_ctrl_2, 0, wx.ALL, 5)
        sizer_7.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_7.Add(self.spin_ctrl_3, 0, wx.ALL, 5)
        sizer_12.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_12.Add(self.checkbox_2, 0, wx.ALL, 5)
        sizer_6.Add(sizer_12, 0, wx.EXPAND|wx.ALL, 5)
        sizer_13.Add(self.checkbox_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.spin_ctrl_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_6.Add(sizer_13, 0, wx.EXPAND, 0)
        self.notebook_1_pane_2.SetSizer(sizer_6)
        sizer_11.Add(self.text_ctrl_2, 0, wx.ALL|wx.EXPAND, 5)
        sizer_11.Add(self.label_6, 0, wx.ALL, 5)
        sizer_8.Add(sizer_11, 0, wx.EXPAND|wx.ALL, 5)
        sizer_9.Add(self.label_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_9.Add(self.choice_1, 0, wx.ALL, 5)
        sizer_8.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_8.Add(self.checkbox_4, 0, wx.ALL, 5)
        self.notebook_1_pane_3.SetSizer(sizer_8)
        self.notebook_1.AddPage(self.notebook_1_pane_1, _("General"))
        self.notebook_1.AddPage(self.notebook_1_pane_2, _("File Management"))
        self.notebook_1.AddPage(self.notebook_1_pane_3, _("Miscellaneous"))
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_2.Add(self.button_1, 0, wx.ALL, 5)
        sizer_2.Add(self.button_2, 0, wx.ALL, 5)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def OnClose(self, evt):
	self.Destroy()
	
# end of class MySettingDialog


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
        self.txtLink = wx.HyperlinkCtrl(self, -1, _('Visit Homepage'), HOMEPAGE)
        self.btnOK = wx.Button(self, wx.ID_OK)

        self.__set_properties()
        self.__do_layout()

	self.Bind(wx.EVT_CLOSE, self.OnClose)
	
    def __set_properties(self):
        self.SetTitle(_("About"))

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.imgLogo, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(self.txtAppName, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(self.txtInfo, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(wx.StaticLine(self), 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer.Add(self.txtLink, 0, wx.ALIGN_CENTRE_VERTICAL)
        subsizer.Add((20, 20), 1, wx.ALIGN_CENTRE_VERTICAL)
        subsizer.Add(self.btnOK, 0, wx.ALIGN_CENTRE_VERTICAL)
        sizer.Add(subsizer, 0, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        self.Centre()
		
    def OnClose(self, evt):
	self.Destroy()
	
# end of class MyAboutDialog
