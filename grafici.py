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
        "grid.linewidth": 0.5,
        "grid.alpha": 0.7,
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

def darken(color, factor=0.6):
    return tuple(factor * c for c in color)

# Interna
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

def display_dizionario(d):
    html = dict_to_html_table(d)
    display(HTML(html))

# Interna
def arrotonda(x, cifre=2):
    if x == 0:
        return 0
    potenza = int(np.floor(np.log10(abs(x))))
    fattore = 10**(cifre - 1 - potenza)
    return round(x * fattore) / fattore

def formatta_errore(val, err, unit=''):
    if err == 0:
        return rf"${val:.3f} \pm 0 {unit}$".strip()

    err_rounded = arrotonda(abs(err), 2)
    exp = int(np.floor(np.log10(err_rounded)))
    scale = 10 ** (-exp)
    val_scaled = val * scale
    err_scaled = err_rounded * scale

    if abs(exp) >= 2 or abs(val_scaled) >= 1e4 or abs(val_scaled) < 1e-3:
        return rf"$({val_scaled:.1f} \pm {err_scaled:.1f}) \times 10^{{{exp}}}$ {unit}".strip()
    else:
        return rf"${val_scaled:.1f} \pm {err_scaled:.1f}$ {unit}".strip()

def salva_dizionario(lista_dizionari, nome_file="output.html", titoli=None):
    with open(nome_file, "w") as f:
        f.write('<html><head><meta charset="UTF-8"><style>')
        f.write('table { border-collapse: collapse; margin-bottom: 20px; }')
        f.write('td, th { border: 1px solid black; padding: 5px; }')
        f.write('</style></head><body>\n')

        for i, diz in enumerate(lista_dizionari):
            if titoli: f.write(f"<h3>{titoli[i]}</h3>\n")
            else: f.write(f"<h3>Tabella {i + 1}</h3>\n")
            f.write('<table>\n')
            for freq, val in diz.items():
                f.write(f'<tr><td><strong>{freq}</strong></td><td>{val}</td></tr>\n')
            f.write('</table>\n')

        f.write('</body></html>')
