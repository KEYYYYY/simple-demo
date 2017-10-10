def render_template(file_name):
    """渲染模版函数"""
    with open('templates/' + file_name) as fout:
        result = fout.read()
        return result


def redirect(path):
    header = 'HTTP/1.1 302 OK\r\nLocation: {path}\r\n'.format(path=path)
    return header.encode('utf-8')


def json_response(data):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    r = header + '\r\n' + data
    return r.encode('utf-8')
