import pandas as pd

class minLine_cls:
    def exe_minLine(self, st_dd, dataset, long, minute):
        ##--------------------------------------------------------------------------------------------------##
        ## 저점 구하기 ##
        lowpoint_bf = [] # 저점보다 큰값들의 수 리스트(당일 이전)
        lowpoint_af = [] # 저점보다 큰값들의 수 리스트(당일 이후)
        lowpoint_count_bf = 0 # 저점보다 큰값들의 수(당일 이전)
        lowpoint_count_af = 0 # 저점보다 큰값들의 수(당일 이후)
        lowpoint_ind = []
        
        # for문 돌리기
        if st_dd == 0 :
            st_num = 0
        else:
            st_num = dataset[dataset['일시']==st_dd].index[0]# 최저선 데이터 중 마지막을 시작점으로
        for i in dataset.index:
            if i > st_num:
                # 저점 구하기 = 전수
                for l in range(i) : 
                    if i == 0:
                        break
                    if dataset.iloc[i]['저가'] >= dataset.iloc[i-l-1]['저가']:
                        break
                    elif dataset.iloc[i]['저가'] < dataset.iloc[i-l-1]['저가']:
                        lowpoint_count_bf += 1
                    if lowpoint_count_bf >= long :
                        break
                
                # 저점 구하기 = 후수
                for m in range(i,len(dataset)):
                    if i == len(dataset)-1:
                        break
                    if i == m :
                        continue
                    if dataset.iloc[i]['저가'] >= dataset.iloc[m]['저가']:
                        break
                    elif dataset.iloc[i]['저가'] < dataset.iloc[m]['저가']:
                        lowpoint_count_af += 1
                    if lowpoint_count_af >= long :
                        break
                
                # 저점 배열 추가            
                lowpoint_bf.append(lowpoint_count_bf)
                lowpoint_af.append(lowpoint_count_af)
                lowpoint_ind.append(i)
                lowpoint_count_bf = 0
                lowpoint_count_af = 0
            
        # 결과
        lowpoint_data = pd.DataFrame({'전수' : lowpoint_bf, '후수' : lowpoint_af, '인덱스' : lowpoint_ind})
        
        # 전작은값수나 후작은값수가 10미만 인 것들은 필터
        lowpoint_data_long = lowpoint_data[lowpoint_data['전수'] >= long]
        lowpoint_data_long = lowpoint_data_long[lowpoint_data_long['후수'] >= long]
        
        ##--------------------------------------------------------------------------------------------------##        
        # 저점의 일시, 인덱스, 가격 가져오기
        lowpoint_date_long = []
        lowpoint_index_long = []
        lowpoint_open = []
        lowpoint_high = []
        lowpoint_low = []
        lowpoint_close = []
        lowpoint_volume_long = []
        lowpoint_minute = []
        
        for i in range(len(lowpoint_data_long)) :
            # 인덱스 가져오기
            lowidx = lowpoint_data_long.iloc[i]['인덱스']
            
            # 일시
            lowdate = dataset.loc[lowidx]['일시']
            
            # 시가
            lowopen = dataset.loc[lowidx]['시가']
            # 고가
            lowhigh = dataset.loc[lowidx]['고가']
            # 저가
            lowlow = dataset.loc[lowidx]['저가']
            # 종가
            lowclose = dataset.loc[lowidx]['종가'] 
            
            # 거래량
            lowvolume = dataset.loc[lowidx]['거래량']
            
            # 리스트에 값 넣기
            lowpoint_date_long.append(lowdate)
            lowpoint_index_long.append(lowidx)
            lowpoint_open.append(lowopen)
            lowpoint_high.append(lowhigh)
            lowpoint_low.append(lowlow)
            lowpoint_close.append(lowclose)
            lowpoint_volume_long.append(lowvolume)
            lowpoint_minute.append(minute)
          
        # 결과 데이터프레임 만들기
        lowpoint_grape_data_long = pd.DataFrame({
                                                '일시' : lowpoint_date_long, 
                                                '시가' : lowpoint_open, '고가' : lowpoint_high, '저가' : lowpoint_low, '종가' : lowpoint_close,
                                                '거래량' : lowpoint_volume_long, '구분' : lowpoint_minute,
                                                 })
        
        # 오름차순 정리
        lowpoint_grape_data_long = lowpoint_grape_data_long.sort_values('일시', ascending=True)
        
        # 결과 리턴
        return lowpoint_grape_data_long