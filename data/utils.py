from pygame.image import load
from os.path import abspath,join
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)

def load_sprite(name, with_alpha=True, folder='sprites'):
    path = resource_path(f"data\{folder}\{name}")
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()