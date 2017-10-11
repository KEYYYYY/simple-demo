import os

import requests
from pyquery import PyQuery as pq


def cached_url(url):
    folder_name = 'cached_ituring'
    file_name = url.split('page=', 1)[1] + '.html'
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
        content = requests.get(url, headers).content
        with open(path, 'wb') as f:
            f.write(content)
        return content


def books_from_url(url):
    content = cached_url(url)
    images = pq(content)('.book-img')
    titles = pq(content)('.book-info')
    for title, image in zip(titles, images):
        img_url = pq(image)('img').attr('src')
        text = pq(title)('a').attr('title')
        info = pq(title)('.intro').text()
        print('图片:', img_url)
        download_imgs(img_url, text)
        print('书名:', text)
        print('介绍:', info)


def download_imgs(url, name):
    folder_name = 'images_ituring'
    file_name = name + '.jpg'
    if r'/' in file_name:
        file_name = file_name[:1] + '.jpg'
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
    for i in range(1, 53):
        url = 'http://www.ituring.com.cn/book?tab=book&sort=hot&page={page}'.format(
            page=i)
        books_from_url(url)
