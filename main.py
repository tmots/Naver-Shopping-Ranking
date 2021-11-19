from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import sys

########### csv 읽기 ############
f = open('keyword.csv', 'r')
key = csv.reader(f)
keyword=[]

for line in key:
    keyword.extend(line)

print(keyword)
f.close()

########### 크롬띄우기 ############
driver = webdriver.Chrome('d:/python/chromedriver.exe')
driver.implicitly_wait(3)

########### 로그인 ################
print('id=')
id = input()
print('pw=')
pw = input()

driver.get('https://sjnim.com/bbs/login')
driver.find_element_by_id('mb_id').send_keys(id)
driver.find_element_by_id('mb_password').send_keys(pw)
driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/form/button').click()

########### 키워드 검색 ################
store_Name = '스킨멜로우'
key_Rank=[]
key_Name=[]
for key_num in keyword:
    driver.get('https://sjnim.com/content/search_rank?storename='+store_Name+'&keyword='+key_num)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        #### 순위 받아 오기 ####
        key_Rank.append(driver.find_element_by_xpath('//*[@id="product_list"]/section/div/div/div[2]/h4/span').text)
        #### 제품명 받아 오기 ####
        key_Name.append(driver.find_element_by_xpath('//*[@id="product_list"]/section/div/div/div[2]/h6').text)
    except:
        key_Rank.append('x')
        key_Name.append('x')

print(key_Rank, key_Name)
driver.close()

########## PyQt 뿌려주기 ###############

class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainForm()

    def mainForm(self):

        editer = QtForm()
        self.setCentralWidget(editer)
        self.setGeometry(30, 70, 400, 1500)
        self.setWindowTitle('어제 네이버 광고 금액')
        self.show()

class QtForm(QWidget):
    def __init__(self):
        super().__init__()
        self.textUi()

    def textUi(self):

        kw_Label = QLabel('키워드')
        kw_Edit = QTextEdit()
        kw_Num = QTextEdit()
        kw_Name = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(kw_Label, 0, 0)
        grid.addWidget(kw_Edit, 0, 1)
        grid.addWidget(kw_Num, 0, 2)
        grid.addWidget(kw_Name, 0, 3)

        self.setLayout(grid)

        for kw1 in keyword:
            kw_Edit.insertPlainText(kw1 + '\n')
        for kw2 in key_Rank:
            kw_Num.insertPlainText(kw2 + '\n')
        for kw3 in key_Name:
            kw_Name.insertPlainText(kw3 + '\n')

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MyForm()
    sys.exit(app.exec_())
