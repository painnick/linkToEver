import json
import httplib
import urllib

PARSER_HOST = 'www.readability.com'
PARSER_URL = '/api/content/v1/parser'
AUTH_TOKEN = None


class ParseError(Exception):

    def __init__(self, response):
        self.response = response

    def __str__(self):
        return '%d - %s' % (self.response.status, self.response.reason)


def parse(url):
    _conn = httplib.HTTPSConnection(PARSER_HOST)
    _params = {
        'url': url,
        'token': AUTH_TOKEN
    }
    _query_string = urllib.urlencode(_params)
    _conn.request('GET', PARSER_URL + '?' + _query_string)
    _res = _conn.getresponse()

    if _res.status != 200:
        raise ParseError(_res)
    else:
        jsonObj = json.loads(_res.read().decode('utf-8'), "UTF-8")
        return jsonObj['content']


if __name__ == '__main__':

    _result = parse('http://blog.weirdx.io/post/27142')

    print _result