# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 15:52:50 2018

@author: Jason
"""

from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import send_inform_email as sie


def get_page_detail(wd):
    detail=[]
    trs=wd.find_elements_by_xpath("//tbody[@id='123']/tr")
    for tr in trs:
        detail.append([tr.find_elements_by_xpath("td")[i].text  for i in range(1,13)]+
                      [tr.find_elements_by_xpath("td[@style='display:none']")[i].get_attribute("textContent").replace('\xa0','')  
                      for i in range(2,8)])
        
    return detail

def main(url):
    wd = webdriver.Chrome()
    header=['生产企业','通用名称','车辆型号','车辆种类','排量(ml)','额定功率(KW)',
            '变速器类型','市区工况(L/100km)','市郊工况(L/100km)','综合工况(L/100km)',
            '通稿日期','备注','燃料类型','驱动型式','备案号','发动机型号','整车整备质量',
            '最大设计总质量']
    wd.get(url)
    content=get_page_detail(wd)
    i=1
    while i<4665:
         done=True
         wait = WebDriverWait(wd, 20)
         element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/table[2]/tbody/tr/td/table[2]/tbody/tr/td[2]/a[3]")))
         element.click()
         time.sleep(1)
         while done:
           try: 
              newpage=get_page_detail(wd)
              content=content+newpage
              done=False
              i+=1
           except Exception as e:
              time.sleep(1)
              print(e,i)
    df=pd.DataFrame(content,columns=header).set_index('生产企业')
    df.to_csv('announce/fuel.csv')
    df.to_excel('announce/fuel.xlsx')
    
if __name__=='__main__':
       url='http://chaxun.miit.gov.cn/asopCmsSearch/n2257/n2280/index.html'
       main(url)
       sie.email_main('fuel_finish')