set terminal pngcairo enhanced size 1000,800 font "Arial,17"
set output 'plot_muoni.png'

set title "Frequenza apparizioni muoni\nin funzione dell'angolo del rilevatore" font ",19"
set xlabel "Angolo (°)" font ",17"
set ylabel "Frequenza media (min^{-1})" font ",17"

set xrange [-5:90]

set grid lc rgb "gray" lw 1
set border lw 2

#funzioni
degrad(x) = x * pi / 180.0

f1(x) = A1 * cos(B1 * degrad(x) + C1) ** 2 +D1
A1 = 10; B1 = 1; C1 = 0.0001; D1 = 0.0001

f2(x) = A2 * cos(B2 * degrad(x) + C2) ** 2 +D2
A2 = 10; B2 = 1; C2 = 0.0001; D2 = 0.0001

f3(x) = A3 * cos(B3 * degrad(x)) ** 2 +D3
A3 = 10; B3 = 1; D3 = 0.0001

f4(x) = A4 * cos(B4 * degrad(x)) ** 2
A4 = 10; B4 = 1;


#fit
fit f1(x) 'processed_data.txt' using 1:2 via A1, B1, C1, D1
fit f2(x) 'processed_data.txt' using 1:2:3 via A2, B2, C2, D2
fit f3(x) 'processed_data.txt' using 1:2:3 via A3, B3, D3
fit f4(x) 'processed_data.txt' using 1:2:3 via A4, B4

#f2 considera anche l'incertezza, f3 e f4 non considerano i parametri C e D poichè
#la percentuale dell'errore (fit log) era molto alta, superiore al 100%

plot "processed_data.txt" using 1:2:3 with yerrorbars lw 2 lc rgb "black" title "Valori", \
    f1(x) title "f(x) using 1:2" lw 2 lc rgb "green",\
    f2(x) title "f(x) using 1:2:3" lw 2 lc rgb "blue",\
    f3(x) title "f(x) using 1:2:3 without C" lw 2 lc rgb "red",\
    f4(x) title "f(x) using 1:2:3 without C and D" lw 2 lc rgb "pink"