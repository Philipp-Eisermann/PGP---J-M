#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from vigenere_lib import *
import tkinter
import time

# - - - - - - - - - - - - - - - - SOCKET - - - - - - - - - - - - - - - -


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8") # receive msg
            dkmsg = devigenere(msg, chr(20))                # decrypts vig cypher
            msg_list.insert(tkinter.END, dkmsg)             # inserts msg on gui
            msg_list.see(tkinter.END)                       # scrolls down

        except OSError:                                     # Possibly client has left the chat.
            break


def send(event=None):                                       # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()

    if msg == "/quit":                                      # exits the app
        client_socket.close()
        top.quit()                                          # exits the GUI

    else:
        kmsg = vigenerechiffr(msg, chr(20))                 # cyphers msg using vig

        my_msg.set("")                                      # Clears input field.
        client_socket.send(bytes(kmsg, "utf8"))             # sends msg to server for distribution


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("/quit")                                     # calls the msg == "/quit" routine
    send()


def key_setup():
    """Sets up the RSA cyphering"""
    vigkey = 20


def rsa_status():
    """This function handles the sharing of cypher keys"""
    vigkeyint = 20
    try:
        status = RSA.recv(BUFSIZ).decode("utf8")            # rcv status from Server
        print(status)
    except:
        print("problem!")                                   # if status not received, throw error
        return 0

    if status == "head":

        # greeting messages
        msg_list.insert(tkinter.END, "You are head client!")
        msg_list.insert(tkinter.END, "Welcome! If you ever want to quit, type /quit to exit.")
        msg_list.insert(tkinter.END, "What is your name?")

        while True:
            pubkey2 = RSA.recv(BUFSIZ).decode("utf8")       # rcv pubkey from sheep via server

            pubkey2_s = pubkey2.split(' ')                  # prepare received key for usage
            pubkey2_s_n = int(pubkey2_s[0])
            pubkey2_s_e = int(pubkey2_s[1])

            rsavigkey = encrypt(vigkeyint, pubkey2_s_n, pubkey2_s_e) #msg, n, e
            RSA.send(bytes(str(rsavigkey), "utf8")) # envoyer au serveur

    else:
        rsapub_n, rsapub_e = publickey(input_p, input_q)    # p, q
        rsapriv = privatekey(input_p, input_q, rsapub_e)    # p, q, e

        pubkey = str(rsapub_n) + ' ' + str(rsapub_e)
        RSA.send(bytes(pubkey, "utf8"))                     # sheep sends pubkey to server
        time.sleep(1)

        rsavigkey = RSA.recv(BUFSIZ).decode("utf8")         # sheep rcv vigkey from head, via serv
        vigkey = decrypt(int(rsavigkey), int(rsapriv), rsapub_n)  # c, d, n !! All variables should be int, not float !!

        # greeting messages
        msg_list.insert(tkinter.END, "Welcome! If you ever want to quit, type /quit to exit.")
        msg_list.insert(tkinter.END, "What is your name?")
        return vigkey


# - - - - - - - - - - - - - - - - TKINTER - - - - - - - - - - - - - - - -
top = tkinter.Tk()
top.title("J & M messenger")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()                                # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)               # To navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=send)    # calls send on push of button
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# - - - - - - - - - - - - - - - - M A I N - - - - - - - - - - - - - - - -

input_p = 53
input_q = 59
vigkey = "thisisthekey"
vigkeyint = 20

gen_n, gen_e = publickey(input_p, input_q)                      # RSA pub setup
gen_d = privatekey(input_p, input_q, gen_e)                     # RSA private setup

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:                                                    # default value
    PORT = 33000
else:
    PORT = int(PORT)

RSAPORT = 8081
BUFSIZ = 1024

# sets up addresses
ADDR = (HOST, PORT)
RSAADDR = (HOST, RSAPORT)

# sets up RSA socket
RSA = socket(AF_INET, SOCK_STREAM)
RSA.connect(RSAADDR)

# sets up client socket
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# client2_n, client_e = setup_rsa(gen_n, gen_e)

# sets up the threads
receive_thread = Thread(target=receive)
rsastatus_thread = Thread(target=rsa_status)
keysetup_thread = Thread(target=key_setup)

# runs the threads
rsastatus_thread.start()
receive_thread.start()

tkinter.mainloop()                                              # Starts GUI execution.
