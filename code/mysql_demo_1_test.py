# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:12:39 2018

@author: xinmei_jlu
"""

import numpy as np
import pandas as pd

# import package for upload data to mysql
import pymysql
from sqlalchemy import *



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
    

def sql_merge(condition,filename):
    data_ev= pd.read_sql_query('SELECT * FROM '+ tablename_announce+ condition,engine)
    for i in range(0, len(data_ev.columns)):
             data_ev.rename(columns={data_ev.columns[i]: data_ev.columns[i]+'_G'}, inplace=True)
    data_ev.to_sql(name = 'middle',con = engine,if_exists = 'replace',index = False,index_label = False)
    tablename_middle = 'middle'       # 公告
    common_col_middle = 'middle.产品型号_G'
    sql_dataframe_ev = pd.read_sql_query('SELECT * FROM '+ tablename_middle + ' LEFT JOIN '+ tablename_evpromot
                                  + ' on '+ common_col_middle  + ' = ' + common_col_evpromot,engine)
    sql_dataframe_ev.to_sql(name = 'middle',con = engine,if_exists = 'replace',index = False,index_label = False)
    sql_dataframe1_ev = pd.read_sql_query('SELECT * FROM '+ tablename_middle + ' LEFT JOIN '+ tablename_taxfree
                                  + ' on '+ common_col_middle + ' = ' + common_col_taxfree
                                  ,engine)
    sql_dataframe1_ev=sql_dataframe1_ev.set_index('企业名称_G')
    sql_dataframe1_ev.to_csv(filename)
    sql_dataframe1_ev.to_excel(filename[:-4]+'.xlsx')
def main():
    conditions=[' WHERE (产品名称 LIKE "%%乘用车%%" or 产品名称 LIKE "%%轿车%%") and (产品名称 LIKE "%%纯电动%%")',
                ' WHERE (产品名称 LIKE "%%乘用车%%" or 产品名称 LIKE "%%轿车%%") and (产品名称 LIKE "%%插电式%%"  and 产品名称 NOT LIKE "%%非%%")',
                ' WHERE 产品名称 LIKE "%%纯电动%%" and 产品名称 LIKE "%%客车%%"',
                ' WHERE 产品名称 LIKE "%%混合动力%%" and 产品名称 LIKE "%%客车%%"']
    filenames=['table_merge_ev.csv','table_merge_phev.csv','table_merge_ke_ev.csv','table_merge_ke_hev.csv']
    for i in range(0,4):
        sql_merge(conditions[i],'worktable/'+filenames[i])
if __name__ == '__main__':
    main()
  

  
    