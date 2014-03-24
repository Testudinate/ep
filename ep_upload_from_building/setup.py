#!/usr/bin/env python
#encoding:utf-8

#usage: python setup.py py2exe 
#FileName: setup.py
#Creation of date:  2014.03.07
#Author:    ouyang
#E-mail:    ouyangjiaohui@gmail.com


#----bundle_files有效值----
#	3 (默认)不打包。
#	2 打包，但不打包Python解释器。
#	1 打包，包括Python解释器。

#----zipfile的有效值----
#	不填	(默认)生成一个library.zip文件
#	None	把所有东西打包进.exe文件中

from distutils.core import setup
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
        "script": "transferEngergyData.py",
        #"icon_resources": [(1, "logo.ico")],
        "dest_base":"StartLink",    #输出程序的名称，没有此项的话默认为主script的文件名main
        "author": "作者",
        'description':u"程序描述信息",
        'copyright':u'(C) www.company.com Inc.  All rights reserved.', 
        'company_name':u"公司名称"
    }],
	data_files=[("",
				["config.ini", "time.txt"]),  
               ],
)