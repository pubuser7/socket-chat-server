#!/usr/bin/python
import socket
import select
import sys

HOST = '127.0.0.1'
SOCKETS_LIST = []
RECV_BUFFER = 4096
PORT = 9009


def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKETS_LIST.append(server_socket)

    print("[!] Chat server started on {}:{}".format(HOST, PORT))

    while True:
        ready_to_read, ready_to_write, in_error = select.select(SOCKETS_LIST, [], [], 0)

        for sock in ready_to_read:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKETS_LIST.append(sockfd)
                print ("[+] Client (%s:%s) connected" % addr)

                broadcast(server_socket, sockfd, "[%s:%s] Joined chat room\n" % addr)

            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        if sock in SOCKETS_LIST:
                            SOCKETS_LIST.remove(sock)

                        broadcast(server_socket, sock, "[-] Client (%s:%s) is offline\n" % addr)

                except:
                    broadcast(server_socket, sock, "[-] Client (%s:%s) is offline\n" % addr)
                    continue

    server_socket.close()


def broadcast(server_socket, sock, message):
    for socket in SOCKETS_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                if socket in SOCKETS_LIST:
                    SOCKETS_LIST.remove(socket)


if __name__ == "__main__":
    sys.exit(chat_server())
