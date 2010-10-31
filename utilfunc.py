# -*- coding: utf-8 -*-

import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re, commands, shutil
import random
import wx
import urllib, urllib2
import ConfigParser
from consts import *
from httpredirect import *

def get_url_host(url):
	try:
		host = re.search(r'^https?:\/\/[^\/]+', url).group(0)
	except:
		return ''
	return host

def get_url_path(url):
	try:
		path = re.search(r'^(https?:\/\/[^\/]+(/[^\/]*)*)[^\/]*$', url).group(1)
	except:
		return ''
	return path

def get_python_version():
	(status, pyver) = commands.getstatusoutput('python -V')
	return re.search(r'ython\s+([\d\.]+)', pyver).group(1)
	
def get_temp_filename(fname, suffix=''):
	base, ext = os.path.splitext(os.path.basename(fname))
	return os.path.join(TEMP_DIR, '%s%s%04d%s' % (base, suffix, random.randint(0, 10000), ext))

def get_html_info(html):
	head = re.search(r'<title>(.*)</title>', html).group(1)
	body = re.search(r'<div[^>]*>(.*)</div>', html).group(1)
	body = re.sub(r'<[^>]*>', '', body)
	return head, body

def get_file_url(html, index = 0):
	url = re.search(r'<url>(.*)</url>', html).group(1)
	url = url.replace('bbs.fudan.edu.cn', BBS_HOSTS[index])
	return url

def get_update_info(html, key):
	val = re.search(r'%s=([^\r\n]*)' % key, html).group(1).strip()
	return val
	
def commands_getstatusoutput(cmd):
	if not sys.platform.startswith('win32'):
		return commands.getstatusoutput(cmd)
	from subprocess import Popen, PIPE, STDOUT
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
	output, unused = p.communicate()
	status = p.returncode
	return status, output
    
def get_tool_path(tool):
	if sys.platform.startswith('linux'):
		return tool
	else:
		return '%s%s%s' % ('tool', os.path.sep, tool)

def restore_default_encoding():
	reload(sys)
	if sys.platform.startswith('win32'):
		sys.setdefaultencoding('gb18030')
	else:
		sys.setdefaultencoding('utf-8')

def get_exif_info(filename, keys, use_unicode = True):
	vals = []
	if use_unicode:
		if 'utf-8' != sys.getdefaultencoding():
			reload(sys)
	    		sys.setdefaultencoding('utf-8')
	    		filename = filename.encode('gb18030')
	else:
		reload(sys)
	    	sys.setdefaultencoding('gb18030')
	    	if not sys.platform.startswith('win32'):
	    		filename = filename.encode('utf-8')
	(status, exif) = commands_getstatusoutput('%s -S "%s"' % (get_tool_path('exiftool'), filename))
	restore_default_encoding()
	if status == 0:
		for key in keys:
			try:
				val = re.compile(r'^%s:\s(.*)$' % key, re.M).search(exif).group(1)
			except:
				val = ''
			vals.append(val)
	if re.compile(r'^ThumbnailImage:', re.M).search(exif):
		has_thumb = True
	else:
		has_thumb = False
	return vals, has_thumb

def get_exif_thumbnail(filename, use_unicode = True):
	thumb = os.path.join(CONFIG_ROOT, 'thumbnail.jpg')
	if use_unicode:
		if 'utf-8' != sys.getdefaultencoding():
			reload(sys)
	    		sys.setdefaultencoding('utf-8')
	    		filename = filename.encode('gb18030')
	else:
		reload(sys)
	    	sys.setdefaultencoding('gb18030')
	    	if not sys.platform.startswith('win32'):
	    		filename = filename.encode('utf-8')
	    		thumb = thumb.encode('utf-8')
	(status, info) = commands_getstatusoutput('%s -b -ThumbnailImage "%s" > "%s"' % (get_tool_path('exiftool'), filename, thumb))
	restore_default_encoding()
	if status != 0:
		thumb = ''
	return thumb

def process_exif(filename, dict, thumb = '', inplace = True, backup = True, use_unicode = False):
	params = ' '.join(['-%s="%s"' % (k, dict[k].replace('\n', '').strip()) for k in dict.keys()])
	if not inplace:
		newfile = get_temp_filename(filename, '_exif')
		shutil.copy(filename, newfile)
		filename = newfile
	if not backup:
		params += ' -overwrite_original'
	if use_unicode:
		if 'utf-8' != sys.getdefaultencoding():
			reload(sys)
	    		sys.setdefaultencoding('utf-8')
	    		filename = filename.encode('gb18030')
	    		params = params.encode('gb18030')
	else:
		reload(sys)
	    	sys.setdefaultencoding('gb18030')
	    	if not sys.platform.startswith('win32'):
	    		filename = filename.encode('utf-8')
			thumb = thumb.encode('utf-8')
	if thumb == '-':
		params += ' "-ThumbnailImage<="'
	elif thumb:
		params += ' "-ThumbnailImage<=%s"' % thumb
	(status, info) = commands_getstatusoutput('%s %s "%s"' % (get_tool_path('exiftool'), params, filename))
	restore_default_encoding()
	if status != 0:
		return ''
	else:
		return filename

def copy_exif(filename, original, inplace = True):
	if not inplace:
		newfile = get_temp_filename(filename, '_rexif')
		shutil.copy(filename, newfile)
		filename = newfile
	if sys.platform.startswith('win32'):
		filename = filename.encode('gb18030')
	    	original = original.encode('gb18030')
	(status, info) = commands_getstatusoutput('%s -tagsFromFile "%s" "%s"' % (get_tool_path('exiftool'), original, filename))
	if status != 0:
		return ''
	else:
		return filename

