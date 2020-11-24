from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
from datetime import datetime
from datetime import timedelta

os.chdir(r'D:\Python\immg')
'''
Parameter setting
'''
column=['日期','管制站','入境:香港居民','入境:內地訪客','入境:其他訪客','入境:總計',
        '出境:香港居民', '出境:內地訪客', '出境:其他訪客', '出境:總計']
date=datetime(2020, 8, 1) #change if necessary

'''
Main program
'''
raw=pd.DataFrame(columns=column)
while date != datetime(2020, 11, 23): #change if necessary
    mmdd=str(date.month).zfill(2)+str(date.day).zfill(2)
    date+=timedelta(days=1)

    url=r'https://www.immd.gov.hk/hkt/stat_2020{}.html'.format(mmdd)
    link=requests.get(url)
    soup = BeautifulSoup(link.content, 'html.parser')

    table=soup.find('table',class_='grid table-stat hRight txt_small')
    table=table.find_all('tr')[5:5+15]

    download_list=[]
    for i in range(len(table)):
        control_point_data=['2020'+mmdd]
        for j in range(len(table[i].find_all('td'))):
            if j>0:
                control_point_data.append(int(table[i].find_all('td')[j].get_text().replace(',','')))
            else:
                control_point_data.append(table[i].find_all('td')[j].get_text())
        download_list.append(control_point_data)
    tmp=pd.DataFrame(download_list,columns=column)
    raw=pd.concat([raw,tmp])

raw.to_excel('output.xlsx',index=False,encoding='utf-8')


