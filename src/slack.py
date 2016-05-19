# Copyright 2016 Lukas Kollmer<lukas@kollmer.me>

from config import config
import urllib2
import json

slack_webhook_url = config['slack-webhook-url']
slack_channel = config['slack-channel']


def send_new_forum_post_to_slack(post):
    attachments = [
        {
            'fallback': 'New post by @' + post.user.name,  # Fallback is used in iOS notifications
            'color': '#36a64f',
            # 'author_name' : post.user.name,
            # 'author_link' : 'https://forum.omz-software.com/user/' + post.user.name,
            # 'author_icon' : post.user.avatar_url,
            'title': post.title,
            'title_link': post.url,
            'text': post.text
        }
    ]

    data = json.dumps(
        {
            'channel' : slack_channel,
            'username' : post.user.name,
            'icon_url' : post.user.avatar_url,
            'attachments' : attachments
        }
    )
    req = urllib2.Request(slack_webhook_url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response == 'ok'
