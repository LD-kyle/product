# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 12:56:00 2018

@author: Administrator
"""

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
import merge_sohu_sales as mss

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}


url0='http://s.auto.sohu.com/search.at?suggest='

def get_data(uid): 
    r = requests.get('http://db.auto.sohu.com/api/para/data/trim_{}.json'.format(uid),timeout=10,headers=headers)   
    return r.json()

def get_data1(uid): 
    r = requests.get('http://db.auto.sohu.com/api/model/select/trims_{}.json'.format(uid), timeout=10,headers=headers)   
    return r.json()

def get_status(s):
    if s==1:
        a='在售'
    elif s==-2:
        a='停产在售'
    elif s==-1:
        a='停售'
    else:
        a=s
    return a
    

                                
def get_ev(c):
    s = requests.Session()
    c0=quote(c,encoding='gbk')
    r=s.get(url0+c0, timeout=10,headers=headers)
    root = etree.HTML(r.content)
    div=root.xpath("//div[@class='l_part']/div")[0]
    url1=div.xpath("h2/a")[0].get('href')
    dict1=get_data1(re.findall(r'\d+\d?',url1)[-1])
    #dict2=get_data( dict1["trimyears"][0]["trims"][0]["tid"])
    content0=[]
    list1=[]
    for x in ['车厂','汽缸数(个)','官方0-100加速(s)','变速箱','级别','车体结构','车身结构']:
        list1.append(scd.get_detail(x))
    #type0=unquote(dict2['SIP_C_303']).replace('%', '\\').encode().decode('unicode_escape')
    list0=['SIP_C_303','SIP_C_117','SIP_C_118','SIP_C_119','SIP_C_120','SIP_C_112',
            'SIP_C_123','SIP_C_307','SIP_C_308','SIP_C_309','SIP_C_310','SIP_C_311',
            'SIP_C_353','SIP_C_294']+list1
    
    for i in range(0, len(dict1["trimyears"])):
            dict1_1=dict1["trimyears"][i]
            year=dict1_1['y']
            for j in range(0,len(dict1_1["trims"])):
               dict1_2=dict1_1["trims"][j]
               
               dict3=get_data(dict1_2["tid"])
               types=[c,year,dict1_2["tname"],dict1_2["price"],get_status(dict1_2["status"])]
               for model in list0:
                  try:
                      types.append(unquote(dict3[model]).replace('%', '\\').encode().decode('unicode_escape'))
                  except Exception as e:
                      types.append('')
               content0.append(types)
        
    return content0


def crawl():
    s=requests.Session()
    url='http://db.auto.sohu.com/cxdata/iframe.html'
    r=s.get(url,headers=headers)
    root = etree.HTML(r.content)
    column,content,content1=[],[],[]
    trs=root.xpath('//div[@class="sales_con"]/div[3]/table/tbody/tr')
    column.append(trs[0].xpath('td/text()')[0])
    for th in trs[0].xpath('th'):
          column.append(th.xpath('span/text()')[0])
    column1=['车型','年份','款式','售价','销售状态','动力类型','长度(mm)',
             '宽度(mm)','高度(mm)','轴距(mm)',
             '最高车速','整备质量','电动机最大功率(kW)','电动机最大扭矩', 
            '最大行驶里程(km)', '电池种类','电池容量(kWh)','电机数',
            '工信部油耗(L/100km)(城市/市郊/综合)','车厂',
            '汽缸数(个)','官方0-100加速(s)','变速箱','级别','车体结构','车身结构']
    for i in range(1,len(trs)):
        x=0
        tds=trs[i].xpath('td')
        #name=tds[1].xpath('a')[0].text
        detail=[]
        detail.append(tds[0].text)
        detail.append(tds[1].xpath('a')[0].text)
        for x in range(2,len(tds)):
                   detail.append(tds[x].text)
        content.append(detail)
        done,done1,name=True,True,detail[1]
        while done1:
          try:
             list0=get_ev(name)
             done1=False
          except Exception as e:
             x+=1
             if ('Read timed out' not in str(e))|(x>5):               
                 done1,done=False,False
             print(e,tds[1].xpath('a')[0].text)
        print(name)
        if done:    
           content1=content1+list0
    df=pd.DataFrame(content,columns=column)
    df1=pd.DataFrame(content1,columns=column1)
    df.set_index('序号').to_csv('sales/sales.csv')
    df.set_index('序号').to_excel('sales/sales.xlsx')
    df1.set_index('车型').to_csv('sales/sales_par1.csv')
    df1.set_index('车型').to_excel('sales/sales_par1.xlsx')



if __name__=='__main__':
    crawl()
    mss.main()