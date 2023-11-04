import os
from functools import cached_property

from utils import File, Log, String

from utils_future import Image

log = Log('ImageToEmoji')

DEFAULT_MAX_DIM = 20
MIN_SAT = 0.2 * 256


class ImageToEmoji:
    def __init__(
        self,
        image_path: str,
        emojis,
        max_dim: int = None,
    ):
        self.image_path = image_path
        self.max_dim = max_dim or DEFAULT_MAX_DIM
        self.emojis = emojis
        self.image = Image.load(self.image_path)

    @cached_property
    def hashtag(self):
        return (
            '#'
            + String(os.path.basename(self.image_path).split('.')[0]).camel
        )

    @cached_property
    def emoji_width(self):
        return int(self.image.width / self.k)

    @cached_property
    def emoji_height(self):
        return int(self.image.height / self.k)

    @cached_property
    def k(self) -> float:
        return max(self.image.width, self.image.height) / self.max_dim

    @cached_property
    def id_to_ci_to_n(self) -> dict:
        n_clusters = len(self.emojis) - 1
        ci_list = self.image.cluster_pixels(n_clusters)
        id_to_ci_to_n = {}
        ci_to_n = {}
        for i in range(self.image.width):
            ei = int(i / self.k)
            for j in range(self.image.height):
                ej = int(j / self.k)
                id = Image.id([ei, ej])

                pixel = self.image.im.getpixel((i, j))
                s = pixel[1]
                if s < MIN_SAT:
                    ci = 0
                else:
                    ci = ci_list[i * self.image.height + j] + 1
                if id not in id_to_ci_to_n:
                    id_to_ci_to_n[id] = {}
                if ci not in id_to_ci_to_n[id]:
                    id_to_ci_to_n[id][ci] = 0
                id_to_ci_to_n[id][ci] += 1
                if ci not in ci_to_n:
                    ci_to_n[ci] = 0
                ci_to_n[ci] += 1
        log.info(f'ci_to_n: {ci_to_n}')
        return id_to_ci_to_n

    def get_emoji_inner_lines(self) -> list[str]:
        lines = []
        max_ci_to_n = {}
        for ej in range(self.emoji_height):
            line = []
            for ei in range(self.emoji_width):
                id = Image.id([ei, ej])
                ci_to_n = self.id_to_ci_to_n[id]
                sorted_ci_to_n = sorted(
                    ci_to_n.items(), key=lambda x: x[1], reverse=True
                )
                max_ci = sorted_ci_to_n[0][0]
                if max_ci not in max_ci_to_n:
                    max_ci_to_n[max_ci] = 0
                max_ci_to_n[max_ci] += 1
                line.append(self.emojis[max_ci])
            lines.append(''.join(line))
        log.info(f'{max_ci_to_n=}')
        return lines

    def get_emoji(self) -> str:
        lines = ['']
        lines.append(self.hashtag)
        lines.extend(self.get_emoji_inner_lines())
        lines.append('')
        return '\n'.join(lines)

    def write(self, output_path: str) -> None:
        File(output_path).write(self.get_emoji())
        log.info(f'Wrote emoji to {output_path}')
