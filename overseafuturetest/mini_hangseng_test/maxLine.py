import pandas as pd

class maxLine_cls:
    def exe_maxLine(self, st_dd, inte_lowhigh, dataset, long, minute):
        ##--------------------------------------------------------------------------------------------------##
        ## 고점 구하기 ##
        highpoint_bf = [] # 저점보다 큰값들의 수 리스트(당일 이전)
        highpoint_af = [] # 저점보다 큰값들의 수 리스트(당일 이후)
        highpoint_count_bf = 0 # 저점보다 큰값들의 수(당일 이전)
        highpoint_count_af = 0 # 저점보다 큰값들의 수(당일 이후).
        highpoint_ind = []
        
        # for문 돌리기
        if len(inte_lowhigh) == 2 :
            st_num = 0
        else :
            st_num = dataset[dataset['일시']==st_dd].index[0]# 최저최대선 데이터 중 마지막을 시작점으로
            
        for i in dataset.index:
            # 고점 구하기
            if i > st_num:
                for l in range(i) : 
                    if i == 0:
                        break
                    if dataset.iloc[i]['고가'] <= dataset.iloc[i-l-1]['고가']:
                        break
                    elif dataset.iloc[i]['고가'] > dataset.iloc[i-l-1]['고가']:
                        highpoint_count_bf += 1
                    
                for m in range(i,len(dataset)):
                    if i == len(dataset)-1:
                        break
                    if i == m :
                        continue
                    if dataset.iloc[i]['고가'] <= dataset.iloc[m]['고가']:
                        break
                    elif dataset.iloc[i]['고가'] > dataset.iloc[m]['고가']:
                        highpoint_count_af += 1
                
                # 저점 배열 추가            
                highpoint_bf.append(highpoint_count_bf)
                highpoint_af.append(highpoint_count_af)
                highpoint_ind.append(i)
                highpoint_count_bf = 0
                highpoint_count_af = 0
            
        # 결과
        highpoint_data = pd.DataFrame({'전수' : highpoint_bf, '후수' : highpoint_af, '인덱스' : highpoint_ind})
        
        # 전작은값수나 후작은값수가 10미만 인 것들은 필터
        highpoint_data_long = highpoint_data[highpoint_data['전수'] >= long]
        highpoint_data_long = highpoint_data_long[highpoint_data_long['후수'] >= long]
        
        ##--------------------------------------------------------------------------------------------------##        
        # 저점의 일시, 인덱스, 가격 가져오기
        highpoint_date_long = []
        highpoint_index_long = []
        highpoint_open = []
        highpoint_high = []
        highpoint_low = []
        highpoint_close = []
        highpoint_volume_long = []
        highpoint_minute = []
        highpoint_touch1 = []
        highpoint_touch1_price = []
        highpoint_jiji = []
        highpoint_touch2 = []
        highpoint_touch2_price = []
        highpoint_position = []
        highpoint_standard = []
        highpoint_before = []
        highpoint_after = []
        
        for i in range(len(highpoint_data_long)) :
            # 인덱스 가져오기
            highidx = highpoint_data_long.iloc[i]['인덱스']
            
            # 일시
            highdate = dataset.loc[highidx]['일시']
            
            # 시가
            highopen = dataset.loc[highidx]['시가']
            # 고가
            highhigh = dataset.loc[highidx]['고가']
            # 저가
            highlow = dataset.loc[highidx]['저가']
            # 종가
            highclose = dataset.loc[highidx]['종가'] 
                
            # 거래량
            highvolume = dataset.loc[highidx]['거래량']
            
            # 기준가
            standardprice = (highhigh + highlow + highclose) / 3
            
            # 전수
            cnt_bf = highpoint_data_long.iloc[i]['전수']
            
            # 후수
            cnt_af = highpoint_data_long.iloc[i]['후수']
            
            # 리스트에 값 넣기
            highpoint_date_long.append(highdate)
            highpoint_index_long.append(highidx)
            highpoint_open.append(highopen)
            highpoint_high.append(highhigh)
            highpoint_low.append(highlow)
            highpoint_close.append(highclose)
            highpoint_volume_long.append(highvolume)
            highpoint_minute.append(minute)
            highpoint_touch1.append("없음")
            highpoint_jiji.append("없음")
            highpoint_touch2.append("없음")
            highpoint_position.append("없음")
            highpoint_touch1_price.append("없음")
            highpoint_touch2_price.append("없음")
            highpoint_standard.append(standardprice)
            highpoint_before.append(cnt_bf)
            highpoint_after.append(cnt_af)
            
        # 결과 데이터프레임 만들기
        highpoint_grape_data_long = pd.DataFrame({
                                                '일시' : highpoint_date_long, 
                                                '시가' : highpoint_open, '고가' : highpoint_high, '저가' : highpoint_low, '종가' : highpoint_close,
                                                '거래량' : highpoint_volume_long, '구분' : highpoint_minute, '기준가' : highpoint_standard,
                                                '전수' : highpoint_before, '후수' : highpoint_after,
                                                '첫터치' : highpoint_touch1, '지지저항' : highpoint_jiji, '첫가격' : highpoint_touch1_price,
                                                '둘터치' : highpoint_touch2, '포지션' : highpoint_position, '둘가격' : highpoint_touch2_price
                                                 })
        
        # 내림차순 정리
        highpoint_grape_data_long = highpoint_grape_data_long.sort_values('일시', ascending=True)
        
        # 결과 리턴
        return highpoint_grape_data_long