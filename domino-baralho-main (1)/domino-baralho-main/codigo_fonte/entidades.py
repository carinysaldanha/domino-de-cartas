import random
from .carta import Carta, Naipe, Valores

ORDEM_NAIPE = [Naipe.ESPADAS, Naipe.COPAS, Naipe.PAUS, Naipe.OUROS]

class Baralho:
    def __init__(self):
        self.cartas = [Carta(valor, naipe) for naipe in Naipe for valor in Valores]

    def embaralhar(self):
        random.shuffle(self.cartas)
 
    def distribuir(self, jogadores: int = 4):
        if len(self.cartas) % jogadores != 0:
            raise ValueError("Não é possível dividir igualmente entre os jogadores.")
        tamanho_mao = len(self.cartas) // jogadores
        return [self.cartas[i * tamanho_mao:(i + 1) * tamanho_mao] for i in range(jogadores)]

class Mesa:
    def __init__(self):
        self.pilhas = {naipe: {'acima': [], 'abaixo': [], 'central': None} for naipe in Naipe}

    def jogar_carta(self, carta: Carta) -> bool:
        pilha = self.pilhas[carta.naipe]

        if carta.valor == Valores.SETE:
            if pilha['central'] is None:
                pilha['central'] = carta
                return True
            return False

        if pilha['central'] is None:
            return False

        if carta.valor.value > 7:
            topo = pilha['acima'][0].valor.value if pilha['acima'] else 7
            if carta.valor.value == topo + 1:
                pilha['acima'].insert(0, carta)
                return True
        elif carta.valor.value < 7:
            fundo = pilha['abaixo'][-1].valor.value if pilha['abaixo'] else 7
            if carta.valor.value == fundo - 1:
                pilha['abaixo'].append(carta)
                return True

        return False
