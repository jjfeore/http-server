"""Build Echo Server."""
import socket
import sys


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
                response = ''
                keep_parsing = True
                while keep_parsing:
                    response += conn.recv(buffsize).decode('utf8')
                    if response == '' or response.endswith('\r\n\r\n'):
                        keep_parsing = False
                print(response)
                conn.sendall(response_ok())
                conn.close()
            except KeyboardInterrupt:
                break
        echo_server_sock.close()
        sys.exit(0)


def response_ok():
    """Return a properly formatted HTTP 200 OK."""
    return b'HTTP/1.1 200 OK\r\n\r\n'


def response_error():
    """Return a properly formatted HTTP 500 Internal Server Error."""
    return b'HTTP/1.1 500 Internal Server Error\r\n\r\n'


if __name__ == "__main__":  # pragma: no cover
    server()
