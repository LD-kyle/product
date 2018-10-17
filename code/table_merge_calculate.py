# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 18:29:28 2018

@author: Administrator
"""

import pandas as pd

def cal_ef(df,a,b,name):
    list0=[]
    for i in range(0,len(df)):
        m=df.loc[i,'整备质量(kg)_G_Max']
        if pd.isna(m):
            list0.append('')
        else:
            if m<=1000:
                y=0.0126*m+0.45
            elif (m>1000)&(m<=1600):
                y=0.0108*m+2.25
            else:
                y=0.0045*m+12.33
            list0.append(y*a*b)
    df[name]=list0
    return df

def cal_pct(df,name):
    list0=[]
    for i in range(0,len(df)):
        x=df.loc[i,'工况条件下百公里耗电量(Y)(kWh/100km)_X_Min']
        m=df.loc[i,'整备质量(kg)_G_Max']
        if pd.isna(m)|pd.isna(x):
            list0.append('')
        else:
            if m<=1000:
                y=0.0126*m+0.45
            elif (m>1000)&(m<=1600):
                y=0.0108*m+2.25
            else:
                y=0.0045*m+12.33
            list0.append(x/y)
    df[name]=list0
    return df
    
def cal_mark(df,ef_real,ef_ref,markname):
    list0=[]
    for i in range(0,len(df)):
        x=df.loc[i,ef_real]
        y=df.loc[i,ef_ref]
        if pd.isna(x)|pd.isna(y):
            list0.append('')
        else:
            if y>=x:
                list0.append(1)
            else:
                list0.append(0)
    df[markname]=list0
    return df
    



def main():
    filename='worktable/table_merge_ev_cut_change.csv'
    df=pd.read_csv(filename)
    
    #计算政策能效，添加能效列
    ef_name='1.1倍能效要求（kWh/100公里）'
    df=cal_ef(df,0.75,1.005,ef_name)
    #比较实际能效和目标能效是否达标,添加标记列；
    ef_real='工况条件下百公里耗电量(Y)(kWh/100km)_X_Min'
    markname='1.1达标'
    df=cal_mark(df,ef_real,ef_name,markname)
    
    #计算高级能效，添加能效列
    ef_name='更高能效要求（kWh/100公里）'
    df=cal_ef(df,0.7,1.005,ef_name)
    #比较实际能效和目标能效是否达标,添加标记列；
    ef_real='工况条件下百公里耗电量(Y)(kWh/100km)_X_Min'
    markname='高级达标'
    df=cal_mark(df,ef_real,ef_name,markname)
    
    #直接计算能效比
    markname='能耗/门槛'
    df=cal_pct(df,markname)
       
    
    #output csv and xlsx file.
    df.set_index('企业名称_G').to_csv('worktable/table_merge_ev_cut_change_cal.csv')
    df.set_index('企业名称_G').to_excel('worktable/table_merge_ev_cut_change_cal.xlsx')
    
if __name__=='__main__':
    main()
    
    