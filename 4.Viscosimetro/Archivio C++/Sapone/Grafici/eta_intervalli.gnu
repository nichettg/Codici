#eta_intervalli.txt
set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

set grid lc rgb "gray" lw 2
set ylabel "Viscosità (N * (s/m^2))"
set xlabel "Spazio (m)"
set ytics 0.5
set key left top

x_start = 0
x_end = 0.3
m = 6.55889
dev = 1.28827

set output "eta_intervalli.png"
set arrow from x_start, m to x_end, m nohead lt 2 lw 2 lc rgb "blue"
set arrow from x_start, m + dev to x_end, m + dev nohead lt 3 lw 2 lc rgb "violet"
set arrow from x_start, m - dev to x_end, m - dev nohead lt 3 lw 2 lc rgb "violet"

plot "eta_intervalli.txt" index 0 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "red" title ("1.5mm"), \
    "eta_intervalli.txt" index 1 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "purple" title ("2.0mm"), \
    "eta_intervalli.txt" index 2 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "blue" title ("3.18mm"), \
    "eta_intervalli.txt" index 3 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "pink" title ("4.76mm"), \
    "eta_intervalli.txt" index 4 using 9:7:10:8 with xyerrorbars lw 2 lc rgb "violet" title ("6.35mm")