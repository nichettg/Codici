import matplotlib.pyplot as plt
from matplotlib import rcParams
from IPython.display import display, HTML
import numpy as np

# ======== IMPOSTAZIONI GLOBALI ========
def imposta_stile_globale():
    rcParams.update({
        # Figure
        "figure.figsize": (8, 6),
        "figure.dpi": 200,

        # Titoli e testo
        "axes.titlesize": 20,
        "axes.labelsize": 18, # Dimensione etichette assi
        "legend.fontsize": 16,
        "font.family": "serif",

        # Linee e marker
        "lines.linewidth": 2,
        "lines.markersize": 6,

        # Griglia
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.color": "gray",
    })

def default_error_params():
    return {
        'elinewidth': 0.5,
        'capsize': 5,
        'capthick': 1,
    }

# Imposta automaticamente titolo, label degli assi e formatta i caratteri
def parametri_grafico(ax, titolo=None, xlabel=None, ylabel=None, zlabel=None, tridimensionale=False):

    if tridimensionale:
        if titolo: ax.set_title(titolo, pad=20)
        if xlabel: ax.set_xlabel(xlabel, labelpad=10)
        if ylabel: ax.set_ylabel(ylabel, labelpad=10)
        if zlabel: ax.set_zlabel(zlabel, labelpad=10)
        ax.tick_params(axis='both', labelsize=16)
        ax.tick_params(axis='z', labelsize=16)
    else:
        if titolo: ax.set_title(titolo, pad=15)
        if xlabel: ax.set_xlabel(xlabel, labelpad=10)
        if ylabel: ax.set_ylabel(ylabel, labelpad=10)

    ax.tick_params(axis='both', labelsize=16)

# Funzione linea
def linea(ax, vx, color='black', verticale=False, salto=0):
    if verticale:
        ax.plot(np.zeros(len(vx)) + salto, vx, color=color, linestyle="-.", linewidth=1)
    else: ax.plot(vx, np.zeros(len(vx)) + salto, color=color, linestyle="-.", linewidth=1)

# Funzione per creare una descrizione della legenda
def descrizione_legenda(ax, testo, color=None, marker=None, show=False):
    if color is not None and marker is not None:
        ax.scatter([], [], label=testo, s=5, marker=marker, color=color)
    elif color is not None:
        ax.scatter([], [], label=testo, s=5, color=color)
    else:
        ax.plot([], [], label=testo, linestyle='None', marker='', color='black')
    if show:
        ax.legend(bbox_to_anchor=(1,1))


# Salva e mostra l'immagine
def salva_grafico(fig, nomefile, legenda=(1, 1), formato='pdf', noLegenda=False):
    fig.tight_layout()

    if not noLegenda:
        fig.legend(bbox_to_anchor=legenda, loc='upper left')

    fig.savefig(nomefile, bbox_inches='tight', format=formato)

    plt.show()


def tabula (tabelle):

    if not isinstance(tabelle, list):
        tabelle = [tabelle]

    html = '<div style="display: flex; gap: 40px; flex-wrap: wrap;">' + \
       ''.join(f'<div>{tbl}</div>' for tbl in tabelle) + \
       '</div>'

    display(HTML(html))