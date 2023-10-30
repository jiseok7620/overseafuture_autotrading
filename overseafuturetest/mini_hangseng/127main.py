import pandas as pd
import time
import datetime
import win32com.client
import pythoncom
from OverseasFutures.mini_hangseng.ebest_server_login import logindemo_cls
from OverseasFutures.mini_hangseng.minuteData import o3103_cls
from OverseasFutures.mini_hangseng.bring_data import bring_data_cls
from OverseasFutures.mini_hangseng.send_sign import send_sign_cls
from OverseasFutures.mini_hangseng.minmaxLine_repeat import minmaxLine_repeat_cls
from OverseasFutures.mini_hangseng.message import cacao_login_cls
from OverseasFutures.mini_hangseng.orderNew import newbuy_cls
from OverseasFutures.mini_hangseng.orderCancel import orderCancel_cls
#from OverseasFutures.Short_Invest.ebest_server_login import login_cls
'''
주의사항
1. 해외선물은 마감일 몇일 전부터 당월선물은 api거래가 안됨(3월 29일)
'''
class all_cls:
    def __init__(self):
        # 종목코드
        self.jongcode = "HMHM22"
        
        # 1분 데이터를 전일 10:15~04:00만 뽑기
        ## 시간 측정
        agodate = "20220620"
        nowdate = "20220621"
        st_time = '091400'
        end_time = '030000'
        start_dd = int(agodate+st_time) # 전일 장시작
        end_dd = int(nowdate+end_time) # 전일 장마감
        self.now_dd = int(nowdate+st_time) # 오늘 장시작
        
        # 1분 // 전일 최저선, 최대선 데이터 가져오기
        bring_data_cls.exe_bring_data(self, self.jongcode, self.now_dd, start_dd, end_dd)
        
    def exe_all(self):
        ##-----------------------------------------------------------------------------------------------------------##
        # 결과데이터 가져오기
        result_data = pd.read_excel('F:/JusikData/short_invest/result.xlsx', engine='openpyxl')
        
        # 1분 데이터
        dataset_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', engine='openpyxl')
        
        # 1분 최대-최저선 데이터
        inte_lowhigh_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', engine='openpyxl')
        
        ##-----------------------------------------------------------------------------------------------------------##
        # 1분마다 데이터 가져오기
        data_1m = o3103_cls.exe_o3103(self, self.jongcode, "1", "100", 1)
        data_1m = data_1m[data_1m['일시'] >= self.now_dd] # 데이터 자르기
        data_1m['fastk'] = bring_data_cls.make_stochastic(self, data_1m, 14, '고가', '저가')
        data_1m = data_1m.reset_index(drop=True) # 인덱스 초기화
        data_1m = data_1m.drop(len(data_1m)-1) # 마지막 행 삭제 = 마지막 행은 현재시간으로 진행되고 있기 때문에
        inte_df_1m = dataset_1m.append(data_1m, sort=False) # 전체 데이터에 하나의 데이터 추가
        inte_df_1m = inte_df_1m.drop_duplicates(['일시']) # 중복이 있으면 제거
        inte_df_1m = inte_df_1m.reset_index(drop=True) # 인덱스 초기화
        inte_df_1m.to_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', index=False) # 엑셀로 저장
        
        #print('1분 추가 :',inte_df_1m.iloc[-1]['일시'].astype('str'))
        
        ##-----------------------------------------------------------------------------------------------------------##
        # 첫터치, 둘터치 데이터 가져와서, 둘터치 시 신호 발생
        결과, 포지션, 손절가, 목표가 = send_sign_cls.exe_send_sign(self, inte_df_1m, inte_lowhigh_1m, result_data)
        if 결과 == "성공" :
            return 결과, 포지션, 손절가, 목표가
        
        ##-----------------------------------------------------------------------------------------------------------##
        # 1분 최대-최저선 데이터 다시 로드
        inte_lowhigh_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', engine='openpyxl')
        
        # 최저선, 최대선 데이터 가져오기
        minmaxLine_repeat_cls.exe_minmaxLine_repeat(self, inte_lowhigh_1m, inte_df_1m, 20) # 숫자 = 시작시점 이후 데이터 전후수
        
        return '실패','실패', '실패', '실패'
    
class TC3_cls:
    # query_state
    query_state = 0
    tc3_result = ''
    buy_price = 0
    
    def OnReceiveRealData(self, tr_code):
        ccls_prc = self.GetFieldData("OutBlock", "ccls_prc")
        print('TC3_cls 진입성공 :',  ccls_prc)
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
            
            if str(int(start_time)+45) == str(end_time) :
                TC3_cls.query_state = 1
                TC3_cls.tc3_result = '실패'
                
            pythoncom.PumpWaitingMessages()
            
        return TC3_cls.tc3_result, TC3_cls.buy_price
    
