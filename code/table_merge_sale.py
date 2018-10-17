# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 11:33:09 2018

@author: Jason
"""

import pandas as pd
import re

df1=pd.read_csv('sales/sales_ev_par.csv')
df=pd.read_csv('sales/sales_ev.csv')
df2=pd.read_csv('worktable/table_merge_ev_cut_change.csv')

content=[]
columns=list(df1.columns)+list(df2.columns)
models=list(set(df1['车型'].values))
for model in models:
    df11=df1[(df1['车型']==model)&(df1['整备质量'].notna())]
    #df2[(df2['整车长_G_Max']==df11.iloc[1]['长度(mm)'])&(df2['整车宽_G_Max']==df11.iloc[1]['宽度(mm)'])&(df2['整车高_G_Max']==df11.iloc[1]['高度(mm)'])&((df2['最高车速(km/h)_G_Max']==df11.iloc[0]['最高车速']))]
    for i in range(0,len(df11)):
        df3=df2[(df2['整车长_G_Max']==df11.iloc[i]['长度(mm)'])&
                (df2['整车宽_G_Max']==df11.iloc[i]['宽度(mm)'])&
                (df2['整车高_G_Max']==df11.iloc[i]['高度(mm)'])&
                (df2['整备质量(kg)_G_Max']==max([float(x) for x in re.findall(r'\d+?\d*',df11.iloc[i]['整备质量'])]))&
                (df2['轴距(mm)_G_Max']==df11.iloc[i]['轴距(mm)'])]
        for j in range(0,len(df3)):
            content.append(list(df11.iloc[i].values)+list(df3.iloc[j].values))
df=pd.DataFrame(content,columns=columns)
df.set_index('车型').to_csv('worktable/get_sale_model.csv')
            