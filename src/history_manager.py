import json
from pathlib import Path

ARQUIVO = Path("data/historico_pautas.json")

def carregar():
    if not ARQUIVO.exists():
        return []
    try:
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except Exception:
        return []

def salvar(pautas):
    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    atual = carregar()
    for p in pautas:
        atual.append({
            "titulo": p.get("titulo", ""),
            "url": p.get("url", ""),
            "tema": p.get("tema", "")
        })
    ARQUIVO.write_text(json.dumps(atual[-200:], ensure_ascii=False, indent=2), encoding="utf-8")
