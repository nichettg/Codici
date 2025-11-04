#serie di dati

f(x) = a + b*x
fit f(x) "dati1a.txt" using ($1*9.81e-3):($2*1e-6) via a,b
fit f(x) "dati1b.txt" using ($1*9.81e-3):($2*1e-6) via a,b
fit f(x) "dati2a.txt" using ($1*9.81e-3):($2*1e-6) via a,b
fit f(x) "dati2b.txt" using ($1*9.81e-3):($2*1e-6) via a,b
fit f(x) "dati3a.txt" using ($1*9.81e-3):($2*1e-6) via a,b
fit f(x) "dati3b.txt" using ($1*9.81e-3):($2*1e-6) via a,b
fit f(x) "dati4a.txt" using ($1*9.81e-3):($2*1e-6) via a,b
fit f(x) "dati4b.txt" using ($1*9.81e-3):($2*1e-6) via a,b