#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from vigenere_lib import *
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
            print(vigkey)
            dkmsg = devigenere(msg, chr(20))
            msg_list.insert(tkinter.END, dkmsg)
            msg_list.see(tkinter.END)

        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()

    if msg == "/quit":
        client_socket.close()
        top.quit()
    else:
        kmsg = vigenerechiffr(msg, chr(20)) # message chiffre en vigenere
        print(vigkey)
        print(msg, ' ', kmsg)

        my_msg.set("")  # Clears input field.
        client_socket.send(bytes(kmsg, "utf8"))



def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("/quit")
    send()

def key_setup():
    vigkey = 20
    # envoyer au serveur la clef publique et recevoir la clef publique de l'autre client
    #client_socket.send(bytes(str(n), "utf8"))
    #time.sleep(1)
    #client_socket.send(bytes(str(e), "utf8"))
    #time.sleep(1)
    #n2 = client_socket.recv(BUFSIZ).decode("utf8")
    #time.sleep(1)
    #e2 = client_socket.recv(BUFSIZ).decode("utf8")
    #return [n2, e2]



def rsa_status():
    vigkeyint = 20
    try:
        status = RSA.recv(BUFSIZ).decode("utf8")
        print(status)
    except:
        print("couille")
        return 0

    if status == "head":
        msg_list.insert(tkinter.END, "You are head client!")
        msg_list.insert(tkinter.END, "Welcome! If you ever want to quit, type /quit to exit.")
        msg_list.insert(tkinter.END, "What is your name?")
        while True:
            pubkey2 = RSA.recv(BUFSIZ).decode("utf8") #recevoir la clepub du sheep via le serv
            pubkey2_s = pubkey2.split(' ') #decomposer la cle
            pubkey2_s_n = int(pubkey2_s[0])
            pubkey2_s_e = int(pubkey2_s[1])
            rsavigkey = encrypt(vigkeyint, pubkey2_s_n, pubkey2_s_e) #msg, n, e
            print(str(rsavigkey))
            RSA.send(bytes(str(rsavigkey), "utf8")) # envoyer au serveur

    else:
        rsapub_n, rsapub_e = publickey(input_p, input_q) #p, q
        rsapriv = privatekey(input_p, input_q, rsapub_e) #p, q, e
        print(str(rsapub_n) + " " + str(rsapub_e))
        pubkey = str(rsapub_n) + ' ' + str(rsapub_e)
        print("be")
        RSA.send(bytes(pubkey, "utf8")) #sheep envoie la cle publique au serveur
        print("af")
        time.sleep(1)
        rsavigkey = RSA.recv(BUFSIZ).decode("utf8") #sheep recoit vigkey du head
        print("c: " + rsavigkey)
        print("d: " + str(rsapriv))
        print("n: " + str(rsapub_n))
        vigkey = decrypt(int(rsavigkey), int(rsapriv), rsapub_n) #c, d, n !!! Attention les variables doivent toutes etre des int, pas de float !!!
        print(str(vigkey))
        msg_list.insert(tkinter.END, "Welcome! If you ever want to quit, type /quit to exit.")
        msg_list.insert(tkinter.END, "What is your name?")
        return vigkey


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

input_p = 53
input_q = 59
vigkey = "thisisthekey"
vigkeyint = 20

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
rsastatus_thread = Thread(target=rsa_status)
keysetup_thread = Thread(target=key_setup)

rsastatus_thread.start()
receive_thread.start()

tkinter.mainloop()  # Starts GUI execution.
