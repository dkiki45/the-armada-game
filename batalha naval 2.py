import random  # usado para gerar coordenadas aleatórias no modo computador
import time  # usado para o delay do jogo
from colorama import init, Fore, Style  # Biblioteca de Cor

init(autoreset=True)

# Constantes Globais
TAMANHO = 10  # Tabuleiro (10x10)
AGUA = " ~ "
TIRO_AGUA = Fore.BLUE + " o " + Style.RESET_ALL
TIRO_ACERTO = Fore.RED + " X " + Style.RESET_ALL
NAVIO = Fore.GREEN + " N " + Style.RESET_ALL

# Dicionário dos navios com seus respectivos tamanhos
NAVIOS = {
    "Encouraçado": 5,
    "Porta-Aviões": 4,
    "Contratorpedeiro1": 3,
    "Contratorpedeiro2": 3,
    "Submarino1": 2,
    "Submarino2": 2
}


def menu_inicial():
    print("=" * 40)
    print(" " * 10 + "BATALHA NAVAL")
    print("=" * 40)
    print("1 - Jogador vs Computador")
    print("2 - Jogador vs Jogador")
    modo = input("Escolha o modo (1 ou 2): ")

    while modo not in ["1", "2"]:
        modo = input("Entrada inválida. Escolha 1 ou 2: ")
    return int(modo)


def configurar_tabuleiro():
    tabuleiro = []
    for linha in range(TAMANHO):
        linha_atual = []
        for coluna in range(TAMANHO):
            linha_atual.append(AGUA)
        tabuleiro.append(linha_atual)
    return tabuleiro


def mostrar_tabuleiro(tabuleiro, ocultar=False):
    print("   " + " ".join([f"{chr(65 + i):2}" for i in range(TAMANHO)]))
    for i, linha in enumerate(tabuleiro):
        linha_formatada = ""
        for celula in linha:
            if ocultar and celula == NAVIO:
                linha_formatada += AGUA
            else:
                linha_formatada += celula
        print(f"{i:2} {linha_formatada}")


def pode_posicionar(tabuleiro, linha, coluna, tamanho, orientacao):
    for i in range(tamanho):
        if orientacao == "V":
            r = linha + i
            c = coluna
        elif orientacao == "H":
            r = linha
            c = coluna + i
        else:
            return False

        if r >= TAMANHO or c >= TAMANHO or tabuleiro[r][c] != AGUA:
            return False
    return True


def posicionar_navios(tabuleiro, manual=True):
    print("\n--- Posicionando Navios ---")

    for nome, tamanho in NAVIOS.items():
        posicionado = False

        while not posicionado:
            if manual:
                print(f"\nNavio: {nome} (tamanho {tamanho})")
                try:
                    linha_str = input("Linha inicial (0 a 9): ").strip()
                    coluna_str = input("Coluna inicial (A a J): ").strip().upper()
                    orientacao = input("Orientação (H ou V): ").strip().upper()

                    if not linha_str.isdigit():
                        raise ValueError("Linha deve ser um número inteiro.")

                    if len(coluna_str) != 1 or not coluna_str.isalpha() or not 'A' <= coluna_str <= 'J':
                        raise ValueError("Coluna inválida. Use letras de A a J.")

                    linha = int(linha_str)
                    coluna = ord(coluna_str) - 65

                    if not (0 <= linha < TAMANHO):
                        raise ValueError("Coordenadas fora do tabuleiro.")

                    if orientacao not in ["H", "V"]:
                        raise ValueError("Orientação inválida.")

                except ValueError as e:
                    print(f"Erro: {e}")
                    continue

            else:
                linha = random.randint(0, TAMANHO - 1)
                coluna = random.randint(0, TAMANHO - 1)
                orientacao = random.choice(["H", "V"])

            if pode_posicionar(tabuleiro, linha, coluna, tamanho, orientacao):
                for i in range(tamanho):
                    if orientacao == "H":
                        tabuleiro[linha][coluna + i] = NAVIO
                    else:
                        tabuleiro[linha + i][coluna] = NAVIO
                posicionado = True
                if manual:
                    mostrar_tabuleiro(tabuleiro)
            else:
                if manual:
                    print("Não é possível posicionar aqui. Tente novamente.")


