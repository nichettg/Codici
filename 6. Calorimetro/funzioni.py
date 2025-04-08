import math
from scipy.stats import chi2, t
from scipy.optimize import curve_fit
import numpy as np

# La prossima volta da usare scipy invece dei minimi quadrati analitici

# Funzione media
def media(v):
    return sum(v) / len(v)

# Funzione media pesate
def media_p(v, w):
    sum1 = sum(v[i] * w[i] for i in range(len(v)))
    sum2 = sum(w)
    return sum1 / sum2

# Funzione incertezza media pesata
def s_media_p(v, w):
    sum1 = sum(w[i] for i in range(len(v)))
    sum2 = sum(w[i] ** 2 for i in range(len(v)))
    return math.sqrt(sum1 / (sum1 ** 2 - sum2))
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
    x_m = media(vx)
    y_m = media(vy)
    dev_x = dev(vx)
    dev_y = dev(vy)
    cov = sum((vx[i] - x_m) * (vy[i] - y_m) for i in range(len(vx))) / (len(vx) - 1)
    return cov / (dev_x * dev_y)

# Funzione incertezza indice Pearson
def s_pearson(vx, p):
    return math.sqrt((1 - p**2) / (len(vx) - 2))

# Minimi quadrati 1
def delta1(vx):
    sum1 = sum(x ** 2 for x in vx)
    sum2 = sum(vx)
    return len(vx) * sum1 - sum2 ** 2
def a1(vx, vy, delta):
    sum1 = sum(x ** 2 for x in vx)
    sum2 = sum(vy)
    sum3 = sum(vx)
    sum4 = sum(vx[i] * vy[i] for i in range(len(vx)))
    return (sum1 * sum2 - sum3 * sum4) / delta
def b1(vx, vy, delta):
    sum1 = sum(vx[i] * vy[i] for i in range(len(vx)))
    sum2 = sum(vx)
    sum3 = sum(vy)
    return (len(vx) * sum1 - sum2 * sum3) / delta
def sa1(vx, sy, delta):
    sum1 = sum(x ** 2 for x in vx)
    return (math.sqrt(sum1 / delta)) * sy
def sb1(vx, sy, delta):
    return (math.sqrt(len(vx) / delta)) * sy

# Minimi quadrati 2
def delta2(vx, vsy):
    sum1 = sum(1 / (sy ** 2) for sy in vsy)
    sum2 = sum((x ** 2) / (sy ** 2) for x, sy in zip(vx, vsy))
    sum3 = sum(x / (sy ** 2) for x, sy in zip(vx, vsy))
    return sum1 * sum2 - sum3 ** 2
def a2(vx, vy, vsy, delta):
    sum1 = sum((x ** 2) / (sy ** 2) for x, sy in zip(vx, vsy))
    sum2 = sum(y / (sy ** 2) for y, sy in zip(vy, vsy))
    sum3 = sum(x / (sy ** 2) for x, sy in zip(vx, vsy))
    sum4 = sum((x * y) / (sy ** 2) for x, y, sy in zip(vx, vy, vsy))
    return (sum1 * sum2 - sum3 * sum4) / delta
def b2(vx, vy, vsy, delta):
    sum1 = sum(1 / (sy ** 2) for sy in vsy)
    sum2 = sum((x * y) / (sy ** 2) for x, y, sy in zip(vx, vy, vsy))
    sum3 = sum(x / (sy ** 2) for x, sy in zip(vx, vsy))
    sum4 = sum(y / (sy ** 2) for y, sy in zip(vy, vsy))
    return (sum1 * sum2 - sum3 * sum4) / delta
def sa2(vx, vsy, delta):
    sum1 = sum((x ** 2) / (sy ** 2) for x, sy in zip(vx, vsy))
    return math.sqrt(sum1 / delta)
def sb2(vx, vsy, delta):
    sum1 = sum(1 / (sy ** 2) for sy in vsy)
    return math.sqrt(sum1 / delta)

# Funzione errore a posteriori
def errpost(vx, vy, a, b):
    return math.sqrt(sum((y - (a + b * x)) ** 2 for x, y in zip(vx, vy)) / (len(vx) - 2))

# Funzioni chi quadro
def chi_quadro1(vx, vy, sy, a, b):
    return sum(((y - (a + b * x)) / sy) ** 2 for x, y in zip(vx, vy))
def chi_quadro2(vx, vy, vsy, a, b):
    return sum(((y - (a + b * x)) / sy) ** 2 for x, y, sy in zip(vx, vy, vsy))

