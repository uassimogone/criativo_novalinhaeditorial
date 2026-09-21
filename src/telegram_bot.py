import requests
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def enviar_mensagem(texto: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(texto)
        print("Telegram não configurado; pauta exibida apenas no log.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "disable_web_page_preview": True
    }, timeout=20).raise_for_status()

def enviar_pautas(pautas):
    enviar_mensagem("RADAR EDITORIAL — PAUTAS DO DIA\n\nResponda depois com: gostei / não gostei / motivo.")
    for i, p in enumerate(pautas, 1):
        texto = (
            f"PAUTA {i} — {p.get('pilar','')}\n"
            f"Tema: {p.get('tema','')}\n"
            f"Título-base: {p.get('titulo','')}\n"
            f"Por que importa: {p.get('por_que_importa','')}\n"
            f"Ângulo sugerido: {p.get('angulo','')}\n"
            f"Formato: {p.get('formato','')}\n"
            f"Gancho: {p.get('gancho','')}\n"
            f"Nota editorial: {p.get('nota',0)}/10\n"
            f"Validação: {p.get('validacao','AUTOMÁTICA')}\n"
            f"Fonte: {p.get('url','')}"
        )
        enviar_mensagem(texto)
