"""Tests for the Echo Server."""

import pytest


TEST_ECHO = [
    ('Hey, how ya, doing?'),
    ('Short'),
    ('buffsize'),
    ('James Feore'),
    ('Ophelia Yin'),
    ('Testing testing testing'),
    ('Here is a much longer one to test with. It\'s super long.'),
    ('!@#$^^&'),
    ('words \r\n\r\n words')
]


@pytest.mark.parametrize('msg', TEST_ECHO)
def test_client(msg):
    """Take a msg,send it, return that same message."""
    from client import client
    assert client(msg) == 'HTTP/1.1 200 OK\r\n\r\n'


def test_response_ok():
    """Take a msg,send it, return that same message."""
    from server import response_ok
    assert response_ok() == b'HTTP/1.1 200 OK\r\n\r\n'


def test_response_error():
    """Take a msg,send it, return that same message."""
    from server import response_error
    assert response_error() == b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
