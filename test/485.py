#!/usr/bin/env python
#!encoding=utf-8
'''
Pymodbus Client Framer Overload
--------------------------------------------------------------------------

All of the modbus clients are designed to have pluggable framers
so that the transport and protocol are decoupled. This allows a user
to define or plug in their custom protocols into existing transports
(like a binary framer over a serial connection).

It should be noted that although you are not limited to trying whatever
you would like, the library makes no gurantees that all framers with
all transports will produce predictable or correct results (for example
tcp transport with an RTU framer). However, please let us know of any
success cases that are not documented!
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

#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import time
#import os,sys
#import sqlite3

from ep_upload import UploadService 
SERVER='192.168.0.200:8008'
URL_PREFIX_POST='http://%s/WebApi/Point.php?fun=sqlquery&param=' %SERVER
URL_PREFIX_GET='http://%s/WebApi/GetPointInfoByBuildingId_controller.php?building_id=' %SERVER

from logger import Logger 
from locate_module_path import module_path
__dir__ = module_path()  
logger=Logger(logname='%s/log.txt' %__dir__,loglevel=1,logger=__file__).getlog() 


#import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# Initialize the client
#---------------------------------------------------------------------------# 
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600,\
    bytesize=8,parity='N',stopbits=1,timeout=1)
#client = ModbusClient(port=1,stopbits=1,bytesize=8,parity='N',baudrate=9600) 
#client = ModbusClient('localhost',port=502, framer=ModbusFramer)
client.connect()

#---------------------------------------------------------------------------# 
# perform your requests
#---------------------------------------------------------------------------# 
#rq = client.write_coil(1, True)
#rr = client.read_coils(1,1)
#assert(rq.function_code < 0x80)     # test that we are not an error
#assert(rr.bits[0] == True)          # test the expected value
service=UploadService(URL_PREFIX_POST,URL_PREFIX_GET)
t=0
rh=0
while 1:
	rr=client.read_holding_registers(address=0,count=2,unit=1) 
	now=time.localtime()
	dt="%s-%s-%s %s:%s:%s" %now[:6]
	if rr:
		t=rr.getRegister(1)/10.0
		rh=rr.getRegister(0)/10.0
		logger.info('室内温度=%s度,室内湿度=%s%%' %(t,rh))
		service.insert_single(265,t,dt)
		service.insert_single(266,rh,dt)
	time.sleep(10)
#---------------------------------------------------------------------------# 
# close the client
#---------------------------------------------------------------------------# 
client.close()
