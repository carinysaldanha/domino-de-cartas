import os
from .carta import Carta, Valores, Naipe
from .entidades import Mesa, ORDEM_NAIPE
from itertools import zip_longest

RED = "\033[31m"
RESET = "\033[0m"

def cor_do_naipe(naipe):
    return RED if naipe in [Naipe.COPAS, Naipe.OUROS] else ""

def gerar_bloco_vazio(linhas):
    return [
        "           "
    ]

def gerar_lateral_esquerda(carta: Carta):
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
        "╭──", f"│{cor}{valor:>2}{RESET}", "│  ", "│  ", "│  ", f"│{cor}{naipe:>2}{RESET}", "╰──"
    ]

def gerar_lateral_direita(carta: Carta):
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
        "──╮", f"{cor}{valor:2}{RESET}│", "  │", "  │", "  │", f"{cor}{naipe:2}{RESET}│", "──╯"
    ]
def gerar_parcial_superior(carta: Carta):
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
        "╭─────────╮",
        f"│{cor}{valor:>2}     {naipe:<2}{RESET}│",    
    ]

def gerar_parcial_inferior(carta: Carta):
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
         f"│{cor}{naipe:>2}     {valor:<2}{RESET}│",
        "╰─────────╯"  
    ]

def gerar_carta_inteira(carta: Carta):
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
        "╭─────────╮",
        f"│{cor}{valor:>2}     {naipe:<2}{RESET}│",
        "│         │",
        f"│    {cor}{naipe}{RESET}    │",
        "│         │",
        f"│{cor}{naipe:>2}     {valor:<2}{RESET}│",
        "╰─────────╯"
    ]

def gerar_espaco_carta():
    return [
        "╭─  ───  ─╮",
        "           ",
        "│         │",
        "           ",
        "│         │",
        "           ",
        "╰─  ───  ─╯"
    ]

def imprime_mao_jogador(mao: list[Carta]):
    if not mao:
        print("\nSua mão está vazia! (0 cartas)\n")
        return

    linhas_mao = [[] for _ in range(7)]
    for carta in mao[:-1]:
        lateral = gerar_lateral_esquerda(carta)
        for i in range(7):
            linhas_mao[i].append(lateral[i])
    inteira = gerar_carta_inteira(mao[-1])
    for i in range(7):
        linhas_mao[i].append(inteira[i])

    for linha in linhas_mao:
        print("".join(linha))
    
    print(f"SUA MÃO: {len(mao)} cartas")

def buscar_carta(pilha, valor):
    if valor == Valores.SETE:
        return pilha['central']
    for carta in pilha['acima'] + pilha['abaixo']:
        if carta.valor == valor:
            return carta
    return None

def gerar_pilha_completa(pilha: dict, naipe: Naipe):
    valores_ordem = [
        Valores.REI, Valores.DAMA, Valores.VALETE, Valores.DEZ, Valores.NOVE, Valores.OITO,
        Valores.SETE,
        Valores.SEIS, Valores.CINCO, Valores.QUATRO, Valores.TRES, Valores.DOIS, Valores.AS
    ]

    def buscar_carta(valor):
        if valor == Valores.SETE:
            return pilha['central']
        for carta in pilha['acima'] + pilha['abaixo']:
            if carta.valor == valor:
                return carta
        return None

    linhas = []

    for valor in valores_ordem:
        carta = buscar_carta(valor)
        if carta:
            if valor == Valores.SETE:
                linhas.extend(gerar_carta_inteira(carta))
            elif valor.value > 7:
                linhas.extend(gerar_parcial_superior(carta))
            else:
                linhas.extend(gerar_parcial_inferior(carta))

    return linhas

def imprime_mesa(mesa: Mesa): 
    colunas = []
    for idx, naipe in enumerate(ORDEM_NAIPE):
        pilha = mesa.pilhas[naipe]

        if pilha['central'] is None:
            coluna = gerar_espaco_carta()
        else:
            coluna = gerar_pilha_completa(pilha, naipe)

        colunas.append(coluna)
    
    linhas = list(zip_longest(*colunas, fillvalue=" " * 11))
    
    for linha in linhas:
        print("  ".join(linha))

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def imprime_bots(bots):
    for bot in bots:
        quantidade = len(bot.mao)
        miniatura = '🂠 ' * quantidade
        print(f"{bot.nome}: {miniatura} ({quantidade} cartas)")

def imprime_estado(mesa, jogador, bots):
    limpar_tela()
    imprime_mesa(mesa)
    imprime_bots(bots)
    imprime_mao_jogador(jogador.mao)
