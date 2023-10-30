import win32com.client
import pythoncom
from ebest_server_login import logindemo_cls # 모의서버 로그인

class newbuy_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        newbuy_cls.query_state = 1
        print(code, ' : 데이터 수신 완료')
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('신규주문에러 : ', err)
        print(msgco)
        print(msg)
    
    def exe_newbuy(self, acntno, pwd, isucode, bnstp, ordprc, ordqty):
        # 로그인
        logindemo_cls.exe_logindemo(self)
        
        # query_state
        newbuy_cls.query_state = 0
        
        ## ----------------------------------------------------------------------------------------------- ##
        # 쿼리 객체 생성
        object_newbuy = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", newbuy_cls)
        
        # Res 파일 등록
        object_newbuy.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CIDBT00100.res"
        
        # InBlock에 값 설정
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "AcntNo", 0, acntno) # 계좌번호
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "Pwd", 0, pwd) # 비밀번호
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "IsuCodeVal", 0, isucode) # 종목코드
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "FutsOrdTpCode", 0, "1") # 선물주문구분코드 : 1=신규
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "BnsTpCode", 0, bnstp) # 매매구분코드 : 1=매도, 2=매수
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "AbrdFutsOrdPtnCode", 0, "2") # 해외선물주문유형코드 1=시장가, 2=지정가
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "OvrsDrvtOrdPrc", 0, ordprc) # 해외파생주문가격
        object_newbuy.SetFieldData("CIDBT00100InBlock1", "OrdQty", 0, ordqty) # 주문수량

        # 데이터 요청
        object_newbuy.Request(False)
        
        # 수신 대기
        while newbuy_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()
        
        # 데이터 가져오기
        date = object_newbuy.GetFieldData("CIDBT00100OutBlock1", "OrdDt", 0) # 일자
        jongcode = object_newbuy.GetFieldData("CIDBT00100OutBlock1", "IsuCodeVal", 0) # 종목코드
        order_how = object_newbuy.GetFieldData("CIDBT00100OutBlock1", "BnsTpCode", 0) # 매매구분코드 : 1=매도, 2=매수
        order_price = object_newbuy.GetFieldData("CIDBT00100OutBlock1", "OvrsDrvtOrdPrc", 0) # 해외파생주문가격
        order_count = object_newbuy.GetFieldData("CIDBT00100OutBlock1", "OrdQty", 0) # 주문수량
        order_num = object_newbuy.GetFieldData("CIDBT00100OutBlock2", "OvrsFutsOrdNo", 0) # 주문번호
        
        return order_num
    
#conn = newbuy_cls()
#conn.exe_newbuy("55500238871", "1016", "HMHJ22", "2", "21850", "1")