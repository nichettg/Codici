set terminal pngcairo enhanced size 2500,1000 font "Arial,27"
set grid lc rgb "gray" lw 2
set xlabel "Forza (N)"
set ylabel "Differenza Allungamento (m)"
set format y "%.1e"
set key left top

set xrange [*:*]
set yrange [*:*]

files_a = "dati1a_o.txt dati2a_o.txt dati3a_o.txt dati4a_o.txt"
files_b = "dati1b_o.txt dati2b_o.txt dati3b_o.txt dati4b_o.txt"

plot_file(group) = sprintf("dati_%s_combined.png", group)

do for [group in "a b"] {
    set output plot_file(group)
    files = (group eq "a") ? files_a : files_b

    total_mean = 0
    count = words(files)

    do for [i=1:count] {
        stats word(files, i) using 2 nooutput
        total_mean = total_mean + STATS_mean
    }

    mean_value = total_mean / count

    plot for [i=1:count] word(files, i) using ($1*9.81e-3):($2*1e-6) with linespoints lw 2 pt i ps 2 lc i title word(files, i), \
         mean_value with lines lw 2 lc rgb "blue" title "Fit orizzontale"
}
