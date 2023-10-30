import pandas as pd
import time
import datetime
import os
import schedule
from OverseasFutures.Short_Invest.ebest_server_login import login_cls
from OverseasFutures.Short_Invest.o3103_pre import o3103_cls
from OverseasFutures.Short_Invest.o3103_pre_1minute import o3103_1m_cls
from OverseasFutures.Short_Invest.o3103_pre_5minute import o3103_5m_cls
from OverseasFutures.Short_Invest.secret_technique import trendline_cls

class all_cls:
    def exe_all(self):
        # 로그인
        login_cls.exe_login(self)
        
        # 저장된 선물 데이터를 가져오기
        dataset = pd.read_excel('F:/JusikData/short_invest/mini_hangseng1.xlsx', engine='openpyxl')
        dataset = dataset.astype({'일시':'str'}) # 다시 형식을 str로 바꾸기
        
        # 인덱스를 카운트하기위한 변수
        count_ind = 0
        
        # 데이터프레임을 담기위한 변수
        inte_df = pd.DataFrame()
        
        # 자신보다 이전에 저가의 수를 구하기위한 변수
        high_count_bf = 0
        high_count_af = 0
        
        # 전, 후의 봉이 n개 이상인 값들 담을 배열
        high_bf_arr = []
        high_af_arr = []
        
        # 최저선 데이터 모으는 데이터 프레임
        #low_df = pd.DataFrame(columns=('일시','시가','고가','저가','종가','거래량','위꼬리','몸통','아래꼬리','틱수','최저수'))
        high_df = pd.DataFrame(columns=('일시','시가','고가','저가','종가','거래량','최저수'))
                
        # final
        len_fi = 0
        
        ######################################################################################################################### 
        # 반복문의 시작
        while True:
            ### 1단계 : 선물데이터에서 데이터 하나씩 가져오기 ###
            data = dataset.iloc[count_ind]
            
            ### 2단계 : 하나씩 저장하면서 데이터프레임 만들기 ###
            inte_df = inte_df.append(data, sort=False) # 데이터 합치기
            
            ### 3단계 : 데이터프레임에서 최고선 데이터 만들기 ###
            # 고점 구하기
            for i in range(count_ind) : 
                if count_ind == 0:
                    break
                if inte_df.iloc[count_ind]['고가'] >= inte_df.iloc[count_ind-i-1]['고가']:
                    high_count_bf += 1
                elif inte_df.iloc[count_ind]['고가'] < inte_df.iloc[count_ind-i-1]['고가']:
                    break
                    
            #########################################################################################################################                    
            # 표시할 값들 넣기
            # 일시
            dd = inte_df.iloc[-1]['일시']
            
            # 거래량
            td = inte_df.iloc[-1]['거래량']
            
            # 위꼬리, 몸통, 아래꼬리, 봉의 틱수
            '''
            leng_bar = inte_df.iloc[-1]['고가'] - inte_df.iloc[-1]['저가']
            if inte_df.iloc[-1]['시가'] <= inte_df.iloc[-1]['종가'] : # 양봉일때
                up_tail = round(((inte_df.iloc[-1]['고가'] - inte_df.iloc[-1]['종가']) / leng_bar * 100), 0)
                down_tail = round(((inte_df.iloc[-1]['시가'] - inte_df.iloc[-1]['저가']) / leng_bar * 100), 0)
                body = round(((inte_df.iloc[-1]['종가'] - inte_df.iloc[-1]['시가']) / leng_bar * 100), 0)
            else :
                up_tail = round(((inte_df.iloc[-1]['고가'] - inte_df.iloc[-1]['시가']) / leng_bar * 100), 0)
                down_tail = round(((inte_df.iloc[-1]['종가'] - inte_df.iloc[-1]['저가']) / leng_bar * 100), 0)
                body = round(((inte_df.iloc[-1]['시가'] - inte_df.iloc[-1]['종가']) / leng_bar * 100), 0)
            '''
            
            # 시고저종 넣기
            open = inte_df.iloc[-1]['시가']
            high = inte_df.iloc[-1]['고가']
            low = inte_df.iloc[-1]['저가']
            close = inte_df.iloc[-1]['종가']
            
            ### 전 봉수가 n개 이상이면 배열에 담기 ###
            if high_count_bf >= 10 :
                high_bf_arr.append(dd)
                high_bf_arr.append(open)
                high_bf_arr.append(high)
                high_bf_arr.append(low)
                high_bf_arr.append(close)
                high_bf_arr.append(td)
                #low_bf_arr.append(up_tail)
                #low_bf_arr.append(body)
                #low_bf_arr.append(down_tail)
                #low_bf_arr.append(leng_bar)
                high_bf_arr.append(high_count_bf)
                
                ### 해당 배열을 데이터프레임에 담기 ###
                high_df = high_df.append(pd.Series(high_bf_arr, index=high_df.columns), ignore_index=True)
                
            #########################################################################################################################
            # 고점 구하기
            for m in high_df.index:
                high_ind = inte_df[inte_df['일시']==high_df.iloc[m]['일시']].index[0]
                
                for n in range(high_ind+1, len(inte_df)):
                    if n == len(inte_df)-1:
                        break
                    if inte_df.iloc[high_ind]['고가'] >= inte_df.iloc[n]['고가']:
                        high_count_af += 1
                    elif inte_df.iloc[high_ind]['고가'] < inte_df.iloc[n]['고가']:
                        break
                
                high_af_arr.append(high_count_af)
                ### 카운트 초기화 ###
                high_count_af = 0
                
            ### 데이터프레임에 리스트를 열로 추가하기 ###
            high_df['최대수'] = high_af_arr
                
            #########################################################################################################################
            # 초기화 작업
            ### 카운트 초기화 ###
            high_count_bf = 0
            
            ### 배열 초기화 ###
            high_bf_arr = []
            high_af_arr = []
            
            ### 인덱스 1증가 ###
            count_ind += 1
            
            ### 5초 뒤에 실행 ###
            #time.sleep(0.1)

            ### 데이터프레임 출력 ###
            #print(low_df)
            
            #########################################################################################################################
            # 최저라인 조건을 만족하는 값들 가져오기
            # 최저라인의 첫터치, 둘터치 구하기
            # 전작은값수나 후작은값수가 10미만 인 것들은 필터
            high_data = high_df[high_df['최대수'] >= 10]
            high_data = high_data.reset_index(drop=True)
            
            # 첫번째 터치 구하기
            touch1_data_arr = []
            touch_date = '없음'
            
            for i in high_data.index: 
                high_ind2 = inte_df[inte_df['일시']==high_data.iloc[i]['일시']].index[0]
                for j in inte_df.index:
                    if j > high_ind2 :
                        if inte_df.iloc[j]['종가'] >= high_data.iloc[i]['고가']:
                            touch_date = inte_df.iloc[j]['일시']
                            break

                # 터치1 일자 값을 넣기
                touch1_data_arr.append(touch_date)
                            
                # 터치데이터 초기화
                touch_date = '없음'
                
            high_data['첫터치'] = touch1_data_arr
            
            # 두번째 터치 구하기
            touch2_data_arr = []
            touch2_price_arr = []
            touch_date2 = '없음'
            touch_price2 = '없음'
            
            for i in high_data.index: 
                for j in inte_df.index:
                    if high_data.iloc[i]['첫터치'] == '없음' :
                        break
                    else :
                        high_ind3 = inte_df[inte_df['일시']==high_data.iloc[i]['첫터치']].index[0]
                        if j > high_ind3 :
                            if inte_df.iloc[j]['종가'] <= high_data.iloc[i]['고가']:
                                touch_date2 = inte_df.iloc[j]['일시']
                                touch_price2 = inte_df.iloc[j]['종가']
                                break
                            
                # 터치2 일자 값을 넣기
                touch2_data_arr.append(touch_date2)
                touch2_price_arr.append(touch_price2)
                
                # 터치데이터 초기화
                touch_date2 = '없음'
                touch_price2 = '없음'
                
            high_data['둘터치'] = touch2_data_arr
            high_data['진입가'] = touch2_price_arr
            
            #########################################################################################################################
            # 진입, 청산, 손절 해보기
            # 진입 = 둘터치 종가, 청산 = 진입에서 손절사이의 최대값 or 10분 내 최대값, 손절 = 첫터치에서 둘터치 사이의 최소값
            final_data = high_data[high_data["둘터치"] != "없음"]
            final_data = final_data[['최저수','최대수','첫터치','둘터치','진입가']]
            final_data = final_data.reset_index(drop=True)
            
            # 손절가 구하기
            stop_loss_arr = []
            stop_loss = 0
            
            for i in final_data.index:
                touch1_ind = inte_df[inte_df['일시']==final_data.iloc[i]['첫터치']].index[0]
                touch2_ind = inte_df[inte_df['일시']==final_data.iloc[i]['둘터치']].index[0]
                stop_loss = inte_df[touch1_ind:touch2_ind]['고가'].max()
                
                # stop_loss_arr에 넣기
                stop_loss_arr.append(stop_loss)
            
            final_data['손절가'] = stop_loss_arr
            
            # 둘터치 이후 10분이내의 동향 살펴보기
            if len(final_data) != len_fi : 
                final_data = final_data.sort_values('둘터치', ascending=True)
                ind = dataset[dataset['일시']==final_data.iloc[-1]['둘터치']].index[0]
                
                print(final_data.iloc[-1])
                print(dataset[ind+1:ind+11])
                
                len_fi = len(final_data)
            
            #########################################################################################################################
            ### 데이터프레임에서 최대수 열 없애기
            high_df = high_df.drop(['최대수'], axis=1)
            #print(count_ind)
    def min_line(self):
        pass

## 실행 ##
conn = all_cls()
conn.exe_all()
