import matplotlib.pyplot as plt
from matplotlib import rcParams

# ======== IMPOSTAZIONI GLOBALI ========
def imposta_stile_globale():
    rcParams.update({
        # Figure
        "figure.figsize": (8, 6),
        "figure.dpi": 200,

        # Titoli e testo
        "axes.titlesize": 16,
        "axes.labelsize": 14, # Dimensione etichette assi
        "legend.fontsize": 12,
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

# ======== FUNZIONI PER GRAFICI 2D ========
def setup_2d_axes(ax, titolo=None, xlabel=None, ylabel=None):
    if titolo: ax.set_title(titolo, pad=15)
    if xlabel: ax.set_xlabel(xlabel, labelpad=10)
    if ylabel: ax.set_ylabel(ylabel, labelpad=10)
    ax.tick_params(axis='both', labelsize=12)   # Dimensione valori assi


# ======== FUNZIONI PER GRAFICI 3D ========
def setup_3d_axes(ax, titolo=None, xlabel=None, ylabel=None, zlabel=None):
    if titolo: ax.set_title(titolo, pad=20)
    if xlabel: ax.set_xlabel(xlabel, labelpad=10)
    if ylabel: ax.set_ylabel(ylabel, labelpad=10)
    if zlabel: ax.set_zlabel(zlabel, labelpad=10)
    ax.tick_params(axis='both', labelsize=12)
    ax.tick_params(axis='z', labelsize=12) # Dimensione valori asse z


# ======== LAYOUT & SALVATAGGIO ========
def salva_figura(nomefile, legenda = (1,1), formato='pdf'):
    plt.tight_layout()
    plt.legend(bbox_to_anchor = legenda, loc = 'upper left')
    plt.savefig(nomefile, bbox_inches='tight', format=formato)
    plt.show()