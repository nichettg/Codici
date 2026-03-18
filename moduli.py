"""
Importa i moduli nella cartella Codici
"""
import importlib
import sys
sys.path.append("/home/nichettg/Ubuntu/Laboratorio")

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
Meme
"""
import meme as meme