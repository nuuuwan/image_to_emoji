from functools import cache, cached_property

from PIL import Image as PImage
from sklearn.cluster import KMeans
from utils import Log

DEFAULT_MODE = 'HSV'
log = Log('Image')
MIN_SAT = 0.2 * 256


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

    @cached_property
    def pixels(self) -> list[tuple]:
        pixels = []
        for i in range(self.width):
            for j in range(self.height):
                pixels.append(self.im.getpixel((i, j)))
        return pixels

    @cache
    def cluster_pixels(self, n_clusters: int):
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(self.pixels)
        return list(kmeans.labels_)
