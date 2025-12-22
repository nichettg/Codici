import math
import numpy as np
import sympy as sp
from scipy.stats import chi2, t, pearsonr

# Funzione percentuale
def percento(x, perc, stringa):
    if stringa == "+": return x * (1 + perc/100)
    if stringa == "-": return x * (1 - perc/100)

# Funzione media
def media(v):
    return sum(v) / len(v)

# Funzione incertezza media
def s_media(v):
    v = np.array(v, dtype=float)
    return np.std(v, ddof=1) / np.sqrt(len(v))

# Funzione media pesata
def media_p(v, w):
    sum1 = sum(v[i] / (w[i]**2) for i in range(len(v)))
    sum2 = sum((1/w[i])**2 for i in range(len(v)))
    return sum1 / sum2

# Funzione incertezza media pesata
def s_media_p(v, w):
    sum1 = sum((1/w[i])**2 for i in range(len(v)))
    return math.sqrt(1/sum1)

# Funzione semidispersione massima
def semidisp(x):
    return (np.max(x) - np.min(x)) / 2

# Funzione deviazione standard
def dev(v):
    m = media(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))

# Funzione covarianza
def cov(vx, vy):
    x_m = media(vx)
    y_m = media(vy)
    return sum((vx[i] - x_m) * (vy[i] - y_m) for i in range(len(vx))) / (len(vx) - 1)

