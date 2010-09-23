# -*- coding: utf-8 -*-

import locale, gettext
try:
	gettext.install('messages', 'locale', unicode = True)
	gettext.translation('messages', 'locale', locale.getdefaultlocale()[0]).install(True)
except:
	pass

APPNAME = _('UploadHelper')
APPCODENAME = 'uploadhelper'
PACKAGE = 'uploadhelper'
VERSION = '3.93'
AUTHOR = 'tyllr'
EMAIL = 'tyllrxs@gmail.com'
HOMEPAGE = 'http://homepage.fudan.edu.cn/~tyllr/uh/'
BBS_HOSTS = ['bbs.fudan.edu.cn', 'bbs.fudan.sh.cn', '202.120.225.9', '61.129.42.9']
LIST_CONTEXT_MENU = (_('&Add Files...'), _('A&dd Directory...'), '', 
		_('&Remove Selected'), _('Remove &Copies'), _('Remove &Invalid'), '', 
		_('Remove A&ll'))
SEPARATOR = '\n--------------------------------------------\n--------------------------------------------\n'
DATA_DIR = '/usr/share/uploadhelper/'
FILE_BOARDS = 'data/boards.xml' 

# Some common messages
MSG_ERROR = _('Error')
MSG_FAIL = _('Fail')
MSG_ERROR_CODE = _('Error code')
MSG_NETWORK_ERROR = _('Network Error')
MSG_FILL_BLANKS = _('Fill the blanks first.')
MSG_FILE_SELECTED = _('%d File(s) Selected')
MSG_UNKNOWN_ERROR = _('Unknown Error')
MSG_INVALID_FILE = _('Invalid File')
MSG_UNSUPPORTED_FORMAT = _('Unsupported File Format')
MSG_ENTITY_TOO_LARGE = _('Too Large File')
MSG_CHECK_UPDATE = _('Check for Updates')
MSG_FILE_UPLOADING = '[File %d Uploading...]'
MSG_FILE_UPLOADING_2 = r'[File \1 Uploading...]'
MSG_LOGOUT = _('Logout')
STATUS_UPLOADING = _('Uploading')
STATUS_UPLOADED = _('Finished')

# Set directories to save data

import sys, os

if sys.platform.startswith('win32'):
	CONFIG_ROOT = os.path.join(os.environ['APPDATA'], APPCODENAME)
	TEMP_DIR = os.path.join(os.environ['TEMP'], APPCODENAME)
else:
	CONFIG_ROOT = os.path.join(os.getenv('HOME'), '.config', APPCODENAME)
	TEMP_DIR = os.path.join('/tmp', APPCODENAME)

if not os.path.exists(CONFIG_ROOT):
    os.makedirs(CONFIG_ROOT)

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

CONFIG_FILE = os.path.join(CONFIG_ROOT, 'user.conf')


STATUSBAR_INFO = ['', _('Contact tyllr (at) RYGH BBS for help or advice')]
