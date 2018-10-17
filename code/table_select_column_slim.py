# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 11:38:17 2018

@author: Administrator
"""

import pandas as pd

#columns_select=['企业名称_G','产品型号_G','公告批次_G','产品商标_G','产品名称_G',
#                '整备质量(kg)_G','轮胎规格_G','生产地址_G','发动机企业_G','排量(ml)_G',
#                '功率(kw)_G','整车长_G','整车宽_G','整车高_G',	'推荐目录颁布年份_X',
#                '推荐目录颁布批次_X','储能装置种类_X'	,'工况条件下百公里耗电量(Y)(kWh/100km)_X',
#                '燃料消耗量(L/100km，B状态)_X','驱动电机峰值功率/转速/转矩(kW /r/min/N.m)_X',
#                '驱动电机类型_X','最高车速(km/h)_X','纯电动模式下续驶里程(km，工况法)_X',
#                '节油率水平(%)_X','批次_M','产品名称_M','纯电动续驶里程(km)_M',
#                '燃料消耗量(L/100km)_M','发动机排量(mL)_M','整车整备质量(kg)_M',
#                '动力蓄电池组总质量(kg)_M'	,'动力蓄电池组总能量(kWh)_M','整车长_G_Max',
#                '整车宽_G_Max','整车高_G_Max','最高车速(km/h)_X_Max','燃料消耗量(L/100km，B状态)_X_Max',
#                '纯电动续驶里程(km)_M_Max','燃料消耗量(L/100km)_M_Max','发动机排量(mL)_M_Max',
#                '整车整备质量(kg)_M_Max','动力蓄电池组总质量(kg)_M_Max','动力蓄电池组总能量(kWh)_M_Max',
#                '工况条件下百公里耗电量(Y)(kWh/100km)_X_Min','最大电机总功率_X','电机单_多_X',
#                '电机总功率0_X','电池供应商_G','电池种类_G']

columns_select_phev=['企业名称_G','产品型号_G','公告批次_G','变更(扩展)记录_G','产品商标_G','产品名称_G','批次_M','产品名称_M',
                '整备质量(kg)_G','轮胎规格_G',	'推荐目录颁布年份_X',
                '推荐目录颁布批次_X','工况条件下百公里耗电量(Y)(kWh/100km)_X',
                '燃料消耗量(L/100km，B状态)_X','驱动电机峰值功率/转速/转矩(kW /r/min/N.m)_X',
                '最高车速(km/h)_X','纯电动模式下续驶里程(km，工况法)_X',
                '节油率水平(%)_X','纯电动续驶里程(km)_M',
                '动力蓄电池组总能量(kWh)_M',
                '整车长_G_Max','整车整备质量(kg)_M_Max',
                '纯电动续驶里程(km)_M_Max','动力蓄电池组总能量(kWh)_M_Max',
                '燃料消耗量(L/100km，B状态)_X_Max','工况条件下百公里耗电量(Y)(kWh/100km)_X_Min','最大电机总功率_X','电机单_多_X']

columns_select_ev=['企业名称_G','产品型号_G','公告批次_G','变更(扩展)记录_G','产品商标_G','产品名称_G','批次_M','通用名称_M',
                '整备质量(kg)_G','轮胎规格_G','推荐目录颁布年份_X',
                '推荐目录颁布批次_X','电池系统能量密度(Wh/kg)_X','工况条件下百公里耗电量(Y)(kWh/100km)_X',
                '驱动电机峰值功率/转速/转矩(kW /r/min/N.m)_X',
                '最高车速(km/h)_X','续驶里程(km，工况法)_X',
                '动力蓄电池组总能量(kWh)_M',
                '整车长_G_Max','整备质量(kg)_G_Max',
                '续驶里程(km，工况法)_X_Max','电池系统能量密度(Wh/kg)_X_Max','动力蓄电池组总能量(kWh)_M_Max',
                '工况条件下百公里耗电量(Y)(kWh/100km)_X_Min','最大电机总功率_X','电机单_多_X','电池供应商_G','电机供应商1_G','1.1倍能效要求（kWh/100公里）',
                '1.1达标','更高能效要求（kWh/100公里）','高级达标','能耗/门槛']
 
columns_select=[columns_select_phev,columns_select_ev]               


#filenames=['table_merge_ev_cut_change.csv','table_merge_ke_ev_cut_change.csv',
#      'table_merge_phev_cut_change.csv','table_merge_ke_hev_cut_change.csv']

filenames=['worktable/table_merge_phev_cut_change.csv','worktable/table_merge_ev_cut_change_cal.csv']


def main():
  
  i=0
  for filename in filenames:
      df=pd.read_csv(filename)
      df=df[columns_select[i]]
      df.rename(columns={'批次_M': '免购置税目录批次_M'}, inplace=True)
      df.set_index('企业名称_G').to_csv(filename[:-4]+'_slim.csv')
      df.set_index('企业名称_G').to_excel(filename[:-4]+'_slim.xlsx')
      i+=1
      
if __name__ == '__main__':
    main()
  



