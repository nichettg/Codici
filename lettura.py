import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import importlib
import classi
importlib.reload(classi)
from classi import Misura,RisultatiFit

############################################################################################
### Input
############################################################################################

# Funzione Lettura File ".csv" in Dizionario
def csv_to_dict(csv: str, tab=False) -> dict:
    # L'opzione tab legge un file csv spaziato da tablature, classico se copia incollato da Excel
    if tab:
        dati = {} 
        with open(csv, "r") as f:
            header = f.readline().strip().split()
            for col in header:
                dati[col] = []
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue
                valori = riga.split()
                for col, val in zip(header, valori):
                    dati[col].append(float(val))
            for key in dati:
                dati[key] = np.array(dati[key])
        return dati
    else:
        df = pd.read_csv(csv)
        dizionario = {col: np.array(df[col]) for col in df.columns}
        return dizionario

# Funzione lettura file Pickle
def importa_pickle(filename="data.pkl"):
    import pickle
    with open(filename, "rb") as f:
        return pickle.load(f)

############################################################################################
### Output
############################################################################################

# Funzione per la Creazione di un File di Output Vuoto
def inizializza_output (output_filename):
    with open(output_filename, "w") as file:
        file.write('')

# Salva e mostra l'immagine
def salva_grafico(fig, nomefile, formato='jpg'):
    fig.savefig(nomefile, format=formato)

# Salva una analisi in un file testo
def salva_analisi(anal, parametri, nome_file):
    with open(nome_file, "w") as f:
        for i, nome in enumerate(parametri):
            valore = anal.val[i]
            errore = anal.s[i]
            
            # formato con 3 cifre significative
            riga = f"{nome} = {valore} ± {errore} ({errore/valore * 100:.2f}%)\n"
            f.write(riga)


# Funzionalità PICKLE per file dati molto lunghi
def esporta_pickle(data, filename="data.pkl"):
    import pickle
    inizializza_output(filename)
    with open(filename, "wb") as f:
        pickle.dump(data, f)

# Funzione che dalla classe RisultatiFit crea un dizionario
def ris_fit_to_dict(ris_fit):
    dizionario = {
        "parametri" : ris_fit.anal.val,
        "s_parametri" : ris_fit.anal.s,
        "res": ris_fit.res,
        "chi": ris_fit.chi,
        "chi_ridotto": ris_fit.chi_ridotto
    }
    return dizionario

def dict_to_ris_fit(dict):
    ris_fit = RisultatiFit(None,None,None)
    ris_fit.anal = Misura(dict["parametri"], dict["s_parametri"])
    ris_fit.res = dict["res"]
    ris_fit.chi = dict["chi"]
    ris_fit.chi_ridotto = dict["chi_ridotto"]
    return ris_fit

# Funzione Scrittura Dizionario in File ".csv"
def dict_to_csv(dizionario: dict, nome_file: str, risultati_fit = False):
    inizializza_output(nome_file)
    if risultati_fit:
        dizionario = ris_fit_to_dict(dizionario)
    df = pd.DataFrame(dizionario)
    df.to_csv(nome_file, index=False)