import json,urllib
import time 

from logger import Logger 
from path import module_path
__dir__ = module_path()
logger=Logger(logname='%s\\log.txt' %__dir__,loglevel=1,logger=__file__).getlog()

class UploadService():
	def __init__(self,url_prefix_post,url_prefix_get):
		self.url_prefix_post=url_prefix_post
		self.url_prefix_get=url_prefix_get
		
	def post(self,url):  
		self.url=url
		f=urllib.urlopen(url)
		j=json.loads(f.read()) 
		endtime=time.time() 	
		return j
	
	# update ep-point value
	def update(self,_id,value): 
		url=self.url_prefix_post+'update point set present_value="%s" where id=%d' %(value,_id)
		return self.post(url)
	
	def update(self,data): 
		for item in data: 
			_id,value,time=item
			url=self.url_prefix_post+'update point set present_value="%s" where id=%d' %(value,_id)
			self.post(url)    
	
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