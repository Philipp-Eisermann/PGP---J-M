def vigenerechiffr(Cryptage, encryptcode):
    # valeurs a incrémenter
    y = 0

    # la séquence cryptée
    w = ""

    # processus d'encryption
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


#msg = input("your message: ")
#key = input("key: ")

#print(vigenerechiffr(msg, key))
#print(devigenere(vigenerechiffr(msg,key), key))
