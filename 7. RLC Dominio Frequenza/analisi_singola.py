############################################################################################
### Importa i moduli necessari nel codice
############################################################################################
import importlib
import sys
sys.path.append("/home/nichettg/Ubuntu/Laboratorio")

import os
import json
import pandas as pd
import lettura as let
importlib.reload(let)

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

import matplotlib.pyplot as plt
import grafici as gf
importlib.reload(gf)

gf.imposta_stile_globale()

############################################################################################
### Lettura
############################################################################################

### Lettura file json

with open("config_singola.json") as f:
    nomi = json.load(f)

file_input = os.path.join(nomi["cartella"]["input"],nomi["metodi"]["file_input"])

### Creazione cartelle

os.makedirs(nomi["cartella"]["output"], exist_ok=True)

### Lettura dati

dati = let.csv_to_dict(file_input)

xdata = misure(dati["x"],dati["sx"])
ydata = misure(dati["y"],dati["sy"])

############################################################################################
### Analisi
############################################################################################

def modello(par, x):
    return par[0] + par[1]*x

param_labels = ['a', 'b']

beta0 = [0, 1]

titolo = f"{nomi["metodi"]["titolo"]}"
file_output1 = os.path.join(
    nomi["cartella"]["output"],
    nomi["output"]["regressione"] + ".txt"
)
file_output2 = os.path.join(
    nomi["cartella"]["output"],
    nomi["output"]["residui"] + ".txt"
)
file_output3 = os.path.join(
    nomi["cartella"]["output"],
    nomi["output"]["chi"] + ".txt"
)

### Regressione

anal = an.fit(xdata, ydata, modello, beta0)
let.inizializza_output(file_output1)
let.salva_analisi(anal, param_labels, file_output1)

### Residui

let.inizializza_output(file_output2)
res = an.residui(xdata, ydata, anal.val, modello, file_output2, titolo)

### Chi Quadro

let.inizializza_output(file_output3)
chi = an.residui(xdata, ydata, anal.val, modello, file_output3, titolo)

############################################################################################
### Grafici
############################################################################################

xlabel = f"{nomi["metodi"]["xlabel"]}"
xunit = f"{nomi["metodi"]["xunit"]}"
ylabel = f"{nomi["metodi"]["ylabel"]}"
yunit = f"{nomi["metodi"]["yunit"]}"

file_output1 = os.path.join(
    nomi["cartella"]["output"],
    nomi["output"]["regressione"] + ".jpg"
)
file_output2 = os.path.join(
    nomi["cartella"]["output"],
    nomi["output"]["residui"] + ".jpg"
)
file_output3 = os.path.join(
    nomi["cartella"]["output"],
    nomi["output"]["chi"] + ".jpg"
)

### Regressione

# Inizializzazione e labels
fig,ax = plt.subplots(1, 1,  figsize=(10, 5), constrained_layout = True)
gf.parametri_grafico(ax, f"{titolo}, Regressione", xlabel= rf"${xlabel} [{xunit}]$", ylabel= rf"${ylabel} [{yunit}]$")

# Dati
ax.errorbar(
    xdata.val,
    ydata.val,
    xerr=xdata.s,
    yerr=ydata.s,
    label="Dati",
    **gf.errorbar_params,
    color = gf.colori[0]
)

# Fit
fit_label = "Fit: " + "".join(f"{param_labels[i]}={gf.formatta_errore(anal.val[i],anal.s[i])}\n" for i in range(len(param_labels)))
x_fit = np.linspace(min(xdata.val), max(xdata.val), 500)
ax.plot(
    x_fit,
    modello(anal.val,x_fit),
    label=fit_label,
    **gf.plot_params,
    color = gf.colori[1]
)

ax.legend()

let.salva_grafico(fig,file_output1)

### Residui

# Inizializzazione e label
fig,ax = plt.subplots(1, 1,  figsize=(10, 3), constrained_layout = True)
gf.parametri_grafico(ax, xlabel=rf"${xlabel} [{xunit}]$", ylabel="Residui")

# Residui
ax.errorbar(
    res[0],
    res[1],
    yerr=res[2],
    **gf.errorbar_params,
    color=gf.colori[0]
)
# Linea orizzontale
ax.axhline(
    0,
    **gf.line_params,
    color="red"
)

let.salva_grafico(fig, file_output2)

### Chi Quadro

# Inizializzaiozne e label
fig,ax = plt.subplots(1, 1,  figsize=(10, 3), constrained_layout = True)
gf.parametri_grafico(ax, xlabel=rf"${xlabel} [{xunit}]$", ylabel=r"$\chi^2$")

# Chi Quadri
ax.errorbar(
    chi[0],
    chi[1],
    yerr=chi[2],
    **gf.errorbar_params,
    color=gf.colori[0]
)

# Linea orizzontale
ax.axhline(
    0,
    **gf.line_params,
    color="red"
)

let.salva_grafico(fig, file_output3)
plt.show()