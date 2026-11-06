---
base_model: Qwen/Qwen3.8-27B
base_model_relation: finetune
library_name: transformers
pipeline_tag: image-text-to-text
license: apache-2.0
language:
  - en
tags:
  - safetensors
  - qwen3_5
  - heretic
---

# Model card · Qwen3.8-27B-Ultimate-Heretic-Uncensored

**Checkpoint** `DavidAU/Qwen3.8-27B-Ultimate-Heretic-Uncensored`  
**Revisione esaminata** `5d5158cd7f8d76e28bfb3866c664fb0a9f7a593d`  
**Data della scheda** 5 novembre 2026 · **Tipo** scheda indipendente in italiano, basata sulla documentazione pubblica. Il campo YAML `language` indica la lingua etichettata per il modello.  
**Ambito** pesi sorgente BF16 di DavidAU. Le osservazioni su altre build o quantizzazioni sono identificate separatamente. Verifica documentale, senza esecuzione del modello.

## Identità e uso previsto

DavidAU pubblica un fine-tune del modello multimodale di Qwen per generare testo a partire da testo e, per la pipeline dichiarata, da immagini con una richiesta testuale. L’autore illustra soprattutto scrittura creativa, gioco di ruolo, generazione di codice SVG e selezione di modalità tramite prompt. Generare codice che disegna un pellicano dimostra una generazione testuale. Per misurare la comprensione visiva serve invece fornire un’immagine e verificare la risposta su ciò che contiene. [Scheda del derivato][card] · [Scheda del modello di base][base]

Un uso adatto al progetto è confrontare documentazione e comportamento del derivato con quelli del modello di base, mantenendo costanti input e criteri di giudizio. L’inglese compare nei metadati. La qualità dell’italiano e la parità fra lingue restano da misurare sul derivato. Per decisioni ad alto impatto o azioni automatiche con strumenti esterni, questa scheda non offre una validazione applicativa. [Scheda del derivato][card]

## Specifiche tecniche

| Campo | Valore osservato | Come interpretarlo |
|---|---|---|
| Famiglia e implementazione | Base dichiarata `Qwen/Qwen3.8-27B`. Classe `Qwen3_5ForConditionalGeneration`, tipo `qwen3_5` | Il nome della release e l’identificatore della classe Transformers descrivono due proprietà distinte. |
| Dimensione | 27B nel nome, circa 28B nella stima arrotondata del Hub | Registrare entrambi con provenienza e precisione. Il conteggio esatto richiederebbe un conteggio dei tensori con una regola esplicita per gli eventuali pesi ausiliari. |
| Distribuzione | Safetensors BF16, 12 shard principali, indice e file MTP separato. Il Hub mostra 55,7 GB per il repository | La dimensione su disco è distinta dalla memoria di picco, che dipende anche da runtime, cache, contesto e batch. |
| Ramo testuale | 64 blocchi, dimensione nascosta 5.120, intermedia 17.408, vocabolario di 248.320 token | Il pattern configurato alterna tre blocchi di attenzione lineare e uno di attenzione completa. Per l’attenzione completa sono indicate 24 teste query e 4 teste key/value. |
| Contesto | `max_position_embeddings = 262144` | È il limite posizionale configurato. La capacità di recuperare correttamente un dettaglio a quella distanza richiede una prova dedicata. |
| Ramo visivo | 27 blocchi, ampiezza 1.152, patch spaziale di 16, proiezione in uscita a 5.120 | Il file configura un ramo visivo e include identificatori immagine e video. La qualità sul video resta da verificare separatamente. |
| Generazione predefinita | Campionamento attivo, temperatura 1,0, top-k 20, top-p 0,95 | Salvare i parametri effettivi e il template usato a ogni esecuzione. Un runtime può sovrascrivere i valori del repository. |

Fonti tecniche: [configurazione del modello][config], [parametri di generazione][generation], [inventario dei file][tree], [metadati del Hub][card].

