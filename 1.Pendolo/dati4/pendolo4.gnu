set terminal pngcairo enhanced size 2000,800 font "Arial,27"
set output "pendolo4.png"

set title "Analisi periodo di oscillazione di un pendolo semplice \n\ con misurazione di quattro oscillazioni"
set xlabel "Periodo (s)"
set ylabel "Frequenza assoluta"

set grid lc rgb "gray" lw 2

set xrange [1.5:2.5]
set xtics 0.1
set yrange [0:45]

f4(x) = a / (sqrt(2. * pi) * c) * exp(-((x - b)**2.) / (2. * c**2.))
a= 2.323
b= 2.07653
c= 0.0371332

set arrow from 2.08167 - 0.0152888,0 to 2.08167 - 0.0152888,45 dt 3 lw 2 lc rgb "orange" nohead
set arrow from 2.08167 + 0.0152888,0 to 2.08167 + 0.0152888,45 dt 3 lw 2 lc rgb "orange" nohead
set arrow from 2.08167 - 2*0.0152888,0 to 2.08167 - 2*0.0152888,45 dt 3 lw 2 lc rgb "orange" nohead
set arrow from 2.08167 + 2*0.0152888,0 to 2.08167 + 2*0.0152888,45 dt 3 lw 2 lc rgb "orange" nohead
set arrow from 2.08167 - 3*0.0152888,0 to 2.08167 - 3*0.0152888,45 dt 3 lw 2 lc rgb "orange" nohead
set arrow from 2.08167 + 3*0.0152888,0 to 2.08167 + 3*0.0152888,45 dt 3 lw 2 lc rgb "orange" nohead

fit f4(x) "plot4.txt" via a,b,c

plot "plot4.txt" using 1:2 with steps lw 1 lc rgb "blue" title "Dati",\
    f4(x) lc rgb "red" dt 4 lw 2 title "Fit gaussiano"