set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

set output "t_confronto.png"
set grid lc rgb "gray" lw 3
set ylabel "t (s)"
set xlabel "Serie"
set xtics 1
set xrange [0:7]

plot "t_confronto.txt" using 1:2:3 with yerrorbars lw 2 lc rgb "red" title "Dati con errori"