## Addestramento e provenienza dei dati

Il publisher presenta il checkpoint come fine-tune in più fasi e usa le denominazioni *Heretic*, *Cold Fusion* e *GAIN*. Nei metadati cita `DavidAU/Polar-STRICT-Datasets` e `DavidAU/F451-STRICT-Datasets`. Questo documenta i nomi dichiarati. Per riprodurre il training servirebbero anche versioni dei dati, proporzioni, trasformazioni, ordine delle fasi, iperparametri e checkpoint intermedi. La documentazione consultata lascia indeterminati questi dettagli. Il termine *Heretic* da solo non identifica i tensori modificati o l’entità della modifica in questa build. [Scheda e metadati del publisher][card]

Restano da documentare per il derivato la composizione per lingua e dominio, il trattamento dei dati personali, le verifiche di sovrapposizione fra training e test, le ore di acceleratore e il consumo energetico. Il tag Apache-2.0 è la licenza dichiarata per il repository del modello. La provenienza e le licenze dei singoli corpus richiedono documentazione separata. [Scheda del derivato][card]

## Valutazioni disponibili

| Affermazione da valutare | Evidenza pubblicata | Conclusione consentita |
|---|---|---|
| Il modello può seguire un prompt creativo con più personaggi | L’autore mostra due generazioni e descrive una prova su Ultimate 2 in Q6. | Esempio qualitativo riferito a quella build. Manca un tasso di successo su un campione definito per il checkpoint BF16. |
| Il modello produce codice SVG | Il publisher mostra immagini di output e indica una variante Q4KS di un ramo intermedio. | L’esempio supporta l’esistenza di un output selezionato. L’affidabilità su nuovi prompt e sulla distribuzione BF16 resta aperta. |
| “50x” indica un guadagno prestazionale | La denominazione compare nelle modalità promosse dall’autore. | Per convertirla in uno speedup occorrono una baseline, una metrica di tempo o throughput, qualità comparabile, hardware e ripetizioni. |
| Il derivato mantiene i punteggi del modello Qwen di base | La scheda upstream ha un soggetto e una procedura di valutazione propri. | I risultati del genitore possono fare da riferimento. Al derivato vanno assegnati soltanto risultati ottenuti sul derivato. |

Nelle fonti esaminate non emerge una suite standardizzata del checkpoint BF16 con versione del dataset, protocollo, baseline e punteggi riproducibili. Nessun benchmark è stato eseguito per produrre questa scheda. [Esempi e note dell’autore][card] · [Modello di base][base]

## Limiti, bias e comportamento di rifiuto

*Uncensored* descrive il posizionamento scelto dall’autore. Per quantificarne l’effetto servono almeno due gruppi distinti: richieste lecite che potrebbero essere rifiutate per errore e richieste per le quali la policy del progetto prescrive un rifiuto. Un unico tasso di rifiuto aggregato potrebbe nascondere un peggioramento in uno dei due gruppi. La documentazione consultata lascia aperti anche accuratezza fattuale, differenze di comportamento tra gruppi e affidabilità nella lettura delle immagini. [Scheda del derivato][card]

## Protocollo proposto per una verifica successiva

| Proprietà | Prova ripetibile | Metrica |
|---|---|---|
| Rifiuti appropriati ed eccessivi | Predisporre prompt sintetici etichettati secondo una policy scritta prima del test. Confrontare base e derivato sugli stessi esempi e sottoporre i casi ambigui a doppia revisione. | Rifiuti su richieste lecite / richieste lecite. Risposte che violano la policy / richieste soggette a restrizione. Riportare i due denominatori. |
| Istruzioni e lingua | Usare compiti appaiati in italiano e inglese, con vincoli verificabili sul formato e sul contenuto. | Percentuale di vincoli soddisfatti per lingua e per compito. |
| Visione | Generare immagini sintetiche con conteggi e posizioni noti. Ripetere la domanda con immagine corretta, assente e scambiata. | Accuratezza per condizione e differenza fra condizioni. |
| Efficienza | Confrontare le modalità sulla stessa build, stesso hardware e budget di output. Registrare token di ingresso e uscita, eventuali token di ragionamento esposti, latenza e correttezza. | Tempo mediano, p95 e token per risposta corretta. Riportare a parte le esecuzioni che esauriscono il budget. |

