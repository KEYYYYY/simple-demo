import socket
import urllib.parse
from collections import namedtuple

import views

# 请求封装类
Request = namedtuple('Request', ('method', 'path', 'query_dict', 'form_dict'))


def split_request(request):
    """将请求切割为方法，路径-查询，首部字典"""
    method, path_and_query, other = request.split(maxsplit=2)
    # print('切割出的方法，路径为：', method, path)
    headers_dict = {}
    headers = other.split('\r\n')[1:]
    # print(headers)
    for header in headers[:-2]:
        k, v = header.split(': ', maxsplit=1)
        headers_dict[k] = v
    # print(headers_dict)
    body = other.split('\r\n\r\n', maxsplit=1)[1]
    return method, path_and_query, headers_dict, body


def split_query(path_and_query):
    """path_and_query分解为path，query字典"""
    """/static?file_name=img.jpg"""
    data = path_and_query.split('?', maxsplit=1)
    if len(data) == 1:
        # 如果长度为1则说明不存在query
        return data[0], {}
    else:
        query_dict = {}
        querys = data[1].split('&')
        for item in querys:
            item = urllib.parse.unquote(item)
            k, v = item.split('=')
            query_dict[k] = v
        return data[0], query_dict


def split_form(body):
    """根据body将其中的表单拆分为dict"""
    form = {}
    data = body.split('&')
    if len(data) == 1:
        return form
    for item in data:
        k, v = item.split('=', maxsplit=1)
        form[k] = v
    return form


def get_view(request):
    """通过path来获取相应的路由函数"""
    from views import views_dict
    view = views_dict.get(request.path, views.error)
    return view(request)


def run(host='', port=5000):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(3)
        while True:
            connection, address = s.accept()
            r = connection.recv(1024).decode('utf-8')
            print('原始请求为:', r)
            method, path_and_query, header_dict, body = split_request(r)
            path, query_dict = split_query(path_and_query)
            # print('path:', path_and_query)
            # print('query_dict:', query_dict)
            body_dict = split_form(body)
            request = Request(method, path, query_dict, body_dict)
            print(request)
            response = get_view(request)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    run()
