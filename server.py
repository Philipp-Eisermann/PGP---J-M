#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        rsa, rsa_address = RSA.accept()
        # print("%s:%s has connected." % client_address)

        if not addresses:
            # client.send(bytes("You are head client!!", "utf8"))
            rsa.send(bytes("head", "utf8"))
            HEAD = rsa
        else:
            rsa.send(bytes("sheep", "utf8"))
            time.sleep(1)
            pubkey = rsa.recv(BUFSIZ).decode("utf8")                # sheep's pubkey

            HEAD.send(bytes(pubkey, "utf8"))

            rsavigkey = HEAD.recv(BUFSIZ).decode("utf8")            # head's vigkey

            rsa.send(bytes(rsavigkey, "utf8"))                      # send vigkey to sheep
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()  # starts thread to handle client


def handle_client(client, client_address):                          # Takes client socket as argument.
    """Handles a single client connection."""

    # client.send(bytes("Hi, what's your name?", "utf8"))
    name = client.recv(BUFSIZ).decode("utf8")
    # welcome = 'Welcome %s! If you ever want to quit, type /quit to exit.' % name

    # client.send(bytes(welcome, "utf8"))
    # msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))                                   # send messages to all client

    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)

        if msg != bytes("/quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))  # send messages to all clients
            break


def broadcast(msg, prefix=""):                                        # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


def rsa():
    return 0
    #client2_n = client.recv(BUFSIZ).decode("utf8")
    #print(str(client1_n))
    #client2_e = client.recv(BUFSIZ).decode("utf8")
    #print(str(client1_e))
    #client.send(bytes(client1_n, "utf8"))
    #time.sleep(1)
    #client.send(bytes(client1_e, "utf8"))


clients = {}
addresses = {}
HEAD = socket()
rsa_addresses = {}

HOST = ''
PORT = 8080
RSAPORT = 8081
BUFSIZ = 1024

# sets up addresses
ADDR = (HOST, PORT)
RSAADDR = (HOST, RSAPORT)

# sets up sockets
SERVER = socket(AF_INET, SOCK_STREAM)
RSA = socket(AF_INET, SOCK_STREAM)

# binds addresses to sockets
SERVER.bind(ADDR)
RSA.bind(RSAADDR)


if __name__ == "__main__":
    # sockets to listening mode
    SERVER.listen(5)
    RSA.listen(5)
    print("Waiting for connection...")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)              # sets up accept thread
    ACCEPT_THREAD.start()                                                   # starts accept thread
    ACCEPT_THREAD.join()                                                    # waits for accept thread to stop

    # close sockets
    SERVER.close()
    RSA.close()
