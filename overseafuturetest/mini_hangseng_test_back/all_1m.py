import pandas as pd
import time
import os
from OverseasFutures.mini_hangseng.ebest_server_login import logindemo_cls
from OverseasFutures.mini_hangseng.minuteData import o3103_cls
from OverseasFutures.mini_hangseng_test.send_sign import send_sign_cls
from OverseasFutures.mini_hangseng_test.minmaxLine_repeat import minmaxLine_repeat_cls


class all_cls:
    def exe_all(self):
        # 로그인
        logindemo_cls.exe_logindemo(self)
        
        # 반복 횟수
        repeat_num = 200
        code = "HMHK22"
        
        ## 시간 측정
        agodate = "20220518"
        nowdate = "20220519"
        tomdate = "20220520"
        st_time = '091400'
        end_time = '030000'
        start_dd = int(agodate+st_time) # 전일 장시작
        end_dd = int(nowdate+end_time) # 전일 장마감
        now_dd = int(nowdate+st_time) # 오늘 장시작
        tom_dd = int(tomdate+end_time) # 오늘 장마감
        
        # 1분 데이터 생성하기
        if os.path.isfile('F:/JusikData/short_invest/test/alldaydata/mini_hangseng.xlsx') :
            dataset = pd.read_excel('F:/JusikData/short_invest/test/alldaydata/mini_hangseng.xlsx', engine='openpyxl')
        else :
            dataset = o3103_cls.exe_o3103(self, code, "1", "100", repeat_num) # 종목코드, 몇분데이터, 몇개, 몇번반복
            
            # 엑셀로 저장
            dataset.to_excel('F:/JusikData/short_invest/test/alldaydata/mini_hangseng.xlsx', index=False)
        
        if os.path.isfile('F:/JusikData/short_invest/test/onedaydata/mini_hangseng'+nowdate+'.xlsx') :
            dataset_now = pd.read_excel('F:/JusikData/short_invest/test/onedaydata/mini_hangseng'+nowdate+'.xlsx', engine='openpyxl')
        else :
            # 당일 데이터만 추출
            dataset_now = dataset[dataset['일시'] >= now_dd]
            dataset_now = dataset_now[dataset['일시'] <= tom_dd]
            
            # 인덱스 초기화
            dataset_now = dataset_now.reset_index(drop=True) # 인덱스 초기화 
            
            # 당일 데이터 엑셀로 저장
            dataset_now.to_excel('F:/JusikData/short_invest/test/onedaydata/mini_hangseng'+nowdate+'.xlsx', index=False)
            
            #### 과거 최대선, 최저선 구하기 ####
            # 전일 데이터 자르기
            dataset_1m_ago = dataset[dataset['일시'] >= start_dd]
            dataset_1m_ago = dataset_1m_ago[dataset_1m_ago['일시'] <= end_dd]
            
            # 고가, 저가선 구하기
            mm = dataset_1m_ago['고가'].argmax()
            ss = dataset_1m_ago['저가'].argmin()
            inte_lowhigh_1m = pd.DataFrame({
                    '일시' : [dataset_1m_ago.iloc[mm]['일시'], dataset_1m_ago.iloc[ss]['일시']],
                    '시가' : [dataset_1m_ago.iloc[mm]['시가'], dataset_1m_ago.iloc[ss]['시가']],
                    '고가' : [dataset_1m_ago.iloc[mm]['고가'], dataset_1m_ago.iloc[ss]['고가']],
                    '저가' : [dataset_1m_ago.iloc[mm]['저가'], dataset_1m_ago.iloc[ss]['저가']],
                    '종가' : [dataset_1m_ago.iloc[mm]['종가'], dataset_1m_ago.iloc[ss]['종가']],
                    '거래량' : [dataset_1m_ago.iloc[mm]['거래량'], dataset_1m_ago.iloc[ss]['거래량']],
                    '구분' : ['전일최대','전일최소']
                })
            
            # 첫터치, 둘터치 열 추가
            inte_lowhigh_1m['기준가'] = (inte_lowhigh_1m['고가'] + inte_lowhigh_1m['저가'] + inte_lowhigh_1m['종가']) / 3
            inte_lowhigh_1m['전수'] = '없음'
            inte_lowhigh_1m['후수'] = '없음'
            inte_lowhigh_1m['첫터치'] = '없음'
            inte_lowhigh_1m['지지저항'] = '없음'
            inte_lowhigh_1m['첫가격'] = '없음'
            inte_lowhigh_1m['둘터치'] = '없음'
            inte_lowhigh_1m['포지션'] = '없음'
            inte_lowhigh_1m['둘가격'] = '없음'
            
            # 최대, 최저선 데이터 엑셀로 저장
            inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/test/mini_hangseng_lh1m.xlsx', index=False)
        
        #---------------------------------------------------------------------------------------------------------------------# 
        # 반복문의 시작
        for i in dataset_now.index :
            # 결과데이터 가져오기
            result_data = pd.read_excel('F:/JusikData/short_invest/test/result.xlsx', engine='openpyxl')
            
            # 1분 데이터
            dataset_1m = pd.read_excel('F:/JusikData/short_invest/test/mini_hangseng1r.xlsx', engine='openpyxl')
            
            # 1분 최대-최저선 데이터
            inte_lowhigh_1m = pd.read_excel('F:/JusikData/short_invest/test/mini_hangseng_lh1m.xlsx', engine='openpyxl')
            
            ##-----------------------------------------------------------------------------------------------------------##
            # 1분마다 데이터 가져오기
            inte_df_1m = dataset_1m.append(dataset_now.iloc[i], sort=False) # 전체 데이터에 하나의 데이터 추가
            inte_df_1m = inte_df_1m.reset_index(drop=True) # 인덱스 초기화
            inte_df_1m.to_excel('F:/JusikData/short_invest/test/mini_hangseng1r.xlsx', index=False) # 엑셀로 저장
            
            ##-----------------------------------------------------------------------------------------------------------##
            # 첫터치, 둘터치 데이터 가져와서, 둘터치 시 신호 발생
            결과, 포지션, 손절가 = send_sign_cls.exe_send_sign(self, inte_df_1m, inte_lowhigh_1m, result_data)
            print('결과 : ' + 결과, '포지션 : ' + 포지션, '손절가 : ' + 손절가)
            
            ##-----------------------------------------------------------------------------------------------------------##
            # 1분 최대-최저선 데이터 다시 로드
            inte_lowhigh_1m = pd.read_excel('F:/JusikData/short_invest/test/mini_hangseng_lh1m.xlsx', engine='openpyxl')
            
            # 최저선, 최대선 데이터 가져오기
            minmaxLine_repeat_cls.exe_minmaxLine_repeat(self, inte_lowhigh_1m, inte_df_1m, 10) # 10 = 시작시점 이후 데이터 전후수

## 실행 ##
conn = all_cls()
conn.exe_all()
