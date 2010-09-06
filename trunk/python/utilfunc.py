# -*- coding: utf-8 -*-

import re
import wx
import urllib, urllib2

from consts import *
from httpredirect import *


def get_html_info(html):
	head = re.search(r'<title>(.*)</title>', html).group(1)
	body = re.search(r'<div[^>]*>(.*)</div>', html).group(1)
	body = re.sub(r'<[^>]*>', '', body)
	return head, body

def get_file_url(html):
	url = re.search(r'<url>(.*)</url>', html).group(1)
	return url

def get_update_info(html, key):
	val = re.search(r'%s=([^\r\n]*)' % key, html).group(1).strip()
	return val

def invalid_file_name(fname):
	try:
		open(fname, 'r')
	except:
		return True
	else:
		return False

def supported_file_type(fname):
	if re.match(r'.*\.(jpe?g|gif|png|pdf)$', fname, re.I):
		return True
	else:
		return False
		
def get_file_type(fname):
	try:
		ext = re.search(r'\.[\w\d]{1,4}$', fname, re.I).group(0)
	except:
		return ''
	else:
		return ext

def perfect_connect(window, url, post = {}, retry = False):
	req = urllib2.Request(url, post)
	cfg1 = wx.FileConfig(APPCODENAME)
	req.add_header('Cookie', cfg1.Read('/Login/Cookie'))
	try:		    
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError, e:  
		info = '%s|%s: %d' % ('Network Error', 'Error code', e.code)
		return info
	except:
		info = 'Error|Network Error.'
		return info
	else:
		the_page = resp.read().decode('gb18030').encode('utf8')
		if the_page.find('发生错误') >= 0:
			k, v = get_html_info(the_page)
			info = '|'.join([k, v])
			if retry or the_page.find('登录') < 0:
				return info
			else:
				host = cfg1.ReadInt('/Login/Host', 0)
				userid = cfg1.Read('/Login/UserID')
				pwd = cfg1.Read('/Login/Password')
				if userid and pwd:
					opener = urllib2.build_opener(SmartRedirectHandler())  
					urllib2.install_opener(opener)  
					req2 = urllib2.Request('http://%s/bbs/login' % BBS_HOSTS[host], urllib.urlencode({'id': userid, 'pw': pwd}))  
					try:
						resp2 = urllib2.urlopen(req2)  
					except urllib2.HTTPError, e:  
						info = '%s|%s: %d' % ('Network Error', 'Error code', e.code)
						return info
					except:
						info = 'Error|Network Error.'
						return info
					else:
						if resp2.code != 302:			
							the_page = resp2.read().decode('gb18030').encode('utf8')
							k, v = get_html_info(the_page)
							info = '|'.join([k, v])
							return info
						else:
							cookie = ';'.join(resp2.headers['set-cookie'].split(','))
							cfg1.Write('/Login/Cookie', cookie)
							return perfect_connect(window, url, post, True)
				else:
					return 'No User'
		else:
			return ''
