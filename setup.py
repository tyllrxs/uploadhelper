# -*- coding: utf-8 -*-

import os, sys
reload(sys)
sys.setdefaultencoding('utf8')

from distutils.core import setup
import py2exe, glob

includes = ['encodings', 'encodings.*', 'gettext', 'glob', 'wx',
            'urllib', 'urllib2', 'cookielib', 'ConfigParser',
            ]

options = {"py2exe":
            {"compressed": 1, #压缩
             "optimize": 2,
             "includes": includes,
             "packages": ["wx.lib.pubsub"],
             "bundle_files": 1
            }
           }

manifest = ''' 
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" 
manifestVersion="1.0"> 
<assemblyIdentity 
version="0.6.8.0" 
processorArchitecture="x86" 
name="YourApp" 
type="win32" 
/> 
<description>YourApp</description> 
<trustInfo xmlns="urn:schemas-microsoft-com:asm.v3"> 
<security> 
<requestedPrivileges> 
<requestedExecutionLevel 
level="asInvoker" 
uiAccess="false" 
/> 
</requestedPrivileges> 
</security> 
</trustInfo> 
<dependency> 
<dependentAssembly> 
<assemblyIdentity 
type="win32" 
name="Microsoft.VC90.CRT" 
version="9.0.21022.8" 
processorArchitecture="x86" 
publicKeyToken="1fc8b3b9a1e18e3b" 
/> 
</dependentAssembly> 
</dependency> 
<dependency> 
<dependentAssembly> 
<assemblyIdentity 
type="win32" 
name="Microsoft.Windows.Common-Controls" 
version="6.0.0.0" 
processorArchitecture="x86" 
publicKeyToken="6595b64144ccf1df" 
language="*" 
/> 
</dependentAssembly> 
</dependency> 
</assembly> 
''' 


setup(     
    options = options,
    version = "3.9.3", 
    name = u'日月光华上传助手',
    description = u'日月光华上传助手',
    author = 'tyllr',
    author_email = 'tyllrxs@gmail.com',
    url = 'http://homepage.fudan.edu.cn/~tyllr/uh/',
    data_files = [('icon', glob.glob('icon/*.*')),
                  ('icon/16', glob.glob('icon/16/*.*')),
                  ('icon/24', glob.glob('icon/24/*.*')),
                  ('icon/32', glob.glob('icon/32/*.*')),
                  ('icon/indicator', glob.glob('icon/indicator/*.*')),
                  ('locale/zh_CN/LC_MESSAGES', glob.glob('locale/zh_CN/LC_MESSAGES/*')),
                  ('ui', glob.glob('ui/*.xrc')),
                  ('data', glob.glob('data/*.*')),
                  #('.', [os.path.join(os.environ['SystemRoot'], 'system32', 'msvcp71.dll')]),
                  ],  
    zipfile=None,   #不生成library.zip文件
    windows=[{"script": "uploadhelper.py",
              "icon_resources": [(1, "icon/logo32.ico")],
              "other_resources": [(24, 1, manifest)],
              }]#源文件，程序图标
    )
