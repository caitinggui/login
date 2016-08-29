#!/usr/bin/python
#coding:utf-8

import os
import time

import requests
from bs4 import BeautifulSoup

page_url = raw_input("Please input cl page url:")
path = '/home/ctg/myself'
folder_name = raw_input("Please input folder to save:")
real_path = os.path.join(path,folder_name)
while os.path.exists(real_path):
    folder_name = raw_input('This folder is existed, please input another one:')
    real_path = os.path.join(path,folder_name)
os.makedirs(real_path)
print 'Save photos to "%s"' % real_path

def download(url):
    with open(os.path.join(real_path, url.split('/')[-1]), 'wb') as f:
        try:
            r = requests.get(url, stream=True)
            f.write(r.content)
        except Exception, e:
            print 'Get photo fail:%s' % str(e)
        

        
r = requests.get(page_url)
soup = BeautifulSoup(r.text, 'lxml')
for photo_info in soup.find_all('img',style="cursor:pointer"):
    url = photo_info['src']
    print url
    download(url)
    time.sleep(1)