'''
Pro3. 최저선 구하기
'''

import pandas as pd

class trendline_cls:
    def exe_trendline(self, dataset, long):
        ##--------------------------------------------------------------------------------------------------##
        ## 저점 구하기 ##
        lowpoint_bf = [] # 저점보다 큰값들의 수 리스트(당일 이전)
        lowpoint_af = [] # 저점보다 큰값들의 수 리스트(당일 이후)
        lowpoint_count_bf = 0 # 저점보다 큰값들의 수(당일 이전)
        lowpoint_count_af = 0 # 저점보다 큰값들의 수(당일 이후)
        
        # for문 돌리기
        for i in dataset.index:
            # 저점 구하기
            for l in range(i) : 
                if i == 0:
                    break
                if dataset.iloc[i]['저가'] >= dataset.iloc[i-l-1]['저가']:
                    break
                elif dataset.iloc[i]['저가'] < dataset.iloc[i-l-1]['저가']:
                    lowpoint_count_bf += 1
                
            for m in range(i,len(dataset)):
                if i == len(dataset)-1:
                    break
                if i == m :
                    continue
                if dataset.iloc[i]['저가'] >= dataset.iloc[m]['저가']:
                    break
                elif dataset.iloc[i]['저가'] < dataset.iloc[m]['저가']:
                    lowpoint_count_af += 1
            
            # 저점 배열 추가            
            lowpoint_bf.append(lowpoint_count_bf)
            lowpoint_af.append(lowpoint_count_af)
            lowpoint_count_bf = 0
            lowpoint_count_af = 0
            
        # 결과
        lowpoint_data = pd.DataFrame({'전수' : lowpoint_bf, '후수' : lowpoint_af})
        
        # 전작은값수나 후작은값수가 10미만 인 것들은 필터
        lowpoint_data_long = lowpoint_data[lowpoint_data['전수'] >= long]
        lowpoint_data_long = lowpoint_data_long[lowpoint_data_long['후수'] >= long]
        
        ##--------------------------------------------------------------------------------------------------##        
        # 저점의 일시, 인덱스, 가격 가져오기
        lowpoint_date_long = []
        lowpoint_index_long = []
        lowpoint_price_long = []
        lowpoint_volume_long = []
        
        for i in range(len(lowpoint_data_long)) :
            # 인덱스 가져오기
            lowidx = lowpoint_data_long.index[i]
            
            # 해당 인덱스의 일자 가져오기
            lowdate = dataset.loc[lowidx]['일시']
            
            # 해당 인덱스의 가격 가져오기
            # 양봉 일때는 시가, 음봉 일때는 종가 기준
            if int(dataset.loc[lowidx]['시가']) - int(dataset.loc[lowidx]['종가']) <= 0 :
                lowprice = dataset.loc[lowidx]['시가']
            else :
                lowprice = dataset.loc[lowidx]['종가']
                
            # 해당 인덱스의 거래량 가져오기
            lowvolume = dataset.loc[lowidx]['거래량']
            
            # 리스트에 값 넣기
            lowpoint_date_long.append(lowdate)
            lowpoint_index_long.append(lowidx)
            lowpoint_price_long.append(lowprice)
            lowpoint_volume_long.append(lowvolume)
            
        # 결과 데이터프레임 만들기
        lowpoint_grape_data_long = pd.DataFrame({
                                                '일시' : lowpoint_date_long, '인덱스' : lowpoint_index_long, '가격' : lowpoint_price_long, 
                                                '거래량' : lowpoint_volume_long
                                                 })
        
        # 내림차순 정리
        lowpoint_grape_data_long = lowpoint_grape_data_long.sort_values('일시', ascending=True)
        
        ##--------------------------------------------------------------------------------------------------##     
        # 첫번째 터치 구하기
        lowpoint_grape_data_long = lowpoint_grape_data_long.reset_index(drop=True)
        
        touch1_data_dd = []
        touch1_index = []
        touch_date = []
        touch_ind = []
        
        for i in lowpoint_grape_data_long.index: 
            for j in dataset.index:
                if j > lowpoint_grape_data_long.iloc[i]['인덱스'] + long :
                    if dataset.iloc[j]['종가'] <= lowpoint_grape_data_long.iloc[i]['가격']:
                        touch_date.append(dataset.iloc[j]['일시'])
                        touch_ind.append(j)
            
            if len(touch_date) == 0:
                touch1_data_dd.append('최저')
                touch1_index.append('최저')
            else: 
                touch1_data_dd.append(touch_date[0])
                touch1_index.append(touch_ind[0])
            
            touch_date = []
            touch_ind = []
            
        lowpoint_grape_data_long['첫터치'] = touch1_data_dd
        lowpoint_grape_data_long['첫인덱스'] = touch1_index
        
        ##--------------------------------------------------------------------------------------------------##     
        # 두번째 터치 구하기
        touch2_data_dd = []
        touch2_index = []
        touch_date2 = []
        touch_ind2 = []
        
        for i in lowpoint_grape_data_long.index: 
            for j in dataset.index:
                if lowpoint_grape_data_long.iloc[i]['첫인덱스'] == '최저' :
                    touch_date2.append('최저')
                    touch_ind2.append('최저')
                else :
                    if j > lowpoint_grape_data_long.iloc[i]['첫인덱스'] :
                        if dataset.iloc[j]['종가'] >= lowpoint_grape_data_long.iloc[i]['가격']:
                            touch_date2.append(dataset.iloc[j]['일시'])
                            touch_ind2.append(j)
            
            if len(touch_date2) == 0:
                touch2_data_dd.append('최저')
                touch2_index.append('최저')
            else: 
                touch2_data_dd.append(touch_date2[0])
                touch2_index.append(touch_ind2[0])
                
            touch_date2 = []
            touch_ind2 = []
            
        lowpoint_grape_data_long['둘터치'] = touch2_data_dd
        lowpoint_grape_data_long['둘인덱스'] = touch2_index
        
        return lowpoint_grape_data_long
        
'''
conn = trendline_cls()
conn.exe_trendline()
'''
