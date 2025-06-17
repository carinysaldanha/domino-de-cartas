import threading  # Trabalhar com múltiplas threads (execução paralela)
import time       # Funções relacionadas a tempo e pausas

from .entidades import Baralho, Mesa  # Cartas e estado da mesa do jogo
from .jogador import Jogador          # Jogador humano
from .bot import Bot                  # Jogadores controlados pelo computador (bots)
from .visual import imprime_estado, cor_do_naipe, RESET  # Exibir o estado do jogo com cores no terminal

class Jogo:
    def __init__(self):
        # Cria o baralho e a mesa do jogo
        self.baralho = Baralho()
        self.mesa = Mesa()

        # Cria 4 jogadores: 1 humano e 3 bots
        self.jogadores = [
            Jogador("Você"),
            Bot("Bot 1"),
            Bot("Bot 2"),
            Bot("Bot 3")
        ]

        self.turno = 0  # Controla de quem é a vez (índice do jogador)
        self.lock = threading.Semaphore(1)  # Controle de acesso para evitar conflitos na saída
        self.turno_cond = threading.Condition()  # Condição para controlar a passagem da vez entre threads
        self.jogo_ativo = True  # Flag para indicar se o jogo está ativo ou terminou

    def distribuir_cartas(self):
        # Embaralha o baralho e distribui cartas igualmente entre os 4 jogadores
        self.baralho.embaralhar()
        maos = self.baralho.distribuir(jogadores=4)
        for i, jogador in enumerate(self.jogadores):
            jogador.receber_cartas(maos[i])

    def executar_turno(self, id_jogador):
        # Função que cada thread executa, representando o turno de cada jogador
        while self.jogo_ativo:
            with self.turno_cond:
                # Espera até que seja o turno deste jogador ou o jogo acabar
                self.turno_cond.wait_for(lambda: self.turno == id_jogador or not self.jogo_ativo)

                if not self.jogo_ativo:
                    # Se o jogo acabou, sai do loop e termina a thread
                    break

                self.lock.acquire()  # Garante que só uma thread escreva no console por vez

                jogador_atual = self.jogadores[id_jogador]  # Pega o jogador atual
                # O jogador tenta jogar uma carta na mesa (humano ou bot)
                jogada = jogador_atual.jogar(self.mesa, self, self.jogadores[1:])
                
                # Atualiza a tela do jogo mostrando o estado atual
                imprime_estado(self.mesa, self.jogadores[0], self.jogadores[1:])
                
                self.lock.release()  # Libera o acesso para outra thread escrever

                if jogada:
                    # Se o jogador jogou uma carta, imprime qual carta foi jogada com cor
                    cor = cor_do_naipe(jogada.naipe)
                    print(f"{jogador_atual.nome} jogou {cor}{jogada.valor.name}{RESET} de {cor}{jogada.naipe.value}{RESET}")
                else:
                    # Se passou a vez (não jogou carta), imprime mensagem
                    print(f"{jogador_atual.nome} passou a vez.")

                # Passa o turno para o próximo jogador (0 a 3, em loop)
                self.turno = (self.turno + 1) % 4
                self.turno_cond.notify_all()  # Notifica todas as threads que o turno mudou

                time.sleep(0.1)  # Pequena pausa para evitar execução muito rápida

    def iniciar(self):
        # Inicia o jogo: distribui as cartas e começa as threads para os turnos dos jogadores
        self.distribuir_cartas()
        # Imprime o estado inicial da mesa e das mãos
        imprime_estado(self.mesa, self.jogadores[0], self.jogadores[1:])

        threads = []
        # Cria e inicia uma thread para cada jogador, rodando executar_turno
        for id_jogador in range(4):
            t = threading.Thread(target=self.executar_turno, args=(id_jogador,))
            threads.append(t)
            t.start()

        # Aguarda todas as threads terminarem antes de continuar
        for t in threads:
            t.join()

    def verificar_fim_de_jogo(self):
        # Verifica se o jogo terminou (algum jogador ficou sem cartas)
        with self.turno_cond:
            if len(self.jogadores[0].mao) == 0:
                # Jogador humano venceu
                self.jogo_ativo = False  
                self.resultado = "vitoria"
                self.turno_cond.notify_all()  # Notifica threads para saírem do wait
            elif any(len(bot.mao) == 0 for bot in self.jogadores[1:]):
                # Algum bot venceu, jogador humano perdeu
                self.jogo_ativo = False
                self.resultado = "derrota"
                self.turno_cond.notify_all()  # Notifica threads para saírem do wait
