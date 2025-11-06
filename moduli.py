"""
Importa i moduli nella cartella Codici
"""
import importlib
import sys
sys.path.append("/home/nichettg/Linux Programmi/Codici")

"""
Moduli per la raccolta dati
"""
import os
import pandas as pd

"""
Moduli per l'analisi dati
"""
import numpy as np
import funzioni as f
importlib.reload(f)

"""
Moduli per la visualizzazione grafica
"""
import matplotlib.pyplot as plt
import grafici as gf
importlib.reload(gf)

gf.imposta_stile_globale()

"""
Cicli di colori
"""
import itertools

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
color_cycle_fisso = itertools.cycle(colors)

cmap = plt.get_cmap('tab10')
color_cycle = itertools.cycle(cmap.colors)

"""
Meme
"""
import meme as meme