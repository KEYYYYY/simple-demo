import os

import requests
from pyquery import PyQuery as pq


def cached_url(url):
    folder_name = 'cached_douban'
    file_name = url.split('=', 1)[1] + '.html'
    path = os.path.join(folder_name, file_name)
    # 如果缓存中有直接从本地读取
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            s = f.read()
            return s
    else:
        # 如果不存在放缓存的目录
        # 也就是第一次运行程序
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
        }
        r = requests.get(url, headers)
        # 写入缓存`
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def movies_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.item')
    for item in items:
        item = pq(item)
        title = item('.title').text()
        rating_num = item('.rating_num').text()
        img_url = item('img').attr('src')
        inq = item('.inq').text()
        print('电影名:', title)
        print('评分:', rating_num)
        print('海报:', img_url)
        print('引语:', inq)
        # 下载电影海报
        download_imgs(img_url, title[:2])


def download_imgs(url, name):
    folder_name = 'images_douban'
    file_name = name + '.jpg'
    path = os.path.join(folder_name, file_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    if not os.path.exists(path):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
        }
        content = requests.get(url, headers).content
        with open(path, 'wb') as f:
            f.write(content)


if __name__ == '__main__':
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies = movies_from_url(url)
