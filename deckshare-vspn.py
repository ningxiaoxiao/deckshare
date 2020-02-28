# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import csv
import time
import json
import urllib
from urllib import request
from urllib import parse
import os
import shutil
from urllib.request import urlretrieve


allcards = json.load(open('cards.json', encoding='utf-8'))


# 把网站返回的数据转成数组
def toCardArray(jdata):
    ret = []
    tmp = {}
    for c in jdata['data']['cardID']:
        cj = findcard(c)
        # print(cj)
        # print(c)

        name = cj['name'].replace("‧", "·")
        if c in tmp:
            tmp[c] = [
                name,
                str(cj['cost']),
                int(tmp[c][2]) + 1
            ]
        else:
            tmp[c] = [name, str(cj['cost']),  1]

    for c in tmp:
        ret.append(tmp[c])
    # 按cost排序
    ret = sorted(ret, key=lambda x: int(x[1]))
    return ret
# 从全卡组中找到卡,返回详细数据


def findcard(cardid):
    for c in allcards:
        if int(c['url']) == int(cardid):
            return c
# 从网站得数据


def getCards(code):
    data = {
        "deck_code": code,
    }
    postdata = parse.urlencode(data).encode('utf-8')
    jtext = urllib.request.urlopen("https://exp.16163.com/sv/to_cards",
                                   postdata)
    html = jtext.read().decode('utf-8')
    j = json.loads(html)
    return j  # todo 不成功的问题


def getdeck(name, clan, code):
    jdata = getCards(code)
    cards = toCardArray(jdata)

    xls = open('c:/deckshare/cards.csv', 'w', newline='', encoding='utf-8-sig')
    cw = csv.writer(xls)
    cw.writerow(['name', 'cost', 'count', 'pic'])
    for c in cards:
        cw.writerow(c)
    # 费用图
    costmap = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for c in cards:
        cost = int(c[1])
        count = int(c[2])
        if cost == 0:  # 0费计到1费中
            costmap[0] += count
            continue
        if cost > 9:  # 9和9费以上 者放到9中
            costmap[8] += count
            continue
        costmap[cost-1] += count
    xls = open('c:/deckshare/deckshare.csv', 'w',
               newline='', encoding='utf-8-sig')
    cw = csv.writer(xls)
    # 写标题
    titles = []
    titles.append('name')
    titles.append('class')
    for x in range(1, 19):
        titles.append('pic'+str(x))
    for x in range(1, 10):
        titles.append('cost'+str(x))

    cw.writerow(titles)

    row = []
    row.append(name)
    row.append('c:/deckshare/class/'+clan+'.png')
    for x in range(1, 19):
        row.append('c:/deckshare/cards/'+str(x)+'.png')
    for x in costmap:
        row.append(x)
    cw.writerow(row)
    # 清空cards
    for x in os.listdir("cards"):
        os.remove('cards/'+x)

    # 这里要把少的图片用一个空图片补上,不然会出问题
    for x in range(len(cards), 19):
        shutil.copy('null.png', 'cards/'+str(x)+'.png')


# 读出带名字与卡码的
codeFile = csv.reader(open(''))

# 形成输出文件
output = csv.writer(open(''))
# 构建标题
rowTitle = ['name']
for x in range(1, 19):
    rowTitle.append('c'+str(x))
output.writerow(rowTitle)

for row in codeFile:
    code = row[2]
    cards = toCardArray(getCards(code))
    # cards info[name,cost,count]
    row = [row[0]]
    for c in cards:
        row.append(c[0]+'x'+c[2]+'.png')  # 直接生成带.png的文件
    output.writerow(row)
