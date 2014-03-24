#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import win32event
import win32service
import win32serviceutil

SERVICE_NAME="TransferEnergyDataService"
SERVICE_DISPLAY_NAME="python27 transferEngergyData service"
SERVICE_DESCRIPTION='''Energy data transmission service developed by OUYANG.'''
PYTHON_COMMAND="python transferEngergyData.py"

class WinService(win32serviceutil.ServiceFramework):
	# '''Python Windows Service''' 
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		
    def SvcStop(self):
        # 先告诉SCM停止这个过程
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)
		
    def SvcDoRun(self):
        command= PYTHON_COMMAND
        try:
            Proc=Popen(command,shell=True,stdout=PIPE,stderr=STDOUT)  
            Str=RRDDataProc.stdout.readline()  
        except:  
            Str="error happend" 
        # 等待服务被停止
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
		
if __name__=='__main__':
    win32serviceutil.HandleCommandLine(WinService)