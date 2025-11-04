#plot.txt
set terminal pngcairo enhanced size 2500,1000 font "Arial,27"

set grid lc rgb "gray" lw 2
set ylabel "Tempo (s)"
set xlabel "Spazio (m)"
set key left top

f(x) = a + b*x

set output "velocita_1.png"
fit f(x) "plot.txt" index 0 using 1:4:5 via a,b
plot "plot.txt" index 0 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "red" title ("Dati con errori"), \
    f(x) lw 2 lc rgb "blue"

set output "velocita_2.png"
fit f(x) "plot.txt" index 1 using 1:4:5 via a,b
plot "plot.txt" index 1 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "red" title ("Dati con errori"), \
    f(x) lw 2 lc rgb "blue"

set output "velocita_3.png"
fit f(x) "plot.txt" index 2 using 1:4:5 via a,b
plot "plot.txt" index 2 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "red" title ("Dati con errori"), \
    f(x) lw 2 lc rgb "blue"

set output "velocita_4.png"
fit f(x) "plot.txt" index 3 using 1:4:5 via a,b
plot "plot.txt" index 3 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "red" title ("Dati con errori"), \
    f(x) lw 2 lc rgb "blue"

set output "velocita_5.png"
fit f(x) "plot.txt" index 4 using 1:4:5 via a,b
plot "plot.txt" index 4 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "red" title ("Dati con errori"), \
    f(x) lw 2 lc rgb "blue"

set output "confronto_velocita.png"
plot "plot.txt" index 0 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "red" title ("Serie 1"), \
    "plot.txt" index 1 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "purple" title ("Serie 2"), \
    "plot.txt" index 2 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "blue" title ("Serie 3"), \
    "plot.txt" index 3 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "pink" title ("Serie 4"), \
    "plot.txt" index 4 using 1:4:2:5 with xyerrorbars lw 2 lc rgb "violet" title ("Serie 5")
