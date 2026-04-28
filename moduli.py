############################################################################################
### Importa i moduli necessari nel codice
############################################################################################
import importlib
import os
import json
import pandas as pd
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt

import classi
importlib.reload(classi)
from classi import Misura,RisultatiFit
import lettura as let
importlib.reload(let)
import analisi as an
importlib.reload(an)
import grafici as gf
importlib.reload(gf)

gf.imposta_stile_globale()

def analizza(json_path: str, modello, param_labels, beta0):
    ############################################################################################
    ### Lettura
    ############################################################################################

    ### Lettura file json

    with open(json_path) as f:
        nomi = json.load(f)

    file_input = os.path.join(nomi["cartella"]["input"],nomi["metodi"]["file_input"])

    ### Creazione cartelle

    os.makedirs(nomi["cartella"]["output"], exist_ok=True)

    ### Lettura dati

    dati = let.csv_to_dict(file_input)

    xdata = Misura(dati["x"],dati["sx"])
    ydata = Misura(dati["y"],dati["sy"])

    ############################################################################################
    ### Analisi
    ############################################################################################

    titolo = f"{nomi['metodi']['titolo']}"
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
    chi = an.chi_quadro(xdata, ydata, anal.val, modello, file_output3, titolo)

    ############################################################################################
    ### Grafici
    ############################################################################################

    xlabel = f"{nomi['metodi']['xlabel']}"
    xunit = f"{nomi['metodi']['xunit']}"
    ylabel = f"{nomi['metodi']['ylabel']}"
    yunit = f"{nomi['metodi']['yunit']}"

    file_output1 = os.path.join(
        nomi["cartella"]["output"],
        nomi["output"]["regressione"] + ".jpg"
    )
    file_output2 = os.path.join(
        nomi["cartella"]["output"],
        nomi["output"]["chi"] + ".jpg"
    )

    ### Regressione

    # Inizializzazione e labels
    fig1, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(10, 8),
        gridspec_kw={'height_ratios': [5, 3]},
        constrained_layout=True,
        sharex=True
    )
    ax1.tick_params(axis='x', labelbottom=False)
    gf.parametri_grafico(ax1, f"{titolo}", ylabel= rf"${ylabel}\quad [{yunit}]$")
    gf.parametri_grafico(ax2, xlabel=rf"${xlabel}\quad [{xunit}]$", ylabel="Residui")

    fig2,ax = plt.subplots(1, 1,  figsize=(10, 3), constrained_layout = True)
    gf.parametri_grafico(ax, xlabel=rf"${xlabel}\quad [{xunit}]$", ylabel=r"$\chi^2$")

    # Dati
    ax1.errorbar(
        xdata.val,
        ydata.val,
        xerr=xdata.s,
        yerr=ydata.s,
        label="Dati",
        **gf.errorbar_params,
        color = gf.colori[0]
    )

    # Fit
    fit_label = f"Fit {titolo}:\n" + "".join(f"${param_labels[i]}$=${gf.formatta_errore(anal.val[i],anal.s[i])}$\n" for i in range(len(param_labels)))
    x_fit = np.linspace(min(xdata.val), max(xdata.val), 500)
    ax1.plot(
        x_fit,
        modello(anal.val,x_fit),
        label=fit_label,
        **gf.plot_params,
        color = gf.colori[1]
    )

    ax1.legend()

    # Residui
    ax2.errorbar(
        res[0],
        res[1],
        yerr=res[2],
        **gf.errorbar_params,
        color=gf.colori[0]
    )

    # Linea orizzontale
    ax2.axhline(
        0,
        **gf.line_params,
        color="red"
    )

    let.salva_grafico(fig1, file_output1)

    ### Chi Quadro

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

    let.salva_grafico(fig2, file_output2)
    plt.show()

    return RisultatiFit(anal,res,chi)