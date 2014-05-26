#!/usr/bin/env python
#encoding:utf-8
'''
scan for ameters in cabr
--------------------------------------------------------------------------
To sample the Q of four ameters in cabr, save them to [DB_FILE], and tranfer them
up to our server via web-api.
'''
import time
import os,string,thread
import sqlite3

from ep_upload import UploadService 
from mail import send_mail
from pymodbus.client.sync import ModbusTcpClient as ModbusClient 
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer 

from logger import Logger 
from locate_module_path import module_path

__dir__ = module_path()  
logger=Logger(logname='%s/log.txt' %__dir__,loglevel=1,logger=__file__).getlog() 

RETRIES=3
HOST = '192.168.0.254'              # host name
PORT = 4001                        # listening porT
ADDR = (HOST, PORT)                 # 
CONFIG_FILE='%s/point.txt' %__dir__
DB_FILE='db.energydata'

BUILDING_ID=9
SERVER='192.168.0.200:8008'
URL_PREFIX_POST='http://%s/WebApi/Point.php?fun=sqlquery&param=' %SERVER
URL_PREFIX_GET='http://%s/WebApi/GetPointInfoByBuildingId_controller.php?building_id=' %SERVER

MAIL_LIST=('yangjiaohui@pkpm.com.cn','lizongning@pkpm.com.cn')
    
# read configure info, return all points info, like (['1','350','2','1'],)
def init():
    ret=[]
    f=open(CONFIG_FILE)
    try:
        lines=f.readlines()
        for l in lines:
            l=l.lstrip(' ').strip('\n')
            if l[0]!='#':
                point=l.split(',')
                ret.append(point)
        return ret
    except IOError:
        logger.error("[%s] doesn't exist." %CONFIG_FILE)
    finally:
        f.close()


def mapping(): 
    ret={}
    try:
        service=UploadService(URL_PREFIX_POST,URL_PREFIX_GET)
        ep_point=service.get_point(BUILDING_ID) # from EpExhibit
    except Exception,e:
        logger.error('EP-WebAPI is not available: %s. URL="%s".' % (e,service.url) )
        return False
    if ep_point:
        for item in ep_point:
            k=str(item[3])
            ret[k]=item[0] 
    return ret        
        
# read point, return (id,value) like('1','100.00')
def read(client,point):
    _id,_address,_count,_unit,divisor=point 
    rr=client.read_holding_registers(address=string.atoi(_address),count=string.atoi(_count),unit=string.atoi(_unit))
    if rr: 
        h=rr.getRegister(0) 
        l=rr.getRegister(1)
        value=(h*256*256+l)/string.atof(divisor)   
        return _id,value
    else:
        return None
            
#
def storage(dbfile,recordlist):  
		dbexist = os.path.exists(dbfile)
		db = sqlite3.connect(dbfile)
		cur = db.cursor()
		sqlstring=''
		# create table first time new database is accessed
		if not dbexist:
			sqlstring = 'CREATE TABLE energydata \
			(id INTEGER PRIMARY KEY, p_id INTEGER, val TEXT, datetime TEXT)'
		cur.execute(sqlstring)
		db.commit()   
		sqlstring='INSERT INTO energydata(id,p_id,val,datetime) VALUES(NULL,?,?,?)'  
		cur.executemany(sqlstring,recordlist)
		db.commit()  

def mail_notify(interval):  
    while 1:
        send_mail('HAILI building','running...',MAIL_LIST)
        logger.info("email OK!") 
        time.sleep(interval)   
    thread.exit_thread()    

def sample(): 
    points=init()
    print 'all points:',points
    map=mapping()
    print 'mapping:',map
    if not points:
        logger.error("there is no valid record in [%s]." %CONFIG_FILE)        
    thread.start_new_thread(mail_notify, (3600*12,))          
    while True: 
        try: 
            # -- connect to the server --
            client = ModbusClient(HOST,port=PORT,framer=ModbusFramer)
            client.connect() 
            print 'connection ok!'
            # -- current time--
            now=time.localtime()
            dt="%s-%s-%s %s:%s:%s" %now[:6]       
            # -- read all points --      
            recordlist=[]  # id,value,time          
            for p in points:
                record=read(client,p) 
                if record:
                    _id= record[0]
                    if map[_id]:  
                        mem=map[_id],record[1],dt  
                        recordlist.append(mem)
            print 'recordlist',recordlist
            # -- insert all recordlist --        
            if recordlist:
                service=UploadService(URL_PREFIX_POST,URL_PREFIX_GET)
                r1=service.insert(recordlist) 
                r2=service.update(recordlist) 
                r3=storage(DB_FILE,recordlist)
                #print r1,r2,r3
                logger.info("OK!")
        except Exception,e:
            logger.error('error:%s' %e)
        finally:
            client.close() 
            time.sleep(300)                 
 
sample()
 

def search():
    client = ModbusClient(HOST,port=PORT,framer=ModbusFramer)
    if not client.connect():
        logger.error("cannot connect to [%s:%d]." %(HOST,PORT))     
    n=0
    while n<247:
        rr=client.read_holding_registers(address=0x015e,count=2,unit=n)
        assert(rr.function_code < 0x80) 
        if rr:
            print n
        else:
            print 'fail',n
        n=n+1
    client.close()
            
#search()