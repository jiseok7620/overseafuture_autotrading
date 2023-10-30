class touch_cls:
    def exe_touch(self, data, close1, open1, fast1, close_ago, todaydatetime):
        dataset = data.copy()
        
        # 최저선, 최대선 모두 지지와 저항이 가능하다고 보기        
        # 첫 터치 구하기
        for i in dataset.index:
            if dataset.iloc[i]['첫터치'] == "없음" and dataset.iloc[i]['구분'] != '전일최소' and dataset.iloc[i]['구분'] != '전일최대' :
                if dataset.iloc[i]['구분'] == '최저선':        
                    # 지지 : 전일 종가 >= 최저선 >= 현재종가 / 첫터치 봉은 음봉
                    if close_ago >= dataset.iloc[i]['저가'] >= close1 and close1 < open1 and fast1 < 21:
                        dataset.loc[i, '첫터치'] = todaydatetime
                        dataset.loc[i, '지지저항'] = "지지"
                        dataset.loc[i, '첫가격'] = open1
                elif dataset.iloc[i]['구분'] == '최대선' :
                    # 저항 : 전일 종가 <= 최대선 <= 현재종가 / 첫터치 봉은 양봉    
                    if close_ago <= dataset.iloc[i]['고가'] <= close1 and close1 > open1 and fast1 > 79:
                        dataset.loc[i, '첫터치'] = todaydatetime
                        dataset.loc[i, '지지저항'] = "저항"
                        dataset.loc[i, '첫가격'] = open1
        
        # 둘 터치 구하기
        for i in dataset.index:
            if dataset.iloc[i]['첫터치'] != "없음" and dataset.iloc[i]['둘터치'] == "없음" and dataset.iloc[i]['둘터치'] != "끝" :
                # 지지
                if dataset.iloc[i]['지지저항'] == "지지" and fast1 >= 31 :
                    dataset.loc[i, '둘터치'] = todaydatetime
                    dataset.loc[i, '포지션'] = "매수"
                    dataset.loc[i, '둘가격'] = close1
                # 저항  
                elif dataset.iloc[i]['지지저항'] == "저항" and fast1 <= 69 :
                    dataset.loc[i, '둘터치'] = todaydatetime
                    dataset.loc[i, '포지션'] = "매도"
                    dataset.loc[i, '둘가격'] = close1
                    
        # 데이터리턴
        return dataset