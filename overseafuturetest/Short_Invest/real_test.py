import win32com.client
import pythoncom
import time
from OverseasFutures.Short_Invest.ebest_server_login import login_cls

class XReal_S3_:
    def __init__(self):
        login_cls.exe_login(self)
        super().__init__()
        self.count = 0

    def OnReceiveRealData(self, tr_code): # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        stockcode = self.GetFieldData("OutBlock", "shcode")
        price = self.GetFieldData("OutBlock", "price")
        chetime = self.GetFieldData("OutBlock", "chetime")
        print(self.count, stockcode, price, chetime)

    def start(self):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\S3_.res" # RES 파일 등록
        self.SetFieldData("InBlock", "shcode", "020560")
        self.AdviseRealData() # 실시간데이터 요청

    def add_item(self, stockcode):
        # 실시간데이터 요청 종목 추가
        self.SetFieldData("InBlock", "shcode", stockcode)
        self.AdviseRealData()

    def remove_item(self, stockcode):
        # stockcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(stockcode)

    def end(self):
        self.UnadviseRealData() # 실시간데이터 요청 모두 취소

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xreal

if __name__ == "__main__":
    def get_real_data():
        xreal = XReal_S3_.get_instance()
        xreal.start()
        
        while True:
            pythoncom.PumpWaitingMessages()
            
        '''
        while xreal.count < 100:
            pythoncom.PumpWaitingMessages()
            if xreal.count == 5:
                xreal.add_item("003490") # 대한항공 추가
            
            if xreal.count == 20:
                xreal.remove_item("005930")
            
            if xreal.count == 30:
                xreal.end()
                time.sleep(10)
                print("---- end -----")
                break
        '''
        
get_real_data()