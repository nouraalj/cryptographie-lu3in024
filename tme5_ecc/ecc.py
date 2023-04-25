# Sorbonne Université LU3IN024 2021-2022
# TME 5 : Cryptographie à base de courbes elliptiques
#
# Etudiant.e 1 : NOURA ALJANE 28600768
# Etudiant.e 2 : RAMI BENELMIR 21221977

from math import *
import matplotlib.pyplot as plt
import random
from random import randint

# Fonctions utiles


def exp(a, N, p):
    """Renvoie a**N % p par exponentiation rapide."""
    def binaire(N):
        L = list()
        while (N > 0):
            L.append(N % 2)
            N = N // 2
        L.reverse()
        return L
    res = 1
    for Ni in binaire(N):
        res = (res * res) % p
        if (Ni == 1):
            res = (res * a) % p
    return res


def factor(n):
    """ Return the list of couples (p, a_p) where p is a prime divisor of n and
    a_p is the p-adic valuation of n. """
    def factor_gen(n):
        j = 2
        while n > 1:
            for i in range(j, int(sqrt(n)) + 1):
                if n % i == 0:
                    n //= i
                    j = i
                    yield i
                    break
            else:
                if n > 1:
                    yield n
                    break

    factors_with_multiplicity = list(factor_gen(n))
    factors_set = set(factors_with_multiplicity)

    return [(p, factors_with_multiplicity.count(p)) for p in factors_set]


def inv_mod(x, p):
    """Renvoie l'inverse de x modulo p."""

    return exp(x, p-2, p)


