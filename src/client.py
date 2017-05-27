"""Simple Echo Socket Client."""


import socket


def client(msg):
    """Send server a message, receives another msg, and returns it."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    cli_sock = socket.socket(*stream_info[:3])
    cli_sock.connect(stream_info[-1])
    msg = msg.encode('utf8')
    cli_sock.sendall(msg)
    buffsize = 8
    response = ''.encode('utf8')
    while True:
        response += cli_sock.recv(buffsize)
        temp_res = response
        if b'\r\n\r\n' in temp_res and b'200' not in temp_res.split(b'\r\n')[0]:
            break
        elif b'\r\n\r\n' in temp_res and b'Content-Length: ' in temp_res:
            msg_len = int(temp_res.split(b'Content-Length: ')[1].split(b'\r\n')[0])
            if len(temp_res.split(b'\r\n\r\n')[1]) >= msg_len:
                break
    cli_sock.close()
    return response


if __name__ == '__main__':  # pragma: no cover
    msg = 'GET sample.txt HTTP/1.1\r\nHost: localhost\r\n\r\n'
    print('Sent: ' + msg)
    print('Received: ' + client(msg))
