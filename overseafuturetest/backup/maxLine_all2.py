import pandas as pd

class maxLine_all_cls:
    def exe_maxLine_all(self, dataset, long, minute):
        ##--------------------------------------------------------------------------------------------------##
        ## 고점 구하기 ##
        highpoint_bf = [] # 저점보다 큰값들의 수 리스트(당일 이전)
        highpoint_af = [] # 저점보다 큰값들의 수 리스트(당일 이후)
        highpoint_count_bf = 0 # 저점보다 큰값들의 수(당일 이전)
        highpoint_count_af = 0 # 저점보다 큰값들의 수(당일 이후)
        
        # for문 돌리기
        for i in dataset.index:
            # 고점 구하기
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
            
            # 고점 배열 추가            
            highpoint_bf.append(highpoint_count_bf)
            highpoint_af.append(highpoint_count_af)
            highpoint_count_bf = 0
            highpoint_count_af = 0
            
        # 결과
        highpoint_data = pd.DataFrame({'전수' : highpoint_bf, '후수' : highpoint_af})
        
        # 전작은값수나 후작은값수가 10미만 인 것들은 필터
        highpoint_data_long = highpoint_data[highpoint_data['전수'] >= long]
        highpoint_data_long = highpoint_data_long[highpoint_data_long['후수'] >= long]
        
        ##--------------------------------------------------------------------------------------------------##        
        # 고점의 일시, 인덱스, 가격 가져오기
        highpoint_date_long = []
        highpoint_index_long = []
        highpoint_price_long = []
        highpoint_volume_long = []
        highpoint_minute = []
        highpoint_trends = []
        
        for i in range(len(highpoint_data_long)) :
            # 인덱스 가져오기
            highidx = highpoint_data_long.index[i]
            
            # 일시
            highdate = dataset.loc[highidx]['일시']
            
            # 저가
            highprice = dataset.loc[highidx]['고가']
                
            # 거래량
            highvolume = dataset.loc[highidx]['거래량']
            
            # 추세가져오기
            bfnum = highpoint_data_long.iloc[i]['전수']
            afnum = highpoint_data_long.iloc[i]['후수']
            bfmin = dataset[highidx-bfnum:highidx]['저가'].min() # 해당 일부터 전수만큼 전까지 중 최소값
            afmin = dataset[highidx+1:highidx+afnum+1]['고가'].min() # 해당 일부터 후수만큼 후까지 중 최소값
            if bfmin > afmin :
                highpoint_result = "하락세"
            else:
                highpoint_result = "상승세"
            
            # 리스트에 값 넣기
            highpoint_date_long.append(highdate)
            highpoint_index_long.append(highidx)
            highpoint_price_long.append(highprice)
            highpoint_volume_long.append(highvolume)
            highpoint_minute.append(minute)
            highpoint_trends.append(highpoint_result)
            
        # 결과 데이터프레임 만들기
        highpoint_grape_data_long = pd.DataFrame({
                                                '일시' : highpoint_date_long, '가격' : highpoint_price_long, 
                                                '거래량' : highpoint_volume_long, '추세': highpoint_trends, '구분' : highpoint_minute
                                                 })
        
        # 내림차순 정리
        highpoint_grape_data_long = highpoint_grape_data_long.sort_values('일시', ascending=True)
        
        # 결과 리턴
        return highpoint_grape_data_long