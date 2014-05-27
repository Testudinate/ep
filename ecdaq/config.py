#!/usr/bin/env python
# coding:utf-8

'''

'''
import version as __version
__version__ = __version.version.short()
__author__ = 'ououcool'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class TConfig():
    '''
    
    '''
    src_file="config.xml"
    def __init__(self):
        tree = ET.ElementTree(file=TConfig.src_file)
        
    def readBuilding(self):
        print "1"
        
        
class Building(object):
    '''
    '''    
    def __init__(self,id,name):
        self.id=id
        self.name=name
        
        
class Platform(object):
    '''
    '''
    def __init__(self,id,template,user,password,aes,alias):
        self.id=id
        self.template=template
        self.user=user
        self.password=password
        self.aes=aes
        self.alias=alias
        
    def loadTemplate(self):
        # load template 
        tree = ET.ElementTree(file=self.template)