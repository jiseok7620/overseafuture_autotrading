import requests
import json
from datetime import datetime
from django.shortcuts import redirect

class cacao_login_cls:
    # 2개월에 한번 refresh코드 발급받기
    def token(self, code):
        # 카카오톡 메시지 API
        url = "https://kauth.kakao.com/oauth/token"
        
        data = {
            "grant_type" : "authorization_code",
            "client_id" : "",
            "redirect_url" : "https://naver.com",
            "code" : code
        }
        response = requests.post(url, data=data)
        tokens = response.json()
        
        with open("kakao_refcode.json","w") as fp:
            json.dump(tokens, fp)
    
    # refresh 코드로 계속 acc코드 갱신하기
    def auth_refresh(self): 
        with open("kakao_refcode.json", "r") as fp: 
            ts = json.load(fp) 
            
        r_token = ts["refresh_token"] 
        
        url = "https://kauth.kakao.com/oauth/token"
        
        data = { 
            "grant_type": "refresh_token", 
            "client_id": "",
            "refresh_token": r_token } 
        
        response = requests.post(url, data=data) 
        tokens = response.json() 
        
        with open(r"kakao_acccode.json", "w") as fp: 
            json.dump(tokens, fp) 
        
        with open("kakao_acccode.json", "r") as fp: 
            ts2 = json.load(fp) 
            
        token = ts2["access_token"] 
        return token
    
    # 나에게 메세지 보내기
    def send_myself(self, token, sendMessage):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        
        header = {
                "Content-Type": "application/x-www-form-urlencoded", 
                "Authorization": 'Bearer ' + token}
        
        post = {
            "object_type": "text",
            "text": sendMessage,
            "link": {
                "web_url": "https://developers.kakao.com",
                "mobile_web_url": "https://developers.kakao.com"
            },
            "button_title": "바로 확인"      
        }
        data = {"template_object": json.dumps(post)}
        returnValue=requests.post(url, headers=header, data=data)
        print(returnValue)
    
    
    ####-------------------------------------------------------------------------####
    # 친구에게 메세지 보내기
    def findFriends(self, token):
        url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
        header = {"Authorization": 'Bearer ' + token}
        #header = {"Authorization": 'Bearer ' + tokens["access_token"]}
        
        result = json.loads(requests.get(url, headers=header).text)
        friends_list = result.get("elements")
        print(friends_list)
        
        #friend_id = friends_list[0].get("uuid")
        #print(friend_id)

    def sendToMessage(self):
        friend_id = ""
        
        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        
        data={
            #'receiver_uuids': '["{}"]'.format(friend_id)
            'receiver_uuids': friend_id,
            "template_object": json.dumps({
                "object_type":"text",
                "text":"성공입니다!",
                "link":{
                    "web_url" : "http://naver.com",
                    "mobile_web_url" : "http://naver.com"
            },
            "button_title": "바로 확인"
            })
        }

# https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=49beafbf3d0867b0d7ad6679e63d85ea&redirect_uri=https://naver.com
'''
conn = cacao_login_cls()
code = "WflkaLIrKJVIdOM5WrWLhuxk-QzYJLlp3WNn0QnRC-N7GtIczMm5JnVKxofhwVQcE4g8pAo9dRoAAAGBTBf3Lg"
conn.token(code)
token = conn.auth_refresh()
conn.send_myself(token, '아아')
conn.sendToMessage()
'''
#conn.findFriends(token)
