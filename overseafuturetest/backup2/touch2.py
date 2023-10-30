class touch_cls:
    def exe_touch(self, data, close1, open1, high1, low1, todaydatetime):
        dataset = data.copy()
        
        # 첫 터치 구하기
        for i in dataset.index:
            if dataset.iloc[i]['첫터치'] == "없음" :
                # 최대선
                if dataset.iloc[i]['구분'] == '전일최대' or dataset.iloc[i]['구분'] == '당일최대' or dataset.iloc[i]['구분'] == '최대선' :
                    # 최대선 양봉 (1) = 종가 (2) = 고가 / 위꼬리가 20틱 이하
                    if dataset.iloc[i]['시가'] < dataset.iloc[i]['종가'] and dataset.iloc[i]['고가'] - dataset.iloc[i]['종가'] <= 20 :
                        if open1 < close1 : # 첫터치 양봉
                            if low1 < dataset.iloc[i]['종가'] and high1 >= dataset.iloc[i]['종가'] :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "저항"
                                dataset.loc[i, '첫가격'] = open1
                            elif dataset.iloc[i]['종가'] <= low1 <= dataset.iloc[i]['고가'] :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "저항"
                                dataset.loc[i, '첫가격'] = open1
                    # 최대선 음봉 (1) = 시가 (2) = 고가 / 위꼬리가 20틱 이하
                    elif dataset.iloc[i]['시가'] > dataset.iloc[i]['종가'] and dataset.iloc[i]['고가'] - dataset.iloc[i]['시가'] <= 20 :
                        if open1 < close1 : # 첫터치 양봉
                            if low1 < dataset.iloc[i]['시가'] and high1 >= dataset.iloc[i]['시가'] :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "저항"
                                dataset.loc[i, '첫가격'] = open1
                            elif dataset.iloc[i]['시가'] <= low1 <= dataset.iloc[i]['고가'] :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "저항"
                                dataset.loc[i, '첫가격'] = open1
                # 최저선    
                elif dataset.iloc[i]['구분'] == '전일최소' or dataset.iloc[i]['구분'] == '당일최소' or dataset.iloc[i]['구분'] == '최저선':
                    # 최저선 양봉 (1) = 저가 (2) = 시가
                    if dataset.iloc[i]['시가'] < dataset.iloc[i]['종가'] and dataset.iloc[i]['시가'] - dataset.iloc[i]['저가'] <= 20 : 
                        if close1 < open1 : # 첫터치 음봉
                            if dataset.iloc[i]['시가'] < low1 and dataset.iloc[i]['시가'] >= high1 :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "지지"
                                dataset.loc[i, '첫가격'] = open1
                            elif dataset.iloc[i]['저가'] <= low1 <= dataset.iloc[i]['시가'] :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "지지"
                                dataset.loc[i, '첫가격'] = open1
                                
                    # 최저선 음봉 (1) = 저가 (2) = 종가
                    elif dataset.iloc[i]['시가'] > dataset.iloc[i]['종가'] and dataset.iloc[i]['종가'] - dataset.iloc[i]['저가'] <= 20: 
                        if close1 < open1 : # 첫터치 음봉
                            if dataset.iloc[i]['종가'] < low1 and dataset.iloc[i]['종가'] >= high1 :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "지지"
                                dataset.loc[i, '첫가격'] = open1
                            elif dataset.iloc[i]['저가'] <= low1 <= dataset.iloc[i]['종가'] :
                                dataset.loc[i, '첫터치'] = todaydatetime
                                dataset.loc[i, '지지저항'] = "지지"
                                dataset.loc[i, '첫가격'] = open1
                 
        # 둘 터치 구하기
        for i in dataset.index:
            if dataset.iloc[i]['첫터치'] != "없음" and  dataset.iloc[i]['둘터치'] == "없음" :
                # 매수진입 : 지지를 받는 첫터치 봉의 시가보다 둘터치의 종가가 크다면 + 양봉 
                if dataset.iloc[i]['지지저항'] == "지지" and dataset.iloc[i]['첫가격'] <= close1 and close1 > open1 :
                    dataset.loc[i, '둘터치'] = todaydatetime
                    dataset.loc[i, '포지션'] = "매수"
                    dataset.loc[i, '둘가격'] = close1
                # 매도진입 : 저항을 받는 첫터치 봉의 시가보다 줄터치의 종가가 작다면 + 음봉
                elif dataset.iloc[i]['지지저항'] == "저항" and dataset.iloc[i]['첫가격'] >= close1 and close1 < open1 :
                    dataset.loc[i, '둘터치'] = todaydatetime
                    dataset.loc[i, '포지션'] = "매도"
                    dataset.loc[i, '둘가격'] = close1
                        
        # 데이터리턴
        return dataset
