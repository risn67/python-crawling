import requests
from lxml import etree
import csv 

#  新建一个csv文件

# Permission denied
# 重复使用同一个csv文件会出现[没有权限；拒绝访问]
fp=open('/Users/lcn/Documents/file/file-python/douban250_IMDB250.csv','wt',newline='',encoding='utf-8')
writer=csv.writer(fp)
# 写入表头信息
writer.writerow(('name','url','rate','director','type','country','year'))

#  构造urls
urls=['https://www.douban.com/doulist/968362/?start={}'.format(i) for i in range(0,175,25)]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

for url in urls:
    # 用requests库获取网页信息,lxml解析html文件
    html=requests.get(url,headers=headers)
    selector=etree.HTML(html.text)

    # 取大标签,以此类推
    # <tr class='item'>
    infos=selector.xpath('//div[@class="doulist-item"]')

    name = selector.xpath('//div[@class="title"]/a/text()')
    name = list(set(name))
    name.remove('\n          ')
    url = selector.xpath('//div[@class="title"]/a/@href')
    rate = selector.xpath('//div[@class="rating"]/span[2]/text()')
    filmInfo = selector.xpath('//div[@class="abstract"]/text()')
    #filmInfo = list(set(filmInfo))

    for info in range(len(infos)):

        nameValue = name[info].replace('\n', ' ').strip()
        urlValue = url[info]
        rateValue = rate[info]
        director = filmInfo[info * 5].replace('\n', ' ').strip()
        type = filmInfo[info * 5 + 2].replace('\n', ' ').strip()
        country = filmInfo[info * 5 + 3].replace('\n', ' ').strip()
        year = filmInfo[info * 5 + 4].replace('\n', ' ').strip()

        info = info + 1

        print(nameValue,urlValue,rateValue,director,type,country,year)
        writer.writerow((nameValue,urlValue,rateValue,director,type,country,year))

 #  关闭csv文件
fp.close()


