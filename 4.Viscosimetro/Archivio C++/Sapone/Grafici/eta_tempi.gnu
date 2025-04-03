#eta_tempi.txt
set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

set grid lc rgb "gray" lw 2
set ylabel "Viscosità (N * (s/m^2))"
set xlabel "Tempo"
set ytics 0.5
set xrange [-1:22]
set format x ""
#unset xtics
set key right top

set output "eta_tempi.png"

plot "eta_tempi.txt" index 0 using 3:6:7 with yerrorbars lw 2 lc rgb "red" title ("1.5mm"), \
    "eta_tempi.txt" index 1 using 3:6:7 with yerrorbars lw 2 lc rgb "purple" title ("2.0mm"), \
    "eta_tempi.txt" index 2 using 3:6:7 with yerrorbars lw 2 lc rgb "blue" title ("3.18mm"), \
    "eta_tempi.txt" index 3 using 3:6:7 with yerrorbars lw 2 lc rgb "pink" title ("4.76mm"), \
    "eta_tempi.txt" index 4 using 3:6:7 with yerrorbars lw 2 lc rgb "violet" title ("6.35mm")

#plot "eta_tempi.txt" using ($1 == 0.0015 ? $3 : 1/0):6:7 with xyerrorbars title "1.5mm", \
     "eta_tempi.txt" using ($1 == 0.002 ? $3 : 1/0):6:7 with xyerrorbars title "2.0mm", \
     "eta_tempi.txt" using ($1 == 0.00318 ? $3 : 1/0):6:7 with xyerrorbars title "3.18mm", \
     "eta_tempi.txt" using ($1 == 0.00476 ? $3 : 1/0):6:7 with xyerrorbars title "4.76mm", \
     "eta_tempi.txt" using ($1 == 0.00635 ? $3 : 1/0):6:7 with xyerrorbars title "6.35mm"
