import hashlib
import json
import time


class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def save(self):
        user_json = json.dumps(self, default=lambda obj: obj.__dict__)
        with open('db/users.txt', 'a', encoding='utf-8') as f:
            f.write(user_json + '\n')

    def verify_password(self, password):
        password_hash = (hashlib.md5(
            password.encode('utf-8'))
        ).hexdigest()
        return self.password_hash == password_hash

    @classmethod
    def new(cls, username, password):
        password_hash = (hashlib.md5(
            password.encode('utf-8'))
        ).hexdigest()
        user = User(int(time.time()), username, password_hash)
        return user

    @classmethod
    def find_by(cls, **kwargs):
        user_list = User.find_all()
        for k, v in kwargs.items():
            for user in user_list:
                if getattr(user, k) == v:
                    return user

    @classmethod
    def find_all(cls):
        user_list = []
        with open('db/users.txt', encoding='utf-8') as f:
            for line in f:
                user_dict = json.loads(line)
                user = User(**user_dict)
                user.id = user_dict['id']
                user_list.append(user)
            return user_list
