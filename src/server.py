"""Build Echo Server."""
import socket
import sys


def server():
        """Echo server."""
        try:
            echo_server_sock = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM,
                                             socket.IPPROTO_TCP)
            address = ('127.0.0.1', 5001)
            echo_server_sock.bind(address)
            echo_server_sock.listen(1)
            conn, addr = echo_server_sock.accept()
            buffsize = 8
            response = ""
            msg_len = int(conn.recv(buffsize))
            n = 0
            while n < msg_len:
                response += conn.recv(buffsize).decode('utf8')
                n += buffsize
            response = append_len(response)
            conn.sendall(response.encode('utf8'))
            conn.close()
            echo_server_sock.close()
        except KeyboardInterrupt:
            echo_server_sock.close()
            sys.exit(0)


def append_len(msg):
    """Take a msg and adds a str length to the front of the str."""
    extra_zeros = 8 - len(str(len(msg)))
    return ('0' * extra_zeros) + str(len(msg)) + msg


if __name__ == "__main__":  # pragma: no cover
    server()
