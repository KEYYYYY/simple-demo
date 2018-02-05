def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    client_id = '4025666664'
    redirect_uri = 'http://127.0.0.1:8000/weibo/'
    auth_url = weibo_auth_url + '?client_id={client_id}&redirect_uri={redirect_uri}'.format(
        client_id=client_id,
        redirect_uri=redirect_uri,
    )

    print(auth_url)


def get_access_token(code='4deb0a8e162af8418e3664cd44618544'):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    import requests
    print(requests.post(access_token_url, data={
        'client_id': '4025666664',
        'client_secret': '51c3e8bbcd92e5adb3f41526ef297873',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/weibo/'
    }).text)


def get_user_info():
    url = 'https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}'.format(
        access_token='2.00v4Vy4GUnR85E471f672560TljxYE',
        uid='5851073047',
    )
    print(url)


if __name__ == '__main__':
    get_auth_url()
    get_access_token()
    get_user_info()
