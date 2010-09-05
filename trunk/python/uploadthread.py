# -*- coding: utf-8 -*-

import urllib2
import wx
from threading import Thread
from wx.lib.pubsub import Publisher

from consts import *
from utilfunc import *
import MultipartPostHandler

class UploadThread(Thread):
    """Upload Thread."""
 
    def __init__(self, window, host, board, upindex, cookie):
        Thread.__init__(self)
	self.window = window
	self.host = host
	self.board = board
	self.upindex = upindex
	self.cookie = cookie
	self.start()
 
    def run(self):
	wx.CallAfter(self.PreUploadInfo)
	filename = self.window.list.GetItem(self.upindex, 1).GetText()
	req = urllib2.Request('http://%s/bbs/upload?b=%s' % (self.host, self.board))
	req.add_header('Cookie', self.cookie)
	opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
	self.upOK = False
	try:
		params = { 'up' : open(filename, 'rb') }
	except IOError:
		self.info = '%s: %s' % ('Fail', 'Invalid File or Not Permitted to Read')
	except:
		self.info = '%s: %s' % ('Fail', 'Unknown Error')
	else:
		try:
			the_page = opener.open(req, params).read().decode('gb18030').encode('utf8')
		except:
			self.info = '%s: %s' % ('Fail', 'Network Error')
		else:
			if the_page.find('发生错误') >= 0:
				head, body = get_html_info(the_page)
				self.info = '%s: %s' % (head, body)
			else:
				self.upOK = True
				self.info = 'OK'
				self.fileurl = get_file_url(the_page)
        wx.CallAfter(self.PostUploadInfo)
 
    def PreUploadInfo(self):
	self.window.list.SetStringItem(self.upindex, 3, 'Uploading', 1)
 
    def PostUploadInfo(self):
	if self.upOK:
		self.window.list.SetStringItem(self.upindex, 3, self.info, 2)
		content = self.window.postbody.GetValue()
		self.window.postbody.SetValue(content.replace('[File %d Uploading...]' % (self.upindex + 1), self.fileurl))
	else:
		self.window.list.SetStringItem(self.upindex, 3, self.info, 3)
	Publisher().sendMessage("update", '%s|' % 'Upload')

