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
    print(str(n),str(e))
    return [n, e]


def privatekey(p, q, e):
    #regenerer phi
    phi = (p-1)*(q-1)
    # Generer clee privee d comme decrypt
    # d = (1 + k*phi) / e pour k une variable int constante, (ex. k=2)
    k = 2
    d = ( 1 + (k*phi) ) / e
    print(str(d))
    return d


def encrypt(msg, n, e):
    # Trouver c, le message crypte
    # c = (msg ^ e) % n
    c = pow(msg, e) % n
    print(str(pow(msg,e) % n))
    return c


def decrypt(c, d, n):
    # msg = (c^d) % n
    m = pow(c, d) % n
    return m


input_p = 53
input_q = 59
message = 20

gen_n, gen_e = publickey(input_p, input_q)
gen_d = privatekey(input_p, input_q, gen_e)

print("Start message: " + str(message))
message_crypte = encrypt(message, gen_n, gen_e)
print("The crypted message is: " + str(message_crypte))
message_decrypte = decrypt(message_crypte, gen_d, gen_n)
print("The decrypted message is: " + str(message_decrypte))
