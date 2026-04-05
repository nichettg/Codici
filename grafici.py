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

# Visualizzazione di un dizionario in Jupyter in tabella HTML
def display_dizionario(d):
    html = dict_to_html_table(d)
    display(HTML(html))

# Formattazione di un valore con incertezza alle giuste cifre significative
def formatta_errore(val, err, unit='', html=False, txt=False):
    if err < 0:
        raise ValueError("Errore negativo no grazie.")

    # caso errore zero
    if np.isclose(err, 0):
        val_rounded = round(val, 3)
        if html:
            return f"{val_rounded:.3f} &plusmn; 0 {unit}"
        return rf"${val_rounded:.3f} \pm 0$ {unit}"

    # arrotonda errore a 1 cifra significativa
    err_round = arrotonda_significative(err, cifre=1)

    # ordine di grandezza errore
    exp_err = int(np.floor(np.log10(err_round)))
    dec = max(0, -exp_err)

    # 👉 SE TROPPI DECIMALI → SCIENTIFICA
    if dec > 3:
        exp = int(np.floor(np.log10(abs(val)))) if val != 0 else exp_err

        val_sci = val / 10**exp
        err_sci = err / 10**exp

        err_sci = arrotonda_significative(err_sci, cifre=1)

        # numero di decimali per mantissa
        exp_err_sci = int(np.floor(np.log10(err_sci)))
        dec_sci = max(0, -exp_err_sci)

        if html:
            return f"({val_sci:.{dec_sci}f} &plusmn; {err_sci:.{dec_sci}f}) × 10<sup>{exp}</sup> {unit}"
        if txt:
            return f"({val_sci:.{dec_sci}f} ± {err_sci:.{dec_sci}f}) × 10^{exp} {unit}"
        return rf"$({val_sci:.{dec_sci}f} \pm {err_sci:.{dec_sci}f}) \times 10^{{{exp}}}$ {unit}"

    # 👉 CASO NORMALE
    val_round = round(val, dec)

    if html:
        return f"{val_round:.{dec}f} &plusmn; {err_round:.{dec}f} {unit}"
    if txt:
        return f"{val_round:.{dec}f} ± {err_round:.{dec}f} {unit}"
    else:
        return rf"${val_round:.{dec}f} \pm {err_round:.{dec}f}$ {unit}"

############################################################################################
### Stile Estetico Grafici
############################################################################################

# Funzione chiamata automaticamente in ogni file con "moduli.py"
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

# Scala gli errori se difficili da vedere
def scaled_error_params(y, scale_factor=1.0):
    scale = (max(y) - min(y)) * scale_factor
    return {
        'elinewidth': 0.02 * scale,
        'capsize':    0.05 * scale,
        'capthick':   0.02 * scale,
    }

# Numera i punti del grafico
def numera_punti(ax,x,y):
    for i, (xi, yi) in enumerate(zip(x, y)):
        ax.text(1/xi, 1/yi, str(i+1), fontsize=9, ha='left', va='bottom')

############################################################################################
### Importazine e Esportazione
############################################################################################

# Salva e mostra l'immagine
def salva_grafico(fig, nomefile, formato='pdf', show=True):
    fig.tight_layout()

    fig.savefig(nomefile, bbox_inches='tight', format=formato, dpi=600, pad_inches=0.2)

    if show:
        plt.show()

# Salva una analisi in un file testo
def salva_analisi(anal, parametri, nome_file):
    with open(nome_file, "w") as f:
        for i, nome in enumerate(parametri):
            valore = anal[i, 0]
            errore = anal[i, 1]
            
            # formato con 3 cifre significative
            riga = f"{nome} = {formatta_errore(valore,errore,txt=True)} ({errore/valore * 100:.2f}%)\n"
            f.write(riga)

# Salva un dizionario come tabella in LATEX
def dict_to_latex_table(d, depth=0):
    latex = ""
    indent = "\\quad " * depth

    if isinstance(d, dict):
        latex += "\\begin{tabular}{|l|l|}\n"
        latex += "\\hline\n"
        for key, value in d.items():
            latex += f"{indent}\\textbf{{{key}}} & "
            if isinstance(value, dict):
                latex += "\\\\\n"
                latex += "\\hline\n"
                latex += f"\\multicolumn{{2}}{{|l|}}{{\n{dict_to_latex_table(value, depth + 1)}\n}} \\\\\n"
            else:
                latex += f"{indent}{value} \\\\\n"
            latex += "\\hline\n"
        latex += "\\end{tabular}"
    else:
        latex += f"{indent}{d}"

    return latex

# Funzionalità PICKLE per file dati molto lunghi
def esporta_pickle(data, filename="data.pkl"):
    import pickle
    with open(filename, "wb") as f:
        pickle.dump(data, f)
def importa_pickle(filename="data.pkl"):
    import pickle
    with open(filename, "rb") as f:
        return pickle.load(f)

############################################################################################
### Funzioni Interne
############################################################################################
def arrotonda_significative(x, cifre=2):
    if x == 0:
        return 0.0
    exp = int(np.floor(np.log10(abs(x))))
    fattore = 10**(cifre - 1 - exp)
    return round(x * fattore) / fattore

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