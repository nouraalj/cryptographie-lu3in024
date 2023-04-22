# Sorbonne Université LU3IN024 2021-2022
# TME 5 : Cryptographie à base de courbes elliptiques
#
# Etudiant.e 1 : Noura ALJANE 28600768
# Etudiant.e 2 : Rami BENENELMIR 21221977 

from math import sqrt
import matplotlib.pyplot as plt
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
    """
    Renvoie True si la courbe E est elliptique et False sinon.

    E : un triplet (p, a, b) représentant la courbe d'équation
    y^2 = x^3 + ax + b sur F_p, p > 3
    """
    return 


def point_sur_courbe(P, E):
    """Renvoie True si le point P appartient à la courbe E et False sinon."""

    return


def symbole_legendre(a, p):
    """Renvoie le symbole de Legendre de a mod p."""
    
    return 


def cardinal(E):
    """Renvoie le cardinal du groupe de points de la courbe E."""
    
    return


def liste_points(E):
    """Renvoie la liste des points de la courbe elliptique E."""
    p, a, b = E

    assert p % 4 == 3, "erreur: p n'est pas congru à 3 mod 4."

    return


def cardinaux_courbes(p):
    """
    Renvoie la distribution des cardinaux des courbes elliptiques définies sur F_p.

    Renvoie un dictionnaire D où D[i] contient le nombre de courbes elliptiques
    de cardinal i sur F_p.
    """
    D = {}
    
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

    return 


def est_egal(P1, P2, p):
    """Teste l'égalité de deux points mod p."""

    return


def est_zero(P):
    """Teste si un point est égal au point à l'infini."""

    return


def addition(P1, P2, E):
    """Renvoie P1 + P2 sur la courbe E."""
    
    return


def multiplication_scalaire(k, P, E):
    """Renvoie la multiplication scalaire k*P sur la courbe E."""
    
    return


def ordre(N, factors_N, P, E):
    """Renvoie l'ordre du point P dans les points de la courbe E mod p. 
    N est le nombre de points de E sur Fp.
    factors_N est la factorisation de N en produit de facteurs premiers."""

    return 


def point_aleatoire_naif(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E."""
    
    return 


def point_aleatoire(E):
    """Renvoie un point aléatoire (différent du point à l'infini) sur la courbe E."""

    return


def point_ordre(E, N, factors_N, n):
    """Renvoie un point aléatoire d'ordre N sur la courbe E.
    Ne vérifie pas que n divise N."""

    return

def keygen_DH(P, E, n):
    """Génère une clé publique et une clé privée pour un échange Diffie-Hellman.
    P est un point d'ordre n sur la courbe E.
    """
    sec = None # A remplacer
    pub = None # A remplacer
    
    return (sec, pub)

def echange_DH(sec_A, pub_B, E):
    """Renvoie la clé commune à l'issue d'un échange Diffie-Hellman.
    sec_A est l'entier secret d'Alice et pub_b est l'entier public de Bob."""

    return
