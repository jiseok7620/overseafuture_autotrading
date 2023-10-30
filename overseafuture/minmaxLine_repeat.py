from minLine import minLine_cls
from maxLine import maxLine_cls

class minmaxLine_repeat_cls:
    def exe_minmaxLine_repeat(self, inte_lowhigh_1m, inte_df_1m, s_long):
        if len(inte_lowhigh_1m) == 0:
            data1 = minLine_cls.exe_minLine(self, 0, inte_df_1m, s_long, "최저선")
            data2 = maxLine_cls.exe_maxLine(self, 0, inte_df_1m, s_long, "최대선")
        else :
            # 1분 마다 최저선, 최대선 데이터 가져오기
            dd_1m = inte_lowhigh_1m.iloc[-1]['일시'] # 1분 최저,최대선 데이터의 마지막 일시
            data1 = minLine_cls.exe_minLine(self, dd_1m, inte_df_1m, s_long, "최저선")
            data2 = maxLine_cls.exe_maxLine(self, dd_1m, inte_df_1m, s_long, "최대선")
        
        if data1.empty :
            pass
        else : 
            inte_lowhigh_1m = inte_lowhigh_1m.append(data1, sort=False) # 최저선 추가
            inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
            # 엑셀로 저장
            inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)
            
        if data2.empty :
            pass
        else :
            inte_lowhigh_1m = inte_lowhigh_1m.append(data2, sort=False)
            inte_lowhigh_1m = inte_lowhigh_1m.reset_index(drop=True) # 인덱스 초기화
            # 엑셀로 저장
            inte_lowhigh_1m.to_excel('F:/JusikData/short_invest/mini_hangseng_lh1m.xlsx', index=False)