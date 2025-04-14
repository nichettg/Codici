# Aggiornamenti
Graficati istogrammi, fatto fit esponenziale ed eseguito test del chi-quadro.

IL GRAFICO 2m HA UN ERRORE NEL CALCOLO DEL FIT.
# Processo
I dati grezzi (Raw) sono stati elaborati con numero di bin bin=1 (modificabile) dal file RawToData. I file processati dal codice C++ sono salvati nella cartella Data. Viene poi graficato l'istogramma eseguendo uno zoom sull'area attorno al valore di 360, dove ci aspettiamo un picco (Images). E' poi eseguito un fit esponenziale sull'intero set di dati, anche se, avendo eseguito uno zoom, esso sembra ad occhio quasi lineare decrescente. E' eseguito un test del chi-quadro rispetto all'ipotesi del fit (Elaborati).

Leggere file conteggi.ipynb per dettagli.