import pandas as pd
import openpyxl
import os
import win32com.client
import pythoncom
import time

class ebestapi_orderCancel_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_orderCancel_cls.query_state = 1
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('ebestapi_orderCancel_cls 에러발생 : ', err)
        
class orderCancel_cls:
    def exe_orderCancel(self, AcntNo, Pwd, IsuCode, OrdNo):
        # 쿼리 객체 생성
        object_orderCancel = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_orderCancel_cls)
        
        # Res 파일 등록
        object_orderCancel.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CIDBT01000.res"
        
        # InBlock에 값 설정
        object_orderCancel.SetFieldData("CIDBT01000InBlock1", "AcntNo", 0, AcntNo) # 계좌번호
        object_orderCancel.SetFieldData("CIDBT01000InBlock1", "Pwd", 0, Pwd) # 비밀번호
        object_orderCancel.SetFieldData("CIDBT01000InBlock1", "IsuCodeVal", 0, IsuCode) # 종목코드
        object_orderCancel.SetFieldData("CIDBT01000InBlock1", "OvrsFutsOrgOrdNo", 0, OrdNo) # 주문번호 : 우측정렬 후 나머지는 0을 할당 [0000012345]
        object_orderCancel.SetFieldData("CIDBT01000InBlock1", "FutsOrdTpCode", 0, "3") # 선물주문구분코드 : 3=취소
        
        # 데이터 요청
        object_orderCancel.Request(False)
        
        # 수신 대기
        while ebestapi_orderCancel_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()
        
        # 필요한 필드 가져오기
        date = object_orderCancel.GetFieldData("CIDBT01000OutBlock1", "OrdDt", 0) # 일자
        jongcode = object_orderCancel.GetFieldData("CIDBT01000OutBlock1", "IsuCodeVal", 0) # 종목코드
        order_num = object_orderCancel.GetFieldData("CIDBT01000OutBlock2", "OvrsFutsOrdNo", 0) # 주문번호       
        nessage = object_orderCancel.GetFieldData("CIDBT01000OutBlock2", "InnerMsgCnts", 0) # 내부메세지
        
        return nessage
