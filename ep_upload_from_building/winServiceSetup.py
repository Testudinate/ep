#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
'''from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*",'decimal'];

options = {
    "py2exe": {"compressed":1,
    "optimize":0,
    "includes":includes,
    "bundle_files":1}
};

setup( 
	version = "0.0.1",
    description = "描述",
    name = "程序名",
    options = options,
    zipfile=None,
    windows=[{
        "script": "winService.py",
        #"icon_resources": [(1, "logo.ico")],
        #"dest_base":"StartLink",    #输出程序的名称，没有此项的话默认为主script的文件名main
        "author": "作者",
        'description':u"程序描述信息",
        'copyright':u'(C) www.company.com Inc.  All rights reserved.', 
        'company_name':u"公司名称"
    }], 
	service=["winService"], 
	data_files=[("",
				["config.ini", "time.txt"]),  ##
               ],
	)
'''

from distutils.core import setup
import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "1.0.0"
        self.company_name = "Founder Software Suzhou Co. Ltd."
        self.copyright = "Copyright &copy; 2009 Founder Software (Suzhou) Co., Ltd. "
        self.name = "Jchem cartridge windows service"


myservice = Target(
    description = 'foo',
    modules = ['winService'],
    cmdline_style='pywin32',
    #icon_resources=[(1, "cartrigde.ico")]
)

options = {"py2exe":  
            {   "compressed": 1,  
                "bundle_files": 1
            }  
          } 
         
setup(
    service=[myservice],
    options = options,
    zipfile = None,
    windows=[{"script": "winService.py"}],
	data_files=[("",
				["config.ini", "time.txt"]),  ##
               ],
)