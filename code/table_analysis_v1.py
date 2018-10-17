 # -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 11:38:17 2018

@author: Administrator
"""

import pandas as pd


columns_prompt_ev=['企业_X',
    '品牌_X',
    '类型_X',
    '产品型号_X',
    '变更扩展记录_X',
    '推荐目录颁布年份_X',
    '推荐目录颁布批次_X',
    '外廓尺寸长(mm)_X_Max',
    '整备质量(kg)_X_Max',
    '储能装置种类_X',
    '电池系统能量密度(Wh/kg)_X_Max',
    '工况条件下百公里耗电量(Y)(kWh/100km)_X_Min',
    '发动机型号_X',
    '发动机生产企业_X',
    '排量/功率(ml/kW)_X',
    '驱动电机峰值功率/转速/转矩(kW /r/min/N.m)_X',
    '驱动电机类型_X',
    '最高车速(km/h)_X_Max',
    '纯电动模式下续驶里程(km，工况法)_X',
    '纯电动模式下续驶里程(km，等速法)_X',
    '续驶里程(km，工况法)_X_Max',
    '最大电机总功率_X',
    '电机单_多_X',
    '电机最大转速_X',
    '电机最大转矩_X',
    '整车厂企业简称_X']

#表头转置成列
#'企业_X'
#'品牌_X'
#'类型_X'
#'产品型号_X'
#'变更扩展记录_X'
#'推荐目录颁布年份_X'
#'推荐目录颁布批次_X'
#'外廓尺寸宽(mm)_X'
#'外廓尺寸长(mm)_X'
#'外廓尺寸高(mm)_X'
#'总质量(kg)_X'
#'整备质量(kg)_X'
#'储能装置总储电量(kWh)_X'
#'储能装置种类_X'
#'电池系统总质量占整车整备质量比例(%)_X'
#'电池系统能量密度(Wh/kg)_X'
#'快充倍率_X'
#'工况条件下百公里耗电量(Y)(kWh/100km)_X'
#'是否允许外接充电_X'
#'发动机型号_X'
#'发动机生产企业_X'
#'排量/功率(ml/kW)_X'
#'燃料消耗量(L/100km，B状态)_X'
#'燃料消耗量(L/100km，电量平衡运行阶段)_X'
#'燃料电池系统峰值功率(kW)_X'
#'燃料电池系统生产企业(主要包含电堆)_X'
#'燃料电池系统额定功率(kW)_X'
#'燃料种类_X'
#'驱动电机峰值功率/转速/转矩(kW /r/min/N.m)_X'
#'驱动电机类型_X'
#'最高车速(km/h)_X'
#'纯电动模式下续驶里程(km，工况法)_X'
#'纯电动模式下续驶里程(km，等速法)_X'
#'续驶里程(km，工况法)_X'
#'续驶里程(km，等速法)_X'
#'节油率水平(%)_X'
#'Ekg单位载质量能量消耗量(Wh/km·kg)_X'
#'30分钟最高车速(km/h)_X'
#'吨百公里电耗(kWh/t·100km)_X'
#'车辆基本信_X'
#外廓尺寸宽(mm)_X_Max
#外廓尺寸长(mm)_X_Max
#外廓尺寸高(mm)_X_Max
#总质量(kg)_X_Max
#整备质量(kg)_X_Max
#储能装置总储电量(kWh)_X_Max
#电池系统能量密度(Wh/kg)_X_Max
#快充倍率_X_Max
#工况条件下百公里耗电量(Y)(kWh/100km)_X_Max
#最高车速(km/h)_X_Max
#续驶里程(km，工况法)_X_Max
#30分钟最高车速(km/h)_X_Max
#燃料消耗量(L/100km，B状态)_X_Max
#工况条件下百公里耗电量(Y)(kWh/100km)_X_Min
#最大电机总功率_X
#电机单_多_X
#电机最大转速_X
#电机最大转矩_X
#整车厂企业简称_X

               

      
if __name__ == '__main__':
    
  
    #filename=filenames[0]
    filename='table_evpromot_change.csv'
    df=pd.read_csv(filename)
    df=df[columns_prompt_ev]
    df=df[(df['类型_X'].str.contains('纯电动'))&(df['类型_X'].str.contains('轿车')|df['类型_X'].str.contains('乘用车'))]
    df.set_index('企业_X').to_excel(filename[:-4]+'_select.xlsx')

    
  



