import os.path
import re
import requests
import urllib.parse as parse
import urllib.request as request
import csv
import time

query_string = {
    'word': '千峰教育'
}

keyword = parse.urlencode(query_string)
base_url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&{}&x_bfe_rqs=03200000000000000000080000000000000000000000000800000000000000000002&x_bfe_tjscore=0.080000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&rsv_dl=news_b_pn&pn={}'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}

# 代理ip防止被ban
proxies = {
    "https": "127.0.0.1:7890",
    "http": "127.0.0.1:7890"
}

csvfile = open('./data/baiduzixun.csv', mode='w', encoding="utf-8")
fieldnames = ['title', 'context']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()


def replace_prama_value(url, prama, value):
    # 使用正则表达式匹配并替换参数的值
    pattern = re.compile(r'(' + prama + '=\d+)')
    replaced_url = re.sub(pattern, f'pn={value}', url)
    return replaced_url


for i in range(0, 5):
    response = requests.get(url=base_url.format(keyword, str(i*10)), headers=headers, proxies=proxies)
    response.encoding = 'utf-8'
    html_str = response.text
    a_list = re.findall("aria-label=\"(.*?)\"", html_str, re.S)
    news = {"title": "", "context": ""}
    flag = 0
    time.sleep(5)
    print("?")
    for a in a_list:
        print("*")
        if re.match("标题", a, re.S):
            news['title'] = a[3:]
            flag = flag + 1
        elif re.match("摘要", a, re.S):
            news['context'] = a[3:-12]
            flag = flag + 1
        if flag == 2:
            flag = 0
            writer.writerow(news)
