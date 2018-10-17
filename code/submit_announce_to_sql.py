import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import time
import re

def submit_main(filename,tablename):

     engine = create_engine("mysql+pymysql://likai:2017422100@rm-2ze86u1j19c151g4dmo.mysql.rds.aliyuncs.com:3306/lk_test?charset=utf8")
     data=pd.read_csv(filename,encoding='gbk').astype(str)
     data=data.replace(to_replace=re.compile(r'.*nan.*'), value='')
     for i in range(0,len(data.columns)):
             data.rename(columns={data.columns[i]: data.columns[i].replace('（', '(')}, inplace=True)
             data.rename(columns={data.columns[i]: data.columns[i].replace('）', ')')}, inplace=True)
     for i in range(0,len(data)):
              data['轮距(前/后)mm'][i]=data['轮距(前/后)mm'][i][0:data['轮距(前/后)mm'][i].index('\r')] + '/' + data['轮距(前/后)mm'][i][data['轮距(前/后)mm'][i].index('后'):]

     long,wide,high=[],[],[]
     for i in range(0,len(data)):
              detail=data['外形尺寸(mm)'][i]
              long.append(detail[0:detail.index('宽')].split('：')[1].split(',')[0].replace(' ','').replace('-',''))
              wide.append(detail[detail.index('宽'):detail.index('高')].split('：')[1].split(',')[0].replace(' ','').replace('-',''))
              high.append(detail[detail.index('高'):].split('：')[1].split(',')[0].replace(' ','').replace('-',''))
     data['整车长'],data['整车宽'],data['整车高'] = long,wide,high
     long,wide,high=[],[],[]
     for i in range(0,len(data)):
           detail=data['货箱栏板内尺寸(mm)'][i]
           long.append(detail[0:detail.index('宽')].split('：')[1].split(',')[0].replace(' ','').replace('-',''))
           wide.append(detail[detail.index('宽'):detail.index('高')].split('：')[1].split(',')[0].replace(' ','').replace('-',''))
           high.append(detail[detail.index('高'):].split('：')[1].split(',')[0].replace(' ','').replace('-',''))
     data['货厢长'],data['货厢宽'],data['货厢高'] = long,wide,high

     df=pd.DataFrame(data[ '轮距(前/后)mm'].str.split('/',1).tolist(),columns=['前轮距', '后轮距'])
     for  i in range(0,len(df.columns)):
            for j in range(0,len(df)):
                df[df.columns[i]][j]=re.split(':|,|/',df[df.columns[i]][j])[1].replace('-','').replace(' ','')
     data= pd.concat([data, df], axis=1, join='inner')
     data.to_sql(name = tablename,con = engine,if_exists = 'append',index = False,index_label = False)