import time

import slackweb

WEBHOOK = None


def message(title, link):
    attachments = [
        {
            "fallback": "Save links to Evernote.",
            "color": "good",
            "title": title,
            "title_link": link,
            "text": link
        }
    ]
    _hook(attachments)


def warning(msg):
    attachments = [
        {
            "fallback": msg,
            "color": "warning",
            "text": msg,
            "ts": time.time()
        }
    ]
    _hook(attachments)


def danger(msg):
    attachments = [
        {
            "fallback": msg,
            "color": "danger",
            "text": msg,
            "ts": time.time()
        }
    ]
    _hook(attachments)


_slack = None


def _hook(attachments):
    if WEBHOOK is not None and WEBHOOK != '':
        if _slack is None:
            slack = slackweb.Slack(url=WEBHOOK)
        slack.notify(attachments=attachments)
    else:
        print 'Set Slack Web incomming webhook link to config.ini!'


if __name__ == '__main__':
    WEBHOOK = None
    danger("Cannot read links")
