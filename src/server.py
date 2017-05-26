"""Build Echo Server."""
import socket
import sys
from os import walk, path


def server():  # pragma: no cover
        """Echo server."""
        echo_server_sock = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM,
                                         socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5000)
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


def response_ok(uri):
    """Return a properly formatted HTTP 200 OK."""
    file_type, body_len, body = resolve_uri(uri)
    msg = b'HTTP/1.1 200 OK\r\nContent-Type: ' + file_type.encode('utf8') + b'\r\nContent-Length: ' + str(body_len).encode('utf8') + b'\r\n\r\n' + body
    return msg


def resolve_uri(uri):
    """Return a body of requested resource."""
    if uri.startswith('/'):
        uri = uri[1:]
    file_path = path.realpath(__file__).replace('server.py', '../webroot')
    the_file = path.join(file_path, uri)
    if path.isdir(the_file):
        # Partially stolen from Stack Overflow and rewritten heavily
        file_dir = []
        for dp, dn, fn in walk(the_file):
            for f in fn:
                file_dir.append(path.join(dp, f).replace(file_path, ''))
        html_start = '<!DOCTYPE html><html><body><h1>File Directory</h1><ul>'
        html_end = '</ul></body></html>'
        for file in file_dir:
            html_start += '<li>{}</li>'.format(file)
        the_body = (html_start + html_end).encode('utf8')
        file_size = len(the_body)
        file_type = 'text/html; charset=utf-8'
    elif path.isfile(the_file):
        file_size = path.getsize(the_file)
        the_body = open(the_file, "rb").read()
        if uri.lower().endswith(".html"):
            file_type = "text/html; charset=utf-8"
        elif uri.lower().endswith(".txt"):
            file_type = "text/plain; charset=utf-8"
        elif uri.lower().endswith('.py'):
            file_type = 'text/python'
        elif uri.lower().endswith(".jpg"):
            file_type = "image/jpeg"
        elif uri.lower().endswith(".png"):
            file_type = "image/png"
    else:
        raise NameError('404 File Not Found')
    return file_type, file_size, the_body


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
