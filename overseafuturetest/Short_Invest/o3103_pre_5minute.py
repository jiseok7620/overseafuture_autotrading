import pandas as pd
import openpyxl
import os
import time
import win32com.client
import pythoncom
import time as tm
from OverseasFutures.Short_Invest.ebest_server_login import login_cls
from _ast import If

class ebestapi_o3103_5m_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_o3103_5m_cls.query_state = 1
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('o3103_5m 에러발생 : ', err)

class o3103_5m_cls:
    def exe_o3103_5m(self):
        # 쿼리 객체 생성 
        object_o3103 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_o3103_5m_cls)
        
        # Res 파일 등록
        object_o3103.ResFileName = "C:\\eBEST\\xingAPI\\Res\\o3103.res"

        # 쿼리 상태 초기화 
        ebestapi_o3103_5m_cls.query_state = 0
        
        # InBlock에 값 설정
        object_o3103.SetFieldData("o3103InBlock", "shcode", 0, "HMHH22") # 조회 종목 코드(CME 거래소는 신청해야 가능)
        object_o3103.SetFieldData("o3103InBlock", "ncnt", 0, "5") # 조회 분 
        object_o3103.SetFieldData("o3103InBlock", "readcnt", 0, "1") # 조회 개수
        object_o3103.SetFieldData("o3103InBlock", "cts_date", 0, "")
        object_o3103.SetFieldData("o3103InBlock", "cts_time", 0, "")
            
        # 데이터 요청
        object_o3103.Request(False)
        
        # 10분내 요청한 요청 횟수 취득
        count_limit = object_o3103.GetTRCountLimit("o3103")
        count_request = object_o3103.GetTRCountRequest("o3103")
        print('o3103_5m 10분 당 제한 건수 : ', count_limit)
        print('o3103_5m 10분 내 요청 횟수 : ', count_request)
        
        # 수신 대기
        while ebestapi_o3103_5m_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()
            
        arr_datetime = [] # 일시
        arr_open = [] # 시가
        arr_high = [] # 고가
        arr_low = [] # 저가
        arr_close = [] # 종가
        arr_volume = [] # 거래량
        
        # 필요한 필드 가져오기
        date = object_o3103.GetFieldData("o3103OutBlock1", "date", 0)
        time = object_o3103.GetFieldData("o3103OutBlock1", "time", 0)
        open = object_o3103.GetFieldData("o3103OutBlock1", "open", 0)
        high = object_o3103.GetFieldData("o3103OutBlock1", "high", 0)
        low = object_o3103.GetFieldData("o3103OutBlock1", "low", 0)
        close = object_o3103.GetFieldData("o3103OutBlock1", "close", 0)
        volume = object_o3103.GetFieldData("o3103OutBlock1", "volume", 0)
        
        arr_datetime.append(date + time)
        arr_open.append(open)
        arr_high.append(high)
        arr_low.append(low)
        arr_close.append(close)
        arr_volume.append(volume)
            
        # 데이터 프레임으로 만들기
        data = pd.DataFrame({'일시' : arr_datetime, '시가' : arr_open, 
                             '고가' : arr_high, '저가' : arr_low, '종가' : arr_close,
                             '거래량' : arr_volume                           
                             })
        
        # 데이터 타입 바꾸기
        dataset = data.astype({'시가':'float'})
        dataset = dataset.astype({'고가':'float'})
        dataset = dataset.astype({'저가':'float'})
        dataset = dataset.astype({'종가':'float'})
        dataset = dataset.astype({'거래량':'float'})
        
        # 데이터프레임 리턴하기
        print(dataset)
        return dataset
'''
conn = o3103_5m_cls()
conn.exe_o3103_5m()
'''