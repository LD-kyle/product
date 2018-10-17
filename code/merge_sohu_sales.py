# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 13:11:49 2018

@author: Administrator
"""

import pandas as pd
import re
import numpy as np


def main():
   df=pd.read_csv('sales/sales.csv')
   df1=pd.read_csv('sales/sales_par1.csv')
   df1=df1[df1['销售状态'].str.contains('在售')]
   columns=list(df.columns)
   columns1=['车系配置数量','最高价','最低价','平均价','级别','车体结构','车身结构',
          '长度(mm)','宽度(mm)','高度(mm)','轴距(mm)']
   content=[]
   for i in range(0,len(df)):
       list0,list1=list(df.loc[i].values),[]
       df2=df1[df1['车型']==list0[1]]
       try:
           if len(df2)==0:
              list1=['' for x in columns1]
           else:
              s=list(df2['售价'].values)
              list1.append(len(s))
              list1.append(max(s))
              list1.append(min(s))
              list1.append(np.mean(s))
              for column in columns1[4:]:
                  list1.append(df2.iloc[0][column])
       except Exception as e:
              list1=['' for x in columns1]
       content.append(list0+list1)
   df3=pd.DataFrame(content,columns=columns+columns1)
   df3.set_index('序号').to_csv('sales/sales_merge.csv')
   df3.set_index('序号').to_excel('sales/sales_merge.xlsx')
if __name__=='__main__':
    main()
            
    
    
    