# -*- coding: utf-8 -*-

import sys, os
import ConfigParser
import locale, gettext

APPCODENAME = 'uploadhelper'
PACKAGE = 'uploadhelper'
VERSION = '3.95'
AUTHOR = 'tyllr'
EMAIL = 'tyllrxs@gmail.com'
HOMEPAGE = 'http://homepage.fudan.edu.cn/~tyllr/uh/'
HOME_PYTHON = 'http://www.python.org/'
HOME_WXPYTHON = 'http://www.wxpython.org/'
APPLANGUAGES = [('de','Deutsch'), ('en','English'), ('es','Español'), ('fr','Française'), 
		('ja_JP','日本語'), ('ko_KR','한국어'), ('pt','Português'), ('ru','Россию'), 
		('zh_CN','简体中文'), ('zh_TW','繁體中文')]
BBS_HOSTS = ['bbs.fudan.edu.cn', 'bbs.fudan.sh.cn', '202.120.225.9', '61.129.42.9']
SEPARATOR = '\n--------------------------------------------\n--------------------------------------------\n'
DATA_DIR = '/usr/share/uploadhelper/'
FILE_BOARDS = 'data/boards.xml' 
SAMPLE_IMAGE = 'pic/sample.jpg'

# Set directories to save data

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
LOG_FILE = os.path.join(CONFIG_ROOT, 'log.txt')

# Locale settings

gettext.install('messages', 'locale', unicode = True)
lang = locale.getdefaultlocale()[0]
try:
	cf = ConfigParser.ConfigParser()
	cf.read(CONFIG_FILE)
	lang = cf.get('General', 'language', lang)
	gettext.translation('messages', 'locale', languages = [lang]).install(True)
except:
	if not cf.has_section('General'):
		cf.add_section('General')
	cf.set('General', 'language', lang)
finally:
	cf.write(open(CONFIG_FILE, 'w'))

# Some common messages

APPNAME = _('UploadHelper')
MSG_ERROR = _('Error')
MSG_FAIL = _('Fail')
MSG_ERROR_CODE = _('Error code')
MSG_NETWORK_ERROR = _('Network Error')
MSG_SAVE_SETTINGS_ERROR = _('Error occurred when saving settings')
MSG_FILL_BLANKS = _('Fill the blanks first.')
MSG_FILE_SELECTED = _('%d Files Selected')
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
STATUSBAR_INFO = ['', _('Contact tyllr (at) RYGH BBS for help or advice')]
LIST_CONTEXT_MENU = ('%s...' % _('&Add Files'), '%s...' % _('A&dd Directory'), '', 
		_('&Remove Selected'), _('Remove &Copies'), _('Remove &Invalid'), '', 
		_('Remove A&ll'))
MARK_POSITIONS = [_("Top Left"), _("Top Right"), _("Center"), _("Bottom Left"), _("Bottom Right")]
