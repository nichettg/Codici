set terminal pngcairo enhanced size 1000,800 font "Arial,17"
set output 'plot_muoni.png'

#set terminal pdfcairo enhanced size 1000,800 font "Arial,17"
#set output 'plot_muoni.pdf'

set title "Frequenza apparizioni muoni\nin funzione dell'angolo del rilevatore" font ",19"
set xlabel "Angolo (°)" font ",17"
set ylabel "Frequenza media (min^{-1})" font ",17"

set xrange [-5:90]

set grid lc rgb "gray" lw 1
set border lw 2

set label "f_1(x) = A_1 cos^{B_1}\n   A_1 = 37.5 ± 2.0\n   B_1 = 1.7 ± 0.1\n\n\
f_2(x) = A_2 cos^{2}\n   A_2 = 39.6 ± 2.0"\
    at 0,13 boxed font ",16"
#A1= 37.4989 ± 1.913   B1= 1.69279 ± 0.1412   A2= 39.5525 ± 1.92

#funzioni
degrad(x) = x * pi / 180.0

f1(x) = A1 * cos(degrad(x)) ** B1
f2(x) = A2 * cos(degrad(x)) ** 2

A1 = 1; B1 = 2;
A2 = 1;

#fit
fit f1(x) 'processed_data.txt' using 1:2:3 via A1, B1
fit f2(x) 'processed_data.txt' using 1:2:3 via A2

plot "processed_data.txt" using 1:2:3 with yerrorbars lw 2 lc rgb "black" title "Valori", \
    f1(x) title "f_1(x)" lw 2 lc rgb "blue",\
    f2(x) title "f_2(x)" lw 2 lc rgb "red"