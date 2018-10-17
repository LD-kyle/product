import sys
import csv
import os
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import time
import submit_announce_to_sql as sal
import send_inform_email as sie

logfilepath = 'logs/Log'

def WirteLog(logfilepath,logfilename,Log):
    if not os.path.exists(logfilepath):
            os.makedirs(logfilepath)
            print ('folder ', logfilepath, 'does not exist! It will be created')
    try:
        with open(logfilepath + logfilename,'a+') as LogFileHandler:
            LogFileHandler.writelines(time.strftime('%Y-%m-%d %H:%M:%S ') + Log + '\n')
    except IOError as err:
        print("Write Log File Error:"+str(err))

def get_detail_imgs(url,batch,img_path,update_time):
    detail = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', {'class': 'w_banner'})
    td = div.findAll('td')
    detail = detail + [td[i].text.strip() for i in range(0, 7)]
    detail = detail + [td[i].text.strip() for i in range(8, 48)]
    detail = detail + [batch,update_time]
    tmp = td[7].findAll('img')
    imgs = [img.attrs['src'] for img in tmp]
    detail=detail+download_imgs(img_path, detail[1], batch, imgs)
    return detail



def download_imgs(path, number, batch,imgs):
    url='http://data.miit.gov.cn'
    detail_img=[]
    for i in range(0, len(imgs)):
        try:
           r = requests.get(url+imgs[i])
           number=number.replace('/','_')
           filename = '{}_{}_{:02d}.jpg'.format(number,batch, i)
           detail_img.append(filename)
           with open(str(Path(path).joinpath(filename)), 'wb') as f:
              for chunk in r:
                  f.write(chunk)
        except Exception as e:
            WirteLog(logfilepath, '308.Log', url+imgs[i])

    return detail_img

def get_notice_page(soup):
    div = soup.find('div', {'id': 'page-wrapper'})
    div = div.find_all('div', recursive=False)[1]
    td = div.table.tbody.findAll('td')
    return [td[i].a.attrs['href'] for i in range(1, len(td), 5)]

def get_announcement_batch(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    strong=soup.body.h1.strong
    announcement_batch=strong.text[1:4]
    print(int(announcement_batch))
    return announcement_batch

def crawl(out_filename,img_path,batch,update_time):
    url = 'http://data.miit.gov.cn/resultSearch?categoryTreeId=1128&pagenow='
    r = requests.get(url+'1')
    soup = BeautifulSoup(r.text, 'html.parser')
    ul = soup.find('ul', {'class': 'pagination'})
    li = ul.findChildren()[-1]
    total=int(li['onclick'][8:10])
    index=[]
    for i in range(1, total+1):
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        r = requests.get(url + str(i), headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        index = index + get_notice_page(soup)
    column0 = []
    column1=['公告批次','发布时间']
    for i in range(0,10):
        column1.append('图片'+str(i))
    url = 'http://data.miit.gov.cn'
    r = requests.get(url+index[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', {'class': 'w_banner'})
    th = div.findAll('th')
    column0 = column0 + [th[i].text.strip()[:-1] for i in range(0, 37)]
    column0 = column0 + [th[i].text.strip() for i in range(37, 47)]
    column0=column0+column1
    with open(str(Path('announce').joinpath(out_filename)), 'w', newline='') as csvfile:
        detail_wirter = csv.writer(csvfile, dialect=csv.excel())
        detail_wirter.writerow(column0)
        for x in index:
            try:
                detail = get_detail_imgs(url + x,batch,img_path,update_time)
                detail_wirter.writerow(detail)
            except Exception as e:
                print(x, e)
    
def main(announcemen_batch_new):
    url = 'http://data.miit.gov.cn/resultSearch?categoryTreeId=1128'
    sie.email_main(announcemen_batch_new+'批次更新')
    img_path =r'announce\img{}'.format(announcemen_batch_new)
    if not os.path.exists(img_path):
            os.makedirs(img_path)
            print('folder ', img_path, 'does not exist! It will be created')
    crawl(announcemen_batch_new+'.csv',img_path,announcemen_batch_new,time.strftime('%Y-%m-%d '))
    sal.submit_main(str(Path('announce').joinpath(announcemen_batch_new+'.csv')),'scw')


if __name__ == '__main__':
        url = 'http://data.miit.gov.cn/resultSearch?categoryTreeId=1128'
        announcemen_batch_new='311'
        img_path =r'announce\img{}'.format(announcemen_batch_new)
        if not os.path.exists(img_path):
            os.makedirs(img_path)
            print('folder ', img_path, 'does not exist! It will be created')
        crawl(announcemen_batch_new+'.csv',img_path,announcemen_batch_new, time.strftime('%Y-%m-%d '))
