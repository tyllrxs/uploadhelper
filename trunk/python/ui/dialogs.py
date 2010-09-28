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

class MyImageDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Listbook(self, -1, style=wx.LB_TOP)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.sizer_16_staticbox = wx.StaticBox(self.notebook_1_pane_2, -1, _("EXIF Settings"))
        self.sizer_WatermarkText_staticbox = wx.StaticBox(self.notebook_1_pane_3, -1, _("Watermark Text"))
        self.sizer_WatermarkImage_staticbox = wx.StaticBox(self.notebook_1_pane_3, -1, _("Watermark Image"))
        self.sizer_Watermark_Setting_staticbox = wx.StaticBox(self.notebook_1_pane_3, -1, _("Watermark Settings"))
        self.sizer_Watermark_Preview_staticbox = wx.StaticBox(self.notebook_1_pane_3, -1, _("Preview"))
        self.sizer_17_staticbox = wx.StaticBox(self.notebook_1_pane_1, -1, _("Resize Settings"))
        self.chkResize = wx.CheckBox(self.notebook_1_pane_1, -1, _("Enable Resize for Large Images"))
        self.label_18 = wx.StaticText(self.notebook_1_pane_1, -1, _("Resize To"))
        self.txtResizeWidth = wx.SpinCtrl(self.notebook_1_pane_1, -1, "", min=0, max=100)
        self.label_19 = wx.StaticText(self.notebook_1_pane_1, -1, _("X"))
        self.txtResizeHeight = wx.SpinCtrl(self.notebook_1_pane_1, -1, "", min=0, max=100)
        self.chkResizeLarger = wx.CheckBox(self.notebook_1_pane_1, -1, _("Resize only for Image Size (KB) >"))
        self.txtResizeLarger = wx.SpinCtrl(self.notebook_1_pane_1, -1, "", min=0, max=100)
        self.chkEXIF = wx.CheckBox(self.notebook_1_pane_2, -1, _("Enable EXIF Editing for JPEG"))
        self.label_10 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_10"), style=wx.ALIGN_CENTRE)
        self.text_ctrl_3 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.label_14 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_14"))
        self.text_ctrl_7 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.label_11 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_11"))
        self.text_ctrl_4 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.label_15 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_15"))
        self.text_ctrl_8 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.label_12 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_12"))
        self.text_ctrl_5 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.label_16 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_16"))
        self.text_ctrl_9 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.label_13 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_13"))
        self.text_ctrl_6 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.label_17 = wx.StaticText(self.notebook_1_pane_2, -1, _("label_17"))
        self.text_ctrl_10 = wx.TextCtrl(self.notebook_1_pane_2, -1, "")
        self.btnImportEXIF = wx.Button(self.notebook_1_pane_2, -1, _("Import EXIF from Image..."))
        self.chkWatermark = wx.CheckBox(self.notebook_1_pane_3, -1, _("Enable Watermark"))
        self.rdWatermarkType = wx.RadioBox(self.notebook_1_pane_3, -1, _("Watermark Type"), choices=[_("Text"), _("Image")], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.label_3 = wx.StaticText(self.notebook_1_pane_3, -1, _("Text"))
        self.txtWatermarkText = wx.TextCtrl(self.notebook_1_pane_3, -1, "")
        self.label_4 = wx.StaticText(self.notebook_1_pane_3, -1, _("Font"))
        self.lblWatermarkTextFont = wx.StaticText(self.notebook_1_pane_3, -1, _("label_5"))
        self.btnWatermarkTextFont = wx.Button(self.notebook_1_pane_3, -1, _("Change Font..."))
        self.label_9 = wx.StaticText(self.notebook_1_pane_3, -1, _("Transparency"))
        self.sldWatermarkTextTransparency = wx.Slider(self.notebook_1_pane_3, -1, 0, 0, 100, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.label_6 = wx.StaticText(self.notebook_1_pane_3, -1, _("Position"))
        self.cmbWatermarkTextPosition = wx.Choice(self.notebook_1_pane_3, -1, choices=[_("Top Left"), _("Top Right"), _("Bottom Left"), _("Bottom Right")])
        self.label_7 = wx.StaticText(self.notebook_1_pane_3, -1, _("Padding"))
        self.txtWatermarkTextPadding = wx.SpinCtrl(self.notebook_1_pane_3, -1, "", min=0, max=100)
        self.label_8 = wx.StaticText(self.notebook_1_pane_3, -1, _("Image"))
        self.txtWatermarkImage = wx.TextCtrl(self.notebook_1_pane_3, -1, "")
        self.btnWatermarkImage = wx.Button(self.notebook_1_pane_3, -1, _("button_4"))
        self.label_9_copy = wx.StaticText(self.notebook_1_pane_3, -1, _("Transparency"))
        self.sldWatermarkImageTransparency = wx.Slider(self.notebook_1_pane_3, -1, 0, 0, 100, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)
        self.label_6_copy = wx.StaticText(self.notebook_1_pane_3, -1, _("Position"))
        self.cmbWatermarkImagePosition = wx.Choice(self.notebook_1_pane_3, -1, choices=[_("Top Left"), _("Top Right"), _("Bottom Left"), _("Bottom Right")])
        self.label_7_copy = wx.StaticText(self.notebook_1_pane_3, -1, _("Padding"))
        self.txtWatermarkImagePadding = wx.SpinCtrl(self.notebook_1_pane_3, -1, "", min=0, max=100)
        self.lblOriginal = wx.StaticText(self.notebook_1_pane_3, -1, _("Original"))
        self.imgOriginal = wx.StaticBitmap(self.notebook_1_pane_3, -1, wx.NullBitmap)
        self.lblEffect = wx.StaticText(self.notebook_1_pane_3, -1, _("Effect"))
        self.imgEffect = wx.StaticBitmap(self.notebook_1_pane_3, -1, wx.NullBitmap)
        self.btnOK = wx.Button(self, wx.ID_OK, _("OK"))
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle(_("Image Manipulation"))
        self.chkResize.SetValue(1)
        self.rdWatermarkType.SetSelection(0)
        self.cmbWatermarkTextPosition.SetSelection(3)
        self.cmbWatermarkImagePosition.SetSelection(3)

    def __do_layout(self):
        sizer_dialog = wx.BoxSizer(wx.VERTICAL)
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Resize = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Watermark = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Watermark_Preview = wx.StaticBoxSizer(self.sizer_Watermark_Preview_staticbox, wx.VERTICAL)
        sizer_Watermark_Main = wx.BoxSizer(wx.VERTICAL)
        sizer_Watermark_Setting = wx.StaticBoxSizer(self.sizer_Watermark_Setting_staticbox, wx.VERTICAL)
        sizer_WatermarkImage = wx.StaticBoxSizer(self.sizer_WatermarkImage_staticbox, wx.VERTICAL)
        sizer_13_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_WatermarkText = wx.StaticBoxSizer(self.sizer_WatermarkText_staticbox, wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_EXIF = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.StaticBoxSizer(self.sizer_16_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(4, 4, 0, 0)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.StaticBoxSizer(self.sizer_17_staticbox, wx.VERTICAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7.Add(self.chkResize, 0, wx.ALL, 5)
        sizer_18.Add(self.label_18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_18.Add(self.txtResizeWidth, 0, wx.ALL, 5)
        sizer_18.Add(self.label_19, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_18.Add(self.txtResizeHeight, 0, wx.ALL, 5)
        sizer_17.Add(sizer_18, 0, wx.EXPAND, 0)
        sizer_19.Add(self.chkResizeLarger, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_19.Add(self.txtResizeLarger, 0, wx.ALL, 5)
        sizer_17.Add(sizer_19, 0, wx.EXPAND, 0)
        sizer_7.Add(sizer_17, 1, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_7)
        sizer_EXIF.Add(self.chkEXIF, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.label_10, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.text_ctrl_3, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_14, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.text_ctrl_7, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.text_ctrl_4, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_15, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.text_ctrl_8, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.text_ctrl_5, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_16, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.text_ctrl_9, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.text_ctrl_6, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.label_17, 0, wx.ALL, 5)
        grid_sizer_1.Add(self.text_ctrl_10, 0, wx.ALL|wx.EXPAND, 5)
        sizer_16.Add(grid_sizer_1, 0, wx.EXPAND, 0)
        sizer_EXIF.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_EXIF.Add(self.btnImportEXIF, 0, wx.ALL, 5)
        self.notebook_1_pane_2.SetSizer(sizer_EXIF)
        sizer_Watermark_Main.Add(self.chkWatermark, 0, wx.ALL, 5)
        sizer_Watermark_Setting.Add(self.rdWatermarkType, 0, wx.EXPAND, 0)
        sizer_11.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_11.Add(self.txtWatermarkText, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_WatermarkText.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_10.Add(self.label_4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.lblWatermarkTextFont, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.btnWatermarkTextFont, 0, wx.ALL, 5)
        sizer_10.Add(self.label_9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10.Add(self.sldWatermarkTextTransparency, 1, wx.EXPAND, 0)
        sizer_WatermarkText.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_13.Add(self.label_6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.cmbWatermarkTextPosition, 0, wx.ALL, 5)
        sizer_13.Add(self.label_7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.txtWatermarkTextPadding, 0, wx.ALL, 5)
        sizer_WatermarkText.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_Watermark_Setting.Add(sizer_WatermarkText, 0, wx.EXPAND, 0)
        sizer_15.Add(self.label_8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_15.Add(self.txtWatermarkImage, 1, wx.ALL|wx.EXPAND, 5)
        sizer_15.Add(self.btnWatermarkImage, 0, wx.ALL, 5)
        sizer_WatermarkImage.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_10_copy.Add(self.label_9_copy, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_10_copy.Add(self.sldWatermarkImageTransparency, 1, wx.EXPAND, 0)
        sizer_10_copy.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_WatermarkImage.Add(sizer_10_copy, 1, wx.EXPAND, 0)
        sizer_13_copy.Add(self.label_6_copy, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13_copy.Add(self.cmbWatermarkImagePosition, 0, wx.ALL, 5)
        sizer_13_copy.Add(self.label_7_copy, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13_copy.Add(self.txtWatermarkImagePadding, 0, wx.ALL, 5)
        sizer_WatermarkImage.Add(sizer_13_copy, 1, wx.EXPAND, 0)
        sizer_Watermark_Setting.Add(sizer_WatermarkImage, 1, wx.EXPAND, 0)
        sizer_Watermark_Main.Add(sizer_Watermark_Setting, 1, wx.EXPAND, 0)
        sizer_Watermark.Add(sizer_Watermark_Main, 1, wx.EXPAND, 0)
        sizer_Watermark_Preview.Add(self.lblOriginal, 0, wx.ALL, 5)
        sizer_Watermark_Preview.Add(self.imgOriginal, 0, 0, 0)
        sizer_Watermark_Preview.Add(self.lblEffect, 0, wx.ALL, 5)
        sizer_Watermark_Preview.Add(self.imgEffect, 0, 0, 0)
        sizer_Watermark.Add(sizer_Watermark_Preview, 0, wx.EXPAND, 0)
        self.notebook_1_pane_3.SetSizer(sizer_Watermark)
        self.notebook_1.AddPage(self.notebook_1_pane_1, _("Resize"))
        self.notebook_1.AddPage(self.notebook_1_pane_2, _("EXIF"))
        self.notebook_1.AddPage(self.notebook_1_pane_3, _("Watermark"))
        sizer_Resize.Add(self.notebook_1, 1, wx.EXPAND, 0)
        sizer_dialog.Add(sizer_Resize, 1, wx.EXPAND, 0)
        sizer_button.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_button.Add(self.btnOK, 0, wx.ALL, 5)
        sizer_button.Add(self.btnCancel, 0, wx.ALL, 5)
        sizer_dialog.Add(sizer_button, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_dialog)
        sizer_dialog.Fit(self)
        self.Layout()

# end of class MyImageDialog

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
