# encoding: utf-8
'''
@author: niko
@contact: simaqingsheng@gmail.com
@file: 02.处理json数据.py
@time: 2020/2/6 18:17
@desc:
'''

from urllib import request
import json

# 获取数据
def get_data():

    url="https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=rank&page_limit=300&page_start=0"

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }

    req=request.Request(url=url,headers=headers)
    response=request.urlopen(req)
    if response.getcode()==200:
        data=response.read()
        # print(type(data),data) #bytes类型
        return data

# 解析数据
def parse_data(html):
    # 将字符串形式的json转换为dict字典
    result=json.loads(html)
    # print(type(result),result)
    movies=result['subjects']
    for movie in movies:
        print(movie['title'],movie['rate'])


if __name__ == '__main__':
    parse_data(get_data())
