import requests
from lxml import etree
import csv 

# print (r.content)
# url = 'https://movie.douban.com/top250?start=0&filter='

#  新建一个csv文件

# Permission denied
# 重复使用同一个csv文件会出现[没有权限；拒绝访问]
fp=open('/Users/lcn/Documents/file/file-python/douban_books.csv','wt',newline='',encoding='utf-8')
writer=csv.writer(fp)
# 写入表头信息
writer.writerow(('name','url','author','publisher','date','price','rate','comment'))

#  构造urls
urls=['https://book.douban.com/top250?start={}'.format(i) for i in range(0,250,25)]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

for url in urls:
    # 用requests库获取网页信息,lxml解析html文件
    html=requests.get(url,headers=headers)
    selector=etree.HTML(html.text)

    # 取大标签,以此类推
    # <tr class='item'>
    infos=selector.xpath('//tr[@class="item"]')

    for info in infos:
        #  IndexError: list index out of range
        name = info.xpath('td/div/a/@title')[0]
        url = info.xpath('td/div/a/@href')[0]
        # /text 是获取到定位元素的文本值
        book_infos = info.xpath('td/p/text()')[0]
        # print(book_infos)
        #if book_infos.find('/', beg=0, end=len(book_infos))
        if name != '圣经' :
            author = book_infos.split('/')[0]
            publisher = book_infos.split('/')[-3]
            date=book_infos.split('/')[-2]
            price=book_infos.split('/')[-1]
            rate=info.xpath('td[2]/div[2]/span[2]/text()')[0]
            comments=info.xpath('td/p/span/text()')
            comment=comments[0] if len(comments) !=0 else "空"
        else :
            author = ''
            publisher = book_infos.split('/')[0]
            date=book_infos.split('/')[-1]
            price=''
            rate=info.xpath('td[2]/div[2]/span[2]/text()')[0]
            comments=info.xpath('td/p/span/text()')
            comment=comments[0] if len(comments) !=0 else "空"

        #  打印查看结果
        print(name, url, author, publisher, date, price, rate, comment)
        #  将上述的数据写入到csv文件
        writer.writerow((name,url,author,publisher,date,price,rate,comment))

 #  关闭csv文件
fp.close()