def realizar_ataque(tabuleiro, linha, coluna):
    if linha < 0 or linha >= TAMANHO or coluna < 0 or coluna >= TAMANHO:
        print("Coordenada fora do tabuleiro.")
        return None

    alvo = tabuleiro[linha][coluna]

    if alvo == TIRO_AGUA or alvo == TIRO_ACERTO:
        print("Essa posição já foi atacada.")
        return None

    if alvo == NAVIO:
        tabuleiro[linha][coluna] = TIRO_ACERTO
        print("ACERTOU UM NAVIO!")
        return True
    else:
        tabuleiro[linha][coluna] = TIRO_AGUA
        print("ÁGUA!")
        return False

#Modo jogador vs maquina
def jogo_vs_computador():
    tab_jogador = configurar_tabuleiro()
    tab_computador = configurar_tabuleiro()

    print("\nSeu tabuleiro inicial:")
    mostrar_tabuleiro(tab_jogador)

    posicionar_navios(tab_jogador, manual=True)
    posicionar_navios(tab_computador, manual=False)

    turno_jogador = True
    vencedor = None

    ataques_computador = set()

    while vencedor is None:
        if turno_jogador:
            print("\nSua vez de atacar!")
            mostrar_tabuleiro(tab_computador, ocultar=True)

            linha_str = input("Linha de ataque (0-9): ")
            coluna_str = input("Coluna de ataque (A a J): ").upper()

            if not linha_str.isdigit() or len(coluna_str) != 1 or not coluna_str.isalpha() or not 'A' <= coluna_str <= 'J':
                print("Entrada inválida. Tente novamente.")
                continue

            linha = int(linha_str)
            coluna = ord(coluna_str) - 65

            resultado = realizar_ataque(tab_computador, linha, coluna)
            if resultado is None:
                continue

        else:
            print("\n Turno do computador...")
            time.sleep(1)
            linha, coluna = random.randint(0, 9), random.randint(0, 9)
            while (linha, coluna) in ataques_computador:
                linha, coluna = random.randint(0, 9), random.randint(0, 9)
            ataques_computador.add((linha, coluna))

            print(f"Computador atacando ({linha}, {coluna})...")
            time.sleep(1)
            realizar_ataque(tab_jogador, linha, coluna)

        if not any(NAVIO in linha for linha in tab_computador):
            vencedor = "Jogador"
        elif not any(NAVIO in linha for linha in tab_jogador):
            vencedor = "Computador"
        else:
            turno_jogador = not turno_jogador

    print(f"\n Fim de jogo! Vencedor: {vencedor}")


# Modo PvP 
def jogo_pvp():
    print("\n=== Jogador vs Jogador ===\n")

    tab_jogador1 = configurar_tabuleiro()
    tab_jogador2 = configurar_tabuleiro()

    print("\nJogador 1, posicione seus navios:")
    posicionar_navios(tab_jogador1, manual=True)
    print("\n" * 50)
    print("\nJogador 2, posicione seus navios:")
    posicionar_navios(tab_jogador2, manual=True)
    print("\n" * 50)

    turno_jogador1 = True
    vencedor = None

    while vencedor is None:
        if turno_jogador1:
            print("\nJogador 1, sua vez de atacar!")
            mostrar_tabuleiro(tab_jogador2, ocultar=True)
            tab_ataque = tab_jogador2
        else:
            print("\nJogador 2, sua vez de atacar!")
            mostrar_tabuleiro(tab_jogador1, ocultar=True)
            tab_ataque = tab_jogador1

        linha_str = input("Linha de ataque (0-9): ")
        coluna_str = input("Coluna de ataque (A a J): ").upper()

        if not linha_str.isdigit() or len(coluna_str) != 1 or not coluna_str.isalpha() or not 'A' <= coluna_str <= 'J':
            print("Entrada inválida. Tente novamente.")
            continue

        linha = int(linha_str)
        coluna = ord(coluna_str) - 65

        resultado = realizar_ataque(tab_ataque, linha, coluna)
        if resultado is None:
            continue

        if not any(NAVIO in linha for linha in tab_ataque):
            vencedor = "Jogador 1" if turno_jogador1 else "Jogador 2"
        else:
            turno_jogador1 = not turno_jogador1

    print(f"\nFim de jogo! Vencedor: {vencedor}")


# Chamada principal 
def jogo():
    modo = menu_inicial()
    if modo == 1:
        jogo_vs_computador()
    elif modo == 2:
        jogo_pvp()


if __name__ == "__main__":
    jogo()
