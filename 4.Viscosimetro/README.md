# Guida alla cartella
Il file "viscosimetro.ipynb" è il codice Jupiter che elabora i file dati "glicerolo.txt" e "sapone.txt".
Il file "funzioni.py" è l'header file con le funzioni utilizzate, si consiglia una consultazione per la scrittura del formulario in appendice.
Il file "grafici.mplstyle" è un file complementare a "viscosimetro.ipynb" che serve a definire uno stile per i grafici, non è necessaria la consultazione.

# Grafici -> Elaborati
Guida a quali elaborati corrispondono a quali grafici.  
1.1 -> stokes (serie 1)  
1.2 -> stokes (serie 2)  
1.1_nocorrezione e 1.2_nocorrezione -> nocorrezione  
2 -> miglioristime  
4.1 e 4.2 (sono la stessa cosa) -> profondita  
5 -> memoria  
Il file "nome_elaborato_temporale.txt" non ha una corrispondenza con un grafico poichè rappresenta semplicemente l'analisi della bontà delle interpolazioni fatte per ogni sferetta: si è infatti calcolata una velocità limite per ogni sferetta, con cui poi si è calcolato un eta per ogni sferetta, graficati nel grafico 5. Nel codice questi passaggi sono presentati nel punto 3. Intervalli di Tempo; l'interpolazione e la valutazione citata sono svolte nel punto 3.2 Interpolazione.