# -*- coding: utf-8 -*-

import os, sys, shutil
import urllib, urllib2, cookielib
import wx
from xml.dom import minidom
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from utilfunc import *
from dialogs import *
from dnd import *
from logoutthread import *
from checkcookiethread import *
from uploadthread import *
from checkupdatethread import *
from downloadthread import *
from parsehtml import *
from taskbaricon import *

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)

        if sys.platform.startswith('win32'):
		self.SetIcon(wx.Icon('icon/logo32.ico', wx.BITMAP_TYPE_ICO))
		self.trayicon = ddTaskBarIcon(wx.Icon('icon/logo16.ico', wx.BITMAP_TYPE_ICO), APPNAME, self)
	elif sys.platform.find('linux') >= 0:
		self.SetIcon(wx.Icon('icon/logo32.png', wx.BITMAP_TYPE_PNG))
		self.trayicon = ddTaskBarIcon(wx.Icon('icon/logo16.png', wx.BITMAP_TYPE_PNG), APPNAME, self)
        
        self.__set_menubar()
        self.__set_toolbar()
        self.__set_statusbar()
        
        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook_pane3 = wx.Panel(self.notebook, -1)
        self.notebook_pane2 = wx.Panel(self.notebook, -1)
        self.notebook_pane1 = wx.Panel(self.notebook, -1)
        self.object_8_staticbox = wx.StaticBox(self.notebook_pane2, -1, _("Destination"))
        self.object_3_staticbox = wx.StaticBox(self.notebook_pane1, -1, _("Destination"))
        self.cmbZone = wx.ComboBox(self.notebook_pane1, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cmbBoard = wx.ComboBox(self.notebook_pane1, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.chkLock = wx.CheckBox(self.notebook_pane1, -1, _("Locked"))
        self.label_1 = wx.StaticText(self.notebook_pane1, -1, _("Select Files to Upload"))
        self.btnBrowse = wx.Button(self.notebook_pane1, -1, '%s...' % _("Browse"))
        self.lstUpFile = DragList(self.notebook_pane1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.lblProgress = wx.StaticText(self.notebook_pane1, -1, "")
        self.btnUpload = wx.Button(self.notebook_pane1, -1, _("Upload"))
        self.gagProgress = wx.Gauge(self.notebook_pane1, -1, 100)
        self.label_3 = wx.StaticText(self.notebook_pane2, -1, _("Title"))
        self.txtTitle = wx.TextCtrl(self.notebook_pane2, -1, "")
        self.label_4 = wx.StaticText(self.notebook_pane2, -1, _("Signature"))
        self.txtSignature = wx.SpinCtrl(self.notebook_pane2, -1, "", min=0, max=10)
        self.txtBody = wx.TextCtrl(self.notebook_pane2, -1, "", style=wx.TE_MULTILINE)
        self.cmbPostZone = wx.ComboBox(self.notebook_pane2, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cmbPostBoard = wx.ComboBox(self.notebook_pane2, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.btnPost = wx.Button(self.notebook_pane2, -1, _("Post"))
        self.label_5 = wx.StaticText(self.notebook_pane3, -1, _("Copy the Webpage Fraction to Clipboard, then Click"))
        self.btnReship = wx.Button(self.notebook_pane3, -1, _("Start Reshipping"))
        self.txtReship = wx.TextCtrl(self.notebook_pane3, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()
        
        # bind events to UI controls
        self.Bind(wx.EVT_COMBOBOX, self.OnZoneChange, self.cmbZone)
	self.Bind(wx.EVT_COMBOBOX, self.OnBoardChange, self.cmbBoard)
	self.Bind(wx.EVT_COMBOBOX, self.OnPostZoneChange, self.cmbPostZone)
	self.Bind(wx.EVT_CHECKBOX, self.OnchkLockClick, self.chkLock)
	self.Bind(wx.EVT_BUTTON, self.OnbtnBrowseClick, self.btnBrowse)
	self.Bind(wx.EVT_BUTTON, self.OnbtnUploadClick, self.btnUpload)
	self.Bind(wx.EVT_BUTTON, self.OnbtnPostClick, self.btnPost)
	self.Bind(wx.EVT_BUTTON, self.OnbtnReshipClick, self.btnReship)
	# for win32 compatibility issues
	#self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnlstUpFileRClick, self.lstUpFile)
	self.lstUpFile.Bind(wx.EVT_CONTEXT_MENU, self.OnlstUpFileRClick)
	self.Bind(wx.EVT_CLOSE, self.OnClose)
	self.Bind(wx.EVT_ICONIZE, self.on_iconify)
        
    def __set_menubar(self):
        menuBar = wx.MenuBar()
        mnuLogin = wx.Menu()
        mnuSwitch = wx.MenuItem(mnuLogin, wx.NewId(), '%s...' % _("&Switch User"), "", wx.ITEM_NORMAL)
        mnuSwitch.SetBitmap(wx.Bitmap('icon/16/switch.png'))
        mnuLogin.AppendItem(mnuSwitch)
        mnuLogin.AppendSeparator()
        mnuLogout = wx.MenuItem(mnuLogin, wx.NewId(), '%s...' % _("Logo&ut"), "", wx.ITEM_NORMAL)
        mnuLogout.SetBitmap(wx.Bitmap('icon/16/logout.png'))
        mnuLogin.AppendItem(mnuLogout)
        menuBar.Append(mnuLogin, _("&Login"))
        mnuSetting = wx.Menu()
        mnuPreference = wx.MenuItem(mnuSetting, wx.ID_PREFERENCES, '%s...' % _("&Preferences"))
        mnuSetting.AppendItem(mnuPreference)
        mnuImageManipulation = wx.MenuItem(mnuSetting, wx.NewId(), '%s...' % _("Image &Manipulation"))
        mnuImageManipulation.SetBitmap(wx.Bitmap('icon/16/imagemani.png'))
        mnuSetting.AppendItem(mnuImageManipulation)
        mnuSetting.AppendSeparator()
        mnuLang = wx.Menu()
        target_lang = read_config('General', 'language', 'en') 
        for cod, lng in APPLANGUAGES:
        	mnulng = wx.MenuItem(mnuLang, wx.NewId(), lng.decode('utf8'), cod, wx.ITEM_RADIO)
        	mnuLang.AppendItem(mnulng)
        	if cod == target_lang:
        		mnulng.Check(True)
        	self.Bind(wx.EVT_MENU, self.OnmnuLangClick, mnulng)
        mnuSetting.AppendMenu(-1, _("&Language"), mnuLang, _("Select interface language"))
        mnuToolbar = wx.Menu()
        mnuTBShowIcon = wx.MenuItem(mnuToolbar, wx.NewId(), _('Show &Icons'), '1', wx.ITEM_CHECK)
        mnuToolbar.AppendItem(mnuTBShowIcon)
        mnuTBShowText = wx.MenuItem(mnuToolbar, wx.NewId(), _('Show &Texts'), '2', wx.ITEM_CHECK)
        mnuToolbar.AppendItem(mnuTBShowText)
        tool_style = read_config_int('General', 'ToolbarStyle', 260)
        mnuTBShowIcon.Check(not (tool_style & wx.TB_NOICONS))
        mnuTBShowText.Check(tool_style & wx.TB_TEXT)
        mnuSetting.AppendMenu(-1, _("T&oolbar"), mnuToolbar)
        mnuSetting.AppendSeparator()
        if sys.platform.startswith('win32'):
        	mnuTerm = wx.Menu()
        	mnuFterm = wx.MenuItem(mnuTerm, wx.NewId(), 'Fterm', '', wx.ITEM_NORMAL)
        	mnuTerm.AppendItem(mnuFterm)
        	mnuCterm = wx.MenuItem(mnuTerm, wx.NewId(), 'Cterm', '', wx.ITEM_NORMAL)
        	mnuTerm.AppendItem(mnuCterm)
        	mnuSetting.AppendMenu(-1, '%s *T&erm' % _("Integrate to"), mnuTerm)
        	self.Bind(wx.EVT_MENU, self.OnmnuFtermClick, mnuFterm)
		self.Bind(wx.EVT_MENU, self.OnmnuCtermClick, mnuCterm)
        mnuAlwaysOnTop = wx.MenuItem(mnuSetting, wx.NewId(), _("Always on &Top"), "", wx.ITEM_CHECK)
        mnuSetting.AppendItem(mnuAlwaysOnTop)
        menuBar.Append(mnuSetting, _("&Setting"))
        mnuHelp = wx.Menu()
        mnuFAQ = wx.MenuItem(mnuHelp, wx.ID_HELP, _("&FAQ"))
        mnuHelp.AppendItem(mnuFAQ)
        mnuHelp.AppendSeparator()
        mnuHomepage = wx.MenuItem(mnuHelp, wx.NewId(), _("&Homepage"), _("Visit Homepage"), wx.ITEM_NORMAL)
        mnuHomepage.SetBitmap(wx.Bitmap('icon/16/home.png'))
        mnuHelp.AppendItem(mnuHomepage)
        mnuCheckUpdate = wx.MenuItem(mnuHelp, wx.NewId(), '%s...' % _("Check for &Updates"), "", wx.ITEM_NORMAL)
        mnuHelp.AppendItem(mnuCheckUpdate)
        mnuHelp.AppendSeparator()
        mnuAbout = wx.MenuItem(mnuHelp, wx.ID_ABOUT, '%s...' % _("&About"), _("Show about dialog"))
        mnuHelp.AppendItem(mnuAbout)
        menuBar.Append(mnuHelp, _("&Help"))
        # Mac issues
        menuBar.SetAutoWindowMenu(False)
	# Bind events
	self.Bind(wx.EVT_MENU, self.OnmnuSwitchClick, mnuSwitch)
	self.Bind(wx.EVT_MENU, self.OnmnuLogoutClick, mnuLogout)
	self.Bind(wx.EVT_MENU, self.OnmnuTBShowClick, mnuTBShowIcon)
	self.Bind(wx.EVT_MENU, self.OnmnuTBShowClick, mnuTBShowText)
	self.Bind(wx.EVT_MENU, self.OnmnuPreferenceClick, mnuPreference)
	self.Bind(wx.EVT_MENU, self.OnmnuImageManipulationClick, mnuImageManipulation)
	self.Bind(wx.EVT_MENU, self.OnmnuAlwaysOnTopClick, mnuAlwaysOnTop)
	self.Bind(wx.EVT_MENU, self.OnmnuFAQClick, mnuFAQ)
	self.Bind(wx.EVT_MENU, self.OnmnuHomepageClick, mnuHomepage)
	self.Bind(wx.EVT_MENU, self.OnmnuCheckUpdateClick, mnuCheckUpdate)
	self.Bind(wx.EVT_MENU, self.OnmnuAboutClick, id=wx.ID_ABOUT)
	# Attach menubar to frame   
	self.SetMenuBar(menuBar)

    def __set_toolbar(self):
    	toolBar = wx.ToolBar(self, style = read_config_int('General', 'ToolbarStyle', 260))
	tlbSwitch = toolBar.AddLabelTool(-1, _("Switch user"), wx.Bitmap('icon/24/switch.png'), wx.NullBitmap, wx.ITEM_NORMAL, _("Switch user"), _("Switch user"))
        tlbLogout = toolBar.AddLabelTool(-1, _("Logout"), wx.Bitmap('icon/24/logout.png'), wx.NullBitmap, wx.ITEM_NORMAL, _("Logout"), _("Logout"))
        toolBar.AddSeparator()
        tlbPreference = toolBar.AddLabelTool(-1, _("Preferences"), wx.Bitmap('icon/24/setting.png'), wx.NullBitmap, wx.ITEM_NORMAL, _("Preferences"), _("Preferences"))
        tlbImageManipulation = toolBar.AddLabelTool(-1, _("Image Manipulation"), wx.Bitmap('icon/24/imagemani.png'), wx.NullBitmap, wx.ITEM_NORMAL, _("Image Manipulation"), _("Image Manipulation"))
        toolBar.AddSeparator()
        tlbFAQ = toolBar.AddLabelTool(wx.ID_HELP, _("FAQ"), wx.Bitmap('icon/24/help.png'), wx.NullBitmap, wx.ITEM_NORMAL, _("FAQ"), _("FAQ"))
        # Bind events
        self.Bind(wx.EVT_TOOL, self.OnmnuSwitchClick, tlbSwitch)
	self.Bind(wx.EVT_TOOL, self.OnmnuLogoutClick, tlbLogout)
	self.Bind(wx.EVT_TOOL, self.OnmnuPreferenceClick, tlbPreference)
	self.Bind(wx.EVT_TOOL, self.OnmnuImageManipulationClick, tlbImageManipulation)
	self.Bind(wx.EVT_TOOL, self.OnmnuFAQClick, tlbFAQ)
        # Attach
        toolBar.Realize()
        self.SetToolBar(toolBar) 
    
    def __set_statusbar(self):
    	statusBar = wx.StatusBar(self)
	statusBar.SetFields(STATUSBAR_INFO)
	statusBar.SetStatusWidths([-1, -2])
	self.SetStatusBar(statusBar)
    
    def __set_properties(self):
	update_title()
	self.read_zones()
	self.cmbZone.SetSelection(read_config_int('Upload', 'UpZone', 4))
	self.cmbPostZone.SetSelection(read_config_int('Upload', 'PostZone', 4))
	self.read_boards()
	self.cmbBoard.SetSelection(read_config_int('Upload', 'UpBoard', 16))
	self.read_postboards()
	self.cmbPostBoard.SetSelection(read_config_int('Upload', 'PostBoard', 16))
	self.chkLock.SetValue(read_config_bool('Upload', 'UpBoardLock'))
	evt = wx.CommandEvent()
	self.OnchkLockClick(evt)
	il = wx.ImageList(16,16, True)
	for name in ['alarm', 'process', 'ok', 'error']:
		il.Add(wx.Bitmap('icon/indicator/%s.png' % name))
	self.lstUpFile.AssignImageList(il, wx.IMAGE_LIST_SMALL)
	for col, text in enumerate(['No.', _('Filename'), '%s (KB)' % _('Size'), _('Status')]):
		if col == 0 or col == 2:
			self.lstUpFile.InsertColumn(col, text, wx.LIST_FORMAT_CENTER)
		else:
			self.lstUpFile.InsertColumn(col, text, wx.LIST_FORMAT_LEFT)
	col_widths = read_config('Upload', 'ColumnWidths', '40,320,80,120').split(',')
	for col in xrange(self.lstUpFile.GetColumnCount()):
		self.lstUpFile.SetColumnWidth(col, int(col_widths[col]))
	self.txtSignature.SetValue(read_config_int('Upload', 'PostSignature', 1))
	
	# create popup menu
	self.ppmenu = wx.Menu()
	for text in LIST_CONTEXT_MENU:
		if len(text) <= 0:
			self.ppmenu.AppendSeparator()
		else:
			item = self.ppmenu.Append(-1, text)
			self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
	
	# check the versions of python and wxpython
	if not sys.platform.startswith('win32'):
		pyver = get_python_version()
		if pyver < '2.5':
			self.txtReship.AppendText('\n%s:\n%s\n' % (_('Python is too old. Get a newer 2.X (NO 3.0 OR ABOVE) version at'), HOME_PYTHON))
		elif pyver >= '3':
			self.txtReship.AppendText('\n%s:\n%s\n' % (_('Python 3 is not supported. Get a 2.X version at'), HOME_PYTHON))
		
	    	wxver = wx.VERSION
	    	if '.'.join([str(i) for i in wxver[:3]]) < '2.8.10':
	    		self.txtReship.AppendText('\n%s:\n%s\n' % (_('wxPython is too old. Get a newer version at'), HOME_WXPYTHON))
	
	# make the list control be a drop target
	dt = ListDrop(self.lstUpFile)
        self.lstUpFile.SetDropTarget(dt)
	
	# set some status variables
	self.PostedMode = False
	self.UploadedMode = False
	self.ReshipMode = False
	self.to_upload = False
	self.to_post = False
	
	# receive message from check for updates thread
	Publisher().subscribe(self.updateDisplay, "update")


    def __do_layout(self):
        object_1 = wx.BoxSizer(wx.VERTICAL)
        object_9 = wx.BoxSizer(wx.VERTICAL)
        object_10 = wx.BoxSizer(wx.HORIZONTAL)
        object_6 = wx.BoxSizer(wx.VERTICAL)
        object_8 = wx.StaticBoxSizer(self.object_8_staticbox, wx.HORIZONTAL)
        object_7 = wx.BoxSizer(wx.HORIZONTAL)
        object_2 = wx.BoxSizer(wx.VERTICAL)
        object_5 = wx.BoxSizer(wx.HORIZONTAL)
        object_4 = wx.BoxSizer(wx.HORIZONTAL)
        object_3 = wx.StaticBoxSizer(self.object_3_staticbox, wx.HORIZONTAL)
        object_3.Add(self.cmbZone, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_3.Add(self.cmbBoard, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_3.Add(self.chkLock, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_2.Add(object_3, 0, wx.ALL|wx.EXPAND, 5)
        object_4.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_4.Add(self.btnBrowse, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_4.Add((20, 20), 1, 0, 0)
        object_2.Add(object_4, 0, wx.ALL|wx.EXPAND, 5)
        object_2.Add(self.lstUpFile, 1, wx.ALL|wx.EXPAND, 5)
        object_5.Add(self.lblProgress, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_5.Add(self.btnUpload, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_5.Add(self.gagProgress, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_2.Add(object_5, 0, wx.ALL|wx.EXPAND, 5)
        self.notebook_pane1.SetSizer(object_2)
        object_7.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_7.Add(self.txtTitle, 3, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_7.Add(self.label_4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_7.Add(self.txtSignature, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_6.Add(object_7, 0, wx.ALL|wx.EXPAND, 5)
        object_6.Add(self.txtBody, 1, wx.ALL|wx.EXPAND, 5)
        object_8.Add(self.cmbPostZone, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_8.Add(self.cmbPostBoard, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_6.Add(object_8, 0, wx.ALL|wx.EXPAND, 5)
        object_6.Add(self.btnPost, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        self.notebook_pane2.SetSizer(object_6)
        object_10.Add(self.label_5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_10.Add(self.btnReship, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        object_9.Add(object_10, 0, wx.ALL|wx.EXPAND, 5)
        object_9.Add(self.txtReship, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_pane3.SetSizer(object_9)
        self.notebook.AddPage(self.notebook_pane1, _("Upload Files"))
        self.notebook.AddPage(self.notebook_pane2, _("Post Article"))
        self.notebook.AddPage(self.notebook_pane3, _("Reship Webpage"))
        if sys.platform != 'darwin':
		il = wx.ImageList(32, 32)
		imgs = ['upload.png', 'post.png', 'reship.png']
		self.notebook.AssignImageList(il)
		for page in xrange(self.notebook.GetPageCount()):
			img = il.Add(wx.Bitmap('icon/32/%s' % imgs[page]))
			self.notebook.SetPageImage(page, img)
	self.notebook.SetSelection(read_config_int('Upload', 'ActivePage', 0))
        object_1.Add(self.notebook, 1, wx.EXPAND, 0)
        self.SetSizer(object_1)
        self.Fit()
        self.set_window_size()
        if not (self.get_user_id() and self.get_auto_login()):
		self.show_login()
	if read_config_bool('General', 'AutoUpdate', True):
		CheckUpdateThread(False)

    def set_window_size(self):
	w = read_config_int('General', 'WinWidth', 600)
	h = read_config_int('General', 'WinHeight', 600)
	self.SetSize(wx.Size(w, h))
        self.Layout()
        self.CentreOnScreen()
        if read_config_bool('General', 'WinMaximized', False):
        	self.Maximize()
        
    def read_zones(self):
        xmldoc = minidom.parse(FILE_BOARDS)
	num = 0
	for zone in xmldoc.getElementsByTagName('Zone'):
		self.cmbZone.Append('%d) %s' % (num, zone.attributes['name'].value))
		self.cmbPostZone.Append('%d) %s' % (num, zone.attributes['name'].value))
		num = num + 1

    def read_boards(self):
	self.cmbBoard.Clear()
        xmldoc = minidom.parse(FILE_BOARDS)
	for board in xmldoc.getElementsByTagName('Zone')[self.cmbZone.GetSelection()].childNodes:
		if board.nodeType == board.ELEMENT_NODE:
			self.cmbBoard.Append('%s (%s) [%s]' % (board.nodeName, board.attributes['name'].value, board.attributes['bid'].value))

    def read_postboards(self):
	self.cmbPostBoard.Clear()
        xmldoc = minidom.parse(FILE_BOARDS)
	for board in xmldoc.getElementsByTagName('Zone')[self.cmbPostZone.GetSelection()].childNodes:
		if board.nodeType == board.ELEMENT_NODE:
			self.cmbPostBoard.Append('%s (%s) [%s]' % (board.nodeName, board.attributes['name'].value, board.attributes['bid'].value))

    def get_board_name(self, post=False):
	if post:
		board = self.cmbPostBoard.GetValue()
	else:
		board = self.cmbBoard.GetValue()
	return re.compile('^(\S+)').search(board).group(1)

    def get_board_id(self, post=False):
	if post:
		board = self.cmbPostBoard.GetValue()
	else:
		board = self.cmbBoard.GetValue()
	return re.compile('\[(\d+)\]').search(board).group(1)

    def get_cookie(self):
	return read_config('Login', 'Cookie')

    def get_host(self):
	return BBS_HOSTS[read_config_int('Login', 'Host', 0)]
	
    def get_new_host(self):
	return read_config_int('General', 'FileURL', 0)
	
    def get_user_id(self):
	return read_config('Login', 'UserID')
	
    def get_auto_login(self):
	return read_config('Login', 'AutoLogin')
	
    def get_dialog_path(self):
	return read_config('Upload', 'DefaultPath')

    def show_login(self):
	dialog = MyLoginDialog(self)
	dialog.ShowModal()

    def OnmnuSwitchClick(self, evt):
	self.show_login()
	
    def OnmnuLogoutClick(self, evt):
    	if wx.NO == wx.MessageBox(_('Are you sure to logout?'), _('Confirm'), wx.YES_NO|wx.NO_DEFAULT|wx.ICON_EXCLAMATION):
    		return
	LogoutThread(self.get_host(), self.get_cookie())
	
    def OnmnuPreferenceClick(self, evt):
    	dialog = MySettingDialog(self)
    	dialog.ShowModal()
    	
    def OnmnuImageManipulationClick(self, evt):
    	dialog = MyImageDialog(self)
    	dialog.ShowModal()
	
    def OnmnuTBShowClick(self, evt):
    	menu = self.GetMenuBar().FindItemById(evt.GetId())
    	if menu.GetHelp() == '1':
    		if menu.IsChecked():
    			self.GetToolBar().SetWindowStyleFlag(self.GetToolBar().GetWindowStyleFlag() & ~wx.TB_NOICONS)
    		else:
    			self.GetToolBar().SetWindowStyleFlag(self.GetToolBar().GetWindowStyleFlag() | wx.TB_NOICONS)
    	elif menu.GetHelp() == '2':
    		if menu.IsChecked():
    			self.GetToolBar().SetWindowStyleFlag(self.GetToolBar().GetWindowStyleFlag() | wx.TB_TEXT)
    		else:
    			self.GetToolBar().SetWindowStyleFlag(self.GetToolBar().GetWindowStyleFlag() & ~wx.TB_TEXT)
    
    def OnmnuFtermClick(self, evt):
    	self.add_to_term('Fterm')

    def OnmnuCtermClick(self, evt):
    	self.add_to_term('Cterm')
    
    def add_to_term(self, term):
    	wx.MessageBox('%s %s %s' % (_('Be sure'), term, _('has been closed')))
    	dialog = wx.FileDialog(None, '%s %s' % (_('Select Location of'), term), '', '', '%s (%s.exe)|%s.exe' % (term, term, term), wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK:
		path = os.path.abspath(os.path.dirname(dialog.GetPath()))
		if term == 'Fterm':
			configfile = os.path.join(path, 'fterm.ini')
			cf = ConfigParser.ConfigParser()
			try:
				cf.read(configfile)
				value = cf.getint('Script', 'TotalNumber')
			except:
				wx.MessageBox('%s: %s' % (_('Read Error'), configfile), '%s %s' % (_('Integrate to'), term), wx.ICON_ERROR)
				return
			cf.set('Script', 'TotalNumber', value + 1)
			cf.set('SCRIPT%d' % value, 'DESC', '%s v%s' % (APPNAME.decode('utf8').encode('gb18030'), VERSION))
			cf.set('SCRIPT%d' % value, 'CMDTYPE', 1)
			cf.set('SCRIPT%d' % value, 'CATEGORY', APPNAME.decode('utf8').encode('gb18030'))
			cf.set('SCRIPT%d' % value, 'COMMAND', sys.argv[0].decode('utf8').encode('gb18030'))
			cf.write(open(configfile, 'w'))
		else:
			configfile = os.path.join(path, 'user', 'mycmds.txt')
			if not os.path.isfile():
				try:
					shutil.copy(os.path.join(path, 'user', 'mycmds.txt.example'), configfile)
				except:
					wx.MessageBox('%s: %s' % (_('Read Error'), configfile), '%s %s' % (_('Integrate to'), term), wx.ICON_ERROR)
					return
			fp = open(configfile, 'w+')
			new_line = r'99; ; %s; true; py:import os\\nos.startfile(r\"%s\");' % (APPNAME.decode('utf8').encode('gb18030'), sys.argv[0].replace(r'\', r'\\').decode('utf8').encode('gb18030'))
			try:
				fp.writelines([new_line])
			except:
				wx.MessageBox('%s: %s' % (_('Write Error'), configfile), '%s %s' % (_('Integrate to'), term), wx.ICON_ERROR)
				return
			fp.close()
		wx.MessageBox('%s %s %s' % (_('Integrate to'), term, _('successfully')), '%s %s' % (_('Integrate to'), term), wx.ICON_INFORMATION)
	dialog.Destroy()
        
    def OnmnuAlwaysOnTopClick(self, evt):
	if self.GetMenuBar().FindItemById(evt.GetId()).IsChecked():
        	self.SetWindowStyleFlag(self.GetWindowStyleFlag() | wx.STAY_ON_TOP)
	else:
		self.SetWindowStyleFlag(self.GetWindowStyleFlag() & ~wx.STAY_ON_TOP)

    def OnmnuFAQClick(self, evt):
        wx.LaunchDefaultBrowser('%s%s' % (HOMEPAGE, 'faq.htm'))

    def OnmnuHomepageClick(self, evt):
        wx.LaunchDefaultBrowser(HOMEPAGE)

    def OnmnuCheckUpdateClick(self, evt):
        CheckUpdateThread()

    def OnmnuAboutClick(self, evt):
	dialog3 = MyAboutDialog(self)
	dialog3.ShowModal()

    def OnZoneChange(self, evt):
	tmp = self.cmbBoard.GetSelection()        
	self.read_boards()
	self.cmbBoard.SetSelection(min(tmp, self.cmbBoard.GetCount()-1))     
	self.cmbPostZone.SetSelection(self.cmbZone.GetSelection())
	self.read_postboards()
	self.cmbPostBoard.SetSelection(self.cmbBoard.GetSelection())

    def OnBoardChange(self, evt):
        if self.cmbPostZone.GetSelection() != self.cmbZone.GetSelection():
		self.OnZoneChange(evt)
	else:
		self.cmbPostBoard.SetSelection(self.cmbBoard.GetSelection())

    def OnPostZoneChange(self, evt):
	tmp = self.cmbPostBoard.GetSelection()        
	self.read_postboards()
	self.cmbPostBoard.SetSelection(min(tmp, self.cmbPostBoard.GetCount()-1))    

    def OnchkLockClick(self, evt):
	self.cmbZone.Enabled = not self.chkLock.IsChecked()
	self.cmbBoard.Enabled = not self.chkLock.IsChecked()

    def OnbtnBrowseClick(self, evt):
	wildcard = '%s (*.jpg;*.gif;*.png;*.pdf)|*.jpg;*.gif;*.png;*.pdf|'\
		'%s (*.jpg;*.gif;*.png)|*.jpg;*.gif;*.png|'\
		'%s (*.pdf)|*.pdf|'\
		'%s (*)|*' \
		% (_('All Supported Files'), _('Image Files'), _('PDF Documents'), _('All Files'))
	if sys.platform[:5] == 'linux':
		wildcard = '%s (*.jpg;*.gif;*.png;*.pdf)|*.[Jj][Pp][Gg];*.[Gg][Ii][Ff];*.[Pp][Nn][Gg];*.[Pp][Dd][Ff]|'\
		'%s (*.jpg;*.gif;*.png)|*.[Jj][Pp][Gg];*.[Gg][Ii][Ff];*.[Pp][Nn][Gg]|'\
		'%s (*.pdf)|*.[Pp][Dd][Ff]|'\
		'%s (*)|*' \
		% (_('All Supported Files'), _('Image Files'), _('PDF Documents'), _('All Files'))
	dialog = wx.FileDialog(None, _('Select Files to Upload'), self.get_dialog_path(), '', wildcard, wx.OPEN|wx.MULTIPLE)
	if dialog.ShowModal() == wx.ID_OK:
		self.append_files(dialog.GetPaths())
		write_config('Upload', {'DefaultPath': os.path.abspath(os.path.dirname(dialog.GetPaths()[0]))})
	dialog.Destroy()
	
    def append_files(self, filenames):
    	if self.UploadedMode:
    		self.lstUpFile.DeleteAllItems()
    		self.UploadedMode = False
    	highlight = read_config_bool('General', 'Highlight', True)
    	file_no_larger = read_config_int('General', 'FileNoLarger', 1024)
	for f in filenames:
		if os.path.isdir(f):
			self.append_files(search_files(f, r'\.(jpe?g|gif|png|pdf)$'))
			continue
		index = self.lstUpFile.InsertStringItem(sys.maxint, '%s' % (self.lstUpFile.GetItemCount() + 1))
		self.lstUpFile.SetStringItem(index, 1, f)
		try:
			fz = os.path.getsize(f) / 1024
		except:
			fz = -1
		self.lstUpFile.SetStringItem(index, 2, '%ld' % fz)
		if invalid_file_name(f):
			self.lstUpFile.SetStringItem(index, 3, MSG_INVALID_FILE, 0)
			self.lstUpFile.SetItemTextColour(index, wx.RED)
		elif not supported_file_type(f):
			self.lstUpFile.SetStringItem(index, 3, MSG_UNSUPPORTED_FORMAT, 0)
			self.lstUpFile.SetItemTextColour(index, wx.RED)
		elif fz > file_no_larger:
			if highlight:
				self.lstUpFile.SetStringItem(index, 3, MSG_ENTITY_TOO_LARGE, 0)
				self.lstUpFile.SetItemTextColour(index, wx.BLUE)
	self.lblProgress.SetLabel(MSG_FILE_SELECTED % self.lstUpFile.GetItemCount())    	

    def OnbtnUploadClick(self, evt):
    	self.to_upload = False
	self.lblProgress.SetLabel('%s: %d / %d' % (_('Progress'), 0, self.lstUpFile.GetItemCount()))
	self.gagProgress.SetValue(0)
	if self.lstUpFile.GetItemCount() <= 0:
		wx.MessageBox(_('Select at least one file for uploading.'), _('Upload'), wx.ICON_EXCLAMATION)
		return
	self.btnUpload.Disable()
	if self.PostedMode:
		self.txtBody.SetValue('')
		self.PostedMode = False
	CheckCookieThread(self)
	
    def start_upload_threads(self):
	self.upcount = 0
	self.finishcount = 0
	if not self.ReshipMode:
		for i in xrange(self.lstUpFile.GetItemCount()):
			self.txtBody.SetValue(self.txtBody.GetValue() + '\n%s\n' % MSG_FILE_UPLOADING % (i + 1))
	threads = read_config_int('General', 'Threads', 3)
	for i in range(0, threads):
		if i < self.lstUpFile.GetItemCount():
			self.upcount += 1
			UploadThread(self, self.get_host(), self.get_board_name(), i, self.get_cookie(), self.get_new_host())

    def list_re_number(self):
	for i in xrange(self.lstUpFile.GetItemCount()):
		self.lstUpFile.SetStringItem(i, 0, str(i+1))

    def OnbtnPostClick(self, evt):
    	self.to_post = False
	self.lstUpFile.DeleteAllItems()
	self.lblProgress.SetLabel(MSG_FILE_SELECTED % 0)
	self.gagProgress.SetValue(0)
	if self.txtTitle.GetValue().strip() == '' or self.txtBody.GetValue().strip() == '':
		wx.MessageBox(MSG_FILL_BLANKS)
		return
	self.btnPost.Disable()
	post_title = self.txtTitle.GetValue()
	post_content = self.txtBody.GetValue()
	title_template = read_config('General', 'TitleTemplate', '')
	if title_template.strip():
		title_template = apply_template(title_template)
		title_template = title_template.replace('$TITLE', post_title)
		post_title = title_template
	template = read_config('General', 'Template', '')
	if template.strip():
		template = apply_template(template)
		template = template.replace('$BODY', post_content)
		template = template.replace('$TITLE', post_title)
		post_content = template
	info = perfect_connect('http://%s/bbs/snd?bid=%s' % (self.get_host(), self.get_board_id(True)),
		urllib.urlencode({'title': post_title.encode('gb18030'), 
				'signature': self.txtSignature.GetValue(),
				'text': post_content.encode('gb18030')}))
	self.btnPost.Enable()
	if info == '':
		wx.MessageBox('%s %s.' % (_('Post Successfully to Board'), self.get_board_name(True)), _('Post Article'), wx.ICON_INFORMATION)
		self.PostedMode = True
	elif info.find('No User') >= 0:
		self.to_post = True
		self.show_login()
	else:
		tips = info.split('|')
		wx.MessageBox(tips[1], tips[0])

    def OnbtnReshipClick(self, evt):
    	html = ''
    	source_url = ''
        if not wx.TheClipboard.IsOpened():
		wx.TheClipboard.Open()
	# List all possible clipboard formats for HTML on Windows, Linux and Mac
	formats = ['HTML Format', 'text/html', 'public.html', 'com.apple.webarchive']
	for fm in formats:
		do = wx.CustomDataObject(fm)
        	if wx.TheClipboard.GetData(do):
        		html = do.GetData()
        		if fm == 'HTML Format': # Windows browsers
                        	begin = html.find('SourceURL')
                        	html = html[begin + 10:]
                        	begin = html.find('\n')
                        	source_url = html[:begin]
                        	html = html[begin + 1:]
        		elif fm == 'com.apple.webarchive': # Safari
        			begin = html.find('text/html')
				end = html.rfind('U')
				html = html[begin + 13: end]
			break
    	wx.TheClipboard.Close()
    	try:
    		html.decode('utf8') 
    	except:
    		try:
    			html = html.decode('utf16').encode('utf8')
    		except:
    			pass
    			
	if html.strip() == '':
    		self.txtReship.SetValue(_('No webpage content is ready to reship, check if it has been copied correctly.'))
    		return
	
	html = prettify_html(html)
    	urls, text = parse_html_images(html)
    	tmptext = source_url.strip() + '\n' + parse_html_texts(text.strip())
    	html += SEPARATOR + tmptext + SEPARATOR
    	tmptext = re.sub(r'\[\[Image (\d+)[^\]]*\]\]', '\n\n%s\n\n' % MSG_FILE_UPLOADING_2, tmptext)
    	self.txtReship.SetValue(html.decode('utf8'))
	self.txtBody.SetValue(compress_spaces(tmptext).decode('utf8'))
    	if urls:
    		DownloadThread(self, urls, source_url)
    	else:
    		self.notebook.SetSelection(1)

    def OnlstUpFileRClick(self, evt):
	self.notebook.PopupMenu(self.ppmenu)#	print self.GetToolBar().GetSize()

    def OnPopupItemSelected(self, evt):
	menutext = self.ppmenu.FindItemById(evt.GetId()).GetText().replace('_', '&')
	for k, v in enumerate(LIST_CONTEXT_MENU):
		if v == menutext:
			break
	if k == 0:
		self.OnbtnBrowseClick(wx.CommandEvent())
	elif k == 1:
		dialog = wx.DirDialog(None, _('Choose a directory'), self.get_dialog_path(), style=wx.DD_DEFAULT_STYLE)
	    	if dialog.ShowModal() == wx.ID_OK:
			self.append_files([dialog.GetPath()])
			write_config('Upload', {'DefaultPath': dialog.GetPath()})
	    	dialog.Destroy()
	elif k == 3:
		while self.lstUpFile.GetSelectedItemCount() > 0:
			self.lstUpFile.DeleteItem(self.lstUpFile.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED))
	elif k == 4:
		total = self.lstUpFile.GetItemCount()
		for i in xrange(total - 1, 0, -1):
			for j in xrange(i):
				if self.lstUpFile.GetItem(i, 1).GetText() == self.lstUpFile.GetItem(j, 1).GetText():
					self.lstUpFile.DeleteItem(i)
					break
	elif k == 5:
		total = self.lstUpFile.GetItemCount()
		for i in xrange(total - 1, -1, -1):
			fname = self.lstUpFile.GetItem(i, 1).GetText()
			if invalid_file_name(fname) or not supported_file_type(fname):
				self.lstUpFile.DeleteItem(i)
	elif k == 7:
		self.lstUpFile.DeleteAllItems()
	self.list_re_number()
	self.lblProgress.SetLabel(MSG_FILE_SELECTED % self.lstUpFile.GetItemCount())
	
    def OnmnuLangClick(self, evt):
	lng = self.GetMenuBar().FindItemById(evt.GetId()).GetHelp()
	lng = lng.replace('__', '_')
	write_config('General', {'language': lng})
	wx.MessageBox(_('Language has changed. Restart to take effects.'))
	
    def on_iconify(self, evt):
        if read_config_bool('General', 'MinimizeToTray', False):
        	self.Hide()

    def OnClose(self, evt):
    	try:
		write_config('Upload', 
			{'UpZone': self.cmbZone.GetSelection(), \
			'UpBoard': self.cmbBoard.GetSelection(), \
			'UpBoardLock': self.chkLock.IsChecked(), \
			'PostSignature': self.txtSignature.GetValue(), \
			'PostZone': self.cmbPostZone.GetSelection(), \
			'PostBoard': self.cmbPostBoard.GetSelection(), \
			'ActivePage': self.notebook.GetSelection(), \
			'ColumnWidths': ','.join([str(self.lstUpFile.GetColumnWidth(col)) for col in xrange(self.lstUpFile.GetColumnCount())]), \
			})
		write_config('General', 
			{'WinWidth': self.GetSize().x, \
			'WinHeight': self.GetSize().y, \
			'WinMaximized': self.IsMaximized(), \
			'ToolbarStyle': self.GetToolBar().GetWindowStyleFlag(), \
			})
	except:
		wx.MessageBox(MSG_SAVE_SETTINGS_ERROR, MSG_ERROR, wx.ICON_ERROR)
	try:
		self.trayicon.Destroy()
	except:
		pass
	self.Destroy()

    def updateDisplay(self, msg):
        """
        Receives data from threads and updates the display
        """
        t = msg.data.strip()

	if t.startswith('Cookie|'):
		if t.find('No User') >= 0:
			self.btnUpload.Enable()
			self.to_upload = True
			self.show_login()
		elif t.split('|')[1] == '':
			self.start_upload_threads()
		else:
			tips = t.split('|')
			wx.MessageBox(tips[2], tips[1])
			self.btnUpload.Enable()
	elif t.startswith('Upload|'):
		self.finishcount += 1
		self.lblProgress.SetLabel('%s: %d / %d' % (_('Progress'), self.finishcount, self.lstUpFile.GetItemCount()))
		self.gagProgress.SetValue(self.finishcount * 100 / self.lstUpFile.GetItemCount())
		if self.finishcount >= self.lstUpFile.ItemCount:
			self.notebook.SetSelection(1)
			self.UploadedMode = True
			self.ReshipMode = False
			self.btnUpload.Enable()
			return
		if self.upcount < self.lstUpFile.ItemCount:
			self.upcount += 1
			UploadThread(self, self.get_host(), self.get_board_name(), self.upcount - 1, self.get_cookie(), self.get_new_host())
	elif t.startswith('Download|'):
		filenames=t.split('|')[1:]
		self.lstUpFile.DeleteAllItems()
	    	self.append_files(filenames)
	    	self.notebook.SetSelection(0)
	    	self.ReshipMode = True
	    	evt = wx.CommandEvent()
	    	self.OnbtnUploadClick(evt)
	elif t.startswith('Update|'):
		if t.split('|')[1] == '':
			if t.split('|')[2] == '':
				wx.MessageBox(_('Failed to check for updates, try again later.'), MSG_CHECK_UPDATE, wx.ICON_ERROR)
		else:
			if VERSION < '%s' % t.split('|')[1]:
				if wx.YES == wx.MessageBox(_('A new version %s is available! Would you like to update now?') % t.split('|')[1], MSG_CHECK_UPDATE, wx.YES_NO|wx.ICON_QUESTION):
					wx.LaunchDefaultBrowser(HOMEPAGE)
			else:
				if t.split('|')[2] == '':
					wx.MessageBox(_('You are using the latest version.'), MSG_CHECK_UPDATE, wx.ICON_INFORMATION)
	elif t.startswith('Logout|'):
		if t.split('|')[1] == 'OK':
			wx.MessageBox('%s %s' % (self.get_user_id(), _('has logged out.')), _('Logout'), wx.ICON_INFORMATION)
			remove_config('Login')
			update_title()
		else:
			tips = t.split('|')
			wx.MessageBox(tips[2], tips[1])


# end of class MyFrame

