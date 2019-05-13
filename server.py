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
        print("%s:%s has connected." % client_address)

        if not addresses:
            client.send(bytes("You are head client!!", "utf8"))
            rsa.send(bytes("head", "utf8"))
            HEAD = rsa
        else:
            rsa.send(bytes("sheep", "utf8"))
            pubkey = rsa.recv(BUFSIZ).decode("utf8")
            print(ord(pubkey[0]), ' ', ord(pubkey[1]))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(client, client_address):  # Takes client socket as argument.
    """Handles a single client connection."""

    client.send(bytes("Hi, what's your name?", "utf8"))
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type /quit to exit.' % name

    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))

    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)

        if msg != bytes("/quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break



def broadcast(msg, prefix=""):  # prefix is for name identification.
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

<<<<<<< HEAD


HOST = '172.20.10.4'
PORT = 5566
RSAPORT = 8080
=======
HOST = ''
PORT = 8080
RSAPORT = 8081
>>>>>>> e82148418105d98bed65d90b788d6ca4080eafe1
BUFSIZ = 1024
ADDR = (HOST, PORT)
RSAADDR = (HOST, RSAPORT)

SERVER = socket(AF_INET, SOCK_STREAM)
#RSA = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
#RSA.bind(RSAADDR)



if __name__ == "__main__":
    SERVER.listen(5)
    #RSA.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    RSA.close()
