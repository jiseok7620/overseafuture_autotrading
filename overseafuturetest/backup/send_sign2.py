from OverseasFutures.mini_hangseng.message import cacao_login_cls
from OverseasFutures.mini_hangseng.touch import touch_cls
import pandas as pd

class send_sign_cls:
    def exe_send_sign(self, inte_df_1m, inte_lowhigh_1m, result_data):
        close_1m = inte_df_1m.iloc[-1]['종가'] # 현재 종가 = 신호 시 진입가
        open_1m = inte_df_1m.iloc[-1]['시가'] # 현재 시가
        close_1m_ago = inte_df_1m.iloc[-2]['종가'] # 전일 종가
        todaydatetime_1m = inte_df_1m.iloc[-1]['일시'] # 일시
        
        # 터치 데이터
        touch_data_1m = touch_cls.exe_touch(self, inte_lowhigh_1m, close_1m, open_1m, close_1m_ago, todaydatetime_1m)
        touch_data_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
        
        # 둘터치 발생 시 알림
        info_1m_touch2 = touch_data_1m[touch_data_1m['둘터치'] != "없음"]
        
        # 1분 신호 발생
        if info_1m_touch2.empty:
            pass
        else:
            # 결과 출력하기
            result_append_1m = info_1m_touch2.astype('str')
            print('둘터치 발생(1분) : ', result_append_1m)
            
            for i in range(len(result_append_1m)):
                # 표시 데이터 변수
                minline_trend = result_append_1m.iloc[i]['추세']
                minline_dd = result_append_1m.iloc[i]['일시']
                minline_price = result_append_1m.iloc[i]['가격']
                minline_gubun = result_append_1m.iloc[i]['구분']
                first_touch_dd = result_append_1m.iloc[i]['첫터치']
                second_touch_dd = result_append_1m.iloc[i]['둘터치']
                invest_how = result_append_1m.iloc[i]['포지션'] # 포지션
                stop_loss = "" # 손절가
                ftouch_ind = inte_df_1m[inte_df_1m['일시'] == float(first_touch_dd)].index[0]
                stouch_ind = inte_df_1m[inte_df_1m['일시'] == float(second_touch_dd)].index[0]
                second_avg = inte_df_1m[inte_df_1m['일시'] == float(second_touch_dd)]['20이평'].iloc[0] # 둘터치 20이평선
                first_RSI = inte_df_1m[inte_df_1m['일시'] == float(first_touch_dd)]['RSI'].iloc[0] # 첫터치 RSI
                second_RSI = inte_df_1m[inte_df_1m['일시'] == float(second_touch_dd)]['RSI'].iloc[0] # 둘터치 RSI
                ago_RSI =inte_df_1m.iloc[stouch_ind-1]['RSI'] # 전일 RSI
                first_price = result_append_1m.iloc[i]['첫가격']
                second_price = result_append_1m.iloc[i]['둘가격']
                first_open =inte_df_1m.iloc[ftouch_ind]['시가'] # 첫터치 시가
                first_close =inte_df_1m.iloc[ftouch_ind]['종가'] # 첫터치 종가
                second_open =inte_df_1m.iloc[stouch_ind]['시가'] # 둘터치 시가
                second_close =inte_df_1m.iloc[stouch_ind]['종가'] # 둝처치 종가
                first_body = abs(first_open-first_close)
                second_body = abs(second_open-second_close)
                
                # 투자할지 말지 판단
                # 매수진입시 : 음봉시가 < 양봉종가 || 첫터치와 둘터치 사이의 봉이 3개 이하 || 음봉 시가와 양봉 종가의 틱수차이가 1이상 || 둘터치 봉크기가 첫터치의 5배이하
                if invest_how == "매수" and float(first_price) + 1 <= float(second_price) and stouch_ind - ftouch_ind <= 4 and first_body * 5 > second_body :
                    stop_loss = inte_df_1m[ftouch_ind:stouch_ind+1]['저가'].min() # 손절가
                    tic_num = close_1m - stop_loss # 손절 틱수
                    goal_price = close_1m + tic_num # 청산가
                    tic_range = abs(second_avg-close_1m)# 이평선과 진입가의 거리(틱수)
                    
                    # 첫터치, 둘터치 변경
                    touch_data_1m['첫터치'] = '없음'
                    touch_data_1m['지지저항'] = '없음'
                    touch_data_1m['첫가격'] = '없음'
                    touch_data_1m['둘터치'] = '없음'
                    touch_data_1m['포지션'] = '없음'
                    touch_data_1m['둘가격'] = '없음'
                    
                    # 엑셀로 저장
                    touch_data_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
                    
                    # 보낼메세지
                    sendMessage = "최저선(신호) 일시/가격/추세/구분 : " + minline_dd + " / " + minline_price + " / " + minline_trend + " / " + minline_gubun + \
                            "\n첫터치(대기) 일시 : " + first_touch_dd + \
                            "\n둘터치(진입) 일시 : " + second_touch_dd + \
                            "\n진입가 / 포지션 : " + str(close_1m) + " / " + invest_how + \
                            "\n손절가 / 청산가 : " + str(stop_loss)+"("+str(tic_num)+"틱)" + " / " + str(goal_price)+"("+str(tic_num)+"틱)"
                    
                    # 값 리턴하기
                    # 틱수 10 초과, 전봉 RSi 30이하이면 과매도세이므로 매수로만 진입
                    if tic_num > 10 and ago_RSI <= 30 :
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num
                    
                    # 틱수 10초과, 전봉 RSI 30~45, 이평선과 진입가의 차이가 tic_num보다 크면 매도세이지만 매수로 진입가능
                    elif tic_num > 10 and 30 < ago_RSI < 45 and tic_range > tic_num :
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num
                    
                    # 전봉의 RSI가 55~70사이이면 매수추세이므로 매수로 진입 가능
                    elif tic_num > 10 and 55 < ago_RSI < 70 :
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num
                        
                    # 전봉 또는 진입봉의 RSI가 45~55사이면 어디로 튈지모르니까 진입 금지
                    elif 45 <= second_RSI <= 55 or 45 <= ago_RSI <= 55 :
                        # 메세지 : 둘터치일자만 보내기
                        sendMessage = "[신호 실패] : RSI 45~55 사이" + second_touch_dd 
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                    
                    # 틱수 10 미만
                    elif tic_num < 10 :
                        # 메세지 : 둘터치일자만 보내기
                        sendMessage = "[신호 실패] : 틱수 10미만" + second_touch_dd
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                    
                    else :
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                    
                # 매도진입시 :음봉종가 < 양봉시가 || 첫터치와 둘터치 사이의 봉이 3개 이하 || 양봉 시가와 음봉 종가의 틱수차이가 1이상 || 둘터치 봉크기가 첫터치의 5배이하
                elif invest_how == "매도" and float(first_price) - 1 >= float(second_price) and stouch_ind - ftouch_ind <= 4 and first_body *5 > second_body :
                    stop_loss = inte_df_1m[ftouch_ind:stouch_ind+1]['고가'].max() # 손절가
                    tic_num = stop_loss - close_1m # 손절 틱수
                    goal_price = close_1m - tic_num # 청산가
                    tic_range = abs(second_avg-close_1m)# 이평선과 진입가의 거리(틱수)
                    
                    # 첫터치, 둘터치 변경
                    touch_data_1m['첫터치'] = '없음'
                    touch_data_1m['지지저항'] = '없음'
                    touch_data_1m['첫가격'] = '없음'
                    touch_data_1m['둘터치'] = '없음'
                    touch_data_1m['포지션'] = '없음'
                    touch_data_1m['둘가격'] = '없음'
                    
                    # 엑셀로 저장
                    touch_data_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
                    
                    # 보낼메세지
                    sendMessage = "최저선(신호) 일시/가격/추세/구분 : " + minline_dd + " / " + minline_price + " / " + minline_trend + " / " + minline_gubun + \
                    "\n첫터치(대기) 일시 : " + first_touch_dd + \
                    "\n둘터치(진입) 일시 : " + second_touch_dd + \
                    "\n진입가 / 포지션 : " + str(close_1m) + " / " + invest_how + \
                    "\n손절가 / 청산가 : " + str(stop_loss)+"("+str(tic_num)+"틱)" + " / " + str(goal_price)+"("+str(tic_num)+"틱)"
                    
                    # 값 리턴하기
                    # 틱수 10초과, 전봉 RSI 70 이상이면 과매수세이므로 매도로만 진입
                    if tic_num > 10 and ago_RSI >= 70 :
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num
                    
                    # 틱수 10초과, 전봉 RSI 55~70, 이평선과 진입가의 차이가 tic_num보다 크면 매수세이지만 매도로 진입 가능
                    elif tic_num > 10 and 55 < ago_RSI < 70 and tic_range > tic_num :
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num
                    
                    # 전봉의 RSI가 30~45사이이면 매도추세이므로 매도로 진입 가능
                    elif tic_num > 10 and 30 < ago_RSI < 45 :
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num
                    
                    # 전봉과 진입봉의 RSI가 45~55사이면 어디로 튈지모르니까 진입 금지
                    elif 45 <= second_RSI <= 55 or 45 <= ago_RSI <= 55 :
                        # 메세지 : 둘터치일자만 보내기
                        sendMessage = "[신호 실패] : RSI 45~55 사이" + second_touch_dd 
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                    
                    # 틱수 10 미만
                    elif tic_num < 10 :
                        # 메세지 : 둘터치일자만 보내기
                        sendMessage = "[신호 실패] : 틱수 10미만" + second_touch_dd
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                    
                    else :
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                else :
                    # 둘터치 발생 시 해당 인덱스 가져오기
                    touch_data_sec_ind = touch_data_1m[touch_data_1m['일시'] == float(minline_dd)].index[0]
                    
                    # 둘터치의 데이터를 첫터치로 바꾸기
                    # 둘터치 -> 첫터치 // 포지션 : 매도 -> 지지, 매수 -> 저항 // 둘가격 : 종가 -> 시가
                    if invest_how == '매도' :
                        trans_po = '지지' 
                    elif invest_how == '매수' :
                        trans_po = '저항'
                    trans_pr = inte_df_1m.iloc[stouch_ind]['시가']
                    
                    # 1분 첫터치에 둘터치 데이터 넣기
                    touch_data_1m.loc[touch_data_sec_ind, '첫터치'] = second_touch_dd
                    touch_data_1m.loc[touch_data_sec_ind, '지지저항'] = trans_po
                    touch_data_1m.loc[touch_data_sec_ind, '첫가격'] = float(trans_pr)
                    
                    # 둘터치는 '없음'으로 바꾸기
                    touch_data_1m.loc[touch_data_sec_ind, '둘터치'] = '없음'
                    touch_data_1m.loc[touch_data_sec_ind, '포지션'] = '없음'
                    touch_data_1m.loc[touch_data_sec_ind, '둘가격'] = '없음'
                    
                    # 엑셀로 저장
                    touch_data_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
                    
                    # 메세지 : 신호일자, 첫터치일자, 둘터치일자만 보내기
                    sendMessage = "[신호 실패]" + \
                    "실패신호 일시 : " + minline_dd + \
                    "\n첫터치(대기) 일시 : " + first_touch_dd + \
                    "\n둘터치(진입) 일시 : " + second_touch_dd + \
                    "\n첫둘가격차이 / 첫둘봉차이 : " + str(float(first_price)-float(second_price)) + " / " + str(stouch_ind - ftouch_ind) + \
                    "\n첫둘몸통차이 : " + str(first_body) + " / " + str(second_body)
                    
                    # 메세지 보내기
                    token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                    cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                    
                    # 정지
                    continue
                
        return '실패', '실패', '실패', '실패', '실패', '실패'

'''
# 결과데이터 가져오기
result_data = pd.read_excel('F:/JusikData/short_invest/result.xlsx', engine='openpyxl')

# 1분, 5분 데이터
dataset_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', engine='openpyxl')
dataset_5m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng5.xlsx', engine='openpyxl')

# 1분, 5분 최대-최저선 데이터
inte_lowhigh_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', engine='openpyxl')
inte_lowhigh_5m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng_lh5m.xlsx', engine='openpyxl') 

conn = send_sign_cls()
conn.exe_send_sign(dataset_1m, dataset_5m, inte_lowhigh_1m, inte_lowhigh_5m, result_data)
'''