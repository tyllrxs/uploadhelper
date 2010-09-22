# -*- coding: utf-8 -*-

import os, sys
import re
from xml.dom import minidom
import wx
from wx import xrc
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from DlgLogin import *
from DlgAbout import *
from logoutthread import *
from checkcookiethread import *
from uploadthread import *
from checkupdatethread import *
from downloadthread import *
from parsehtml import *
from ui.dialogs import *

class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
	wx.FileDropTarget.__init__(self)
	self.window = window

    def OnDropFiles(self, x, y, filenames):
	self.window.append_upload_files(filenames)

class MyFrame(wx.Frame):

    def __init__(self):
        self.res = xrc.XmlResource('ui/frmMain.xrc')
	self.frame = self.res.LoadFrame(None, 'frmMain')
	# load UI settings from config file
	self.menubar = self.res.LoadMenuBar('menubar1')
	self.menubar.SetAutoWindowMenu(False)
	self.menubar.FindItemById(xrc.XRCID('mnuAbout')).SetId(wx.ID_ABOUT)
	self.frame.SetMenuBar(self.menubar)
	self.toolbar = self.res.LoadToolBar(self.frame, 'toolbar1')
	self.frame.SetToolBar(self.toolbar)
	self.frame.SetSize(wx.Size(600, 600))
	self.frame.CenterOnScreen()
	self.notebook = xrc.XRCCTRL(self.frame, 'notebook')
	self.notebook.SetSelection(read_config_int('Upload', 'ActivePage', 0))
	if sys.platform == 'darwin':
		for page in xrange(self.notebook.GetPageCount()):
			self.notebook.SetPageImage(page, -1)
        self.zone = xrc.XRCCTRL(self.frame, 'cmbZone')
	self.postzone = xrc.XRCCTRL(self.frame, 'cmbPostZone')
        self.board = xrc.XRCCTRL(self.frame, 'cmbBoard')
	self.postboard = xrc.XRCCTRL(self.frame, 'cmbPostBoard')
	self.read_zones()
	self.zone.SetSelection(read_config_int('Upload', 'UpZone', 4))
	self.postzone.SetSelection(read_config_int('Upload', 'PostZone', 4))
	self.read_boards()
	self.board.SetSelection(read_config_int('Upload', 'UpBoard', 16))
	self.read_postboards()
	self.postboard.SetSelection(read_config_int('Upload', 'PostBoard', 16))
	self.lock = xrc.XRCCTRL(self.frame, 'chkLock')
	self.lock.SetValue(read_config_bool('Upload', 'UpBoardLock'))
	il = wx.ImageList(16,16, True)
	for name in ['alarm', 'process', 'ok', 'error']:
		bmp = wx.Bitmap('icon/indicator/%s.png' % name, wx.BITMAP_TYPE_PNG)
		il_max = il.Add(bmp)
	self.list = xrc.XRCCTRL(self.frame, 'lstUpFile')
	self.list.AssignImageList(il, wx.IMAGE_LIST_SMALL)
	for col, text in enumerate(['No.', _('Filename'), '%s (KB)' % _('Size'), _('Status')]):
		if col == 0 or col == 2:
			self.list.InsertColumn(col, text, wx.LIST_FORMAT_CENTER)
		else:
			self.list.InsertColumn(col, text, wx.LIST_FORMAT_LEFT)
	self.list.SetColumnWidth(0, 40)
	self.list.SetColumnWidth(1, 320)
	self.list.SetColumnWidth(2, 80)
	self.list.SetColumnWidth(3, 130)
	if sys.platform.startswith('win32'):
		self.list.SetColumnWidth(3, 100)
	self.progress = xrc.XRCCTRL(self.frame, 'lblProgress')
	self.progressnum = xrc.XRCCTRL(self.frame, 'gagProgress')
	self.uploadbutton = xrc.XRCCTRL(self.frame, 'btnUpload')
	self.posttitle = xrc.XRCCTRL(self.frame, 'txtTitle')
	self.signature = xrc.XRCCTRL(self.frame, 'txtSignature')
	self.signature.SetValue(read_config_int('Upload', 'PostSignature', 1))
	self.postbody = xrc.XRCCTRL(self.frame, 'txtBody')
	self.postbutton = xrc.XRCCTRL(self.frame, 'btnPost')
	self.reshipinfo = xrc.XRCCTRL(self.frame, 'txtReship')
	self.statusbar = xrc.XRCCTRL(self.frame, 'stsBar')
	self.statusbar.SetFields(STATUSBAR_INFO)
	# set some status variables
	self.PostedMode = False
	self.UploadedMode = False
	self.ReshipMode = False
	# bind events to UI controls
	self.frame.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
	self.frame.Bind(wx.EVT_MENU, self.OnmnuSwitchClick, id=xrc.XRCID('mnuSwitch'))
	self.frame.Bind(wx.EVT_TOOL, self.OnmnuSwitchClick, id=xrc.XRCID('tlbSwitch'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuLogoutClick, id=xrc.XRCID('mnuLogout'))
	self.frame.Bind(wx.EVT_TOOL, self.OnmnuLogoutClick, id=xrc.XRCID('tlbLogout'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuAlwaysOnTopClick, id=xrc.XRCID('mnuAlwaysOnTop'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuFAQClick, id=xrc.XRCID('mnuFAQ'))
	self.frame.Bind(wx.EVT_TOOL, self.OnmnuFAQClick, id=xrc.XRCID('tlbFAQ'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuHomepageClick, id=xrc.XRCID('mnuHomepage'))
	self.frame.Bind(wx.EVT_TOOL, self.OnmnuHomepageClick, id=xrc.XRCID('tlbHomepage'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuCheckUpdateClick, id=xrc.XRCID('mnuCheckUpdate'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuAboutClick, id=wx.ID_ABOUT)
        self.frame.Bind(wx.EVT_COMBOBOX, self.OnZoneChange, id=xrc.XRCID('cmbZone'))
	self.frame.Bind(wx.EVT_COMBOBOX, self.OnBoardChange, id=xrc.XRCID('cmbBoard'))
	self.frame.Bind(wx.EVT_COMBOBOX, self.OnPostZoneChange, id=xrc.XRCID('cmbPostZone'))
	self.frame.Bind(wx.EVT_CHECKBOX, self.OnchkLockClick, id=xrc.XRCID('chkLock'))
	self.frame.Bind(wx.EVT_BUTTON, self.OnbtnBrowseClick, id=xrc.XRCID('btnBrowse'))
	self.frame.Bind(wx.EVT_BUTTON, self.OnbtnUploadClick, id=xrc.XRCID('btnUpload'))
	self.frame.Bind(wx.EVT_BUTTON, self.OnbtnPostClick, id=xrc.XRCID('btnPost'))
	self.frame.Bind(wx.EVT_BUTTON, self.OnbtnReshipClick, id=xrc.XRCID('btnReship'))
	self.frame.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnlstUpFileRClick, id=xrc.XRCID('lstUpFile'))
	self.frame.Bind(wx.EVT_CLOSE, self.OnClose)
	# make the list control be a drop target
	dt = MyFileDropTarget(self)
	self.list.SetDropTarget(dt)
	# receive message from check for updates thread
	Publisher().subscribe(self.updateDisplay, "update")


    def read_zones(self):
        xmldoc = minidom.parse(FILE_BOARDS)
	num = 0
	for zone in xmldoc.getElementsByTagName('Zone'):
		self.zone.Append('%d) %s' % (num, zone.attributes['name'].value))
		self.postzone.Append('%d) %s' % (num, zone.attributes['name'].value))
		num = num + 1

    def read_boards(self):
	self.board.Clear()
        xmldoc = minidom.parse(FILE_BOARDS)
	for board in xmldoc.getElementsByTagName('Zone')[self.zone.GetSelection()].childNodes:
		if board.nodeType == board.ELEMENT_NODE:
			self.board.Append('%s (%s) [%s]' % (board.nodeName, board.attributes['name'].value, board.attributes['bid'].value))

    def read_postboards(self):
	self.postboard.Clear()
        xmldoc = minidom.parse(FILE_BOARDS)
	for board in xmldoc.getElementsByTagName('Zone')[self.postzone.GetSelection()].childNodes:
		if board.nodeType == board.ELEMENT_NODE:
			self.postboard.Append('%s (%s) [%s]' % (board.nodeName, board.attributes['name'].value, board.attributes['bid'].value))

    def get_board_name(self, post=False):
	if post:
		board = self.postboard.GetValue()
	else:
		board = self.board.GetValue()
	return re.compile('^(\S+)').search(board).group(1)

    def get_board_id(self, post=False):
	if post:
		board = self.postboard.GetValue()
	else:
		board = self.board.GetValue()
	return re.compile('\[(\d+)\]').search(board).group(1)

    def get_cookie(self):
	return read_config('Login', 'Cookie')

    def get_host(self):
	return BBS_HOSTS[read_config_int('Login', 'Host', 0)]

    def get_user_id(self):
	return read_config('Login', 'UserID')
	
    def get_auto_login(self):
	return read_config('Login', 'AutoLogin')
	
    def get_dialog_path(self):
	return read_config('Upload', 'DefaultPath')
	
    def OnCreate(self, evt):
    	self.frame.Unbind(wx.EVT_WINDOW_CREATE)
	if not (self.get_user_id() and self.get_auto_login()):
		dialog = DlgLogin()
		dialog.dialog.ShowModal()
		dialog.dialog.Destroy()
	if self.get_user_id():
		self.frame.SetTitle('%s [%s: %s]' % (APPNAME, _('User'), self.get_user_id()))
	else:
		self.frame.SetTitle(APPNAME)

    def OnmnuSwitchClick(self, evt):
	dialog = MyLoginDialog(self.frame)
	dialog.ShowModal()
	if self.get_user_id():
		self.frame.SetTitle('%s [%s: %s]' % (APPNAME, _('User'), self.get_user_id()))
	else:
		self.frame.SetTitle(APPNAME)
	
    def OnmnuLogoutClick(self, evt):
	LogoutThread(self.get_host(), self.get_cookie())

    def OnmnuAlwaysOnTopClick(self, evt):
	if evt.GetEventObject().IsChecked(evt.GetId()):
        	self.frame.SetWindowStyleFlag(self.frame.GetWindowStyleFlag() | wx.STAY_ON_TOP)
	else:
		self.frame.SetWindowStyleFlag(self.frame.GetWindowStyleFlag() ^ wx.STAY_ON_TOP)

    def OnmnuFAQClick(self, evt):
        wx.LaunchDefaultBrowser('%s%s' % (HOMEPAGE, 'faq.htm'))

    def OnmnuHomepageClick(self, evt):
        wx.LaunchDefaultBrowser(HOMEPAGE)

    def OnmnuCheckUpdateClick(self, evt):
        CheckUpdateThread()

    def OnmnuAboutClick(self, evt):
	dialog3 = MyAboutDialog(self.frame)
	dialog3.ShowModal()
	dialog3.Destroy()

    def OnZoneChange(self, evt):
	tmp = self.board.GetSelection()        
	self.read_boards()
	self.board.SetSelection(min(tmp, self.board.GetCount()-1))     
	self.postzone.SetSelection(self.zone.GetSelection())
	self.read_postboards()
	self.postboard.SetSelection(self.board.GetSelection())

    def OnBoardChange(self, evt):
        if self.postzone.GetSelection() != self.zone.GetSelection():
		self.OnZoneChange(evt)
	else:
		self.postboard.SetSelection(self.board.GetSelection())

    def OnPostZoneChange(self, evt):
	tmp = self.postboard.GetSelection()        
	self.read_postboards()
	self.postboard.SetSelection(min(tmp, self.postboard.GetCount()-1))    

    def OnchkLockClick(self, evt):
	self.zone.Enabled = not self.lock.IsChecked()
	self.board.Enabled = not self.lock.IsChecked()

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
		self.append_upload_files(dialog.GetPaths())
		write_config('Upload', {'DefaultPath': os.path.abspath(os.path.dirname(dialog.GetPaths()[0]))})
	dialog.Destroy()
	
    def append_upload_files(self, filenames):
    	if self.UploadedMode:
    		self.list.DeleteAllItems()
    		self.UploadedMode = False
	for f in filenames:
		if os.path.isdir(f):
			self.append_upload_files(search_files(f, r'\.(jpe?g|gif|png|pdf)$'))
			continue
		index = self.list.InsertStringItem(sys.maxint, '%s' % (self.list.GetItemCount() + 1))
		self.list.SetStringItem(index, 1, f)
		try:
			fz = os.path.getsize(f) / 1024
		except:
			fz = -1
		self.list.SetStringItem(index, 2, '%ld' % fz)
		if invalid_file_name(f):
			self.list.SetStringItem(index, 3, MSG_INVALID_FILE, 0)
			self.list.SetItemTextColour(index, wx.RED)
		elif not supported_file_type(f):
			self.list.SetStringItem(index, 3, MSG_UNSUPPORTED_FORMAT, 0)
			self.list.SetItemTextColour(index, wx.RED)
		elif fz > 1024:
			self.list.SetStringItem(index, 3, MSG_ENTITY_TOO_LARGE, 0)
			self.list.SetItemTextColour(index, wx.BLUE)
	self.progress.SetLabel(_('%d File(s) Selected') % self.list.GetItemCount())    	

    def OnbtnUploadClick(self, evt):
	self.progress.SetLabel('%s: %d / %d' % (_('Progress'), 0, self.list.GetItemCount()))
	self.progressnum.SetValue(0)
	if self.list.GetItemCount() <= 0:
		wx.MessageBox(_('Select at least one file for uploading.'))
		return
	self.uploadbutton.Disable()
	if self.PostedMode:
		self.postbody.SetValue('')
		self.PostedMode = False
	CheckCookieThread(self)
	
    def start_upload_threads(self):
	self.upcount = 0
	self.finishcount = 0
	if not self.ReshipMode:
		for i in xrange(self.list.GetItemCount()):
			self.postbody.SetValue(self.postbody.GetValue() + '\n%s\n' % MSG_FILE_UPLOADING % (i + 1))
	for i in range(0, 3):
		if i < self.list.GetItemCount():
			self.upcount += 1
			UploadThread(self, self.get_host(), self.get_board_name(), i, self.get_cookie())

    def list_re_number(self):
	for i in xrange(self.list.GetItemCount()):
		self.list.SetStringItem(i, 0, str(i+1))

    def OnbtnPostClick(self, evt):
	self.list.DeleteAllItems()
	self.progress.SetLabel(MSG_FILE_SELECTED % 0)
	self.progressnum.SetValue(0)
	if self.posttitle.GetValue().strip() == '' or self.postbody.GetValue().strip() == '':
		wx.MessageBox(MSG_FILL_BLANKS)
		return
	self.postbutton.Disable()
	info = perfect_connect('http://%s/bbs/snd?bid=%s' % (self.get_host(), self.get_board_id(True)),
		urllib.urlencode({'title': self.posttitle.GetValue().encode('gb18030'), 
				'signature': self.signature.GetValue(),
				'text': self.postbody.GetValue().encode('gb18030')}))
	if info == '':
		wx.MessageBox(_('Post Successfully to Board "%s".') % self.get_board_name(True))
		self.PostedMode = True
	elif info.find('No User') >= 0:
		evt = wx.CommandEvent()
		self.OnmnuSwitchClick(evt)
		self.OnbtnPostClick(evt)
	else:
		tips = info.split('|')
		wx.MessageBox(tips[1], tips[0])
	self.postbutton.Enable()

    def OnbtnReshipClick(self, evt):
        if not wx.TheClipboard.IsOpened():
		wx.TheClipboard.Open()
	do = wx.CustomDataObject('text/html')
        success = wx.TheClipboard.GetData(do)
    	wx.TheClipboard.Close()
    	try: 
    		html = do.GetData().decode('utf16') #Firefox
    	except:
    		try:
    			html = do.GetData().decode('utf8') #Chrome
    		except:
    			wx.MessageBox('Unknown Format')
    			return
    	if html.strip() == '':
    		self.reshipinfo.SetValue(_('(No webpage content is ready to reship, check if it has been copied correctly.)'))
    		return
    	self.reshipinfo.SetValue(prettify_html(html))
    	self.reshipinfo.AppendText(SEPARATOR)
    	urls, html = parse_html_images(html)
    	html = parse_html_texts(html)
    	self.reshipinfo.AppendText(html)
    	self.reshipinfo.AppendText(SEPARATOR)
    	self.postbody.SetValue(re.sub(r'\[\[Image (\d+)[^\]]*\]\]', '\n%s\n' % MSG_FILE_UPLOADING_2, html))
    	DownloadThread(self, urls)

    def OnlstUpFileRClick(self, evt):
	self.popupmenu = wx.Menu()
	for text in LIST_CONTEXT_MENU:
		if len(text) <= 0:
			self.popupmenu.AppendSeparator()
		else:
			item = self.popupmenu.Append(-1, text)
			self.frame.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
	pos = evt.GetPosition()
	self.list.PopupMenu(self.popupmenu, pos)
	self.popupmenu.Destroy()

    def OnPopupItemSelected(self, evt):
	menutext = self.popupmenu.FindItemById(evt.GetId()).GetText().replace('_', '&')
	for k, v in enumerate(LIST_CONTEXT_MENU):
		if v == menutext:
			break
	if k == 0:
		self.OnbtnBrowseClick(wx.CommandEvent())
	elif k == 1:
		dialog = wx.DirDialog(None, _('Choose a directory'), self.get_dialog_path(), style=wx.DD_DEFAULT_STYLE)
	    	if dialog.ShowModal() == wx.ID_OK:
			self.append_upload_files([dialog.GetPath()])
			write_config('Upload', {'DefaultPath': dialog.GetPath()})
	    	dialog.Destroy()
	elif k == 3:
		while self.list.GetSelectedItemCount() > 0:
			self.list.DeleteItem(self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED))
	elif k == 4:
		total = self.list.GetItemCount()
		for i in xrange(total - 1, 0, -1):
			for j in xrange(i):
				if self.list.GetItem(i, 1).GetText() == self.list.GetItem(j, 1).GetText():
					self.list.DeleteItem(i)
					break
	elif k == 5:
		total = self.list.GetItemCount()
		for i in xrange(total - 1, -1, -1):
			fname = self.list.GetItem(i, 1).GetText()
			if invalid_file_name(fname) or not supported_file_type(fname):
				self.list.DeleteItem(i)
	elif k == 7:
		self.list.DeleteAllItems()
	self.list_re_number()
	self.progress.SetLabel(MSG_FILE_SELECTED % self.list.GetItemCount())

    def OnClose(self, evt):
	write_config('Upload', {'UpZone': self.zone.GetSelection(), \
		'UpBoard': self.board.GetSelection(), \
		'UpBoardLock': self.lock.IsChecked(), \
		'PostSignature': self.signature.GetValue(), \
		'PostZone': self.postzone.GetSelection(), \
		'PostBoard': self.postboard.GetSelection(), \
		'ActivePage': self.notebook.GetSelection()})
	self.frame.Destroy()

    #----------------------------------------------------------------------
    def updateDisplay(self, msg):
        """
        Receives data from threads and updates the display
        """
        t = msg.data.strip()

	if t.startswith('Cookie|'):
		if t.find('No User') >= 0:
			evt = wx.CommandEvent()
			self.OnmnuSwitchClick(evt)
			self.uploadbutton.Enable()
		elif t.split('|')[1] == '':
			self.start_upload_threads()
		else:
			tips = t.split('|')
			wx.MessageBox(tips[2], tips[1])
			self.uploadbutton.Enable()
	elif t.startswith('Upload|'):
		self.finishcount += 1
		self.progress.SetLabel('%s: %d / %d' % (_('Progress'), self.finishcount, self.list.GetItemCount()))
		self.progressnum.SetValue(self.finishcount * 100 / self.list.GetItemCount())
		if self.finishcount >= self.list.ItemCount:
			self.notebook.SetSelection(1)
			self.UploadedMode = True
			self.ReshipMode = False
			self.uploadbutton.Enable()
			return
		if self.upcount < self.list.ItemCount:
			self.upcount += 1
			UploadThread(self, self.get_host(), self.get_board_name(), self.upcount - 1, self.get_cookie())
	elif t.startswith('Download|'):
		filenames=t.split('|')[1:]
		self.list.DeleteAllItems()
	    	self.append_upload_files(filenames)
	    	self.notebook.SetSelection(0)
	    	self.ReshipMode = True
	    	evt = wx.CommandEvent()
	    	self.OnbtnUploadClick(evt)
	elif t.startswith('Update|'):
		if t.split('|')[1] == '':
			wx.MessageBox(_('Failed to check for updates, try again later.'), MSG_CHECK_UPDATE)
		else:
			if VERSION < '%s' % t.split('|')[1]:
				if wx.YES == wx.MessageBox(_('A new version %s is available!\nWould you like to update now?') % t, MSG_CHECK_UPDATE, wx.YES_NO):
					wx.LaunchDefaultBrowser(HOMEPAGE)
			else:
				wx.MessageBox(_('You are using the latest version.'), MSG_CHECK_UPDATE)
	elif t.startswith('Logout|'):
		if t.split('|')[1] == 'OK':
			wx.MessageBox(_('User "%s" has logged out.') % self.get_user_id())
			remove_config('Login')
			self.frame.SetTitle(APPNAME)
		else:
			tips = t.split('|')
			wx.MessageBox(tips[2], tips[1])

