Si ricorda che il progetto è obbligatorio.

Il  progetto può essere richiesto e può essere presentato sia prima che dopo aver sostenuto la prova scritta.

Il progetto deve essere richiesto al docente tramite email indicando email e Cognome, Nome, NumeroDiMatricola del/dei partecipante/i in accordo con le indicazioni sottostanti, **nel caso di progetti di gruppo lo studente che spedisce la mail deve mettere in indirizzo oltre al docente anche l'altro membro del gruppo**.

L’**assegnazione del progetto** verrà confermata e trascritta su UniStudium, se non vedete la trascrizione ma avete ricevuto email di conferma dal docente il progetto è confermato.

Tutti i progetti prevedono un **massimo di due persone per gruppo**, a meno che diversamente indicato. I progetti possono essere assegnati a gruppi diversi l’eventuale esaurimento delle disponibilità di un progetto verrà segnalata dal docente su UniStudium (se necessario l’NFC verrà fornito dal docente)

Il progetto deve essere presentato oralmente da tutti i membri, la presentazione deve includere una demo del funzionamento dell’oggetto software sviluppato ed una relazione.

### Relazione
**La** **consegna del progetto avviene tramite upload sulla piattaforma** di un unico file .zip, e consiste in una **relazione** ed eventuali file aggiuntivi contenenti:
- Copertina con **_titolo del progetto, anno accademico, nome, cognome e matricola dei membri del gruppo_**_, nome del corso e del docente_
- **Abstract-sommario,** del progetto (credo sia l'indice)
- **Obiettivo del progetto** = descrizione breve, espansione del titolo
- ==**Analisi dei requisiti**==, incluso glossario dei principali termini, **descrizione dei requisiti del sistema**. Attenzione: l’analisi dei requisiti **NON è l’analisi del progetto realizzato**, ma è preliminare alla realizzazione del progetto stesso.
- ==**Architettura del sistema**==, descrizione testuale e attraverso i seguenti diagrammi UML:
	- diagramma di classe completo
	- diagramma di un caso d’uso A
	- diagramma di sequenza e diagramma di collaborazione riferito al caso d'uso A X
	- diagramma di stato di un elemento del sistema a scelta che si ritiene significativo
	- diagramma di una attività a scelta del sistema
- **Realizzazione e implementazione**: ==codice== sorgente del programma, query creazione/interrogazione database, file di configurazione etc.
- **==Test==:** un insieme di casi di test funzionali per un aspetto del progetto ritenuto significativo, valutando e dando descrizione motivata del grado di copertura ottenuta da tali test.
- il codice ed i dati di test saranno forniti in file aggiuntivi, la relazione in pdf ed eventuali slides di presentazione in pdf/ppt/odt

La **qualità e l’usabilità delle interfacce** e delle funzioni di uso e del prodotto software sarà oggetto di valutazione.

**A meno che diversamente specificato i progetti prevedono tutti max 2 persone, possono essere scelti da uno o due studenti.**


--------

### Progetto scelto
I seguenti progetti richiedono anche una parte di programmazione lato server (es. in Php, Python, ...) e potranno richiedere l’uso di semplici tabelle di database con le quali saranno reperite o memorizzate le informazioni richieste; alcune informazioni da ricercare/visualizzare potranno essere reperite da siti web.
**Attenzione:** Le classi dell’architettura UML fornite in questi progetti non dovranno essere quelle programmate, nel linguaggio utilizzato, ma riflettere le associazione tra i dati e gli oggetti principali del sistema.

**10.5 Canale per Consegna di un compito**
Si predisponga un canale in cui i partecipanti, sono di due tipi DOCENTI e STUDENTI.

Gli studenti hanno a disposizione:
- il comando LISTA DOCENTI in cui viene fornito l’elenco dei docenti e dei loro ID,
- il comando CONSEGNA _ID_docente_ in cui la foto di uno o più pagine di una prova scritta cartacea viene caricata per la consegna al docente.

I DOCENTI hanno a disposizione:
- il comando CONSEGNE che restituisce la lista degli _ID_studenti_ che hanno effettuato delle consegne nel giorno corrente,
- il comando LEGGI _ID_studente_ che visualizza o rende scaricabili le foto caricate dagli studenti nel giorno corrente.
- Eventuali comandi per ampliare il periodo temporale.

La configurazione Docenti, Studenti e Consegne con data/ora relativa è mantenuta in apposite tabelle del database lato server.

==_Tabelle docenti, studenti, consegne con data/ora_==


Segui questi passaggi:
1. Definizione del flusso di interazione:
	- Gli studenti possono utilizzare il comando /lista_docenti per ottenere l'elenco dei docenti e i loro ID.
	- Gli studenti possono utilizzare il comando /consegna ID_docente per caricare la foto della prova scritta per la consegna al docente.
	- I docenti possono utilizzare il comando /consegne per visualizzare gli ID degli studenti che hanno effettuato consegne nel giorno corrente.
	- I docenti possono utilizzare il comando /leggi ID_studente per visualizzare o scaricare le foto caricate dagli studenti nel giorno corrente.
2. Progettazione del database:
	- Creare tre tabelle nel database per memorizzare le informazioni sui docenti, gli studenti e le consegne.
	- La tabella "docenti" dovrebbe includere i campi per l'ID del docente e altri dati pertinenti.
	- La tabella "studenti" dovrebbe includere i campi per l'ID dello studente e altri dati pertinenti.
	- La tabella "consegne" dovrebbe includere i campi per l'ID dello studente, l'ID del docente, la data/ora di consegna e altre informazioni relative alla consegna.
3. Implementazione del bot Telegram:
	- Utilizza un framework o una libreria per sviluppare il bot Telegram, come ad esempio python-telegram-bot per Python.
	- Crea i gestori di comandi per i comandi descritti sopra (/lista_docenti, /consegna, /consegne, /leggi) che interagiscono con il database per recuperare e memorizzare le informazioni necessarie.
	- Per il comando /lista_docenti, recupera le informazioni sui docenti dalla tabella "docenti" e invia un messaggio contenente l'elenco degli studenti e dei loro ID.
	- Per il comando /consegna, salva le informazioni sulla consegna nella tabella "consegne", inclusa la foto caricata dallo studente.
	- Per il comando /consegne, recupera gli ID degli studenti che hanno effettuato consegne nel giorno corrente dalla tabella "consegne" e invia un messaggio contenente l'elenco degli ID degli studenti.
	- Per il comando /leggi, recupera le foto caricate dagli studenti nel giorno corrente dalla tabella "consegne" utilizzando l'ID dello studente specificato e invia o rendi scaricabile la foto al docente.
4. Gestione delle date/orari:
	- Assicurati che il sistema abbia una gestione accurata delle date e degli orari, in modo da poter registrare correttamente le consegne effettuate nel giorno corrente.
	- Utilizza funzionalità o librerie appropriate per gestire le date e gli orari nel linguaggio di programmazione utilizzato.
5. Gestione delle autorizzazioni:
	- Implementa un sistema di autorizzazioni per garantire che solo gli studenti e i docenti autorizzati possano accedere ai comandi pertinenti.
	- Puoi utilizzare ad esempio un sistema di autenticazione basato su token o altri meccanismi di autenticazione per verificare l'identità degli utenti.

Assicurati di adattare l'implementazione alle tue specifiche esigenze e al linguaggio di programmazione che stai utilizzando. Considera anche la gestione degli errori, la sicurezza e altre funzionalità aggiuntive che potrebbero essere necessarie nel contesto del tuo progetto.

token: 6370580588:AAGKKqCgMAtPduC4Nb63IzwPepFycdkvn8w


tasto destro, ispeziona.
libreria da usare per prendere solo tabelle da sito: Beautiful soup