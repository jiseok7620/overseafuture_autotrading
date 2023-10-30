import pandas as pd
import openpyxl
import os
import win32com.client
import pythoncom
import time

class ebestapi_orderCorrect_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_orderCorrect_cls.query_state = 1
        #print(code, ' : ChartIndex 데이터 수신 완료')
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('ebestapi_orderCorrect_cls 에러발생 : ', err)
        #print('ChartIndex 메세지 : ', msg)
        
class orderCorrect_cls:
    def exe_orderCorrect(self, AcntNo, Pwd, OrdNo, IsuCode, BnsTp, OrdPrc, OrdQty):
        # query_state
        ebestapi_orderCorrect_cls.query_state = 0
        
        ## ----------------------------------------------------------------------------------------------- ##
        # 쿼리 객체 생성
        object_orderCorrect = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_orderCorrect_cls)
        
        # Res 파일 등록
        object_orderCorrect.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CIDBT00900.res"
        
        # InBlock에 값 설정
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "AcntNo", 0, AcntNo) # 계좌번호
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "Pwd", 0, Pwd) # 비밀번호
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "OvrsFutsOrgOrdNo", 0, OrdNo) # 주문번호 : 우측정렬 후 나머지는 0을 할당 [0000012345]
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "IsuCodeVal", 0, IsuCode) # 종목코드
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "FutsOrdTpCode", 0, "2") # 선물주문구분코드 : 2=정정
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "BnsTpCode", 0, BnsTp) # 매매구분코드 : 1=매도, 2=매수
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "AbrdFutsOrdPtnCode", 0, "2") # 해외선물주문유형코드 2=지정가
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "OvrsDrvtOrdPrc", 0, OrdPrc) # 해외파생주문가격
        object_orderCorrect.SetFieldData("CIDBT00900InBlock1", "OrdQty", 0, OrdQty) # 주문수량
        
        # 데이터 요청
        object_orderCorrect.Request(False)
        
        # 10분내 요청한 요청 횟수 취득
        count_limit = object_orderCorrect.GetTRCountLimit("CIDBT00900")
        count_request = object_orderCorrect.GetTRCountRequest("CIDBT00900")
        #print('ChartIndex 10분 당 제한 건수 : ', count_limit)
        #print('ChartIndex 10분 내 요청 횟수 : ', count_request)
        
        # 수신 대기
        while ebestapi_orderCorrect_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()
        
        # 데이터 가져오기
        date = object_orderCorrect.GetFieldData("CIDBT00900OutBlock1", "OrdDt", 0) # 일자
        jongcode = object_orderCorrect.GetFieldData("CIDBT00900OutBlock1", "IsuCodeVal", 0) # 종목코드
        order_how = object_orderCorrect.GetFieldData("CIDBT00900OutBlock1", "BnsTpCode", 0) # 매매구분코드 : 1=매도, 2=매수
        order_price = object_orderCorrect.GetFieldData("CIDBT00900OutBlock1", "OvrsDrvtOrdPrc", 0) # 해외파생주문가격
        order_count = object_orderCorrect.GetFieldData("CIDBT00900OutBlock1", "OrdQty", 0) # 주문수량
        order_num = object_orderCorrect.GetFieldData("CIDBT00900OutBlock2", "OvrsFutsOrdNo", 0) # 주문번호
        message = object_orderCorrect.GetFieldData("CIDBT00900OutBlock2", "InnerMsgCnts", 0) # 내부메세지 내용
        
        print(date, jongcode, order_how, order_price, order_count, order_num, message)
        
#conn = orderCorrect_cls()
# 지정가 매수
#conn.exe_orderCorrect("55500238871", "1016", "HMHH22", "2", "2", "18820", "1")
# 지정가 매도
#conn.exe_orderCorrect("55500238871", "1016", "", "HMHH22", "1", "2", "18790", "1")