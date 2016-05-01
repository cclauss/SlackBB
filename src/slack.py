# Copyright 2016 Lukas Kollmer<lukas@kollmer.me>

from slacker import Slacker
from config import config

slack_token = config['slack-token']
slack_channel = config['slack-channel']
slack = Slacker(slack_token)


def send_new_forum_post_to_slack(post):
    # Slack documentation: https://api.slack.com/methods/chat.postMessage
    # Slack documentation: https://api.slack.com/docs/attachments

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

    slack_username = post.user.name + ' (via ForumBot)'

    response = slack.chat.post_message(slack_channel,
                                       text=None,
                                       username=slack_username,
                                       icon_url=post.user.avatar_url,  # TODO: Create/Find an avatar for the bot
                                       attachments=attachments
                                       )
    return response.successful
