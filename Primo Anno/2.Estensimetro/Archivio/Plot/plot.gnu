set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

#allungamento
set output "grafico_allungamento.png"

set grid lc rgb "gray" lw 2
set xlabel "Forza (N)"
set ylabel "Allungamento (m)"
set format y "%.1e"
set key left top

f(x) = a + b*x
fit f(x) "allungamento_media.txt" using ($1*8.91e-3):($2*1e-6) via a,b

plot "allungamento_media.txt" using ($1*8.91e-3):($2*1e-6):($1*0+20*8.91e-3):($2*0+10*1e-6) with xyerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2ex + %.2e", b, a) lw 2 lc rgb "blue"

#accorciamento
set output "grafico_accorciamento.png"

set grid lc rgb "gray" lw 2
set xlabel "Forza (N)"
set ylabel "Allungamento (m)"
set format y "%.1e"
set key left top

f(x) = a + b*x
fit f(x) "accorciamento_media.txt" using ($1*8.91e-3):($2*1e-6) via a,b

plot "accorciamento_media.txt" using ($1*8.91e-3):($2*1e-6):($1*0+20*8.91e-3):($2*0+10*1e-6) with xyerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2ex + %.2e", b, a) lw 2 lc rgb "blue"

#unione
set output "grafico_unione.png"

set grid lc rgb "gray" lw 2
set xlabel "Forza (N)"
set ylabel "Allungamento (m)"
set format y "%.1e"
set key left top

f(x) = a + b*x
fit f(x) "unione_media.txt" using ($1*8.91e-3):($2*1e-6) via a,b

plot "unione_media.txt" using ($1*8.91e-3):($2*1e-6):($1*0+20*8.91e-3):($2*0+10*1e-6) with xyerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2ex + %.2e", b, a) lw 2 lc rgb "blue"