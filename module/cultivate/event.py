import numpy as np
from method.image_handler import *


def event(d, screen):

    if np.all(screen[679, 360] == np.array([3, 206, 121])):
        d.click(360, 720)
    elif np.all(screen[567, 360] == np.array([3, 206, 121])):
        d.click(360, 610)
    elif np.all(screen[343, 360] == np.array([3, 206, 121])):
        d.click(360, 830)
