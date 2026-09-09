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

if __name__ == '__main__':
    poivre_sel()