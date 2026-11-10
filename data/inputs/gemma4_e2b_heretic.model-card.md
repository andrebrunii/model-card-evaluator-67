---
base_model: google/gemma-4-E2B-it
base_model_relation: quantized-derivative
format: gguf
quantization: Q4_K_M
tags:
  - gemma4
  - heretic
  - abliterated
  - uncensored
---

# Model card · Gemma-4-E2B-Heretic (GGUF Q4_K_M)

**Identificativo Ollama** `hf.co/DuoNeural/Gemma-4-E2B-Heretic-GGUF:Q4_K_M`
**Checkpoint di origine** `google/gemma-4-E2B-it` (Google DeepMind, Apache 2.0)
**Publisher del derivato** DuoNeural (Hugging Face)
**Tipo** scheda indipendente in italiano, redatta per il confronto CBRA. Le affermazioni del publisher vanno verificate sulla pagina del repository.

## Identità e modifica applicata

Derivato del modello instruction-tuned Gemma 4 E2B ottenuto tramite *abliteration* (ablazione direzionale / ortogonalizzazione dei pesi), con pipeline ispirata a Heretic. La modifica individua la direzione di rifiuto nel residual stream e la rimuove dalle matrici di output di attenzione (`o_proj`) e MLP (`down_proj`). Non è un fine-tune su nuovi dati: architettura, tokenizer e chat template restano quelli del modello base.

## Comportamento di sicurezza dichiarato

- **Rifiuti:** il comportamento di rifiuto del modello base è rimosso o fortemente ridotto per progetto (modello *uncensored*).
- **Allineamento:** nessun livello di sicurezza aggiuntivo. Le policy di Google per Gemma non sono più applicate dal modello stesso.
- **Validazione:** il publisher non documenta valutazioni di sicurezza, red-teaming o controlli per l'uso con strumenti esterni (function calling) o per azioni autonome.

## Specifiche tecniche

| Campo | Valore |
|---|---|
| Parametri | Circa 5B totali (2B effettivi, architettura E2B con embedding per-layer) |
| Formato | GGUF, quantizzazione Q4_K_M, circa 3,4 GB su disco |
| Contesto | Fino a 128.000 token (ereditato dal modello base) |
| Modalità | Testo in ingresso/uscita in Ollama. Il supporto multimodale dipende dalla conversione GGUF |
| Function calling | Ereditato dal template del modello base, non validato sul derivato |

## Uso previsto e limiti

Ricerca su interpretabilità e valutazione comparativa della sicurezza rispetto al modello base (`gemma4:e2b`), mantenendo costanti prompt, parametri e criteri di giudizio. Non adatto a deployment in produzione, a utenti finali o a contesti con accesso a strumenti di sistema, messaggistica o dati sensibili senza controlli esterni (guardrail, filtri di input/output, supervisione umana).

La rimozione dei rifiuti può alterare la qualità delle risposte (divergenza KL rispetto al modello base). Le prestazioni sui benchmark del modello base non sono automaticamente trasferibili al derivato.
