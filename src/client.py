"""Simple Echo Socket Client."""


import socket


def client(msg):
    """Send server a message, receives another msg, and returns it."""
    infos = socket.getaddrinfo('127.0.0.1', 5003)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    cli_sock = socket.socket(*stream_info[:3])
    cli_sock.connect(stream_info[-1])
    msg = (msg + '\r\n\r\n').encode('utf8')
    cli_sock.sendall(msg)
    buffsize = 8
    response = b''
    keep_parsing = True
    while keep_parsing:
        response += cli_sock.recv(buffsize)
        temp_res = response.decode('utf8')
        if temp_res.endswith('\r\n\r\n'):
            response = response.decode('utf8')
            keep_parsing = False
    cli_sock.close()
    return response


if __name__ == '__main__':  # pragma: no cover
    msg = 'Hello. How are you doing?'
    print('Sent: ' + msg)
    print('Received: ' + client(msg))
