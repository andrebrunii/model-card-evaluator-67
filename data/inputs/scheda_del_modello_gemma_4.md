# Scheda del modello Gemma 4 | Google AI for Developers

* **Risorse ufficiali:** Hugging Face | GitHub | Blog di lancio | Documentazione | Report tecnico
* **Licenza:** Apache 2.0
* **Autori:** Google DeepMind

Gemma è una famiglia di modelli aperti creati da Google DeepMind. I modelli **Gemma 4** sono multimodali, gestiscono l'input di testo e immagini (con audio supportato sui modelli E2B, E4B e 12B) e generano output di testo. Questa release include modelli *open-weights* nelle varianti pre-addestrate e ottimizzate per le istruzioni (*instruction-tuned*). Gemma 4 ha una finestra contestuale fino a **256.000 token** e mantiene il supporto multilingue in oltre **140 lingue**.

Caratterizzato da architetture **Dense** e **Mixture-of-Experts (MoE)**, Gemma 4 è adatto ad attività come la generazione di testo, la programmazione e il ragionamento. I modelli sono disponibili in cinque dimensioni distinte: **E2B, E4B, 12B, 26B A4B e 31B**. Le loro diverse dimensioni li rendono implementabili in ambienti che vanno dagli smartphone di fascia alta ai laptop e ai server, democratizzando l'accesso all'AI allo stato dell'arte.

### Progressi architettonici e funzionalità chiave
* **Ragionamento:** tutti i modelli della famiglia sono progettati per essere ottimi ragionatori, con modalità di pensiero (*thinking mode*) configurabili.
* **Multimodalità estese:** elabora testo, immagini con supporto di proporzioni e risoluzione variabili (tutti i modelli), video e audio (funzionalità integrata nei modelli E2B, E4B e 12B).
* **Architetture diverse ed efficienti:** offre varianti dense e Mixture-of-Experts (MoE) di dimensioni diverse per un deployment scalabile.
* **Ottimizzato per il dispositivo (On-device):** i modelli più piccoli sono progettati specificamente per un'esecuzione locale efficiente su laptop e dispositivi mobili.
* **Finestra contestuale più ampia:** i modelli piccoli hanno una finestra contestuale di $128.000$ token, mentre i modelli medi e grandi supportano $256.000$ token.
* **Funzionalità di codifica e agenti avanzate:** ottiene miglioramenti notevoli nei benchmark di programmazione insieme al supporto nativo delle chiamate di funzioni (*function calling*), alimentando agenti autonomi altamente capaci.
* **Supporto nativo per il prompt di sistema:** Gemma 4 introduce il supporto nativo per il ruolo `system`, consentendo conversazioni più strutturate e controllabili.

---

## Panoramica dei modelli

I modelli Gemma 4 sono progettati per offrire prestazioni di livello avanzato in ogni dimensione, con l'obiettivo di scenari di deployment da dispositivi mobili e periferici (E2B, E4B) a GPU e workstation consumer (12B, 26B A4B, 31B). Sono adatti per ragionamento, flussi di lavoro agentici, programmazione e comprensione multimodale.

I modelli utilizzano un meccanismo di attenzione ibrido che alterna l'attenzione della finestra scorrevole locale (*sliding window attention*) con l'attenzione globale completa, garantendo che l'ultimo livello sia sempre globale. Questo design ibrido offre la velocità di elaborazione e l'ingombro di memoria ridotto di un modello leggero senza sacrificare la consapevolezza profonda necessaria per attività complesse e di contesto lungo. Per ottimizzare la memoria per contesti lunghi, i livelli globali sono caratterizzati da chiavi e valori unificati e applicano *Proportional RoPE* (p-RoPE).

### Modelli Densi

