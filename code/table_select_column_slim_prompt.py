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

columns_select_phev=['企业_X','品牌_X','产品型号_X','产品名称_M','类型_X','推荐目录颁布年份_X','推荐目录颁布批次_X','公告批次_G','变更(扩展)记录_G','批次_M',
                '整备质量(kg)_X','轮胎规格_G','工况条件下百公里耗电量(Y)(kWh/100km)_X',
                '燃料消耗量(L/100km，B状态)_X','驱动电机峰值功率/转速/转矩(kW /r/min/N.m)_X',
                '最高车速(km/h)_X','纯电动模式下续驶里程(km，工况法)_X',
                '节油率水平(%)_X','动力蓄电池组总能量(kWh)_M',
                '外廓尺寸长(mm)_X_Max','整备质量(kg)_X_Max',
                '纯电动模式下续驶里程(km，工况法)_X_Max',
                '燃料消耗量(L/100km，B状态)_X_Min','工况条件下百公里耗电量(Y)(kWh/100km)_X_Min',
                '能耗/门槛','B状态油耗/国标限值',
                '最大电机总功率_X','电机单_多_X','电池供应商_G']

columns_select_ev=['企业_X','品牌_X','产品型号_X','通用名称_M','类型_X','推荐目录颁布年份_X','推荐目录颁布批次_X','公告批次_G','变更(扩展)记录_G','批次_M',
                '整备质量(kg)_X','轮胎规格_G','电池系统能量密度(Wh/kg)_X','工况条件下百公里耗电量(Y)(kWh/100km)_X',
                '驱动电机峰值功率/转速/转矩(kW /r/min/N.m)_X',
                '最高车速(km/h)_X','续驶里程(km，工况法)_X',
                '动力蓄电池组总能量(kWh)_M',
                '外廓尺寸长(mm)_X_Max','整备质量(kg)_X_Max',
                '续驶里程(km，工况法)_X_Max','电池系统能量密度(Wh/kg)_X_Max','动力蓄电池组总能量(kWh)_M_Max',
                '工况条件下百公里耗电量(Y)(kWh/100km)_X_Min','最大电机总功率_X','电机单_多_X','电池供应商_G','电机供应商1_G','1.1倍能效要求（kWh/100公里）',
                '1.1达标','更高能效要求（kWh/100公里）','高级达标','能耗/门槛']
 
        





def main():
  
      #读取纯电动乘用车数据
      filename='worktable/table_evpromot_announce_taxfree_merge_change_cal.csv'
      df=pd.read_csv(filename)
      df=df[columns_select_ev]#ev
      df.rename(columns={'批次_M': '免购置税目录批次_M'}, inplace=True)
      df.rename(columns={'电机供应商1_G': '电机供应商_G'}, inplace=True)
      df=df[(df['类型_X'].str.contains('纯电动'))&(df['类型_X'].str.contains('轿车')|df['类型_X'].str.contains('乘用车'))]
      df.set_index('企业_X').to_csv(filename[:-4]+'_slim_ev.csv')
      df.set_index('企业_X').to_excel(filename[:-4]+'_slim_ev.xlsx')
 
      #读取PHEV乘用车数据
      df=pd.read_csv(filename)
      df=df[columns_select_phev]#phev
      df.rename(columns={'批次_M': '免购置税目录批次_M'}, inplace=True)
#      df.rename(columns={'电机供应商1_G': '电机供应商_G'}, inplace=True)
      df=df[(df['类型_X'].str.contains('插电'))&(df['类型_X'].str.contains('轿车')|df['类型_X'].str.contains('乘用车'))]#phev
      df.set_index('企业_X').to_csv(filename[:-4]+'_slim_phev.csv') #phev
      df.set_index('企业_X').to_excel(filename[:-4]+'_slim_phev.xlsx')  #phev   
 
      
      
if __name__ == '__main__':
    main()
  



