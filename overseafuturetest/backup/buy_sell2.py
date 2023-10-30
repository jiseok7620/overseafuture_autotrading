import pandas as pd
import time
import datetime
import win32com.client
import pythoncom
from OverseasFutures.mini_hangseng.ebest_server_login import logindemo_cls
from OverseasFutures.Short_Invest.ebest_server_login import login_cls
from OverseasFutures.mini_hangseng.minuteData import o3103_cls
from OverseasFutures.mini_hangseng.bring_data import bring_data_cls
from OverseasFutures.mini_hangseng.send_sign import send_sign_cls
from OverseasFutures.mini_hangseng.minmaxLine_repeat import minmaxLine_repeat_cls
from OverseasFutures.mini_hangseng.message import cacao_login_cls
from OverseasFutures.mini_hangseng.orderNew import newbuy_cls
from OverseasFutures.mini_hangseng.orderCancel import orderCancel_cls

class all_cls:
    def __init__(self):
        # 0322 테스트 || 100*100 = 10000개 데이터, 과거 전후 150봉, 현재 전후 20봉
        # 단순이평 RSI, 단순 20이평
        
        # 0323 테스트 || 100*100 = 10000개 데이터, 과거 전후 100봉, 현재 전후 15봉
        # 단순이평 RSI, 단순 20이평 
        # 반대매매 확인하고 추가 필요 시 추가하기
        
        # 0324 테스트 || 전일, 당일 데이터만 사용, 전일 = 최대, 최저선, 당일 = 최대, 최저선, 10봉지지저항선, 중앙선
        # RSI, 단순 20이평
        
        # 1분, 5분데이터 // 최저선, 최대선 데이터 가져오기
        #bring_data_cls.exe_bring_data(self, 100, 150) # param1 : 반복수, param2 : 과거데이터 전후수
        bring_data_cls.exe_bring_data(self, "HMHH22", 25, 100)
        
    def exe_all(self, cacao_update):
        if cacao_update == "1" : 
            # 2개월마다 갱신
            # https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=49beafbf3d0867b0d7ad6679e63d85ea&redirect_uri=https://naver.com
            # => 여기서 나온 인가코드 아래 appropriation_code에 넣기
            appropriation_code = ""
            cacao_login_cls.token(self, appropriation_code)
        
        ##-----------------------------------------------------------------------------------------------------------##
        # 결과데이터 가져오기
        result_data = pd.read_excel('F:/JusikData/short_invest/result.xlsx', engine='openpyxl')
        
        # 1분, 5분 데이터
        dataset_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', engine='openpyxl')
        
        # 1분, 5분 최대-최저선 데이터
        inte_lowhigh_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', engine='openpyxl')
        
        ##-----------------------------------------------------------------------------------------------------------##
        # 1분마다 데이터 가져오기
        data_1m = o3103_cls.exe_o3103(self, "HMHH22", "1", "30", 1)
        data_1m = data_1m.reset_index(drop=True) # 인덱스 초기화
        data_1m = data_1m.drop(len(data_1m)-1) # 마지막 행 삭제 = 마지막 행은 현재시간으로 진행되고 있기 때문에
        data_1m['20이평'] = data_1m['종가'].rolling(window=20).mean() # 20일 이동평균만들기
        data_1m['RSI'] = bring_data_cls.make_rsi(self, data_1m, 14) # RSI 추가하기
        inte_df_1m = dataset_1m.append(data_1m, sort=False) # 전체 데이터에 하나의 데이터 추가
        inte_df_1m = inte_df_1m.drop_duplicates(['일시']) # 중복이 있으면 제거
        inte_df_1m = inte_df_1m.reset_index(drop=True) # 인덱스 초기화
        inte_df_1m.to_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', index=False) # 엑셀로 저장
        
        print('1분 추가 :',inte_df_1m.iloc[-1]['일시'].astype('str'))
        
        ##-----------------------------------------------------------------------------------------------------------##
        # 첫터치, 둘터치 데이터 가져와서, 둘터치 시 신호 발생
        결과, entry_price, goal_price, stop_price, entry_position, tic_count = send_sign_cls.exe_send_sign(self, inte_df_1m, inte_lowhigh_1m, result_data)
        if 결과 == "성공" :
            return 결과, entry_price, goal_price, stop_price, entry_position, tic_count
        
        ##-----------------------------------------------------------------------------------------------------------##
        # 최저선, 최대선 데이터 가져오기 => 일시, 가격, 거래량, 구분+ ...
        minmaxLine_repeat_cls.exe_minmaxLine_repeat(self, inte_lowhigh_1m, inte_df_1m, 15) # 15 = 시작시점 이후 데이터 전후수
        
        return '실패','실패','실패','실패','실패', '실패'
        
