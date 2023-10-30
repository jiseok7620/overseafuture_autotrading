from OverseasFutures.mini_hangseng.message import cacao_login_cls
from OverseasFutures.mini_hangseng.touch import touch_cls
import pandas as pd

class send_sign_cls:
    def exe_send_sign(self, inte_df_1m, inte_lowhigh_1m, result_data):
        close_1m = inte_df_1m.iloc[-1]['종가'] # 현재 종가 = 신호 시 진입가
        open_1m = inte_df_1m.iloc[-1]['시가'] # 현재 시가
        high_1m = inte_df_1m.iloc[-1]['고가'] # 현재 고가
        low_1m = inte_df_1m.iloc[-1]['저가'] # 현재 저가
        todaydatetime_1m = inte_df_1m.iloc[-1]['일시'] # 일시
        center_line_prepare = round(inte_df_1m.iloc[-1]['중앙대비'],2) # 중앙대비가격
        
        # 터치 데이터
        touch_data_1m = touch_cls.exe_touch(self, inte_lowhigh_1m, close_1m, open_1m, high_1m, low_1m, todaydatetime_1m)
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
                minline_dd = result_append_1m.iloc[i]['일시'] # 기준선 일시
                minline_gubun = result_append_1m.iloc[i]['구분'] # 기준선 구분
                first_touch_dd = result_append_1m.iloc[i]['첫터치'] # 첫터치 일자
                second_touch_dd = result_append_1m.iloc[i]['둘터치'] # 둘터치 일자
                invest_how = result_append_1m.iloc[i]['포지션'] # 포지션
                stop_loss = "" # 손절가
                ftouch_ind = inte_df_1m[inte_df_1m['일시'] == float(first_touch_dd)].index[0] # 첫터치 인덱스
                stouch_ind = inte_df_1m[inte_df_1m['일시'] == float(second_touch_dd)].index[0] # 둘터치 인덱스
                first_RSI = inte_df_1m[inte_df_1m['일시'] == float(first_touch_dd)]['RSI'].iloc[0] # 첫터치 RSI
                second_RSI = inte_df_1m[inte_df_1m['일시'] == float(second_touch_dd)]['RSI'].iloc[0] # 둘터치 RSI
                ago_RSI =inte_df_1m.iloc[stouch_ind-1]['RSI'] # 전일 RSI
                first_open =inte_df_1m.iloc[ftouch_ind]['시가'] # 첫터치 시가
                first_close =inte_df_1m.iloc[ftouch_ind]['종가'] # 첫터치 종가
                second_open =inte_df_1m.iloc[stouch_ind]['시가'] # 둘터치 시가
                second_close =inte_df_1m.iloc[stouch_ind]['종가'] # 둘터치 종가
                first_body = abs(first_open-first_close)
                second_body = abs(second_open-second_close)
                
                # ROC 넣어보자
                minline_ind = inte_df_1m[inte_df_1m['일시'] == float(minline_dd)].index[0] # 기준선 인덱스
                section_ROC_min = inte_df_1m[minline_ind:stouch_ind+1]['저가'].min() # 기준선-진입 // 최저~진입 ROC
                section_ROC_max = inte_df_1m[minline_ind:stouch_ind+1]['고가'].max() # 기준선-진입 // 최저~진입 ROC
                similar_ROC = round((second_close-section_ROC_min)/(section_ROC_max-section_ROC_min) * 100,2)
                
                # 투자할지 말지 판단
                # 매수진입시 : 첫터치와 둘터치 사이의 봉이 5개 이하
                if invest_how == "매수" and stouch_ind - ftouch_ind <= 6 :
                    stop_loss = inte_df_1m[ftouch_ind:stouch_ind+1]['저가'].min() # 손절가
                    tic_num = close_1m - stop_loss # 손절 틱수
                    goal_price = close_1m + tic_num # 청산가
                    
                    # 첫터치, 둘터치 변경
                    touch_data_1m['첫터치'] = '없음'
                    touch_data_1m['지지저항'] = '없음'
                    touch_data_1m['첫가격'] = '없음'
                    touch_data_1m['둘터치'] = '없음'
                    touch_data_1m['포지션'] = '없음'
                    touch_data_1m['둘가격'] = '없음'
                    
                    # 엑셀로 저장
                    touch_data_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
                    
                    # 값 리턴하기
                    # 틱수 10 초과 진입 // RSI가 45~55은 제외
                    if tic_num > 10 and second_RSI >= 55 or second_RSI <= 45 :
                        # 보낼메세지
                        sendMessage = "최저선(신호)일시/구분 : " + minline_dd + " / " + minline_gubun + \
                            "\n첫터치(대기)일시 : " + first_touch_dd + \
                            "\n둘터치(진입)일시 : " + second_touch_dd + \
                            "\n진입가/포지션 : " + str(close_1m) + " / " + invest_how + \
                            "\n손절가/청산가 : " + str(stop_loss)+"("+str(tic_num)+"틱)" + " / " + str(goal_price)+"("+str(tic_num)+"틱)" + \
                            "\nRSI/ROC : " + str(second_RSI) + " / " + str(similar_ROC) + \
                            "\n중앙대비 : " + str(center_line_prepare) 
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num

                    # 틱수 10 미만 실패
                    elif tic_num < 10 :
                        # 메세지 : 둘터치일자만 보내기
                        sendMessage = "[신호 실패] : 틱수 10미만" + second_touch_dd
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                    
                # 매도진입시 : 첫터치와 둘터치 사이의 봉이 5개 이하
                elif invest_how == "매도" and stouch_ind - ftouch_ind <= 6 :
                    stop_loss = inte_df_1m[ftouch_ind:stouch_ind+1]['고가'].max() # 손절가
                    tic_num = stop_loss - close_1m # 손절 틱수
                    goal_price = close_1m - tic_num # 청산가
                    
                    # 첫터치, 둘터치 변경
                    touch_data_1m['첫터치'] = '없음'
                    touch_data_1m['지지저항'] = '없음'
                    touch_data_1m['첫가격'] = '없음'
                    touch_data_1m['둘터치'] = '없음'
                    touch_data_1m['포지션'] = '없음'
                    touch_data_1m['둘가격'] = '없음'
                    
                    # 엑셀로 저장
                    touch_data_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
                    
                    # 값 리턴하기
                    # 틱수 10 초과 진입 // RSI가 45~55은 제외
                    if tic_num > 10 and second_RSI >= 55 or second_RSI <= 45:
                        # 보낼메세지
                        sendMessage = "최저선(신호)일시/구분 : " + minline_dd + " / " + minline_gubun + \
                            "\n첫터치(대기)일시 : " + first_touch_dd + \
                            "\n둘터치(진입)일시 : " + second_touch_dd + \
                            "\n진입가/포지션 : " + str(close_1m) + " / " + invest_how + \
                            "\n손절가/청산가 : " + str(stop_loss)+"("+str(tic_num)+"틱)" + " / " + str(goal_price)+"("+str(tic_num)+"틱)" + \
                            "\nRSI/ROC : " + str(second_RSI) + " / " + str(similar_ROC) + \
                            "\n중앙대비 : " + str(center_line_prepare) 
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        
                        # 결과 저장
                        result_data = result_data.append(result_append_1m, sort=False)
                        result_data.to_excel('F:/JusikData/short_invest/result.xlsx', index=False)
                        return '성공', close_1m, goal_price, stop_loss, invest_how, tic_num

                    # 틱수 10 미만 실패
                    elif tic_num < 10 :
                        # 메세지 : 둘터치일자만 보내기
                        sendMessage = "[신호 실패] : 틱수 10미만" + second_touch_dd
                        
                        # 메세지 보내기
                        token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                        cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                        return '실패', '실패', '실패', '실패', '실패', '실패'
                    
                else :
                    # 둘터치 발생 시 해당 인덱스 가져오기
                    touch_data_sec_ind = touch_data_1m[touch_data_1m['일시'] == float(minline_dd)].index[0]
                    
                    # 첫터치, 둘터치 '없음'으로 바꾸기
                    touch_data_1m.loc[touch_data_sec_ind, '첫터치'] = '없음'
                    touch_data_1m.loc[touch_data_sec_ind, '지지저항'] = '없음'
                    touch_data_1m.loc[touch_data_sec_ind, '첫가격'] = '없음'
                    touch_data_1m.loc[touch_data_sec_ind, '둘터치'] = '없음'
                    touch_data_1m.loc[touch_data_sec_ind, '포지션'] = '없음'
                    touch_data_1m.loc[touch_data_sec_ind, '둘가격'] = '없음'
                    
                    # 엑셀로 저장
                    touch_data_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
                    
                    # 메세지 : 신호일자, 첫터치일자, 둘터치일자만 보내기
                    sendMessage = "[신호 실패]" + \
                    "실패신호 일시 : " + minline_dd + \
                    "\n첫터치(대기) 일시 : " + first_touch_dd + \
                    "\n둘터치(진입) 일시 : " + second_touch_dd
                    
                    # 메세지 보내기
                    token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                    cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                    
                    # 계속
                    continue
                
        return '실패', '실패', '실패', '실패', '실패', '실패'
