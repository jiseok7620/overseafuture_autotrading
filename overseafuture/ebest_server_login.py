import win32com.client
import pythoncom

'''
[모의투자 로그인을 위해선]
1. 모의투자 신청
2. xingApi 폴더 내 모든 항목 삭제 후 업데이트
'''

class ebest_server_logindemo_cls:
    login_state = 0

    def OnLogin(self, code, msg): # OnLogin으로 써야만 code, msg 정보를 리턴받을 수 있음
        if code == "0000":
            print('login : ',msg)
            ebest_server_logindemo_cls.login_state = 1
        else:
            print('login : ',msg)
                
    def OnDisconnect(self):
        print('서버와 연결이 끊겼습니다.')
        
    def OnLogout(self):
        print('로그아웃 되었습니다.')

class logindemo_cls:
    def exe_logindemo(self): 
        # 객체 생성하기
        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", ebest_server_logindemo_cls)
        
        # 연결 끊기
        instXASession.DisconnectServer()
        
        # 로그인 정보
        id = ""
        passwd = ""
        cert_passwd = ""
        
        # 로그인 서비 및 로그인
        instXASession.ConnectServer("demo.ebestsec.co.kr", 20001)
        blogin = instXASession.Login(id, passwd, cert_passwd, 0, 0) # 로그인 서버에 전송
        
        # 수신(응답) 대기
        while ebest_server_logindemo_cls.login_state == 0:
            pythoncom.PumpWaitingMessages()
            
        account = []
        num_account = instXASession.GetAccountListCount()
        for i in range(num_account):
            account.append(instXASession.GetAccountList(i))
            
        print(account)