| Proprietà | E2B | E4B | 12B Unified | 31B Dense |
| :--- | :--- | :--- | :--- | :--- |
| **Parametri totali** | 2,3 Mld effettivi (5,1 Mld con embedding) | 4,5 Mld effettivi (8 Mld con embedding) | 11,95 Mld | 30,7 Mld |
| **Livelli** | 35 | 42 | 48 | 60 |
| **Finestra scorrevole** | 512 token | 512 token | 1024 token | 1024 token |
| **Lunghezza del contesto** | 128.000 token | 128.000 token | 256.000 token | 256.000 token |
| **Dimensioni del vocabolario** | 262.000 | 262.000 | 262.000 | 262.000 |
| **Modalità supportate** | Testo, immagine, audio | Testo, immagine, audio | Testo, immagine, audio | Testo, immagine |
| **Parametri dell'encoder Vision** | ~150 milioni | ~150 milioni | - (Unificato) | ~550 milioni |
| **Parametri del codificatore Audio** | ~300 milioni | ~300 milioni | - (Unificato) | Nessun audio |

* **Nota su "E" (E2B ed E4B):** La "E" sta per parametri *"effettivi"*. I modelli più piccoli incorporano gli incorporamenti per livello (*Per-Layer Embeddings*, PLE) per massimizzare l'efficienza dei parametri nelle implementazioni sul dispositivo. Anziché aggiungere altri livelli o parametri al modello, PLE assegna a ogni livello del decodificatore un piccolo embedding per ogni token. Queste tabelle di incorporamento sono grandi, ma vengono utilizzate solo per ricerche rapide, motivo per cui il conteggio dei parametri effettivi è molto inferiore al totale.
* **Nota su "Unified" (12B Unified):** Si riferisce alla sua architettura senza encoder esterni. Gli altri modelli Gemma 4 utilizzano encoder dedicati per elaborare i dati multimodali prima di passarli all'LLM. Gemma 4 12B elimina completamente questi encoder, proiettando le patch di immagini grezze e le forme d'onda audio direttamente nello spazio di incorporamento dell'LLM tramite livelli lineari leggeri. Tutte le modalità confluiscono direttamente in un unico Transformer solo con decoder, riducendo la latenza multimodale e consentendo l'ottimizzazione dell'intero modello in un'unica passata.

### Modello Mixture of Experts (MoE)

| Proprietà | 26B A4B MoE |
| :--- | :--- |
| **Parametri totali** | 25,2 Mld |
| **Parametri attivi** | 3,8 Mld |
| **Livelli** | 30 |
| **Finestra scorrevole** | 1024 token |
| **Lunghezza del contesto** | 256.000 token |
| **Dimensioni del vocabolario** | 262.000 |
| **Conteggio esperti** | 8 attivi / 128 totali e 1 condiviso |
| **Modalità supportate** | Testo, immagine |
| **Parametri dell'encoder Vision** | ~550 milioni |

* **Nota su "A" (26B A4B):** La "A" sta per *"parametri attivi"* in contrasto con il numero totale di parametri contenuti nel modello. Attivando solo un sottoinsieme di ~4 miliardi di parametri durante l'inferenza, il modello Mixture-of-Experts viene eseguito molto più velocemente di quanto potrebbe suggerire il totale di 26 miliardi (quasi alla stessa velocità di un modello denso da 4 miliardi di parametri).

---

## Risultati Benchmark

Questi modelli sono stati valutati in base a una vasta raccolta di set di dati e metriche per coprire diversi aspetti della generazione di testo, codice, matematica, multimodalità e contesto lungo. I risultati nella tabella si riferiscono ai modelli ottimizzati per le istruzioni (*Instruction-Tuned*).

