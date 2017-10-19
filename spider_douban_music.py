import os

import requests
from pyquery import PyQuery as pq


def cached_url(url):
    folder_name = 'cached'
    file_name = url.split('=')[1] + '.html'
    path = os.path.join(folder_name, file_name)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    else:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
        }
        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def musics_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.item')
    for item in items:
        item = pq(item)
        name = item('.pl2>a').text()
        author_name = item('p.pl').text()
        comment_num = item('span.pl').text()
        rate_num = item('.rating_nums').text()
        print('歌名：', name)
        print('作者：', author_name)
        print('评论数：', comment_num)
        print('评分：', rate_num)
        download_img(item('img').attr('src'), name)


def download_img(img_url, name):
    if '/' in name:
        name = name[:1]
    folder_name = 'images_musics'
    file_name = name + '.jpg'
    path = os.path.join(folder_name, file_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    if not os.path.exists(path):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
        }
        content = requests.get(img_url, headers).content
        with open(path, 'wb') as f:
            f.write(content)


if __name__ == '__main__':
    for i in range(0, 250, 25):
        url = 'https://music.douban.com/top250?start={page}'.format(page=i)
        musics_from_url(url)
