#eta_intervalli.txt
set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

set grid lc rgb "gray" lw 2
set ylabel "Viscosità (N * (s/m^2))"
set xlabel "Spazio (m)"
set ytics 0.1
set key left top

set output "eta_intervalli.png"
set arrow from 0, 1.42193 to 100, 1.42193 nohead lt 2 lw 2 lc rgb "blue"
set arrow from 0, 1.42193 + 0.163141 to 100, 1.42193 + 0.163141 nohead lt 3 lw 2 lc rgb "violet"
set arrow from 0, 1.42193 - 0.163141 to 100, 1.42193 - 0.163141 nohead lt 3 lw 2 lc rgb "violet"

plot "eta_intervalli.txt" index 0 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "red" title ("1.5mm"), \
    "eta_intervalli.txt" index 1 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "purple" title ("2.0mm"), \
    "eta_intervalli.txt" index 2 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "blue" title ("3.18mm"), \
    "eta_intervalli.txt" index 3 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "pink" title ("4.76mm"), \
    "eta_intervalli.txt" index 4 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "violet" title ("6.35mm")