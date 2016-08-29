#!usr/bin/python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
import webbrowser

class ZhihuLogin(object):
    
    def __init__(self):
        self.s = requests.Session()
        self.s.headers = self.headers
        self.login_url = 'http://www.zhihu.com/login/email'
        self.captcha_name = '/home/ctg/tmp/captcha.jpg'
        self.host = 'https://www.zhihu.com'
        self.headers={
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0)     Gecko/20100101 Firefox/47.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'http://www.zhihu.com',
            'Connection': 'keep-alive',
        }
        self.data = {
            'email':'',
            'password':'',
            'remember_me':'true',
        }
        
    def read_captcha(self, captcha_url):
        r = self.s.get(captcha_url)
        with open(captcha_name,'wb') as f:
            f.write(r.content)
            f.close()
        webbrowser.open(self.captcha_name)
        captcha_solution = raw_input('input the captcha:')
        return captcha_solution
        
    def handle_captcha(self, soup):
        captcha_id = soup.find(attrs={'name':"captcha-id"})['value']
        captcha_url = soup.find(id='captcha_image')['src']
        captcha_solution = self.read_captcha(captcha_url)
        self.data["captcha-solution"] = captcha_solution
        self.data["captcha-id"] = captcha_id
        
    def login_zhihu(self):
        r = self.s.get(self.host)
        email = raw_input("Please input email:")
        password = raw_input("Please input password:")
        soup = BeautifulSoup(r.text, 'lxml')
        if soup.find(attrs={'name':"captcha-id"}):
            self.handle_captcha(soup)
            
        _xsrf = soup.find(attrs={'name':'_xsrf'})['value']
        self.data['_xsrf'] = _xsrf
        
        r = self.s.post(self.login_url, data=self.data)
        if r.url == self.login_url:
            soup = BeautifulSoup(r.text, 'lxml')
            self.handle_captcha(soup)
            r = s.post(login_url, data=data)
        else:
            pass
        print r.text
        print 'login success'
