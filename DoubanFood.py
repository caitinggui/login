#!/usr/bin/python
#coding:utf-8

import os
import re
import time

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import doubanlogin 

class DoubanFood(object):
    
    def __init__(self):
        self.url = 'https://www.douban.com/subject/all'
        self.first_page = '?cat_id=1000&start=8760'
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.column_dimensions['B'].width = 50
        self.ws.column_dimensions['C'].width = 40
        self.ws.column_dimensions['D'].width = 120
        self.get_food_times = 2
        douban_login = doubanlogin.DoubanLogin()
        self.s = douban_login.login_douban()
        try:
            os.mkdir('douban_food')
        except:
            pass
        self.path = os.path.join(os.getcwd(), 'douban_food')
        self.logger = open(os.path.join(self.path, 'log.txt'), 'a')
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Host': 'www.douban.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0)     Gecko/20100101 Firefox/47.0'
         }
        
    def download_food(self):
        next_page = self.first_page
        n = 439
        while next_page:
            print('get page %d' % n)
            print(next_page)
            try:
                r = self.s.get(self.url+next_page)
                soup = BeautifulSoup(r.text, 'lxml')
                next_page = self.get_next_page(soup)
                self.get_food_info(soup)
                self.wb.save(os.path.join(self.path, 'food.xlsx'))
                self.logger.write(str(n))
                self.logger.write(':'+next_page+'\n')
                self.logger.flush()
                time.sleep(60)
            except Exception, e:
                print 'get page %d failed:%s' % (n, e)
            n += 1
        
    def download_photos(self, name, food_soup):
        photo_tag = food_soup.find(id='th-photos')
        urls = photo_tag.find_all('li')
        url_num = len(urls)
        if url_num > 1:
            path = os.path.join(self.path, name)
            try:
                os.mkdir(path)
            except:
                pass
        else:
            path = self.path
            fname = os.path.join(path, name+'.jpg')
            
        for url in urls:
            try:
                r = requests.get(url.a['href'], headers=self.headers)
                soup = BeautifulSoup(r.text, 'lxml')
                real_url = soup.find(class_='photo').a.img['src']
                #print('real_url:%s' % real_url)
                r = requests.get(real_url, stream=True).content
                if url_num > 1:
                    fname = os.path.join(path, url.img['src'].split('/')[-1])
                f = open(fname, 'wb')
                f.write(r)
                f.close()
                
            except Exception, e:
                print('download photos failed:%s' % e)

        
    def get_next_page(self, soup):
        try:
            next_page = soup.find(attrs={'rel':'next'})['href']
        except Exception,e:
            print 'get next page failed:%s' % str(e)
            return False
        return next_page
    
    def get_food_url(self, soup):
        # food tag
        tag = soup.find(class_='thing-list')
        # contain url and name
        return tag.find_all(title=True, text=True)
        
    def get_food_info(self, soup):
        
        urls = self.get_food_url(soup)

        for url_name in urls:
            try:
                # name, info, url, review
                food_info = []
                url = url_name['href']
                name = url_name.text
                for i in range(self.get_food_times):
                    try:
                        r = self.s.get(url)
                        break
                    except Exception, e:
                        print 'get food info faied:%s\ntry again!' % str(e)
                food_soup = BeautifulSoup(r.text, 'lxml')
                # food info
                info = food_soup.find(id='link-report').p.text
                
                food_info.append(name)
                food_info.append(info)
                food_info.append(url)
                try:
                    first_review_soup = food_soup.find(class_='review-list').div
                    review = first_review_soup.find(class_='review-content').text
                    food_info.append(review)
                except:
                    pass
                self.save_food_info_to_excel(food_info)
                self.download_photos(name, food_soup)
                time.sleep(30)
            except Exception, e:
                pass
            
            
    def save_food_info_to_excel(self, food_info):
        self.ws.append(food_info)
            
if __name__ == '__main__':
    a = DoubanFood()
    a.download_food()
    
    
            

