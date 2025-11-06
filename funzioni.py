import math
import numpy as np
import sympy as sp
from scipy.stats import chi2, t, pearsonr
from scipy.optimize import curve_fit

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
def pearson(vx, vy):
    matrix = np.cov(vx,vy,ddof=1)
    dev_x = np.sqrt(matrix[0,0])
    dev_y = np.sqrt(matrix[1,1])
    cov_xy = matrix[0,1]
    p = cov_xy / (dev_x * dev_y)
    if np.abs(p) > 1:
        raise ValueError(f"Pearson Impossibile ({p})")
    return p

# Funzione incertezza indice Pearson
def s_pearson(vx, p):
    return np.sqrt((1 - p**2) / (len(vx) - 2))

# Funzione per il test di linearità con Pearson
def test_linearita(vx, vy, significanza=0.05, con = 0, code=1):
    p, skip = pearsonr(vx, vy)
    if len(vx) < 3:
        raise ValueError(f"len(vx) = {len(vx)}")
    if (1 - p**2) / (len(vx) - 2) < 0:
        raise ValueError(f"Radice di Negativo, Pearson = {p}")
    s_p = s_pearson(vx, p)
    NDOF = len(vx) - 2
    p_atteso = float(con)
    t_value = abs((p - p_atteso) / s_p)
    p_value = code * t.sf(t_value, NDOF)
    compatibile = p_value > significanza
    return compatibile, p_value, p, s_p

# Funzione errore a posteriori
def errpost(vx, vy, a, b):
    return np.sqrt(sum((y - (a + b * x)) ** 2 for x, y in zip(vx, vy)) / (len(vx) - 2))

from scipy.odr import ODR, Model, RealData

# Funzione elaborato
def elaborato(vx, vy, vsy, output_filename, n, vsx = None, elaborato = True, ritorno = False, latex = False):

    analitico = False
    print("\nElaborazione serie " + str(n+1))
    if vsx is None:
        analitico = True
        print("\tIncertezze x nulle")
        vsx = [0] * len(vx)
    elif isinstance(vsx, float):
        print("\tIncertezze x uniformi")
        vsx = [vsx] * len(vx)
    elif vsx[0] == vsx[1]:
        print("\tIncertezze x uniformi")
    else:
        print("\tIncertezze x variabili")

    if isinstance(vsy, float):
        lq = 1
        print("\tIncertezze y uniformi")
        vsy = [vsy] * len(vx)
    elif vsy[0] == vsy[1]:
        lq = 1
        print("\tIncertezze y uniformi")
    else:
        lq = 2
        print("\tIncertezze y variabili")

    vx = np.array(vx, dtype=float)
    vy = np.array(vy, dtype=float)
    vsy = np.array(vsy, dtype=float)
    vsx = np.array(vsx, dtype=float)

    if analitico == True:
        def modello (x,a,b):
            return a + b * x
        
        par, mcov = curve_fit(modello, vx, vy, sigma=vsy, absolute_sigma=True)
        a, b = par
        sa, sb = np.sqrt(np.diag(mcov))  # deviazioni standard
        cov = mcov[0, 1]

        print(f"\tMinimi quadrati {lq}")

    else:
        def modello (B, x):
            return B[0] + B[1] * x

        dati = RealData(vx, vy, sx=vsx, sy=vsy)
        modello_odr = Model(modello)
        odr = ODR(dati, modello_odr, beta0=[0.0, 1.0])
        output = odr.run()
        
        a, b = output.beta
        sa, sb = output.sd_beta
        cov = output.cov_beta[0, 1]

        print("\tMinimi quadrati 3")

    x_media = media(vx)
    y_media = media(vy)

    errpost_fit = errpost(vx, vy, a, b)

    # Medie pesate per eventuale compatibilità
    y_media_p = media_p(vy, vsy)
    sy_media_p = s_media_p(vy, vsy)

    cov_xy = sum((vx[i] - x_media) * (vy[i] - y_media) for i in range(len(vx))) / (len(vx) - 1)
    pearson_xy = pearson(vx, vy)
    s_pearson_xy = s_pearson(vx, pearson_xy)

    NDOF = len(vx) - 2

    if latex and not elaborato:
        raise ValueError("latex=True richiede che elaborato=True")

    if elaborato == True:
        with open(output_filename, 'a') as output_elab:
            output_elab.write('*' * 100 + '\n')
            output_elab.write(f"SERIE {n+1}\n")
            output_elab.write('*' * 100 + '\n\n')

            output_elab.write("Test ipotesi linearità_____________________________________\n")
            output_elab.write(f"Covarianza = {cov_xy:.5f}\n")
            output_elab.write(f"Indice Pearson = {pearson_xy:.5f} +/- {s_pearson_xy:.5f}\n")
            output_elab.write(f"Gradi di Liberta' = {NDOF}\n")
            output_elab.write(f"\tt = {abs((pearson_xy) / s_pearson_xy)}\n") # Variabile t per il test di Pearson
            output_elab.write(f"\tp-value (due code) = {2 * t.sf(abs((pearson_xy) / s_pearson_xy ), NDOF)}\n") # p-value per il test di Pearson
            output_elab.write('\n')
        
            output_elab.write("Parametri___________________________________________________\n")
            output_elab.write("y = a + bx\n")
            output_elab.write(f"a = {a:.5f} +/- {sa:.5f}\n")
            output_elab.write(f"b = {b:.5f} +/- {sb:.5f}\n\n")

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

            output_elab.write("Test ipotesi funzione costante_______________________________\n")
            output_elab.write(f"Gradi di Liberta' = {NDOF}\n")
            output_elab.write(f"t = {abs(b /sb)}\n") # Variabile t per test funzione costante
            output_elab.write(f"p-value = {2 * t.sf(abs(b/sb), NDOF)}\n\n") # p-value test funzione costante

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


    # Apertura del file LaTeX
    if latex == True:
        latex_filename = output_filename.replace('.txt', '.tex')
        with open(latex_filename, 'a') as latex_file:

            latex_file.write(r"\section*{Analisi Serie " + str(n+1) + "}" + '\n\n')

            latex_file.write(r"\b" + r"egin{table}[h]" + '\n' + '\n')
            latex_file.write('\t' +r"\centering" + '\n' + '\n')
            latex_file.write('\t' +r"\b" + r"egin{tabular}{{|c|c|}}" + '\n')
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
            latex_file.write('\t' + '\t'+ f"p-value & {form(t.fs(abs(b/sb), NDOF))}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' + r"\hline" + '\n')
            latex_file.write('\t' + r"\end{tabular}" + '\n')
            latex_file.write('\n')
            latex_file.write(r"\caption{}" + '\n')
            latex_file.write(r"\label{tab:my_label}" + '\n')
            latex_file.write(r"\end{table}" + '\n' + '\n' + '\n')

    if ritorno == True:
        return a, b, sa, sb, cov, p_value_fit, errpost_fit

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
        return risultato, stringa
    else: return stringa