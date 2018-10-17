# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 22:38:12 2018

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

#查询型号输入
num= '\"%%BYD6460%%\"'
char_num_pro=' WHERE 产品型号_X LIKE '+num
char_num_tax=' WHERE 车辆型号_M LIKE '+num
char_num_ann=' WHERE 产品型号 LIKE '+num


df_evpromot= pd.read_sql_query('SELECT * FROM '+ tablename_evpromot + char_num_pro,engine).set_index('企业_X')
#df_evpromot.to_csv('tablename_evpromot_num.csv')
df_taxfree= pd.read_sql_query('SELECT * FROM '+tablename_taxfree + char_num_tax,engine).set_index('车辆型号_M')
#df_taxfree.to_csv('tablename_taxfree_num.csv')
df_announce= pd.read_sql_query('SELECT * FROM '+ tablename_announce+ char_num_ann,engine).set_index('企业名称')
#df_announce.to_csv('tablename_announce_num.csv')