############################################################################################
### Importa i moduli nella cartella Codici
############################################################################################
import importlib
import sys
sys.path.append("/home/nichettg/Ubuntu/Laboratorio")


############################################################################################
### Moduli per la lettura dati
############################################################################################
import os
import json
import pandas as pd
import lettura as let
importlib.reload(let)


############################################################################################
### Moduli per l'analisi dati e Data Class Custom
############################################################################################
import numpy as np
from dataclasses import dataclass
@dataclass(frozen=True)
class misura:
    val: float
    s: float
@dataclass(frozen=True)
class misure:
    val: np.ndarray
    s: np.ndarray
import analisi as an
importlib.reload(an)

############################################################################################
### Moduli per la visualizzazione grafica dei dati
############################################################################################
import matplotlib.pyplot as plt
import grafici as gf
importlib.reload(gf)

gf.imposta_stile_globale()