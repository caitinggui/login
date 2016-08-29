#!usr/bin/python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
import webbrowser

class DoubanLogin(object):
    
    def __init__(self):
        self.login_url = 'https://www.douban.com/accounts/login'
        self.captcha_name = '/home/ctg/tmp/captcha.jpg'
        self.host = 'https://www.douban.com'
        self.headers={
            'Host': 'www.douban.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0)     Gecko/20100101 Firefox/47.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.douban.com',
        }
        self.data = {
            'source':'index_nav',
            'form_email':'',
            'form_password':'',
            'remember':'on',
        }
        self.s = requests.Session()
        self.s.headers = self.headers
        print str(self.s.headers)
        
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
        
    def login_douban(self):
        r = self.s.get(self.host)
        soup = BeautifulSoup(r.text, 'lxml')
        # print r.text
        form_email = raw_input('Please input username:')
        form_password = raw_input('Please input password')
        self.data['form_email'] = form_email
        self.data['form_password'] = form_password
        is_captcha = False
        try:
            is_captcha = soup.find(attrs={'name':"captcha-id"})
        except:
            pass
        if is_captcha:
            self.handle_captcha(soup)
        
        r = self.s.post(self.login_url, data=self.data)
        if r.url == self.login_url:
            print r.text
            soup = BeautifulSoup(r.text, 'lxml')
            self.handle_captcha(soup)
            r = self.s.post(self.login_url, data=self.data)
            print r.text
        else:
            pass
        # print r.text
        print 'login success'
        return self.s
