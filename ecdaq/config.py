#!/usr/bin/env python
# coding:utf-8
'''

'''  
import xml.etree.cElementTree as ET
#try:
#    import xml.etree.cElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET

import set
    
class XmlConfig():
    '''   
     
    '''  
    #**************************************************************************
    #* 三种类型
    #**************************************************************************
    config_file="./config.xml"      # 主配置文件 
    def readAttrib(self,source,tag):
        tree = ET.ElementTree(file=source)        
        node=tree.find(tag) 
        return node.attrib
    
    def readChildren(self,source,tag):
        children=[]
        tree = ET.ElementTree(file=source)    
        node=tree.find(tag)        
        for child in node:
            children.append(child.attrib)
        return children
    
    def readSub(self,source,tag):        
        sub={}
        tree = ET.ElementTree(file=source) 
        node=tree.find(tag)            
        for child in node:
            sub[child.tag]=child.text      
        return sub
    
    #**************************************************************************
    #* 读子节点集合
    #**************************************************************************    
    def readObjects(self,tag):
        objects=[]
        children=self.readChildren(self.__class__.config_file,tag)
        for i in range(len(children)):
            c=set.TObject(children[i])
            objects.append(c)
        return objects 
    
    def readLinkObjects(self,tag):
        items=[]
        children=self.readChildren(self.__class__.config_file,tag)
        for i in range(len(children)):
            c=set.TLinkObject(children[i])
            c.common=self.readSub(c.properties['template'],'common')
            cm=self.readChildren(c.properties['template'],'items')
            for j in range(len(cm)):
                v=set.TObject(cm[i])
                c.items.append(v)
            items.append(c)
        return items 
    
    #**************************************************************************
    #* 读取配置信息
    #**************************************************************************    
    def readBuilding(self):
        attribs=self.readAttrib(self.__class__.config_file,'building')
        return set.TBuilding(attribs)            
    
    def readPlatforms(self):
        return self.readLinkObjects('platform')
    
    def readModels(self):
        return self.readLinkObjects('model')
    
    def readUploads(self):        
        return self.readObjects('upload')            
    
    def readProtocols(self):
        return self.readObjects('protocol')   
    
    def readTransports(self):
        return self.readObjects('transport')     
        
    def readRules(self):
        return self.readLinkObjects('rule')      
    
    def readSamples(self):
        items=[]
        samples= self.readObjects('sample')
        for c in samples:
            items.append(set.TSample(c.properties)) 
        return items        
        
    def readThresholds(self):
        return self.readObjects('threshold')
        
    def readDevices(self):
        return self.readObjects('device')  
    
    def readAlarms(self):                          
        return self.readObjects('alarm') 
    
    def readEmails(self):                          
        return self.readObjects('email')    

#**************************************************************************
#* 测试
#**************************************************************************  
# -- building --
def testBuilding():
    xc=XmlConfig()    
    b=xc.readBuilding()
    print b.properties    

# -- platforms --
def testPlatform():
    xc=XmlConfig() 
    p=xc.readPlatforms()
    for i in p:
        print i.properties
        print i.common 
        for c in i.items:
            print c.properties        
        
# -- upload -- 
def testUpload():   
    xc=XmlConfig()  
    u=xc.readUploads()
    for i in u:
        print i.properties
        
# -- model --
def testModel():
    xc=XmlConfig() 
    m=xc.readModels()
    for i in m:
        print i.properties
        print i.common
        for c in i.items:
            print c.properties

# -- upload -- 
def testProtocol():   
    xc=XmlConfig()  
    p=xc.readProtocols()     
    for i in p:
        print i.properties 
# -- transport --
def testTransport():   
    xc=XmlConfig()  
    p=xc.readTransports()     
    for i in p:
        print i.properties 
        
# -- rule --
def testRule():   
    xc=XmlConfig()  
    p=xc.readRules()     
    for i in p:
        print i.properties   
        print i.common
        for c in i.items:  
            print c.properties  
            
# -- sample --
def testSample():   
    xc=XmlConfig()  
    p=xc.readSamples()     
    for i in p:
        print i.properties  
        
# -- threshold --
def testThreshold():   
    xc=XmlConfig()  
    p=xc.readThresholds()     
    for i in p:
        print i.properties    
        
# -- device --
def testDevice():   
  xc=XmlConfig()  
  p=xc.readDevices()     
  for i in p:
      print i.properties   
    
# -- email --
def testEmail():   
  xc=XmlConfig()  
  p=xc.readEmails()     
  for i in p:
      print i.properties                  

if __name__=="__main__":
    #testBuilding()
    #testPlatform()
    #testModel()
    #testUpload()
    
    #testProtocol()
    #testTransport()
    #testRule()
    #testSample()
    
    #testThreshold()
    #testDevice()
    testEmail()