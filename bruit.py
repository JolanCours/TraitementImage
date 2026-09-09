from main import CustomImage
import random

def poivre_sel(peekaboo = list[list]):

    taux_bruit = 0.05

    largeur = len(peekaboo)
    hauteur = len(peekaboo[0])

    for x in range(largeur):
        for y in range(hauteur):
            proba = random.random()
            if proba < taux_bruit:
                valeur = 255 if random.random() < 0.5 else 0
                peekaboo[x][y] = (valeur, valeur, valeur)

    return peekaboo




def generer_bruit(width, height):
    pixels = []

    for y in range(width):
        ligne = []

        for x in range(height):
            valeur = float(random.randint(40, 100)/100)
            r, g, b = valeur, valeur, valeur
            ligne.append([r, g, b])

        pixels.append(ligne)

    return pixels

def multiplicatif(peekaboo = list[list]):
    largeur = len(peekaboo)
    hauteur = len(peekaboo[0])

    temp = generer_bruit(largeur, hauteur)

    for x in range(largeur):
        for y in range(hauteur):

            valeur = (peekaboo[x][y][0] * temp[x][y][0], peekaboo[x][y][1] * temp[x][y][1], peekaboo[x][y][2] * temp[x][y][2])
            peekaboo[x][y] = valeur

    return peekaboo

if __name__ == '__main__':
    poivre_sel()