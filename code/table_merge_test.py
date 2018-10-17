# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 16:24:07 2018

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
    md1.main()
    rdsf.main()
    tmc.main()
    tmcc.main()
    anncal.main()
    tscs.main()
    tmcu.main()
    tmccp.main()
    procal.main()
    tscsp.main()
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
if __name__=='__main__':
    main()