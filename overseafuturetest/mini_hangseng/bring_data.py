import os
import numpy as np
import pandas as pd
from OverseasFutures.mini_hangseng.minuteData import o3103_cls

class bring_data_cls:
    def make_rsi(self, data1, how_price, period):
        U = np.where(data1[how_price].diff(1) > 0, data1[how_price].diff(1), 0)
        D = np.where(data1[how_price].diff(1) < 0, data1[how_price].diff(1)*(-1), 0)
        
        AU = pd.DataFrame(U).ewm(alpha=1/period, min_periods=period).mean()
        AD = pd.DataFrame(D).ewm(alpha=1/period, min_periods=period).mean()
        RSI = AU.div(AD+AU) *100
        
        return round(RSI,0)
    
    # 스토캐스틱 중 Fast%K 구하기
    def make_stochastic(self, dataset, nn, price_high, price_low):
        # n일중 최고가
        ndays_high = dataset[price_high].rolling(window=nn, min_periods=1).max()
        
        # n일중 최저가
        ndays_low = dataset[price_low].rolling(window=nn, min_periods=1).min()
        
        # Fast %K 계산
        fast_k = ((dataset['종가'] - ndays_low) / (ndays_high - ndays_low)) * 100
        
        return fast_k
    
    def exe_bring_data(self, code, now_dd, start_dd, end_dd):
        # 어제, 당일 1분데이터 가져오기
        if os.path.isfile('F:/JusikData/short_invest/mini_hangseng1.xlsx') :
            dataset_1m = pd.read_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', engine='openpyxl')
        else :
            dataset_1m = o3103_cls.exe_o3103(self, code, "1", "100", 20) # 종목코드, 몇분데이터, 몇개, 몇번반복
            dataset_1m = dataset_1m.reset_index(drop=True) # 인덱스 초기화 
            
            # 당일 데이터만 추출
            dataset_now = dataset_1m[dataset_1m['일시'] >= now_dd]
            
            # fastk 넣기
            ndays_high = dataset_now['고가'].rolling(window=14, min_periods=1).max() # n일중 최고가
            ndays_low = dataset_now['저가'].rolling(window=14, min_periods=1).min() # n일중 최저가
            fast_k = ((dataset_now['종가'] - ndays_low) / (ndays_high - ndays_low)) * 100 # Fast %K 계산
            dataset_now['fastk'] = fast_k
            
            # 인덱스 초기화
            dataset_now = dataset_now.reset_index(drop=True) # 인덱스 초기화 
            
            # 마지막행 두번 삭제
            dataset_now = dataset_now.drop(len(dataset_now)-1) # 마지막 행은 현재시간으로 진행되고 있기 때문에
            dataset_now = dataset_now.drop(len(dataset_now)-1) 
            
            # 당일 데이터 엑셀로 저장
            dataset_now.to_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', index=False)
            
            #### 과거 최대선, 최저선 구하기 ####
            # 전일 데이터 자르기
            dataset_1m_ago = dataset_1m[dataset_1m['일시'] >= start_dd]
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
            inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
            
#conn = bring_data_cls()
#conn.exe_bring_data("HMHH22", 10)
