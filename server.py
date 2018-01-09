import socket


def run(host='', port=5000):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(3)
        while True:
            print('正在监听5000端口')
            connection, address = s.accept()
            r = connection.recv(1024).decode('utf-8')
            print(r)
            print(address)


if __name__ == '__main__':
    run()
