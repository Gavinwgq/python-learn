from bs4 import BeautifulSoup
import requests
import re
import mysql.connector

# 爬取数据并保存到数据库

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="test"
)
mycursor = mydb.cursor()


def getCityLis(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features='html.parser')
    return soup.find_all('a', href=re.compile('citycn*'), class_='dropdown-item')


def getTargetDiv(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features='html.parser')
    return soup.select(".col-md-6>h4")


urlP = 'https://brt.fareast.mobi/'
cityList = getCityLis("https://brt.fareast.mobi/quanc?param=8")
x = 0
for city in cityList:
    name = city.get_text().strip().replace("\n", "").replace('\r', '')
    href = urlP + city['href']
    print("*************************************")
    print(name, "(", href, ")")
    x = x + 1
    if x < 34:
        continue
    titleList = getTargetDiv(href)
    for title in titleList:
        titleText = title.get_text().strip().replace("\n", "").replace('\r', '')
        print('----------------------')
        print(titleText)
        for data in title.next_siblings:
            if data == '\n':
                continue
            if data.name == 'h4':
                break
            if data.name == 'table':
                for dtr in data.children:
                    if dtr == '\n':
                        continue
                    itemKey = dtr.a.get_text()
                    itemVal = ''
                    n = 0
                    for v in dtr.a.next_siblings:
                        if v.name == 'img':
                            if v['src'] == '../../images/tick.gif':
                                itemVal = '是'
                                break
                            elif v['src'] == '../../images/cross.gif':
                                itemVal = '否'
                                break
                            elif v['src'] == '../../images/partial.gif':
                                itemVal = '部分'
                                break
                        if v.name == 'span':
                            n = n + 1
                            text = v.get_text().strip().replace("\n", "").replace('\r', '')
                            if n == 2 and text != '':
                                itemVal = itemVal + '(' + text + ')'
                                break
                            else:
                                itemVal = itemVal + text

                    print(itemKey, ':', itemVal)
                    param = (name, titleText, itemKey, itemVal)
                    mycursor.execute("INSERT INTO brtdata(city,title,itemKey,itemVal) VALUES(%s,%s,%s,%s)", param)
                    mydb.commit()
