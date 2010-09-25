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
        self.cmbHost = wx.Choice(self, -1, choices = BBS_HOSTS)
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
		wx.MessageBox(MSG_FILL_BLANKS, _('Login'), wx.ICON_EXCLAMATION)
		return
	opener = urllib2.build_opener(SmartRedirectHandler())  
	urllib2.install_opener(opener)  
	req = urllib2.Request('http://%s/bbs/login' % BBS_HOSTS[host], urllib.urlencode({'id': userid, 'pw': pwd}))  
	try:
		resp = urllib2.urlopen(req)  
	except urllib2.HTTPError, e:  
		wx.MessageBox('%s: %d' % (MSG_ERROR_CODE, e.code), MSG_NETWORK_ERROR, wx.ICON_ERROR) 
		return
	except:
		wx.MessageBox(MSG_NETWORK_ERROR, MSG_ERROR, wx.ICON_ERROR)
		return
	else:
		if resp.code != 302:			
			the_page = resp.read().decode('gb18030')
			head, body = get_html_info(the_page)
			wx.MessageBox(body, head, wx.ICON_EXCLAMATION)
			return
		else:
			cookie = ';'.join(resp.headers['set-cookie'].split(','))
			write_config('Login', {'UserID': userid, 'Password': pwd, 'Cookie': cookie, 'Host': host, 'AutoLogin': autologin})
			wx.MessageBox(_('Login OK. Prepare to upload files.'), _('Login'), wx.ICON_INFORMATION)
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
        self.notebook = wx.Notebook(self, -1, style=0)
        
        self.notebook_pane1 = wx.Panel(self.notebook, -1)
        self.label_1 = wx.StaticText(self.notebook_pane1, -1, _("Threads to Upload"))
        self.txtThreads = wx.SpinCtrl(self.notebook_pane1, -1, "", min=1, max=10)
        self.chkTray = wx.CheckBox(self.notebook_pane1, -1, _("Minimize to Tray"))
        
        self.notebook_pane2 = wx.Panel(self.notebook, -1)
        self.staticbox1 = wx.StaticBox(self.notebook_pane2, -1, _("Search Files"))
        self.label_2 = wx.StaticText(self.notebook_pane2, -1, '%s (KB)' % _("Range of Size"))
        self.txtMinFileSize = wx.SpinCtrl(self.notebook_pane2, -1, "", size = wx.Size(100, wx.DefaultSize.y), min=0, max=9999)
        self.label_3 = wx.StaticText(self.notebook_pane2, -1, "-")
        self.txtMaxFileSize = wx.SpinCtrl(self.notebook_pane2, -1, "", size = wx.Size(100, wx.DefaultSize.y), min=0, max=9999)
        self.chkSubFolder = wx.CheckBox(self.notebook_pane2, -1, _("Search for Subfolders"))
        self.chkHighlight = wx.CheckBox(self.notebook_pane2, -1, '%s (KB)' % _("Highlight when file size is larger than"))
        self.txtFileNoLarger = wx.SpinCtrl(self.notebook_pane2, -1, "", size = wx.Size(100, wx.DefaultSize.y), min=0, max=9999)
        
        self.notebook_pane3 = wx.Panel(self.notebook, -1)
        self.staticbox2 = wx.StaticBox(self.notebook_pane3, -1, _("Template to Post Article"))
        self.label_4 = wx.StaticText(self.notebook_pane3, -1, _("Title"))
        self.txtTitleTemplate = wx.TextCtrl(self.notebook_pane3, -1, "")
        self.label_5 = wx.StaticText(self.notebook_pane3, -1, _("Content"))
        self.txtTemplate = wx.TextCtrl(self.notebook_pane3, -1, "")
        self.lblNote = wx.StaticText(self.notebook_pane3, -1, '%s:\n$TITLE (%s); $BODY (%s); \\n (%s)' % (_("Notes"), _('Title'), _('Content of article'), _('New line')))
        self.label_6 = wx.StaticText(self.notebook_pane3, -1, _("Post-upload URL"))
        self.cmbFileURL = wx.Choice(self.notebook_pane3, -1, choices = BBS_HOSTS)
        self.chkAutoUpdate = wx.CheckBox(self.notebook_pane3, -1, _("Automatic Update"))
        
        self.btnOK = wx.Button(self, wx.ID_OK, _("OK"))
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_CHECKBOX, self.OnchkHighlightClick, self.chkHighlight)
        self.Bind(wx.EVT_BUTTON, self.OnbtnOKClick, self.btnOK)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def __set_properties(self):
        self.SetTitle(_("Preferences"))
        self.txtThreads.SetValue(read_config_int('General', 'Threads', 3))
        self.chkTray.SetValue(read_config_bool('General', 'MinimizeToTray', False))
    	self.txtMinFileSize.SetValue(read_config_int('General', 'MinFileSize', 0))
    	self.txtMaxFileSize.SetValue(read_config_int('General', 'MaxFileSize', 1024))
    	self.chkSubFolder.SetValue(read_config_bool('General', 'SubFolder', False))
    	self.chkHighlight.SetValue(read_config_bool('General', 'Highlight', True))
    	self.txtFileNoLarger.SetValue(read_config_int('General', 'FileNoLarger', 1024))
    	evt = wx.CommandEvent()
    	self.OnchkHighlightClick(evt)
    	self.txtTitleTemplate.SetValue(read_config('General', 'TitleTemplate', ''))
    	self.txtTemplate.SetValue(read_config('General', 'Template', ''))
    	self.cmbFileURL.SetSelection(read_config_int('General', 'FileURL', 0))
    	self.chkAutoUpdate.SetValue(read_config_bool('General', 'AutoUpdate', True))
    			
    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.StaticBoxSizer(self.staticbox2, wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(self.staticbox1, wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_5.Add(self.txtThreads, 0, wx.ALL, 5)
        sizer_4.Add(sizer_5, 1, wx.EXPAND|wx.ALL, 5)
        sizer_4.Add(self.chkTray, 0, wx.ALL, 5)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        self.notebook_pane1.SetSizer(sizer_3)
        sizer_7.Add(self.label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_7.Add(self.txtMinFileSize, 0, wx.ALL, 5)
        sizer_7.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_7.Add(self.txtMaxFileSize, 0, wx.ALL, 5)
        sizer_12.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_12.Add(self.chkSubFolder, 0, wx.ALL, 5)
        sizer_6.Add(sizer_12, 0, wx.EXPAND|wx.ALL, 5)
        sizer_13.Add(self.chkHighlight, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.txtFileNoLarger, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_6.Add(sizer_13, 0, wx.EXPAND, 0)
        self.notebook_pane2.SetSizer(sizer_6)
        mysizer = wx.BoxSizer(wx.HORIZONTAL)
        mysizer.Add(self.label_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        mysizer.Add(self.txtTitleTemplate, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5)
        sizer_11.Add(mysizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 0)
        mysizer2 = wx.BoxSizer(wx.HORIZONTAL)
        mysizer2.Add(self.label_5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        mysizer2.Add(self.txtTemplate, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5)
        sizer_11.Add(mysizer2, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 0)
        sizer_11.Add(self.lblNote, 0, wx.ALL, 5)
        sizer_8.Add(sizer_11, 0, wx.EXPAND|wx.ALL, 5)
        sizer_9.Add(self.label_6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_9.Add(self.cmbFileURL, 0, wx.ALL, 5)
        sizer_8.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_8.Add(self.chkAutoUpdate, 0, wx.ALL, 5)
        self.notebook_pane3.SetSizer(sizer_8)
        self.notebook.AddPage(self.notebook_pane1, _("General"))
        self.notebook.AddPage(self.notebook_pane2, _("File Management"))
        self.notebook.AddPage(self.notebook_pane3, _("Miscellaneous"))
        sizer_1.Add(self.notebook, 1, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_2.Add(self.btnOK, 0, wx.ALL, 5)
        sizer_2.Add(self.btnCancel, 0, wx.ALL, 5)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        self.Centre()
        
    def OnchkHighlightClick(self, evt):
    	if self.chkHighlight.IsChecked():
    		self.txtFileNoLarger.Enable()
    	else:
    		self.txtFileNoLarger.Enable(False)
    
    def OnbtnOKClick(self, evt):
	try:
    		write_config('General', 
    			{'Threads': self.txtThreads.GetValue(), \
    			'MinimizeToTray': self.chkTray.IsChecked(), \
    			'MinFileSize': self.txtMinFileSize.GetValue(), \
    			'MaxFileSize': self.txtMaxFileSize.GetValue(), \
    			'SubFolder': self.chkSubFolder.IsChecked(), \
    			'Highlight': self.chkHighlight.IsChecked(), \
    			'FileNoLarger': self.txtFileNoLarger.GetValue(), \
    			'TitleTemplate': self.txtTitleTemplate.GetValue(), \
    			'Template': self.txtTemplate.GetValue(), \
    			'FileURL': self.cmbFileURL.GetSelection(), \
    			'AutoUpdate': self.chkAutoUpdate.IsChecked(), \
    			})
    	except:
    		wx.MessageBox(MSG_SAVE_SETTINGS_ERROR, MSG_ERROR, wx.ICON_ERROR)
    	self.Close()
    		
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
        self.btnOK = wx.Button(self, wx.ID_OK, _("OK"))

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
