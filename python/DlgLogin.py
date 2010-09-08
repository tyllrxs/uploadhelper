# -*- coding: utf-8 -*-

import urllib, urllib2, cookielib
import wx
from wx import xrc

from consts import *
from httpredirect import *
from utilfunc import *

class DlgLogin(wx.Dialog):
    def __init__(self):
        self.res = xrc.XmlResource('ui/dlgLogin.xrc')
	self.dialog = self.res.LoadDialog(None, 'dlgLogin')
	self.host = xrc.XRCCTRL(self.dialog, 'cmbHost')
	for item in BBS_HOSTS:
		self.host.Append(item)
	self.host.SetSelection(read_config_int('Login', 'Host', 0))
	self.user = xrc.XRCCTRL(self.dialog, 'txtUser')
	self.user.SetValue(read_config('Login', 'UserID'))
	self.pwd = xrc.XRCCTRL(self.dialog, 'txtPwd')
	self.pwd.SetValue(read_config('Login', 'Password'))
	self.autologin = xrc.XRCCTRL(self.dialog, 'chkAutoLogin')
	self.autologin.SetValue(read_config_bool('Login', 'AutoLogin', True))
	self.dialog.Bind(wx.EVT_BUTTON, self.OnbtnLoginClick, id=xrc.XRCID('btnLogin'))
	self.dialog.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnbtnLoginClick(self, evt):
	host = self.host.GetSelection()
	userid = self.user.GetValue().strip()
	pwd = self.pwd.GetValue().strip()
	autologin = self.autologin.IsChecked()
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
			the_page = resp.read().decode('gb18030').encode('utf8')
			head, body = get_html_info(the_page)
			wx.MessageBox(body, head)
			return
		else:
			cookie = ';'.join(resp.headers['set-cookie'].split(','))
			write_config('Login', {'UserID': userid, 'Password': pwd, 'Cookie': cookie, 'Host': host, 'AutoLogin': autologin})
			wx.MessageBox(_('Login OK. Prepare to upload files.'))
			self.dialog.Close()

    def OnClose(self, evt):
	self.dialog.Destroy()

