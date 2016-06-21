#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser

import evernoteutil
import readabilityutil
import instapaperutil
import slackutil


def loadConfig():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    instapaperutil.INSTAPAPER_KEY = config.get("Instapaper", "INSTAPAPER_KEY")
    instapaperutil.INSTAPAPER_SECRET = config.get("Instapaper", "INSTAPAPER_SECRET")
    instapaperutil.INSTAPAPER_LOGIN = config.get("Instapaper", "INSTAPAPER_LOGIN")
    instapaperutil.INSTAPAPER_PASSWORD = config.get("Instapaper", "INSTAPAPER_PASSWORD")

    readabilityutil.AUTH_TOKEN = config.get("Readabilty", "AUTH_TOKEN")

    evernoteutil.AUTH_TOKEN = config.get("Evernote", "AUTH_TOKEN")

    slackutil.AUTH_TOKEN = config.get("Slack", "AUTH_TOKEN")
    slackutil.CHANNEL = config.get("Slack", "CHANNEL")


def save(_url, _title):
    html = readabilityutil.parse(_url)
    evernoteutil.save(_title, _url, html)


if __name__ == '__main__':

    loadConfig()

    slack_client = None

    try:
        slack_client = slackutil.login()
    except Exception, e:
        print e

    try:
        _instapaper = instapaperutil.login();
        _bookmarks = instapaperutil.get_links(_instapaper, 30)
    except Exception, e:
        print e
        if slackutil is not None:
            slackutil.send_message(slack_client, "Cannot get instapaper links")
        exit(-1)

    for (idx, bookmark) in enumerate(_bookmarks):
        title = bookmark.title.encode('utf-8')
        link = bookmark.url.encode('utf-8')
        print idx, title, link
        try:
            save(link, title)
            instapaperutil.archive(bookmark)
            if slackutil is not None:
                slackutil.send_message(slack_client, "%s - %s" % (title, link))
        except Exception, e:
            print e
            if slackutil is not None:
                slackutil.send_message(slack_client, "Cannot save to evernote - %s" % (title))
