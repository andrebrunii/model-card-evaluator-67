"""
Confronto CBRA & Red-Teaming: Gemma 4 E2B (allineato) vs Gemma 4 E2B Heretic (abliterated).

Riusa la pipeline di run_assessment2.py (red-teaming, telemetria deterministica,
auditor CBRA, report markdown) cambiando solo i due modelli confrontati.
Stesso modello base, stessa dimensione e quantizzazione simile: la differenza
misurata isola l'effetto dell'abliteration.

Uso (dalla cartella src):
    python run_compare_gemma4_heretic.py
    python run_compare_gemma4_heretic.py --num-prompts 20 --fresh
    python run_compare_gemma4_heretic.py --baseline gemma4 --heretic hf.co/DuoNeural/Gemma-4-E2B-Heretic-GGUF:Q4_K_M
"""
import argparse

import ollama

import run_assessment2 as ra

DEFAULT_BASELINE = "gemma4:e2b"
DEFAULT_HERETIC = "hf.co/DuoNeural/Gemma-4-E2B-Heretic-GGUF:Q4_K_M"
HERETIC_CARD_NAME = "gemma4_e2b_heretic.model-card.md"


def ensure_model_available(model: str) -> None:
    """Scarica il modello in Ollama se non è già presente."""
    try:
        listed = ollama.list()
        models = listed.get("models", []) if isinstance(listed, dict) else getattr(listed, "models", [])
        names = set()
        for m in models:
            name = m.get("model") or m.get("name") if isinstance(m, dict) else getattr(m, "model", None)
            if name:
                names.add(name)
                names.add(name.removesuffix(":latest"))
    except Exception as e:
        raise SystemExit(f"[!] Ollama non raggiungibile ({e}). Avvia l'app Ollama e riprova.")

    if model in names or f"{model}:latest" in names:
        print(f"[+] Modello presente in Ollama: {model}")
        return
    print(f"[*] Modello '{model}' non trovato, download in corso (ollama pull)...")
    ollama.pull(model)
    print(f"[+] Download completato: {model}")


def resolve_heretic_card(inputs_dir):
    card = inputs_dir / HERETIC_CARD_NAME
    if not card.exists():
        raise SystemExit(f"[!] Model card del modello heretic non trovata: {card}")
    return card


def main():
    parser = argparse.ArgumentParser(description="Confronto CBRA gemma4 vs gemma4 heretic")
    parser.add_argument("--baseline", default=DEFAULT_BASELINE, help="Modello Ollama allineato (baseline)")
    parser.add_argument("--heretic", default=DEFAULT_HERETIC, help="Modello Ollama abliterated (sfidante)")
    parser.add_argument("--num-prompts", type=int, default=20, help="Numero di prompt Semantic-Harmful da testare")
    parser.add_argument("--fresh", action="store_true",
                        help="Riesegue sempre il red-teaming anche se esistono già log per i modelli")
    args = parser.parse_args()

    # La pipeline legge NUM_PROMPTS come globale per l'intestazione del report
    ra.NUM_PROMPTS = args.num_prompts

    inputs_dir = ra.BASE_DIR / "data" / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    card_baseline = ra.resolve_gemma_model_card(inputs_dir)
    card_heretic = resolve_heretic_card(inputs_dir)

    for model_id in (args.baseline, args.heretic, ra.EVAL_MODEL):
        ensure_model_available(model_id)

    # 1. Red-teaming (stessi prompt, stessi tool esposti, stessa temperatura)
    for model_id in (args.baseline, args.heretic):
        existing = ra.count_model_logs(ra.LOG_FILE, target_model=model_id)
        if args.fresh or existing < args.num_prompts:
            ra.run_redteam_simulation(target_model=model_id, num_samples=args.num_prompts)
        else:
            print(f"[+] Trovati già {existing} log per '{model_id}', uso gli ultimi {args.num_prompts}.")

    # 2. Indice CBRA (ChromaDB + embeddinggemma-2)
    cbra_collection = ra.build_or_load_cbra_index(ra.CBRA_DOC_PATH)

    # 3. Valutazione dei due modelli con lo stesso auditor
    reports = {}
    for model_id, card in ((args.baseline, card_baseline), (args.heretic, card_heretic)):
        history, telemetry = ra.parse_api_history_for_cbra(
            ra.LOG_FILE, target_model=model_id, max_entries=args.num_prompts
        )
        reports[model_id] = ra.evaluate_system(
            collection=cbra_collection,
            model_card_path=card,
            history_report=history,
            telemetry=telemetry,
            target_model_name=model_id,
        )

    # 4. Salvataggio JSON
    data_dir = ra.BASE_DIR / "data"
    baseline_json = data_dir / "cbra_assessment_gemma4_e2b.json"
    heretic_json = data_dir / "cbra_assessment_gemma4_e2b_heretic.json"
    baseline_json.write_text(reports[args.baseline].model_dump_json(indent=2), encoding="utf-8")
    heretic_json.write_text(reports[args.heretic].model_dump_json(indent=2), encoding="utf-8")

    # 5. Report markdown comparativo
    md_content = ra.generate_markdown_comparison(
        rep_a=reports[args.baseline],
        rep_b=reports[args.heretic],
        card_a=card_baseline,
        card_b=card_heretic,
        entries_a=ra.get_recent_model_entries(ra.LOG_FILE, args.baseline, max_entries=args.num_prompts),
        entries_b=ra.get_recent_model_entries(ra.LOG_FILE, args.heretic, max_entries=args.num_prompts),
    )
    md_path = data_dir / "cbra_comparison_gemma4_vs_heretic.md"
    md_path.write_text(md_content, encoding="utf-8")

    print("\n" + "=" * 70)
    print("[+] COMPARAZIONE GEMMA 4 vs GEMMA 4 HERETIC COMPLETATA")
    print(f"[+] JSON baseline: {baseline_json}")
    print(f"[+] JSON heretic:  {heretic_json}")
    print(f"[+] REPORT:        {md_path}")
    print("=" * 70 + "\n")
    print(md_content)


if __name__ == "__main__":
    main()
