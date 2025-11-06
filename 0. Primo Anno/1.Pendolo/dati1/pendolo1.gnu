set terminal pngcairo enhanced size 2000,800 font "Arial,27"
set output "pendolo1.png"

set title "Analisi periodo di oscillazione di un pendolo semplice \n\ con misurazione in serie"
set xlabel "Periodo (s)"
set ylabel "Frequenza assoluta"

set grid lc rgb "gray" lw 2

set xrange [1.5:2.5]
set xtics 0.1
set yrange [0:45]

f1(x) = a / (sqrt(2. * pi) * c) * exp(-((x - b)**2.) / (2. * c**2.))
a= 6.104
b= 2.04404
c= 0.0971551

set arrow from 2.04739 - 0.0801211,0 to 2.04739 - 0.0801211,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 2.04739 + 0.0801211,0 to 2.04739 + 0.0801211,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 2.04739 - 2*0.0801211,0 to 2.04739 - 2*0.0801211,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 2.04739 + 2*0.0801211,0 to 2.04739 + 2*0.0801211,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 2.04739 - 3*0.0801211,0 to 2.04739 - 3*0.0801211,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 2.04739 + 3*0.0801211,0 to 2.04739 + 3*0.0801211,45 dt 2 lw 1 lc rgb "orange" nohead

fit f1(x) "plot1.txt" via a,b,c

plot "plot1.txt" using 1:2 with steps lw 1 lc rgb "blue" title "Dati",\
    f1(x) lc rgb "red" dt 4 lw 2 title "Fit gaussiano"