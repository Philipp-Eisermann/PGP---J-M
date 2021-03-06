#Jose & Mehmout messenger; a free messenging app
#    Copyright (C) 2019  Philipp EISERMANN and Elouan GROS

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import *
from threading import Thread
from krypt_lib import *
import tkinter
import time

# - - - - - - - - - - - - - - - - SOCKET - - - - - - - - - - - - - - - -


def receive():
    """Handles receiving of messages."""
    global NAME
    global MSGNB

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8") # receive msg
            
            MSGNB += 1
            dkmsg = devigenere(msg, chr(20))                # decrypts vig cypher

            if NAME in dkmsg[:len(NAME)]:                   # Check if msg comes from user1
                msg_list.insert(tkinter.END, dkmsg)
                msg_list.itemconfig(MSGNB, fg = 'blue')
                                                            # inserts msg on gui
            else:
                msg_list.insert(tkinter.END, dkmsg)
                msg_list.see(tkinter.END)                   # scrolls down

            dkmsg = devigenere(msg, chr(20))                # decrypts vig cypher
         

        except OSError:                                     # Possibly client has left the chat.
            break


def send(event=None):                                       # event is passed by binders.
    """Handles sending of messages."""
    global NAME
    global vigkeyint

    msg = my_msg.get()

    if msg == "/quit":                                      # exits the app
        client_socket.close()
        top.quit()                                          # exits the GUI


    elif msg[:5] == "/name":
        old = NAME
        NAME = msg[6:]
        my_msg.set("")
        client_socket.send(bytes(vigenerechiffr(old + " changed name to " + NAME, chr(vigkeyint)), "utf8"))

    else:
        kmsg = vigenerechiffr(NAME + ": " + msg, chr(vigkeyint))                 # cyphers msg using vig

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
        msg_list.insert(tkinter.END, "If you want to change your name type /name <NAME>.")

        client_socket.send(bytes(vigenerechiffr(NAME, chr(vigkeyint)), "utf8"))

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

        msg_list.insert(tkinter.END, "You are sheep client!")

        msg_list.insert(tkinter.END, "Welcome! If you ever want to quit, type /quit to exit.")
        msg_list.insert(tkinter.END, "If you want to change your name type /name <NAME>.")

        client_socket.send(bytes(vigenerechiffr(NAME, chr(vigkeyint)), "utf8"))
        client_socket.send(bytes(vigenerechiffr(NAME + " joined the chat!", chr(vigkeyint)), "utf8"))

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
NAME = getfqdn()

MSGNB = 2


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
