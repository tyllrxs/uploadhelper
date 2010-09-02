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
	cfg1 = wx.FileConfig(APPCODENAME)
	self.host = xrc.XRCCTRL(self.dialog, 'cmbHost')
	for item in BBS_HOSTS:
		self.host.Append(item)
	self.host.SetSelection(cfg1.ReadInt('/Login/Host', 0))
	self.user = xrc.XRCCTRL(self.dialog, 'txtUser')
	self.user.SetValue(cfg1.Read('/Login/UserID'))
	self.pwd = xrc.XRCCTRL(self.dialog, 'txtPwd')
	self.pwd.SetValue(cfg1.Read('/Login/Password'))
	self.autologin = xrc.XRCCTRL(self.dialog, 'chkAutoLogin')
	self.autologin.SetValue(cfg1.ReadInt('/Login/AutoLogin', 1))
	self.dialog.Bind(wx.EVT_BUTTON, self.OnbtnLoginClick, id=xrc.XRCID('btnLogin'))
	self.dialog.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnbtnLoginClick(self, evt):
	host = self.host.GetSelection()
	userid = self.user.GetValue().strip()
	pwd = self.pwd.GetValue().strip()
	autologin = self.autologin.GetValue()
	if userid == '' or pwd == '':
		wx.MessageBox('Fill the blanks first.')
		return
	opener = urllib2.build_opener(SmartRedirectHandler())  
	urllib2.install_opener(opener)  
	req = urllib2.Request('http://%s/bbs/login' % BBS_HOSTS[host], urllib.urlencode({'id': userid, 'pw': pwd}))  
	try:
		resp = urllib2.urlopen(req)  
	except urllib2.HTTPError, e:  
		wx.MessageBox('%s: %d' % ('Error code', e.code), 'Network Error') 
		return
	except:
		wx.MessageBox('Network Error')
		return
	else:
		if resp.code != 302:			
			the_page = resp.read().decode('gb18030').encode('utf8')
			head, body = get_html_info(the_page)
			wx.MessageBox(body, head)
			return
		else:
			cookie = ';'.join(resp.headers['set-cookie'].split(','))
			cfg1 = wx.FileConfig(APPCODENAME)
			if autologin:
				cfg1.Write('/Login/UserID', userid)
				cfg1.Write('/Login/Password', pwd)
				cfg1.Write('/Login/Cookie', cookie)
			else:
				if cfg1.HasGroup('Login'):
					cfg1.DeleteGroup('Login')
			cfg1.WriteInt('/Login/Host', host)
			cfg1.WriteInt('/Login/AutoLogin', autologin)
			wx.MessageBox('Login OK. Prepare to upload files.')
			self.dialog.Close()

    def OnClose(self, evt):
	self.dialog.Destroy()

