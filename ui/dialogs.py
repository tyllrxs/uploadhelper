# -*- coding: utf-8 -*-

import os, sys
import urllib, urllib2, cookielib
import wx
from consts import *
from utilfunc import *
from httpredirect import *
from imagemanipulation import *

class MyLoginDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        self.imgTitle = wx.StaticBitmap(self, -1, wx.Bitmap("icon/title.png"))
        self.label_1 = wx.StaticText(self, -1, _("BBS host"), style=wx.ALIGN_CENTRE)
        self.cmbHost = wx.Choice(self, -1, choices = BBS_HOSTS)
        self.label_2 = wx.StaticText(self, -1, _("User"), style=wx.ALIGN_CENTRE)
        self.txtUser = wx.TextCtrl(self, -1, "")
        self.lnkRegister = wx.HyperlinkCtrl(self, -1, _("Register"), 'http://bbs.fudan.edu.cn/reg.htm')
        self.label_3 = wx.StaticText(self, -1, _("Password"), style=wx.ALIGN_CENTRE)
        self.txtPwd = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.chkRememberPwd = wx.CheckBox(self, -1, _("Remember"))
        self.chkProxy = wx.CheckBox(self, -1, _("Use proxy"))
        self.proxy_staticbox = wx.StaticBox(self, -1, _("Proxy Settings"))
        self.label_4 = wx.StaticText(self, -1, _("Host"))
        self.txtProxyHost = wx.TextCtrl(self, -1, "")
        self.label_5 = wx.StaticText(self, -1, _("Port"))
        self.txtProxyPort = wx.TextCtrl(self, -1, "")
        self.label_6 = wx.StaticText(self, -1, _("Username"))
        self.txtProxyUser = wx.TextCtrl(self, -1, "")
        self.label_7 = wx.StaticText(self, -1, _("Password"))
        self.txtProxyPwd = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.chkAutoLogin = wx.CheckBox(self, -1, _("Auto Login"))
        self.btnLogin = wx.Button(self, -1, _("Login"))
        
        self.__set_properties()
        self.__do_layout()
        
        self.OnchkProxyClick(wx.CommandEvent())
        
        self.Bind(wx.EVT_CHECKBOX, self.OnchkProxyClick, self.chkProxy)
	self.Bind(wx.EVT_BUTTON, self.OnbtnLoginClick, self.btnLogin)
	self.Bind(wx.EVT_CLOSE, self.OnClose)
	
    def __set_properties(self):
        self.SetTitle(_("Login"))
        self.cmbHost.SetSelection(read_config_int('Login', 'Host', 0))
        self.txtUser.SetValue(read_config('Login', 'UserID'))
	self.txtPwd.SetValue(read_config('Login', 'Password'))
	self.chkRememberPwd.SetValue(read_config_bool('Login', 'RememberPassword', True))
	self.chkProxy.SetValue(read_config_bool('Login', 'Proxy', False))
	self.txtProxyHost.SetValue(read_config('Login', 'ProxyHost'))
	self.txtProxyPort.SetValue(read_config('Login', 'ProxyPort'))
	self.txtProxyUser.SetValue(read_config('Login', 'ProxyUser'))
	self.txtProxyPwd.SetValue(read_config('Login', 'ProxyPwd'))
	self.chkAutoLogin.SetValue(read_config_bool('Login', 'AutoLogin', True))
	self.btnLogin.SetDefault()

    def __do_layout(self):
        object_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(3, 3, 0, 0)
        object_2 = wx.StaticBoxSizer(self.proxy_staticbox, wx.VERTICAL)
        object_5 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(2, 4, 0, 0)
        
        object_1.Add(self.imgTitle, 0, wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        grid_sizer_1.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.cmbHost, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add((20, 20), 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        
        grid_sizer_1.Add(self.label_2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.txtUser, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.lnkRegister, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
	
	
        grid_sizer_1.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.txtPwd, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.chkRememberPwd, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        grid_sizer_1.AddGrowableCol(1)
        object_1.Add(grid_sizer_1, 0, wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
	
	object_1.Add(self.chkProxy, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.label_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.txtProxyHost, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.label_5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.txtProxyPort, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.label_6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.txtProxyUser, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.label_7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.Add(self.txtProxyPwd, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_2.AddGrowableCol(1)
	grid_sizer_2.AddGrowableCol(3)
	object_2.Add(grid_sizer_2, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
	object_1.Add(object_2, 0, wx.ALL|wx.EXPAND|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
	
        object_5.Add((20, 20), 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        object_5.Add(self.btnLogin, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_5.Add(self.chkAutoLogin, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        object_1.Add(object_5, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.SetSizer(object_1)
        object_1.Fit(self)
        self.Layout()
        self.Centre()
        
    def OnchkProxyClick(self, evt):
    	if self.chkProxy.IsChecked():
    		self.GetSizer().Show(3)
    	else:
    		self.GetSizer().Hide(3)
    	self.Fit()
    	self.Layout()

    def OnbtnLoginClick(self, evt):
	host = self.cmbHost.GetSelection()
	userid = self.txtUser.GetValue().strip()
	pwd = self.txtPwd.GetValue().strip()
	autologin = self.chkAutoLogin.IsChecked()
	rememberpwd = self.chkRememberPwd.IsChecked()
	useproxy = self.chkProxy.IsChecked()
	p_host = self.txtProxyHost.GetValue()
	p_port = self.txtProxyPort.GetValue()
	p_user = self.txtProxyUser.GetValue()
	p_pwd = self.txtProxyPwd.GetValue()
	if userid == '' or pwd == '':
		wx.MessageBox(MSG_FILL_BLANKS, _('Login'), wx.ICON_EXCLAMATION)
		return
	if useproxy:
		proxy = 'http://%s:%s@%s:%s' % (p_user, p_pwd, p_host, p_port)
		opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}), SmartRedirectHandler())
	else:
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
			write_config('Login', \
				{'UserID': userid, \
				'Cookie': cookie, \
				'Host': host, \
				'AutoLogin': autologin, \
				'RememberPassword': rememberpwd, \
    		      		'Proxy': useproxy, \
    		      		'ProxyHost': p_host, \
    		      		'ProxyPort': p_port, \
    		      		'ProxyUser': p_user, \
    		      		'ProxyPwd': p_pwd, \
				})
			if rememberpwd:
				write_config('Login', {'Password': pwd})
			else:
				remove_config('Login', 'Password')
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
        self.staticbox3 = wx.StaticBox(self.notebook_pane1, -1, _("Upload"))
        self.label_1 = wx.StaticText(self.notebook_pane1, -1, _("Threads to Upload"))
        self.txtThreads = wx.SpinCtrl(self.notebook_pane1, -1, "", min=1, max=10)
        self.staticbox4 = wx.StaticBox(self.notebook_pane1, -1, _("Display and Layout"))
        self.label_6 = wx.StaticText(self.notebook_pane1, -1, _("Post-upload URL"))
        self.cmbFileURL = wx.Choice(self.notebook_pane1, -1, choices = BBS_HOSTS)
        self.label_7 = wx.StaticText(self.notebook_pane1, -1, _("Empty Lines between URLs"))
        self.txtEmptyLines = wx.SpinCtrl(self.notebook_pane1, -1, "", min=0, max=20)
        self.chkLogoutOnExit = wx.CheckBox(self.notebook_pane1, -1, _("Logout on exit"))
        self.chkTray = wx.CheckBox(self.notebook_pane1, -1, _("Minimize to Tray"))
        
        self.notebook_pane2 = wx.Panel(self.notebook, -1)
        self.staticbox1 = wx.StaticBox(self.notebook_pane2, -1, _("Search Files"))
        self.label_2 = wx.StaticText(self.notebook_pane2, -1, '%s (KB)' % _("Range of Size"))
        self.txtMinFileSize = wx.SpinCtrl(self.notebook_pane2, -1, "", size=(100, -1), min=0, max=9999)
        self.label_3 = wx.StaticText(self.notebook_pane2, -1, "-")
        self.txtMaxFileSize = wx.SpinCtrl(self.notebook_pane2, -1, "", size=(100, -1), min=0, max=9999)
        self.chkSubFolder = wx.CheckBox(self.notebook_pane2, -1, _("Search for Subfolders"))
        self.chkHighlight = wx.CheckBox(self.notebook_pane2, -1, '%s (KB)' % _("Highlight when file size is larger than"))
        self.txtFileNoLarger = wx.SpinCtrl(self.notebook_pane2, -1, "", size=(100, -1), min=0, max=9999)
        self.chkPreviewImage = wx.CheckBox(self.notebook_pane2, -1, "%s (%s)" % (_("Preview images"), _("Require restarting")))
        
        self.notebook_pane3 = wx.Panel(self.notebook, -1)
        self.staticbox2 = wx.StaticBox(self.notebook_pane3, -1, _("Template to Post Article"))
        self.label_4 = wx.StaticText(self.notebook_pane3, -1, _("Title"))
        self.txtTitleTemplate = wx.TextCtrl(self.notebook_pane3, -1, "")
        self.label_5 = wx.StaticText(self.notebook_pane3, -1, _("Content"))
        self.txtTemplate = wx.TextCtrl(self.notebook_pane3, -1, "")
        self.lblNote = wx.StaticText(self.notebook_pane3, -1, '%s:\n$TITLE (%s); $BODY (%s); \\n (%s)' % (_("Notes"), _('Title'), _('Content of article'), _('New line')))
        self.chkPreUploadClearArticle = wx.CheckBox(self.notebook_pane3, -1, _("Clear article before uploading"))
        self.chkPreUploadClearArticleTitle = wx.CheckBox(self.notebook_pane3, -1, _("Include title"))
        self.chkNoUpload = wx.CheckBox(self.notebook_pane3, -1, _("Image manipulation only, no uploading"))
        self.chkAutoUpdate = wx.CheckBox(self.notebook_pane3, -1, _("Automatic Update"))
        
        self.notebook_pane4 = wx.Panel(self.notebook, -1)
        self.chkProxy = wx.CheckBox(self.notebook_pane4, -1, _("Use proxy"))
        self.staticbox5 = wx.StaticBox(self.notebook_pane4, -1, _("Proxy Settings"))
        self.label_8 = wx.StaticText(self.notebook_pane4, -1, _("Host"))
        self.txtProxyHost = wx.TextCtrl(self.notebook_pane4, -1, "")
        self.label_9 = wx.StaticText(self.notebook_pane4, -1, _("Port"))
        self.txtProxyPort = wx.TextCtrl(self.notebook_pane4, -1, "")
        self.label_10 = wx.StaticText(self.notebook_pane4, -1, _("Username"))
        self.txtProxyUser = wx.TextCtrl(self.notebook_pane4, -1, "")
        self.label_11 = wx.StaticText(self.notebook_pane4, -1, _("Password"))
        self.txtProxyPwd = wx.TextCtrl(self.notebook_pane4, -1, "", style=wx.TE_PASSWORD)
        
        self.btnOK = wx.Button(self, wx.ID_OK, _("OK"))
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_CHECKBOX, self.OnchkHighlightClick, self.chkHighlight)
        self.Bind(wx.EVT_CHECKBOX, self.OnchkPreUploadClearArticleClick, self.chkPreUploadClearArticle)
        self.Bind(wx.EVT_BUTTON, self.OnbtnOKClick, self.btnOK)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def __set_properties(self):
        self.SetTitle(_("Preferences"))
        self.txtThreads.SetValue(read_config_int('General', 'Threads', 3))
        self.chkLogoutOnExit.SetValue(read_config_bool('General', 'LogoutOnExit', False))
        self.chkTray.SetValue(read_config_bool('General', 'MinimizeToTray', False))
    	self.txtMinFileSize.SetValue(read_config_int('General', 'MinFileSize', 0))
    	self.txtMaxFileSize.SetValue(read_config_int('General', 'MaxFileSize', 1024))
    	self.chkSubFolder.SetValue(read_config_bool('General', 'SubFolder', False))
    	self.chkHighlight.SetValue(read_config_bool('General', 'Highlight', True))
    	self.txtFileNoLarger.SetValue(read_config_int('General', 'FileNoLarger', 1024))
    	evt = wx.CommandEvent()
    	self.OnchkHighlightClick(evt)
    	self.chkPreviewImage.SetValue(read_config_bool('General', 'PreviewImage', True))
    	self.txtTitleTemplate.SetValue(read_config('General', 'TitleTemplate', '').decode('unicode_escape'))
    	self.txtTemplate.SetValue(read_config('General', 'Template', '').decode('unicode_escape'))
    	self.cmbFileURL.SetSelection(read_config_int('General', 'FileURL', 0))
    	self.txtEmptyLines.SetValue(read_config_int('General', 'EmptyLines', 1))
    	self.chkPreUploadClearArticle.SetValue(read_config_bool('General', 'PreUploadClearArticle', False))
    	self.chkPreUploadClearArticleTitle.SetValue(read_config_bool('General', 'PreUploadClearArticleTitle', False))
    	self.OnchkPreUploadClearArticleClick(evt)
    	self.chkNoUpload.SetValue(read_config_bool('General', 'NoUpload', False))
    	self.chkAutoUpdate.SetValue(read_config_bool('General', 'AutoUpdate', True))
    	self.chkProxy.SetValue(read_config_bool('Login', 'Proxy', False))
	self.txtProxyHost.SetValue(read_config('Login', 'ProxyHost'))
	self.txtProxyPort.SetValue(read_config('Login', 'ProxyPort'))
	self.txtProxyUser.SetValue(read_config('Login', 'ProxyUser'))
	self.txtProxyPwd.SetValue(read_config('Login', 'ProxyPwd'))
    			
    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.StaticBoxSizer(self.staticbox2, wx.VERTICAL)
        sizer_14 = wx.StaticBoxSizer(self.staticbox3, wx.VERTICAL)
        sizer_15 = wx.StaticBoxSizer(self.staticbox4, wx.VERTICAL)
        sizer_19 = wx.StaticBoxSizer(self.staticbox5, wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(self.staticbox1, wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 4, 0, 0)
        
        sizer_5.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_5.Add(self.txtThreads, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_14.Add(sizer_5, 0, wx.ALL, 0)
        sizer_4.Add(sizer_14, 0, wx.EXPAND|wx.ALL, 5)
        sizer_9.Add(self.label_6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_9.Add(self.cmbFileURL, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_15.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_16.Add(self.label_7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_16.Add(self.txtEmptyLines, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_15.Add(sizer_16, 0, wx.EXPAND, 0)
        sizer_4.Add(sizer_15, 0, wx.EXPAND|wx.ALL, 5)
        sizer_4.Add(self.chkLogoutOnExit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_4.Add(self.chkTray, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
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
        sizer_6.Add(self.chkPreviewImage, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
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
        sizer_17.Add(self.chkPreUploadClearArticle, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_17.Add(self.chkPreUploadClearArticleTitle, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(sizer_17, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 0)
        sizer_8.Add(self.chkNoUpload, 0, wx.ALL, 5)
        sizer_8.Add(self.chkAutoUpdate, 0, wx.ALL, 5)
        self.notebook_pane3.SetSizer(sizer_8)
        
        sizer_18.Add(self.chkProxy, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.label_8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.txtProxyHost, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.label_9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.txtProxyPort, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.label_10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.txtProxyUser, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.label_11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.Add(self.txtProxyPwd, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
	grid_sizer_1.AddGrowableCol(1)
	grid_sizer_1.AddGrowableCol(3)
	sizer_19.Add(grid_sizer_1, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
	sizer_18.Add(sizer_19, 0, wx.ALL|wx.EXPAND|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
	self.notebook_pane4.SetSizer(sizer_18)
        
        self.notebook.AddPage(self.notebook_pane1, _("General"))
        self.notebook.AddPage(self.notebook_pane2, _("File Management"))
        self.notebook.AddPage(self.notebook_pane4, _("Network Proxy"))
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
    	self.txtFileNoLarger.Enable(self.chkHighlight.IsChecked())
    
    def OnchkPreUploadClearArticleClick(self, evt):
    	self.chkPreUploadClearArticleTitle.Enable(self.chkPreUploadClearArticle.IsChecked())
    
    def OnbtnOKClick(self, evt):
	try:
    		write_config('General', 
    			{'Threads': self.txtThreads.GetValue(), \
    			'LogoutOnExit': self.chkLogoutOnExit.IsChecked(), \
    			'MinimizeToTray': self.chkTray.IsChecked(), \
    			'MinFileSize': self.txtMinFileSize.GetValue(), \
    			'MaxFileSize': self.txtMaxFileSize.GetValue(), \
    			'SubFolder': self.chkSubFolder.IsChecked(), \
    			'Highlight': self.chkHighlight.IsChecked(), \
    			'FileNoLarger': self.txtFileNoLarger.GetValue(), \
    			'PreviewImage': self.chkPreviewImage.IsChecked(), \
    			'TitleTemplate': self.txtTitleTemplate.GetValue().encode('unicode_escape'), \
    			'Template': self.txtTemplate.GetValue().encode('unicode_escape'), \
    			'FileURL': self.cmbFileURL.GetSelection(), \
    			'EmptyLines': self.txtEmptyLines.GetValue(), \
    			'PreUploadClearArticle': self.chkPreUploadClearArticle.GetValue(), \
    			'PreUploadClearArticleTitle': self.chkPreUploadClearArticleTitle.GetValue(), \
    			'NoUpload': self.chkNoUpload.IsChecked(), \
    			'AutoUpdate': self.chkAutoUpdate.IsChecked(), \
    			})
    		write_config('Login', 
			{'Proxy': self.chkProxy.IsChecked(), \
	      		'ProxyHost': self.txtProxyHost.GetValue(), \
	      		'ProxyPort': self.txtProxyPort.GetValue(), \
	      		'ProxyUser': self.txtProxyUser.GetValue(), \
	      		'ProxyPwd': self.txtProxyPwd.GetValue(), \
			})
    	except:
    		wx.MessageBox(MSG_SAVE_SETTINGS_ERROR, MSG_ERROR, wx.ICON_ERROR)
    	self.Close()
    		
    def OnClose(self, evt):
	self.Destroy()
	
# end of class MySettingDialog

class MyImageDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        self.notebook = wx.Listbook(self, -1, style = wx.LB_LEFT)
        self.notebook_pane_3 = wx.Panel(self.notebook, -1)
        self.notebook_pane_2 = wx.Panel(self.notebook, -1)
        self.notebook_pane_1 = wx.Panel(self.notebook, -1)
        
        self.chkResize = wx.CheckBox(self.notebook_pane_1, -1, _("Enable Resize for Large Images"))
        self.sizer_17_staticbox = wx.StaticBox(self.notebook_pane_1, -1, _("Resize Settings"))
        self.label_18 = wx.StaticText(self.notebook_pane_1, -1, _("Resize To"))
        self.txtResizeWidth = wx.SpinCtrl(self.notebook_pane_1, -1, "", size=(100, -1), min=0, max=9999)
        self.label_19 = wx.StaticText(self.notebook_pane_1, -1, "X")
        self.txtResizeHeight = wx.SpinCtrl(self.notebook_pane_1, -1, "", size=(100, -1), min=0, max=9999)
        self.chkResizeLarger = wx.CheckBox(self.notebook_pane_1, -1, '%s (KB) >' % _("Resize only for Image Size"))
        self.txtResizeLarger = wx.SpinCtrl(self.notebook_pane_1, -1, "", size=(100, -1), min=0, max=9999)
        self.label_22 = wx.StaticText(self.notebook_pane_1, -1, _("Resizing quality"))
        self.cmbResizeQuality = wx.Choice(self.notebook_pane_1, -1, choices=[_("Very fast"), _("Fast"), _("High quality"), _("Very high quality")])
        
        self.chkEXIF = wx.CheckBox(self.notebook_pane_2, -1, _("Enable EXIF Editing for JPEG"))
        self.chkPreserveEXIF = wx.CheckBox(self.notebook_pane_2, -1, _("Preserve original EXIF"))
        self.sizer_16_staticbox = wx.StaticBox(self.notebook_pane_2, -1, _("EXIF Settings"))
        self.txtEXIFInfo = []
        for item, desc in EXIF_TAGS:
        	lbl = wx.StaticText(self.notebook_pane_2, -1, desc)
        	txt = wx.TextCtrl(self.notebook_pane_2, -1, "", size=(160, -1))
        	chk1 = wx.CheckBox(self.notebook_pane_2, -1, 'r')
        	chk2 = wx.CheckBox(self.notebook_pane_2, -1, 'w')
        	self.txtEXIFInfo.append((lbl, txt, chk1, chk2))
        self.lblEXIFThumbnail = wx.StaticText(self.notebook_pane_2, -1, _("Thumbnail"))
        self.imgEXIFThumbnail = wx.StaticBitmap(self.notebook_pane_2, -1, size=(160, 120))
        self.chkThumbR = wx.CheckBox(self.notebook_pane_2, -1, 'r')
        self.chkThumbW = wx.CheckBox(self.notebook_pane_2, -1, 'w')
        self.btnChangeThumbnail = wx.Button(self.notebook_pane_2, -1, _("Change"))
        self.btnRemoveThumbnail = wx.Button(self.notebook_pane_2, -1, _("Remove"))
        self.chkAllReadable = wx.CheckBox(self.notebook_pane_2, -1, _("All Readable"))
        self.chkAllWritable = wx.CheckBox(self.notebook_pane_2, -1, _("All Writable"))
        self.btnClearAll = wx.Button(self.notebook_pane_2, -1, _("Clear All"))
        self.btnImportEXIF = wx.Button(self.notebook_pane_2, -1, '%s...' % _("Import EXIF from Image"))
        self.btnWriteEXIF = wx.Button(self.notebook_pane_2, -1, '%s...' % _("Write EXIF manually"))
        self.chkWriteEXIFBackup = wx.CheckBox(self.notebook_pane_2, -1, _("Backup"))
        self.chkWriteEXIFUnicode = wx.CheckBox(self.notebook_pane_2, -1, _("Use unicode"))
        
        self.chkWatermark = wx.CheckBox(self.notebook_pane_3, -1, _("Enable Watermark"))
        self.sizer_WatermarkText_staticbox = wx.StaticBox(self.notebook_pane_3, -1, _("Watermark Text"))
        self.sizer_WatermarkImage_staticbox = wx.StaticBox(self.notebook_pane_3, -1, _("Watermark Image"))
        self.sizer_Watermark_Setting_staticbox = wx.StaticBox(self.notebook_pane_3, -1, _("Watermark Settings"))
        self.sizer_Watermark_Preview_staticbox = wx.StaticBox(self.notebook_pane_3, -1, _("Preview"))
        self.rdWatermarkType = wx.RadioBox(self.notebook_pane_3, -1, _("Watermark Type"), choices=[_("Text"), _("Image")], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.label_3 = wx.StaticText(self.notebook_pane_3, -1, _("Text"))
        self.txtWatermarkText = wx.TextCtrl(self.notebook_pane_3, -1, "")
        self.label_4 = wx.StaticText(self.notebook_pane_3, -1, _("Font"))
        self.cmbWatermarkTextFont = wx.Choice(self.notebook_pane_3, -1)
        self.txtWatermarkTextFont = wx.TextCtrl(self.notebook_pane_3, -1, '')
        self.btnWatermarkTextFont = wx.Button(self.notebook_pane_3, -1, '%s...' % _("Browse"))
        self.label_21 = wx.StaticText(self.notebook_pane_3, -1, _("Size"))
        self.txtWatermarkTextSize = wx.SpinCtrl(self.notebook_pane_3, -1, "", min=0, max=200)
        self.label_20 = wx.StaticText(self.notebook_pane_3, -1, _("Color"))
        self.btnWatermarkTextColor = wx.Button(self.notebook_pane_3, -1, '')
        self.label_6 = wx.StaticText(self.notebook_pane_3, -1, _("Position"))
        self.cmbWatermarkTextPosition = wx.Choice(self.notebook_pane_3, -1, choices=MARK_POSITIONS)
        self.label_7 = wx.StaticText(self.notebook_pane_3, -1, _("Padding"))
        self.txtWatermarkTextPadding = wx.SpinCtrl(self.notebook_pane_3, -1, "", min=0, max=100)
        self.label_8 = wx.StaticText(self.notebook_pane_3, -1, _("Image"))
        self.txtWatermarkImage = wx.TextCtrl(self.notebook_pane_3, -1, "")
        self.btnWatermarkImage = wx.Button(self.notebook_pane_3, -1, '%s...' % _("Browse"))
        self.label_9_copy = wx.StaticText(self.notebook_pane_3, -1, _("Opacity"))
        self.sldWatermarkImageOpacity = wx.Slider(self.notebook_pane_3, -1, 0, 0, 100, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.label_6_copy = wx.StaticText(self.notebook_pane_3, -1, _("Position"))
        self.cmbWatermarkImagePosition = wx.Choice(self.notebook_pane_3, -1, choices=MARK_POSITIONS)
        self.label_7_copy = wx.StaticText(self.notebook_pane_3, -1, _("Padding"))
        self.txtWatermarkImagePadding = wx.SpinCtrl(self.notebook_pane_3, -1, "", min=0, max=100)
        self.lblOriginal = wx.StaticText(self.notebook_pane_3, -1, _("Original"))
        self.imgOriginal = wx.StaticBitmap(self.notebook_pane_3, -1, wx.Bitmap(SAMPLE_IMAGE))
        self.lblEffect = wx.StaticText(self.notebook_pane_3, -1, _("Effect"))
        self.imgEffect = wx.StaticBitmap(self.notebook_pane_3, -1, wx.Bitmap(SAMPLE_IMAGE))
        self.btnOK = wx.Button(self, wx.ID_OK, _("OK"))
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
	
        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_CHECKBOX, self.OnchkResizeLargerClick, self.chkResizeLarger)
        
        self.Bind(wx.EVT_BUTTON, self.OnbtnChangeThumbnailClick, self.btnChangeThumbnail)
        self.Bind(wx.EVT_BUTTON, self.OnbtnRemoveThumbnailClick, self.btnRemoveThumbnail)
        self.Bind(wx.EVT_CHECKBOX, self.OnchkAllReadableClick, self.chkAllReadable)
        self.Bind(wx.EVT_CHECKBOX, self.OnchkAllWritableClick, self.chkAllWritable)
        self.Bind(wx.EVT_BUTTON, self.OnbtnClearAllClick, self.btnClearAll)
        self.Bind(wx.EVT_BUTTON, self.OnbtnImportEXIFClick, self.btnImportEXIF)
        self.Bind(wx.EVT_BUTTON, self.OnbtnWriteEXIFClick, self.btnWriteEXIF)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnchkWatermarkClick, self.chkWatermark)
        self.Bind(wx.EVT_RADIOBOX, self.add_watermark, self.rdWatermarkType)
        self.Bind(wx.EVT_TEXT, self.add_watermark, self.txtWatermarkText)
        self.Bind(wx.EVT_CHOICE, self.OncmbWatermarkTextFontChange, self.cmbWatermarkTextFont)
        self.Bind(wx.EVT_TEXT, self.add_watermark, self.txtWatermarkTextFont)
        self.Bind(wx.EVT_SPINCTRL, self.add_watermark, self.txtWatermarkTextSize)
        self.Bind(wx.EVT_CHOICE, self.add_watermark, self.cmbWatermarkTextPosition)
        self.Bind(wx.EVT_SPINCTRL, self.add_watermark, self.txtWatermarkTextPadding)
        self.Bind(wx.EVT_TEXT, self.add_watermark, self.txtWatermarkImage)
        self.Bind(wx.EVT_SCROLL, self.add_watermark, self.sldWatermarkImageOpacity)
        self.Bind(wx.EVT_CHOICE, self.add_watermark, self.cmbWatermarkImagePosition)
        self.Bind(wx.EVT_SPINCTRL, self.add_watermark, self.txtWatermarkImagePadding)
        self.Bind(wx.EVT_BUTTON, self.OnbtnWatermarkTextFontClick, self.btnWatermarkTextFont)
        self.Bind(wx.EVT_BUTTON, self.OnbtnWatermarkTextColorClick, self.btnWatermarkTextColor)
        self.Bind(wx.EVT_BUTTON, self.OnbtnWatermarkImageClick, self.btnWatermarkImage)
        
        self.Bind(wx.EVT_BUTTON, self.OnbtnOKClick, id = wx.ID_OK)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def __set_properties(self):
        self.SetTitle(_("Image Manipulation"))
        self.default_path = ''
        self.chkResize.SetValue(read_config_bool('Resize', 'Resize', True))
        self.txtResizeWidth.SetValue(read_config_int('Resize', 'ResizeWidth', 1000))
        self.txtResizeHeight.SetValue(read_config_int('Resize', 'ResizeHeight', 800))
        self.chkResizeLarger.SetValue(read_config_bool('Resize', 'ResizeLarger', True))
        self.txtResizeLarger.SetValue(read_config_int('Resize', 'ResizeLargerThan', 1024))
        evt = wx.CommandEvent()
        self.OnchkResizeLargerClick(evt)
        self.cmbResizeQuality.SetSelection(read_config_int('Resize', 'ResizeQuality', 0))
        
        self.chkEXIF.SetValue(read_config_bool('EXIF', 'EXIF', False))
        self.chkPreserveEXIF.SetValue(read_config_bool('EXIF', 'PreserveEXIF', False))
        tmp = read_config('EXIF', 'EXIFInfoCheck', '')
        tmp_list = tmp.split(',')
        for i in xrange(len(self.txtEXIFInfo)):
		self.txtEXIFInfo[i][1].SetValue(read_config('EXIF', 'EXIFInfo%02d' % i).decode('unicode_escape'))
		try:
			num = int(tmp_list[i])
		except:
			num = 7
		if 4 & num:
			self.txtEXIFInfo[i][2].SetValue(True)
		if 2 & num:
			self.txtEXIFInfo[i][3].SetValue(True)
	self.thumbnail = read_config('EXIF', 'EXIFThumbnail', '').decode('unicode_escape')
	self.set_thumbnail(self.thumbnail)
	self.chkThumbR.SetValue(read_config_bool('EXIF', 'ThumbR', True))
	self.chkThumbW.SetValue(read_config_bool('EXIF', 'ThumbW', True))
	self.chkWriteEXIFBackup.SetValue(read_config_bool('EXIF', 'WriteEXIFBackup', True))
	self.chkWriteEXIFUnicode.SetValue(read_config_bool('EXIF', 'WriteEXIFUnicode', False))
	
	self.chkWatermark.SetValue(read_config_bool('Watermark', 'Watermark', False))
	self.rdWatermarkType.SetSelection(read_config_int('Watermark', 'WatermarkType', 0))
	self.txtWatermarkText.SetValue(read_config('Watermark', 'WatermarkText', 'This is a watermark').decode('unicode_escape'))
	for k, v in PREDEFINE_FONTS:
		self.cmbWatermarkTextFont.Append(k)
	self.cmbWatermarkTextFont.SetSelection(read_config_int('Watermark', 'WatermarkTextPreFont', 0))
	if not sys.platform.startswith('win32'):
		self.cmbWatermarkTextFont.Hide()
	self.txtWatermarkTextFont.SetValue(read_config('Watermark', 'WatermarkTextFont', '').decode('unicode_escape'))
	if not self.txtWatermarkTextFont.GetValue():
		self.OncmbWatermarkTextFontChange(wx.CommandEvent())
	self.txtWatermarkTextSize.SetValue(read_config_int('Watermark', 'WatermarkTextSize', 24))
	try:
		mycolor = read_config('Watermark', 'WatermarkTextColor', '')
		r, g, b = [int(item) for item in mycolor[1: -1].split(',')]
	except:
		r, g, b = [0, 0, 0]
	self.btnWatermarkTextColor.SetBackgroundColour(wx.Colour(r, g, b))
	self.btnWatermarkTextColor.SetLabel(wx.Colour(r, g, b).GetAsString(wx.C2S_HTML_SYNTAX))
	self.cmbWatermarkTextPosition.SetSelection(read_config_int('Watermark', 'WatermarkTextPosition', 0))
	self.txtWatermarkTextPadding.SetValue(read_config_int('Watermark', 'WatermarkTextPadding', 10))
	self.txtWatermarkImage.SetValue(read_config('Watermark', 'WatermarkImage', '').decode('unicode_escape'))
	self.sldWatermarkImageOpacity.SetValue(read_config_int('Watermark', 'WatermarkImageOpacity', 60))
	self.cmbWatermarkImagePosition.SetSelection(read_config_int('Watermark', 'WatermarkImagePosition', 0))
	self.txtWatermarkImagePadding.SetValue(read_config_int('Watermark', 'WatermarkImagePadding', 10))
	self.add_watermark()

    def __do_layout(self):
        sizer_dialog = wx.BoxSizer(wx.VERTICAL)
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Resize = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Watermark = wx.BoxSizer(wx.VERTICAL)
        sizer_Watermark_Main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Watermark_Setting = wx.StaticBoxSizer(self.sizer_Watermark_Setting_staticbox, wx.VERTICAL)
        sizer_Watermark_Preview = wx.StaticBoxSizer(self.sizer_Watermark_Preview_staticbox, wx.VERTICAL)
        sizer_WatermarkImage = wx.StaticBoxSizer(self.sizer_WatermarkImage_staticbox, wx.VERTICAL)
        sizer_13_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20 = wx.BoxSizer(wx.VERTICAL)
        sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_23 = wx.BoxSizer(wx.VERTICAL)
        sizer_24 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_WatermarkText = wx.StaticBoxSizer(self.sizer_WatermarkText_staticbox, wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10_my = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_EXIF = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.StaticBoxSizer(self.sizer_16_staticbox, wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(5, 6, 0, 0)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.StaticBoxSizer(self.sizer_17_staticbox, wx.VERTICAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_7.Add(self.chkResize, 0, wx.ALL, 5)
        sizer_18.Add(self.label_18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_18.Add(self.txtResizeWidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_18.Add(self.label_19, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_18.Add(self.txtResizeHeight, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_17.Add(sizer_18, 0, wx.EXPAND, 0)
        sizer_19.Add(self.chkResizeLarger, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_19.Add(self.txtResizeLarger, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_17.Add(sizer_19, 0, wx.EXPAND, 0)
        sizer_25.Add(self.label_22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_25.Add(self.cmbResizeQuality, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_17.Add(sizer_25, 0, wx.EXPAND, 0)
        sizer_7.Add(sizer_17, 1, wx.EXPAND, 0)
        self.notebook_pane_1.SetSizer(sizer_7)
        
        sizer_24.Add(self.chkEXIF, 0, wx.ALL, 5)
        sizer_24.Add(self.chkPreserveEXIF, 0, wx.ALL, 5)
        sizer_EXIF.Add(sizer_24, 0, wx.ALL, 0)
        for label, text, check1, check2 in self.txtEXIFInfo:
        	grid_sizer_1.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        	grid_sizer_1.Add(text, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        	sizer_rw = wx.BoxSizer(wx.HORIZONTAL)
        	sizer_rw.Add(check1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        	sizer_rw.Add(check2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        	grid_sizer_1.Add(sizer_rw, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.lblEXIFThumbnail, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.imgEXIFThumbnail, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_22.Add(self.chkThumbR, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_22.Add(self.chkThumbW, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(sizer_22, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(self.btnChangeThumbnail, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(self.btnRemoveThumbnail, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(sizer_20, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_16.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_23.Add((20, 20), 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_23.Add(self.chkAllReadable, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_23.Add(self.chkAllWritable, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_23.Add(wx.StaticLine(self.notebook_pane_2), 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_23.Add(self.btnClearAll, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_23.Add((20, 20), 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_16.Add(sizer_23, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_EXIF.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_21.Add(self.btnImportEXIF, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_21.Add((20, 20), 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_21.Add(self.btnWriteEXIF, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_21.Add(self.chkWriteEXIFBackup, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_21.Add(self.chkWriteEXIFUnicode, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_EXIF.Add(sizer_21, 0, wx.EXPAND, 5)
        self.notebook_pane_2.SetSizer(sizer_EXIF)
        
        sizer_Watermark.Add(self.chkWatermark, 0, wx.ALL, 5)
        sizer_Watermark_Setting.Add(self.rdWatermarkType, 0, wx.EXPAND, 0)
        sizer_11.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_11.Add(self.txtWatermarkText, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_WatermarkText.Add(sizer_11, 0, wx.EXPAND, 0)
        sizer_10.Add(self.label_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.cmbWatermarkTextFont, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.txtWatermarkTextFont, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.btnWatermarkTextFont, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_WatermarkText.Add(sizer_10, 0, wx.EXPAND, 0)
	sizer_10_my.Add(self.label_21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10_my.Add(self.txtWatermarkTextSize, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10_my.Add(self.label_20, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10_my.Add(self.btnWatermarkTextColor, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_WatermarkText.Add(sizer_10_my, 0, wx.EXPAND, 0)
        sizer_13.Add(self.label_6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.cmbWatermarkTextPosition, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.label_7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.txtWatermarkTextPadding, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_WatermarkText.Add(sizer_13, 0, wx.EXPAND, 0)
        sizer_Watermark_Setting.Add(sizer_WatermarkText, 0, wx.EXPAND, 0)
        sizer_15.Add(self.label_8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_15.Add(self.txtWatermarkImage, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_15.Add(self.btnWatermarkImage, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_WatermarkImage.Add(sizer_15, 0, wx.EXPAND, 0)
        sizer_10_copy.Add(self.label_9_copy, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10_copy.Add(self.sldWatermarkImageOpacity, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_10_copy.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_WatermarkImage.Add(sizer_10_copy, 1, wx.EXPAND, 0)
        sizer_13_copy.Add(self.label_6_copy, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13_copy.Add(self.cmbWatermarkImagePosition, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13_copy.Add(self.label_7_copy, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13_copy.Add(self.txtWatermarkImagePadding, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_WatermarkImage.Add(sizer_13_copy, 1, wx.EXPAND, 0)
        sizer_Watermark_Setting.Add(sizer_WatermarkImage, 0, wx.EXPAND, 0)
        sizer_Watermark_Main.Add(sizer_Watermark_Setting, 1, wx.EXPAND, 0)
        sizer_Watermark_Preview.Add(self.lblOriginal, 0, wx.ALL, 5)
        sizer_Watermark_Preview.Add(self.imgOriginal, 0, 0, 0)
        sizer_Watermark_Preview.Add(self.lblEffect, 0, wx.ALL, 5)
        sizer_Watermark_Preview.Add(self.imgEffect, 0, 0, 0)
        sizer_Watermark_Main.Add(sizer_Watermark_Preview, 0, wx.EXPAND, 0)
        sizer_Watermark.Add(sizer_Watermark_Main, 1, wx.EXPAND, 0)
        self.notebook_pane_3.SetSizer(sizer_Watermark)
        
        self.notebook.AddPage(self.notebook_pane_1, _("Resize"))
        self.notebook.AddPage(self.notebook_pane_2, _("EXIF"))
        self.notebook.AddPage(self.notebook_pane_3, _("Watermark"))
	il = wx.ImageList(64, 64)
	imgs = ['resize.png', 'exif.png', 'watermark.png']
	self.notebook.AssignImageList(il)
	for page in xrange(self.notebook.GetPageCount()):
		img = il.Add(wx.Bitmap('icon/64/%s' % imgs[page]))
		self.notebook.SetPageImage(page, img)        
        sizer_Resize.Add(self.notebook, 1, wx.EXPAND, 0)
        sizer_dialog.Add(sizer_Resize, 1, wx.EXPAND, 0)
        sizer_button.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_button.Add(self.btnOK, 0, wx.ALL, 5)
        sizer_button.Add(self.btnCancel, 0, wx.ALL, 5)
        sizer_dialog.Add(sizer_button, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_dialog)
        
        sizer_dialog.Fit(self)
        self.Layout()
        self.Centre()
        
    def OnchkResizeLargerClick(self, evt):
    	self.txtResizeLarger.Enable(self.chkResizeLarger.IsChecked())
    	
    def set_thumbnail(self, thumb = ''):
    	if not (self.thumbnail or thumb):
    		return
    	self.thumbnail = thumb
	if thumb:
		self.imgEXIFThumbnail.SetBitmap(wx.Bitmap(thumb))
	else:
		self.imgEXIFThumbnail.SetBitmap(wx.EmptyBitmap(160, 120))
	self.imgEXIFThumbnail.Parent.Layout()

    def open_jpeg_dialog(self):
    	wildcard = '%s (*.jpg)|*.jpg' % 'JPEG %s' % _('Images')
	if sys.platform[:5] == 'linux':
		wildcard = '%s (*.jpg)|*.[Jj][Pp][Gg]' % 'JPEG %s' % _('Images')
	jpegfile = ''
	dialog = wx.FileDialog(None, _('Select an image'), self.default_path, '', wildcard, wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK:
		self.default_path = os.path.abspath(os.path.dirname(dialog.GetPath()))
		jpegfile = dialog.GetPath()
	dialog.Destroy()
	return jpegfile
		
    def OnbtnChangeThumbnailClick(self, evt):
    	jpeg = self.open_jpeg_dialog()
    	if jpeg:
		self.set_thumbnail(jpeg)	
    	
    def OnbtnRemoveThumbnailClick(self, evt):
    	self.set_thumbnail()
    	
    def OnchkAllReadableClick(self, evt):
    	checked = self.chkAllReadable.IsChecked()
    	for i in xrange(len(self.txtEXIFInfo)):
    		self.txtEXIFInfo[i][2].SetValue(checked)
    	self.chkThumbR.SetValue(checked)
    	
    def OnchkAllWritableClick(self, evt):
    	checked = self.chkAllWritable.IsChecked()
    	for i in xrange(len(self.txtEXIFInfo)):
    		self.txtEXIFInfo[i][3].SetValue(checked)
    	self.chkThumbW.SetValue(checked)
    	
    def OnbtnClearAllClick(self, evt):
    	for i in xrange(len(self.txtEXIFInfo)):
    		self.txtEXIFInfo[i][1].SetValue('')
    	self.set_thumbnail()
			
    def OnbtnImportEXIFClick(self, evt):
    	jpeg = self.open_jpeg_dialog()
    	if jpeg:
    		use_unicode = self.chkWriteEXIFUnicode.IsChecked()
		vals, has_thumb = get_exif_info(jpeg, [k for k, v in EXIF_TAGS], use_unicode)
		i = 0
		for val in vals:
			if self.txtEXIFInfo[i][2].IsChecked():
				try:
					self.txtEXIFInfo[i][1].SetValue(val)
				except:
					try:
						self.txtEXIFInfo[i][1].SetValue(val.decode('gb18030'))
					except:
						pass
			i += 1
		if self.chkThumbR.IsChecked():
			if has_thumb:
				thumb = get_exif_thumbnail(jpeg, use_unicode)
				self.set_thumbnail(thumb)
			else:
				self.set_thumbnail()
	
    def OnbtnWriteEXIFClick(self, evt):
    	jpg = self.open_jpeg_dialog()
    	if jpg:
    		dict = {}
    		for i in xrange(len(self.txtEXIFInfo)):
    			if self.txtEXIFInfo[i][3].IsChecked():
    				dict[EXIF_TAGS[i][0]] = self.txtEXIFInfo[i][1].GetValue()
    		if self.chkThumbW.IsChecked():
    			if self.thumbnail:
    				thumb = self.thumbnail
    			else:
    				thumb = '-'
    		else:
    			thumb = ''
    		backup = self.chkWriteEXIFBackup.IsChecked()
    		use_unicode = self.chkWriteEXIFUnicode.IsChecked()
    		exif_jpg = process_exif(jpg, dict, thumb, True, backup, use_unicode)
    		if exif_jpg:
    			wx.MessageBox('%s.' % _('Write successfully'), _('Write EXIF manually'), wx.ICON_INFORMATION)
    		else:
    			wx.MessageBox(_('Failed to write'), _('Write EXIF manually'), wx.ICON_ERROR)
    	
    def OnchkWatermarkClick(self, evt):
    	self.add_watermark()
    
    def OncmbWatermarkTextFontChange(self, evt):
    	if not sys.platform.startswith('win32'):
    		return
    	font_file = PREDEFINE_FONTS[self.cmbWatermarkTextFont.GetSelection()][1]
    	font_file = os.path.join(os.environ['WINDIR'], 'Fonts', font_file)
    	self.txtWatermarkTextFont.SetValue(font_file)
    
    def OnbtnWatermarkTextFontClick(self, evt):
    	wildcard = '%s (*.ttf;*.ttc;*.otf)|*.ttf;*.ttc;*.otf' % 'True Type/Open Type %s' % _('Fonts')
	if sys.platform[:5] == 'linux':
		wildcard = '%s (*.ttf;*.ttc;*.otf)|*.[Tt][Tt][Ff];*.[Tt][Tt][Cc];*.[Oo][Tt][Ff]' % 'True Type/Open Type %s' % _('Fonts')
	default_path = os.path.abspath(os.path.dirname(self.txtWatermarkTextFont.GetValue()))
	if default_path == os.path.abspath('.'):
		if sys.platform.startswith('win32'):
			default_path = os.path.join(os.environ['WINDIR'], 'Fonts')
		elif sys.platform.find('linux') >= 0:	
			default_path = '/usr/share/fonts'
		else:
			default_path = '/Library/Fonts'
	dialog = wx.FileDialog(None, _('Select a font for watermark'), default_path, '', wildcard, wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK:
		self.txtWatermarkTextFont.SetValue(dialog.GetPath())
	dialog.Destroy()
		
    def OnbtnWatermarkTextColorClick(self, evt):
    	initColor = wx.ColourData()
    	initColor.SetColour(self.btnWatermarkTextColor.GetBackgroundColour())
    	dialog = wx.ColourDialog(self, initColor)
    	dialog.GetColourData().SetChooseFull(True)
	if wx.ID_OK == dialog.ShowModal():
		data = dialog.GetColourData()
		self.btnWatermarkTextColor.SetBackgroundColour(data.GetColour())
		self.btnWatermarkTextColor.SetLabel(data.GetColour().GetAsString(wx.C2S_HTML_SYNTAX))
	dialog.Destroy()
	self.add_watermark()
	
    def OnbtnWatermarkImageClick(self, evt):
    	wildcard = '%s (*.jpg;*.gif;*.png)|*.jpg;*.gif;*.png' % _('Image Files')
	if sys.platform[:5] == 'linux':
		wildcard = '%s (*.jpg;*.gif;*.png)|*.[Jj][Pp][Gg];*.[Gg][Ii][Ff];*.[Pp][Nn][Gg]' % _('Image Files')
	default_path = os.path.abspath(os.path.dirname(self.txtWatermarkImage.GetValue()))
	dialog = wx.FileDialog(None, _('Select a picture as watermark'), default_path, '', wildcard, wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK:
		self.txtWatermarkImage.SetValue(dialog.GetPath())
	dialog.Destroy()
	
    def OnbtnOKClick(self, evt):
    	try:
    		write_config('Resize', 
    			{'Resize': self.chkResize.IsChecked(), \
    			'ResizeWidth': self.txtResizeWidth.GetValue(), \
    			'ResizeHeight': self.txtResizeHeight.GetValue(), \
    			'ResizeLarger': self.chkResizeLarger.IsChecked(), \
    			'ResizeLargerThan': self.txtResizeLarger.GetValue(), \
    			'ResizeQuality': self.cmbResizeQuality.GetSelection(), \
    			})
    		dict = {'EXIF': self.chkEXIF.IsChecked(), \
    			'PreserveEXIF': self.chkPreserveEXIF.IsChecked(), \
    			'EXIFThumbnail': self.thumbnail.encode('unicode_escape'), \
    			'ThumbR': self.chkThumbR.IsChecked(), \
    			'ThumbW': self.chkThumbW.IsChecked(), \
    			'WriteEXIFBackup': self.chkWriteEXIFBackup.IsChecked(), \
    			'WriteEXIFUnicode': self.chkWriteEXIFUnicode.IsChecked(), \
    			}
    		tmp_list = []
        	for i in xrange(len(self.txtEXIFInfo)):
			dict['EXIFInfo%02d' % i] = self.txtEXIFInfo[i][1].GetValue().encode('unicode_escape')
			num = 0
			if self.txtEXIFInfo[i][2].IsChecked():
				num += 4
			if self.txtEXIFInfo[i][3].IsChecked():
				num += 2
			tmp_list.append(str(num))
		dict['EXIFInfoCheck'] = ','.join(tmp_list)
    		write_config('EXIF', dict)
    		write_config('Watermark', 
    			{'Watermark': self.chkWatermark.IsChecked(), \
    			'WatermarkType': self.rdWatermarkType.GetSelection(), \
    			'WatermarkText': self.txtWatermarkText.GetValue().encode('unicode_escape'), \
    			'WatermarkTextPreFont': self.cmbWatermarkTextFont.GetSelection(), \
    			'WatermarkTextFont': self.txtWatermarkTextFont.GetValue().encode('unicode_escape'), \
    			'WatermarkTextSize': self.txtWatermarkTextSize.GetValue(), \
    			'WatermarkTextColor': self.btnWatermarkTextColor.GetBackgroundColour().Get(), \
    			'WatermarkTextPosition': self.cmbWatermarkTextPosition.GetSelection(), \
    			'WatermarkTextPadding': self.txtWatermarkTextPadding.GetValue(), \
    			'WatermarkImage': self.txtWatermarkImage.GetValue().encode('unicode_escape'), \
    			'WatermarkImageOpacity': self.sldWatermarkImageOpacity.GetValue(), \
    			'WatermarkImagePosition': self.cmbWatermarkImagePosition.GetSelection(), \
    			'WatermarkImagePadding': self.txtWatermarkImagePadding.GetValue(), \
    			})
    	except:
    		wx.MessageBox(MSG_SAVE_SETTINGS_ERROR, MSG_ERROR, wx.ICON_ERROR)
    	self.Close()

    def OnClose(self, evt):
	self.Destroy()
	
    def add_watermark(self, evt = None):
    	if not self.chkWatermark.GetValue():
    		self.imgEffect.SetBitmap(self.imgOriginal.GetBitmap())
    		return  
    	try:  		
	    	if self.rdWatermarkType.GetSelection() == 0: # text type
	    		ww = signature(SAMPLE_IMAGE, 
	    			self.txtWatermarkText.GetValue(),
	    			self.cmbWatermarkTextPosition.GetSelection(),
	    			self.txtWatermarkTextPadding.GetValue(),
	    			self.txtWatermarkTextFont.GetValue(),
	    			self.txtWatermarkTextSize.GetValue(),
	    			self.btnWatermarkTextColor.GetBackgroundColour().Get()
	    			)
	    	else: # image type
		    	ww = watermark(SAMPLE_IMAGE, 
		    		self.txtWatermarkImage.GetValue(), 
		    		self.cmbWatermarkImagePosition.GetSelection(),
		    		self.txtWatermarkImagePadding.GetValue(),
		    		self.sldWatermarkImageOpacity.GetValue() / 100.0
		    		)
	    	image = wx.EmptyImage(ww.size[0], ww.size[1])
		image.SetData(ww.convert('RGB').tostring())
		self.imgEffect.SetBitmap(image.ConvertToBitmap())
	except:
		self.imgEffect.SetBitmap(self.imgOriginal.GetBitmap())
    		return 

# end of class MyImageDialog

class MyAboutDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):    
        wx.Dialog.__init__(self, *args, **kwargs)
        self.imgLogo = wx.StaticBitmap(self, -1, wx.Bitmap('icon/logo.png'))
        self.txtAppName = wx.StaticText(self, label = APPNAME)
        font1 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        self.txtAppName.SetFont(font1)
        
	self.notebook = wx.Notebook(self, -1)
        self.notebook_pane1 = wx.Panel(self.notebook, -1)
        self.txtInfo = wx.StaticText(self.notebook_pane1)
        self.txtInfo.SetLabel('%s: %s\n%s: %s (%s)\n%s: %s\n%s: GPL v2' 
		% (_('Version'), VERSION, _('Author'), AUTHOR, EMAIL, _('Homepage'), HOMEPAGE, _('License')))
		
        self.notebook_pane2 = wx.Panel(self.notebook, -1)
        self.label_1 = wx.StaticText(self.notebook_pane2)
        self.label_1.SetLabel('%s: (%s)' % (_('Thanks for advice and feedback from following IDs'), _('in alphabetical order')))
        self.txtCredits = wx.TextCtrl(self.notebook_pane2, -1, size=(400, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.txtLink = wx.HyperlinkCtrl(self, -1, _('Visit Homepage'), HOMEPAGE)
        self.btnOK = wx.Button(self, wx.ID_OK, _("OK"))

        self.__set_properties()
        self.__do_layout()

	self.Bind(wx.EVT_CLOSE, self.OnClose)
	
    def __set_properties(self):
        self.SetTitle(_("About"))
        credit_list = [item.strip() for item in CREDITS.split(',')]
        credit_list.sort()
        self.txtCredits.SetValue(', '.join(credit_list))

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.imgLogo, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer.Add(self.txtAppName, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.txtInfo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.notebook_pane1.SetSizer(sizer_1)
        sizer_2.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.txtCredits, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5)
        self.notebook_pane2.SetSizer(sizer_2)
        self.notebook.AddPage(self.notebook_pane1, _("Detailed Information"))
        self.notebook.AddPage(self.notebook_pane2, _("Credits"))
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
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