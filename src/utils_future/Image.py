from functools import cached_property

from PIL import Image as PImage

DEFAULT_MODE = 'HSV'


class Image:
    @staticmethod
    def id(t: tuple) -> str:
        return str(t)

    @staticmethod
    def pixel_id(pixel: tuple) -> str:
        return Image.id(pixel)

    def __init__(self, im: PImage):
        self.im = im

    def load(file_path: str):
        im = PImage.open(file_path)
        im = im.convert(DEFAULT_MODE)
        return Image(im)

    def write(self, output_path: str):
        self.im.save(output_path)

    def __str__(self) -> str:
        return f'Image({self.width}x{self.height})'

    def __repr__(self) -> str:
        return self.__str__()

    @cached_property
    def size(self):
        return self.im.size

    @cached_property
    def width(self):
        return self.size[0]

    @cached_property
    def height(self):
        return self.size[1]
