# copyright 2016 Lukas Kollmer<lukas@kollmer.me>

import json
import threading
import urllib2
from bs4 import BeautifulSoup
import slack
from config import config


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

    def __init__(self, json_object, forum_url_endpoint):
        self.user = ForumUser()
        self.user.name = json_object['user']['username']
        _avatar_url = json_object['user']['picture']
        if 'http' not in _avatar_url: # The user uploaded its avatar to the forum, fetch it from there
            _avatar_url = forum_url_endpoint + _avatar_url
        self.user.avatar_url = _avatar_url
        self.title = json_object['topic']['title']
        self.index = str(json_object['index'])
        self.url = forum_url_endpoint + '/topic/' + json_object['topic']['slug'] + '/' + self.index
        self.id = json_object['topic']['tid']

        content = json_object['content']
        soup = BeautifulSoup(content, 'html.parser')
        self.text = soup.get_text()


def get_recent_posts(forum_url_endpoint):
    posts = []

    api_endpoint = forum_url_endpoint + '/api/recent/posts'

    try:
        api_response = urllib2.urlopen(api_endpoint).read()
    except:
        #print('Unable to reach the Forum API, will try again in 10 minutes')
        return []

    json_data = json.loads(api_response)

    for post in json_data:
        post_index = int(post['index'])
        if post_index == 1:
            _post = ForumPost(post, forum_url_endpoint)
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


def check_for_new_posts(forum_url_endpoint):
    recent_posts = get_recent_posts(forum_url_endpoint)

    for post in recent_posts:
        if not did_already_notify_about_topic_with_id(post.id):
            success = slack.send_new_forum_post_to_slack(post)
            save_send_notification_success_for_topic_with_id(post.id, success)
            if success is True:
                print('Sent slack message for topic ' + post.title)
        else:
            pass

    threading.Timer(60*10, check_for_new_posts).start()


if __name__ == '__main__':
    forum_url = config['forum-url']
    print('Will start monitoring ' + forum_url + ' for new posts')
    check_for_new_posts(forum_url)