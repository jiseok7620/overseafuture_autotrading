from OverseasFutures.mini_hangseng.minLine import minLine_cls
from OverseasFutures.mini_hangseng.maxLine import maxLine_cls

class minmaxLine_repeat_cls:
    def exe_minmaxLine_repeat(self, inte_lowhigh_1m, inte_df_1m, s_long):
        # 1분 마다 최저선, 최대선 데이터 가져오기
        dd_1m = inte_lowhigh_1m.iloc[-1]['일시'] # 1분 최저,최대선 데이터의 마지막 일시
        data1 = minLine_cls.exe_minLine(self, dd_1m, inte_lowhigh_1m, inte_df_1m, s_long, "최저선")
        data2 = maxLine_cls.exe_maxLine(self, dd_1m, inte_lowhigh_1m, inte_df_1m, s_long, "최대선")
        
        '''
        if data1.empty :
            pass
        else : 
            inte_lowhigh_1m = inte_lowhigh_1m.append(data1, sort=False) # 새로운 최저선은 추가
            inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
            # 엑셀로 저장
            inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
            
        if data2.empty :
            pass
        else :
            inte_lowhigh_1m = inte_lowhigh_1m.append(data2, sort=False) # 새로운 최대선은 추가
            inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
            # 엑셀로 저장
            inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
        '''

        if data1.empty :
            pass
        else : 
            lowhigh_min = inte_lowhigh_1m[inte_lowhigh_1m['구분'] == '최저선']['저가'].min()
            print(lowhigh_min)
            if data1.iloc[0]['저가'] < lowhigh_min :
                # 새로운 최저선의 저가보다 저가가 큰 것들은 없애기
                inte_idx = inte_lowhigh_1m[(inte_lowhigh_1m['저가'] > lowhigh_min) & (inte_lowhigh_1m['구분'] == '최저선')].index  
                #inte_lowhigh_1m = inte_lowhigh_1m.drop(inte_idx, axis=0) # 해당 인덱스를 제거함
                try:
                    print('minmaxLine_repeat 39line : ' + inte_lowhigh_1m)
                    # 해당 인덱스의 터치는 끝으로 바꾸기
                    inte_lowhigh_1m.loc[inte_idx, '첫터치'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx, '지지저항'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx, '첫가격'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx, '둘터치'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx, '포지션'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx, '둘가격'] = '끝'
                    inte_lowhigh_1m = inte_lowhigh_1m.append(data1, sort=False) # 새로운 최저선은 추가
                    inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
                    print('minmaxLine_repeat 49line : ' + inte_lowhigh_1m)
                except:
                    print('minmaxLine 최소값 없애기 오류발생')
                    inte_lowhigh_1m = inte_lowhigh_1m.append(data1, sort=False) # 새로운 최저선은 추가
                    inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
                    # 엑셀로 저장
                    inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
            else :
                inte_lowhigh_1m = inte_lowhigh_1m.append(data1, sort=False) # 최저선 추가
                inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
                # 엑셀로 저장
                inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
            
        if data2.empty :
            pass
        else :
            lowhigh_max = inte_lowhigh_1m[inte_lowhigh_1m['구분'] == '최대선']['고가'].max()
            print(lowhigh_max)
            if data2.iloc[0]['고가'] > lowhigh_max :
                # 새로운 최대선의 고가보다 고가가 작은 것들은 없애기
                inte_idx2 = inte_lowhigh_1m[(inte_lowhigh_1m['고가'] < lowhigh_max) & (inte_lowhigh_1m['구분'] == '최대선')].index  
                #inte_lowhigh_1m = inte_lowhigh_1m.drop(inte_idx2, axis=0) # 해당 인덱스를 제거함
                try:
                    print('minmaxLine_repeat 72line : ' + inte_lowhigh_1m)
                    # 해당 인덱스의 터치는 끝으로 바꾸기
                    inte_lowhigh_1m.loc[inte_idx2, '첫터치'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx2, '지지저항'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx2, '첫가격'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx2, '둘터치'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx2, '포지션'] = '끝'
                    inte_lowhigh_1m.loc[inte_idx2, '둘가격'] = '끝'
                    inte_lowhigh_1m = inte_lowhigh_1m.append(data2, sort=False) # 새로운 최저선은 추가
                    inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
                    print('minmaxLine_repeat 82line : ' + inte_lowhigh_1m)
                except:
                    print('minmaxLine 최대값 없애기 오류발생')
                    inte_lowhigh_1m = inte_lowhigh_1m.append(data2, sort=False) # 새로운 최저선은 추가
                    inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
                    # 엑셀로 저장
                    inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
            else :
                inte_lowhigh_1m = inte_lowhigh_1m.append(data2, sort=False)
                inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
                # 엑셀로 저장
                inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
