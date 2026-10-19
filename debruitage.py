import numpy as np


#Remplis les nouveaux pixels avec les valeurs des bords
def agrandir_bords(image, rayon):
    return np.pad(image, ((rayon, rayon), (rayon, rayon), (0, 0)), mode="edge")


def uniformiser(tableau):
    tableau = np.round(tableau)
    tableau = np.clip(tableau, 0, 255)
    return tableau.astype(np.uint8)


def convolution(image, noyau):
    taille = len(noyau)
    rayon = taille // 2
    hauteur = image.shape[0]
    largeur = image.shape[1]

    grande = agrandir_bords(image.astype(float), rayon)
    resultat = np.zeros((hauteur, largeur, 3))

    for i in range(taille):
        for j in range(taille):
            voisin = grande[i:i + hauteur, j:j + largeur]
            resultat = resultat + noyau[i][j] * voisin

    return uniformiser(resultat)


def moyenneur(image, taille=3):
    noyau = np.ones((taille, taille)) / (taille * taille)
    return convolution(image, noyau)


def ligne_pascal(n):
    ligne = [1]
    for k in range(n - 1):
        nouvelle_ligne = [1]
        for i in range(len(ligne) - 1):
            nouvelle_ligne.append(ligne[i] + ligne[i + 1])
        nouvelle_ligne.append(1)
        ligne = nouvelle_ligne
    return ligne


def gaussien(image, taille=3):
    ligne = ligne_pascal(taille)
    noyau = np.zeros((taille, taille))
    for i in range(taille):
        for j in range(taille):
            noyau[i][j] = ligne[i] * ligne[j]
    noyau = noyau / np.sum(noyau)
    return convolution(image, noyau)


def median(image, taille=3):
    rayon = taille // 2
    hauteur = image.shape[0]
    largeur = image.shape[1]

    grande = agrandir_bords(image, rayon)
    resultat = np.zeros_like(image)

    for canal in range(3):
        voisins = []
        for i in range(taille):
            for j in range(taille):
                voisins.append(grande[i:i + hauteur, j:j + largeur, canal])
        resultat[:, :, canal] = np.median(voisins, axis=0)

    return resultat


def moyenne_carre(tableau, y, x, cote, hauteur, largeur):
    somme = 0
    for i in range(cote):
        for j in range(cote):
            somme = somme + tableau[y + i:y + i + hauteur, x + j:x + j + largeur]
    return somme / (cote * cote)


def kuwahara(image, taille=5):
    rayon = taille // 2
    cote = rayon + 1
    hauteur = image.shape[0]
    largeur = image.shape[1]

    grande = agrandir_bords(image.astype(float), rayon)
    luminosite = 0.299 * grande[:, :, 0] + 0.587 * grande[:, :, 1] + 0.114 * grande[:, :, 2]
    luminosite_carre = luminosite * luminosite

    coins = [(0, 0), (0, rayon), (rayon, 0), (rayon, rayon)]
    resultat = None
    meilleure_variance = None

    for (y, x) in coins:
        moyenne = moyenne_carre(grande, y, x, cote, hauteur, largeur)
        moyenne_lum = moyenne_carre(luminosite, y, x, cote, hauteur, largeur)
        moyenne_lum_carre = moyenne_carre(luminosite_carre, y, x, cote, hauteur, largeur)
        variance = moyenne_lum_carre - moyenne_lum * moyenne_lum

        if resultat is None:
            resultat = moyenne
            meilleure_variance = variance
        else:
            plus_homogene = variance < meilleure_variance
            resultat[plus_homogene] = moyenne[plus_homogene]
            meilleure_variance[plus_homogene] = variance[plus_homogene]

    return uniformiser(resultat)