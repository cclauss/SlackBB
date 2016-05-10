# SlackBB [![Build Status](https://travis-ci.org/lukaskollmer/SlackBB.svg?branch=master)](https://travis-ci.org/lukaskollmer/SlackBB)

SlackBB is a Python script that monitors a NodeBB forum for new posts and sends Slack notifications to a channel of your choice.

### Usage

You will need to create a `config.json` file in the project root.
Your config file should contain:

```
{
  "slack-webhook-url" : "YOUR_SLACK_TOKEN",
  "slack-channel" : "YOUR_SLACK_CHANNEL",
  "forum-url" : "YOUR_FORUM_URL"
}
```

You'll also need to create an empty `data.txt` file in the project root. SlackBB will store a list of topics for which notifications have already been sent in the `data.txt` file.