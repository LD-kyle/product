# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:27:03 2018

@author: Administrator
"""

import numpy as np
import pandas as pd

# import package for upload data to mysql
import pymysql
from sqlalchemy import *
#import send_email_attachment as sea

# database setting

user_SQL = 'likai'
pass_SQL = '2017422100'
host = 'rm-2ze86u1j19c151g4dmo.mysql.rds.aliyuncs.com:3306/'
database = 'lk_test'

tablename_announce = 'scw'       # 公告
common_col_announce = 'scw.产品型号'
tablename_evpromot = 'tablename_evpromot'       # 新能源汽车推广应用推荐车型目录
common_col_evpromot = 'tablename_evpromot.产品型号_X'
tablename_taxfree = 'tablename_taxfree'        # 新能源汽车免征购置税目录
common_col_taxfree ='tablename_taxfree.车辆型号_M'

SQLengine = 'mysql+pymysql://' + user_SQL + ':' + pass_SQL + '@'+ host + database + '?charset=utf8'

engine = create_engine(SQLengine,echo=True)


def batch_updata_new(batch):
    if batch[4:]=='12':
        batch_new=str(int(batch[:4]+'01')+100)
    else:
        batch_new=str(int(batch)+1)
    return batch_new
def main():
    batch='201703'
    while int(batch)<201804:
         a=batch[:4]
         b=str(int(batch[4:]))
         df=pd.read_sql_query('SELECT * FROM '+ tablename_evpromot+' WHERE 推荐目录颁布年份_X = "'+a+'" and 推荐目录颁布批次_X = "'+b+'"'
                                  ,engine).set_index('企业_X')
         df.to_csv('evpromot/'+batch+'.csv')
         batch=batch_updata_new(batch)
   
main()


























