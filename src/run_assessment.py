import json
from evaluator_pipeline import (
    build_or_load_cbra_index,
    evaluate_system,
    BASE_DIR,
    CBRA_DOC_PATH
)
from ollama_logger import LOG_FILE
from history_parser import parse_api_history_for_cbra
from redteam_loader import run_redteam_simulation


def main():
    # 1. Verifica presenza Model Card in data/inputs/
    inputs_dir = BASE_DIR / "data" / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    model_card_file = inputs_dir / "gemma_4_model_card.md"
    if not model_card_file.exists():
        model_card_file = inputs_dir / "model_card_target.json"
        if not model_card_file.exists():
            print(f"[*] Creazione Model Card di fallback in: {model_card_file}")
            sample_mc = {
                "model_name": "gemma4:latest",
                "intended_use": "Assistente multimodale sicuro per generazione testo, codice e ragionamento.",
                "safety_policy": "Rifiuto rigoroso di prompt dannosi, cyber-attacchi, frodi o azioni autonome pericolose.",
                "permissions_declared": "Supporto tool/function calling sotto supervisione."
            }
            with open(model_card_file, "w", encoding="utf-8") as f:
                json.dump(sample_mc, f, indent=2, ensure_ascii=False)

    # 2. Esecuzione Red-Teaming con dataset Hugging Face 'heretic-org/Semantic-Harmful'
    run_redteam_simulation(target_model="gemma4", num_samples=5)

    # 3. Creazione o caricamento Vector Store CBRA con embeddinggemma-2
    cbra_collection = build_or_load_cbra_index(CBRA_DOC_PATH)

    # 4. Calcolo metriche automatiche (Refusal Rate / Jailbreak Rate) e report History
    history_report, redteam_telemetry = parse_api_history_for_cbra(
        LOG_FILE,
        target_model="gemma4",
        max_entries=20
    )

    print("\n--- METRICHE AUTOMATICHE RED-TEAMING CALCOLATE DA PYTHON ---")
    print(redteam_telemetry.model_dump_json(indent=2))
    print("------------------------------------------------------------\n")

    # 5. Valutazione CBRA (Gemma 4 + Calcolo Matematico Python)
    risultato = evaluate_system(
        collection=cbra_collection,
        model_card_path=model_card_file,
        history_report=history_report,
        telemetry=redteam_telemetry
    )

    # 6. Salvataggio e stampa del report finale
    output_report_path = BASE_DIR / "data" / "cbra_final_assessment.json"
    output_json = risultato.model_dump_json(indent=2)

    with open(output_report_path, "w", encoding="utf-8") as f:
        f.write(output_json)

    print("\n=== REPORT FINALE CBRA COMPLETO ===")
    print(output_json)
    print(f"\n[+] Report salvato con successo in: {output_report_path}")


if __name__ == "__main__":
    main()