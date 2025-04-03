set terminal pngcairo enhanced size 2000,800 font "Arial,27"
set output "pendolo3.png"

set title "Analisi periodo di oscillazione di un pendolo semplice \n\ con misurazione start e stop"
set xlabel "Periodo (s)"
set ylabel "Frequenza assoluta"

set grid lc rgb "gray" lw 2

set xrange [1.5:2.5]
set xtics 0.1
set yrange [0:45]

f3(x) = a / (sqrt(2. * pi) * c) * exp(-((x - b)**2.) / (2. * c**2.))
a= 6.5
b= 1.99
c= 0.131418

set arrow from 1.96557 - 0.126444,0 to 1.96557 - 0.126444,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 1.96557 + 0.126444,0 to 1.96557 + 0.126444,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 1.96557 - 2*0.126444,0 to 1.96557 - 2*0.126444,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 1.96557 + 2*0.126444,0 to 1.96557 + 2*0.126444,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 1.96557 - 3*0.126444,0 to 1.96557 - 3*0.126444,45 dt 2 lw 1 lc rgb "orange" nohead
set arrow from 1.96557 + 3*0.126444,0 to 1.96557 + 3*0.126444,45 dt 2 lw 1 lc rgb "orange" nohead

fit f3(x) "plot3.txt" via a,b,c

plot "plot3.txt" using 1:2 with steps lw 1 lc rgb "blue" title "Dati",\
    f3(x) lc rgb "red" dt 4 lw 2 title "Fit gaussiano"