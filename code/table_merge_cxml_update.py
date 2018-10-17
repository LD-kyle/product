# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 12:05:32 2018

@author: Administrator
"""

import pandas as pd


['推荐目录颁布年份_X','推荐目录颁布批次_X','产品型号_X','产品型号_G',
 '公告批次_G','车辆型号_M','批次_M']


dict0={'201701':[292,1],'201702':[293,2],'201703':[294,3],'201704':[295,4],'201705':[296,5],
          '201706':[297,6],'201707':[298,7],'201708':[299,8],'201709':[300,9],'201710':[301,10],
          '201711':[302,11],'201712':[303,12],'201801':[304,13],'201802':[305,14],'201803':[306,15],
          '201804':[307,16],'201805':[307,17],'201806':[308,18],'201807':[309,19],'201808':[310,20],'201809':[311,21]}


def find_line(df_cxml,df_merge,s,column0,column1,x,limit):
    
    batch=dict0['{}{:02d}'.format(s[1],s[2])][x]
    df=df_merge[df_merge[column0]==batch]
    df=df[df[column1]==s[0]]
    while (df.empty)&(batch>limit):
            batch-=1
            df=df_merge[df_merge[column0]==batch]
            df=df[df[column1]==s[0]]
    if len(df)>=1:#修正了bug20180805，原来是==1；应该是>=1,可能出现有该车型标号的多个行，如果没有多个行才赋空字符；==1的话出现多个行就会赋空字符。
            list0=list(df.iloc[0].values)
    else:
            list0=['' for i in range(0,len(df.columns))]
    return list0


def find_line_tax(df_cxml,df_merge,s,column0,column1,x,limit_low,limit_up):
    
    batch=dict0['{}{:02d}'.format(s[1],s[2])][x]
    df=df_merge[df_merge[column0]==batch]
    df=df[df[column1]==s[0]]
    a,b=batch,batch
    while (df.empty)&(a<limit_up):
            a+=1
            df=df_merge[df_merge[column0]==a]
            df=df[df[column1]==s[0]]
    while (df.empty)&(b>limit_low):
            b-=1
            df=df_merge[df_merge[column0]==b]
            df=df[df[column1]==s[0]]
    if len(df)>=1:#修正了bug20180805，原来是==1；应该是>=1,可能出现有该车型标号的多个行，如果没有多个行才赋空字符；==1的话出现多个行就会赋空字符。v
            list0=list(df.iloc[0].values)
    else:
            list0=['' for i in range(0,len(df.columns))]
    return list0


def get_df_add(df_cxml,df,column0,column1,x,limit):
    content=[]
    for i in range(0,len(df_cxml)):
        s=df_cxml.loc[i,['产品型号_X','推荐目录颁布年份_X','推荐目录颁布批次_X']]
        content.append(find_line(df_cxml,df,s,column0,column1,x,limit))
    df_add=pd.DataFrame(content,columns=df.columns)
    return df_add
    
def get_df_add_tax(df_cxml,df,column0,column1,x,limit_low,limit_up):
    content=[]
    for i in range(0,len(df_cxml)):
        s=df_cxml.loc[i,['产品型号_X','推荐目录颁布年份_X','推荐目录颁布批次_X']]
        content.append(find_line_tax(df_cxml,df,s,column0,column1,x,limit_low,limit_up))
    df_add=pd.DataFrame(content,columns=df.columns)
    return df_add

def main():
    df_cxml,df_scw=pd.read_csv('worktable/table_evpromot_nep.csv'),pd.read_csv('worktable/table_announce_nep.csv')
    df_ms=pd.read_csv('worktable/tablename_taxfree.csv')
    df_add1=get_df_add(df_cxml,df_scw,'公告批次_G','产品型号_G',0,0)
    df_add2=get_df_add_tax(df_cxml,df_ms,'批次_M','车辆型号_M',1,0,20)
    df = pd.concat([df_cxml, df_add1,df_add2], axis=1)
    df.set_index('企业_X').to_csv('worktable/table_evpromot_announce_taxfree_merge.csv')
    df.set_index('企业_X').to_excel('worktable/table_evpromot_announce_taxfree_merge.xlsx')   
if __name__=='__main__':
    main()
    
            
     