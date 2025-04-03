set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

set output "g_confronto.png"
set grid lc rgb "gray" lw 3
set ylabel "g (m/s^2)"
set xlabel "Serie"
set xtics 1
set ytics 0.1
set format y "%.1f"
set xrange [0:5]

plot "g_costanti.txt" using 1:2:3 with yerrorbars lw 2 lc rgb "red" title "Dati con errori"