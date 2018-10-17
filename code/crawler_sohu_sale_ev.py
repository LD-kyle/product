# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:45:06 2018

@author: Jason
"""

import requests
#import eventlet
import sohu_car_dict as scd 
import pandas as pd
from lxml import etree
from urllib.parse import unquote
from urllib.parse import quote
import json
import re


url0='http://s.auto.sohu.com/search.at?suggest='
cookies={'beans_12539':'visit:2',
 'beans_13981':'visit:1',
 'IPLOC':'CN2201',
 'SUV':'180827155148MKF3',
 'vjuids':'20b64ffac.1657a57a580.0.0aec2beccbdc4',
 'JSESSIONID':'aaaYy6mW07WlXeeKY9Bvw; ipcncode=CN220100',
 'vjlast':'1535355889.1535414233.13',
 'records_models':'%u672C%u7530%u601D%u57DF%7C%7C1993%3B%u5927%u4F17%u5E15%u8428%u7279%7C%7C2524%3B%u4E30%u7530%u5361%u7F57%u62C9%7C%7C1016'}   

def get_data(uid): 
    r = requests.get('http://db.auto.sohu.com/api/para/data/trim_{}.json'.format(uid),verify=False, timeout=10)   
    return r.json()

def get_data1(uid): 
    r = requests.get('http://db.auto.sohu.com/api/model/select/trims_{}.json'.format(uid),verify=False, timeout=10)   
    return r.json()

                                
def get_ev(c):
    s = requests.Session()
    c0=quote(c,encoding='gbk')
    r=s.get(url0+c0,verify=False, timeout=10)
    root = etree.HTML(r.content)
    div=root.xpath("//div[@class='l_part']/div")[0]
    url1=div.xpath("h2/a")[0].get('href')
    dict1=get_data1(re.findall(r'\d+\d?',url1)[-1])
    dict2=get_data( dict1["trimyears"][0]["trims"][0]["tid"])
    content0=[]
    list1=[]
    for x in ['车厂','汽缸数(个)','官方0-100加速(s)','变速箱','级别','车体结构']:
        list1.append(scd.get_detail(x))
    type0=unquote(dict2['SIP_C_303']).replace('%', '\\').encode().decode('unicode_escape')
    list0=['SIP_C_303','SIP_C_117','SIP_C_118','SIP_C_119','SIP_C_120','SIP_C_112',
            'SIP_C_123','SIP_C_307','SIP_C_308','SIP_C_309','SIP_C_310','SIP_C_311',
            'SIP_C_353','SIP_C_294']+list1
    if type0=='纯电动':
        for i in range(0, len(dict1["trimyears"])):
            dict1_1=dict1["trimyears"][i]
            year=dict1_1['y']
            for j in range(0,len(dict1_1["trims"])):
               dict1_2=dict1_1["trims"][j]
               dict3=get_data(dict1_2["tid"])
               types=[c,year,dict1_2["tname"],dict1_2["price"]]
               for model in list0:
                  try:
                      types.append(unquote(dict3[model]).replace('%', '\\').encode().decode('unicode_escape'))
                  except Exception as e:
                      types.append('')
               content0.append(types)
        
    return (type0=='纯电动'),content0


def crawl():
    s=requests.Session()
    url='http://db.auto.sohu.com/cxdata/iframe.html'
    r=s.get(url)
    root = etree.HTML(r.content)
    column,content,content1=[],[],[]
    trs=root.xpath('//div[@class="sales_con"]/div[3]/table/tbody/tr')
    column.append(trs[0].xpath('td/text()')[0])
    for th in trs[0].xpath('th'):
          column.append(th.xpath('span/text()')[0])
    column1=['车型','年份','款式','售价','动力类型','长度(mm)',
             '宽度(mm)','高度(mm)','轴距(mm)',
             '最高车速','整备质量','电动机最大功率(kW)','电动机最大扭矩', 
            '最大行驶里程(km)', '电池种类','电池容量(kWh)','电机数',
            '工信部油耗(L/100km)(城市/市郊/综合)','车厂',
            '汽缸数(个)','官方0-100加速(s)','变速箱','级别','车体结构']
    for i in range(1,len(trs)):
        x=0
        tds=trs[i].xpath('td')
        name=tds[1].xpath('a')[0].text
        done1=True
        while done1:
          try:
             done,list0=get_ev(name)
             done1=False
          except Exception as e:
             x+=1
             if ('Read timed out' not in str(e))&(x<10):               
                 done1=False
             print(e,tds[1].xpath('a')[0].text)
             done=False
        print(name)
        if done:
            detail=[]
            detail.append(tds[0].text)
            detail.append(tds[1].xpath('a')[0].text)
            for x in range(2,len(tds)):
                   detail.append(tds[x].text)
            content.append(detail)
            content1=content1+list0
    df=pd.DataFrame(content,columns=column)
    df1=pd.DataFrame(content1,columns=column1)
    df.set_index('序号').to_csv('sales/sales_ev1.csv')
    df.set_index('序号').to_excel('sales/sales_ev1.xlsx')
    df1.set_index('车型').to_csv('sales/sales_ev_par1.csv')
    df1.set_index('车型').to_excel('sales/sales_ev_par1.xlsx')



if __name__=='__main__':
    crawl()