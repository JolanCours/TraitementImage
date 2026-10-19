import os
import sys
import time

import numpy as np
import pygame
from PIL import Image

import bruit
import debruitage
from snr import calculer_snr

IMAGE = "images/sample_1280×853.bmp"

BRUITS = [
    {"nom": "Poivre et sel", "fonction": bruit.poivre_sel,
     "reglage": "Taux", "min": 1, "max": 30, "pas": 1, "defaut": 5, "unite": " %"},
    {"nom": "Additif", "fonction": bruit.additif,
     "reglage": "Amplitude", "min": 5, "max": 100, "pas": 5, "defaut": 50, "unite": ""},
    {"nom": "Multiplicatif", "fonction": bruit.multiplicatif,
     "reglage": "Intensité", "min": 5, "max": 80, "pas": 5, "defaut": 30, "unite": " %"},
]

FILTRES = [
    {"nom": "Convolution", "fonction": debruitage.convolutions},
    {"nom": "Médian", "fonction": debruitage.median},
    {"nom": "Kuwahara", "fonction": debruitage.kuwahara},
]

#
LARGEUR = 1280
HAUTEUR = 760
PANNEAU = 260
MARGE = 20

# Zone
ZONE_X = PANNEAU + MARGE
ZONE_Y = 44
ZONE_LARGEUR = LARGEUR - PANNEAU - 2 * MARGE
ZONE_HAUTEUR = HAUTEUR - ZONE_Y - MARGE


#Couleurs
FOND = (30, 30, 30)
FOND_PANNEAU = (42, 42, 42)
BOUTON = (62, 62, 62)
BOUTON_SURVOL = (80, 80, 80)
BOUTON_INACTIF = (50, 50, 50)
ACCENT = (90, 150, 230)
TEXTE = (230, 230, 230)
TEXTE_DOUX = (150, 150, 150)
TEXTE_INACTIF = (95, 95, 95)



def charger_image(chemin):
    image = Image.open(chemin).convert("RGB")
    return np.array(image)


def creer_surface(pixels):
    hauteur = pixels.shape[0]
    largeur = pixels.shape[1]
    surface = pygame.image.frombuffer(pixels.tobytes(), (largeur, hauteur), "RGB")

    echelle = min(ZONE_LARGEUR / largeur, ZONE_HAUTEUR / hauteur, 1)
    nouvelle_taille = (int(largeur * echelle), int(hauteur * echelle))
    return pygame.transform.smoothscale(surface, nouvelle_taille)


class Bouton:
    def __init__(self, texte, x, y, largeur, hauteur):
        self.texte = texte
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.actif = True
        self.selectionne = False

    def est_clique(self, position):
        return self.actif and self.rect.collidepoint(position)

    def dessiner(self, ecran, police):
        if not self.actif:
            couleur_fond = BOUTON_INACTIF
            couleur_texte = TEXTE_INACTIF
        elif self.selectionne:
            couleur_fond = ACCENT
            couleur_texte = FOND
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            couleur_fond = BOUTON_SURVOL
            couleur_texte = TEXTE
        else:
            couleur_fond = BOUTON
            couleur_texte = TEXTE

        pygame.draw.rect(ecran, couleur_fond, self.rect)
        texte = police.render(self.texte, True, couleur_texte)
        ecran.blit(texte, texte.get_rect(center=self.rect.center))


class Curseur:
    def __init__(self, x, y, largeur, mini, maxi, pas, valeur):
        self.rect = pygame.Rect(x, y, largeur, 18)
        self.actif = True
        self.dragging = False
        self.changer_reglage(mini, maxi, pas, valeur)

    def changer_reglage(self, mini, maxi, pas, valeur):
        self.mini = mini
        self.maxi = maxi
        self.pas = pas
        self.valeur = valeur

    def place(self, x_souris):
        proportion = (x_souris - self.rect.x) / self.rect.width
        if proportion < 0:
            proportion = 0
        if proportion > 1:
            proportion = 1
        nombre_de_pas = round(proportion * (self.maxi - self.mini) / self.pas)
        self.valeur = self.mini + nombre_de_pas * self.pas

    def handle_event(self, evenement):
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            if self.actif and self.rect.collidepoint(evenement.pos):
                self.dragging = True
                self.place(evenement.pos[0])
        if evenement.type == pygame.MOUSEMOTION and self.dragging:
            self.place(evenement.pos[0])
        if evenement.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

    def dessiner(self, ecran):
        proportion = (self.valeur - self.mini) / (self.maxi - self.mini)
        x_poignee = self.rect.x + proportion * self.rect.width
        y_milieu = self.rect.centery

        if self.actif:
            couleur_remplie = ACCENT
            couleur_poignee = TEXTE
        else:
            couleur_remplie = BOUTON_INACTIF
            couleur_poignee = TEXTE_INACTIF

        pygame.draw.rect(ecran, BOUTON, (self.rect.x, y_milieu - 2, self.rect.width, 4))
        pygame.draw.rect(ecran, couleur_remplie, (self.rect.x, y_milieu - 2, x_poignee - self.rect.x, 4))
        pygame.draw.rect(ecran, couleur_poignee, (x_poignee - 4, self.rect.y, 8, self.rect.height))


