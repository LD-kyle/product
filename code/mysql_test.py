# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 17:38:48 2018

@author: Administrator
"""

import numpy as np
import pandas as pd

# import package for upload data to mysql
import pymysql
from sqlalchemy import *
from sqlalchemy.types import NVARCHAR
import re

#key_id=[]
#for i in range(0,len(df)):
    #s=df.loc[i,['推荐目录颁布年份_X','推荐目录颁布批次_X']]
    #key_id.append(int('{}{:02d}{}'.format(s[0],int(s[1]),i+1)))
#df['ID']=[i for i in range(0,len(df))]
#df['ID']=key_id

# database setting

user_SQL = 'likai'
pass_SQL = '2017422100'
host = 'rm-2ze86u1j19c151g4dmo.mysql.rds.aliyuncs.com:3306/'
database = 'lk_test'
tablename = 'key_test'       # 公告
SQLengine = 'mysql+pymysql://' + user_SQL + ':' + pass_SQL + '@'+ host + database + '?charset=utf8'
engine = create_engine(SQLengine,echo=True)
df=df.replace(to_replace=re.compile(r'.*nan.*'), value='')


df.to_sql(con=engine, name=tablename , if_exists='replace',index_label=False,
                    index=False,dtype={'产品型号_X': NVARCHAR(length=255),
                                       '推荐目录颁布年份_X':NVARCHAR(length=255),
                                       '推荐目录颁布批次_X': NVARCHAR(length=255)})
with engine.connect() as con:
    con.execute("ALTER TABLE `key_test` ADD index  (`产品型号_X`,`推荐目录颁布年份_X`,`推荐目录颁布批次_X`);")
#with engine.connect() as con:
    #con.execute("ALTER TABLE `key_test` MODIFY `企业_X` VARCHAR(255) CHARACTER SET utf8;")