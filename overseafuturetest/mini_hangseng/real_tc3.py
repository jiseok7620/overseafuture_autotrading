import win32com.client
import pythoncom
import time
import pandas as pd
import os
import datetime
from OverseasFutures.Short_Invest.ebest_server_login import login_cls # 실서버 로그인
from OverseasFutures.mini_hangseng.ebest_server_login import logindemo_cls # 모의서버 로그인

class TC3_cls:
    def __init__(self):
        pass
    
    def OnReceiveRealData(self, tr_code):
        ccd = self.GetFieldData("OutBlock", "s_b_ccd")
        ccls_q = self.GetFieldData("OutBlock", "ccls_q")
        ccls_prc = self.GetFieldData("OutBlock", "ccls_prc")
        
        print(ccd,ccls_q,ccls_prc)
        
        #return ccd, ccls_q, ccls_prc
            
    def exe_TC3(self):
        ## 이베스트 로그인 ## 
        #logindemo_cls.exe_logindemo(self) # 모투 로그인
        
        ## ----------------------------------------------------------------------------------------------- ##
        # 쿼리 객체 생성
        object_TC3 = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", TC3_cls)
        
        # Res 파일 등록
        object_TC3.ResFileName = "C:\\eBEST\\xingAPI\\Res\\TC3.res"
        
        # 실시간데이터 요청
        object_TC3.AdviseRealData()
        
        # 수신 대기
        while True:
            pythoncom.PumpWaitingMessages()