class TC3_cls:
    # query_state
    query_state = 0
    tc3_result = ''
    buy_price = 0
    
    def OnReceiveRealData(self, tr_code):
        ccls_prc = self.GetFieldData("OutBlock", "ccls_prc")
        
        TC3_cls.query_state = 1
        TC3_cls.tc3_result = '성공'
        TC3_cls.buy_price = ccls_prc
        self.UnadviseRealData() # 실시간데이터 요청 모두 취소
            
    def exe_TC3(self):
        # query_state 초기화
        TC3_cls.query_state = 0
        TC3_cls.tc3_result = ''
        
        ## 시간 측정
        now = datetime.datetime.now()
        start_time = now.strftime('%S')
        
        # 쿼리 객체 생성
        object_TC3 = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", TC3_cls)
        
        # Res 파일 등록
        object_TC3.ResFileName = "C:\\eBEST\\xingAPI\\Res\\TC3.res"
        
        # 실시간데이터 요청
        object_TC3.AdviseRealData()
        
        # 수신 대기
        while TC3_cls.query_state == 0:
            now2 = datetime.datetime.now()
            end_time = now2.strftime('%S')
            
            if str(int(start_time)+30) == str(end_time) :
                TC3_cls.query_state = 1
                TC3_cls.tc3_result = '실패'
                
            pythoncom.PumpWaitingMessages()
            
        return TC3_cls.tc3_result, TC3_cls.buy_price
            
class OVH_cls:
    # query_state
    query_state = 0 # 쿼리 상태
    goal_price = 0 # 목표 청산가
    stop_loss = 0 # 목표 손절가
    tic = 0 # 청산, 손절 틱수
    position = '' # 포지션
    ovh_result = '' # 청산 or 손절
    order_num = '' # 주문번호
    how = '' # 구매 or 판매
    acntno = '' # 계좌번호
    pwd = '' # 비밀번호
    isucode = '' # 인수코드
    ordqty = '' # 주문수량
    cc = newbuy_cls()
    dd = orderCancel_cls()
        
    def OnReceiveRealData(self, tr_code):
        offerho1 = self.GetFieldData("OutBlock", "offerho1") # 매도호가1
        offerho2 = self.GetFieldData("OutBlock", "offerho2") # 매도호가2
        offerho5 = self.GetFieldData("OutBlock", "offerho5") # 매도호가5
        bidho1 = self.GetFieldData("OutBlock", "bidho1") # 매수호가1        
        bidho2 = self.GetFieldData("OutBlock", "bidho2") # 매수호가2
        bidho5 = self.GetFieldData("OutBlock", "bidho5") # 매수호가5
        
        if OVH_cls.how == '구매' :
            if OVH_cls.position == '매수' : # 1: 매도, 2: 매수
                OVH_cls.ovh_result = '진입'
                OVH_cls.query_state = 1
                self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "2", str(offerho2), OVH_cls.ordqty)
                
            elif OVH_cls.position == '매도' :
                OVH_cls.ovh_result = '진입'
                OVH_cls.query_state = 1
                self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "1", str(bidho2), OVH_cls.ordqty)
                
        elif OVH_cls.how == '판매' :
            if OVH_cls.position == '매수' :
                if float(OVH_cls.goal_price) <= float(offerho5) : # 청산
                    OVH_cls.ovh_result = '청산'
                    OVH_cls.query_state = 1
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "1", str(bidho1), OVH_cls.ordqty)
                    
                elif float(OVH_cls.stop_loss) - 4 >= float(bidho5) : # 손절
                    OVH_cls.ovh_result = '손절'
                    OVH_cls.query_state = 1
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "1", str(bidho1), OVH_cls.ordqty)
                    
            elif OVH_cls.position == '매도' :
                if float(OVH_cls.goal_price) >= float(bidho5) : # 청산
                    OVH_cls.ovh_result = '청산'
                    OVH_cls.query_state = 1
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "2", str(offerho1), OVH_cls.ordqty)
                    
                elif float(OVH_cls.stop_loss) + 4  <= float(offerho5) : # 손절
                    OVH_cls.ovh_result = '손절'
                    OVH_cls.query_state = 1
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "2", str(offerho1), OVH_cls.ordqty)
        
    def exe_OVH(self, how_bs, 청산가, 손절가, 포지션, 틱수, Acntno, Pwd, Isucode, Ordqty):
        # 변수 초기화
        OVH_cls.query_state = 0
        OVH_cls.ovh_result = ''
        OVH_cls.goal_price = 청산가
        OVH_cls.stop_loss = 손절가
        OVH_cls.position = 포지션
        OVH_cls.tic = 틱수
        OVH_cls.how = how_bs
        OVH_cls.acntno = Acntno
        OVH_cls.pwd = Pwd
        OVH_cls.isucode = Isucode
        OVH_cls.ordqty = Ordqty
        
        # 쿼리 객체 생성
        object_OVH = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", OVH_cls)
        
        # Res 파일 등록
        object_OVH.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OVH.res"
        
        # InBlock에 값 설정
        object_OVH.SetFieldData("InBlock", "symbol", "HMHH22")
        
        # 실시간데이터 요청
        object_OVH.AdviseRealData()
        
        print('실시간 호가 받음')
        
        # 수신 대기
        while OVH_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()

        return OVH_cls.ovh_result, OVH_cls.order_num
    