# Funzione elaborato
def elaborato(vx, vy, vsy, output_filename, n, elaborato = True, ritorno = False, latex = False, analitico = False):

    if isinstance(vsy, float):
        print(f"Minimi quadrati I")
        vsy = [vsy] * len(vx)
    elif isinstance(vsy, list):
        print(f"Minimi quadrati II")

    if analitico == False:
        par, cov = curve_fit(lambda x, a, b: a + b * x, vx, vy, sigma=vsy, absolute_sigma = True)
        a, b = par
        sa, sb = np.sqrt (np.diag(cov))
        print (f"Processo al calcolatore\n")

    if analitico == True:
        delta = delta2(vx, vsy)
        a = a2(vx, vy, vsy, delta)
        sa = sa2(vx, vsy, delta)
        b = b2(vx, vy, vsy, delta)
        sb = sb2(vx, vsy, delta)
        print (f"Processo analitico\n")

    x_media = media(vx)
    y_media = media(vy)

    y_media_p = media_p(vy, vsy)
    sy_media_p = s_media_p(vy, vsy)

    dev_x = dev(vx)
    dev_y = dev(vy)
    cov_xy = sum((vx[i] - x_media) * (vy[i] - y_media) for i in range(len(vx))) / (len(vx) - 1)
    pearson_xy = pearson(vx, vy)
    s_pearson_xy = s_pearson(vx, pearson_xy)

    NDOF = len(vx) - 2

    if elaborato == True:
        with open(output_filename, 'a') as output_elab:
            output_elab.write('*' * 100 + '\n')
            output_elab.write(f"SERIE {n+1}\n")
            output_elab.write('*' * 100 + '\n\n')

            output_elab.write("Verifica ipotesi linearità_________________________________\n")
            output_elab.write(f"Covarianza = {cov_xy:.5f}\n")
            output_elab.write(f"Indice Pearson = {pearson_xy:.5f} +/- {s_pearson_xy:.5f}\n")
            output_elab.write(f"Gradi di Liberta' = {NDOF}\n")
            output_elab.write(f"\tt = {abs((pearson_xy - 1) / s_pearson_xy)}\n")
            p_value_pearson_xy_1 = 2 * t.sf(abs((pearson_xy - 1) / s_pearson_xy ), NDOF)
            output_elab.write(f"\tp-value = {p_value_pearson_xy_1}\n")
            #output_elab.write("___Correlazione Assente (pearson=0)____\n")
            #output_elab.write(f"\tt = {abs(pearson_xy / s_pearson_xy)}\n")
            #p_value_pearson_xy_0 = 2 * t.sf(abs(pearson_xy / s_pearson_xy ), NDOF)
            #output_elab.write(f"\tp-value (2 tails)= {p_value_pearson_xy_0}\n")
            output_elab.write('\n')
        
            output_elab.write("Parametri___________________________________________________\n")
            output_elab.write("y = a + bx\n")
            output_elab.write(f"a = {a:.5f} +/- {sa:.5f}\n")
            output_elab.write(f"b = {b:.5f} +/- {sb:.5f}\n\n")

            # Chi-Quadro
            output_elab.write("Test Chi Quadro_____________________________________________\n")
            output_elab.write(f"{'x':<10}{'y':<10}{'sy':<13}{'y*':<14}{'Chi-quadro':<13}\n")
            sum1 = 0.
            for i in range(len(vx)):
                y = vy[i]
                y_star = a + b * vx[i]
                sy = vsy[i]
                chi_quadro_i = ((y - y_star) / sy) ** 2
                sum1 += chi_quadro_i
                output_elab.write(f"{vx[i]:<10.5f}{y:<10.5f}{sy:<13.5f}{y_star:<14.5f}{chi_quadro_i:<13.5f}\n")
            chi_quadro = sum1
            output_elab.write(f"\nGradi di liberta = {NDOF}\n")
            output_elab.write(f"Chi-quadro = {chi_quadro}\n")
            p_value = chi2.sf(chi_quadro, NDOF)
            output_elab.write(f"p-value = {p_value}\n\n")

            """# Errore a Posteriori
            output_elab.write("Test Errore a Posteriori____________________________________\n")
            sum2 = sum((vy[i] - (a + b * vx[i])) ** 2 for i in range(len(vx)))
            err = math.sqrt(sum2 / (len(vx) - 2))
            output_elab.write(f"{'Deviazione Residua':<20}{'':<5}{'Incertezza Ordinate':<30}\n")
            magg = 0
            min = 0
            for c in vsy:
                output_elab.write(f"{err:<20.6f}")
                if err > c:
                    output_elab.write(f"{'>':<5}")
                    magg += 1
                elif err < c:
                    output_elab.write(f"{'<':<5}")
                    min += 1
                output_elab.write(f"{c:<20.6f}\n")
            output_elab.write(f"\nDeviazioni Residue maggiori delle Incertezze: {magg}\n")
            output_elab.write(f"Deviazioni Residue minori delle Incertezze: {min}\n\n")"""

            """# Test Student
            output_elab.write("Test Student Intercetta-Origine____________________________\n")
            output_elab.write(f"Gradi di Liberta' = {NDOF}\n")
            output_elab.write(f"t = {abs(a /sa)}\n")
            p_value_t_1tail = t.sf(abs(a/sa), NDOF)
            p_value_t_2tails = 2 * p_value_t_1tail
            output_elab.write(f"p-value (1 tail)= {p_value_t_1tail}\n")
            output_elab.write(f"p-value (2 tails)= {p_value_t_2tails}\n\n")"""

            output_elab.write("Verifica ipotesi funzione costante_________________________\n")
            output_elab.write(f"Gradi di Liberta' = {NDOF}\n")
            output_elab.write(f"t = {abs(b /sb)}\n\n")
            p_value_t_1tail = t.sf(abs(b/sb), NDOF)
            p_value_t_2tails = 2 * p_value_t_1tail
            #output_elab.write(f"p-value (1 tail)= {p_value_t_1tail}\n")
            output_elab.write(f"p-value = {p_value_t_2tails}\n\n")
            output_elab.write(f"{'x':<10}{'y':<10}{'sy':<13}{'y_media_p':<14}{'Chi-quadro':<13}\n")
            sum1 = 0.
            for i in range(len(vx)):
                y = vy[i]
                sy = vsy[i]
                chi_quadro_i = ((y - y_media_p) / sy) ** 2
                sum1 += chi_quadro_i
                output_elab.write(f"{vx[i]:<10.5f}{y:<10.5f}{sy:<13.5f}{y_media_p:<14.5f}{chi_quadro_i:<13.5f}\n")
            chi_quadro = sum1
            output_elab.write(f"\nGradi di liberta = {NDOF}\n")
            output_elab.write(f"Chi-quadro = {chi_quadro}\n")
            p_value = chi2.sf(chi_quadro, NDOF)
            output_elab.write(f"p-value = {p_value}\n\n")


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
            latex_file.write('\t' + '\t' +r"\multicolumn{2}{|c|}{\textbf{Verifica ipotesi linearità}} \\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +f"Gradi di libertà & {NDOF}" + r"\\" + '\n')    
            latex_file.write('\t' + '\t' +f"Valore t & {form(abs((pearson_xy-1)/s_pearson_xy))}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +f"p-value (2 tails) & {form(p_value_pearson_xy_1)}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +r"\multicolumn{2}{|c|}{\textbf{Verifica della bontà del fit}} \\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +f"Gradi di libertà & {NDOF}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +f"Chi-quadro & {form(chi_quadro)}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +f"p-value & {form(p_value)}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' +r"\multicolumn{2}{|c|}{\textbf{Verifica ipotesi funzione costante}} \\" + '\n')
            latex_file.write('\t' + '\t' +r"\hline" + '\n')
            latex_file.write('\t' + '\t' + f"Gradi di libertà & {NDOF}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' + f"Valore t & {form(abs(b/sb))}" + r"\\" + '\n')
            latex_file.write('\t' + '\t'+ f"p-value & {form(p_value_t_2tails)}" + r"\\" + '\n')
            latex_file.write('\t' + '\t' + r"\hline" + '\n')
            latex_file.write('\t' + r"\end{tabular}" + '\n')
            latex_file.write('\n')
            latex_file.write(r"\caption{}" + '\n')
            latex_file.write(r"\label{tab:my_label}" + '\n')
            latex_file.write(r"\end{table}" + '\n' + '\n' + '\n')

    if ritorno == True:
        return a, b, sa, sb

def output_init (output_filename, latex=False):
    with open(output_filename, "w") as file:
        file.write('')
    if latex == True:
        latex_filename = output_filename.replace('.txt', '.tex')
        with open(latex_filename, 'w') as latex_file:
            latex_file.write('')

def form(float):
    if float == 0.0:
        return 0.0
    elif float < 1e-5 or float > 1e5:
        return f"{float:.2e}"
    else:
        return f"{float:.5f}"