| Benchmark | Gemma 4 31B | Gemma 4 26B A4B | Gemma 4 12B Unified | Gemma 4 E4B | Gemma 4 E2B | Gemma 3 27B (no think) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MMLU Pro** | 85,2% | 82,6% | 77,2% | 69,4% | 60,0% | 67,6% |
| **AIME 2026 (no tools)** | 89,2% | 88,3% | 77,5% | 42,5% | 37,5% | 20,8% |
| **LiveCodeBench v6** | 80,0% | 77,1% | 72,0% | 52,0% | 44,0% | 29,1% |
| **ELO di Codeforces** | 2150 | 1718 | 1659 | 940 | 633 | 110 |
| **GPQA Diamond** | 84,3% | 82,3% | 78,8% | 58,6% | 43,4% | 42,4% |
| **Tau2 (media su 3)** | 76,9% | 68,2% | 69,0% | 42,2% | 24,5% | 16,2% |
| **HLE (no tools)** | 19,5% | 8,7% | 5,2% | - | - | - |
| **HLE (con la ricerca)** | 26,5% | 17,2% | - | - | - | - |
| **BigBench Extra Hard** | 74,4% | 64,8% | 53,0% | 33,1% | 21,9% | 19,3% |
| **MMMLU** | 88,4% | 86,3% | 83,4% | 76,6% | 67,4% | 70,7% |
| **Vista MMMU Pro** | 76,9% | 73,8% | 69,1% | 52,6% | 44,2% | 49,7% |
| **OmniDocBench 1.5** *(più basso è migliore)* | 0,131 | 0,149 | 0,164 | 0,181 | 0,290 | 0,365 |
| **MATH-Vision** | 85,6% | 82,4% | 79,7% | 59,5% | 52,4% | 46,0% |
| **MedXPertQA MM** | 61,3% | 58,1% | 48,7% | 28,7% | 23,5% | - |
| **Audio CoVoST** | - | - | 38,5\* | 35,54 | 33,47 | - |
| **FLEURS** *(più basso è migliore)* | - | - | 0,069\* | 0,08 | 0,09 | - |
| **Contesto lungo MRCR v2 8 needle 128k** | 66,4% | 44,1% | 43,4% | 25,4% | 19,1% | 13,5% |

*\*Esclusa la lingua cinese.*

---

## Funzionalità principali

I modelli Gemma 4 gestiscono un'ampia gamma di attività relative a testo, visione e audio:

* **Ragionamento:** modalità di ragionamento integrata che consente al modello di pensare passo dopo passo prima di rispondere.
* **Contesto lungo:** finestre contestuali fino a $128.000$ token (E2B/E4B) e $256.000$ token (12B/26B A4B/31B).
* **Comprensione delle immagini:** rilevamento di oggetti, analisi di documenti/PDF, comprensione di schermate e interfacce utente (UI), comprensione di grafici, OCR (inclusa la modalità multilingue), riconoscimento della scrittura a mano e puntamento (*pointing*). Le immagini possono essere elaborate con proporzioni e risoluzioni variabili.
* **Comprensione dei video:** analizza i video elaborando sequenze di frame.
* **Input multimodale intercalato:** mescola liberamente testo e immagini in qualsiasi ordine all'interno di un singolo prompt.
* **Chiamata di funzione (Function Calling):** supporto nativo per l'utilizzo strutturato degli strumenti, che consente flussi di lavoro basati su agenti autonomi.
* **Programmazione:** generazione, completamento e correzione del codice.
* **Multilingue:** supporto predefinito per oltre 35 lingue, preaddestramento su più di 140 lingue.
* **Audio (solo E2B, E4B e 12B Unified):** Riconoscimento vocale automatico (ASR) e traduzione speech-to-text in più lingue.

---

## Best practice e configurazione

Per un rendimento ottimale, utilizza queste configurazioni standardizzate:

### 1. Parametri di campionamento
Utilizza la seguente configurazione di campionamento in tutti i casi d'uso:
* `temperature = 1.0`
* `top_p = 0.95`
* `top_k = 64`

### 2. Configurazione della modalità di pensiero (Thinking Mode)
Rispetto a Gemma 3, i modelli utilizzano i ruoli standard `system`, `assistant` e `user`. Per gestire il processo di pensiero, utilizza i seguenti token di controllo:
* **Attivazione del pensiero:** il pensiero viene attivato includendo il token `<|think|>` all'inizio del prompt di sistema. Per disattivare la funzionalità di pensiero, rimuovi il token.
* **Generazione standard:** quando il pensiero è attivato, il modello restituisce il suo ragionamento interno seguito dalla risposta finale utilizzando questa struttura:
  `<|channel>thought\n [Ragionamento interno] <channel|>[Risposta finale]`
