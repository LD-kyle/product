# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 13:57:48 2018

@author: Administrator
"""

import crawler_announce_update as cau
import crawler_cxml as cc
import mysql_demo_1 as md1
import table_merge_cut as tmc
import send_email_attachment as sea
import table_merge_cut_change1 as tmcc
import  read_sql_file as rdsf
import table_merge_cxml_update as tmcu
import table_merge_cut_change1_prompt as tmccp
import table_merge_calculate as anncal
import table_merge_calculate_prompt as procal
import table_select_column_slim as tscs
import table_select_column_slim_prompt as tscsp

import requests
from bs4 import BeautifulSoup
import time


def main(file):
    done=True 
    while done:
       try:
         md1.main()
         done=False
       except Exception as e:
           print(e)
    done=True 
    while done:
       try:
         rdsf.main()
         done=False
       except Exception as e: 
           print(e)
    done=True 
    while done:
       try:
         tmc.main()
         tmcc.main()
         anncal.main()
         tscs.main()
         done=False
       except Exception as e: 
           print(e)
    done=True 
    while done:
       try:
         tmcu.main()
         tmccp.main()
         procal.main()
         tscsp.main()
         done=False
       except Exception as e: 
           print(e)
    
    done=True
    while done:
       try:
         sea.main(['worktable/table_merge_ev_cut_change.xlsx',
              'worktable/table_merge_phev_cut_change.xlsx',
              'worktable/table_merge_ke_ev_cut_change.xlsx',
              'worktable/table_merge_ke_hev_cut_change.xlsx',file,
              'worktable/table_merge_ev_cut_change_cal.xlsx',
              'worktable/table_evpromot_announce_taxfree_merge_change.xlsx',
              'worktable/table_evpromot_announce_taxfree_merge_change_cal.xlsx',
              'worktable/table_merge_phev_cut_change_slim.xlsx',
              'worktable/table_merge_ev_cut_change_cal_slim.xlsx',
              'worktable/table_evpromot_announce_taxfree_merge_change_cal_slim_ev.xlsx',
              'worktable/table_evpromot_announce_taxfree_merge_change_cal_slim_phev.xlsx'])
         done=False
       except Exception as e:
           time.sleep(60)
          

if __name__=='__main__':
    main('announce/313.csv')



