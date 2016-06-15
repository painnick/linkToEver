import binascii
import hashlib
import urllib2

import evernote.edam.type.ttypes as Types
import evernote.edam.userstore.constants as UserStoreConstants
from bs4 import BeautifulSoup
from evernote.api.client import EvernoteClient
from urllib2 import URLError

USE_SAND_BOX = False


def save(title, url, html):
    _note_store, _note = _create_new_note(title, url)
    _soup = BeautifulSoup(html, 'html.parser')
    _clean(_note, _soup, _soup)

    print "==============================================================="
    _enml = _soup.prettify()  # str(_soup).replace('></en-media>', '/>')

    try:
        _save(_note_store, _note, _enml)
    except Exception as e:
        print title, url
        print e
        print _enml


def _create_new_note(title, url):
    # Real applications authenticate with Evernote using OAuth, but for the
    # purpose of exploring the API, you can get a developer token that allows
    # you to access your own Evernote account. To get a developer token, visit
    # https://sandbox.evernote.com/api/DeveloperToken.action
    if USE_SAND_BOX:
        auth_token = "S=s1:U=928db:E=15c56b718a9:C=154ff05e8d0:P=1cd:A=en-devtoken:V=2:H=44cbf7e4adc1c5bf32f7d17cbee5f49f"
    else:
        auth_token = "S=s62:U=66fb1a:E=15c56fdb5a6:C=154ff4c86f0:P=1cd:A=en-devtoken:V=2:H=5f95c8f9bc092da483bad78a0ed8afde"

    # Initial development is performed on our sandbox server. To use the production
    # service, change sandbox=False and replace your
    # developer token above with a token from
    # https://www.evernote.com/api/DeveloperToken.action
    client = EvernoteClient(token=auth_token, sandbox=USE_SAND_BOX)

    user_store = client.get_user_store()

    version_ok = user_store.checkVersion(
        "linkToEver",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )
    if not version_ok:
        print "My Evernote API version is not up to date"
        exit(1)

    note_store = client.get_note_store()

    print "Creating a new note in the default notebook"

    note = Types.Note()
    note.title = title

    note_attribute = Types.NoteAttributes(sourceURL=url)
    note.attributes = note_attribute

    return note_store, note


def _save(note_store, note, html):
    # The content of an Evernote note is represented using Evernote Markup Language
    # (ENML). The full ENML specification can be found in the Evernote API Overview
    # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
                    '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'
    note.content += html.encode('ascii', 'xmlcharrefreplace')
    note.content += '</en-note>'

    created_note = note_store.createNote(note)

    print "Successfully created a new note with GUID: ", created_note.guid
    return created_note


def _clean(note, soup, tag):
    if tag.name is None:  # Text with tag
        return
    else:
        # Convert some tags to span tag
        if tag.name in ['figure', 'time', 'label']:
            tag.name = 'span'
        # Convert some tags to div tag
        if tag.name in ['section', 'figcaption', 'main', 'article', 'rel']:
            tag.name = 'div'

        # Convert img tag to en-media tag with Evernote resource
        if tag.name == 'img':
            # Readability convert srcset-value to src-value
            _src = tag['src'].split('%20')[0]
            try:
                _mime, _hash_hex = _save_image(note, _src)

                new_tag = soup.new_tag('img')
                new_tag['type'] = _mime
                new_tag['hash'] = _hash_hex
                new_tag.name = 'en-media'
                tag.replace_with(new_tag)
            except URLError as eu:
                print eu

        # Remove some attributes
        for attribute in ["class", "id", 'datetime', 'for', 'title', 'tabindex']:
            del tag[attribute]

        # Remove some tags
        for child in tag.children:
            if child is not None:
                if child.name in ['header', 'footer', 'aside', 'nav', 'iframe', 'fieldset', 'head', 'meta', 'annotation-driven']:
                    child.replace_with('')
                else:
                    _clean(note, soup, child)


def _save_image(note, image_url):
    print "Save", image_url

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    }
    req = urllib2.Request(image_url.encode('utf-8'), None, headers)
    image = urllib2.urlopen(req)

    _mime = image.info().type
    if _mime == 'text/html':
        _mime = _guess_mime(image_url)

    _body = image.read()

    # To include an attachment such as an image in a note, first create a Resource
    # for the attachment. At a minimum, the Resource contains the binary attachment
    # data, an MD5 hash of the binary data, and the attachment MIME type.
    # It can also include attributes such as filename and location.
    md5 = hashlib.md5()
    md5.update(_body)
    hash = md5.digest()

    data = Types.Data()
    data.size = len(_body)
    data.bodyHash = hash
    data.body = _body

    resource = Types.Resource()
    resource.mime = _mime
    resource.data = data

    if note.resources is None:
        note.resources = [resource]
    else:
        note.resources.append(resource)

    # To display the Resource as part of the note's content, include an <en-media>
    # tag in the note's ENML content. The en-media tag identifies the corresponding
    # Resource using the MD5 hash.
    hash_hex = binascii.hexlify(hash)

    return _mime, hash_hex


def _guess_mime(url):
    ext = url.split('.')[-1]
    if ext in ['jpg', 'jpeg']:
        return 'image/jpeg'
    elif ext in ['png']:
        return 'image/png'
    else:
        return 'image'