* **Comportamento di pensiero disattivato:** per tutti i modelli, ad eccezione delle varianti E2B ed E4B, se il pensiero è disattivato, il modello genererà comunque i tag, ma con un blocco di pensiero vuoto:
  `<|channel>thought\n <channel|>[Risposta finale]`

### 3. Risoluzione variabile dell'immagine
Oltre alle proporzioni variabili, Gemma 4 supporta la risoluzione variabile delle immagini tramite un budget di token visivi configurabile. Un budget di token più elevato preserva maggiori dettagli visivi a costo di un calcolo aggiuntivo, mentre un budget inferiore consente un'inferenza più rapida per le attività che non richiedono una comprensione granulare.
* **Budget di token visivi supportati:** `70`, `140`, `280`, `560` e `1120`.

---

## Set di dati di addestramento e trattamento

I modelli sono stati addestrati su un set di dati multimodale diversificato comprendente documenti web, codice, testo matematico, immagini e audio, con una **data di interruzione delle conoscenze (knowledge cutoff) fissata a gennaio 2025**. Il set di dati include contenuti in oltre 140 lingue.

* **Documenti web:** una raccolta diversificata di testi web assicura che il modello sia esposto a un'ampia gamma di stili linguistici, argomenti e vocabolari.
* **Codice:** l'esposizione al codice aiuta il modello a imparare la sintassi e i pattern dei linguaggi di programmazione, migliorando la capacità di generare codice e comprendere domande tecniche.
* **Matematica:** l'addestramento su testi matematici aiuta il modello a imparare il ragionamento logico, la rappresentazione simbolica e a rispondere a domande di matematica.
* **Immagini:** un'ampia gamma di immagini consente al modello di eseguire attività di analisi delle immagini, OCR ed estrazione di dati visivi.
* **Audio:** campioni audio diversificati (per i modelli abilitati) per il riconoscimento vocale e la comprensione del parlato multilingue.

---

## Etica e sicurezza

Man mano che i modelli aperti diventano fondamentali per l'infrastruttura aziendale, la provenienza e la sicurezza diventano di primaria importanza. Sviluppato da Google DeepMind, Gemma 4 è sottoposto alle stesse rigorose valutazioni di sicurezza dei modelli Gemini proprietari.

### Approccio di valutazione della sicurezza
I modelli sono stati testati e filtrati rispetto alle seguenti categorie critiche:
* Contenuti relativi a materiale pedopornografico e sfruttamento (CSAM/CSAE).
* Contenuti pericolosi (ad es. promozione del suicidio, autolesionismo, CBRN o istruzioni per attività che potrebbero causare danni nel mondo reale).
* Contenuti sessualmente espliciti.
* Incitamento all'odio (ad es. disumanizzazione dei membri di gruppi protetti).
* Molestie (ad es. incitamento alla violenza o minacce contro le persone).

### Risultati della valutazione di sicurezza
Per la sintesi da testo a testo e la sintesi da immagine a testo, e per tutte le dimensioni dei modelli, Gemma 4 ha prodotto violazioni minime delle norme di sicurezza e ha mostrato miglioramenti significativi rispetto alle prestazioni dei modelli Gemma precedenti.

---

## Utilizzo previsto e Limitazioni

### Utilizzo previsto (Intended Use)
Il seguente elenco di potenziali utilizzi fornisce informazioni contestuali sui casi d'uso che i creatori del modello hanno preso in considerazione nell'ambito dell'addestramento e dello sviluppo:

