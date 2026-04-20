import numpy as np
import sympy as sp
import pandas as pd
from scipy.optimize import minimize
from scipy import odr

############################################################################################
### Data Class Custom
############################################################################################
import importlib
import classi
importlib.reload(classi)
from classi import Misura

############################################################################################
### Statistica Base
############################################################################################

# Funzione media pesata
def media_p(x: Misura) -> Misura:
    w = 1 / x.s**2
    media = np.sum(x.val * w) / np.sum(w)
    s_media = np.sqrt( 1 / np.sum(w) )
    return Misura(media,s_media)

# Funzione semidispersione massima
def semidisp(x: np.ndarray) -> float:
    return (np.max(x) - np.min(x)) / 2

# Funzione matrice covarianza campionaria
def matrice_covarianza(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    da = a - np.mean(a)
    db = b - np.mean(b)

    # varianze e covarianza
    var_a = np.sum(da * da) / (len(a) - 1)
    var_b = np.sum(db * db) / (len(b) - 1)
    cov_ab = np.sum(da * db) / (len(a) - 1)

    return np.array([[var_a, cov_ab],
                     [cov_ab, var_b]])



############################################################################################
### Test Statistici
############################################################################################


# Compatibilità tra Due Misure
def compatibilita(a:Misura, b:Misura) -> float:
    return abs(a.val - b.val) / np.sqrt(a.s**2 + b.s**2)



# Coefficiente di Pearson
def pearson(x: np.ndarray, y: np.ndarray) -> Misura:

    N = len(x)
    matrice = matrice_covarianza(x,y)
    cov_xy = matrice[0][1]
    sx = np.sqrt(matrice[0][0])
    sy = np.sqrt(matrice[1][1])

    r = cov_xy / (sx * sy)
    sigma_r = np.sqrt((1 - r**2) / (N - 2))

    return Misura(r, sigma_r)


# Test dei Residui
def residui(xdata: Misura, ydata: Misura, par: np.ndarray, modello, file: str, titolo: str, n=8, f=2):
    # n decide la spaziatura tra i valori
    # f decide le cifre significative
    somma = 0.
    residui = []

    vx = xdata.val
    vsx = xdata.s
    vy = ydata.val
    vsy = ydata.s

    with open(file, 'a') as output_elab:
        output_elab.write(f"Test residui {titolo}_____________________________________________\n")
        output_elab.write(f"{'':<3}{'x':<{n}}{'y':<{n}}{'y*':<{n}}{'res':<{n}}{'s_res':<{n}}\n")
        for i, (x, y) in enumerate(zip(vx, vy)):
            y_star = modello(par, x)
            res = y - y_star
            s_res = vsy[i]  # banalmente uguale a sy

            somma += abs(res)
            residui.append([x, res, s_res])

            output_elab.write(
                f"{i+1:<3}{x:<{n}.{f}f}{y:<{n}.{f}f}{y_star:<{n}.{f}f}"
                f"{res:<{n}.{f}f}{s_res:<{n}.{f}f}\n"
            )
        output_elab.write(f"\nSomma residui = {somma:.{f}f}\n")
    residui = np.array(residui)
    res = np.array([residui[:,0], residui[:,1], residui[:,2]])
    return res



# Test del Chi Quadro
def chi_quadro(xdata: Misura, ydata: Misura, par: np.ndarray, modello, file: str, titolo: str, n=8, f=2):
    # n decide la spaziatura tra i valori
    # f decide le cifre significative
    somma = 0.
    chi_quadri = []

    vx = xdata.val
    vsx = xdata.s
    vy = ydata.val
    vsy = ydata.s

    with open(file, 'a') as output_elab:
        output_elab.write(f"Test Chi Quadro {titolo}_____________________________________________\n")
        output_elab.write(f"{'':<3}{'x':<{n}}{'y':<{n}}{'y*':<{n}}{'sy':<{n}}{'Chi':<{n}}\n")
        for i,(x,y) in enumerate(zip(vx,vy)):
            y_star = modello(par,x)
            chi = ((y-y_star)/vsy[i])**2
            s_chi = vsy[i]

            somma += chi
            chi_quadri.append([x, chi, s_chi])

            output_elab.write(f"{i+1:<3}{x:<{n}.{f}f}{y:<{n}.{f}f}{y_star:<{n}.{f}f}{vsy[i]:<{n}.{f}f}{chi:<{n}.{f}f}\n")
        output_elab.write(f"Chi Quadro = {somma:.{f}f}\n")
        if np.isscalar(par):
                gradi = len(vy) - 1
        else:
            gradi = len(vy) - len(par)
        output_elab.write(f"Gradi Libertà = {gradi}\n")
        output_elab.write(f"Chi Quadro Ridotto = {somma/gradi:.{f}f}\n\n")
    chi_quadri = np.array(chi_quadri)
    chi = np.array([chi_quadri[:,0], chi_quadri[:,1], chi_quadri[:,2]])
    return chi


############################################################################################
### Regressioni
############################################################################################


# Minimi Quadrati Analitici con Incertezze Uniformi o Variabili sulle Ordinate
def minimi_quadrati(x: np.ndarray, y: Misura):
    y = Misura.val
    sy = Misura.s

    if np.isscalar(sy):
        sy = np.full_like(y, fill_value=sy, dtype=float)

    sy = np.array(sy)
    w = 1 / sy**2

    W = np.sum(w)
    Wx = np.sum(w * x)
    Wy = np.sum(w * y)
    Wxx = np.sum(w * x * x)
    Wxy = np.sum(w * x * y)

    Delta = W * Wxx - Wx**2
    b = (W * Wxy - Wx * Wy) / Delta
    a = (Wxx * Wy - Wx * Wxy) / Delta

    sigma_b = np.sqrt(W / Delta)
    sigma_a = np.sqrt(Wxx / Delta)
    cov_ab = -Wx / Delta
    
    return [[a, sigma_a],
            [b, sigma_b],
            cov_ab]


# Fit Non Lineare con Minimizzazione del Chi Quadro o con Modello ODR
def fit(xdata: Misura, ydata: Misura, modello, beta0, chi=True) -> Misura:
    # Il parametro "chi" fa il fit minimizzando il chi quadro, altrimenti viene fatto con ODR
    # Nel modello definire prima par e poi x
    # Il risultato della funzione è una matrice che ha in ogni riga il valore del parametro e la sua incertezza, l'ordine è quello definito nel modello
    x = xdata.val
    sx = xdata.s
    y = ydata.val
    sy = ydata.s

    def chi2(par, x, y, sy):
        return np.sum(((y - modello(par,x)) / sy) ** 2)

    if chi:
        res = minimize(chi2, beta0, args=(x, y, sy))
        anal_chi = [
            [res.x[i], np.sqrt(abs(res.hess_inv[i][i]))]
            for i in range(len(res.x))
        ]
        val = np.array([p[0] for p in anal_chi])
        err = np.array([p[1] for p in anal_chi])
        return Misura(val, err)

    model = odr.Model(modello)
    data_odr = odr.RealData(x, y, sx=sx, sy=sy)
    odr_instance = odr.ODR(data_odr, model, beta0=beta0)
    res = odr_instance.run()

    anal_odr = [
        [res.beta[i], res.sd_beta[i]]
        for i in range(len(res.beta))
    ]
    val = np.array([p[0] for p in anal_odr])
    err = np.array([p[1] for p in anal_odr])
    return Misura(val, err)


############################################################################################
### Altre Funzioni
############################################################################################


# Funzione Percentuale
def percento(x, perc, stringa):
    if stringa == "+": return x * (1 + perc/100)
    if stringa == "-": return x * (1 - perc/100)


# Propagazione delle Incertezze SENZA COVARIANZA
def propaga_incertezza(formula, variabili, valori = None, incertezze=None, ritorno=False):
    """
    formula: stringa, es. 'x * y + z**2'
    variabili: lista di stringhe, es. ['x', 'y', 'z']
    valori: lista di valori numerici, es. [1.0, 2.0, 0.5]
    incertezze: lista di incertezze, es. [0.1, 0.2, 0.05]
    """

    simboli = sp.symbols(variabili)
    f = sp.sympify(formula)
    derivati = [sp.diff(f, var) for var in simboli]

    if ritorno==True:
        # Sostituzione dei valori e delle incertezze
        dizionario = dict(zip(simboli, valori))
        risultato = sp.sqrt(sum((float(der.evalf(subs=dizionario)) * incertezze[i])**2 for i, der in enumerate(derivati)))

    # Creazione della stringa per la propagazione dell'incertezza
    stringa = 'sqrt('
    for i, (der, var) in enumerate(zip(derivati, simboli)):
        # Aggiungi la parte della derivata
        stringa += f'( {str(der)} * s{str(var)} )**2'
        
        # Aggiungi "+" se non è l'ultimo elemento
        if i < len(derivati) - 1:
            stringa += ' + '
    stringa += ')'

    if ritorno==True:
        return float(risultato), stringa
    else: return stringa


############################################################################################
### Funzioni Interne
############################################################################################
def arrotonda_significative(x, cifre=2):
    if x == 0:
        return 0.0
    exp = int(np.floor(np.log10(abs(x))))
    fattore = 10**(cifre - 1 - exp)
    return round(x * fattore) / fattore
def form(float):
    if float == 0.0:
        return 0.0
    elif float < 1e-5 or float > 1e5:
        return f"{float:.2e}"
    else:
        return f"{float:.5f}"
def formatta_errore(val, err, unit='', html=False, txt=False):
    if err < 0:
        raise ValueError("Errore negativo no grazie.")

    # caso errore zero
    if np.isclose(err, 0):
        val_rounded = round(val, 3)
        if html:
            return f"{val_rounded:.3f} &plusmn; 0 {unit}"
        return rf"${val_rounded:.3f} \pm 0$ {unit}"

    # arrotonda l’errore a una cifra significativa (standard)
    err_round = arrotonda_significative(err, cifre=1)

    # trova il numero di decimali richiesto
    exp_err = int(np.floor(np.log10(err_round)))
    dec = max(0, -exp_err)

    # arrotonda il valore allo stesso numero di decimali
    val_round = round(val, dec)

    # stampa
    if html:
        return f"{val_round:.{dec}f} &plusmn; {err_round:.{dec}f} {unit}"
    if txt:
        return f"{val_round:.{dec}f} ± {err_round:.{dec}f} {unit}"
    return rf"${val_round:.{dec}f} \pm {err_round:.{dec}f}$ {unit}"