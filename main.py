
import bruit
import debruitage
from PIL import Image

class CustomImage:

    def __init__(self, image):
        self.image = Image.open(image)
        self.width, self.height = self.image.size
        self.pixels = []

    def load(self):
        data = self.image.getdata()
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



    def afficher(self):
        pass



image = CustomImage("images/gradient.png")


def mesurer_qualite_image():
    pass


if __name__ == '__main__':
    bruit.poivre_sel()
    debruitage.filtrage_median()


    image.load()

