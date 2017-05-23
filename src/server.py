"""Build Echo Server."""
import socket
import sys


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
                response = ""
                msg_len = conn.recv(buffsize).decode('utf8')
                if msg_len is not '':
                    msg_len = int(msg_len)
                    n = 0
                    while n < msg_len:
                        response += conn.recv(buffsize).decode('utf8')
                        n += buffsize
                    print(response)
                    response = append_len(response_ok()).encode('utf8')
                    conn.sendall(response)
                    conn.close()
                else:
                    continue
            except KeyboardInterrupt:
                break
        echo_server_sock.close()
        sys.exit(0)


def response_ok():
    """Return a properly formatted HTTP 200 OK."""
    return 'HTTP/1.1 200 OK'


def response_error():
    """Return a properly formatted HTTP 500 Internal Server Error."""
    return 'HTTP/1.1 500 Internal Server Error'


def append_len(msg):
    """Take a msg and adds a str length to the front of the str."""
    extra_zeros = 8 - len(str(len(msg)))
    return ('0' * extra_zeros) + str(len(msg)) + msg


if __name__ == "__main__":  # pragma: no cover
    server()
