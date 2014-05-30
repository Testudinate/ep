#!/usr/bin/env python
# coding:utf-8
'''

'''
import traceback 
from logger import Logger 
logger=Logger(logname='./log.txt',loglevel=1,logger=__file__).getlog() 

import define
from config import XmlConfig
import version as __version
__version__ = __version.version.short()
__author__ = 'ououcool'

import xml.etree.cElementTree as ET
#try:
#    import xml.etree.cElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET

class Singleton(object):  
    _instance = None  
    def __new__(cls, *args, **kwargs):  
        if not cls._instance:  
            cls._instance = super(Singleton, cls).__new__(  
                                cls, *args, **kwargs)  
        return cls._instance  

class TControl(Singleton):
    '''
    ''' 
    def __init__(self):
        xc=XmlConfig()
        self.building=xc.readBuilding()
        self.platforms=xc.readPlatforms()
        self.models=xc.readModels()
        self.uploads=xc.readUploads()
        self.protocols=xc.readProtocols()
        self.transports=xc.readTransports()
        self.rules=xc.readRules()
        self.samples=xc.readSamples()
        self.thresholds=xc.readThresholds()
        self.devices=xc.readDevices()
        self.alarms=xc.readAlarms()  
        self.emails=xc.readEmails()

    def check(self):    
        print '===building==='
        print self.building.properties    
        
        print '===platform===' 
        for i in self.platforms:
            print i.properties
            print i.common 
            for c in i.items:
                print c.properties
                                
        print '===model==='
        for i in self.models:
            print i.properties
            print i.common 
            for c in i.items:
                print c.properties      
        
        print '===upload==='
        for i in self.uploads:
             print i.properties           
        
        print '===protocol===' 
        for i in self.protocols:
             print i.properties
                            
        print '===transport==='
        for i in self.transports:
             print i.properties        
        
        print '===rule==='
        for i in self.rules:
             print i.properties        
        
        print '===sample==='
        for i in self.samples:
             print i.properties            
        
        print '===threshold==='
        for i in self.thresholds:
            print i.properties         
        
        print '===device==='
        for i in self.devices:
            print i.properties    
            
        print '===alarm==='
        for i in self.alarms:
            print i.properties                 
        
        print '===email==='
        for i in self.emails:
            print i.properties                
                                                                                                                                                                                                                          
tCtrl=TControl()

#tCtrl.check()