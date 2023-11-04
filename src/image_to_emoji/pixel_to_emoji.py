MIN_SAT = 0.2 * 256


def for_color_groups(emojis, emoji_no_color) -> str:
    def f(pixel_hsv):
        n_colors = len(emojis)
        (h, s, __) = pixel_hsv

        if s < MIN_SAT:
            return emoji_no_color

        dh = 0.5 / n_colors
        i = int((h / 256.0 + dh + 1) * n_colors) % n_colors
        return emojis[i]

    return f


def default(pixel_hsv) -> str:
    f = for_color_groups('🟤🟫🍫🔴🟥🩸🟠🟧🍊🟡🟨⭐🟢🟩🍏🔵🟦🥶🟣🟪🫐⬛⚫🎩', '⚪')
    return f(pixel_hsv)
