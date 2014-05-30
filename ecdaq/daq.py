#!/usr/bin/env python
# coding:utf-8
'''

'''
#---------------------------------------------------------------------------# 
# import the modbus client and the framers
#---------------------------------------------------------------------------# 
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#---------------------------------------------------------------------------# 
# Import the modbus framer that you want
#---------------------------------------------------------------------------# 
#---------------------------------------------------------------------------# 
#from pymodbus.transaction import ModbusSocketFramer as ModbusFramer
#from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
#from pymodbus.transaction import ModbusBinaryFramer as ModbusFramer
#from pymodbus.transaction import ModbusAsciiFramer as ModbusFramer


import time,threading 
from datetime import datetime

from define import * 
from utilities import select
from control import tCtrl

from logger import Logger  
logger=Logger(logname=LOG_FILE,loglevel=1,logger=__file__).getlog() 

#**************************************************************************
#* 解析
#************************************************************************** 
Baudrate=lambda x: int(x.split(',')[0])
Bytesize=lambda x: int(x[-3])
Parity=lambda x: x[-2]
Stopbits=lambda x: int(x[-1])

Begin=lambda x: int(x.split(',')[0])
End=lambda x: int(x.split(',')[1])


class SampleTimer(threading.Thread) :
    '''
    '''
    def __init__(self,index,id):  
        threading.Thread.__init__(self)  
        self.index = index  
        self.id = id 
        self.thread_stop = False  
   
    def run(self): 
        global tCtrl
        _sample=select(tCtrl.samples,'id',self.id)
        _protocol=select(tCtrl.protocols,'id',_sample.properties['protocol_id'])
        _transport=select(tCtrl.transports,'id',_sample.properties['transport_id'])
        _rule=select(tCtrl.rules,'id',_sample.properties['rule_id'])        
        _method=_protocol.properties['method']
        _port=_transport.properties['port']
        _para=_transport.properties['para'] 
        _timeout=int(_transport.properties['timeout'])/1000.0
        client = ModbusClient(method=_method, port=_port,baudrate= \
        Baudrate(_para),bytesize=Bytesize(_para),parity=Parity(_para),\
        stopbits=Stopbits(_para),timeout=_timeout) 
        _index=int(_rule.properties['index'])
        _count=int(_rule.properties['count'])
        _unit_begin=Begin(_rule.properties['range'])
        _unit_end=End(_rule.properties['range'])
        client.connect()  
        self.interval = int(_protocol.properties['period']) 
        while not self.thread_stop: 
            for i in range(_unit_begin,_unit_end):
                start_ = datetime.utcnow()
                response=client.read_holding_registers(address=_index, \
                count=_count,unit=i)                
                tCtrl.samples[self.index].data[i]=response.registers
                print response.registers #getRegister(1)/10.0
                end_ = datetime.utcnow()
                print '[cost time] %s' %(end_-start_)
            time.sleep(self.interval)  
    
    def stop(self):  
        self.thread_stop = True
        client.close()               
    
    
class Daq(object):
    '''
    '''
    def __init__(self):
        self.enabled=False 
        
    def start(self): 
        global tCtrl 
        self.samples=tCtrl.samples
        for i in range(len(self.samples)):
            _sample=self.samples[i]
            t=SampleTimer(i,_sample.properties['id'])
            t.run()
            
daq=Daq()
daq.start()

for  c in tCtrl.samples:
    for i in range(len(c.data)): 
        print c.data[i]
    




