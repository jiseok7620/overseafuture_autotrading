from FuturesTrading.message import cacao_login_cls

class send_sign_cls:
    def exe_send_sign(self, inte_df_1m):
        date_1m = inte_df_1m.iloc[-1]['일시'] # 현재 일시
        close_1m = inte_df_1m.iloc[-1]['종가'] # 현재 종가
        open_1m = inte_df_1m.iloc[-1]['시가'] # 현재 시가
        
        if inte_df_1m.iloc[-1]['RSI'] >= 69 :
            inte_df_1m.loc[len(inte_df_1m)-1, '과열침체'] = '과열'
            
        elif inte_df_1m.iloc[-1]['RSI'] <= 31 :
            inte_df_1m.loc[len(inte_df_1m)-1, '과열침체'] = '침체'
            
        inte_df_1m.to_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', index=False) # 엑셀로 저장
        
        if len(inte_df_1m) >= 3 :
            last_info = inte_df_1m[inte_df_1m['과열침체'] != '없음']
            
            if len(last_info) > 0 :
                f_ind = inte_df_1m[inte_df_1m['일시'] == last_info.iloc[-1]['일시']].index[0]
                # 매도진입            
                if last_info.iloc[-1]['과열침체'] == '과열' and f_ind + 10 > len(inte_df_1m) :
                    if inte_df_1m.iloc[-2]['과열침체'] == '없음' and inte_df_1m.iloc[-1]['과열침체'] == '없음':
                        if inte_df_1m.iloc[-2]['RSI'] > inte_df_1m.iloc[-1]['RSI'] and close_1m < open_1m :
                            # 보낼메세지
                            sendMessage = "일시/구분 : " + str(date_1m) + " / " + '매도'
                            
                            # 메세지 보내기
                            token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                            cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                            
                            return '성공', '매도'
                        
                # 매수진입
                elif last_info.iloc[-1]['과열침체'] == '침체' and f_ind + 10 > len(inte_df_1m) :
                    if inte_df_1m.iloc[-2]['과열침체'] == '없음' and inte_df_1m.iloc[-1]['과열침체'] == '없음':
                        if inte_df_1m.iloc[-2]['RSI'] < inte_df_1m.iloc[-1]['RSI'] and close_1m > open_1m :
                            # 보낼메세지
                            sendMessage = "일시/구분 : " + str(date_1m) + " / " + '매수'
                            
                            # 메세지 보내기
                            token = cacao_login_cls.auth_refresh(self) # 토큰 초기화
                            cacao_login_cls.send_myself(self, token, sendMessage) # 나에게 메세지보내기
                            
                            return '성공', '매수'
        else :
            return '실패', '실패'
        
        return '실패', '실패'
