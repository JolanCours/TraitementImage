import math


def puissance_signal(pixels):
    """
    calcule la puissance du signal de l image de base (u)
    P_signal = Somme( |u(i, j)|^2 )
    """
    # on transforme l image numpy en liste python pour avoir des vrais entiers
    pixels = pixels.tolist()

    puissance = 0.0
    largeur = len(pixels)
    hauteur = len(pixels[0])

    for x in range(largeur):
        for y in range(hauteur):
            r, g, b = pixels[x][y]
            # en puissance le rgb
            puissance += (r**2 + g**2 + b**2)

    return puissance


def puissance_bruit(pixels_originaux, pixels_modifies):
    """
    calcule la puissance du bruit
    P_bruit c est Somme( |v(i, j) - u(i, j)|^2 )
    où v c est l'image bruitee
    """
    # pareil, on passe en liste python
    pixels_originaux = pixels_originaux.tolist()
    pixels_modifies = pixels_modifies.tolist()

    puissance = 0.0
    largeur = len(pixels_originaux)
    hauteur = len(pixels_originaux[0])

    for x in range(largeur):
        for y in range(hauteur):
            r_orig, g_orig, b_orig = pixels_originaux[x][y]
            r_mod, g_mod, b_mod = pixels_modifies[x][y]

            # la difference au carre
            diff_r = (r_mod - r_orig) ** 2
            diff_g = (g_mod - g_orig) ** 2
            diff_b = (b_mod - b_orig) ** 2

            puissance += (diff_r + diff_g + diff_b)

    return puissance


def calculer_snr(pixels_originaux, pixels_modifies):
    """
    Calcule SNR en décibels
    SNR = 10 * log10( P_signal / P_bruit )
    """
    p_signal = puissance_signal(pixels_originaux)
    p_bruit = puissance_bruit(pixels_originaux, pixels_modifies)

    # si c'est 0, hop les images c est les meme
    if p_bruit == 0:
        return float('inf')

    # x 10 pour avoir les DB
    snr = 10 * math.log10(p_signal / p_bruit)

    return snr