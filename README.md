# Cose che mancano da fare per RC in frequenza

Ho fatto fit linearizzato, fit non lineare, fit locale su curva non linearizzata, fit di Bode. Ho poi unito in un unico file il confronto delle varie stime della frequenza di taglio.

- Il fit locale serviva? (forse no) L'ho fatto solo sulla curva non lineare, va fatto anche sulla curva di Bode? (in teoria va bene come ho fatto). L'incertezza di Bode viene alta sulle dispense e bassa a noi perche sulle dispense si usa fit lineare, noi lo usiamo non lineare.

- Fare un check del modo in cui ho convertito i dati grezzi in dati graficati ("conversione.ipynb") e di come poi ho convertito i parametri del fit in ferquenza di taglio ("confronto.ipynb"). In particolare i $\phi$ risultano avere qualche comportamento strano riguardante il segno.

- Variare le incertezze dei dati (abbassarle per i casi in cui si ha chi quadro basso, alzarle quando il chi quadro è alto).

- Togliere gli offset (gradi di libertà aggiunti in quasi tutti i fit) qualora non servano.