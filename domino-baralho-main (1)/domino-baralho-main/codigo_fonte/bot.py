from .carta import Valores
import time
import random

class Bot:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []

    def receber_cartas(self, cartas):
        self.mao.extend(cartas)

    def jogar(self, mesa, jogo, bots = None):
        time.sleep(random.uniform(0.5, 1.0)) 

        for carta in self.mao:
            if carta.valor == Valores.SETE:
                if mesa.jogar_carta(carta):
                    self.mao.remove(carta)
                    jogo.verificar_fim_de_jogo()
                    return carta

        for carta in self.mao:
            if mesa.jogar_carta(carta):
                self.mao.remove(carta)
                jogo.verificar_fim_de_jogo()
                return carta

        jogo.verificar_fim_de_jogo()
        return None
