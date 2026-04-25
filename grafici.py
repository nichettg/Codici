import matplotlib.pyplot as plt
from matplotlib import rcParams
from itertools import cycle
from IPython.display import display, HTML
import numpy as np

############################################################################################
### Visualizzazione Dati e Grafici
############################################################################################

# Imposta automaticamente titolo, label degli assi e formatta i caratteri
def parametri_grafico(ax, titolo=None, xlabel=None, ylabel=None, zlabel=None, tridimensionale=False):

    if tridimensionale:
        if titolo: ax.set_title(titolo)
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)
        if zlabel: ax.set_zlabel(zlabel)
    else:
        if titolo: ax.set_title(titolo)
        if xlabel: ax.set_xlabel(xlabel)
        if ylabel: ax.set_ylabel(ylabel)

# Visualizzazione di un dizionario in Jupyter in tabella HTML
def display_dizionario(d):
    html = dict_to_html_table(d)
    display(HTML(html))

# Formattazione di un valore con incertezza alle giuste cifre significative
def formatta_errore(val, err, txt=False):
    if err < 0:
        raise ValueError("Errore negativo no grazie.")
    exp = int(np.floor(np.log10(abs(err))))
    val_sci = val / 10**exp
    err_sci = err / 10**exp
    err_sci = arrotonda_significative(err_sci, cifre=1)
    err_rounded = arrotonda_significative(err, cifre=1)
    exp_err = int(np.floor(np.log10(abs(err_rounded))))
    dec = max(0, -(exp_err - exp))

    valore = f"{val_sci:.{dec}f}"

    if float(valore) == 0:
        valore = "0"
    if txt:
        return f"( {valore} ± {err_sci:.{dec}f}) × 10^{exp}"
    return rf"({valore} \pm {err_sci:.{dec}f}) \times 10^{{{exp}}}"

############################################################################################
### Stile Estetico Grafici
############################################################################################

# Funzione chiamata automaticamente in ogni file con "moduli.py"
def imposta_stile_globale():
    rcParams.update({
        # Figure
        "figure.figsize": (10, 5),
        "figure.dpi": 400,

        # Titoli e testo
        "axes.titlesize": 20,
        "axes.labelsize": 18,
        "legend.fontsize": 16,
        "font.family": "serif",

        # Linee e marker
        "lines.linewidth": 2,
        "lines.markersize": 6,

        # Griglia
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.color": "gray",
        "grid.linewidth": 0.5,
        "grid.alpha": 0.7,
    })

# Parametri standard per errorbar
errorbar_params = {
        'elinewidth': 0.5,
        'capsize': 5,
        'capthick': 1,
        'fmt': '.',
    }

# Parametri standard per scatter
scatter_params ={
        's': 20,          # dimensione marker
        'marker': 'o',
        'alpha': 0.8,
    }

# Parametri standard per plot
plot_params = {
        'linewidth': 1.5,
        'linestyle': '-',
    }

# Parametri per axhline e axvline
line_params = {
        'linewidth': 1.0,
        'linestyle': '--',
        'alpha': 0.7
    }
line_params_ = {
        'linewidth': 1.0,
        'linestyle': '-',
        'alpha': 0.7
    }

# Ciclo di 10 colori
colori = [
        (0.121, 0.466, 0.705),  # blu
        (1.000, 0.498, 0.054),  # arancione
        (0.172, 0.627, 0.172),  # verde
        (0.839, 0.153, 0.157),  # rosso
        (0.580, 0.404, 0.741),  # viola
        (0.549, 0.337, 0.294),  # marrone
        (0.890, 0.467, 0.761),  # rosa
        (0.498, 0.498, 0.498),  # grigio
        (0.737, 0.741, 0.133),  # giallo-verde
        (0.090, 0.745, 0.811),  # ciano
    ]

ciclo_colori = cycle(colori)
#c = next(color_cycle)

# Scurisce un colore
def darken(color, factor=0.6):
    return tuple(factor * c for c in color)

# Numera i punti del grafico
def numera_punti(ax,x,y):
    for i, (xi, yi) in enumerate(zip(x, y)):
        ax.text(1/xi, 1/yi, str(i+1), fontsize=9, ha='left', va='bottom')


############################################################################################
### Funzioni Interne
############################################################################################
def arrotonda_significative(x, cifre=1):
    if x == 0:
        return 0.0

    x_abs = abs(x)
    exp = int(np.floor(np.log10(x_abs)))
    fattore = 10**(cifre - 1 - exp)
    y = round(x * fattore) / fattore
    if y == 0:
        y = np.sign(x) * 10**exp
    return y

def dict_to_html_table(d, depth=0):
    html = ''
    indent = '&nbsp;' * 4 * depth
    if isinstance(d, dict):
        html += '<table border="1" style="border-collapse: collapse;">'
        for key, value in d.items():
            html += '<tr>'
            html += f'<td>{indent}<strong>{key}</strong></td>'
            if isinstance(value, dict):
                html += f'<td>{dict_to_html_table(value, depth + 1)}</td>'
            else:
                html += f'<td>{indent}{value}</td>'
            html += '</tr>'
        html += '</table>'
    else:
        html += f'{indent}{d}'
    return html