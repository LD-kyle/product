import sys
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import send_inform_email as sie
from pathlib import Path
import os
import time


# get_contents(), crawl() 这两个函数是主要功能函数，
# 其它以下划线开头的函数为内部接口函数。


def _get_item(div,notice):
    """从 div 标签中获取 item.

    Returns
    -------
    item : list
        一辆车的信息。
    """
    item=[]
    td = div.table.tbody.tr.td
    table = td.find_all('table', recursive=False)[1]
    td = table.tbody.tr.find_all('td', recursive=False)[1]
    if len(td.find_all('div', recursive=False))>2:
         item.append(td.find_all('div', recursive=False)[2]
                    .strong.text.strip())
    else:
         item.append(td.div.strong.text.strip())  # title
    item = item[0].replace('*', ' ').split()
    trs = td.table.tbody.find_all('tr', recursive=False)
    item.append(tuple([td.find('strong').text.strip()
                       for td in trs[0].find_all('td')]))  # ID
    for i in range(1, len(trs)):
        item.append(tuple([trs[i].find('th').text.strip()]
                          + [td.text.strip() for td in trs[i].find_all('td')]))
    item.append(('推荐目录颁布年份', notice[0:4]))
    item.append(('推荐目录颁布批次', notice[4:]))
    return item


def _get_item_first(div,notice):
    """从第一个 div 标签中获取 item."""
    item = []
    td = div.table.tbody.tr.td
    table = td.find_all('table', recursive=False)[1]
    td = table.tbody.tr.find_all('td', recursive=False)[1]

    if len(td.find_all('div', recursive=False))>2:
         item.append(td.find_all('div', recursive=False)[2]
                    .strong.text.strip())
    else:
         item.append(td.div.strong.text.strip())  # title
    item = item[0].split()
    trs = td.table.tbody.find_all('tr', recursive=False)
    item.append(tuple([td.find('strong').text.strip()
                       for td in trs[0].find_all('td')]))  # ID
    for i in range(1, len(trs)):
        item.append(tuple([trs[i].find('th').text.strip()]
                          + [td.text.strip() for td in trs[i].find_all('td')]))
    item.append(('推荐目录颁布年份', notice[0:4]))
    item.append(('推荐目录颁布批次', notice[4:]))
    return item


def _get_item_middle(div,notice):
    """从中间（新发布车型和变更扩展车型交界处）的 div 标签中获取 item."""
    item = []
    table = div.find_all('table', recursive=False)[1]
    table = table.tbody.tr.td.find_all('table', recursive=False)[1]
    td = table.tbody.tr.find_all('td', recursive=False)[1]
    item.append(td.find_all('div', recursive=False)[2]
                .strong.text.strip())  # title
    item = item[0].split()
    trs = td.table.tbody.find_all('tr', recursive=False)
    item.append(tuple([td.find('strong').text.strip()
                       for td in trs[0].find_all('td')]))  # ID
    for i in range(1, len(trs)):
        item.append(tuple([trs[i].find('th').text.strip()]
                          + [td.text.strip() for td in trs[i].find_all('td')]))
    item.append(('推荐目录颁布年份', notice[0:4]))
    item.append(('推荐目录颁布批次', notice[4:]))
    return item


def get_contents(notice):
    """获取 notice 批次的全部车辆信息。

    Parameters
    ----------
    notice : int or string
        新能源汽车推广应用推荐车型目录批次。

    Returns
    -------
    content0, content1 :
        content0 和 content1 分别记录新发布车型和变更扩展车型的车辆信息。

    Examples
    --------
    >>> contents = get_contents(201802)  # contents = get_contents('201802')
    """
    r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}.html'
                     .format(notice))
    if r.status_code!=200:
        r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}.htm'
                         .format(notice))
    if r.status_code!=200:
        r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}X.html'
                         .format(notice))
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.body.find_all('div', recursive=False)
    divs = [div.find('div', id='divContent') for div in divs]

    i, content0, content1 = 1, [_get_item_first(divs[0],notice)], []
    while i < len(divs):
        content0.append(_get_item(divs[i],notice))
        if len(divs[i].find_all('table', recursive=False)) > 1:
            content1.append(_get_item_middle(divs[i],notice))
            i += 1
            break
        i += 1
    while i < len(divs):
        content1.append(_get_item(divs[i],notice))
        i += 1

    return (content0, content1)


def _convert_item(item):
    """将 item 由 list 转化为 dict."""
    if '、' in item[0]:
        a=item[0].index('、')
        item[0]=item[0][a+1:]
    item[0] = ('企业', item[0])
    item[1] = ('品牌', item[1])
    for i in range(0, len(item[2])):
        if item[2][i] == '纯' or item[2][i] == '插' or item[2][i] == '混' or item[2][i] == '燃' or item[2][i] == '甲':
            item.append(('类型', item[2][i:]))
            item[2] = ('产品型号', item[2][0:i])
            break
    a=3
    if type(item[3])==str:
        item[3] ,a= ('变更扩展记录', item[3]),4
    for i in range(a, len(item)-3):
            item[i] = (item[i][0][:-1], ', '.join(item[i][1:]))
    return dict(item)


def _contents_to_df(data):
    """将 contents 转化为 pandas.DataFrame."""
    df = pd.DataFrame(data)
    return df.set_index('企业')


def crawl(data, csv_filename):
    df = _contents_to_df(data)
    df.to_csv('evpromot1/'+csv_filename)
    df.to_excel('evpromot1/'+csv_filename[:-4]+'.xlsx')

def submit_to_mysql(csv_filename):
    engine = create_engine("mysql+pymysql://likai:2017422100@rm-2ze86u1j19c151g4dmo.mysql.rds.aliyuncs.com:3306/lk_test?charset=utf8")
    data = pd.read_csv('evpromot/'+csv_filename, encoding='utf8').astype(str)
    data=data.replace(to_replace=re.compile(r'.*nan.*'), value='')
    for i in range(0, len(data.columns)):
        data.rename(columns={data.columns[i]: data.columns[i].replace('（', '(').replace('）', ')')}, inplace=True)
    for i in range(0, len(data.columns)):
        data.rename(columns={data.columns[i]: data.columns[i]+'_X'}, inplace=True)
    #tablename_evpromot = 'tablename_evpromot'
    #tablename_test='cxml'
    data.to_sql(name='tablename_evpromot', con=engine, if_exists='append', index=False, index_label=False)

def batch_updata_new(batch):
    if batch[4:]=='12':
        batch_new=str(int(batch[:4]+'01')+100)
    else:
        batch_new=str(int(batch)+1)
    return batch_new

def find_new_batch(batch_updata):
    r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}.html'
                     .format(batch_updata))
    if r.status_code != 200:
        r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}.htm'
                         .format(batch_updata))
    if r.status_code != 200:
        r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}X.html'
                         .format(batch_updata))
    if r.status_code == 200:
        done=False
    else:
        done=True
    return done

def main(batch_updata):
    sie.email_main(batch_updata+'更新')
    contents = get_contents(batch_updata)
    data=list(map(_convert_item, contents[0] + contents[1]))
    crawl(data,batch_updata+'.csv')
    submit_to_mysql(batch_updata+'.csv')

if __name__ == '__main__':
    batch_updata='201703'
    while int(batch_updata)<201809:
        contents = get_contents(batch_updata)
        data=list(map(_convert_item, contents[0] + contents[1]))
        crawl(data,batch_updata+'.csv')
        #submit_to_mysql(csv_filename)
        batch_updata=batch_updata_new(batch_updata)
