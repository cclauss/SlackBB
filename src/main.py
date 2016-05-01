# copyright 2016 Lukas Kollmer<lukas@kollmer.me>

import slack
import urllib2
import json
from bs4 import BeautifulSoup
import threading


class ForumTopic(object):
    title = None
    url = None
    summary = None
    id = None


class ForumUser(object):
    name = None
    avatar_url = None


class ForumPost(object):
    user = None
    url = None
    index = None
    text = None
    title = None
    id = None

    def __init__(self, json_object):
        self.user = ForumUser()
        self.user.name = json_object['user']['username']
        _avatar_url = json_object['user']['picture']
        if 'http' not in _avatar_url:
            _avatar_url = 'https://forum.omz-software.com' + _avatar_url
        self.user.avatar_url = _avatar_url
        self.title = json_object['topic']['title']
        self.index = str(json_object['index'])
        self.url = 'https://forum.omz-software.com/topic/' + json_object['topic']['slug'] + '/' + self.index
        self.id = json_object['topic']['tid']

        content = json_object['content']
        soup = BeautifulSoup(content, 'html.parser')
        self.text = soup.get_text()


def get_recent_posts():
    posts = []

    endpoint = 'https://forum.omz-software.com/api/recent/posts'

    try:
        api_response = urllib2.urlopen(endpoint).read()
    except:
        return []

    json_data = json.loads(api_response)

    for post in json_data:
        post_index = int(post['index'])
        if post_index == 1:
            print(post)
            _post = ForumPost(post)
            posts.append(_post)
    return posts


def did_already_notify_about_topic_with_id(topic_id):
    with open('../data.txt', 'r') as f:
        did_already_notify = str(topic_id) + '\n' in f.readlines()
        return did_already_notify


def save_send_notification_success_for_topic_with_id(topic_id, success):
    with open('../data.txt', 'a') as f:
        if success is True:
            text = str(topic_id) + '\n'
            f.write(text)


def check_for_new_posts():
    recent_posts = get_recent_posts()

    for post in recent_posts:
        if not did_already_notify_about_topic_with_id(post.id):
            success = slack.send_new_forum_post_to_slack(post)
            save_send_notification_success_for_topic_with_id(post.id, success)
        else:
            pass

    threading.Timer(60, check_for_new_posts).start()


if __name__ == '__main__':
    check_for_new_posts()