if __name__ == "__main__":
    # 이베스트 로그인
    login = logindemo_cls()
    login.exe_logindemo()
    
    ## 클래스 객체 생성
    conn = all_cls()
    aa = TC3_cls()
    bb = OVH_cls()
    cc = newbuy_cls()
    dd = orderCancel_cls()
    mm = cacao_login_cls()
    
    # 기본 변수 설정
    acntno = "55500238871" # 계좌번호
    pwd = "1016" # 계좌비번
    isucode = "HMHH22" # 종목코드
    ordqty = "1" # 주문 수량
    
    while True:
        ## 시간 측정
        now = datetime.datetime.now()
        nowTime = now.strftime('%H%M%S')
        nowMinute = now.strftime('%M')
        start_time = now.strftime('%S')
        
        if start_time == '00' :
            print(nowTime)
            ## step 1. 매수 신호 발생
            result, 진입가, 청산가, 손절가, 포지션, 틱수 = conn.exe_all("0")
            print(result, '진입가 :', 진입가, '청산가 :', 청산가, '손절가 :', 손절가, '포지션 :', 포지션, '틱수 :', 틱수)
            
            #-------------------------------------------------------------------------------#
            if result == '성공' :
                ## 메세지 보내기 위해 토큰 미리 초기화
                token = mm.auth_refresh()
                
                #-------------------------------------------------------------------------------#
                ## step 2. 진입가로 진입
                mm.send_myself(token, '진입 시도') # 나에게 메세지보내기
                result1, OrdNo1 = bb.exe_OVH("구매", 청산가, 손절가, 포지션, 틱수, acntno, pwd, isucode, ordqty) # realdata에서 호가창을 보고 알맞게 진입하기
                
                #-------------------------------------------------------------------------------#
                ## step 3. 매수 완료 확인 => 30초 안에 매수 진입 안될 시 취소하기
                result2, buy_price = aa.exe_TC3()
                
                #-------------------------------------------------------------------------------#
                if result2 == '실패' :
                    mm.send_myself(token, str(진입가) + ' 진입 실패') # 나에게 메세지보내기
                    # 주문 취소를 위해 주문번호 만들기
                    for i in range(10-len(OrdNo1)):
                        OrdNo1 = "0" + OrdNo1
                    
                    ## step 4. 매수완료 실패 시 주문 취소하기
                    dd.exe_orderCancel(acntno, pwd, isucode, OrdNo1) # 주문 취소하기
                    mm.send_myself(token, str(진입가) + ' 주문 취소') # 나에게 메세지보내기
                
                #-------------------------------------------------------------------------------#
                ## step 5. 매수완료 성공 시 청산, 손절 대기하기
                elif result2 == '성공' :
                    mm.send_myself(token, str(buy_price) + ' 진입 성공') # 나에게 메세지보내기
                    
                    #-------------------------------------------------------------------------------#
                    ## step 6. 실시간으로 호가 조회하면서 손절가에 닿으면 주문 취소 후 손절가에 주문
                    result3, OrdNo2 = bb.exe_OVH("판매", 청산가, 손절가, 포지션, 틱수, acntno, pwd, isucode, ordqty) # realdata에서 호가창을 보고 알맞게 주문에 들어가기
                    
                    if result3 == '청산' :
                        result4, buy_price = aa.exe_TC3()
                        if result4 == '성공' : 
                            ## step 7-1. 청산에 성공하면 = 청산 성공 메세지 보내기
                            mm.send_myself(token, str(buy_price) + ' 청산 성공') # 나에게 메세지보내기
                        elif result4 == '실패' :
                            ## step 7-2. 청산에 실패하면 = 주문 취소 후 시장가로 청산하기
                            # 주문 취소를 위해 주문번호 만들기
                            for i in range(10-len(OrdNo2)):
                                OrdNo1 = "0" + OrdNo2
                            dd.exe_orderCancel(acntno, pwd, isucode, OrdNo2) # 주문 취소하기
                            mm.send_myself(token, str(buy_price) + ' 청산 실패, 주문 취소 완료, 재청산 요망') # 나에게 메세지보내기
                    
                    elif result3 == '손절' :
                        result4, buy_price = aa.exe_TC3()
                        if result4 == '성공' : 
                            ## step 7-3. 손절에 성공하면 = 손절 성공 메세지 보내기
                            mm.send_myself(token, str(buy_price) + ' 손절 성공') # 나에게 메세지보내기
                        elif result4 == '실패' :
                            ## step 7-4. 손절 실패하면 = 주문 취소 후 시장가로 손절하기
                            # 주문 취소를 위해 주문번호 만들기
                            for i in range(10-len(OrdNo2)):
                                OrdNo1 = "0" + OrdNo2
                            dd.exe_orderCancel(acntno, pwd, isucode, OrdNo2) # 주문 취소하기
                            mm.send_myself(token, str(buy_price) + ' 손절 실패, 주문 취소 완료, 재손절 요망') # 나에게 메세지보내기
                        
        time.sleep(0.1)
