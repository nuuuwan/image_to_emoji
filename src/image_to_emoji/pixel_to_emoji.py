import colorsys

MIN_SAT = 0.2


def for_color_groups(emojis, emoji_no_color) -> str:
    def f(pixel):
        n_colors = len(emojis)
        (r, g, b, __) = pixel
        (h, s, __) = colorsys.rgb_to_hsv(r, g, b)

        if s < MIN_SAT:
            return emoji_no_color

        dh = 0.5 / n_colors
        i = int((h + dh + 1) * n_colors) % n_colors
        return emojis[i]

    return f


def default(pixel) -> str:
    f = for_color_groups('🟤🔴🟠🟡🟢🔵🟣⚫', '⚪')
    return f(pixel)
