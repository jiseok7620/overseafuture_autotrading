import win32com.client
import pythoncom
import time

class ebest_server_login_cls:
    login_state = 0

    def OnLogin(self, code, msg): # OnLogin으로 써야만 code, msg 정보를 리턴받을 수 있음
        if code == "0000":
            print('login : ',msg)
            ebest_server_login_cls.login_state = 1
        else:
            print('login : ',msg)
                
    def OnDisconnect(self):
        print('서버와 연결이 끊겼습니다.')
        
    def OnLogout(self):
        print('로그아웃 되었습니다.')

class login_cls:
    def exe_login(self): 
        # 객체 생성하기
        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", ebest_server_login_cls)
        
        # 연결 끊기
        instXASession.DisconnectServer()
        
        # 로그인 정보
        id = "ghkd7620"
        passwd = "q741852"
        cert_passwd = "js101600?!"
        
        # 로그인 서비 및 로그인
        instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
        blogin = instXASession.Login(id, passwd, cert_passwd, 0, 0) # 로그인 서버에 전송
        
        # 수신(응답) 대기
        while ebest_server_login_cls.login_state == 0:
            pythoncom.PumpWaitingMessages()