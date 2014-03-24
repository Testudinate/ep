#encoding:utf-8
import pyodbc
import time
import datetime
import struct
'''
DBService for each building'db
'''

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
		print '@@@@@%s' %sql
		cursor.execute(sql)
		rows=cursor.fetchall()
		if rows:
			self.timestamp=rows[0][0]
			for row in rows:
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
		sql="select top 1 r_time from tRecord where r_time>'%s-%s-%s %s:%s:%s' order by r_time"  %timestamp[:6]
		cursor.execute(sql)
		ret=cursor.fetchone()
		cursor.close()
		cnxn.close()
		return ret[0]
	 
		 