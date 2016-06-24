import logging
import time

import slackweb

WEBHOOK = None

logging.config.fileConfig('log.config')
logger = logging.getLogger('slackLogger')


def message(title, link):
    attachments = [
        {
            'fallback': 'Save links to Evernote.',
            'color': 'good',
            'title': title,
            'title_link': link,
            'text': link
        }
    ]
    _hook(attachments)


def warning(msg):
    attachments = [
        {
            'fallback': msg,
            'color': 'warning',
            'text': msg,
            'ts': time.time()
        }
    ]
    _hook(attachments)


def danger(msg, e=None):
    attachments = [
        {
            'fallback': msg,
            'color': 'danger',
            'text': msg,
            'ts': time.time(),
            'fields': [
                {
                    'title': 'Exception',
                    'value': e,
                    'short': False
                }
            ]
        }
    ]
    _hook(attachments)


_slack = None


def _hook(attachments):
    if WEBHOOK is not None and WEBHOOK != '':
        if _slack is None:
            slack = slackweb.Slack(url=WEBHOOK)
        slack.notify(attachments=attachments)
        logger.debug('Send message to Slack.')
    else:
        logger.info('Set Slack Web incomming webhook link to config.ini!')


if __name__ == '__main__':
    WEBHOOK = None
    danger('Cannot read links')
