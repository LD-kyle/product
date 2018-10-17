# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:59:55 2018

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
    
def get_announcement_batch(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    strong=soup.body.h1.strong
    announcement_batch=strong.text[1:4]
    return announcement_batch
    
def find_new_announce(announce_batch_new):
    url = 'http://data.miit.gov.cn/resultSearch?categoryTreeId=1128'  
    if int(get_announcement_batch(url)) > int(announce_batch_new):
                announce_batch_new = get_announcement_batch(url)
                done= False
    else:
        done=True
        print('no new')
    return done, announce_batch_new 

def find_new_evpromot(batch_updata):
    r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}.html'
                     .format(batch_updata))
    if r.status_code != 200:
        r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}.htm'
                         .format(batch_updata))
    if r.status_code != 200:
        r = requests.get('http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/{}X.html'
                         .format(batch_updata))
    if r.status_code == 200:
        done=False
    else:
        done=True
    return done
def evpromot_updata_new(batch):
    if batch[4:5]=='12':
        batch_new=str(int(batch[:4]+'01')+100)
    else:
        batch_new=str(int(batch)+1)
    return batch_new
    
if __name__ == '__main__':
   announce_batch_new,evpromot='311','201810'
   while True:
        while find_new_announce(announce_batch_new)[0]&find_new_evpromot(evpromot):
            time.sleep(14400)
        if find_new_announce(announce_batch_new)[0]==False:
            announce_batch_new=find_new_announce(announce_batch_new)[1]
            cau.main(announce_batch_new)
            main('announce/'+announce_batch_new+'.csv')  
        if find_new_evpromot(evpromot)==False:
            cc.main(evpromot)     
            main('evpromot/'+evpromot+'.csv')
            evpromot=evpromot_updata_new(evpromot)
            
            
            
    
