from .carta import Valores, Carta #Enumeração Usado para criar cartas e validar jogadas
from .visual import cor_do_naipe, RESET, limpar_tela, imprime_estado #texto colorido no teminal lipa a tela, mostra o estado atual do jogo
from .entidades import ORDEM_NAIPE #Lista com a ordem dos naipes no jogo

class Jogador:
    def __init__(self, nome):
        # Inicializa o jogador com um nome e uma mão vazia
        self.nome = nome
        self.mao = [] 

    def receber_cartas(self, cartas):
        # Recebe cartas e as adiciona à mão
        self.mao.extend(cartas)
        self.organizar_mao()  # Organiza a mão após receber

    def organizar_mao(self):
        # Ordena as cartas da mão por ordem de naipe e valor (decrescente)
        self.mao.sort(key=lambda carta: (ORDEM_NAIPE.index(carta.naipe), -carta.valor.value))
        
    def tem_jogada_valida(self, mesa):
        # Verifica se o jogador tem alguma jogada válida na mesa
        for carta in self.mao:
            pilha = mesa.pilhas[carta.naipe]
            centro = pilha['central']

            if centro is None:
                # Se o centro da pilha ainda não tem carta, só o 7 pode ser jogado
                if carta.valor.value == 7:
                    return True
            else:
                if carta.valor.value > 7:
                    # Verifica se pode jogar acima do 7 (8, 9, ...)
                    topo = pilha['acima'][0].valor.value if pilha['acima'] else 7
                    if carta.valor.value == topo + 1:
                        return True
                elif carta.valor.value < 7:
                    # Verifica se pode jogar abaixo do 7 (6, 5, ...)
                    fundo = pilha['abaixo'][-1].valor.value if pilha['abaixo'] else 7
                    if carta.valor.value == fundo - 1:
                        return True
        return False  # Nenhuma jogada válida encontrada

    def jogar(self, mesa, jogo, bots):
        # Executa o turno do jogador humano
        while True:
            try:
                opcoes = []
                print("\nDigite 0 para passar a vez.")  # Instrução para passar

                # Mostra os naipes como opções numeradas
                for idx, naipe in enumerate(ORDEM_NAIPE):
                    cor = cor_do_naipe(naipe)  # Cor personalizada para o naipe
                    opcao = f"{idx+1} {cor}{naipe.value}{RESET} {naipe.name} {cor}{naipe.value}{RESET}"
                    opcoes.append(opcao)

                print(" | ".join(opcoes))  # Mostra as opções

                escolha = int(input("Naipe: "))  # Jogador escolhe um naipe

                if escolha == 99:
                    # Comando secreto de debug para forçar fim de jogo
                    print("⚠ Debug: Forçando fim de jogo manualmente.")
                    self.mao.clear()
                    return None

                if escolha == 0:
                    # Jogador escolheu passar
                    if self.tem_jogada_valida(mesa):
                        # Não pode passar se tiver jogadas válidas
                        raise ValueError("Você tem jogadas possíveis! Não pode passar a vez.")
                    print(f"{self.nome} passou a vez.")
                    return None

                if not 1 <= escolha <= 4:
                    # Entrada inválida para naipe
                    raise ValueError()

                naipe_escolhido = ORDEM_NAIPE[escolha - 1]  # Converte escolha em naipe
                valor = int(input("Valor da carta (1-13): "))  # Jogador escolhe o valor da carta

                if not 1 <= valor <= 13:
                    # Valor fora do intervalo permitido
                    raise ValueError()

                valor_enum = Valores(valor)  # Converte número em enum
                carta = Carta(valor_enum, naipe_escolhido)  # Cria uma instância da carta

                if carta not in self.mao:
                    # Jogador não tem essa carta na mão
                    raise ValueError("Você não tem essa carta.")

                pilha = mesa.pilhas[naipe_escolhido]
                if pilha['central'] is None and valor != 7:
                    # Só o 7 pode ser jogado como a primeira carta de um naipe
                    raise ValueError("Você deve jogar o 7 primeiro nesse naipe.")

                if mesa.jogar_carta(carta):
                    # Jogada válida
                    self.mao.remove(carta)  # Remove carta da mão
                    self.organizar_mao()  # Reorganiza a mão
                    jogo.verificar_fim_de_jogo()  # Verifica se o jogo terminou
                    return carta
                else:
                    # A carta não pôde ser colocada na mesa
                    raise ValueError("Jogada inválida.")

            except Exception as e:
                # Em caso de erro, limpa tela, mostra estado atual e imprime o erro
                limpar_tela()
                imprime_estado(mesa, self, bots)
                print(f"Erro: {e}")
