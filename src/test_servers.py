"""Tests for the HTTP Server."""

import pytest


fa = open("webroot/a_web_page.html", "rb").read()
fb = open("webroot/make_time.py", "rb").read()
fc = open("webroot/sample.txt", "rb").read()
fd = open("webroot/images/JPEG_example.jpg", "rb").read()
fe = open("webroot/images/sample_1.png", "rb").read()
ff = open("webroot/images/Sample_Scene_Balls.jpg", "rb").read()


# TEST_PARSE = [
#     ('PUT google.com HTTP/1.1\r\nHost: localhost\r\n\r\n', ValueError),
#     ('GET google.com Quack/1.0\r\nHost: localhost\r\n\r\n', ValueError),
#     ('GET google.com HTTP/1.1\r\nHawaiian Host: chocolates\r\n\r\n', ValueError),
#     ('GET HTTP/1.1\r\nHost: localhost\r\n\r\n', ValueError),
#     ('GET james.txt HTTP/1.1\r\nHost: localhost\r\n\r\n', NameError)
# ]


TEST_OK = [
    ('a_web_page.html', b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 125\r\n\r\n' + fa),
    ('make_time.py', b'HTTP/1.1 200 OK\r\nContent-Type: text/python\r\nContent-Length: 278\r\n\r\n' + fb),
    ('sample.txt', b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 95\r\n\r\n' + fc),
    ('images/JPEG_example.jpg', b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: 15138\r\n\r\n' + fd),
    ('images/sample_1.png', b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nContent-Length: 8760\r\n\r\n' + fe),
    ('images/Sample_Scene_Balls.jpg', b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: 146534\r\n\r\n' + ff),
    ('/images/Sample_Scene_Balls.jpg', b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: 146534\r\n\r\n' + ff)
]


# TEST_ERROR = [
#     ('400 Bad Request', 'HTTP/1.1 400 Bad Request\r\n\r\n'),
#     ('405 Method Not Allowed', 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'),
#     ('505 HTTP Version Not Supported', 'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n')
# ]


@pytest.mark.parametrize('uri, result', TEST_OK)
def test_client(uri, result):
    """Take a URI, send it, return a well-formatted HTTP response."""
    from client import client
    assert client('GET {} HTTP/1.1\r\nHost: localhost\r\n\r\n'.format(uri)) == result


# def test_client_error():
#     """Take a bad msg,send it, receive the right error."""
#     from client import client
#     assert client('PUT google.com HTTP/1.1\r\nHost: localhost\r\n\r\nHere\'s a message') == 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'


# def test_parse_request():
#     """Parse a good HTTP request."""
#     from server import parse_request
#     assert parse_request('GET google.com HTTP/1.1\r\nHost: localhost\r\n\r\nHere\'s a message').decode('utf8') == 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\ngoogle.com\r\n\r\n'


# @pytest.mark.parametrize('msg, result', TEST_PARSE)
# def test_parse_request_err(msg, result):
#     """Parse an error and return the right HTTP error response."""
#     from server import parse_request
#     with pytest.raises(result):
#         parse_request(msg)


# @pytest.mark.parametrize('msg, result', TEST_OK)
# def test_resolve_uri(msg, result):
#     """Take a msg and return a body of requested resource."""
#     from server import resolve_uri
#     assert resolve_uri(msg) == result


# @pytest.mark.parametrize('msg, result', TEST_OK)
# def test_response_ok(msg, result):
#     """Take a msg and receive a well-formatted HTTP 200 response."""
#     from server import response_ok
#     assert response_ok(msg) == result


# @pytest.mark.parametrize('msg, result', TEST_ERROR)
# def test_response_error(msg, result):
#     """Pass in an error and receive the appropriate response."""
#     from server import response_error
#     assert response_error(msg) == result.encode('utf8')
