"""Build Echo Server."""
import socket
import sys
from os import walk, path


def server():  # pragma: no cover
        """Echo server."""
        echo_server_sock = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM,
                                         socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5004)
        echo_server_sock.bind(address)
        echo_server_sock.listen(1)
        while True:
            try:
                conn, addr = echo_server_sock.accept()
                buffsize = 8
                response = b''
                while True:
                    response += conn.recv(buffsize)
                    temp_res = response.decode('utf8')
                    if temp_res == '' or temp_res.endswith('\r\n\r\n'):
                        response = response.decode('utf8')
                        break
                print(response)
                try:
                    conn.sendall(parse_request(response))
                    conn.close()
                except ValueError as err:
                    conn.sendall(response_error(err.args[0]))
                    conn.close()
                except NameError as err:
                    conn.sendall(response_error(err.args[0]))
                    conn.close()
            except KeyboardInterrupt:
                break
        echo_server_sock.close()
        sys.exit(0)


def response_ok(msg):
    """Return a properly formatted HTTP 200 OK."""
    body = resolve_uri(msg)
    if msg.lower().endswith(".html") or msg.endswith("/"):
        file_type = "text/html"
    elif msg.lower().endswith(".txt") or msg.lower().endswith(".py"):
        file_type = "text/plain"
    elif msg.lower().endswith(".jpg"):
        file_type = "image/jpeg"
    elif msg.lower().endswith(".png"):
        file_type = "image/png"
    body_len = str(len(body))
    msg = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}'.format(file_type, body_len, body)
    return msg.encode('utf8')


def resolve_uri(uri):
    """Return a body of requested resource."""
    root_dir = "../webroot/"
    if uri.endswith('/'):
        # Partially stolen from Stack Overflow and rewritten heavily
        file_dir = []
        for dp, dn, fn in walk('../webroot/'):
            for f in fn:
                file_dir.append(path.join(dp, f).replace(root_dir, ''))
        html_start = '<!DOCTYPE html><html><body><h1>File Directory</h1><ul>'
        html_end = '</ul></body></html>'
        for file in file_dir:
            html_start += '<li>{}</li>'.format(file)
        return html_start + html_end
    elif path.isfile(root_dir + uri):
        the_file = root_dir + uri
        return open(the_file, "rb").read().decode('utf8')
    else:
        raise NameError('404 File Not Found')


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
