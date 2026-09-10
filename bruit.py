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

def bruit_additif(width, height):
    pixels = []
    
    for y in range (width):
        ligne = []
        
        for x in range(height):
            valeur = random.randint(-50, 50)
            r, g, b = valeur, valeur, valeur
            ligne.append([r, g, b])

        pixels.append(ligne)

    return pixels

def limiter(valeur):
    return max(0, min(255, valeur))

def additif(peekaboo = list[list]) :
    
    largeur = len(peekaboo)
    hauteur = len(peekaboo[0])
    
    temp = bruit_additif(largeur, hauteur)
    
    for x in range (largeur):
        for y in range (hauteur):
            valeur = (limiter(peekaboo[x][y][0] + temp[x][y][0]), limiter(peekaboo[x][y][1] + temp[x][y][1]), limiter(peekaboo[x][y][2] + temp[x][y][2]))
            peekaboo[x][y] = valeur
    
    return peekaboo

def multiplicatif(peekaboo = list[list]):
    largeur = len(peekaboo)
    hauteur = len(peekaboo[0])

    temp = generer_bruit(largeur, hauteur)

    for x in range(largeur):
        for y in range(hauteur):

            valeur = (int(peekaboo[x][y][0] * temp[x][y][0]), int(peekaboo[x][y][1] * temp[x][y][1]), int(peekaboo[x][y][2] * temp[x][y][2]))
            peekaboo[x][y] = valeur

    return peekaboo

if __name__ == '__main__':
    poivre_sel()