* **Creazione di contenuti e comunicazione:**
  * *Generazione di testo:* generazione di formati di testo creativi come poesie, copioni, codice, testi di marketing e bozze di email.
  * *Chatbot e AI conversazionale:* potenziamento di interfacce conversazionali per il servizio clienti, assistenti virtuali o applicazioni interattive.
  * *Riepilogo del testo:* generazione di riepiloghi concisi di un corpus di testo, documenti di ricerca o report.
  * *Estrazione dei dati delle immagini:* estrazione, interpretazione e riassunto di dati visivi per le comunicazioni di testo.
  * *Elaborazione e interazione audio:* i modelli E2B, E4B e 12B possono analizzare e interpretare gli input audio, consentendo interazioni e trascrizioni basate sulla voce.
* **Ricerca e istruzione:**
  * *Ricerca sull'elaborazione del linguaggio naturale (NLP) e sui modelli VLM:* base per i ricercatori per sperimentare tecniche VLM e NLP, sviluppare algoritmi e contribuire al progresso del settore.
  * *Strumenti per l'apprendimento delle lingue:* supporto a esperienze di apprendimento interattive, correzione della grammatica o fornitura di esercizi di scrittura.
  * *Esplorazione delle conoscenze:* assistenza ai ricercatori nell'esplorazione di grandi quantità di testo generando riepiloghi o rispondendo a domande su argomenti specifici.

### Limitazioni (Limitations)
* **Dati di addestramento:** la qualità e la diversità dei dati di addestramento influiscono in modo significativo sulle capacità del modello. Bias o lacune nei dati di addestramento possono portare a limitazioni nelle risposte. L'ambito del set di dati di addestramento determina gli argomenti che il modello può gestire in modo efficace.
* **Contesto e complessità dell'attività:** i modelli funzionano bene con attività che possono essere inquadrate con prompt e istruzioni chiari. Le attività aperte o molto complesse potrebbero essere difficili. Il rendimento di un modello può essere influenzato dalla quantità di contesto fornito (un contesto più lungo generalmente porta a risultati migliori, fino a un certo punto).
* **Ambiguità e sfumature del linguaggio:** il linguaggio naturale è intrinsecamente complesso. I modelli potrebbero avere difficoltà a cogliere sfumature sottili, sarcasmo o linguaggio figurato.
* **Accuratezza fattuale:** i modelli generano risposte basate sulle informazioni apprese dai set di dati di addestramento, ma **non sono knowledge base**. Potrebbero generare affermazioni fattuali errate o obsolete (allucinazioni).
* **Common Sense (Buon senso):** i modelli si basano su pattern statistici nel linguaggio. Potrebbero non essere in grado di applicare il ragionamento di buon senso in determinate situazioni del mondo reale.

### Considerazioni etiche e rischi
Nella creazione di un modello aperto, sono stati considerati attentamente i seguenti fattori:
* **Pregiudizi ed equità (Bias & Fairness):** i modelli VLM addestrati su dati di testo e immagini reali su larga scala possono riflettere i bias socio-culturali incorporati nel materiale di addestramento. I modelli Gemma 4 sono stati sottoposti a un attento esame, al pretrattamento dei dati di input e a valutazioni post-addestramento per contribuire a mitigare il rischio di questi bias.
* **Disinformazione e uso improprio:** i VLM possono essere utilizzati in modo improprio per generare testi falsi, fuorvianti o dannosi. Gli sviluppatori devono consultare le linee guida nel *Responsible Generative AI Toolkit* e rispettare la *Gemma Prohibited Use Policy*.
* **Trasparenza e responsabilizzazione:** questa scheda del modello riassume i dettagli sull'architettura, sulle funzionalità, sulle limitazioni e sui processi di valutazione dei modelli per consentire un utilizzo consapevole e responsabile nell'ecosistema AI.

### Vantaggi
Al momento del rilascio, questa famiglia di modelli fornisce implementazioni di modelli *open vision-language* ad alte prestazioni progettate da zero per lo sviluppo di AI responsabile rispetto a modelli di dimensioni simili.