# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 23:08:15 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
import re

# import package for upload data to mysql
import pymysql
from sqlalchemy import *
import send_email_attachment as sea

# database setting

user_SQL = 'likai'
pass_SQL = '2017422100'
host = 'rm-2ze86u1j19c151g4dmo.mysql.rds.aliyuncs.com:3306/'
database = 'lk_test'

tablename_fuel = 'scw'       # 公告


SQLengine = 'mysql+pymysql://' + user_SQL + ':' + pass_SQL + '@'+ host + database + '?charset=utf8'

engine = create_engine(SQLengine,echo=True)

df=pd.read_csv('fuel.csv',encoding='gbk',low_memory=False).astype(str)
df=df.replace(to_replace=re.compile(r'.*nan.*'), value='')
for i in range(0, len(df.columns)):
             df.rename(columns={df.columns[i]: df.columns[i]+'_F'}, inplace=True)
df.to_sql(name = 'fuel',con = engine,if_exists = 'replace',index = False,index_label = False)
