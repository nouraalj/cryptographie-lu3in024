# Sorbonne Université 3I024 2021-2022
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : ALJANE Noura 28600768
# Etudiant.e 2 : BENELMIR Rami 21221977



import sys, getopt, string, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français
# utilisation de frequence.py avec le texte germinal_nettoye du tme1
freq_FR = [0.09213414037491088,  0.010354463742221126,  0.030178915678726964,  0.03753683726285317,  0.17174710607479665,  0.010939030914707838,  0.01061497737343803,  0.010717912027723734,  0.07507240372750529,  0.003832727374391129,  6.989390105819367e-05,  0.061368115927295096,  0.026498684088462805,  0.07030818127173859,  0.049140495636714375,  0.023697844853330825,  0.010160031617459242,  0.06609294363882899,  0.07816806814528274,  0.07374314880919855,  0.06356151362232132,  0.01645048271269667,  1.14371838095226e-05,  0.004071637436190045,  0.0023001447439151006,  0.0012263202640210343]

# Chiffrement César
def chiffre_cesar(txt, key):
    """
    Prend en entrée une chaine de caractères 
    composée de lettre majuscules et une clef (un entier)
    et effectue un décalage du type chiffrement
    de César et renvoie la chaine chiffrée.
    """
    resultat = ""
    for lettre in txt:
        resultat += chr((ord(lettre)-65+key)%26+65)
    return resultat

# Déchiffrement César
def dechiffre_cesar(txt, key):
    """
    Prends en entrée une chaine de caractères 
    composée de lettre majuscules et une clef (un entier)
    et effectue un décalage du type déchiffrement
    de César et renvoie la chaine chiffrée.
    """
    return chiffre_cesar(txt, -(key)%26)

# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """
    Prends en entrée une chaine de caractères 
    composée de lettre majuscules et une clef (un mot)
    et effectue un décalage du type déchiffrement
    de Vigenère et renvoie la chaine chiffrée.
    """
    i=0 #index pour parcourir les lettres de key
    resultat =""
    for lettre in txt:
        """on applique un chiffrement de césar sur chaque lettre du texte avec pour clé 
        la lettre correspondante"""
        resultat += chiffre_cesar(lettre, key[i%len(key)])
        i += 1

    return resultat

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """
    Hypothèse : txt chaine de caractère en majuscule
    Même principe que la fonction précédente mais pour un déchiffrement
    """
    i=0 #index pour parcourir les lettres de key
    resultat =""
    for lettre in txt:
        """on applique un déchiffrement de césar sur chaque lettre du texte avec pour clé 
        la lettre correspondante"""
        resultat += dechiffre_cesar(lettre, key[i%len(key)])
        i += 1
    return resultat

# Analyse de fréquences
def freq(txt):
    """
    Hypothèse : txt chaine de caractère en majuscule
    Prend en entrée un texte et renvoie  un tableau
    qui compte le nombre d'occurences de chaque lettre 
    de ce texte. 
    """
    i =0 #index d'hist
    hist=[0.0]*len(alphabet)
    for lettre in txt:
        indice = alphabet.index(lettre)
        hist[indice] += 1.0

    return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Hypothèse : txt chaine de caractère en majuscule
    Prend en entrée un texte et renvoie la position dans l'
    alphabet de la lettre qui apparait le plus grand 
    nombre de fois dans le texte.
    """
    #on utilise le tableau renvoyé par la fonction freq
    return freq(txt).index(max(freq(txt)))

# indice de coïncidence
def indice_coincidence(hist):
    """
    Prend en entrée un tableau d'occurences de lettre et 
    renvoie l'indice de coincidence
    """
    somme =0.0
    for i in range(len(alphabet)):
        somme += (hist[i]*(hist[i]-1))/(sum(hist)*(sum(hist)-1))

    return somme

# Recherche la longueur de la clé
def longueur_clef(cipher):
    """
    Hypothèse : cipher chaine de caractère en majuscule
    Prend en entrée un texte et renvoie la longueur de la
    clé 
    """
    for l in range(4,21):
        i=0
        liste_ic = []
        for i in range(0, l):
            colonne_i = cipher[i:len(cipher):l] #découpage en collonne 0<= i < l
            liste_ic.append(indice_coincidence(freq(colonne_i))) #IC(colonne_i)
        if (sum(liste_ic)/l >0.06):
            return l

    return 0
    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Pour chaque colonne découpé, on calcule l'index de
    la lettre la plus fréquente de la colonne au quel 
    on soustrait l'index de la lettre E. On obtient le décalage
    qu'à subi cette colonne et on l'ajoute au tableau des décalages.
    """
    decalages=[0]*key_length
    for i in range(key_length):
        lettre_indice = lettre_freq_max(cipher[i:len(cipher):key_length]) - alphabet.index('E')
        #print(lettre_indice)
        decalages[i] = lettre_indice%26
    #print(decalages) 
    return decalages

# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Hypothèse : cipher texte en majuscules
    Prends en entrée un texte et renvoie le texte déchiffré.
    """

    return dechiffre_vigenere(cipher, clef_par_decalages(cipher, longueur_clef(cipher)))

#________________________________________________________________
# QUESTION 9 -- Première cryptanalyse : 

#### Combien de textes sont correctement cryptanalysés ?
# -> Sur les 94 textes, seuls 15 ont été correctements cryptanalysés.

#### Comment expliquez-vous cela ?
# -> On explique cela car pour des textes courts, la fréquence d'apparition de certaines lettres ne coincident
# pas avec la fréquence des lettres d'une certaine langue. De plus, les textes qui ont été correctement cryptanalysés 
# sont des textes avec une apparition fréquente de la lettre E et A et/ou des textes longs. 
# Cette crypanalyse est inefficace sur les textes courts.


