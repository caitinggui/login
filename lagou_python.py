#coding:utf-8

import time

import requests
from openpyxl import Workbook

host = 'http://www.lagou.com/jobs/companyAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Host': 'www.lagou.com',
 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0)     Gecko/20100101 Firefox/47.0'
 }

def get_json(url, page, lang_name):
    data = {'first': 'true', 'pn': page, 'kd': lang_name}
    json = requests.post(url, data).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i['companyFullName'])
        info.append(i['salary'])
        info.append(i['city'])
        info.append(i['education'])
        info.append(i['positionId'])
        info.append(i['positionName'])
        info.append(i['positionAdvantage'])
        info.append(i['financeStage'])
        info.append(i['industryField'])

        info_list.append(info)
    return info_list


def main():
    lang_name = 'python'
    page = 1
    url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    info_result = []
    for page in range(30):
        print page
        try:
            info = get_json(url, page, lang_name)
            info_result = info_result + info
        except:
            print('open %d page failed' % page)
        time.sleep(3)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = lang_name
    for row in info_result:
        ws1.append(row)
    wb.save('manage_info.xlsx')

if __name__ == '__main__':
    main()
