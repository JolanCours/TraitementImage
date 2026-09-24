from main import CustomImage
import random

def bruit_additif(height,width):
    pixels = []
    
    for y in range (height):
        ligne = []
        
        for x in range(width):
            r = random.randint(-50, 50)
            g = random.randint(-50, 50)
            b = random.randint(-50, 50)
            ligne.append([r, g, b])

        pixels.append(ligne)

    return pixels

def limiter(valeur):
    return max(0, min(255, valeur))

def additif(peekaboo = list[list]) :
    
    hauteur = len(peekaboo)
    largeur = len(peekaboo[0])
    
    temp = bruit_additif(hauteur, largeur)
    
    for x in range (hauteur):
        for y in range (largeur):
            valeur = (limiter(peekaboo[x][y][0] + temp[x][y][0]),
                      limiter(peekaboo[x][y][1] + temp[x][y][1]),
                      limiter(peekaboo[x][y][2] + temp[x][y][2]))
            peekaboo[x][y] = valeur
    
    return peekaboo

def convolution(peekaboo = list[list]):
    hauteur = len(peekaboo)
    largeur = len(peekaboo[0])
    
    noyau=[[1/9,1/9,1/9],
           [1/9,1/9,1/9],
           [1/9,1/9,1/9]]
    
    resultat = []
    
    for x in range(hauteur):
        ligne = []
        
        for y in range(largeur):
            ligne.append([0,0,0])
        
        resultat.append(ligne)
    
    for x in range(1,hauteur-1):
        for y in range(1,largeur-1):
            
            r = (peekaboo[x-1][y-1][0]*noyau[0][0]+peekaboo[x-1][y][0]*noyau[0][1]+peekaboo[x-1][y+1][0]*noyau[0][2]+
            peekaboo[x][y-1][0]*noyau[1][0]+peekaboo[x][y][0]*noyau[1][1]+peekaboo[x][y+1][0]*noyau[1][2]+
            peekaboo[x+1][y-1][0]*noyau[2][0]+peekaboo[x+1][y][0]*noyau[2][1]+peekaboo[x+1][y+1][0]*noyau[2][2])
            
            g = (peekaboo[x-1][y-1][1]*noyau[0][0]+peekaboo[x-1][y][1]*noyau[0][1]+peekaboo[x-1][y+1][1]*noyau[0][2]+
            peekaboo[x][y-1][1]*noyau[1][0]+peekaboo[x][y][1]*noyau[1][1]+peekaboo[x][y+1][1]*noyau[1][2]+
            peekaboo[x+1][y-1][1]*noyau[2][0]+peekaboo[x+1][y][1]*noyau[2][1]+peekaboo[x+1][y+1][1]*noyau[2][2])
            
            b = (peekaboo[x-1][y-1][2]*noyau[0][0]+peekaboo[x-1][y][2]*noyau[0][1]+peekaboo[x-1][y+1][2]*noyau[0][2]+
            peekaboo[x][y-1][2]*noyau[1][0]+peekaboo[x][y][2]*noyau[1][1]+peekaboo[x][y+1][2]*noyau[1][2]+
            peekaboo[x+1][y-1][2]*noyau[2][0]+peekaboo[x+1][y][2]*noyau[2][1]+peekaboo[x+1][y+1][2]*noyau[2][2])
            
            resultat[x][y] = [limiter(int(r)),limiter(int(g)),limiter(int(b))]
            
    return resultat

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

            valeur = (int(peekaboo[x][y][0] * temp[x][y][0]), int(peekaboo[x][y][1] * temp[x][y][1]), int(peekaboo[x][y][2] * temp[x][y][2]))
            peekaboo[x][y] = valeur

    return peekaboo

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

def image_originale(peekaboo = list[list]):
    largeur = len(peekaboo)
    hauteur = len(peekaboo[0])

    for x in range(largeur):
        for y in range(hauteur):

            valeur = (peekaboo[x][y][0], peekaboo[x][y][1], peekaboo[x][y][2])
            peekaboo[x][y] = valeur

    return peekaboo



    
if __name__ == '__main__':
    poivre_sel()