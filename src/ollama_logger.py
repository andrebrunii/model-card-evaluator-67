import json
from datetime import datetime, timezone
from pathlib import Path
import ollama

BASE_DIR = Path(r"C:\Users\andre\Documents\GitHub_Labs\model-card-evaluator-67")
LOG_FILE = BASE_DIR / "data" / "logs" / "ollama_api_history.jsonl"


def logged_ollama_chat(
    model: str,
    messages: list[dict],
    tools: list = None,
    options: dict = None,
    session_id: str = "default_session",
    **kwargs
) -> dict:
    """
    Wrapper per ollama.chat che esegue la chiamata API e salva
    l'intero contesto di sicurezza (prompt, tool, risposta) in .jsonl
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    chat_kwargs = {"model": model, "messages": messages}
    if tools:
        chat_kwargs["tools"] = tools
    if options:
        chat_kwargs["options"] = options
    chat_kwargs.update(kwargs)

    response = ollama.chat(**chat_kwargs)

    tool_names = []
    if tools:
        for t in tools:
            if isinstance(t, dict) and "function" in t:
                tool_names.append(t["function"].get("name"))
            elif callable(t):
                tool_names.append(t.__name__)

    # Estrazione sicura di tool_calls (compatibile sia con dict che con oggetti Pydantic di ollama)
    msg_obj = response.get("message", {})
    raw_tool_calls = msg_obj.get("tool_calls") or []
    serialized_tool_calls = []
    for tc in raw_tool_calls:
        if hasattr(tc, "model_dump"):
            serialized_tool_calls.append(tc.model_dump())
        elif isinstance(tc, dict):
            serialized_tool_calls.append(tc)
        else:
            serialized_tool_calls.append(str(tc))

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "model": model,
        "messages": messages,
        "tools_exposed": tool_names,
        "tool_calls_triggered": serialized_tool_calls,
        "assistant_response": msg_obj.get("content", "") or "",
        "options": options or {}
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return response