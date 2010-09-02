# -*- coding: utf-8 -*-

import sys, os, glib


APPNAME = 'UploadHelper'
APPCODENAME = 'UploadHelper'
PACKAGE = 'uploadhelper'
VERSION = '3.9.0.1'
AUTHOR = 'tyllr'
EMAIL = 'tyllrxs@gmail.com'
HOMEPAGE = 'http://homepage.fudan.edu.cn/~tyllr/uh/'
BBS_HOSTS = ('bbs.fudan.edu.cn', 'bbs.fudan.sh.cn', '202.120.225.9', '61.129.42.9')
LIST_CONTEXT_MENU = ('&Add Files...', 'A&dd Directories...', '', 
		'&Remove Selected', 'Remove &Copies', 'Remove &Invalid', '', 
		'Remove A&ll')
DATA_DIR = '/usr/share/uploadhelper/'
FILE_BOARDS = 'data/boards.xml' 
CONFIG_ROOT = os.path.join(glib.get_user_config_dir(), 'uploadhelper')

if not os.path.exists(CONFIG_ROOT):
    os.makedirs(CONFIG_ROOT)

try:
    LANG = os.getenv('LANG').split('.')[0].lower().replace('_','-')
except:
    LANG = 'en-us'

STATUSBAR_INFO = ['Contact tyllr (at) RYGH BBS for help or advice']
