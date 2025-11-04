#grafico moli
set terminal pdfcairo size 32.5cm,18.3cm
set output '../Grafici/moli_primo.pdf'

set title "Numero di moli prima serie" font ",30"
set xlabel "Tempo (s)" font ",20"
set ylabel "Moli" font ",20"

set grid

set key font ",20"
set xtics font ",15"
set ytics font ",15"

f(x)= a*x + b
a = -4.762e-9
b = 0.0009800275

fit f(x) '../Elaborati/moli_primo.txt' using 1:2 via a, b

plot '../Elaborati/moli_primo.txt' using 1:4 with points pt 0 ps 0.5 lc 'red' title 'Incertezza',\
      ""              using 1:5 with points pt 0 ps 0.5 lc 'red' notitle,\
      ""              using 1:2 with points pt 7 ps 0.15 lc 'blue' title 'Numero di moli',\
      f(x) title 'Fit lineare' with lines lw 2 lc 'black'

############################################################################################################################

set terminal pdfcairo size 32.5cm,18.3cm
set output '../Grafici/moli_15.pdf'

set title "Numero di moli 15°C" font ",30"
set xlabel "Tempo (s)" font ",20"
set ylabel "Moli" font ",20"

set grid

set key font ",20"
set xtics font ",15"
set ytics font ",15"

plot '../Elaborati/moli_15.txt' using 1:4 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' title 'Incertezza',\
      ""           using 1:5 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' notitle,\
      ""           using 1:2 with linespoints pt 7 ps 0.15 lc 'blue' title 'Numero di moli'

###############################################################################################################################

set terminal pdfcairo size 32.5cm,18.3cm
set output '../Grafici/moli_25.pdf'

set title "Numero di moli 25°C" font ",30"
set xlabel "Tempo (s)" font ",20"
set ylabel "Moli" font ",20"

set grid

set key font ",20"
set xtics font ",15"
set ytics font ",15"

plot '../Elaborati/moli_25.txt' using 1:4 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' title 'Incertezza',\
      ""           using 1:5 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' notitle,\
      ""           using 1:2 with linespoints pt 7 ps 0.15 lc 'blue' title 'Numero di moli'

###############################################################################################################################

set terminal pdfcairo size 32.5cm,18.3cm
set output '../Grafici/moli_35.pdf'

set title "Numero di moli 35°C" font ",30"
set xlabel "Tempo (s)" font ",20"
set ylabel "Moli" font ",20"

set grid

set key font ",20"
set xtics font ",15"
set ytics font ",15"

plot '../Elaborati/moli_35.txt' using 1:4 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' title 'Incertezza',\
      ""           using 1:5 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' notitle,\
      ""           using 1:2 with linespoints pt 7 ps 0.15 lc 'blue' title 'Numero di moli'

###############################################################################################################################

set terminal pdfcairo size 32.5cm,18.3cm
set output '../Grafici/moli_45.pdf'

set title "Numero di moli 45°C" font ",30"
set xlabel "Tempo (s)" font ",20"
set ylabel "Moli" font ",20"

set grid

set key font ",20"
set xtics font ",15"
set ytics font ",15"

plot '../Elaborati/moli_45.txt' using 1:4 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' title 'Incertezza',\
      ""           using 1:5 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' notitle,\
      ""           using 1:2 with linespoints pt 7 ps 0.15 lc 'blue' title 'Numero di moli'

###############################################################################################################################

set terminal pdfcairo size 32.5cm,18.3cm
set output '../Grafici/moli_55.pdf'

set title "Numero di moli 55°C" font ",30"
set xlabel "Tempo (s)" font ",20"
set ylabel "Moli" font ",20"

set grid

set key font ",20"
set xtics font ",15"
set ytics font ",15"

plot '../Elaborati/moli_55.txt' using 1:4 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' title 'Incertezza',\
      ""           using 1:5 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' notitle,\
      ""           using 1:2 with linespoints pt 7 ps 0.15 lc 'blue' title 'Numero di moli'
      
###############################################################################################################################

set terminal pdfcairo size 32.5cm,18.3cm
set output '../Grafici/moli_temp.pdf'

set title "Moli in funzione dell temperatura" font ",30"
set xlabel "Temperatura (°C)" font ",20"
set ylabel "Moli" font ",20"

set grid

set ytics 0, 0.00001
set xtics 0, 5

set xrange [0:60]
set yrange [0.00093:0.00103]

set key font ",20"
set xtics font ",15"
set ytics font ",15"

f(x)= a*x + b
a = -2.2e-8
b = 0.00101178 

fit f(x) '../Elaborati/moli_temp.txt' using 1:2 via a, b

plot '../Elaborati/moli_temp.txt' using 1:4 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' title 'Incertezza',\
      ""           using 1:5 with linespoints lw 0.5 pt 0 ps 0.5 lc 'red' notitle,\
      ""           using 1:2 with linespoints pt 7 ps 0.15 lc 'blue' title 'Numero di moli',\
      f(x) title 'Fit lineare' with lines lw 2 lc 'black'