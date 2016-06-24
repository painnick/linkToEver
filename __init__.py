#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import logging
from logging import config
import traceback

import evernoteutil
import readabilityutil
import instapaperutil
import slackutil


def load_config():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    instapaperutil.INSTAPAPER_KEY = config.get('Instapaper', 'INSTAPAPER_KEY')
    instapaperutil.INSTAPAPER_SECRET = config.get('Instapaper', 'INSTAPAPER_SECRET')
    instapaperutil.INSTAPAPER_LOGIN = config.get('Instapaper', 'INSTAPAPER_LOGIN')
    instapaperutil.INSTAPAPER_PASSWORD = config.get('Instapaper', 'INSTAPAPER_PASSWORD')
    logger.debug('Instapaper : %s, %s, %s, %s',
                 instapaperutil.INSTAPAPER_KEY,
                 instapaperutil.INSTAPAPER_SECRET,
                 instapaperutil.INSTAPAPER_LOGIN,
                 instapaperutil.INSTAPAPER_PASSWORD
                 )

    readabilityutil.AUTH_TOKEN = config.get('Readabilty', 'AUTH_TOKEN')
    logger.debug('Readabilty : %s', readabilityutil.AUTH_TOKEN)

    evernoteutil.AUTH_TOKEN = config.get('Evernote', 'AUTH_TOKEN')
    logger.debug('Evernote : %s', evernoteutil.AUTH_TOKEN)

    slackutil.WEBHOOK = config.get('Slack', 'WEBHOOK')
    logger.debug('Slack : %s', slackutil.WEBHOOK)


def save(_url, _title):
    html = readabilityutil.parse(_url)
    evernoteutil.save(_title, _url, html)


if __name__ == '__main__':

    logging.config.fileConfig('log.config')
    logger = logging.getLogger('appLogger')

    load_config()

    try:
        _instapaper = instapaperutil.login()

        _bookmarks = instapaperutil.get_links(_instapaper, 30)
        if len(_bookmarks) == 0:
            logger.info('No link to save')
        else:
            logger.info('Read %d link(s) to save', len(_bookmarks))
    except Exception, e:
        logger.exception('Cannot get Instapaper links.')
        slackutil.danger('Cannot get Instapaper links.', traceback.format_exc())
        exit(-1)

    for (idx, bookmark) in enumerate(_bookmarks):
        title = bookmark.title.encode('utf-8')
        link = bookmark.url.encode('utf-8')
        logger.debug('%2d > %s - %s' % (idx, title, link))
        try:
            save(link, title)

            instapaperutil.archive(bookmark)
            logger.debug('Archive link(s) from Instapaper.')

            slackutil.message(title, link)
        except Exception, e:
            logger.exception('Cannot save to Evernote - %s' % title)
            slackutil.danger('Cannot save to Evernote - %s' % title, traceback.format_exc())

    logger.info('Complete.')
