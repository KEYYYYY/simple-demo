import json


class User:
    """用户类"""
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def save(self):
        with open('users.txt', 'a', encoding='utf-8') as fout:
            user_json = json.dumps(self, default=lambda obj: obj.__dict__)
            fout.write(user_json + '\n')

    @classmethod
    def all(cls):
        with open('users.txt', encoding='utf-8') as fin:
            users = []
            for line in fin:
                data = json.loads(line)
                users.append(User(data['username'], data['password_hash']))
            return users
