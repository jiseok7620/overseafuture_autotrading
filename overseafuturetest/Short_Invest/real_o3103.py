import win32com.client
import pythoncom
import time
from OverseasFutures.Short_Invest.ebest_server_login import login_cls

class XReal_OVH_:
    def __init__(self):
        login_cls.exe_login(self)
        super().__init__()
        self.count = 0

    def OnReceiveRealData(self, tr_code): # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        symbol = self.GetFieldData("OutBlock", "symbol")
        hotime = self.GetFieldData("OutBlock", "hotime")
        offerho1 = self.GetFieldData("OutBlock", "offerho1")
        bidho1 = self.GetFieldData("OutBlock", "bidho1")
        
        print(self.count, symbol, hotime, offerho1, bidho1)
        
    def start(self):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OVH.res" # RES 파일 등록
        self.SetFieldData("InBlock", "symbol", "HMHG22")
        self.AdviseRealData() # 실시간데이터 요청

    def add_item(self, stockcode):
        # 실시간데이터 요청 종목 추가
        self.SetFieldData("InBlock", "symbol", stockcode)
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
        xreal = XReal_OVH_.get_instance()
        xreal.start()
        
        while True:
            pythoncom.PumpWaitingMessages()
            
get_real_data()