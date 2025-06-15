import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

def scrivi(ax, testo, pos=(0, 0), scala_x=1.0, scala_y=1.0, densita=0.5, colore='black', line=True, alpha=1):
    font = FontProperties(family="DejaVu Sans", weight="bold", size=100)
    tp = TextPath((0, 0), testo, prop=font)

    verts = tp.vertices
    verts = verts[::max(1, int(1 / densita))]

    verts = verts - verts.min(axis=0)
    verts = verts / verts.ptp(axis=0)

    x = verts[:, 0] * scala_x + pos[0]
    y = verts[:, 1] * scala_y + pos[1]

    if line==False: ax.plot(x, y, 'o', color=colore, markersize=1, zorder=10, alpha=alpha)
    elif line: ax.plot(x, y, color=colore, markersize=1, zorder=10, alpha=alpha)

from PIL import Image

def sfondo(ax, image_path, alpha=1.0):
    img = Image.open(image_path)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    ax.imshow(img, extent=[*xlim, *ylim], aspect='auto', zorder=0, alpha=alpha)