Per ripetere un test, conservare SHA di modello e base, hash del template, precisione o identificativo GGUF, motore e versione, dispositivo, seed, prompt, manifest del test e output grezzo. Riportare numerosità e incertezza per ciascun gruppo. Questo protocollo è una proposta dell’estensore della scheda.

## Record di evidenza per il Model Card Evaluator

Blocco JSON estraibile. `observed` indica un valore letto in un artefatto pubblico, `publisher_reported` un’attribuzione dell’autore o dei suoi metadati, `not_found_in_reviewed_sources` un dato cercato senza riscontro nelle fonti esaminate. `not_run` indica una prova che questa revisione non ha eseguito. Un valore `null` segnala un dato sconosciuto, distinto da un punteggio pari a zero.

```json
{
  "model_id": "DavidAU/Qwen3.8-27B-Ultimate-Heretic-Uncensored",
  "revision": "5d5158cd7f8d76e28bfb3866c664fb0a9f7a593d",
  "review_date": "2026-11-05",
  "subject": "source_bf16_checkpoint",
  "claims": [
    {
      "field": "base_model",
      "value": "Qwen/Qwen3.8-27B",
      "status": "publisher_reported",
      "source": "card"
    },
    {
      "field": "architecture_class",
      "value": "Qwen3_5ForConditionalGeneration",
      "status": "observed",
      "source": "config"
    },
    {
      "field": "max_position_embeddings",
      "value": 262144,
      "status": "observed",
      "source": "config"
    },
    {
      "field": "effective_context_length_tested_by_reviewer",
      "value": null,
      "status": "not_run",
      "source": null
    },
    {
      "field": "publisher_creative_demo",
      "value": "Ultimate 2 Q6",
      "status": "publisher_reported",
      "source": "card"
    },
    {
      "field": "verified_50x_speedup_bf16",
      "value": null,
      "status": "not_found_in_reviewed_sources",
      "source": "card"
    },
    {
      "field": "standardized_benchmark_score_bf16",
      "value": null,
      "status": "not_found_in_reviewed_sources",
      "source": "card"
    },
    {
      "field": "training_energy_kwh",
      "value": null,
      "status": "not_found_in_reviewed_sources",
      "source": "card"
    },
    {
      "field": "independent_inference_run_by_reviewer",
      "value": false,
      "status": "not_run",
      "source": null
    }
  ]
}
```

## Fonti

- [Scheda e dimostrazioni dell’autore, alla revisione esaminata][card]
- [Architettura del checkpoint][config]
- [Configurazione del campionamento][generation]
- [Inventario dei file alla stessa revisione][tree]
- [Scheda upstream di Qwen][base]

[card]: https://huggingface.co/DavidAU/Qwen3.8-27B-Ultimate-Heretic-Uncensored/blob/5d5158cd7f8d76e28bfb3866c664fb0a9f7a593d/README.md
[config]: https://huggingface.co/DavidAU/Qwen3.8-27B-Ultimate-Heretic-Uncensored/blob/5d5158cd7f8d76e28bfb3866c664fb0a9f7a593d/config.json
[generation]: https://huggingface.co/DavidAU/Qwen3.8-27B-Ultimate-Heretic-Uncensored/blob/5d5158cd7f8d76e28bfb3866c664fb0a9f7a593d/generation_config.json
[tree]: https://huggingface.co/DavidAU/Qwen3.8-27B-Ultimate-Heretic-Uncensored/tree/5d5158cd7f8d76e28bfb3866c664fb0a9f7a593d
[base]: https://huggingface.co/Qwen/Qwen3.8-27B
