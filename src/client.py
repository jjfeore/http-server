"""Simple Echo Socket Client."""


import socket


def client(msg):
    """Send server a message, receives another msg, and returns it."""
    infos = socket.getaddrinfo('127.0.0.1', 5002)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    cli_sock = socket.socket(*stream_info[:3])
    cli_sock.connect(stream_info[-1])
    msg = msg.encode('utf8')
    cli_sock.sendall(msg)
    buffsize = 8
    response = b''
    while True:
        response += cli_sock.recv(buffsize)
        temp_res = response.decode('utf8')
        if '\r\n\r\n' in temp_res and '200' not in temp_res.split('\r\n')[0]:
            response = temp_res
            break
        elif '\r\n\r\n' in temp_res and 'Content-Length: ' in temp_res:
            msg_len = int(temp_res.split('Content-Length: ')[1].split('\r\n')[0])
            if len(temp_res.split('\r\n\r\n')[1]) >= msg_len:
                response = temp_res
                break
    cli_sock.close()
    return response


if __name__ == '__main__':  # pragma: no cover
    msg = 'GET sample.txt HTTP/1.1\r\nHost: localhost\r\n\r\n'
    print('Sent: ' + msg)
    print('Received: ' + client(msg))
