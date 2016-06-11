from pyinstapaper.instapaper import Instapaper, Folder

INSTAPAPER_KEY = None
INSTAPAPER_SECRET = None
INSTAPAPER_LOGIN = None
INSTAPAPER_PASSWORD = None


def login():
    _instapaper = Instapaper(INSTAPAPER_KEY, INSTAPAPER_SECRET)
    _instapaper.login(INSTAPAPER_LOGIN, INSTAPAPER_PASSWORD)
    return _instapaper


def get_links(instapaper, limit=10):
    # Get the 10 latest instapaper bookmarks for the given account and do
    # something with the article text
    return instapaper.get_bookmarks('unread', limit)

    # for (idx, bookmark) in enumerate(bookmarks):
    #     print idx, bookmark.title, bookmark.url
    #     bookmark.archive()


def archive(bookmark):
    bookmark.archive()
