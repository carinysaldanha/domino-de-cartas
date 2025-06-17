from .carta import Valores  #Importa uma enumeração ou classe
import time  #Importa o módulo para manipulação de tempo
import random #gerar números aleatórios

class Bot: #Cria uma classe que representa um jogador bot
   
    #lista que armazenará as cartas que o bot possui (sua mão)
    def __init__(self, nome): 
        self.nome = nome 
        self.mao = []


#recebe uma lista de cartas e adiciona essas cartas à mão do bot.
def receber_cartas(self, cartas):
        self.mao.extend(cartas)
#Esse método define como o bot deve jogar sua vez.
def jogar(self, mesa, jogo, bots = None):
        time.sleep(random.uniform(0.5, 1.0)) 
# verifica se tem as cartas validas para jogar
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
