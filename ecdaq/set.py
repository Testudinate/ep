#!/usr/bin/env python
# coding:utf-8
'''

'''
import traceback 
from logger import Logger 
logger=Logger(logname='./log.txt',loglevel=1,logger=__file__).getlog() 

import define 
import version as __version
__version__ = __version.version.short()
__author__ = 'ououcool'

import xml.etree.cElementTree as ET
#try:
#    import xml.etree.cElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET

class TObject(object):
    '''
    '''
    def __init__(self,properties):
        self.properties=properties  
        
    
class TLinkObject(TObject):
    '''
    '''
    def __init__(self,properties):        
        TObject.__init__(self,properties)     
        self.common={}
        self.items=[]      
            
        
class TBuilding(TObject):
    '''
    ''' 

        
class TPlatform(TLinkObject):
    '''
    
    ''' 
        
             
class TUpload(TLinkObject):
    ''' 
    '''  
    
    

class TVirtualItem(TObject):
    '''
    '''


class TModel(TLinkObject):
    '''
    ''' 
        
        
class TProtocol(TObject):
    '''
    '''
    
    
class TTransport(TObject):
    '''
    '''    
    

class TRule(TLinkObject):
    '''
    '''  
            

class TSample(TObject):
    '''
    '''  
    def __init__(self,properties):        
        TObject.__init__(self,properties)     
        self.data={}    

class TThreshold(TObject):
    '''
    '''    


class TProperty(TObject):
    '''
    '''  
   

class TDevice(TObject):
    '''
     
    ''' 
    
        
class TAlarm(TObject):
    '''
    '''    


class TEmail(TObject):
    '''
    ''' 