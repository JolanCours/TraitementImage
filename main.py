#web

import pygame
from pygame.locals import *
import os.path

from PIL import Image

#nos fichiers
import bruit
import debruitage


def init_pygame():
    pygame.init()


    fenetre = pygame.display.set_mode((800, 600))
    fond = pygame.image.load("images/gradient.png").convert()
    fenetre.blit(fond, (0, 0))



def loop_pygame():

    continuer = True
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
    pygame.quit()


class CustomImage:

    def __init__(self, image):
        self.image = Image.open(image)
        self.image_name = image.replace(".png", "").replace(".jpg", "").split("/")[1]
        self.width, self.height = self.image.size
        self.pixels = []

    def load(self):
        data = self.image.get_flattened_data()
        for y in range(0, self.height):
            temp_list = []
            for x in range(0, self.width):

                current_pixel = data[x + y]

                value = [
                    current_pixel[0],
                    current_pixel[1],
                    current_pixel[2]
                ]

                temp_list.append(value)

            self.pixels.append(temp_list)

        if not os.path.isfile(f"data/{self.image_name}.raw"):
            self.save()

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(f"data/{self.image_name}.raw", "w") as f:
            for ligne in self.pixels:
                for pixel in ligne:
                    f.write(f"{pixel[0]},{pixel[1]},{pixel[2]},")
                f.write(f"\n")




    def afficher(self):
        pass



image = CustomImage("images/gradient.png")


def mesurer_qualite_image():
    pass


if __name__ == '__main__':
    init_pygame()
    loop_pygame()

    bruit.poivre_sel()
    debruitage.filtrage_median()


    image.load()

