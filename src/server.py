"""Build Echo Server."""
import socket
import sys


def server():  # pragma: no cover
        """Echo server."""
        echo_server_sock = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM,
                                         socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5002)
        echo_server_sock.bind(address)
        echo_server_sock.listen(1)
        while True:
            try:
                conn, addr = echo_server_sock.accept()
                buffsize = 8
                response = ''
                keep_parsing = True
                while keep_parsing:
                    response += conn.recv(buffsize).decode('utf8')
                    if response == '' or response.endswith('\r\n\r\n'):
                        keep_parsing = False
                print(response)
                try:
                    conn.sendall(parse_request(response))
                    conn.close()
                except ValueError as err:
                    conn.sendall(response_error(err.args[0]))
                    conn.close()
                    pass
            except KeyboardInterrupt:
                break
        echo_server_sock.close()
        sys.exit(0)


def response_ok(msg):
    """Return a properly formatted HTTP 200 OK."""
    msg = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n' + msg + '\r\n\r\n'
    return msg.encode('utf8')


def response_error(code):
    """Return a properly formatted HTTP error response."""
    return ('HTTP/1.1 ' + code + '\r\n\r\n').encode('utf8')


def parse_request(request):
    """Parse a request and return either a good response or an error."""
    request = request.split("\r\n")
    if request[0].startswith('GET'):
        if request[0].endswith('HTTP/1.1'):
            if request[1].startswith('Host: '):
                ret_msg = request[0].replace('GET ', '').replace(' HTTP/1.1', '')
                if ret_msg:
                    return response_ok(ret_msg)
                else:
                    raise ValueError('400 Bad Request')
            else:
                raise ValueError('400 Bad Request')
        else:
            raise ValueError('505 HTTP Version Not Supported')
    else:
        raise ValueError('405 Method Not Allowed')


if __name__ == "__main__":  # pragma: no cover
    server()
