import sys
import pandas as pd
import os
import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

form_class = uic.loadUiType("main.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        
        
        ##----------------------------------------------------------------------------##
        ## 버튼 클릭 시 함수와 연결 모음 ##
        # 대신로그인 버튼 클릭
        self.버튼명.clicked.connect(self.함수명)

        
        
        ##----------------------------------------------------------------------------##
        ## 테이블안의 셀 조작 ##
        # 테이블에서 셀의 내용 더블 클릭 시 함수와 연결 
        self.테이블명.cellDoubleClicked.connect(self.함수명)

        
        
        ##----------------------------------------------------------------------------##
        ## 버튼 기능 활성화
        self.버튼명.setEnabled(False)
        
        
    ''' 
    '''
    '''   
    ## 함수 모음 ##
    '''
    '''
    '''
    ##----------------------------------------------------------------------------##
    ## 테이블 안의 셀 클릭 시 함수
    def Screen1_Cell_Double_Clicked(self):
        # 더블클릭한 곳의 행, 열 번호 조회
        row = self.Table_One.currentRow()
        col = self.Table_One.currentColumn()
        
        # 해당 행과 열의 값을 객체 형태로 가져오기
        result = self.Table_One.item(row, col)
        
        # 해당 셀의 내용을 변수로 저장하고 괄호 빼기
        aa = result.text()
        aa = aa.lstrip('[')
        aa = aa.rstrip(']')
        
        # 해당 셀의 내용을 조회 라인에 입력
        self.Line_Search.setText(aa)
        
        
        
    ##----------------------------------------------------------------------------##    
    ## 버튼클릭시 함수 모음 ##
    def Btn_Search_One_clicked(self):
        pass
    

'''
'''
'''
실행
'''
'''
'''           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()