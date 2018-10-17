import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import time
import re
from pathlib import Path

columns=['车辆型号','批次','通用名称','产品名称','动力类型','功能类型','纯电动续驶里程(km)','燃料消耗量(L/100km)','发动机排量(mL)','整车整备质量(kg)',
         '动力蓄电池组总质量(kg)','动力蓄电池组总能量(kWh)','燃料电池系统额定功率(kW)','驱动电机额定功率(kW)','备注']
engine = create_engine("mysql+pymysql://likai:2017422100@rm-2ze86u1j19c151g4dmo.mysql.rds.aliyuncs.com:3306/lk_test?charset=utf8")
tablename='tablename_taxfree'
table_batch=[20]
for x in table_batch:
   df=pd.read_excel(str(Path('taxfree').joinpath('{}.xlsx'.format(x))),dtype=str)
   df=df.drop(columns=['Unnamed: 1'])
   df=df.replace(to_replace=re.compile(r'.*nan.*'), value='')
   a=[]
   for i in range(0,len(df[df.columns[0]])):
        if df[df.columns[0]][i]=='':
             df.iloc[i - 1]=df.iloc[i-1].add(df.iloc[i], fill_value='')
             a.append(i)
   df=df.drop(df.index[[a]])
   a,b,content0,content1='nan','nan',[],[]
   for i in range(0,len(df[df.columns[0]])):
      if '纯' in df.iloc[i][0]:
          a='纯电动汽车'
      elif '插' in df.iloc[i][0]:
          a='插电式混合动力汽车'
      elif '燃'in df.iloc[i][0]:
           a='燃料电池汽车'
      if '乘' in df.iloc[i][0]:
           b='乘用车'
      elif '客' in df.iloc[i][0]:
           b='客车'
      elif '货' in df.iloc[i][0]:
           b='货车'
      elif '专' in df.iloc[i][0]:
           b = '专用车'
      try:
           int(df.iloc[i][0])
           content0.append(a)
           content1.append(b)
      except Exception as e:
          content0.append('')
          content1.append('')
   df['动力类型']=content0
   df['功能类型']=content1
   df['批次'] = [str(x) for i in range(0, len(df[df.columns[0]]))]
   columns_ev=['车辆型号','通用名称','纯电动续驶里程(km)','整车整备质量(kg)','动力蓄电池组总质量(kg)','动力蓄电池组总能量(kWh)','备注','动力类型','功能类型','批次']
   columns_phev=['车辆型号','产品名称','纯电动续驶里程(km)','燃料消耗量(L/100km)','发动机排量(mL)','整车整备质量(kg)','动力蓄电池组总质量(kg)','动力蓄电池组总能量(kWh)','备注','动力类型','功能类型','批次']
   columns_r=['车辆型号','产品名称',	'纯电动续驶里程(km)','整车整备质量(kg)','燃料电池系统额定功率(kW)','驱动电机额定功率(kW)','备注','动力类型','功能类型','批次']
   data_ev=df.loc[df['动力类型'] == '纯电动汽车']
   data_ev=data_ev.drop(columns=[data_ev.columns[0],data_ev.columns[8],data_ev.columns[9]])
   for i in range(0,len(data_ev.columns)):
            data_ev.rename(columns={data_ev.columns[i]: columns_ev[i]+'_M'}, inplace=True)
   data_ev.to_sql(name=tablename, con=engine, if_exists='append', index=False, index_label=False)

   data_phev=df.loc[df['动力类型'] == '插电式混合动力汽车']
   data_phev=data_phev.drop(columns=[data_phev.columns[0]])
   for i in range(0,len(data_phev.columns)):
          data_phev.rename(columns={data_phev.columns[i]: columns_phev[i]+'_M'}, inplace=True)
   data_phev.to_sql(name=tablename, con=engine, if_exists='append', index=False, index_label=False)

   data_r=df.loc[df['动力类型'] == '燃料电池汽车']
   data_r=data_r.drop(columns=[data_r.columns[0],data_r.columns[8],data_r.columns[9]])
   for i in range(0,len(data_r.columns)):
          data_r.rename(columns={data_r.columns[i]: columns_r[i]+'_M'}, inplace=True)
   data_r.to_sql(name=tablename, con=engine, if_exists='append', index=False, index_label=False)

