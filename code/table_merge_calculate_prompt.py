# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 18:29:28 2018

@author: Administrator
"""

import pandas as pd

def cal_ef(df,a,b,name):
    list0=[]
    for i in range(0,len(df)):
        m=df.loc[i,'整备质量(kg)_X_Max']
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

def cal_oilef(df,name):
    list0=[]
    for i in range(0,len(df)):
        x=df.loc[i,'燃料消耗量(L/100km，B状态)_X_Min']
        m=df.loc[i,'整备质量(kg)_X_Max']
        if pd.isna(m)|pd.isna(x):
            list0.append('')
        else:
            if m<=750:
                y=5.6
            elif (m>750)&(m<=865):
                y=5.9
            elif (m>865)&(m<=980):
                y=6.2                
            elif (m>980)&(m<=1090):
                y=6.5
            elif (m>1090)&(m<=1205):
                y=6.8
            elif (m>1205)&(m<=1320):
                y=7.2
            elif (m>1320)&(m<=1430):
                y=7.6
            elif (m>1430)&(m<=1540):
                y=8.0  
            elif (m>1540)&(m<=1660):
                y=8.4  
            elif (m>1660)&(m<=1770):
                y=8.8  
            elif (m>1770)&(m<=1880):
                y=9.2  
            elif (m>1880)&(m<=2000):
                y=9.6
            elif (m>2000)&(m<=2110):
                y=10.1
            elif (m>2110)&(m<=2280):
                y=10.6  
            elif (m>2280)&(m<=2510):
                y=11.2                      
            else:
                y=11.9
            list0.append(x/y)
    df[name]=list0
    return df

def cal_pct(df,name):
    list0=[]
    for i in range(0,len(df)):
        x=df.loc[i,'工况条件下百公里耗电量(Y)(kWh/100km)_X_Min']
        m=df.loc[i,'整备质量(kg)_X_Max']
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
        if pd.isna(x)|pd.isna(y)|(y==''):
            list0.append('')
        else:
            if y>=x:
                list0.append(1)
            else:
                list0.append(0)
    df[markname]=list0
    return df
    



def main():
    filename='worktable/table_evpromot_announce_taxfree_merge_change.csv'
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
    
    #直接计算B状态燃油目标值
    ef_name='B状态油耗/国标限值'
    df=cal_oilef(df,ef_name)   
    
    #output csv and xlsx file.
    df.set_index('企业名称_G').to_csv('worktable/table_evpromot_announce_taxfree_merge_change_cal.csv')
    df.set_index('企业名称_G').to_excel('worktable/table_evpromot_announce_taxfree_merge_change_cal.xlsx')
    
if __name__=='__main__':
    main()
    
    