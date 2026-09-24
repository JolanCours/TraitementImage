import pygame
from pygame.locals import *
from PIL import Image
import os
import random
import bruit
import debruitage


class CustomImage:

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGB")

        self.width, self.height = self.image.size

        self.image_name = os.path.splitext(
            os.path.basename(image_path)
        )[0]

        self.pixels = []

    def load(self):
        self.pixels = []

        for y in range(self.height):
            ligne = []

            for x in range(self.width):
                r, g, b = self.image.getpixel((x, y))
                ligne.append([r, g, b])

            self.pixels.append(ligne)

    def get_pixels(self):
        return self.pixels

    def set_pixels(self, pixels):
        self.pixels = pixels

    def afficher(self, fenetre):

        surface = pygame.Surface((self.width, self.height))

        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[y][x]

                surface.set_at((x, y), (r, g, b))

        fenetre.blit(surface, (0, 0))


def main():

    pygame.init()

    fenetre = pygame.display.set_mode((1280, 853))
    pygame.display.set_caption("Traitement d'image")

    image = CustomImage("images/sample_1280×853.bmp")
    image.load()

    pixels = image.get_pixels()

    pixels = bruit.additif(pixels)
    
    continuer = True

    while continuer:

        for event in pygame.event.get():

            if event.type == QUIT:
                continuer = False

        fenetre.fill((30, 30, 30))

        image.afficher(fenetre)

        pygame.display.flip()
    
    pixels = bruit.convolution(pixels)
    
    image.pixels = pixels
    
    debruitage = True;
    
    while debruitage:
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                debruitage = False
                
        fenetre.fill((30,30,30))
        
        image.afficher(fenetre)
        
        pygame.display.flip()
        
    pygame.quit()


if __name__ == "__main__":
    main()