#________________________________________________________________


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
    Prend en entrée deux tableaux
    qui correspondent aux fréquences des lettres de deux texte et 
    d l'entier qui correspond à la clé du déclage subit par h2
    Renvoie l'indice de coincidence mutuelle de ces 2 textes
    """
    somme = 0
    len_h1 = len(h1) 
    len_h2 = len(h2)
    h2_v2 = [0]*len_h2 #nouveau tableau de fréquence de h2 sans décalage
    if (sum(h1)==0 or sum(h2)==0):
        #éviter la division par zéro
        return 0
    for i in range(len_h2):
        h2_v2[i] = h2[(i+d)%26] 
    for i in range(len(alphabet)):
        somme += (h1[i]*h2_v2[i])/(sum(h1)*sum(h2)) #calcul de l'indice de coincidence pour chaque lettre
    #print(somme)
    return somme

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Prend un texte et une longueur de clef supposée. Avec la première colonne du
    texte(de longueur de clé), on calcule pour toutes les autres colonnes 
    qui subissent un décalage d (avec d= 0,...,25) les indices de coincidence mutuelle.
    L'indice maximal pour chaque colonne permet de retrouver le décalage relatif entre
    ces 2 colonnes.
    """
    decalages=[0]*key_length
    first_column = cipher[0:len(cipher):key_length]
    d=0
    tab_icm=[]
    column_i = ""
    for i in range(key_length):
        column_i = cipher[i:len(cipher):key_length]
        for d in range(len(alphabet)):
            tab_icm.append(indice_coincidence_mutuelle(freq(first_column), freq(column_i), d))
        decalages[i]= tab_icm.index(max(tab_icm))
        tab_icm = []
    #print("decalages :", decalages)
    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Prend en entrée un texte chiffré et renvoie son déchiffré avec une
    méthode de décalages par ICM.
    """
    longueur  = longueur_clef(cipher)
    decalage = tableau_decalages_ICM(cipher, longueur)
    new_text = dechiffre_vigenere(cipher,decalage)
    key = (lettre_freq_max(new_text)-ord('E') -  65)%26
    return dechiffre_cesar(new_text,key)

#________________________________________________________________
# QUESTION 12 -- Deuxième cryptanalyse : 

#### Combien de textes sont correctement cryptanalysés ?
# -> Sur les 94 textes, 45 ont été correctements cryptanalysés.

#### Comment expliquez-vous cela ?
# -> On explique cela car une cryptanalyse par indice de coincidence mutuelle
# est plus précise qu'une analyse simple par fréquence de lettre, elle attaque la clef et 
# le décalage. 
# Cependant elle continue à comparer avec la fréquence des lettres de la langue et
# reste donc inefficace sur les textes courts.

#________________________________________________________________


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1,L2):
    """
    Hypothése : les listes en entrée sont de meme taille
    Renvoie la corrélation linéaire de Pearson cf. formule du cours  
    """ 
    moy_L1 = sum(L1)/(len(L1))
    moy_L2 = sum(L2)/(len(L2))
    numerateur = 0.0
    denominateur_1 = 0.0
    denominateur_2 = 0.0
    for i in range( len(L1)):
        numerateur += ((L1[i] - moy_L1)*(L2[i] - moy_L2))
        denominateur_1  += (L1[i] - moy_L1) **2
        denominateur_2  += (L2[i] - moy_L2) **2

    return numerateur/ (math.sqrt(denominateur_1 *denominateur_2))


# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Documentation à écrire
    """
    key=[0]*key_length #tableau de décalage (corrélation max) pour chaque colonne
    score = 0.0 #moyenne des corrélations max de chaque colonne
    sum_corr= 0

    for i in range(key_length):
        liste_corr = []
        for d in range(len(alphabet)):
            corr_d = correlation(freq_FR, freq(dechiffre_cesar(cipher[i::key_length], d)))
            liste_corr.append(corr_d)
            
        key[i] = liste_corr.index(max(liste_corr))
        sum_corr += max(liste_corr)
    score = sum_corr/key_length
    #print(score)
    return (score, key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Documentation à écrire
    """
    key_length =[]
    moy_max = 0
    for i in range(1,21):
        (score, key) = clef_correlations(cipher, i)
        if score > moy_max:
            moy_max = score
            key_length = key
    return dechiffre_vigenere(cipher, key_length)

#________________________________________________________________
# QUESTION 15 -- Troisième cryptanalyse : 

#### Combien de textes sont correctement cryptanalysés ?
# -> Sur les 100 textes, 94 ont été correctement cryptanalysés.

#### Quels sont les caractéristiques des textes qui échouent ?
# -> exemple de textes correctement cryptanalysés :
# texte 1 : texte long, clé de taille moyenne
# -> exemple de textes qui échouent :
# texte 81 : texte court, clé longue
# texte 86 : texte court, clé longue 
# Les textes qui échouent n'ont pas la meme fréquence de lettres par rapport à celle de 
# la langue française (plus de l que de u pour le texte 89)

#### Comment expliquez-vous cela ?
# 
# -> Nous avons réussi a cryptanalysés plus de textes que les méthodes précédentes.
# Mais encore une fois, la longueur des textes a un impact et l'utilisation des
# fréquences d'une langue aussi. Le chiffrement de vigenere est un bon cryptosystème
# sur les textes courts à clé longue mais pas sur les textes longs facilement déchiffrable.
#________________________________________________________________

################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
