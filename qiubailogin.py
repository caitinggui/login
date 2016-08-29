#!usr/bin/python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
import webbrowser

login_url = 'http://www.qiushibaike.com/session.js'
captcha_name = '/home/ctg/tmp/captcha.jpg'
host = 'http://www.qiushibaike.com'

headers={
    'Host': 'www.qiushibaike.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'http://www.qiushibaike.com',
}
s = requests.Session()
s.headers = headers
r = s.get(host)
soup = BeautifulSoup(r.text)
login_form_url = host + soup.find(id='uname')['href']
xsrf1 = soup.find('input',attrs={'name':'_xsrf'})['value']
r = s.get(login_form_url)
soup = BeautifulSoup(r.text,'lxml')
xsrf2 = soup.find('input',attrs={'name':'_xsrf'})['value']

username = raw_input("Please input username:")
password = raw_input("Please input password:")

data = {
    'login':username,
    'password':password,
    #"_xsrf":xsrf1,
    "_xsrf":xsrf2,
    'remember_me':'checked',

}

r = s.post(login_url, data=data)
print r.text
print 'login success'