class OVH_cls:
    # query_state
    query_state = 0 # 쿼리 상태
    position = '' # 포지션
    ovh_result = '' # 청산 or 손절
    order_num = '' # 주문번호
    order_price = 0 # 주문가격
    goal_price = 0 # 청산가
    stop_loss = 0 # 손절가
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
                OVH_cls.order_price = offerho2 # 주문가격
                self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "2", str(offerho2), OVH_cls.ordqty)
                print(str(offerho2), '에 매수진입')
                
            elif OVH_cls.position == '매도' :
                OVH_cls.ovh_result = '진입'
                OVH_cls.query_state = 1
                OVH_cls.order_price = bidho2 # 주문가격
                self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "1", str(bidho2), OVH_cls.ordqty)
                print(str(bidho2), '에 매도진입')
                
        elif OVH_cls.how == '판매' :
            if OVH_cls.position == '매수' :
                if float(OVH_cls.goal_price) + 4 <= float(offerho5) : # 청산
                    OVH_cls.ovh_result = '청산'
                    OVH_cls.query_state = 1
                    OVH_cls.order_price = bidho1 # 주문가격
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "1", str(bidho1), OVH_cls.ordqty)
                    
                elif float(OVH_cls.stop_loss) - 4 >= float(bidho5) : # 손절
                    OVH_cls.ovh_result = '손절'
                    OVH_cls.query_state = 1
                    OVH_cls.order_price = bidho1 # 주문가격
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "1", str(bidho1), OVH_cls.ordqty)
                    
            elif OVH_cls.position == '매도' :
                if float(OVH_cls.goal_price) - 4 >= float(bidho5) : # 청산
                    OVH_cls.ovh_result = '청산'
                    OVH_cls.query_state = 1
                    OVH_cls.order_price = offerho1 # 주문가격
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "2", str(offerho1), OVH_cls.ordqty)
                    
                elif float(OVH_cls.stop_loss) + 4  <= float(offerho5) : # 손절
                    OVH_cls.ovh_result = '손절'
                    OVH_cls.query_state = 1
                    OVH_cls.order_price = offerho1 # 주문가격
                    self.UnadviseRealData() # 실시간데이터 요청 모두 취소
                    OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "2", str(offerho1), OVH_cls.ordqty)
        
        elif OVH_cls.how == '시장가주문' :
            if OVH_cls.position == '매수' :
                OVH_cls.ovh_result = '시장가청산'
                OVH_cls.query_state = 1
                OVH_cls.order_price = bidho5 # 주문가격
                OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "1", str(bidho5), OVH_cls.ordqty)
            elif OVH_cls.position == '매도' :
                OVH_cls.ovh_result = '시장가청산'
                OVH_cls.query_state = 1
                OVH_cls.order_price = offerho5 # 주문가격
                OVH_cls.order_num = cc.exe_newbuy(OVH_cls.acntno, OVH_cls.pwd, OVH_cls.isucode, "2", str(offerho5), OVH_cls.ordqty)
                
    def exe_OVH(self, how_bs, 포지션, loss_pri, goal, Acntno, Pwd, Isucode, Ordqty):
        # 변수 초기화
        OVH_cls.query_state = 0
        OVH_cls.ovh_result = ''
        OVH_cls.position = 포지션
        OVH_cls.how = how_bs
        OVH_cls.acntno = Acntno
        OVH_cls.pwd = Pwd
        OVH_cls.isucode = Isucode
        OVH_cls.ordqty = Ordqty
        OVH_cls.order_price = 0
        OVH_cls.stop_loss = loss_pri
        OVH_cls.goal_price = goal
        
        # 쿼리 객체 생성
        object_OVH = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", OVH_cls)
        
        # Res 파일 등록
        object_OVH.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OVH.res"
        
        # InBlock에 값 설정
        object_OVH.SetFieldData("InBlock", "symbol", "HMHM22")
        
        # 실시간데이터 요청
        object_OVH.AdviseRealData()
        
        # 수신 대기
        while OVH_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()

        return OVH_cls.ovh_result, OVH_cls.order_num, OVH_cls.order_price
    
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
    acntno = "55500523871" # 계좌번호
    pwd = "1016" # 계좌비번
    isucode = conn.jongcode # 종목코드
    ordqty = "1" # 주문 수량
    
    while True:
        ## 시간 측정
        now = datetime.datetime.now()
        nowTime = now.strftime('%H%M%S')
        nowMinute = now.strftime('%M')
        start_time = now.strftime('%S')
        
        if start_time == '01' :
            #print(nowTime)
            # 실제 진입, 청산, 손절 로직
            result, 포지션, stop_loss, goal = conn.exe_all()
            #print(result, '포지션 : ', 포지션, '손절가 : ', stop_loss, '목표가 : ', goal)
            
            #-------------------------------------------------------------------------------#
            ## step 1. 매수 신호 발생
            if result == '성공' :
                ## 메세지 보내기 위해 토큰 미리 초기화
                token = mm.auth_refresh()
                
                #-------------------------------------------------------------------------------#
                ## step 2. 진입가로 진입
                result1, OrdNo1, OrdPrice = bb.exe_OVH("구매", 포지션, stop_loss, goal, acntno, pwd, isucode, ordqty) # realdata에서 호가창을 보고 알맞게 진입하기
                mm.send_myself(token, OrdPrice + '에  진입 시도') # 나에게 메세지보내기
                
                #-------------------------------------------------------------------------------#
                ## step 3. 매수 완료 확인 => 45초 안에 매수 진입 안될 시 취소하기
                result2, buy_price = aa.exe_TC3()
                
                #-------------------------------------------------------------------------------#
                ## step 4. 매수완료 실패 시 주문 취소하기
                if result2 == '실패' :
                    mm.send_myself(token, str(buy_price) + '에 진입 실패') # 나에게 메세지보내기
                    # 주문 취소를 위해 주문번호 만들기
                    for i in range(10-len(OrdNo1)):
                        OrdNo1 = "0" + OrdNo1
                    nessage = dd.exe_orderCancel(acntno, pwd, isucode, OrdNo1) # 주문 취소하기
                    mm.send_myself(token, str(nessage) + str(buy_price) + '에 주문 취소') # 나에게 메세지보내기
                
                #-------------------------------------------------------------------------------#
                ## step 5. 매수완료 성공 시 청산, 손절 대기하기
                elif result2 == '성공' :
                    mm.send_myself(token, str(buy_price) + '에 진입 성공') # 나에게 메세지보내기
                    
                    #-------------------------------------------------------------------------------#
                    ## step 6. 실시간으로 호가 조회하면서 손절가에 닿으면 주문 취소 후 손절가에 주문
                    result3, OrdNo2, OrdPrice = bb.exe_OVH("판매", 포지션, stop_loss, goal, acntno, pwd, isucode, ordqty) # realdata에서 호가창을 보고 알맞게 주문에 들어가기
                    
                    if result3 == '청산' :
                        result4, buy_price = aa.exe_TC3() # 실시간 주문 조회
                        if result4 == '성공' : 
                            ## step 7-1. 청산에 성공하면 = 청산 성공 메세지 보내기
                            mm.send_myself(token, str(buy_price) + '에 청산 성공') # 나에게 메세지보내기
                        elif result4 == '실패' :
                            ## step 7-2. 청산에 실패하면 = 주문 취소 후 시장가로 청산하기
                            # 주문 취소를 위해 주문번호 만들기
                            for i in range(10-len(OrdNo2)):
                                OrdNo2 = "0" + OrdNo2
                            nessage = dd.exe_orderCancel(acntno, pwd, isucode, OrdNo2) # 주문 취소하기
                            mm.send_myself(token, str(nessage) + str(buy_price) + '에 청산 실패, 주문 취소 완료, 재청산 요망') # 나에게 메세지보내기
                            
                            ## step 8-1. 시장가로 청산하기
                            result5, OrdNo3, OrdPrice = bb.exe_OVH("시장가주문", 포지션, stop_loss, goal, acntno, pwd, isucode, ordqty)
                            result6, buy_price = aa.exe_TC3() # 실시간 주문 조회
                            mm.send_myself(token, str(buy_price) + '에 시장가청산 성공') # 나에게 메세지보내기
                    
                    elif result3 == '손절' :
                        result4, buy_price = aa.exe_TC3() # 실시간 주문 조회
                        if result4 == '성공' : 
                            ## step 7-3. 손절에 성공하면 = 손절 성공 메세지 보내기
                            mm.send_myself(token, str(buy_price) + '에 손절 성공') # 나에게 메세지보내기
                        elif result4 == '실패' :
                            ## step 7-4. 손절 실패하면 = 주문 취소 후 시장가로 손절하기
                            # 주문 취소를 위해 주문번호 만들기
                            for i in range(10-len(OrdNo2)):
                                OrdNo2 = "0" + OrdNo2
                            nessage = dd.exe_orderCancel(acntno, pwd, isucode, OrdNo2) # 주문 취소하기
                            mm.send_myself(token, str(nessage) + str(buy_price) + '에 손절 실패, 주문 취소 완료, 재손절 요망') # 나에게 메세지보내기
                            
                            # step 8-2. 시장가로 손절하기
                            result5, OrdNo3, OrdPrice = bb.exe_OVH("시장가주문", 포지션, stop_loss, goal, acntno, pwd, isucode, ordqty)
                            result6, buy_price = aa.exe_TC3() # 실시간 주문 조회
                            mm.send_myself(token, str(buy_price) + '에 시장가손절 성공') # 나에게 메세지보내기
                            
        time.sleep(1)  
   
'''
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
    acntno = "55500523871" # 계좌번호
    pwd = "1016" # 계좌비번
    isucode = conn.jongcode # 종목코드
    ordqty = "1" # 주문 수량
    
    while True:
        ## 시간 측정
        now = datetime.datetime.now()
        nowTime = now.strftime('%H%M%S')
        nowMinute = now.strftime('%M')
        start_time = now.strftime('%S')
        
        if start_time == '01' :
            print(nowTime)
            result, 포지션, stop_loss, goal = conn.exe_all()
            print(result, '포지션 : ', 포지션, '손절가 : ', stop_loss, '목표가 : ', goal)
            
        time.sleep(1)  
'''