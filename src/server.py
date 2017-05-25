"""Build Echo Server."""
import socket
import sys
import io
from os import listdir


def server():  # pragma: no cover
        """Echo server."""
        echo_server_sock = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM,
                                         socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5003)
        echo_server_sock.bind(address)
        echo_server_sock.listen(1)
        while True:
            try:
                conn, addr = echo_server_sock.accept()
                buffsize = 8
                response = b''
                keep_parsing = True
                while keep_parsing:
                    response += conn.recv(buffsize)
                    temp_res = response.decode('utf8')
                    if temp_res == '' or temp_res.endswith('\r\n\r\n'):
                        response = response.decode('utf8')
                        keep_parsing = False
                print(response)
                try:
                    conn.sendall(parse_request(response))
                    conn.close()
                except ValueError as err:
                    conn.sendall(response_error(err.args[0]))
                    conn.close()
            except KeyboardInterrupt:
                break
        echo_server_sock.close()
        sys.exit(0)


def response_ok(msg):
    """Return a properly formatted HTTP 200 OK."""
    body = resolve_uri(msg)
    if msg.lower().endswith(".html") or not msg.includes("."):
        file_type = "text/html"
    elif msg.lower().endswith(".txt") or msg.lower().endswith(".py"):
        file_type = "text/plain"
    elif msg.lower().endswith(".jpg"):
        file_type = "image/jpeg"
    elif msg.lower().endswith(".png"):
        file_type = "image/png"
    body_len = str(len(body))
    msg = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}'.format(file_type, body, body_len)
    return msg.encode('utf8')


def resolve_uri(uri):
    """Return a body of requested resource."""
    root_dir = "../webroot"
    uri = 


def response_error(code):
    """Return a properly formatted HTTP error response."""
    return ('HTTP/1.1 ' + code + '\r\n\r\n').encode('utf8')


def parse_request(request):
    """Parse a request and return either a good response or an error."""
    request = request.split("\r\n")
    if request[0].startswith('GET'):
        if request[0].endswith('HTTP/1.1'):
            if request[1].startswith('Host: '):
                uri = request[0].replace('GET ', '').replace(' HTTP/1.1', '').replace('HTTP/1.1', '')
                if uri:
                    return response_ok(uri)
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
