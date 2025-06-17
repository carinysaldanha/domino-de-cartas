import random #Importa o módulo padrão do Python chamado
from .carta import Carta, Naipe, Valores#Importa três itens do módulo,nipe, carta e valor

ORDEM_NAIPE = [Naipe.ESPADAS, Naipe.COPAS, Naipe.PAUS, Naipe.OUROS]

class Baralho: #cria um baralho completo com 52 cartas e conbina os valores com cada naipe
    def __init__(self):
        self.cartas = [Carta(valor, naipe) for naipe in Naipe for valor in Valores]

    def embaralhar(self):# embaralha as cartas aleatoriamente 
        random.shuffle(self.cartas)
 
    def distribuir(self, jogadores: int = 4):# distribui as cartas igualmente, exigindo que seja exata, Retorna uma lista de listas:cada sublista representa a mão de um jogador.
        if len(self.cartas) % jogadores != 0:
            raise ValueError("Não é possível dividir igualmente entre os jogadores.")
        tamanho_mao = len(self.cartas) // jogadores
        return [self.cartas[i * tamanho_mao:(i + 1) * tamanho_mao] for i in range(jogadores)]

class Mesa: #Cria uma estrutura de dicionários para cada naipe
    def __init__(self):
        self.pilhas = {naipe: {'acima': [], 'abaixo': [], 'central': None} for naipe in Naipe}
#Um 7 só pode ser jogado se a pilha central estiver vazia para aquele naipe,se sim vira a base da pilha
    def jogar_carta(self, carta: Carta) -> bool:
        pilha = self.pilhas[carta.naipe]

        if carta.valor == Valores.SETE:
            if pilha['central'] is None:
                pilha['central'] = carta
                return True
            return False
#Um 7 só pode ser jogado se a pilha central estiver vazia para aquele naipe
        if pilha['central'] is None:
            return False
#jogar uma carta acima do 7 ex 8,9,10,11,12,13
        if carta.valor.value > 7:
            topo = pilha['acima'][0].valor.value if pilha['acima'] else 7
            if carta.valor.value == topo + 1:
                pilha['acima'].insert(0, carta)
                return True
                #jogar as cartas abaixo do 7 ex 6,,5,4,3,2,1
        elif carta.valor.value < 7:
            fundo = pilha['abaixo'][-1].valor.value if pilha['abaixo'] else 7
            if carta.valor.value == fundo - 1:
                pilha['abaixo'].append(carta)
                return True
#A carta não pôde ser colocada em nenhuma posição válida.
        return False
