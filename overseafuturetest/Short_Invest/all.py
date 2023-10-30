import pandas as pd
import time
import datetime
import os
import schedule
from OverseasFutures.Short_Invest.ebest_server_login import login_cls
from OverseasFutures.Short_Invest.o3103_pre import o3103_cls
from OverseasFutures.Short_Invest.o3103_pre_1minute import o3103_1m_cls
from OverseasFutures.Short_Invest.o3103_pre_5minute import o3103_5m_cls
from OverseasFutures.Short_Invest.secret_technique import trendline_cls

class all_cls:
    def exe_all(self):
        # 로그인
        login_cls.exe_login(self)
        
        # 어떤 종목 // 몇분데이터 가져올 것인지
        shcode = "HMHH22"
        minit = "5"
        
        if os.path.isfile('F:/JusikData/short_invest/mini_hangseng'+minit+'.xlsx') :
            dataset = pd.read_excel('F:/JusikData/short_invest/mini_hangseng'+minit+'.xlsx', engine='openpyxl')
        else :
            dataset = o3103_cls.exe_o3103(self, shcode, minit)
            dataset.to_excel('F:/JusikData/short_invest/mini_hangseng'+minit+'.xlsx', index=False)
            
        '''
        # count를 달아서 0일 때는 무조건 한번씩 실행하도록 하자
        while True:
            # 1단계 : mini-항생 선물의 데이터를 모두가져오기
            if os.path.isfile('F:/JusikData/short_invest/mini_hangseng'+minit+'.xlsx') :
                dataset = pd.read_excel('F:/JusikData/short_invest/mini_hangseng'+minit+'.xlsx', engine='openpyxl')
            else :
                dataset = o3103_cls.exe_o3103(self, minit)
                dataset.to_excel('F:/JusikData/short_invest/mini_hangseng'+minit+'.xlsx', index=False)
            
            # 2단계 : 5분마다 항생 5분 데이터 가져오고, 최저선 데이터 가져오기
            time.sleep(1)
            data = o3103_5m_cls.exe_o3103_5m(self)
            dataset = dataset.append(data, sort=False) # 데이터 합치기
            dataset = dataset.astype({'일시':'float'}) # 정렬을 위해 float으로 바꾸기
            dataset = dataset.sort_values('일시', ascending=True) # 오름차순 정렬하기
            dataset = dataset.astype({'일시':'str'}) # 다시 형식을 str로 바꾸기
            dataset = dataset.drop_duplicates(['일시']) # 중복 제거하기
            dataset = dataset.reset_index(drop=True) # 인덱스 초기화 하기
            dataset.to_excel('F:/JusikData/short_invest/mini_hangseng.xlsx', index=False) # 엑셀로 저장
            print(dataset)
            
            # 3단계 : 최저선 데이터를 추출
            low_data = trendline_cls.exe_trendline(self, dataset, 10)
            low_data.to_excel('F:/JusikData/short_invest/mini_hangseng_low.xlsx', index=False)
            print(low_data)
            
            # 4단계 : 현재봉이 투자 시점인지 판단
            # 현재봉의 종가가 1차 터치 후 2차 터치하는 선보다 크다면
            
            
            # 5분 뒤에 실행
            time.sleep(300)
        '''
        
## 실행 ##
conn = all_cls()
conn.exe_all()
'''
# 지정 시간에 실행하기
while True:
    now = datetime.datetime.now()
    nowTime = now.strftime('%H%M')
    if nowTime == '1209':
        conn = all_cls()
        conn.exe_all()
        break
    time.sleep(1)
'''