def racine_carree(a, p):
    """Renvoie une racine carrée de a mod p si p = 3 mod 4."""
    assert p % 4 == 3, "erreur: p != 3 mod 4"

    return exp(a, (p + 1) // 4, p)


# Fonctions demandées dans le TME

def est_elliptique(E):
    """Renvoie True si la courbe E est elliptique et False sinon.
    E : un triplet (p, a, b) représentant la courbe d'équation 
    y^2 = x^3 + ax + b sur F_p, p > 3"""
    p, a, b = E
    delta = ((4 * (a**3)) + (27 * (b ** 2))) % p
    if delta == 0:
        return False
    return True


def point_sur_courbe(P, E):
    """Renvoie True si le point P appartient à la courbe E et False sinon."""
    if P == ():
        return True
    p, a, b = E
    x, y = P
    y_1 = (y**2) % p
    y_2 = (x**3 + (a*x) + b) % p
    if y_1 == y_2:
        return True
    return False


def symbole_legendre(a, p):
    """
    Hypothèse : p est premier
    Renvoie le symbole de Legendre de a mod p.
    """
    return exp(a, (p-1) // 2, p)

# Q3 - Pourquoi utilise-t-on cette formule ? Car cette formule d'exponentiation rapide
# nous permet de faciliter le calcul et d'éviter de calculer une racine carrée.


def cardinal(E):
    """Renvoie le cardinal du groupe de points de la courbe E."""
    p, a, b = E
    cpt = 1  # l'infini
    for x in range(p):
        z = (x**3 + x * a + b) % p  # eviter la foction pow

        legendre = symbole_legendre(z, p)

        if legendre == 1:
            cpt += 2

        elif legendre == 0:
            cpt += 1
    # print(cpt)
    return cpt


def liste_points(E):
    """Renvoie la liste des points de la courbe elliptique E."""
    p, a, b = E

    assert p % 4 == 3, "erreur: p n'est pas congru à 3 mod 4."

    liste_points = [()]

    for x in range(p):

        z = (x ** 3 + a * x + b) % p
        legendre = symbole_legendre(z, p)

        if legendre == 0:

            liste_points.append((x, 0))

        elif legendre == 1:

            y = racine_carree(z, p)

            liste_points.append((x, y))
            liste_points.append((x, -y))

    return liste_points


"""Q6 - Théorème de Hasse : 
si E est une courbe elliptique définie sur un corps fini Fq avec q éléments 
(où q est une puissance d'un nombre premier p) et si N est le nombre de points sur la
courbe elliptique, alors :
|N - (q+1)| ≤ 2*sqrt(q)

Le cardinal de E_q est proche de q+1."""


def cardinaux_courbes(p):
    """
    Renvoie la distribution des cardinaux des courbes elliptiques définies sur F_p.

    Renvoie un dictionnaire D où D[i] contient le nombre de courbes elliptiques
    de cardinal i sur F_p.
    """
    D = {}

    for b in range(p):

        for a in range(p):
            E = p, a, b

            if est_elliptique(E):

                card = cardinal(E)
                if card in D:
                    D[card] += 1
                else:
                    D[card] = 1
    return D


def dessine_graphe(p):
    """Dessine le graphe de répartition des cardinaux des courbes elliptiques définies sur F_p."""
    bound = int(2 * sqrt(p))
    C = [c for c in range(p + 1 - bound, p + 1 + bound + 1)]
    D = cardinaux_courbes(p)

    plt.bar(C, [D[c] for c in C], color='b')
    plt.show()


def moins(P, p):
    """Retourne l'opposé du point P mod p."""
    if P == ():
        return ()

    x, y = P
    return x % p, -y % p


def est_egal(P1, P2, p):
    """Teste l'égalité de deux points mod p."""
    if P1 == () and P2 == ():
        return True
    elif P1 == () or P2 == ():
        return False
    else:
        x1, y1 = P1
        x2, y2 = P2
        if x1 % p == x2 % p and y1 % p == y2 % p:
            return True
        return False


def est_zero(P):
    """Teste si un point est égal au point à l'infini."""
    if P == ():
        return True
    return False


def addition(P1, P2, E):
    """Renvoie P1 + P2 sur la courbe E."""
    p, a, b = E

    if est_zero(P1):
        return P2
    elif est_zero(P2):
        return P1

    elif est_egal(P1, moins(P2, p), p) or est_egal(moins(P1, p), P2, p):
        return ()

    x1, y1 = P1
    x2, y2 = P2

    if est_egal(P1, P2, p):

        R = ((3 * (x1 ** 2) + a) * inv_mod(2 * y1, p)) % p

    else:

        R = ((y2 - y1) * inv_mod(x2 - x1, p)) % p

    x = (R ** 2 - x1 - x2) % p
    y = (R * (x1 - x) - y1) % p

    if point_sur_courbe((x, y), E):
        return x, y

    return ()


def multiplication_scalaire(k, P, E):
    """Renvoie la multiplication scalaire k*P sur la courbe E."""
    res = ()
    p, a, b = E

    def conversion_binaire(n):
        list_binaire = list()
        while n > 0:
            list_binaire.append(n % 2)
            n = n // 2
        list_binaire.reverse()
        return list_binaire

    for k_i in conversion_binaire(abs(k)):
        res = addition(res, res, E)
        if k_i == 1:
            res = addition(res, P, E)
    if k < 0:
        res = moins(res, p)
    # print("res == "+str(res))
    return res


def ordre(N, factors_N, P, E):
    """Renvoie l'ordre du point P dans les points de la courbe E mod p. 
    N est le nombre de points de E sur Fp.
    factors_N est la factorisation de N en produit de facteurs premiers."""
    l_div_cardE = [1]
    if P == ():
        return 1
    if not point_sur_courbe(P, E):
        return -1

    for k in factors_N:
        k_i = 1
        for ap in range(1, k[1] + 1):
            k_i = k_i * k[0]
            if k_i not in l_div_cardE:
                l_div_cardE.append(k_i)
            if N / k_i not in l_div_cardE:
                l_div_cardE.append(N // k_i)
    l_div_cardE.append(N)
    # ordonner les diviseurs de N pour retourner l'ordre le plus petit
    l = sorted(l_div_cardE)

    for k_i in l:
        mult = multiplication_scalaire(k_i, P, E)
        if est_zero(mult):
            # print("k = "+str(k_i))
            return k_i
    return -1


def point_aleatoire_naif(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E."""
    p, a, b = E
    while True:
        x = random.randint(0, p-1)
        y_squared = (x**3 + a*x + b) % p
        y = (y_squared**((p+1)//4)) % p
        if (y**2) % p == y_squared:
            return (x, y)


"""Q11- Dans le pire des cas, la complexité est égale à O(p) ou p est l'ordre de E". """
# point_aleatoire_naif((360040014289779780338359, 117235701958358085919867, 18575864837248358617992))
""" Lorsqu'on lance cette fonction, l'éxecution prend énormément de temps car les opérations sont
couteuses et la taille des paramètres est conséquente"""


def point_aleatoire(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E."""
    p, a, b = E
    while True:
        x = random.randint(0, p-1)
        y_squared = (x**3 + a*x + b) % p
        y = racine_carree(y_squared, p)
        if y is not None:
            return (x, y)


"""Q12- La complexité de la fonction est O(p/2)"""
# print(point_aleatoire((360040014289779780338359, 117235701958358085919867, 18575864837248358617992)))
"""Un exemple d'execution pour cette courbe : 
(104689830400682176449062, 162255181558028311378894)"""


def point_ordre(E, N, factors_N, n):
    """Renvoie un point aléatoire d'ordre N sur la courbe E.
    Ne vérifie pas que n divise N."""
    point = point_aleatoire(E)
    ordre_point = ordre(N, factors_N, point, E)

    while ordre_point != n:
        point = point_aleatoire(E)
        ordre_point = ordre(N, factors_N, point, E)

    return point


def keygen_DH(P, E, n):
    """Génère une clé publique et une clé privée pour un échange Diffie-Hellman.
    P est un point d'ordre n sur la courbe E.
    """
    p, a, b = E
    sec = random.randint(1, p-1)
    pub = multiplication_scalaire(sec, P, E)

    return (sec, pub)


def echange_DH(sec_A, pub_B, E):
    """Renvoie la clé commune à l'issue d'un échange Diffie-Hellman.
    sec_A est l'entier secret d'Alice et pub_b est l'entier public de Bob."""

    return multiplication_scalaire(sec_A, pub_B, E)


# Q15 :
p = 248301763022729027652019747568375012323
N = 248301763022729027652019747568375012324
factors_N = [(2, 2), (62075440755682256913004936892093753081, 1)]
E = (p, 1, 0)

P = point_ordre(E, N, factors_N, N)
# print("Un bon point P est : ", P)

"""Un bon point P pour un échange Diffie Hellman 
est :  (204287855979594107717209493799834248051, 158126136277126580562246493372167693567),
ce point est bien choisi car il est d'ordre N, il est difficile 
de calculer le logarithme discret de P"""
