from src.history_manager import carregar, salvar
from src.researcher import RadarEditorial
from src.telegram_bot import enviar_pautas, enviar_mensagem

def main():
    historico = carregar()
    radar = RadarEditorial()

    try:
        pautas = radar.pesquisar(historico)
    except Exception as exc:
        mensagem = f"RADAR EDITORIAL — ERRO NA PESQUISA\n\n{type(exc).__name__}: {exc}"
        print(mensagem)
        # Se o Telegram estiver configurado corretamente, o diagnóstico chega por lá.
        enviar_mensagem(mensagem)
        raise

    if not pautas:
        mensagem = (
            "RADAR EDITORIAL — EXECUÇÃO CONCLUÍDA\n\n"
            "Nenhuma pauta atingiu os critérios editoriais nesta execução."
        )
        print(mensagem)
        enviar_mensagem(mensagem)
        return

    enviar_pautas(pautas)
    salvar(pautas)
    print(f"{len(pautas)} pautas enviadas e registradas.")

if __name__ == "__main__":
    main()