def apply_template(text):
	substs = [('\\n', '\n')]
	txt = text
	for s, r in substs:
		txt = txt.replace(s, r)
	return txt

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
		
def is_image_file(fname):
	if re.match(r'.*\.(jpe?g|gif|png)$', fname, re.I):
		return True
	else:
		return False
		
def is_jpeg_file(fname):
	if re.match(r'.*\.jpe?g$', fname, re.I):
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

def get_bitmap_type(fname):
	if re.match(r'.*\.png$', fname, re.I):
		return wx.BITMAP_TYPE_PNG
	elif re.match(r'.*\.gif$', fname, re.I):
		return wx.BITMAP_TYPE_GIF
	else:
		return wx.BITMAP_TYPE_JPEG

def search_files(path, expr = '.*'):
	min_size = read_config_int('General', 'MinFileSize', 0)
	max_size = read_config_int('General', 'MaxFileSize', 1024)
	files = os.listdir(path)
	r = re.compile(expr, re.I)
	newfiles = []
        if read_config_bool('General', 'SubFolder', False):
		for root, dirs, files in os.walk(path):  
			for f in files:  
				fn = os.path.join(root, f)
				if r.search(fn):
					try:
						sz = os.path.getsize(fn)
						if sz >= 1024 * min_size and sz <= 1024 * max_size:
							newfiles.append(fn)
					except:
						pass
	else:
		for f in files:
			fn = os.path.join(path, f)
			if r.search(fn) and os.path.isfile(fn):
				try:
					sz = os.path.getsize(fn)
					if sz >= 1024 * min_size and sz <= 1024 * max_size:
						newfiles.append(fn)
				except:
					pass
	return newfiles

def update_title():
	mainwin = wx.GetApp().GetTopWindow()
	if mainwin.get_user_id():
		mainwin.SetTitle('%s v%s [%s: %s]' % (APPNAME, VERSION, _('User'), mainwin.get_user_id()))
	else:
		mainwin.SetTitle('%s v%s' % (APPNAME, VERSION))

def read_config(section, option, default = ''):
	cf = ConfigParser.ConfigParser()
	try:
		cf.read(CONFIG_FILE)
		value = cf.get(section, option)
	except:
		return default
	else:
		return value

def read_config_int(section, option, default = 0):
	cf = ConfigParser.ConfigParser()
	try:
		cf.read(CONFIG_FILE)
		value = cf.getint(section, option)
	except:
		return default
	else:
		return value
		
def read_config_bool(section, option, default = False):
	cf = ConfigParser.ConfigParser()
	try:
		cf.read(CONFIG_FILE)
		value = cf.getboolean(section, option)
	except:
		return default
	else:
		return value

def write_config(section, dic):
	cf = ConfigParser.ConfigParser()
	try:
		cf.read(CONFIG_FILE)
	except:
		pass
	if not cf.has_section(section):
		cf.add_section(section)
	for k, v in dic.items():
		cf.set(section, k, v)
	cf.write(open(CONFIG_FILE, 'w'))

def remove_config(section, option = ''):
	cf = ConfigParser.ConfigParser()
	try:
		cf.read(CONFIG_FILE)
		if option:
			cf.remove_option(section, option)
		else:
			cf.remove_section(section)
		cf.write(open(CONFIG_FILE, 'w'))
	except:
		pass

def perfect_connect(url, post = '', retry = False, proxy = ''):
	req = urllib2.Request(url, post)
	req.add_header('Cookie', read_config('Login', 'Cookie'))
	if proxy:
		opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}))
		urllib2.install_opener(opener)
	try:		    
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError, e:  
		info = '%s|%s: %d' % (MSG_NETWORK_ERROR, MSG_ERROR_CODE, e.code)
		return info
	except urllib2.URLError, e:
                info = '%s|%s: %s' % (MSG_NETWORK_ERROR, MSG_ERROR_CODE, e.reason)
		return info
	except Exception, e:
		info = '%s|%s' % (MSG_ERROR, MSG_NETWORK_ERROR)
		print e
		return info
	else:
		the_page = resp.read().decode('gb18030')
		if the_page.find(u'发生错误') >= 0:
			k, v = get_html_info(the_page)
			info = '|'.join([k, v])
			if retry or the_page.find(u'登录') < 0:
				return info
			else:
				host = read_config_int('Login', 'Host', 0)
				userid = read_config('Login', 'UserID')
				pwd = read_config('Login', 'Password')
				if userid and pwd:
					if proxy:
						opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}), SmartRedirectHandler())
					else:
						opener = urllib2.build_opener(SmartRedirectHandler())  
					urllib2.install_opener(opener)  
					req2 = urllib2.Request('http://%s/bbs/login' % BBS_HOSTS[host], urllib.urlencode({'id': userid, 'pw': pwd}))  
					try:
						resp2 = urllib2.urlopen(req2)  
					except urllib2.HTTPError, e:  
						info = '%s|%s: %d' % (MSG_NETWORK_ERROR, MSG_ERROR_CODE, e.code)
						return info
					except:
						info = '%s|%s' % (MSG_ERROR, MSG_NETWORK_ERROR)
						return info
					else:
						if resp2.code != 302:			
							the_page = resp2.read().decode('gb18030')
							k, v = get_html_info(the_page)
							info = '|'.join([k, v])
							return info
						else:
							cookie = ';'.join(resp2.headers['set-cookie'].split(','))
							write_config('Login', {'Cookie': cookie})
							return perfect_connect(url, post, True)
				else:
					return 'No User'
		else:
			return ''
