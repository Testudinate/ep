#encoding:utf-8
import sys,os  
import ConfigParser   
import json
import urllib
from logger import Logger 
import time
import datetime
import pyodbc
import socket

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.""" 
	
    return hasattr(sys, "frozen") 

def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))

    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
	
current_path =  module_path()
logger=Logger(logname='%s\\log.txt' %current_path,loglevel=1,logger='DataTransmission').getlog()
hour_file='%s\\time.txt' %current_path
'''
Web API for EpExhibit system with [ip] & [self.url_prefix_post] only

'''
class DataTransmission():
	def __init__(self, config_file_path):	
		self.map={}
		self.record={}
		self.buildingId,self.host,self.port,self.interval,self.drive,self.path,self.conn, \
		self.str_post,self.str_get=self.read_config(config_file_path)
		prefix='http://%s:%s' %(self.host,self.port)
		self.url_prefix_post=prefix+self.str_post
		self.url_prefix_get=prefix+self.str_get
		self.dir="%s:%s" %(self.drive,self.path)
		self.dir_new= "%s:%s_new" %(self.drive,self.path)
		self.dbservice=DBService(str(self.conn))
		self.service=UploadService(self.url_prefix_post,self.url_prefix_get)
		if self.mapping() :
			if self.map:
				self.start()
			else:
				logger.error("cannot map any points.")
		
	def mapping(self):
		try:
			self.all_point=self.dbservice.get_all_point()	# from db
		except Exception,e:
			logger.error("cannot connect to database, please check the connection string [%s] is correct or whether table [sRegister] exists or not: %s" %(self.conn,e))
			return False
		try:
			self.ep_point=self.service.get_point(self.buildingId) # from EpExhibit
		except Exception,e:
			logger.error('EP-WebAPI is not available: %s. URL="%s".' % (e,self.service.url) )
			return False
		if self.all_point and self.ep_point:
			for (k,v) in self.all_point.items():
				for item in self.ep_point:
					if k==item[3]:
						self.map[k]=item[0]
						break
		return True
		
	# read the config file 
	def read_config(self, config_file_path):  
		try:
			cf = ConfigParser.ConfigParser()  
			cf.readfp(open(config_file_path))
			buildingId = cf.get("baseconf", "buildingId")  
			host = cf.get("baseconf", "host")  
			port = cf.get("baseconf", "port") 
			interval = cf.getint("baseconf", "interval") 
			drive = cf.get("baseconf", "drive") 
			path = cf.get("baseconf", "path") 
			conn=cf.get("baseconf","connection")
			post = cf.get("baseconf", "post") 
			get = cf.get("baseconf", "get") 
			return (buildingId,host,port,interval,drive,path,conn,post,get)  
		except IOError:
			logger.error("File [%s] is not available." %config_file_path)
		except Exception,e:
			logger.error("wrong format or info from file [%s]." %config_file_path) 
	
	# return time tuple
	def get_first_item_time_from_txt(self):
		f=open(hour_file)
		try:
			line=f.readline()
			print line
			self.first_item_time_tuple = time.strptime(line, '%Y-%m-%d %H:%M:%S')  
			return self.first_item_time_tuple
		finally:
			f.close() 
		
	# set the value as the first time from table  
	def set_first_item_time(self):
		year,month,day,hour,minute,second=self.first_item_time_tuple[:6]
		timestamp=datetime.datetime(year,month,day,hour,minute,second)  
		timestamp=timestamp+datetime.timedelta(minutes=5) # add 5 minutes
		line=timestamp.strftime('%Y-%m-%d %H:%M:%S')
		f=open(hour_file,'w')
		try:
			f.write(line) 
		finally:
			f.close()	 
	
	# transfer energy data 
	def transfer(self,timestamp):
		try:  
			stamp=timestamp[:6]	  
			data=self.dbservice.get_energy_item(stamp) 
		except Exception,e:
			logger.error("cannot connect to database or table [tRecord] doesn't exists: %s" %e)
			return -1
		if not data or not self.dbservice.timestamp :
			logger.warning("energy item [%s-%s-%s %s:%s:%s] is lost." %stamp)	
			return 0
		ts='%s-%s-%s %s:%s:%s' %(self.dbservice.timestamp[:6]) 
		self.record={}
		recordlist=[]
		for (k,v) in data.items(): 
			if self.map[k]:
				id=self.map[k]
				self.record[id]=v
				recordlist.append((id,v,ts))
		return self.send_data(recordlist,ts) 
		
	def send_data(self,recordlist,ts): 
		if not recordlist:
			return 0 
		retry=0
		while retry<4:
			try:
				self.service.insert(recordlist) 
				logger.info("energy item [%s] is OK." %ts)  
				break
			except IOError,e:
				logger.error('cannot connect to [%s:%s]:%s, please check the network.' %(self.host,self.port,e))
				return -1
			except Exception,e:
				retry=retry+1
				logger.info("try to transfer energy item [%s], retry=%d ." %(ts,retry))
				continue  
		if retry==4:
			return 0 
		else:
			return 1
	
	def update(self):
		try:
			for (k,v) in self.record.items():
				self.service.update(k,v)
		except Exception,e:
			logger.error("cannot connect to database or table [tPoint] doesn't exists: %s" %e) 
	
	def init(self): 
		timestamp=self.get_first_item_time_from_txt() 
		delta=time.time()-time.mktime(timestamp) 
		if delta<0: # need to be less than now
			now = int(time.time()) 
			timeArray = time.localtime(now) 
			self.first_item_time_tuple=timeArray[:6]
			logger.info('The timestamp you set is two large. It is now changed from %s to %s.' %(timestamp,self.first_item_time_tuple))
		else: # maximum one of the two time stamp
			time_db=self.dbservice.get_next_time(timestamp) 
			if time_db:
				timestamp_db = time.strptime(str(time_db), '%Y-%m-%d %H:%M:%S')  
				diff=int(time.mktime(timestamp_db))-int(time.mktime(timestamp))
				if diff>0:
					timestamp=timestamp_db
			self.first_item_time_tuple=timestamp 
		# logger.info('Start to transfer energy data at %s-%s-%s %s:%s:%s.' % timestamp[:6])
		return timestamp
		
	def start(self):  
		update_enable=False 
		while 1:
			# tranfer in 5 minutes 
			timestamp=self.init()
			ts=self.first_item_time_tuple 
			delta=time.time()-int(time.mktime(ts))
			if delta<5*60:	# if time stamp is close to now, sleep until 6 minutes later. update and insert
				print 'waiting for data...'
				update_enable=True
				time.sleep(self.interval)
				continue
			if self.transfer(ts) ==-1: # cannot access to db or host:port
				logger.info("cannot access to db or [%s:%s], it will try again after 10s." %(self.host,self.port))
				time.sleep(10)
				continue
			else: 
				self.set_first_item_time() 
			if update_enable:
				self.update()
				update_enable=False
			
			#break #for test
		logger.info('Windows service [TransferEnergyData] is stopped.')	
			
			
class UploadService():
	def __init__(self,url_prefix_post,url_prefix_get):
		self.url_prefix_post=url_prefix_post
		self.url_prefix_get=url_prefix_get
		
	def post(self,url): 
		starttime=time.time()
		self.url=url
		f=urllib.urlopen(url)
		j=json.loads(f.read()) 
		endtime=time.time()
		t=(endtime-starttime)*1000
		logger.info('time cost=%d ms.' %t)	
		return j
	
	# update ep-point value
	def update(self,_id,value): 
		url=self.url_prefix_post+'update point set present_value="%s" where id=%d' %(value,_id)
		return self.post(url)
	
	# insert ep-point value 
	def insert(self,_id,value,time):
		url=self.url_prefix_post+'insert into record(id,update_time,point_id,value,other) values(NULL,"%s",%d,"%s",NULL)' %(time,_id,value)
		#logger.info('URL=%s' %url)	
		return self.post(url)
	
	def insert(self,data):
		url=self.url_prefix_post+'insert into record(id,update_time,point_id,value,other) values'
		for item in data:
			_id,value,time=item
			url=url+'(NULL,"%s",%d,"%s",NULL),' %(time,_id,value)
		url=url.rstrip(',')
		url=url+';'
		#logger.info('URL=%s' %url)	
		return self.post(url)
	
	def execute(self,sql):
		url=self.url_prefix_post+sql
		return self.post(url)
	
	# get all ep-point via web-api 	
	def get_point(self,buildingId):
		url=self.url_prefix_get+ str(buildingId)  
		return self.post(url) 


#conn='DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=PBEM;UID=sa;PWD=fxjl;\
#	charset ="utf-8";'
class DBService():
	def __init__(self,conn):
		self.conn=conn
		self.timestamp=()
	
	# get all point 
	def get_all_point(self):
		ret={}
		cnxn = pyodbc.connect(self.conn)
		cursor = cnxn.cursor()
		cursor.execute("select r_id,r_name from sRegister")
		rows=cursor.fetchall()
		for row in rows:
			id=row[0]
			name= row[1] 
			ret[id]=name
		cursor.close()
		cnxn.close() 
		return ret
		
	# 	 
	def get_energy_item(self,timestamp): 
		ret={} 
		cnxn = pyodbc.connect(self.conn)
		cursor = cnxn.cursor()
		sql="select r_time,r_p_id,r_p_value from tRecord where DATEDIFF(ss,'%s-%s-%s %s:%s:%s',r_time)>=0 and DATEDIFF(ss,'%s-%s-%s %s:%s:%s',r_time)<300 and r_p_id<1000 order by r_time"  %(timestamp+timestamp)
		# logger.info('%s' %sql)
		cursor.execute(sql)
		rows=cursor.fetchall()
		if rows:
			first=True
			for row in rows:
				if first:
					first=False
					tmp=str(row[0])
					if '.' in tmp:
						index=tmp.index('.')
						stamp=tmp[:index]
					else:
						stamp=tmp[:-1] 
					self.timestamp =time.strptime(stamp, '%Y-%m-%d %H:%M:%S') 
				id=row[1]
				value=row[2]
				ret[id]=value
		cursor.close()
		cnxn.close()
		return ret

	#  
	def get_next_time(self,timestamp):
		cnxn = pyodbc.connect(self.conn)
		cursor = cnxn.cursor()
		sql="select top 1 r_time from tRecord where r_time>='%s-%s-%s %s:%s:%s' order by r_time"  %timestamp[:6]
		cursor.execute(sql)
		ret=cursor.fetchone()
		cursor.close()
		cnxn.close()
		if ret and len(ret):
			return ret[0]
		else:
			return ()
		 
		
def run():
	logger.info('Windows service [TransferEnergyData] starts to run.')
	file_name="%s\config.ini" %current_path
	dt=DataTransmission(file_name)

#a='http://www.pkpm.com.cn:8008/WebApi/Point.php?fun=sqlquery&param=insert into record(id,update_time,point_id,value,other) values(NULL,"2013-11-27 7:35:5",85,"4541.4",NULL),(NULL,"2013-11-27 7:35:5",86,"779.4",NULL),(NULL,"2013-11-27 7:35:5",87,"5511.0",NULL),(NULL,"2013-11-27 7:35:5",88,"5974.8",NULL),(NULL,"2013-11-27 7:35:5",89,"1109.5",NULL),(NULL,"2013-11-27 7:35:5",90,"6440.8",NULL),(NULL,"2013-11-27 7:35:5",91,"7892.3",NULL),(NULL,"2013-11-27 7:35:5",92,"494.5",NULL),(NULL,"2013-11-27 7:35:5",93,"718.9",NULL),(NULL,"2013-11-27 7:35:5",94,"1053.9",NULL),(NULL,"2013-11-27 7:35:5",95,"3690.6",NULL),(NULL,"2013-11-27 7:35:5",96,"6159.6",NULL),(NULL,"2013-11-27 7:35:5",97,"2395.4",NULL),(NULL,"2013-11-27 7:35:5",99,"258.3",NULL),(NULL,"2013-11-27 7:35:5",100,"3282.0",NULL),(NULL,"2013-11-27 7:35:5",101,"826.1",NULL),(NULL,"2013-11-27 7:35:5",102,"2660.0",NULL),(NULL,"2013-11-27 7:35:5",103,"5271.1",NULL),(NULL,"2013-11-27 7:35:5",104,"5463.4",NULL),(NULL,"2013-11-27 7:35:5",105,"6550.6",NULL),(NULL,"2013-11-27 7:35:5",106,"174.0",NULL),(NULL,"2013-11-27 7:35:5",107,"4895.5",NULL),(NULL,"2013-11-27 7:35:5",108,"1992.7",NULL),(NULL,"2013-11-27 7:35:5",109,"1209.5",NULL),(NULL,"2013-11-27 7:35:5",110,"1377.1",NULL),(NULL,"2013-11-27 7:35:5",111,"1585.5",NULL),(NULL,"2013-11-27 7:35:5",112,"2756.7",NULL),(NULL,"2013-11-27 7:35:5",113,"591.2",NULL),(NULL,"2013-11-27 7:35:5",114,"115.1",NULL);'
#f=urllib.urlopen(a)
#j=json.loads(f.read()) 
#print j
run()	

#if __name__=="__main__": 
#	run()
	 