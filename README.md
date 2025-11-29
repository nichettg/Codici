# Note Esperienza
Gli assi verticali dei carrellini, data la forma dei carrellini stessi, potrebbero non essere complanari all asse orizzontale della guida: fintanto che entrambi gli assi verticali risultano comunque spostati di un uguale distanza tale sistematica risulta ininfluente.

Serve quantificare la correzione dovuta alla distanza dal punto di misurazione alla base del carrellino e l'effettiva distanza di CCD e lente.

Poi serve:
+ implementare sul programma le correzioni dei vari errori sistematici e rifare grafici e chi quadrato con dati corretti (meglio se si mette in output i vari errori singoli così possiamo inserire i vari contributi alla misura finale)
+ implementare sul programma le incertezze sulla focale in entrambi i metodi, minimizzare il chi quadrato parametrico per trovare il parametro ottimo, fare il grafico dell'andamento dei parametri (dovrebbe uscire una parabola), stabilire in base al grafico l'incertezza del parametro ottimo (A*=DeltaA/2) e mettere indice di compatibilità per comparare i metodi
+ fare le immagini dell'apparato strumentale come quelle del logbook con tutte le grandezze in gioco e i nomi collegati con le frecce (se possibile le scritte meglio scriverle con la tastiera e non a mano perchè mi urta molto) (i numeri direi di non scriverli nel disegno ma dare un nome che poi viene associato al numero nella tabella)
+ fare l'analisi delle immagini della aberrazione con ImaJ facendo profilo d'intensità sul diametro, scegliere i confini del foro stabilendo la percentuale di intensità, porre il diametro pari a 0.5mm e fare la misura della distanza dei fori marginali, così per tutte le immagini di quelle sfocate e a fuoco
+ implementare il programma (o fare un programma separato) per il calcolo delle aberrazioni sferiche longitudinali e trasversali per ogni colore e poi quelle cromatiche sia per i marginali che trasversali; va implementata anche la correzione degli errori sistematico della lente spessa anche per la lente 2 per il calcolo delle aberrazioni
+ fare la tabella dei dati grezzi senza sistematiche
+ fare la tabella dei dati corretti con le sistematiche, covarianza
+ fare la tabella delle misure delle posizioni/distanze usate per analizzare i dati
+ fare la tabella dei risultati delle focali, indice compatibilità, parametri ottimali con incertezze
+ fare la tabella dei risultati delle aberrazioni



N.B. i p-value qui valgono meno di 0 perchè il chi quadrato qui fallisce pesantemente essendo che le incertezze non sono a priori, se decidiamo di usare la media delle focali NON bisogna usare l'errore della media perchè p e q non sono statisticamente indipendenti
