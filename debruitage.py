
def get_matrice(pixels, x, y):
    matrice = []

    for i in range(x - 1, x + 2):
        ligne = []
        for j in range(y - 1, y + 2):
            ligne.append(pixels[i][j])
        matrice.append(ligne)

    return matrice


def filtrage_median(pixels, image):
    largeur = len(pixels)
    hauteur = len(pixels[0])


    nouveau_pixels = [ligne[:] for ligne in pixels]

    for x in range(1, largeur - 1):
        for y in range(1, hauteur - 1):

            matrice = get_matrice(pixels, x, y)

            liste = [pixel for ligne in matrice for pixel in ligne]

            rouge = sorted([pixel[0] for pixel in liste])[4] #fallait trier
            vert = sorted([pixel[1] for pixel in liste])[4]
            bleu = sorted([pixel[2] for pixel in liste])[4]

            nouveau_pixels[x][y] = (rouge, vert, bleu)

    image.set_pixels(nouveau_pixels)
    return nouveau_pixels

if __name__ == '__main__':
    filtrage_median()