class Application:
    def __init__(self, chemin_image):
        pygame.init()
        pygame.display.set_caption("Traitement d'images")
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        self.police = pygame.font.Font(None, 22)
        self.police_titre = pygame.font.Font(None, 28)
        self.police_petite = pygame.font.Font(None, 19)

        self.nom_image = os.path.splitext(os.path.basename(chemin_image))[0]
        self.originale = charger_image(chemin_image)
        self.bruitee = None
        self.debruitee = None
        self.snr_bruitee = None
        self.snr_debruitee = None
        self.legende_bruitee = ""
        self.legende_debruitee = ""
        self.vue = "original"
        self.surface = creer_surface(self.originale)
        self.message = ""

        self.choix_bruit = 0
        self.choix_filtre = 0
        self.reglages_bruit = []


        for b in BRUITS:
            self.reglages_bruit.append(b["defaut"])

        x = MARGE
        largeur = PANNEAU - 2 * MARGE

        self.boutons_bruit = []
        y = 88
        for b in BRUITS:
            self.boutons_bruit.append(Bouton(b["nom"], x, y, largeur, 28))
            y = y + 32

        premier = BRUITS[0]
        self.curseur_bruit = Curseur(x, 212, largeur, premier["min"], premier["max"], premier["pas"], premier["defaut"])
        self.bouton_bruiter = Bouton("Bruiter", x, 242, largeur, 32)

        self.boutons_filtre = []
        y = 318
        for f in FILTRES:
            self.boutons_filtre.append(Bouton(f["nom"], x, y, largeur, 28))
            y = y + 32

        self.curseur_filtre = Curseur(x, 474, largeur, 3, 9, 2, 3)
        self.bouton_debruiter = Bouton("Débruiter", x, 504, largeur, 32)

        largeur_vue = (largeur - 8) // 3
        self.bouton_vue_originale = Bouton("Originale", x, 580, largeur_vue, 28)
        self.bouton_vue_bruitee = Bouton("Bruité", x + largeur_vue + 4, 580, largeur_vue, 28)
        self.bouton_vue_debruitee = Bouton("Débruite", x + 2 * (largeur_vue + 4), 580, largeur_vue, 28)


        self.update_buttons()

    def update_buttons(self):
        for i in range(len(self.boutons_bruit)):
            self.boutons_bruit[i].selectionne = (i == self.choix_bruit)

        etape2_possible = self.bruitee is not None
        for i in range(len(self.boutons_filtre)):
            self.boutons_filtre[i].selectionne = (i == self.choix_filtre)
            self.boutons_filtre[i].actif = etape2_possible
        self.curseur_filtre.actif = etape2_possible
        self.bouton_debruiter.actif = etape2_possible

        self.bouton_vue_bruitee.actif = self.bruitee is not None
        self.bouton_vue_debruitee.actif = self.debruitee is not None
        self.bouton_vue_originale.selectionne = (self.vue == "originale")
        self.bouton_vue_bruitee.selectionne = (self.vue == "bruitee")
        self.bouton_vue_debruitee.selectionne = (self.vue == "debruitee")

    def image_affichee(self):
        if self.vue == "bruitee":
            return self.bruitee
        if self.vue == "debruitee":
            return self.debruitee
        return self.originale

    def legende_affichee(self):
        if self.vue == "bruitee":
            return self.legende_bruitee
        if self.vue == "debruitee":
            return self.legende_debruitee
        return "Image originale"

    def afficher(self, vue):
        if vue == "bruitee" and self.bruitee is None:
            return
        if vue == "debruitee" and self.debruitee is None:
            return
        self.vue = vue
        self.surface = creer_surface(self.image_affichee())
        self.update_buttons()

    def afficher_message(self, texte):
        self.message = texte
        self.dessiner()
        pygame.display.flip()
        pygame.event.pump()

    def choisir_bruit(self, i):
        self.reglages_bruit[self.choix_bruit] = self.curseur_bruit.valeur
        self.choix_bruit = i
        b = BRUITS[i]
        self.curseur_bruit.changer_reglage(b["min"], b["max"], b["pas"], self.reglages_bruit[i])
        self.update_buttons()

    def choisir_filtre(self, i):
        self.choix_filtre = i
        self.update_buttons()

    def texte_reglage_bruit(self):
        b = BRUITS[self.choix_bruit]
        return b["reglage"] + " : " + str(self.curseur_bruit.valeur) + b["unite"]

    def texte_reglage_filtre(self):
        taille = str(self.curseur_filtre.valeur)
        return "Fenetre : " + taille + "×" + taille

    def bruiter(self):
        b = BRUITS[self.choix_bruit]

        self.bruitee = b["fonction"](self.originale, self.curseur_bruit.valeur)
        self.snr_bruitee = calculer_snr(self.originale, self.bruitee)
        self.legende_bruitee = "Image bruitée : " + b["nom"] + ", " + self.texte_reglage_bruit().lower()

        self.debruitee = None
        self.snr_debruitee = None

        self.message = ""
        self.afficher("bruitee")

    def debruiter(self):
        if self.bruitee is None:
            return
        f = FILTRES[self.choix_filtre]
        taille = self.curseur_filtre.valeur

        self.debruitee = f["fonction"](self.bruitee, taille)

        self.snr_debruitee = calculer_snr(self.originale, self.debruitee)
        self.legende_debruitee = "Image débruitée : " + f["nom"] + " " + str(taille) + "×" + str(taille)
        self.afficher("debruitee")


    def mouse_clicked(self, position):
        for i in range(len(self.boutons_bruit)):
            if self.boutons_bruit[i].est_clique(position):
                self.choisir_bruit(i)
        for i in range(len(self.boutons_filtre)):
            if self.boutons_filtre[i].est_clique(position):
                self.choisir_filtre(i)

        if self.bouton_bruiter.est_clique(position):
            self.bruiter()

        elif self.bouton_debruiter.est_clique(position):
            self.debruiter()
        elif self.bouton_vue_originale.est_clique(position):
            self.afficher("originale")
        elif self.bouton_vue_bruitee.est_clique(position):
            self.afficher("bruitee")
        elif self.bouton_vue_debruitee.est_clique(position):
            self.afficher("debruitee")

    def write(self, texte, x, y, police, couleur):
        rendu = police.render(texte, True, couleur)
        self.ecran.blit(rendu, (x, y))

    def dessiner(self):
        self.ecran.fill(FOND)
        pygame.draw.rect(self.ecran, FOND_PANNEAU, (0, 0, PANNEAU, HAUTEUR))
        self.write("Traitement d'images", MARGE, 24, self.police_titre, TEXTE)

        self.write("1. BRUITAGE", MARGE, 64, self.police_petite, TEXTE_DOUX)
        self.write(self.texte_reglage_bruit(), MARGE, 190, self.police_petite, TEXTE)
        self.curseur_bruit.dessiner(self.ecran)
        pygame.draw.line(self.ecran, BOUTON, (MARGE, 284), (PANNEAU - MARGE, 284))

        if self.bruitee is None:
            self.write("2. DÉBRUITAGE", MARGE, 294, self.police_petite, TEXTE_INACTIF)
            self.write(self.texte_reglage_filtre(), MARGE, 452, self.police_petite, TEXTE_INACTIF)
        else:
            self.write("2. DÉBRUITAGE", MARGE, 294, self.police_petite, TEXTE_DOUX)
            self.write(self.texte_reglage_filtre(), MARGE, 452, self.police_petite, TEXTE)

        self.curseur_filtre.dessiner(self.ecran)
        pygame.draw.line(self.ecran, BOUTON, (MARGE, 546), (PANNEAU - MARGE, 546))

        if self.snr_bruitee is None:
            self.write("SNR bruitée : -", MARGE, 624, self.police, TEXTE_DOUX)
        else:
            texte = f"SNR bruitée : {self.snr_bruitee:.2f} dB"
            self.write(texte, MARGE, 624, self.police, ACCENT)

        if self.snr_debruitee is None:
            self.write("SNR débruitée : -", MARGE, 646, self.police, TEXTE_DOUX)
        else:
            gain = self.snr_debruitee - self.snr_bruitee
            texte = f"SNR débruitée : {self.snr_debruitee:.2f} dB ({gain:+.2f})"
            self.write(texte, MARGE, 646, self.police, ACCENT)

        for bouton in self.boutons_bruit + self.boutons_filtre:
            bouton.dessiner(self.ecran, self.police)

        self.bouton_bruiter.dessiner(self.ecran, self.police)
        self.bouton_debruiter.dessiner(self.ecran, self.police)
        self.bouton_vue_originale.dessiner(self.ecran, self.police_petite)
        self.bouton_vue_bruitee.dessiner(self.ecran, self.police_petite)
        self.bouton_vue_debruitee.dessiner(self.ecran, self.police_petite)

        self.write(self.message, MARGE, 720, self.police_petite, TEXTE_DOUX)

        self.write(self.legende_affichee(), ZONE_X, 16, self.police, TEXTE)
        x_image = ZONE_X + (ZONE_LARGEUR - self.surface.get_width()) // 2
        self.ecran.blit(self.surface, (x_image, ZONE_Y))

    def run(self):
        horloge = pygame.time.Clock()
        continuer = True

        while continuer:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    continuer = False

                self.curseur_bruit.handle_event(evenement)
                self.curseur_filtre.handle_event(evenement)

                if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                    self.mouse_clicked(evenement.pos)

            self.dessiner()
            pygame.display.flip()
            horloge.tick(60)

        pygame.quit()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        chemin = sys.argv[1]
    else:
        chemin = IMAGE

    application = Application(chemin)
    application.run()