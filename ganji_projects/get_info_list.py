import requests
from bs4 import BeautifulSoup
import pymongo
import random

client=pymongo.MongoClient('localhost',27017)
ganji=client['ganji']
ganji_goods_info=ganji['ganji_goods_info2']

headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}

# http://cn-proxy.com/
proxy_list = [
    'http://117.177.250.151:8081',
    'http://111.85.219.250:3129',
    'http://122.70.183.138:8118',
    ]
proxy_ip = random.choice(proxy_list)
proxies = {'http': proxy_ip}

# url='http://cs.ganji.com/jiaju/'
# http://cs.ganji.com/jiaju/o2/

def get_goods_link(channel,page,who_sell='o'):
    url='{}{}{}/'.format(channel,who_sell,str(page))
    wb_data=requests.get(url,headers=headers,proxies=proxies)
    soup=BeautifulSoup(wb_data.text,'lxml')
    links_list=soup.select('tr.zzinfo > td.t > a')
    count=0
    for links in links_list:
        link=links.get('href').split('?')[0]
        count+=1
        if count>=5:
            get_goods_info(link)



def get_goods_info(url):
    wb_data=requests.get(url,headers=headers)
    if wb_data.status_code==404:
        pass
    else:
        soup=BeautifulSoup(wb_data.text,'lxml')
        if 'zhuanzhuan' in url:
            titles_list=soup.select('h1.info_titile')[0].text
            price_list=soup.select('span.price_now i')[0].text
            palce_list=soup.select('div.palce_li span i')[0].text
            personl_name=soup.select('p.personal_name')[0].text

            data={
                'title':titles_list,
                'price':price_list,
                "palce_list":palce_list,
                'personl_name':personl_name
            }

        else:
            titles_list=soup.select('h1.title-name')[0].text
            deal_time=soup.select('li i.pr-5')[0].text.replace('\xa0','')
            price_list = soup.select('li i.f22')[0].text
            palce_list =list(soup.select('ul.det-infor li a').stripped_strings) if soup.find_all('a','ul.det-infor li') else None

            data={
                'title':titles_list,
                'deal_time':deal_time,
                "price_list":price_list,
                'palce_list':palce_list
            }

        ganji_goods_info.insert_one(data)



#get_goods_link('http://cs.ganji.com/jiaju/',3)




