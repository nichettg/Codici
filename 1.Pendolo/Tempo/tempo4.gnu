set terminal pngcairo enhanced size 1000,800 font "Arial,17"
set output "tempo4.png"

set title "Andamento temporale del periodo di oscillazione di un pendolo semplice\n con misurazione in serie" font "Arial,19"
set grid lc rgb "gray" lw 1
set ylabel "Periodo (s)"
set xlabel "Tempo (s)"

set xtics 20
set ytics 0.1

set arrow from 0,2.07653 to 220,2.07653 lc rgb "red" lw 2 nohead
set arrow from 0, (2.07653 - 2*0.0371332) to 220, (2.07653 - 2*0.0371332) lc rgb "pink" lw 1 nohead
set arrow from 0, (2.07653 + 2*0.0371332) to 220, (2.07653 + 2*0.0371332) lc rgb "pink" lw 1 nohead



plot "plot4.txt" using 1:2:3 with yerrorbars lc rgb "blue" notitle