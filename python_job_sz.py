#coding:utf-8

import time

import requests
from bs4 import BeautifulSoup

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Host': 'www.lagou.com',
 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0)     Gecko/20100101 Firefox/47.0'
 }
host = 'http://www.lagou.com/jobs/'

s = requests.Session()
s.headers = headers
jobs_txt = open('/home/ctg/project/scrapy_project/python_jobs_sz.txt', 'w')
with open('/home/ctg/project/scrapy_project/python_company_sz.txt', 'r') as f:
    for i in f.readlines():
        try:
            url = host + i[:-1] + '.html'
            print url
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            tag = soup.find(id='job_detail')
            text = tag.get_text()
            jobs_txt.write(text.encode('utf-8'))
            jobs_txt.write('\n\n\n\n\n\n\n\n\n\n\n\n')
            jobs_txt.flush()
            time.sleep(2)
        except Exception,e:
            print(e)
    jobs_txt.close()

