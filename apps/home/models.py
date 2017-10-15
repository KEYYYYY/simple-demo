import json


class Topic:
    def __init__(self, id, topic, user_id):
        self.id = id
        self.topic = topic
        self.user_id = user_id

    def save(self):
        topic_json = json.dumps(self, default=lambda obj: obj.__dict__)
        with open('db/topics.txt', 'a', encoding='utf-8') as f:
            f.write(topic_json + '\n')

    @classmethod
    def find_all(cls):
        topic_list = []
        with open('db/topics.txt', encoding='utf-8') as f:
            for line in f:
                topic_dict = json.loads(line)
                topic = Topic(**topic_dict)
                topic_list.append(topic)
            return topic_list

    @classmethod
    def find_by(cls, **kwargs):
        topic_list = Topic.find_all()
        topics = []
        for k, v in kwargs.items():
            for topic in topic_list:
                if getattr(topic, k) == v:
                    topics.append(topic)
        return topics


class Comment:
    def __init__(self, id, topic_id, user_id, content):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.content = content

    def save(self):
        comment_json = json.dumps(self, default=lambda obj: obj.__dict__)
        with open('db/comments.txt', 'a', encoding='utf-8') as f:
            f.write(comment_json + '\n')

    @classmethod
    def find_all(cls):
        comment_list = []
        with open('db/comments.txt', encoding='utf-8') as f:
            for line in f:
                comment_dict = json.loads(line)
                comment = Comment(**comment_dict)
                comment_list.append(comment)
            return comment_list

    @classmethod
    def find_by(cls, **kwargs):
        commet_list = Comment.find_all()
        comments = []
        for k, v in kwargs.items():
            for comment in commet_list:
                if getattr(comment, k) == v:
                    comments.append(comment)
        return comments
