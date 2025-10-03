from typing import Tuple


def hue_to_rgb(h: float) -> Tuple[int, int, int]:
    h = h % 1.
    h *= 6.0
    c = 255
    x = int(255 - 255. * abs(h % 2 - 1.0))
    if h < 1:
        r, g, b = c, x, 0
    elif h < 2:
        r, g, b = x, c, 0
    elif h < 3:
        r, g, b = 0, c, x
    elif h < 4:
        r, g, b = 0, x, c
    elif h < 5:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return r, g, b
