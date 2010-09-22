# -*- coding: utf-8 -*-

import sys
if sys.platform.startswith('win32'):
	reload(sys)
	sys.setdefaultencoding('latin1')

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
	self.fileurl = ''
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
		self.info = '%s: %s' % (MSG_FAIL, MSG_INVALID_FILE)
	except:
		self.info = '%s: %s' % (MSG_FAIL, MSG_UNKNOWN_ERROR)
	else:
		try:
			the_page = opener.open(req, params).read().decode('gb18030').encode('utf8')
		except urllib2.HTTPError, e:
			if e.code == 413:
                        	self.info = '%s: %s' % (MSG_FAIL, MSG_ENTITY_TOO_LARGE)
                        elif e.code == 400:
                        	self.info = '%s: %s' % (MSG_FAIL, MSG_UNSUPPORTED_FORMAT)
                        else:
                        	self.info = '%s: %s %d' % (MSG_FAIL, MSG_ERROR_CODE, e.code)
                except Exception, e:
			self.info = '%s: %s' % (MSG_FAIL, MSG_NETWORK_ERROR)
			print e
		else:
			if the_page.find(u'发生错误') >= 0:
				head, body = get_html_info(the_page)
				self.info = '%s: %s' % (head, body)
			else:
				self.upOK = True
				self.info = STATUS_UPLOADED
				self.fileurl = get_file_url(the_page)
        wx.CallAfter(self.PostUploadInfo)
 
    def PreUploadInfo(self):
	self.window.list.SetStringItem(self.upindex, 3, STATUS_UPLOADING, 1)
 
    def PostUploadInfo(self):
	if self.upOK:
		self.window.list.SetStringItem(self.upindex, 3, self.info, 2)
		self.window.list.SetItemTextColour(self.upindex, wx.BLACK)
	else:
		self.window.list.SetStringItem(self.upindex, 3, self.info, 3)
		self.window.list.SetItemTextColour(self.upindex, wx.RED)
	content = self.window.postbody.GetValue()
	self.window.postbody.SetValue(content.replace(MSG_FILE_UPLOADING % (self.upindex + 1), self.fileurl))
	Publisher().sendMessage("update", '%s|' % 'Upload')

