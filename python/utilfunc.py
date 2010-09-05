# -*- coding: utf-8 -*-

import re


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

