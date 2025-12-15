## Guida ai file della cartella
Nel codice "analisi.ipynb" sono presenti dei commenti utili per seguire il processo di analisi dati e per ricordari quali scelte sono state prese nel caso ad esempio dell'assegnazione di certe incertezze.

I file "compatibilita_coniugati.txt" e "compatibilita_bessel.txt" riassumono tutti i metodi usati per calcolare i vari valori delle focali per i due metodi (per dettagli vedere il file jupyter) e mostrano le compatibilità tra i vari metodi. NON serve "scegliere" una sola stima tra le tante presentate.

I file "focali.txt" e "aberrazione.txt" sono quelli che riassumono i risultati forse più importanti, quindi i valori delle focali calcolati con i vari metodi e i valori delle aberrazioni.

#### Dove trovare i vari commenti ai metodi di calcolo
Per i punti coniugati abbiamo che:
- Lineare: si trova al punto 1.2.1 e vuol dire che si è fatta una regressione con minimi quadrati in maniera analitica prima valutando solo incertezze su p e poi solo su q.
- Retta: si trova sempre al punto 1.2.1 e vuol dire che il fit è stato eseguito mantenendo fissata la pendenza al valore teorico di -1.
- Minimi Quadrati: si trova al punto 1.2.2 e vuol dire che è stato usato il metodo della parabola SA/A.
- Campione: si trova al punto 1.2.3 e vuol dire che è stata applicata la formula per ogni coppia $(p_i,q_i)$.
Per avere i dettagli e le formule scritte già in Latex andare ai punti citati nel codice.
Tutte le stime sono riassunte nel file "compatibilita_coniugati.txt".

Per Bessel abbiamo che:
- Media, poi formula: si trova al punto 2.2.1.
- Formula, poi media: si trova al punto 2.2.2.
Per avere i dettagli e le formule scritte già in Latex andare ai punti citati nel codice.
Tutte le stime sono riassunte nel file "compatibilita_bessel.txt".

Nel file "focali.txt" è presentata la compatibilità tra una stima (scelta arbitrariamente) per i coniugati e una per Bessel (ho fatto la compatibilità tra "Minimi Quadrati" per coniugati e "Formula, poi media" per Bessel). La compatibilità è ovviamente indicativa visto che non è stata calcolata per tutte le varie stime, è una compatibilità indicativa dei due metodi.

I residui sono stati calcolati ma forse meglio non metterli in relazione.
