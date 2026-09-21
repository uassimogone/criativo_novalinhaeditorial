from src.history_manager import carregar, salvar
from src.researcher import RadarEditorial
from src.telegram_bot import enviar_pautas

def main():
    historico = carregar()
    radar = RadarEditorial()
    pautas = radar.pesquisar(historico)

    if not pautas:
        print("Nenhuma pauta qualificada encontrada.")
        return

    enviar_pautas(pautas)
    salvar(pautas)
    print(f"{len(pautas)} pautas enviadas e registradas.")

if __name__ == "__main__":
    main()
