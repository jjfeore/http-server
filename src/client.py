"""Simple Echo Socket Client."""


import socket


def client(msg):
    """Send server a message, receives another msg, and returns it."""
    infos = socket.getaddrinfo('127.0.0.1', 5005)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    cli_sock = socket.socket(*stream_info[:3])
    cli_sock.connect(stream_info[-1])
    msg = append_len(msg).encode('utf8')
    cli_sock.sendall(msg)
    buffsize = 8
    response = ''
    msg_len = int(cli_sock.recv(buffsize))
    n = 0
    while n < msg_len:
        response += cli_sock.recv(buffsize).decode('utf8')
        n += buffsize
    cli_sock.shutdown(socket.SHUT_RD)
    cli_sock.close()
    return response


def append_len(msg):
    """Take a msg and adds a str length to the front of the str."""
    extra_zeros = 8 - len(str(len(msg)))
    return ('0' * extra_zeros) + str(len(msg)) + msg


if __name__ == '__main__':  # pragma: no cover
    msg = 'Hello. How are you doing?'
    print('Sent: ' + msg)
    print('Received: ' + client(msg))
