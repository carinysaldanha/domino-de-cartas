import threading
import time
from .entidades import Baralho, Mesa
from .jogador import Jogador
from .bot import Bot
from .visual import imprime_estado, cor_do_naipe, RESET

class Jogo:
    def __init__(self):
        self.baralho = Baralho()
        self.mesa = Mesa()
        self.jogadores = [
            Jogador("Você"),
            Bot("Bot 1"),
            Bot("Bot 2"),
            Bot("Bot 3")
        ]
        self.turno = 0
        self.lock = threading.Semaphore(1)
        self.turno_cond = threading.Condition()
        self.jogo_ativo = True

    def distribuir_cartas(self):
        self.baralho.embaralhar()
        maos = self.baralho.distribuir(jogadores=4)
        for i, jogador in enumerate(self.jogadores):
            jogador.receber_cartas(maos[i])

    def executar_turno(self, id_jogador):
        while self.jogo_ativo:
            with self.turno_cond:
                self.turno_cond.wait_for(lambda: self.turno == id_jogador or not self.jogo_ativo)

                if not self.jogo_ativo:
                    break

                self.lock.acquire()
                jogador_atual = self.jogadores[id_jogador]
                jogada = jogador_atual.jogar(self.mesa, self, self.jogadores[1:])
                imprime_estado(self.mesa, self.jogadores[0], self.jogadores[1:])
                self.lock.release()

                if jogada:
                    cor = cor_do_naipe(jogada.naipe)
                    print(f"{jogador_atual.nome} jogou {cor}{jogada.valor.name}{RESET} de {cor}{jogada.naipe.value}{RESET}")
                else:
                    print(f"{jogador_atual.nome} passou a vez.")

                self.turno = (self.turno + 1) % 4
                self.turno_cond.notify_all()
                time.sleep(0.1)

    def iniciar(self):
        self.distribuir_cartas()
        imprime_estado(self.mesa, self.jogadores[0], self.jogadores[1:])

        threads = []
        for id_jogador in range(4):
            t = threading.Thread(target=self.executar_turno, args=(id_jogador,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def verificar_fim_de_jogo(self):
        with self.turno_cond:
            if len(self.jogadores[0].mao) == 0:
                self.jogo_ativo = False  
                self.resultado = "vitoria"
                self.turno_cond.notify_all()
            elif any(len(bot.mao) == 0 for bot in self.jogadores[1:]):
                self.jogo_ativo = False
                self.resultado = "derrota"
                self.turno_cond.notify_all()
