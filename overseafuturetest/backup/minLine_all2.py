import pandas as pd

class minLine_all_cls:
    def exe_minLine_all(self, dataset, long, minute):
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
        lowpoint_minute = []
        lowpoint_trends = []
        
        
        for i in range(len(lowpoint_data_long)) :
            # 인덱스 가져오기
            lowidx = lowpoint_data_long.index[i]
            
            # 일시
            lowdate = dataset.loc[lowidx]['일시']
            
            # 저가
            lowprice = dataset.loc[lowidx]['저가']
                
            # 거래량
            lowvolume = dataset.loc[lowidx]['거래량']
            
            # 추세가져오기
            bfnum = lowpoint_data_long.iloc[i]['전수']
            afnum = lowpoint_data_long.iloc[i]['후수']
            bfmin = dataset[lowidx-bfnum:lowidx]['고가'].max() # 해당 일부터 전수만큼 전까지 중 최대값
            afmin = dataset[lowidx+1:lowidx+afnum+1]['고가'].max() # 해당 일부터 후수만큼 후까지 중 최대값
            if bfmin > afmin :
                lowpoint_result = "하락세"
            else:
                lowpoint_result = "상승세"
            
            # 리스트에 값 넣기
            lowpoint_date_long.append(lowdate)
            lowpoint_index_long.append(lowidx)
            lowpoint_price_long.append(lowprice)
            lowpoint_volume_long.append(lowvolume)
            lowpoint_minute.append(minute)
            lowpoint_trends.append(lowpoint_result)
            
        # 결과 데이터프레임 만들기
        lowpoint_grape_data_long = pd.DataFrame({
                                                '일시' : lowpoint_date_long, '가격' : lowpoint_price_long, 
                                                '거래량' : lowpoint_volume_long, '추세': lowpoint_trends, '구분' : lowpoint_minute
                                                 })
        
        # 오름차순 정리
        lowpoint_grape_data_long = lowpoint_grape_data_long.sort_values('일시', ascending=True)
        
        # 결과 리턴
        return lowpoint_grape_data_long