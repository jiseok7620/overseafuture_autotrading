from OverseasFutures.mini_hangseng.touch import touch_cls

class send_sign_cls:
    def exe_send_sign(self, inte_df_1m, inte_lowhigh_1m, result_data):
        close_1m = inte_df_1m.iloc[-1]['종가'] # 현재 종가 = 신호 시 진입가
        open_1m = inte_df_1m.iloc[-1]['시가'] # 현재 시가
        if len(inte_df_1m) == 1:
            close_1m_ago = close_1m
        else:
            close_1m_ago = inte_df_1m.iloc[-2]['종가'] # 전일 종가
        todaydatetime_1m = inte_df_1m.iloc[-1]['일시'] # 일시
        
        # 터치 데이터
        touch_data_1m = touch_cls.exe_touch(self, inte_lowhigh_1m, close_1m, open_1m, close_1m_ago, todaydatetime_1m)
        touch_data_1m.to_excel('F:/JusikData/short_invest/test/mini_hangseng_lh1m.xlsx', index=False)
        
        # 첫터치 발생 시 알림
        info_1m_touch1 = touch_data_1m[touch_data_1m['첫터치'] != "없음"]
        info_1m_touch1 = info_1m_touch1[info_1m_touch1['첫터치'] != "끝"]
        
        # 1분 신호 발생
        if info_1m_touch1.empty:
            # 결과 리턴
            return '실패', '실패', '실패' 
        else:
            # 결과 출력하기
            result_append_1m = info_1m_touch1.astype('str')
            print('첫터치 발생(1분) : ', result_append_1m)
            
            for i in range(len(result_append_1m)):
                # 표시 데이터 변수
                minline_dd = result_append_1m.iloc[i]['일시'] # 최대,최저선 일시
                
                # 결과 저장
                result_data = result_data.append(result_append_1m, sort=False)
                result_data.to_excel('F:/JusikData/short_invest/test/result.xlsx', index=False)
                
                # 터치 발생 시 해당 인덱스 가져오기
                touch_data_sec_ind = touch_data_1m[touch_data_1m['일시'] == float(minline_dd)].index[0]
                
                # 터치는 '끝'으로 바꾸기
                touch_data_1m.loc[touch_data_sec_ind, '첫터치'] = '끝'
                touch_data_1m.loc[touch_data_sec_ind, '지지저항'] = '끝'
                touch_data_1m.loc[touch_data_sec_ind, '첫가격'] = '끝'
                touch_data_1m.loc[touch_data_sec_ind, '둘터치'] = '끝'
                touch_data_1m.loc[touch_data_sec_ind, '포지션'] = '끝'
                touch_data_1m.loc[touch_data_sec_ind, '둘가격'] = '끝'
                
                # 엑셀로 저장
                touch_data_1m.to_excel('F:/JusikData/short_invest/test/mini_hangseng_lh1m.xlsx', index=False)
                
                # 결과 리턴
                return '성공', '성공', '성공' 