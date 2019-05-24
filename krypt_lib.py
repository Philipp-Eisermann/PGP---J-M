# - - - - - - - - - - - - - - - - V I G - - - - - - - - - - - - - - - -


def vigenerechiffr(Cryptage, encryptcode):
    # valeurs a incrémenter
    y = 0

    # la séquence chiffrée
    w = ""

    # processus de chiffrement
    for x in range(0, len(Cryptage)):
        b = Cryptage[x]

        while y == len(encryptcode):
            y = 0

        vigenere = encryptcode[y]

        ordb = ord(b)
        ordb += ord(vigenere)

        while ordb > 65535:
            ordb -= 65535

        while ordb < 0:
            ordb += 65535

        out = chr(ordb)
        w += out
        y += 1

    return w


def devigenere(sortie, decryptcode):
    # valeurs a incrémenter en décryptage
    xd = 0
    yd = 0

    # la séquence décryptée
    wd = ""

    # processus de décryption
    while xd < len(sortie):
        bd = sortie[xd]

        while yd == len(decryptcode):
            yd = 0

        vigenere = decryptcode[yd]

        ordbd = ord(bd)

        ordbd -= ord(vigenere)

        while ordbd > 65535:
            ordbd -= 65535

        while ordbd < 0:
            ordbd += 65535

        outd = chr(ordbd)

        wd += outd
        xd += 1
        yd += 1
    # Affichage du résultat
    return wd

# - - - - - - - - - - - - - - - - R S A - - - - - - - - - - - - - - - -

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
