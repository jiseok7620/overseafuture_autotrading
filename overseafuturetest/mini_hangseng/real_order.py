import win32com.client
import pythoncom
import time
import pandas as pd
import os
import datetime
from OverseasFutures.Short_Invest.ebest_server_login import login_cls # 실서버 로그인
from OverseasFutures.mini_hangseng.ebest_server_login import logindemo_cls # 모의서버 로그인

class OVH_cls:
    def __init__(self):
        self.진입가 = ''
        self.청산가 = ''
        self.손절가 = ''
        self.포지션 = ''
        
    def OnReceiveRealData(self, tr_code):
        symbol = self.GetFieldData("OutBlock", "symbol")
        hotime = self.GetFieldData("OutBlock", "hotime")
        offerho1 = self.GetFieldData("OutBlock", "offerho1")
        bidho1 = self.GetFieldData("OutBlock", "bidho1")
        
        print(hotime, symbol, offerho1, bidho1)
        
        '''
        if self.포지션 == "매수" :
            if offerho1 == self.진입가 :
                # 주문신규 - 주문완료면 1값을 return하도록
                pass
            elif offerho1 == self.청산가 : # + 주문완료상태이면
                # 청산신규
                pass
            elif offerho1 == self.손절가 : # + 주문완료상태이면
                # 손절신규
                pass
            elif 1 == 1 : # + 주문완료상태가 1분동안 아니면
                # 주문취소
                pass
    
        elif self.포지션 == "매도" :
            if offerho1 == self.진입가 :
                # 주문신규 - 주문완료면 1값을 return하도록
                pass
            elif offerho1 == self.청산가 : # + 주문완료상태이면
                # 청산신규
                pass
            elif offerho1 == self.손절가 : # + 주문완료상태이면
                # 손절신규
                pass
            elif 1 == 1 : # + 주문완료상태가 1분동안 아니면
                # 주문취소
                pass
        '''      
    
    def exe_OVH(self, 진입, 청산, 손절, 포지):
        ## 전역변수에 넣기
        self.진입가 = 진입
        self.청산가 = 청산
        self.손절가 = 손절
        self.포지션 = 포지
        
        ## 이베스트 로그인 ## 
        #logindemo_cls.exe_logindemo(self) # 모투 로그인
        #login_cls.exe_login(self) # 실투 로그인
        
        ## ----------------------------------------------------------------------------------------------- ##
        # 쿼리 객체 생성
        object_OVH = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", OVH_cls)
        
        # Res 파일 등록
        object_OVH.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OVH.res"
        
        # InBlock에 값 설정
        object_OVH.SetFieldData("InBlock", "symbol", "HMHH22")
        
        # 실시간데이터 요청
        object_OVH.AdviseRealData()
        
        # 수신 대기
        while True:
            pythoncom.PumpWaitingMessages()

#conn = OVH_cls()
#conn.exe_OVH("1","1","1","1")