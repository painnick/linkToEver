#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser

import evernoteutil
import readabilityutil
import instapaperutil
import slackutil


def load_config():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    instapaperutil.INSTAPAPER_KEY = config.get("Instapaper", "INSTAPAPER_KEY")
    instapaperutil.INSTAPAPER_SECRET = config.get("Instapaper", "INSTAPAPER_SECRET")
    instapaperutil.INSTAPAPER_LOGIN = config.get("Instapaper", "INSTAPAPER_LOGIN")
    instapaperutil.INSTAPAPER_PASSWORD = config.get("Instapaper", "INSTAPAPER_PASSWORD")

    readabilityutil.AUTH_TOKEN = config.get("Readabilty", "AUTH_TOKEN")

    evernoteutil.AUTH_TOKEN = config.get("Evernote", "AUTH_TOKEN")

    slackutil.WEBHOOK = config.get("Slack", "WEBHOOK")


def save(_url, _title):
    html = readabilityutil.parse(_url)
    evernoteutil.save(_title, _url, html)


if __name__ == '__main__':

    load_config()

    try:
        _instapaper = instapaperutil.login()
        print "Login instapaper."

        _bookmarks = instapaperutil.get_links(_instapaper, 30)
        print "Get links."
    except Exception, e:
        print e
        slackutil.danger("Cannot get instapaper links")
        exit(-1)

    for (idx, bookmark) in enumerate(_bookmarks):
        title = bookmark.title.encode('utf-8')
        link = bookmark.url.encode('utf-8')
        print idx, title, link
        try:
            save(link, title)
            instapaperutil.archive(bookmark)
            print "Send slack message."
            slackutil.message(title, link)
        except Exception, e:
            print e
            slackutil.danger("Cannot save to evernote - %s" % title)

