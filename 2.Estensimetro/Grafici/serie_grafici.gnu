set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

#allungamento
set output "grafico_allungamento.png"

set grid lc rgb "gray" lw 2
set xlabel "Forza (N)"
set ylabel "Allungamento (m)"
set format y "%.1e"
set key left top

f(x) = a + b*x
fit f(x) "allungamento.txt" using ($1*9.81e-3):($2*1e-6) via a,b

plot "allungamento.txt" using ($1*9.81e-3):($2*1e-6):($2*0 + 10e-6) with yerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2e + %.2ex", a, b) lw 2 lc rgb "blue"

#accorciamento
set output "grafico_accorciamento.png"

set grid lc rgb "gray" lw 2
set xlabel "Forza (N)"
set ylabel "Allungamento (m)"
set format y "%.1e"
set key left top

f(x) = a + b*x
fit f(x) "accorciamento.txt" using ($1*9.81e-3):($2*1e-6) via a,b

plot "accorciamento.txt" using ($1*9.81e-3):($2*1e-6):($2*0 + 10e-6) with yerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2e + %.2ex", a, b) lw 2 lc rgb "blue"