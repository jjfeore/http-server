"""Tests for the Echo Server."""

import pytest


TEST_PARSE = [
    ('GET google.com HTTP/1.1\r\nHost: localhost\r\n\r\nHere\'s a message', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\ngoogle.com\r\n\r\n'),
    ('PUT google.com HTTP/1.1\r\nHost: localhost\r\n\r\nHere\'s a message', 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'),
    ('GET google.com Quack/1.0\r\nHost: localhost\r\n\r\nHere\'s a message', 'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n'),
    ('GET google.com HTTP/1.1\r\nHawaiian Host: chocolates\r\n\r\nHere\'s a message', 'HTTP/1.1 400 Bad Request\r\n\r\n'),
    ('GET HTTP/1.1\r\nHost: localhost\r\n\r\nHere\'s a message', 'HTTP/1.1 400 Bad Request\r\n\r\n')
]


TEST_OK = [
    ('hello', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhello\r\n\r\n'),
    ('buffsize', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nbuffsize\r\n\r\n'),
    ('James Feore', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nJames Feore\r\n\r\n'),
    ('Ophelia Yin', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOphelia Yin\r\n\r\n'),
    ('Testing testing testing', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nTesting testing testing\r\n\r\n'),
    ('!@#$^^&', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n!@#$^^&\r\n\r\n')
]


TEST_ERROR = [
    ('400 Bad Request', 'HTTP/1.1 400 Bad Request\r\n\r\n'),
    ('405 Method Not Allowed', 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'),
    ('505 HTTP Version Not Supported', 'HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n')
]


@pytest.mark.parametrize('msg, result', TEST_PARSE)
def test_client(msg, result):
    """Take a msg,send it, return that same message."""
    from client import client
    assert client(msg) == result


@pytest.mark.parametrize('msg, result', TEST_PARSE)
def test_parse_request(msg, result):
    """Take a msg,send it, return that same message."""
    from server import parse_request
    assert parse_request(msg) == result


@pytest.mark.parametrize('msg, result', TEST_OK)
def test_response_ok(msg, result):
    """Take a msg,send it, return that same message."""
    from server import response_ok
    assert response_ok(msg) == result.encode('utf8')


@pytest.mark.parametrize('msg, result', TEST_ERROR)
def test_response_error(msg, result):
    """Pass in an error and receive the appropriate response."""
    from server import response_error
    assert response_error(msg) == result.encode('utf8')
