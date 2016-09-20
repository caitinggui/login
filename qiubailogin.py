#!usr/bin/python
#coding:utf-8

import re

import requests
from bs4 import BeautifulSoup

class QiubaiLogin(object):
    
    def __init__(self):
        self.login_url = 'http://www.qiushibaike.com/session.js'
        self.captcha_name = '/home/ctg/tmp/captcha.jpg'
        self.host = 'http://www.qiushibaike.com'

        self.headers={
            'Host': 'www.qiushibaike.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Referer': self.host,
        }
        self.s = requests.Session()
        self.s.headers = self.headers
        
    def login_qiubai(self):
        r = self.s.get(self.host)
        soup = BeautifulSoup(r.text, 'lxml')
        login_form_url = self.host + soup.find(id='uname')['href']
        r = self.s.get(login_form_url)
        soup = BeautifulSoup(r.text,'lxml')
        xsrf2 = soup.find('input',attrs={'name':'_xsrf'})['value']

        username = raw_input("Please input username:")
        password = raw_input("Please input password:")

        data = {
            'login':username,
            'password':password,
            "_xsrf":xsrf2,
            'remember_me':'checked',

        }

        r = self.s.post(self.login_url, data=data)
        if re.findall('\"err\": 0', r.text):
            print 'login success'
            return self.s,r
        else:
            print 'login fail'
            return ''
        
        
if __name__ == '__main__':
    ctg_qiubai = QiubaiLogin()
    session = ctg_qiubai.login_qiubai()
