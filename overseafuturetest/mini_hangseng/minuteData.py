import pandas as pd
import win32com.client
import pythoncom
import time

class ebestapi_o3103_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_o3103_cls.query_state = 1
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        pass
        #print('o3103 에러발생 : ', err)

class o3103_cls:
    def exe_o3103(self, code, minit, cnt, num):
        # 쿼리 객체 생성
        object_o3103 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_o3103_cls)
        
        # Res 파일 등록
        object_o3103.ResFileName = "C:\\eBEST\\xingAPI\\Res\\o3103.res"

        # 변수지정
        how = False
        cts_date = ""
        cts_time = ""
        count = 0
        count_num = 0
        dataset = pd.DataFrame()
        
        while True :
            # 쿼리 상태 초기화 
            ebestapi_o3103_cls.query_state = 0
            
            # InBlock에 값 설정
            object_o3103.SetFieldData("o3103InBlock", "shcode", 0, code) # 조회 종목 코드(CME 거래소는 신청해야 가능)
            object_o3103.SetFieldData("o3103InBlock", "ncnt", 0, minit) # 조회 분 
            object_o3103.SetFieldData("o3103InBlock", "readcnt", 0, cnt) # 조회 개수
            object_o3103.SetFieldData("o3103InBlock", "cts_date", 0, cts_date)
            object_o3103.SetFieldData("o3103InBlock", "cts_time", 0, cts_time)
                
            # 데이터 요청
            aa = object_o3103.Request(how) # True : 연속데이터 조회로 요청
            
            # 10분내 요청한 요청 횟수 취득
            '''
            count_limit = object_o3103.GetTRCountLimit("o3103")
            count_request = object_o3103.GetTRCountRequest("o3103")
            print('o3103 10분 당 제한 건수 : ', count_limit)
            print('o3103 10분 내 요청 횟수 : ', count_request)
            '''
            
            # 수신 대기
            while ebestapi_o3103_cls.query_state == 0:
                pythoncom.PumpWaitingMessages()
                
            # 연속조회 OutBlock값
            cts_date = object_o3103.GetFieldData("o3103OutBlock", "cts_date", 0)
            cts_time = object_o3103.GetFieldData("o3103OutBlock", "cts_time", 0)
            how = True
            
            # 연속조회시 개수 가져오기 => 연속 시 1을 붙여줌
            count = object_o3103.GetBlockCount("o3103OutBlock1")
            #print('t1702 가져올 데이터의 수 : ',count)
        
            arr_datetime = [] # 일자시간
            arr_open = [] # 시가
            arr_high = [] # 고가
            arr_low = [] # 저가
            arr_close = [] # 종가
            arr_volume = [] # 거래량
            
            # 필요한 필드 가져오기
            for i in range(count):
                date = object_o3103.GetFieldData("o3103OutBlock1", "date", i)
                tm = object_o3103.GetFieldData("o3103OutBlock1", "time", i)
                open = object_o3103.GetFieldData("o3103OutBlock1", "open", i)
                high = object_o3103.GetFieldData("o3103OutBlock1", "high", i)
                low = object_o3103.GetFieldData("o3103OutBlock1", "low", i)
                close = object_o3103.GetFieldData("o3103OutBlock1", "close", i)
                volume = object_o3103.GetFieldData("o3103OutBlock1", "volume", i)
                
                arr_datetime.append(date + tm)
                arr_open.append(open)
                arr_high.append(high)
                arr_low.append(low)
                arr_close.append(close)
                arr_volume.append(volume)
                
            # 데이터 프레임으로 만들기
            data = pd.DataFrame({'일시' : arr_datetime, '시가' : arr_open, 
                                 '고가' : arr_high, '저가' : arr_low, '종가' : arr_close,
                                 '거래량' : arr_volume                           
                                 })
            
            #print(data)
            # 데이터 형식 int로 바꾸기
            #data = data.astype(int)
            
            # 데이터 프레임에 추가하기
            dataset = dataset.append(data, sort=False)
            
            # count_num는 +1씩 더해줌
            count_num += 1
            
            # n번 가져오고 멈추기
            if count_num == num:
                break
            
            # 1초마다 반복
            time.sleep(1)
            
        # 데이터 타입 바꾸기
        dataset = dataset.astype({'일시':'float'})
        dataset = dataset.astype({'시가':'float'})
        dataset = dataset.astype({'고가':'float'})
        dataset = dataset.astype({'저가':'float'})
        dataset = dataset.astype({'종가':'float'})
        dataset = dataset.astype({'거래량':'float'})
        
        # 오름차순 정렬하기
        dataset = dataset.sort_values('일시', ascending=True)
        
        # 인덱스 초기화하기    
        dataset = dataset.reset_index(drop=True)
        
        # 엑셀로 저장하기
        dataset.to_excel('F:/JusikData/mini_hangseng1.xlsx', index=False) # 엑셀로 저장
        
        # 데이터프레임 리턴하기
        #print(dataset)
        return dataset
