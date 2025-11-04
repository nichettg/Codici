set terminal pngcairo enhanced size 2000,800 font "Arial,27"
set output "gauss.png"

set title "Confronto dei fit gaussiani"
set xlabel "Periodo (s)"
set ylabel "Frequenza assoluta"

set grid lc rgb "gray" lw 2

set xrange [1.5:2.5]
set xtics 0.1
set yrange [0:45]

# Dati 1
f1(x) = a1 / (sqrt(2. * pi) * c1) * exp(-((x - b1)**2.) / (2. * c1**2.))
a1= 6.104
b1= 2.04404
c1= 0.0971551
fit f1(x) "plot1.txt" using 1:2 via a1, b1, c1

# Dati 3
f3(x) = a3 / (sqrt(2. * pi) * c3) * exp(-((x - b3)**2.) / (2. * c3**2.))
a3= 6.5
b3= 1.99
c3= 0.131418
fit f3(x) "plot3.txt" using 1:2 via a3, b3, c3

# Dati 4
f4(x) = a4 / (sqrt(2. * pi) * c4) * exp(-((x - b4)**2.) / (2. * c4**2.))
a4= 2.323
b4= 2.07653
c4= 0.0371332
fit f4(x) "plot4.txt" using 1:2 via a4, b4, c4

# Plot
plot \
    "plot1.txt" using 1:2 with steps dt 3 lw 1 lc rgb "blue" notitle,\
    f1(x) lc rgb "blue" dt 3 lw 2 title "Misurazione in serie", \
    "plot3.txt" using 1:2 with steps dt 3 lw 1 lc rgb "red" notitle,\
    f3(x) lc rgb "red" dt 4 lw 2 title "Misurazione start and stop", \
    "plot4.txt" using 1:2 with steps dt 3 lw 1 lc rgb "orange" notitle,\
    f4(x) lc rgb "orange" lw 2 title "Misurazione di quattro oscillazioni "