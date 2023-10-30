import os
import numpy as np
import pandas as pd
from OverseasFutures.mini_hangseng.minuteData import o3103_cls
from OverseasFutures.mini_hangseng.minLine_all import minLine_all_cls
from OverseasFutures.mini_hangseng.maxLine_all import maxLine_all_cls

class bring_data_cls:
    def make_rsi(self, data1, period):
        # RSI 구하기
        U = np.where(data1['종가'].diff(1) > 0, data1['종가'].diff(1), 0)
        D = np.where(data1['종가'].diff(1) < 0, data1['종가'].diff(1)*(-1), 0)
        
        # 이동평균을 이용한 RSI 계산
        AU = pd.DataFrame(U).rolling(window=period).mean()
        AD = pd.DataFrame(D).rolling(window=period).mean()
        RSI = AU.div(AD+AU) *100
        
        # 지수이동평균을 이용한 RSI 계산
        #AU_jisu = pd.DataFrame(U).ewm(span=period, adjust=False).mean()
        #AD_jisu = pd.DataFrame(D).ewm(span=period, adjust=False).mean()
        #RSI_jisu = AU_jisu.div(AD_jisu+AU_jisu) *100
        
        return round(RSI,0)
    
    def exe_bring_data(self, code, rpt_num, long):
        # 변수 통합 관리
        repeat_num = rpt_num # 1,5분 데이터 몇번 반복 가져올지 - 25 = 25 * 100 = 2500개 데이터
        f_long = long # 처음 repeat_num 만큼 가져온 데이터에서 전,후 봉수 조건 설정
        
        # 1분, 5분 데이터 가져와서 저장하기
        # 1, 5분 데이터
        if os.path.isfile('F:/JusikData/short_invest/mini_hangseng1.xlsx') :
            pass
        else :
            dataset_1m = o3103_cls.exe_o3103(self, code, "1", "100", repeat_num) # 종목코드, 몇분데이터, 몇개, 몇번반복
            dataset_1m = dataset_1m.reset_index(drop=True) # 인덱스 초기화 
            dataset_1m['20이평'] = dataset_1m['종가'].rolling(window=20).mean() # 20일 이동평균만들기
            
            # 마지막 행 삭제 = 마지막 행은 현재시간으로 진행되고 있기 때문에
            dataset_1m = dataset_1m.drop(len(dataset_1m)-1)
            
            # RSI 추가하기(14일)
            U = np.where(dataset_1m['종가'].diff(1) > 0, dataset_1m['종가'].diff(1), 0)
            D = np.where(dataset_1m['종가'].diff(1) < 0, dataset_1m['종가'].diff(1)*(-1), 0)
            
            # 이동평균을 이용한 RSI 계산
            AU = pd.DataFrame(U).rolling(window=14).mean()
            AD = pd.DataFrame(D).rolling(window=14).mean()
            RSI = AU.div(AD+AU) *100
            
            # 지수이동평균을 이용한 RSI 계산
            #AU_jisu = pd.DataFrame(U).ewm(span=14, adjust=False).mean()
            #AD_jisu = pd.DataFrame(D).ewm(span=14, adjust=False).mean()
            #RSI_jisu = AU_jisu.div(AD_jisu+AU_jisu) *100
            
            dataset_1m['RSI'] = round(RSI,0)
            
            # 엑셀로 저장
            dataset_1m.to_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', index=False)
        
        # 1, 5분 최저, 최대선 데이터
        if os.path.isfile('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx') :
            pass
        else :
            low_1m_data = minLine_all_cls.exe_minLine_all(self, dataset_1m, f_long, "1분-최저")
            high_1m_data = maxLine_all_cls.exe_maxLine_all(self, dataset_1m, f_long, "1분-최대")
            # 데이터 합치기
            inte_lowhigh_1m = low_1m_data.append(high_1m_data, sort=False)
            # 오름차순 정렬
            inte_lowhigh_1m = inte_lowhigh_1m.sort_values('일시', ascending=True)
            # 첫터치, 둘터치 열 추가
            inte_lowhigh_1m['첫터치'] = '없음'
            inte_lowhigh_1m['지지저항'] = '없음'
            inte_lowhigh_1m['첫가격'] = '없음'
            inte_lowhigh_1m['둘터치'] = '없음'
            inte_lowhigh_1m['포지션'] = '없음'
            inte_lowhigh_1m['둘가격'] = '없음'
            # 중복 제거
            inte_lowhigh_1m = inte_lowhigh_1m.drop_duplicates(['일시'])
            # 엑셀로 저장
            inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)      
