import win32com.client
import pythoncom
from OverseasFutures.Short_Invest.ebest_server_login import login_cls # 실서버 로그인
from OverseasFutures.mini_hangseng.ebest_server_login import logindemo_cls # 모의서버 로그인

class OVC_cls:
    buy_sum = 0
    sell_sum = 0
    
    def OnReceiveRealData(self, tr_code):
        kordate = self.GetFieldData("OutBlock", "kordate")
        kortm = self.GetFieldData("OutBlock", "kortm")
        curpr = self.GetFieldData("OutBlock", "curpr")
        cgubun = self.GetFieldData("OutBlock", "cgubun")
        trdq = self.GetFieldData("OutBlock", "trdq")
        totq = self.GetFieldData("OutBlock", "totq")
        
        #print('시간 : ', kordate + kortm)
        #print('체결가 :', curpr)
        #print(trdq, cgubun)
        
        if cgubun == '+' :
            OVC_cls.buy_sum += int(trdq)
        else :
            OVC_cls.sell_sum += int(trdq)
            
        print('매수 :', OVC_cls.buy_sum, '/ 매도 :', OVC_cls.sell_sum)
    
    def exe_OVC(self):
        ## 이베스트 로그인 ## 
        logindemo_cls.exe_logindemo(self) # 모투 로그인
        
        ## ----------------------------------------------------------------------------------------------- ##
        # 쿼리 객체 생성
        object_OVC = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", OVC_cls)
        
        # Res 파일 등록
        object_OVC.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OVC.res"
        
        # InBlock에 값 설정
        object_OVC.SetFieldData("InBlock", "symbol", "HMHJ22")
        
        # 실시간데이터 요청
        object_OVC.AdviseRealData()
        
        # 수신 대기
        while True:
            pythoncom.PumpWaitingMessages()
            
            
            
conn = OVC_cls()
conn.exe_OVC()

'''
class OVC_cls:
    query_state = 0 # 쿼리 상태
    buy_sum = 0
    sell_sum = 0
    kordt = ''
    curprice = ''
    en_position = ''
    result_price = ''
    buy_max = 0
    sell_max = 0
    
    def OnReceiveRealData(self, tr_code):
        kordate = self.GetFieldData("OutBlock", "kordate")
        kortm = self.GetFieldData("OutBlock", "kortm")
        curpr = self.GetFieldData("OutBlock", "curpr")
        cgubun = self.GetFieldData("OutBlock", "cgubun")
        trdq = self.GetFieldData("OutBlock", "trdq")
        totq = self.GetFieldData("OutBlock", "totq")
        
        #print('시간 :', kordate+kortm)
        #print('가격 :', curpr)
        #print('+ :', OVC_cls.buy_sum, '- :', OVC_cls.sell_sum)
        
        if OVC_cls.buy_max == 0 :
            OVC_cls.buy_max = trdq
        else :
            if OVC_cls.buy_max < trdq :
                OVC_cls.buy_max = trdq
                print('시간 :', kordate+kortm, ' / ', curpr, ' / ', OVC_cls.buy_max)
            
        if OVC_cls.sell_max == 0 :
            OVC_cls.sell_max = totq
        else :
            if OVC_cls.sell_max < totq :
                OVC_cls.sell_max = totq
                print('시간 :', kordate+kortm, ' / ', curpr, ' / ', OVC_cls.sell_max)
        
        if cgubun == '+' :
            OVC_cls.buy_sum += int(trdq)
        else :
            OVC_cls.sell_sum += int(trdq)
            
        if OVC_cls.buy_sum + OVC_cls.sell_sum >= 500 :
            OVC_cls.query_state = 1
            self.UnadviseRealData() # 실시간데이터 요청 모두 취소
            OVC_cls.kordt = '실패'
            OVC_cls.curprice = '실패'    
        
        for i in OVC_cls.result_price :
            if curpr < i :
                OVC_cls.buy_sum = 0
                OVC_cls.sell_sum = 0
                break
            
        if OVC_cls.buy_sum >= 10 and OVC_cls.sell_sum >= 10 :
            if OVC_cls.en_position == '매수' and OVC_cls.buy_sum > OVC_cls.sell_sum :
                OVC_cls.query_state = 1
                self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                OVC_cls.kordt = kordate + kortm
                OVC_cls.curprice = curpr
                
            elif OVC_cls.en_position == '매도' and OVC_cls.buy_sum < OVC_cls.sell_sum:            
                OVC_cls.query_state = 1
                self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                OVC_cls.kordt = kordate + kortm
                OVC_cls.curprice = curpr
                
            elif OVC_cls.buy_sum + OVC_cls.sell_sum >= 1000 :
                OVC_cls.query_state = 1
                self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                OVC_cls.kordt = '실패'
                OVC_cls.curprice = '실패'
        
    def exe_OVC(self,포지션, result_price):
        # 변수 초기화
        OVC_cls.query_state = 0
        OVC_cls.buy_sum = 0
        OVC_cls.sell_sum = 0
        OVC_cls.en_position = 포지션
        OVC_cls.result_price = result_price
        
        # 쿼리 객체 생성
        object_OVC = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", OVC_cls)
        
        # Res 파일 등록
        object_OVC.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OVC.res"
        
        # InBlock에 값 설정
        object_OVC.SetFieldData("InBlock", "symbol", "HMHJ22")
        
        # 실시간데이터 요청
        object_OVC.AdviseRealData()
        
        # 수신 대기
        while OVC_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()
        
        return OVC_cls.kordt, OVC_cls.curprice, OVC_cls.buy_sum, OVC_cls.sell_sum
'''