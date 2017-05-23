"""Tests for the Echo Server."""

import pytest


TEST_ECHO = [
    ('Hey, how ya, doing?'),
    ('Short'),
    ('buffsize'),
    ('James Feore'),
    ('Ophelia Yin'),
    ('Testing testing testing'),
    ('Here is a much longer one to test with. It\'s super long.')
]


TEST_APPEND = [
    ('Hey, how ya, doing?', '00000019Hey, how ya, doing?'),
    ('James Feore', '00000011James Feore'),
    ('Ophelia Yin', '00000011Ophelia Yin'),
    ('Testing testing testing', '00000023Testing testing testing'),
    ('Here is a much longer one to test with. It\'s super long.', '00000056Here is a much longer one to test with. It\'s super long.')
]


@pytest.mark.parametrize('msg', TEST_ECHO)
def test_client(msg):
    """Take a msg,send it, return that same message."""
    from client import client
    assert client(msg) == 'HTTP/1.1 200 OK'


def test_response_ok():
    """Take a msg,send it, return that same message."""
    from server import response_ok
    assert response_ok() == 'HTTP/1.1 200 OK'


def test_response_error():
    """Take a msg,send it, return that same message."""
    from server import response_error
    assert response_error() == 'HTTP/1.1 500 Internal Server Error'


@pytest.mark.parametrize('msg, result', TEST_APPEND)
def test_append_len(msg, result):
    """Take a msg and add its length in front of it."""
    from client import append_len
    assert append_len(msg) == result
