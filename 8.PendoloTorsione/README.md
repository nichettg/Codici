# Guida Struttura Cartella
Nella cartella **Data** sono caricati i file dati grezzi.

Nella cartella **Images** sono caricati i seguenti grafici:
- *ConfrontoForzanti.pdf*: ampiezza delle oscillazioni a diverse frequenza forzanti; la parte di smorzamento (quindi quando viene tolta la forzante) è stata tagliata ed è presentata nel grafico che segue.
- *ConfrontoSmorzatipdf*: ampiezza delle oscillazioni a diverse frequenze forzanti dopo che quest'ultime sono state tolte; fase di smorzamento.
- *ConfrontoMassimi.pdf*: (grafico di controllo, superfluo) picchi delle oscillazioni usati per definire l'ampiezza media per le varie frequenze forzanti; sono stati trascurati (nel grafico e nei calcoli successivi) i picchi negativi (da modificare?).
- *Lorentziana.pdf*: curva Lorentziana delle ampiezze (media dei punti del grafico precedente) con fit per individuare il picco ( $x_0$ ).

Il file **pendolo.ipynb** è il file Jupyter che contiene tutti i calcoli. Nella sezione 2.3 è presente il modello del fit utilizzato, eseguito con il modulo *scipy.optimize*.