# Funzione indice Pearson
def pearson(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    if x.size != y.size:
        raise ValueError("x e y devono avere la stessa lunghezza")
    N = x.size
    if N < 3:
        raise ValueError("Servono almeno 3 punti per stimare l'incertezza")

    x_mean = np.mean(x)
    y_mean = np.mean(y)
    cov_xy = np.sum((x - x_mean) * (y - y_mean)) / (N - 1)
    sx = np.sqrt(np.sum((x - x_mean)**2) / (N - 1))
    sy = np.sqrt(np.sum((y - y_mean)**2) / (N - 1))

    r = cov_xy / (sx * sy)
    sigma_r = np.sqrt((1 - r**2) / (N - 2))

    return [r, sigma_r]

# Funzione per il test di linearità con Pearson
def test_linearita(vx, vy, significanza=0.05, con = 0, code=1):
    [p,s_p] = pearson(vx,vy)
    NDOF = len(vx) - 2
    p_atteso = float(con)
    t_value = abs((p - p_atteso) / s_p)
    p_value = code * t.sf(t_value, NDOF)
    compatibile = p_value > significanza
    return compatibile, p_value, p, s_p

# Funzione errore a posteriori
def errpost(vx, vy, a, b):
    return np.sqrt(sum((y - (a + b * x)) ** 2 for x, y in zip(vx, vy)) / (len(vx) - 2))

def residui(vx,vy,par,modello,file,titolo, nomi_par=None,n=8,f=2):
    somma = 0.
    # n decide la spaziatura tra i valori
    # f decide le cifre significative
    if nomi_par is None:
        nomi_par = [f"p{i}" for i in range(len(par))]
    with open(file, 'a') as output_elab:
        output_elab.write(f"Test residui {titolo}_____________________________________________\n")
        output_elab.write(f"{'':<3}{'x':<{n}}{'y':<{n}}{'y*':<{n}}{'Residuo':<{n}}\n")
        for i,(x,y) in enumerate(zip(vx,vy)):
            y_star = modello(x,par)
            res = abs(y-y_star)
            somma += res
            output_elab.write(f"{i+1:<3}{x:<{n}.{f}f}{y:<{n}.{f}f}{y_star:<{n}.{f}f}{res:<{n}.{f}f}\n")
        if np.isscalar(par):
            par = [par]
        output_elab.write("Parametri: ")
        output_elab.write(
            ", ".join(
                f"{nome} = {val:.{f}f}"
                for nome, val in zip(nomi_par, par)
            )
        )
        output_elab.write(f"\nSomma residui = {somma:.{f}f}\n")

def minimi_quadrati(x, y, sigma=None):
    x = np.array(x)
    y = np.array(y)

    if sigma is None:
        w = np.ones_like(y)
    else:
        sigma = np.array(sigma)
        w = 1 / sigma**2

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

from scipy.odr import ODR, Model, RealData

# Funzione elaborato
def elaborato(vx, vy, vsx, vsy, output_filename, n, elaborato=True, ritorno=True, test_costanza=False, test_compatibilita=False):

    if np.isscalar(vsx):
        vsx = np.full_like(vx, fill_value=vsx, dtype=float)
    if np.isscalar(vsy):
        vsx = np.full_like(vy, fill_value=vsy, dtype=float)

    vx = np.array(vx, dtype=float)
    vy = np.array(vy, dtype=float)
    vsy = np.array(vsy, dtype=float)
    vsx = np.array(vsx, dtype=float)

    # Elaborazione con ODR
    def modello (B, x):
        return B[0] + B[1] * x
    dati = RealData(vx, vy, sx=vsx, sy=vsy)
    modello_odr = Model(modello)
    odr = ODR(dati, modello_odr, beta0=[0.0, 1.0])
    output = odr.run()
    a, b = output.beta
    sa, sb = output.sd_beta
    cov_ab = output.cov_beta[0][1]

    x_media = np.mean(vx)
    y_media = np.mean(vy)

    errpost_fit = errpost(vx, vy, a, b)

    # Medie pesate per eventuale compatibilità
    y_media_p = media_p(vy, vsy)
    sy_media_p = s_media_p(vy, vsy)

    [[var_x, cov_xy], [cov_yx, var_y]]= matrice_covarianza(vx,vy)

    pearson_xy = pearson(vx, vy)
    s_pearson_xy = s_pearson(vx, pearson_xy)

    NDOF = len(vx) - 2

    if elaborato == True:
        with open(output_filename, 'a') as output_elab:
            output_elab.write('*' * 100 + '\n')
            output_elab.write(f"SERIE {n+1}\n")
            output_elab.write('*' * 100 + '\n\n')
        
            output_elab.write("Parametri___________________________________________________\n")
            output_elab.write("y = a + bx\n")
            output_elab.write(f"a = {a:.5f} +/- {sa:.5f}\n")
            output_elab.write(f"b = {b:.5f} +/- {sb:.5f}\n\n")

            output_elab.write("Matrice Covarianza__________________________________________\n")
            output_elab.write(f"Varianza x = {var_x}\n")
            output_elab.write(f"Varianza y = {var_y}\n")
            output_elab.write(f"Covarianza xy = {cov_xy}\n")
            output_elab.write(f"Covarianza yx = {cov_yx}\n\n")

            output_elab.write("Test ipotesi linearità______________________________________\n")
            output_elab.write(f"Indice Pearson = {formatta_errore(pearson_xy,s_pearson_xy,txt=True)}\n")
            output_elab.write(f"Gradi di Liberta' = {NDOF}\n")
            output_elab.write(f"\tt = {abs((pearson_xy) / s_pearson_xy)}\n") # Variabile t per il test di Pearson
            output_elab.write(f"\tp-value (due code) = {2 * t.sf(abs((pearson_xy) / s_pearson_xy ), NDOF)}\n") # p-value per il test di Pearson
            output_elab.write('\n')

            # Chi-Quadro
            output_elab.write("Test bontà fit _____________________________________________\n")
            output_elab.write(f"{'x':<10}{'y':<10}{'sy':<13}{'y*':<14}{'Chi-quadro':<13}\n")
            sum1 = 0.
            for i in range(len(vx)):
                y = vy[i]
                y_star = a + b * vx[i]
                sy = vsy[i]
                chi_quadro_i = ((y - y_star) / sy) ** 2
                sum1 += chi_quadro_i
                output_elab.write(f"{vx[i]:<10.5f}{y:<10.5f}{sy:<13.5f}{y_star:<14.5f}{chi_quadro_i:<13.5f}\n")
            chi_quadro_fit = sum1 # Chi-quadro bontà fit
            output_elab.write(f"\nGradi di liberta = {NDOF}\n")
            output_elab.write(f"Chi-quadro = {chi_quadro_fit}\n")
            p_value_fit = chi2.sf(chi_quadro_fit, NDOF) # p-value bontà fit
            output_elab.write(f"p-value = {p_value_fit}\n")
            output_elab.write(f"Errore a posteriori = {errpost_fit:.5f}\n\n")

            if test_costanza:
                output_elab.write("Test ipotesi funzione costante_______________________________\n")
                output_elab.write(f"Gradi di Liberta' = {NDOF}\n")
                output_elab.write(f"t = {abs(b /sb)}\n")
                output_elab.write(f"p-value = {2 * t.sf(abs(b/sb), NDOF)}\n\n")

            if test_compatibilita:
                output_elab.write("Test ipotesi compatibilità misure____________________________\n")
                output_elab.write(f"{'x':<10}{'y':<10}{'sy':<13}{'y_media_p':<14}{'Chi-quadro':<13}\n")
                sum1 = 0.
                for i in range(len(vx)):
                    y = vy[i]
                    sy = vsy[i]
                    chi_quadro_i = ((y - y_media_p) / sy) ** 2
                    sum1 += chi_quadro_i
                    output_elab.write(f"{vx[i]:<10.5f}{y:<10.5f}{sy:<13.5f}{y_media_p:<14.5f}{chi_quadro_i:<13.5f}\n")
                chi_quadro_comp = sum1
                output_elab.write(f"\nGradi di liberta = {NDOF}\n")
                output_elab.write(f"Chi-quadro = {chi_quadro_comp}\n") # Chi-quadro compatibilità misure
                output_elab.write(f"p-value = {chi2.sf(chi_quadro_comp, NDOF)}\n\n") # p-value compatibilità misure
                output_elab.write(f"Media pesata = {y_media_p} +/- {sy_media_p}\n\n")

    else:
        chi2_sum = 0.0
        for i in range(len(vx)):
            y_obs = vy[i]
            y_exp = a + b * vx[i]
            sigma_y = vsy[i]
            chi2_i = ((y_obs - y_exp) / sigma_y) ** 2
            chi2_sum += chi2_i

        chi_quadro_fit = chi2_sum  # Statistica chi-quadro per la bontà del fit
        p_value_fit = chi2.sf(chi_quadro_fit, NDOF)  # p-value corrispondente

    """
    # Apertura del file LaTeX
    if latex == True:
        latex_filename = output_filename.replace('.txt', '.tex')
        with open(latex_filename, 'a') as latex_file:

            latex_file.write(r"\section*{Analisi Serie " + str(n+1) + "}" + '\n\n')

            latex_file.write(r"\b" + r"egin{table}[h]" + '\n' + '\n')
            latex_file.write('\t' +r"\centering" + '\n' + '\n')
            latex_file.write('\t' +r"\b" + r"egin{tabular}{|c|c|}" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +r"\multicolumn{2}{|c|}{\textbf{Dati Interpolazione}} \\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +f"Equazione della retta & $y=({form(b)}\pm{form(sb)})x+({form(a)}\pm{form(sa)})$" + r"\\" + '\n')
            latex_file.write('\t' +'\t' +f"Indice Pearson & ${form(pearson_xy)}\pm{form(s_pearson_xy)}$" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +r"\multicolumn{2}{|c|}{\textbf{Verifica ipotesi linearità perfetta}} \\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +f"Gradi di libertà & {NDOF}" + r"\\" + '\n')    
            latex_file.write('\t' + '\t' +f"Valore t & {form(abs((pearson_xy)/s_pearson_xy))}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +f"p-value (due code) & {2 * t.sf(abs((pearson_xy)/s_pearson_xy), NDOF)}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +r"\multicolumn{2}{|c|}{\textbf{Verifica della bontà del fit}} \\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +f"Gradi di libertà & {NDOF}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +f"Chi-quadro & {form(chi_quadro_fit)}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +f"p-value & {form(p_value_fit)}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +r"\multicolumn{2}{|c|}{\textbf{Verifica ipotesi funzione costante}} \\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' + f"Gradi di libertà & {NDOF}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' + f"Valore t & {form(abs(b/sb))}" + r"\\" + '\n')
            latex_file.write('\t' + '\t'+ f"p-value & {form(2 * t.sf(abs(b/sb), NDOF))}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' + r"\hline" + '\n')
            latex_file.write('\t' + r"\end{tabular}" + '\n')
            latex_file.write('\n')
            latex_file.write(r"\caption{}" + '\n')
            latex_file.write(r"\label{tab:my_label}" + '\n')
            latex_file.write(r"\end{table}" + '\n' + '\n' + '\n')
    """

    if ritorno == True:
        return a, b, sa, sb, cov_ab

# Funzione per la creazione di un file di output vuoto
def inizializza_output (output_filename, latex=False):
    with open(output_filename, "w") as file:
        file.write('')
    if latex == True:
        latex_filename = output_filename.replace('.txt', '.tex')
        with open(latex_filename, 'w') as latex_file:
            latex_file.write('')

# Funzione per formattare i numeri
def form(float):
    if float == 0.0:
        return 0.0
    elif float < 1e-5 or float > 1e5:
        return f"{float:.2e}"
    else:
        return f"{float:.5f}"

# Funzione per calcolare l'incertezza di una misura singola con errore sistematico
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

def compatibilita(f1, sf1, f2, sf2):
    f1 = float(f1)
    sf1 = float(sf1)
    f2 = float(f2)
    sf2 = float(sf2)
    return abs(f1 - f2) / np.sqrt(sf1**2 + sf2**2)

def matrice_covarianza(a, b):
    a = np.array(a)
    b = np.array(b)

    da = a - a.mean()
    db = b - b.mean()

    # varianze e covarianza
    var_a = np.sum(da * da) / (len(a) - 1)
    var_b = np.sum(db * db) / (len(b) - 1)
    cov_ab = np.sum(da * db) / (len(a) - 1)

    return np.array([[var_a, cov_ab],
                     [cov_ab, var_b]])

def arrotonda_significative(x, cifre=2):
    if x == 0:
        return 0.0
    exp = int(np.floor(np.log10(abs(x))))
    fattore = 10**(cifre - 1 - exp)
    return round(x * fattore) / fattore

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

import numpy as np
from scipy.optimize import minimize
from scipy import odr

def fit(xdata, ydata, modello, beta0, chi=True):
    x, sx = xdata
    y, sy = ydata

    # --- chi quadro ---
    def chi2(par, x, y, sy):
        return np.sum(((y - modello(par, x)) / sy) ** 2)

    if chi:
        res = minimize(chi2, beta0, args=(x, y, sy))
        anal_chi = [
            [res.x[i], np.sqrt(abs(res.hess_inv[i][i]))]
            for i in range(len(res.x))
        ]
        return anal_chi

    # --- ODR ---
    model = odr.Model(modello)
    data_odr = odr.RealData(x, y, sx=sx, sy=sy)
    odr_instance = odr.ODR(data_odr, model, beta0=beta0)
    res = odr_instance.run()

    anal_odr = [
        [res.beta[i], res.sd_beta[i]]
        for i in range(len(res.beta))
    ]
    return anal_odr

