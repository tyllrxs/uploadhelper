# -*- coding: utf-8 -*-

import os, sys, glob
import re
from xml.dom import minidom
import wx
from wx import xrc
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from DlgLogin import *
from DlgAbout import *
from checkcookiethread import *
from uploadthread import *
from checkupdatethread import *

class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
	wx.FileDropTarget.__init__(self)
	self.window = window

    def OnDropFiles(self, x, y, filenames):
	for f in filenames:
		index = self.window.InsertStringItem(sys.maxint, '%s' % (self.window.GetItemCount() + 1))
		self.window.SetStringItem(index, 1, f)
		fz = os.path.getsize(f) / 1024
		self.window.SetStringItem(index, 2, '%ld' % fz)
		if fz > 1024:
			self.window.SetStringItem(index, 3, 'Too Large', 0)
			self.window.SetItemTextColour(index, wx.RED);

class MyFrame(wx.Frame):

    def __init__(self):
        self.res = xrc.XmlResource('ui/frmMain.xrc')
	self.frame = self.res.LoadFrame(None, 'frmMain')
	# load UI settings from config file
	cfg1 = wx.FileConfig(APPCODENAME)
	self.frame.SetSize(wx.Size(600,600))
	self.notebook = xrc.XRCCTRL(self.frame, 'notebook')
	self.notebook.SetSelection(cfg1.ReadInt('/Upload/ActivePage', 0))
        self.zone = xrc.XRCCTRL(self.frame, 'cmbZone')
	self.postzone = xrc.XRCCTRL(self.frame, 'cmbPostZone')
        self.board = xrc.XRCCTRL(self.frame, 'cmbBoard')
	self.postboard = xrc.XRCCTRL(self.frame, 'cmbPostBoard')
	self.read_zones()
	self.zone.SetSelection(cfg1.ReadInt('/Upload/UpZone', 4))
	self.postzone.SetSelection(cfg1.ReadInt('/Upload/PostZone', 4))
	self.read_boards()
	self.board.SetSelection(cfg1.ReadInt('/Upload/UpBoard', 16))
	self.read_postboards()
	self.postboard.SetSelection(cfg1.ReadInt('/Upload/PostBoard', 16))
	self.lock = xrc.XRCCTRL(self.frame, 'chkLock')
	self.lock.SetValue(cfg1.ReadInt('/Upload/UpBoardLock', 0))
	il = wx.ImageList(16,16, True)
	for name in glob.glob('icon/indicator/*.png'):
		bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
		il_max = il.Add(bmp)
	self.list = xrc.XRCCTRL(self.frame, 'lstUpFile')
	self.list.AssignImageList(il, wx.IMAGE_LIST_SMALL)
	for col, text in enumerate(['No.', 'Filename', 'Size (KB)', 'Status']):
		if col == 0 or col == 2:
			self.list.InsertColumn(col, text, wx.LIST_FORMAT_CENTER)
		else:
			self.list.InsertColumn(col, text, wx.LIST_FORMAT_LEFT)
	self.list.SetColumnWidth(0, 40)
	self.list.SetColumnWidth(1, 320)
	self.list.SetColumnWidth(2, 80)
	self.list.SetColumnWidth(3, 130)
	self.progress = xrc.XRCCTRL(self.frame, 'lblProgress')
	self.progressnum = xrc.XRCCTRL(self.frame, 'gagProgress')
	self.uploadbutton = xrc.XRCCTRL(self.frame, 'btnUpload')
	self.posttitle = xrc.XRCCTRL(self.frame, 'txtTitle')
	self.signature = xrc.XRCCTRL(self.frame, 'txtSignature')
	self.signature.SetValue(cfg1.ReadInt('/Upload/PostSignature', 1))
	self.postbody = xrc.XRCCTRL(self.frame, 'txtBody')
	self.postbutton = xrc.XRCCTRL(self.frame, 'btnPost')
	self.statusbar = xrc.XRCCTRL(self.frame, 'stsBar')
	self.statusbar.SetFields(STATUSBAR_INFO)
	# set some status variables
	self.hasPosted = False
	# bind events to UI controls
	self.frame.Bind(wx.EVT_MENU, self.OnmnuSwitchClick, id=xrc.XRCID('mnuSwitch'))
	self.frame.Bind(wx.EVT_TOOL, self.OnmnuSwitchClick, id=xrc.XRCID('tlbSwitch'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuAlwaysOnTopClick, id=xrc.XRCID('mnuAlwaysOnTop'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuFAQClick, id=xrc.XRCID('mnuFAQ'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuHomepageClick, id=xrc.XRCID('mnuHomepage'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuCheckUpdateClick, id=xrc.XRCID('mnuCheckUpdate'))
	self.frame.Bind(wx.EVT_MENU, self.OnmnuAboutClick, id=xrc.XRCID('mnuAbout'))
        self.frame.Bind(wx.EVT_COMBOBOX, self.OnZoneChange, id=xrc.XRCID('cmbZone'))
	self.frame.Bind(wx.EVT_COMBOBOX, self.OnBoardChange, id=xrc.XRCID('cmbBoard'))
	self.frame.Bind(wx.EVT_COMBOBOX, self.OnPostZoneChange, id=xrc.XRCID('cmbPostZone'))
	self.frame.Bind(wx.EVT_CHECKBOX, self.OnchkLockClick, id=xrc.XRCID('chkLock'))
	self.frame.Bind(wx.EVT_BUTTON, self.OnbtnBrowseClick, id=xrc.XRCID('btnBrowse'))
	self.frame.Bind(wx.EVT_BUTTON, self.OnbtnUploadClick, id=xrc.XRCID('btnUpload'))
	self.frame.Bind(wx.EVT_BUTTON, self.OnbtnPostClick, id=xrc.XRCID('btnPost'))
	self.frame.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnlstUpFileRClick, id=xrc.XRCID('lstUpFile'))
	self.frame.Bind(wx.EVT_CLOSE, self.OnClose)
	# make the list control be a drop target
	dt = MyFileDropTarget(self.list)
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
	cfg1 = wx.FileConfig(APPCODENAME)
	return cfg1.Read('/Login/Cookie', '')

    def get_host(self):
	cfg1 = wx.FileConfig(APPCODENAME)
	return BBS_HOSTS[cfg1.ReadInt('/Login/Host', 0)]

    def OnmnuSwitchClick(self, evt):
	dialog = DlgLogin()
	dialog.dialog.ShowModal()

    def OnmnuAlwaysOnTopClick(self, evt):
	if evt.GetEventObject().IsChecked(evt.GetId()):
        	self.frame.SetWindowStyleFlag(self.frame.GetWindowStyleFlag() | wx.STAY_ON_TOP)
	else:
		self.frame.SetWindowStyleFlag(self.frame.GetWindowStyleFlag() ^ wx.STAY_ON_TOP)

    def OnmnuFAQClick(self, evt):
        wx.LaunchDefaultBrowser('%sfaq.htm' % HOMEPAGE)

    def OnmnuHomepageClick(self, evt):
        wx.LaunchDefaultBrowser(HOMEPAGE)

    def OnmnuCheckUpdateClick(self, evt):
        CheckUpdateThread()

    def OnmnuAboutClick(self, evt):
	try:
		dialog3 = DlgAbout()
		dialog3.dialog.ShowModal()
	finally:
		dialog3.dialog.Destroy()

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
	wildcard = 'All Supported Files (*.jpg;*.gif;*.png;*.pdf)|*.[Jj][Pp][Gg];*.gif;*.png;*.pdf|'\
		'Image Files (*.jpg;*.gif;*.png)|*.jpg;*.gif;*.png|'\
		'PDF Files (*.pdf)|*.pdf|'\
		'All Files (*.*)|*.*'
	dialog = wx.FileDialog(None, 'Select Files to Upload', '', '', wildcard, wx.OPEN|wx.MULTIPLE)
	if dialog.ShowModal() == wx.ID_OK:
		for f in dialog.GetPaths():
			index = self.list.InsertStringItem(sys.maxint, '%s' % (self.list.GetItemCount() + 1))
			self.list.SetStringItem(index, 1, f)
			fz = os.path.getsize(f) / 1024
			self.list.SetStringItem(index, 2, '%ld' % fz)
			if fz > 1024:
				self.list.SetStringItem(index, 3, 'Too Large', 0)
				self.list.SetItemTextColour(index, wx.RED);
		self.progress.SetLabel('%d File(s) Selected' % self.list.GetItemCount())
	dialog.Destroy()

    def OnbtnUploadClick(self, evt):
	if self.list.GetItemCount() <= 0:
		wx.MessageBox('Select at least one file for uploading.')
		return
	self.uploadbutton.Disable()
	if self.hasPosted:
		self.postbody.SetValue('')
		self.hasPosted = False
	CheckCookieThread(self.get_host(), self.get_board_name(), self.get_cookie())
	
    def start_upload_threads(self):
	self.upcount = 0
	self.finishcount = 0
	for i in xrange(self.list.GetItemCount()):
		self.postbody.SetValue(self.postbody.GetValue() + '\n%s\n' % '[File %d Uploading...]' % (i + 1))
	for i in range(0, 3):
		if i < self.list.GetItemCount():
			self.upcount += 1
			UploadThread(self, self.get_host(), self.get_board_name(), i, self.get_cookie())

    def list_re_number(self):
	for i in xrange(self.list.GetItemCount()):
		self.list.SetStringItem(i, 0, str(i+1))

    def OnbtnPostClick(self, evt): 
	if self.posttitle.GetValue().strip() == '' or self.postbody.GetValue().strip() == '':
		wx.MessageBox('No empty title or content is allowed.')
		return
	self.postbutton.Disable()
	self.list.DeleteAllItems()
	cfg1 = wx.FileConfig(APPCODENAME)
	self.host = cfg1.ReadInt('/Login/Host', 0)
	self.cookie = cfg1.Read('/Login/Cookie', '')
	req = urllib2.Request('http://%s/bbs/snd?bid=%s' % (BBS_HOSTS[self.host], self.get_board_id(True)),
		urllib.urlencode({'title': self.posttitle.GetValue().encode('gb18030'), 
				'signature': self.signature.GetValue(),
				'text': self.postbody.GetValue().encode('gb18030')}))
	req.add_header('Cookie', self.cookie)  
	try:
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError, e:  
		wx.MessageBox('%s: %d' % ('Error code', e.code), 'Network Error') 
	except:
		wx.MessageBox('Network Error')
	else:
		the_page = resp.read().decode('gb18030').encode('utf8')
		if the_page.find('发生错误') >= 0:
			head, body = get_html_info(the_page)
			wx.MessageBox(body, head)
		else:
			wx.MessageBox('Post Successfully to Board "%s".' % self.get_board_name(True))
			self.hasPosted = True
	self.postbutton.Enable()

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
	elif k == 3:
		while self.list.GetSelectedItemCount() > 0:
			self.list.DeleteItem(self.list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED))
	else:
		self.list.DeleteAllItems()
	self.list_re_number()
	self.progress.SetLabel('%d File(s) Selected' % self.list.GetItemCount())

    def OnClose(self, evt):
	cfg1 = wx.FileConfig(APPCODENAME)
	cfg1.WriteInt('/Upload/UpZone', self.zone.GetSelection())
	cfg1.WriteInt('/Upload/UpBoard', self.board.GetSelection())
	cfg1.WriteInt('/Upload/UpBoardLock', self.lock.IsChecked())
	cfg1.WriteInt('/Upload/PostSignature', self.signature.GetValue())
	cfg1.WriteInt('/Upload/PostZone', self.postzone.GetSelection())
	cfg1.WriteInt('/Upload/PostBoard', self.postboard.GetSelection())
	cfg1.WriteInt('/Upload/ActivePage', self.notebook.GetSelection())
	self.frame.Destroy()

    #----------------------------------------------------------------------
    def updateDisplay(self, msg):
        """
        Receives data from threads and updates the display
        """
        t = msg.data.strip()

	if t.startswith('Cookie|'):
		if t.split('|')[1] == 'OK':
			self.start_upload_threads()
		else:
			tips = t.split('|')
			wx.MessageBox(tips[2], tips[1])
			self.uploadbutton.Enable()
	elif t.startswith('Upload|'):
		self.finishcount += 1
		self.progress.SetLabel('Progress: %d / %d' % (self.finishcount, self.list.GetItemCount()))
		self.progressnum.SetValue(self.finishcount * 100 / self.list.GetItemCount())
		if self.finishcount >= self.list.ItemCount:
			self.notebook.SetSelection(1)
			self.uploadbutton.Enable()
			return
		if self.upcount < self.list.ItemCount:
			self.upcount += 1
			UploadThread(self, self.get_host(), self.get_board_name(), self.upcount - 1, self.get_cookie())
	elif t.startswith('Update|'):
		if t.split('|')[1] == '':
			wx.MessageBox('Failed to check for updates. Please try again later.', 'Check for Updates')
		else:
			if VERSION < '%s' % t.split('|')[1]:
				if wx.YES == wx.MessageBox('A new version %s is available!\nWould you like to update now?' % t, 'Check for Updates', wx.YES_NO):
					wx.LaunchDefaultBrowser(HOMEPAGE)
			else:
				wx.MessageBox('You are using the latest version.', 'Check for Updates')
