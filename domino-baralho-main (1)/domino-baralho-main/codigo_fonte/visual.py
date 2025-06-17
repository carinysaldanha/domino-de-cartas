import os  # Para operações do sistema, como limpar a tela do terminal
from .carta import Carta, Valores, Naipe  # Importa classes que representam as cartas, seus valores e naipes
from .entidades import Mesa, ORDEM_NAIPE  # Importa a classe Mesa (estado do jogo) e ordem dos naipes para exibição
from itertools import zip_longest  # Função para combinar listas de tamanhos diferentes, usada para imprimir colunas alinhadas

RED = "\033[31m"    # Código ANSI para cor vermelha no terminal
RESET = "\033[0m"   # Código ANSI para resetar cor do texto

def cor_do_naipe(naipe):
    # Retorna vermelho se o naipe for COPAS ou OUROS, senão texto normal
    return RED if naipe in [Naipe.COPAS, Naipe.OUROS] else ""

def gerar_bloco_vazio(linhas):
    # Retorna uma linha em branco para espaçamento visual
    return [
        "           "
    ]

def gerar_lateral_esquerda(carta: Carta):
    # Gera representação da lateral esquerda da carta (parte do desenho em texto)
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
        "╭──", f"│{cor}{valor:>2}{RESET}", "│  ", "│  ", "│  ", f"│{cor}{naipe:>2}{RESET}", "╰──"
    ]

def gerar_lateral_direita(carta: Carta):
    # Gera representação da lateral direita da carta
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
        "──╮", f"{cor}{valor:2}{RESET}│", "  │", "  │", "  │", f"{cor}{naipe:2}{RESET}│", "──╯"
    ]

def gerar_parcial_superior(carta: Carta):
    # Gera parte superior da carta para montagem em pilha (cartas acima do 7)
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
        "╭─────────╮",
        f"│{cor}{valor:>2}     {naipe:<2}{RESET}│",    
    ]

def gerar_parcial_inferior(carta: Carta):
    # Gera parte inferior da carta para montagem em pilha (cartas abaixo do 7)
    cor = cor_do_naipe(carta.naipe)
    valor = carta.valor_str()
    naipe = carta.naipe.value
    return [
         f"│{cor}{naipe:>2}     {valor:<2}{RESET}│",
        "╰─────────╯"  
    ]

def gerar_carta_inteira(carta: Carta):
    # Gera representação completa da carta (ex: na mão do jogador)
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
    # Gera espaço vazio para cartas não jogadas (visualização da mesa)
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
    # Exibe as cartas na mão do jogador em formato gráfico no terminal
    if not mao:
        print("\nSua mão está vazia! (0 cartas)\n")
        return

    linhas_mao = [[] for _ in range(7)]  # Cria 7 linhas para construir as cartas em ASCII
    for carta in mao[:-1]:
        lateral = gerar_lateral_esquerda(carta)  # Gera lateral esquerda para todas menos última carta
        for i in range(7):
            linhas_mao[i].append(lateral[i])
    inteira = gerar_carta_inteira(mao[-1])     # Última carta é desenhada completa
    for i in range(7):
        linhas_mao[i].append(inteira[i])

    for linha in linhas_mao:
        print("".join(linha))  # Imprime linhas concatenadas das cartas

    print(f"SUA MÃO: {len(mao)} cartas")  # Mostra quantidade de cartas na mão

def buscar_carta(pilha, valor):
    # Procura uma carta específica na pilha (central, acima ou abaixo do 7)
    if valor == Valores.SETE:
        return pilha['central']
    for carta in pilha['acima'] + pilha['abaixo']:
        if carta.valor == valor:
            return carta
    return None

def gerar_pilha_completa(pilha: dict, naipe: Naipe):
    # Gera visualização completa da pilha de um naipe, montando as cartas na ordem correta
    valores_ordem = [
        Valores.REI, Valores.DAMA, Valores.VALETE, Valores.DEZ, Valores.NOVE, Valores.OITO,
        Valores.SETE,
        Valores.SEIS, Valores.CINCO, Valores.QUATRO, Valores.TRES, Valores.DOIS, Valores.AS
    ]

    def buscar_carta(valor):
        # Função interna para buscar carta na pilha
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
                linhas.extend(gerar_carta_inteira(carta))          # 7 é carta completa
            elif valor.value > 7:
                linhas.extend(gerar_parcial_superior(carta))       # Cartas acima do 7, parte superior
            else:
                linhas.extend(gerar_parcial_inferior(carta))       # Cartas abaixo do 7, parte inferior

    return linhas

def imprime_mesa(mesa: Mesa): 
    # Imprime o estado atual da mesa com todas as pilhas de cartas
    colunas = []
    for idx, naipe in enumerate(ORDEM_NAIPE):
        pilha = mesa.pilhas[naipe]

        if pilha['central'] is None:
            coluna = gerar_espaco_carta()   # Espaço vazio se nenhuma carta no centro
        else:
            coluna = gerar_pilha_completa(pilha, naipe)  # Pilha completa com cartas visíveis

        colunas.append(coluna)
    
    linhas = list(zip_longest(*colunas, fillvalue=" " * 11))  # Alinha colunas lado a lado
    
    for linha in linhas:
        print("  ".join(linha))  # Imprime linha da mesa com todas as pilhas

def limpar_tela():
    # Limpa a tela do terminal (funciona no Windows e Unix)
    os.system("cls" if os.name == "nt" else "clear")

def imprime_bots(bots):
    # Imprime os bots com quantidade de cartas e miniaturas (cartas viradas)
    for bot in bots:
        quantidade = len(bot.mao)
        miniatura = '🂠 ' * quantidade
        print(f"{bot.nome}: {miniatura} ({quantidade} cartas)")

def imprime_estado(mesa, jogador, bots):
    # Função principal para imprimir todo o estado do jogo (mesa + bots + jogador)
    limpar_tela()
    imprime_mesa(mesa)
    imprime_bots(bots)
    imprime_mao_jogador(jogador.mao)
