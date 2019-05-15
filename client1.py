#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import time

#- - - - - - - - - - - - - - - - R S A - - - - - - - - - - - - - - - -

def gcd(a, h):
    #trouver le pgcd de a et h
    while (1):
        temp = a % h
        if (temp == 0):
            return h
            break
        a = h
        h = temp

def publickey(p, q):
    # Premiere partie de la cle publique
    n = p*q

    # Deuxieme partie de la cle publique
    # e pour encrypt
    phi = (p-1)*(q-1)
    e = 2
    while (e < phi):
        # Trouver e tel que e coprime a phi et e<phi
        if (gcd(e, phi) == 1):
            break
        else:
            e += 1
    return [n, e]

def privatekey(p, q, e):
    #regenerer phi
    phi = (p-1)*(q-1)
    # Generer clee privee d comme decrypt
    # d = (1 + k*phi) / e pour k une variable int constante, (ex. k=2)
    k = 2
    d = ( 1 + (k*phi) ) / e
    return d

def encrypt(msg, n, e):
    # Trouver c, le message crypte
    # c = (msg ^ e) % n
    c = pow(msg, e) % n
    return c

def decrypt(c, d, n):
    # msg = (c^d) % n
    m = pow(c, d) % n
    return m

#- - - - - - - - - - - - - - - - SOCKET - - - - - - - - - - - - - - - -

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)

        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()

    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "/quit":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("/quit")
    send()

def setup_rsa(n, e):
    # envoyer au serveur la clef publique et recevoir la clef publique de l'autre client
    client_socket.send(bytes(str(n), "utf8"))
    time.sleep(1)
    client_socket.send(bytes(str(e), "utf8"))
    time.sleep(1)
    n2 = client_socket.recv(BUFSIZ).decode("utf8")
    time.sleep(1)
    e2 = client_socket.recv(BUFSIZ).decode("utf8")
    return [n2, e2]

def rsa_rcv():
    try:
        status = RSA.recv(BUFSIZ).decode("utf8")
        print(status)
    except:
        print("couille")

    if status == "head":
        pass
    else:
        rsapub = publickey(input_p, input_q)
        pubkey = str(rsapub[0]) + ' ' + str(rsapub[1])
        RSA.send(bytes(pubkey, "utf8"))


#- - - - - - - - - - - - - - - - TKINTER - - - - - - - - - - - - - - - -
top = tkinter.Tk()
top.title("J & M messenger")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#- - - - - - - - - - - - - - - - M A I N - - - - - - - - - - - - - - - -

input_p = 164051
input_q = 164057

gen_n, gen_e = publickey(input_p, input_q)
gen_d = privatekey(input_p, input_q, gen_e)

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

RSAPORT = 8081
BUFSIZ = 1024
ADDR = (HOST, PORT)
RSAADDR = (HOST, RSAPORT)

RSA = socket(AF_INET, SOCK_STREAM)
RSA.connect(RSAADDR)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

#client2_n, client_e = setup_rsa(gen_n, gen_e)

receive_thread = Thread(target=receive)
rsa_thread = Thread(target=rsa_rcv)

rsa_thread.start()
receive_thread.start()

tkinter.mainloop()  # Starts GUI execution.
