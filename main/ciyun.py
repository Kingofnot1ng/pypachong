import csv

import imageio
import jieba
from wordcloud import wordcloud

file_path = '../data/baiduzixun.csv'
data = []
data_str = ''
with open(file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        data.append(row)
    for i in range(0, len(data)):
        data[i] = ''.join(data[i])
    data_str = ''.join(data)

    stopwords_filepath = "../src/stopword.txt"
    stopwords = [line.strip() for line in open(stopwords_filepath, 'r', encoding='utf-8').readlines()]
    for i in stopwords:
        data_str = data_str.replace(i, '')

    seg_list = jieba.cut(data_str, cut_all=False)
    fenci_str = ' '.join(seg_list)

mask = imageio.imread("../src/img/Chinamap.jpg")

c = wordcloud.WordCloud(
    background_color="white",
    max_words=200,
    mask=mask,
    font_path='C:\Windows\Fonts\simsun.ttc', )

c.generate_from_text(text=fenci_str)
c.to_file("../src/img/pywordcloud.png")
