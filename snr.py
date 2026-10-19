import math

import numpy as np


def puissance_signal(pixels):
    u = pixels.astype(float)
    return np.sum(u * u)


def puissance_bruit(pixels_originaux, pixels_modifies):
    difference = pixels_modifies.astype(float) - pixels_originaux.astype(float)
    return np.sum(difference * difference)


def calculer_snr(pixels_originaux, pixels_modifies):
    p_signal = puissance_signal(pixels_originaux)
    p_bruit = puissance_bruit(pixels_originaux, pixels_modifies)

    if p_bruit == 0:
        return float("inf")

    return 10 * math.log10(p_signal / p_bruit)