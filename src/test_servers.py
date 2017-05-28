"""Tests for the HTTP Server."""

import pytest


TEST_PARSE = [
    ('PUT google.com HTTP/1.1\r\nHost: localhost\r\n\r\n', ValueError),
    ('GET google.com Quack/1.0\r\nHost: localhost\r\n\r\n', ValueError),
    ('GET google.com HTTP/1.1\r\nHawaiian Host: chocolates\r\n\r\n', ValueError),
    ('GET barf.jpg HTTP/1.1\r\nlocalhost\r\n\r\n', ValueError),
    ('GET HTTP/1.1\r\nHost: localhost\r\n\r\n', ValueError),
    ('GET james.txt HTTP/1.1\r\nHost: localhost\r\n\r\n', NameError)
]


TEST_OK = [
    ('a_web_page.html', b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 125\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n\n<h1>Code Fellows</h1>\n\n<p>A fine place to learn Python web programming!</p>\n\n</body>\n</html>\n\n'),
    ('make_time.py', b'HTTP/1.1 200 OK\r\nContent-Type: text/python\r\nContent-Length: 278\r\n\r\n#!/usr/bin/env python\n\n"""\nmake_time.py\n\nsimple script that returns and HTML page with the current time\n"""\n\nimport datetime\n\ntime_str = datetime.datetime.now().isoformat()\n\nhtml = """\n<http>\n<body>\n<h2> The time is: </h2>\n<p> %s <p>\n</body>\n</http>\n""" % time_str\n\nprint(html)\n'),
    ('sample.txt', b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 95\r\n\r\nThis is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.\n'),
    ('images', b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 174\r\n\r\n<!DOCTYPE html><html><body><h1>File Directory</h1><ul><li>/images/Sample_Scene_Balls.jpg</li><li>/images/sample_1.png</li><li>/images/JPEG_example.jpg</li></ul></body></html>')
]


TEST_ERROR = [
    ('400 Bad Request', b'HTTP/1.1 400 Bad Request\r\n\r\n'),
    ('405 Method Not Allowed', b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'),
    ('505 HTTP Version Not Supported', b'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'),
    ('404 File Not Found', b'HTTP/1.1 404 File Not Found\r\n\r\n')
]


@pytest.mark.parametrize('uri, result', TEST_OK)
def test_client(uri, result):
    """Take a URI, send it, return a well-formatted HTTP response."""
    from client import client
    assert client('GET {} HTTP/1.1\r\nHost: localhost\r\n\r\n'.format(uri)) == result


def test_client_error():
    """Take a bad msg,send it, receive the right error."""
    from client import client
    assert client('PUT google.com HTTP/1.1\r\nHost: localhost\r\n\r\n') == b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'


@pytest.mark.parametrize('msg, result', TEST_OK)
def test_parse_request(msg, result):
    """Parse a good HTTP request."""
    from server import parse_request
    assert parse_request('GET {} HTTP/1.1\r\nHost: localhost\r\n\r\n'.format(msg)) == result


@pytest.mark.parametrize('msg, result', TEST_PARSE)
def test_parse_request_err(msg, result):
    """Parse an error and return the right HTTP error response."""
    from server import parse_request
    with pytest.raises(result):
        parse_request(msg)


@pytest.mark.parametrize('msg, result', TEST_OK)
def test_resolve_uri(msg, result):
    """Take a msg and return a body of requested resource."""
    from server import resolve_uri
    file_type, body_len, body = resolve_uri(msg)
    assert b'HTTP/1.1 200 OK\r\nContent-Type: ' + file_type.encode('utf8') + b'\r\nContent-Length: ' + str(body_len).encode('utf8') + b'\r\n\r\n' + body == result


@pytest.mark.parametrize('msg, result', TEST_OK)
def test_response_ok(msg, result):
    """Take a msg and receive a well-formatted HTTP 200 response."""
    from server import response_ok
    assert response_ok(msg) == result


@pytest.mark.parametrize('msg, result', TEST_ERROR)
def test_response_error(msg, result):
    """Pass in an error and receive the appropriate response."""
    from server import response_error
    assert response_error(msg) == result
