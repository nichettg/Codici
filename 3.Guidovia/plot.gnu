set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

#1
set output "progressivo1.png"
set grid lc rgb "gray" lw 2
set xlabel "Tempo (s)"
set ylabel "Velocità (m/s)"
set format x "%.1f"
set format y "%.3f"
set key left top

f(x) = a + b*x
fit f(x) "plot1.txt" using 1:2:4 via a,b

plot "plot1.txt" using 1:2:3:4 with xyerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2f + %.3fx", a, b) lw 2 lc rgb "blue"

#2
set output "progressivo2.png"
set grid lc rgb "gray" lw 2
set xlabel "Tempo (s)"
set ylabel "Velocità (m/s)"
set format x "%.1f"
set format y "%.3f"
set key left top

f(x) = a + b*x
fit f(x) "plot2.txt" using 1:2:4 via a,b

plot "plot2.txt" using 1:2:3:4 with xyerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2f + %.3fx", a, b) lw 2 lc rgb "blue"

#3
set output "progressivo3.png"
set grid lc rgb "gray" lw 2
set xlabel "Tempo (s)"
set ylabel "Velocità (m/s)"
set format x "%.1f"
set format y "%.3f"
set key left top

f(x) = a + b*x
fit f(x) "plot3.txt" using 1:2:4 via a,b

plot "plot3.txt" using 1:2:3:4 with xyerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2f + %.3fx", a, b) lw 2 lc rgb "blue"

#4
set output "progressivo4.png"
set grid lc rgb "gray" lw 2
set xlabel "Tempo (s)"
set ylabel "Velocità (m/s)"
set format x "%.1f"
set format y "%.3f"
set key left top

f(x) = a + b*x
fit f(x) "plot4.txt" using 1:2:4 via a,b

plot "plot4.txt" using 1:2:3:4 with xyerrorbars lw 2 lc rgb "red" title "Dati con errori", \
    f(x) title sprintf("Fit lineare: y = %.2f + %.3fx", a, b) lw 2 lc rgb "blue"