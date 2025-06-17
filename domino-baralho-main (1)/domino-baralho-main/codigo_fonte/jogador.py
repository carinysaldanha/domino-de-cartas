from .carta import Valores, Carta
from .visual import cor_do_naipe, RESET, limpar_tela, imprime_estado
from .entidades import ORDEM_NAIPE

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = [] 

    def receber_cartas(self, cartas):
        self.mao.extend(cartas)
        self.organizar_mao()

    def organizar_mao(self):
        self.mao.sort(key=lambda carta: (ORDEM_NAIPE.index(carta.naipe), -carta.valor.value))
        
    def tem_jogada_valida(self, mesa):
        for carta in self.mao:
            pilha = mesa.pilhas[carta.naipe]
            centro = pilha['central']

            if centro is None:
                if carta.valor.value == 7:
                    return True
            else:
                if carta.valor.value > 7:
                    topo = pilha['acima'][0].valor.value if pilha['acima'] else 7
                    if carta.valor.value == topo + 1:
                        return True
                elif carta.valor.value < 7:
                    fundo = pilha['abaixo'][-1].valor.value if pilha['abaixo'] else 7
                    if carta.valor.value == fundo - 1:
                        return True
        return False

    def jogar(self, mesa, jogo, bots):
        while True:
            try:
                opcoes = []
                print("\nDigite 0 para passar a vez.")
                for idx, naipe in enumerate(ORDEM_NAIPE):
                    cor = cor_do_naipe(naipe)
                    opcao = f"{idx+1} {cor}{naipe.value}{RESET} {naipe.name} {cor}{naipe.value}{RESET}"
                    opcoes.append(opcao)

                print(" | ".join(opcoes))

                escolha = int(input("Naipe: "))

                if escolha == 99:
                    print("⚠ Debug: Forçando fim de jogo manualmente.")
                    self.mao.clear()
                    return None

                if escolha == 0:
                    if self.tem_jogada_valida(mesa):
                        raise ValueError("Você tem jogadas possíveis! Não pode passar a vez.")
                    print(f"{self.nome} passou a vez.")
                    return None

                if not 1 <= escolha <= 4:
                    raise ValueError()

                naipe_escolhido = ORDEM_NAIPE[escolha - 1]
                valor = int(input("Valor da carta (1-13): "))

                if not 1 <= valor <= 13:
                    raise ValueError()

                valor_enum = Valores(valor)
                carta = Carta(valor_enum, naipe_escolhido)

                if carta not in self.mao:
                    raise ValueError("Você não tem essa carta.")

                pilha = mesa.pilhas[naipe_escolhido]
                if pilha['central'] is None and valor != 7:
                    raise ValueError("Você deve jogar o 7 primeiro nesse naipe.")

                if mesa.jogar_carta(carta):
                    self.mao.remove(carta)
                    self.organizar_mao()
                    jogo.verificar_fim_de_jogo()
                    return carta
                else:
                    raise ValueError("Jogada inválida.")

            except Exception as e:
                limpar_tela()
                imprime_estado(mesa, self, bots)
                print(f"Erro: {e}")
