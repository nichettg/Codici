import numpy as np
import sympy as sp
from scipy.optimize import minimize
from scipy import odr

# Funzione media pesata
def media_p(vx, vsx):
    vx = np.array(vx, dtype=float)
    vsx = np.array(vsx, dtype=float)
    vw = 1 / vsx**2
    media = np.array([np.sum(vx * vw) / np.sum(vw),
                      np.sqrt( 1 / np.sum(vw) )])
    return media

# Funzione semidispersione massima
def semidisp(vx):
    vx = np.array(vx, dtype=float)
    return (np.max(vx) - np.min(vx)) / 2

# Funzione matrice covarianza campionaria
def matrice_covarianza(a, b):
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
def compatibilita(f1, sf1, f2, sf2):
    f1 = float(f1)
    sf1 = float(sf1)
    f2 = float(f2)
    sf2 = float(sf2)
    return abs(f1 - f2) / np.sqrt(sf1**2 + sf2**2)



# Coefficiente di Pearson
def pearson(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    N = len(x)
    matrice = matrice_covarianza(x,y)
    cov_xy = matrice[0][1]
    sx = np.sqrt(matrice[0][0])
    sy = np.sqrt(matrice[1][1])

    r = cov_xy / (sx * sy)
    sigma_r = np.sqrt((1 - r**2) / (N - 2))

    return np.array([r, sigma_r])


# Test dei Residui
def residui(vx,vy,par,modello,file,titolo,n=8,f=2):
    somma = 0.
    # n decide la spaziatura tra i valori
    # f decide le cifre significative
    with open(file, 'a') as output_elab:
        output_elab.write(f"Test residui {titolo}_____________________________________________\n")
        output_elab.write(f"{'':<3}{'x':<{n}}{'y':<{n}}{'y*':<{n}}{'Residuo':<{n}}\n")
        for i,(x,y) in enumerate(zip(vx,vy)):
            y_star = modello(par,x)
            res = abs(y-y_star)
            somma += res
            output_elab.write(f"{i+1:<3}{x:<{n}.{f}f}{y:<{n}.{f}f}{y_star:<{n}.{f}f}{res:<{n}.{f}f}\n")
        output_elab.write(f"\nSomma residui = {somma:.{f}f}\n")


# Test del Chi Quadro
def chi_quadro(vx,vy,vsy,par,modello,file,titolo,n=8,f=2):
    somma = 0.
    # n decide la spaziatura tra i valori
    # f decide le cifre significative
    if np.isscalar(vsy):
        vsy = np.full_like(vy, fill_value=vsy, dtype=float)

    with open(file, 'a') as output_elab:
        output_elab.write(f"Test Chi Quadro {titolo}_____________________________________________\n")
        output_elab.write(f"{'':<3}{'x':<{n}}{'y':<{n}}{'y*':<{n}}{'sy':<{n}}{'Chi':<{n}}\n")
        for i,(x,y,sy) in enumerate(zip(vx,vy,vsy)):
            y_star = modello(par,x)
            chi = ((y-y_star)/sy)**2
            somma += chi
            output_elab.write(f"{i+1:<3}{x:<{n}.{f}f}{y:<{n}.{f}f}{y_star:<{n}.{f}f}{sy:<{n}.{f}f}{chi:<{n}.{f}f}\n")
        output_elab.write(f"Chi Quadro = {somma:.{f}f}\n")
        if np.isscalar(par):
                gradi = len(vy) - 1
        else:
            gradi = len(vy) - len(par)
        output_elab.write(f"Gradi Libertà = {gradi}\n")
        output_elab.write(f"Chi Quadro Ridotto = {somma/gradi:.{f}f}\n\n")


# Test Compatibilità con Chi Quadro
def chi_quadro_compatibilita(vy, vsy, file, titolo, n=12, f=2):
    # n decide la spaziatura tra i valori
    # f decide le cifre significative
    vy = np.array(vy, dtype=float)
    if np.isscalar(vsy):
        vsy = np.full_like(vy, fill_value=vsy, dtype=float)
    else:
        vsy = np.array(vsy, dtype=float)
    media_pesata = media_p(vy,vsy)[0]
    chi2 = 0.0

    with open(file, 'a') as output_elab:
        output_elab.write(f"Test Chi Quadro Compatibilità {titolo}____________________________________________\n")
        output_elab.write(f"{'':<3}{'y':<{n}}{'sy':<{n}}{'chi':<{n}}\n")

        for i, (y, sy) in enumerate(zip(vy, vsy)):
            contrib = ((y - media_pesata) / sy) ** 2
            chi2 += contrib
            output_elab.write(
                f"{i+1:<3}{y:<{n}.{f}f}{sy:<{n}.{f}f}{contrib:<{n}.{f}f}\n"
            )

        output_elab.write(f"Media pesata = {media_pesata:.{f}f}\n")
        output_elab.write(f"Chi quadro = {chi2:.{f}f}\n")
        gradi = len(vy) - 1
        output_elab.write(f"Gradi Libertà = {gradi}\n")
        output_elab.write(f"Chi Quadro Ridotto = {chi2/gradi:.{f}f}\n\n")


############################################################################################
### Regressioni
############################################################################################


# Minimi Quadrati Analitici con Incertezze Uniformi o Variabili sulle Ordinate
def minimi_quadrati(x, y, sy):
    x = np.array(x)
    y = np.array(y)

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
def fit(xdata, ydata, modello, beta0, chi=True):
    x, sx = xdata
    y, sy = ydata

    def chi2(par, x, y, sy):
        return np.sum(((y - modello(par,x)) / sy) ** 2)

    if chi:
        res = minimize(chi2, beta0, args=(x, y, sy))
        anal_chi = [
            [res.x[i], np.sqrt(abs(res.hess_inv[i][i]))]
            for i in range(len(res.x))
        ]
        return anal_chi

    model = odr.Model(modello)
    data_odr = odr.RealData(x, y, sx=sx, sy=sy)
    odr_instance = odr.ODR(data_odr, model, beta0=beta0)
    res = odr_instance.run()

    anal_odr = [
        [res.beta[i], res.sd_beta[i]]
        for i in range(len(res.beta))
    ]
    return anal_odr


############################################################################################
### Altre Funzioni
############################################################################################


# Funzione Percentuale
def percento(x, perc, stringa):
    if stringa == "+": return x * (1 + perc/100)
    if stringa == "-": return x * (1 - perc/100)


# Funzione per la Creazione di un File di Output Vuoto
def inizializza_output (output_filename, latex=False):
    with open(output_filename, "w") as file:
        file.write('')
    if latex == True:
        latex_filename = output_filename.replace('.txt', '.tex')
        with open(latex_filename, 'w') as latex_file:
            latex_file.write('')


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