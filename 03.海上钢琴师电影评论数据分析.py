# encoding: utf-8
'''
@author: niko
@contact: simaqingsheng@gmail.com
@file: 03.海上钢琴师电影评论数据分析.py
@time: 2020/2/7 23:33
@desc:
'''

from urllib import request
import json
from datetime import datetime,timedelta
import time

# 获取数据
def get_data(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Mobile Safari/537.36'
    }
    req=request.Request(url=url,headers=headers)
    response=request.urlopen(req)
    if response.getcode()==200:
        data=response.read()
        return data

# 解析数据
def parse_data(html):
    result=json.loads(html)
    data=result['cmts']
    comments=[]
    for item in data:
        comment={
            'id':item['id'],
            'nickName':item['nickName'],
            'cityName':item['cityName'] if 'cityName' in item else '', #处理cityName不存在的情况
            'content':item['content'].replace('\n',' '), #处理评论内容中出现的换行情况
            'score':item['score'],
            'startTime':item['startTime']
        }
        comments.append(comment)
    return comments

# 存储数据到文本文件
def save_to_txt():
    start_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S') #当前时间
    end_time='2019-11-15 00:00:00'
    while start_time>end_time:
        # 将空格替换成%20，冒号替换成%3A
        # http://m.maoyan.com/mmdb/comments/movie/1292.json?v=yes&offset=1&startTime=2020-02-08%2023%3A49%3A16
        url='http://m.maoyan.com/mmdb/comments/movie/1292.json?v=yes&offset=0&startTime='+start_time.replace(' ','%20').replace(':','%3A')        #2020-02-08%2023%3A49%3A16
        html=get_data(url)
        comments=parse_data(html)
        for item in comments:
            with open("comments.text",mode='a',encoding='utf-8') as f:
                f.write(str(item['id'])+','+item['nickName']+','+item['cityName']+','+item['content']+','+str(item['score'])+','+item['startTime']+'\n')
        end=comments.__len__()-1
        start_time=comments[end].get('startTime')

        # datetime.strftime() 是把date,datetime,time objects格式变成文本/字符串格式：
        # datetime.strptime() 是反过来, 把文本/字符串格式 变成date,datetime, time objects ：

        start_time=datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')-timedelta(seconds=1)#向前减一秒，防止取到重复的数据
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    save_to_txt()