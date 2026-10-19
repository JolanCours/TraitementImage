import numpy as np

SEED = 42


def poivre_sel(image, taux=5):
    randomizer = np.random.default_rng(SEED)
    hauteur = image.shape[0]
    largeur = image.shape[1]

    tirage = randomizer.random((hauteur, largeur))
    couleur = randomizer.random((hauteur, largeur))

    pixels_touches = tirage < taux / 100
    pixels_blancs = pixels_touches & (couleur < 0.5)
    pixels_noirs = pixels_touches & (couleur >= 0.5)

    resultat = image.copy()
    resultat[pixels_blancs] = 255
    resultat[pixels_noirs] = 0
    return resultat


def additif(image, amplitude=50):
    randomizer = np.random.default_rng(SEED)
    hauteur = image.shape[0]
    largeur = image.shape[1]

    bruit = randomizer.integers(-amplitude, amplitude + 1, size=(hauteur, largeur))

    resultat = image.astype(int)
    for canal in range(3):
        resultat[:, :, canal] = resultat[:, :, canal] + bruit

    resultat = np.clip(resultat, 0, 255)
    return resultat.astype(np.uint8)


def multiplicatif(image, intensite=30):
    randomizer = np.random.default_rng(SEED)
    hauteur = image.shape[0]
    largeur = image.shape[1]

    bruit = randomizer.uniform(-intensite / 100, intensite / 100, size=(hauteur, largeur))

    resultat = image.astype(float)
    for canal in range(3):
        resultat[:, :, canal] = resultat[:, :, canal] * (1 + bruit)

    resultat = np.clip(resultat, 0, 255)
    return resultat.astype(np.uint8)