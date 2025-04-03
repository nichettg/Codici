set terminal pngcairo enhanced size 2500,1000 font "Arial,27"
set output "grafico_tempo.png"

set grid lc rgb "gray" lw 2
set xlabel "Serie"
set ylabel "1/k (m/N)"
set format y "%.2e"
set key left top

# Calcolo della media e deviazione standard dai dati
stats "dati_tempo.txt" using 2 nooutput
mean = STATS_mean
stddev = STATS_stddev

# Allarga il dominio per visualizzare meglio il primo e ultimo valore
set xrange [0.5:8.5]

# Aumenta la risoluzione dell'asse Y
set ytics nomirror
set mytics 5  # Aggiunge suddivisioni più fini tra le tacche principali

# Stili delle linee
set style line 1 lc rgb "blue" lw 3 # Media (spessa)
set style line 2 lc rgb "black" lw 2 dt 2 # Dev. Std. ±2 (tratteggio lungo)
set style line 3 lc rgb "black" lw 2 dt 4 # Dev. Std. ±1 (tratteggio corto)

plot "dati_tempo.txt" using ($1):($2):($3) with yerrorbars lw 2 lc rgb "red" title "Dati con errori", \
     mean with lines ls 1 title "Media", \
     mean + stddev with lines ls 3 title "Media +/- 1 Dev. Std.", \
     mean - stddev with lines ls 3 notitle, \
     mean + 2*stddev with lines ls 2 title "Media +/- 2 Dev. Std.", \
     mean - 2*stddev with lines ls 2 notitle