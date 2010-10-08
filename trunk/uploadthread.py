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
from imagemanipulation import *
import MultipartPostHandler

class UploadThread(Thread):
    """Upload Thread."""
 
    def __init__(self, window, upindex):
        Thread.__init__(self)
	self.window = window
	self.upindex = upindex
	self.fileurl = ''
	self.upOK = False
	self.start()
 
    def run(self):
	filename = self.window.lstUpFile.GetItem(self.upindex, 1).GetText()
	original = filename
	
	if is_image_file(filename) and self.window.enable_resize:
		sz = long(self.window.lstUpFile.GetItem(self.upindex, 2).GetText())
		if (not self.window.resize_larger) or (sz > self.window.resize_larger_than):
			wx.CallAfter(self.PreUploadInfo, STATUS_RESIZING)
			newfile = do_resize(filename, self.window.resize_width, self.window.resize_height, self.window.resize_quality)
			if newfile:
				filename = newfile
		
	if is_image_file(filename) and self.window.enable_watermark:
		wx.CallAfter(self.PreUploadInfo, STATUS_ADDING_WATERMARK)
		if self.window.watermark_type == 0:
			newfile = signature(filename, self.window.watermark_text, self.window.watermark_text_position,
					self.window.watermark_text_padding, self.window.watermark_text_font,
					self.window.watermark_text_size, self.window.watermark_text_color, True)
		else:
			newfile = watermark(filename, self.window.watermark_image, self.window.watermark_image_position,
					self.window.watermark_image_padding, self.window.watermark_image_opacity, True)
		if newfile:
			filename = newfile
	
	if is_jpeg_file(filename) and self.window.preserve_exif:
		wx.CallAfter(self.PreUploadInfo, STATUS_RESTORING_EXIF)
		newfile = copy_exif(filename, original, False)
		if newfile:
			filename = newfile
	
	# EXIF must be the last step to avoid overwritten	
	if is_jpeg_file(filename) and self.window.enable_exif:
		wx.CallAfter(self.PreUploadInfo, STATUS_WRITING_EXIF)
		newfile = process_exif(filename, self.window.exif_dict, self.window.thumbnail, False, False, False)
		if newfile:
			filename = newfile
	
	if not self.window.no_upload:
		# uploading start now!	
		wx.CallAfter(self.PreUploadInfo, STATUS_UPLOADING)			
		req = urllib2.Request('http://%s/bbs/upload?b=%s' % (self.window.host, self.window.board))
		req.add_header('Cookie', self.window.cookie)
		if self.window.proxy:
			opener = urllib2.build_opener(urllib2.ProxyHandler({'http':self.window.proxy}), MultipartPostHandler.MultipartPostHandler)
		else:
			opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
		try:
			params = { 'up' : open(filename, 'rb') }
		except IOError:
			self.info = '%s: %s' % (MSG_FAIL, MSG_INVALID_FILE)
		except:
			self.info = '%s: %s' % (MSG_FAIL, MSG_UNKNOWN_ERROR)
		else:
			try:
				the_page = opener.open(req, params).read().decode('gb18030')
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
					self.fileurl = get_file_url(the_page, self.window.newhost)
	else:
		self.info = _('No Upload')
        wx.CallAfter(self.PostUploadInfo)
 
    def PreUploadInfo(self, msg):
	self.window.lstUpFile.SetStringItem(self.upindex, 3, msg, 1)
 
    def PostUploadInfo(self):
	if self.upOK:
		self.window.lstUpFile.SetStringItem(self.upindex, 3, self.info, 2)
		self.window.lstUpFile.SetItemTextColour(self.upindex, wx.BLACK)
	else:
		self.window.upload_fails += 1
		self.window.lstUpFile.SetStringItem(self.upindex, 3, self.info, 3)
		self.window.lstUpFile.SetItemTextColour(self.upindex, wx.RED)
	content = self.window.txtBody.GetValue()
	self.window.txtBody.SetValue(content.replace(MSG_FILE_UPLOADING % (self.upindex + 1), self.fileurl))
	Publisher().sendMessage("update", '%s|' % 'Upload')

