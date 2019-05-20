#!/usr/bin/python
import socket
import select
import sys


def chat_client():
    if(len(sys.argv) < 3):
        print('Usage : python chat_client.py HOST PORT')
        sys.exit()

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.settimeout(2)

    try:
        socket_server.connect((HOST, PORT))
    except:
        print('[-] Can not connect to the server make sure HOST and PORT are right and the server is running.')
        sys.exit()

    print('[+] Connected to remote host {}:{}'.format(HOST, PORT))
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, socket_server]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == socket_server:
                data = sock.recv(4096)
                if not data:
                    print ('\n[-] Disconnected from server.')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

            else:
                msg = sys.stdin.readline()
                socket_server.send(msg)
                sys.stdout.write('[Me] ')
                sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(chat_client())
