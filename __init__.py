#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser

import evernoteutil
import readabilityutil
import instapaperutil


def loadConfig():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    instapaperutil.INSTAPAPER_KEY = config.get("Instapaper", "INSTAPAPER_KEY")
    instapaperutil.INSTAPAPER_SECRET = config.get("Instapaper", "INSTAPAPER_SECRET")
    instapaperutil.INSTAPAPER_LOGIN = config.get("Instapaper", "INSTAPAPER_LOGIN")
    instapaperutil.INSTAPAPER_PASSWORD = config.get("Instapaper", "INSTAPAPER_PASSWORD")

    readabilityutil.AUTH_TOKEN = config.get("Readabilty", "AUTH_TOKEN")

    evernoteutil.AUTH_TOKEN = config.get("Evernote", "AUTH_TOKEN")


def save(_url, _title):
    html = readabilityutil.parse(_url)
    evernoteutil.save(_title, _url, html)


if __name__ == '__main__':

    loadConfig()

    _instapaper = instapaperutil.login();

    _bookmarks = instapaperutil.get_links(_instapaper, 30)

    for (idx, bookmark) in enumerate(_bookmarks):
        print idx, bookmark.title, bookmark.url
        save(bookmark.url, bookmark.title.encode('utf-8'))
        instapaperutil.archive(bookmark)