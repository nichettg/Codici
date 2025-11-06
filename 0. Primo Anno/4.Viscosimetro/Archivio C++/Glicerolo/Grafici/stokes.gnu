#stokes.txt
set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

set grid lc rgb "gray" lw 2
set ylabel "Velocità (m/s)"
set xlabel "Diametro^2 (m^2)"
set key left top

set output "stokes.png"
plot "stokes.txt" index 0 using 7:3:8:4 with xyerrorbars lw 2 lc rgb "red" title ("Dati con errori")

set grid lc rgb "gray" lw 2
set ylabel "Viscosità (N * (s/m^2))"
set xlabel "Diametro (m)"
set key left top

set output "eta.png"
set arrow from 0.001, 1.45659 to 0.0065, 1.45659 nohead lt 2 lw 2 lc rgb "violet"
set arrow from 0.001, 1.45659 + 0.0201757 to 0.0065, 1.45659 + 0.0201757 nohead lt 3 lw 2 lc rgb "pink"
set arrow from 0.001, 1.45659 - 0.0201757 to 0.0065, 1.45659 - 0.0201757 nohead lt 3 lw 2 lc rgb "pink"
plot "stokes.txt" index 0 using 1:5:2:6 with xyerrorbars lw 2 lc rgb "blue" title ("Dati con errori")