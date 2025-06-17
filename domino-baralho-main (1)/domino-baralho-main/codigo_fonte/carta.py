from enum import Enum #criar enumerações

class Naipe(Enum):#define as nomes da naips usando simbulos
    COPAS = '♥'
    OUROS = '♦'
    ESPADAS = '♠'
    PAUS = '♣'
    
class Valores(Enum): #define os numero das cartas
    AS = 1
    DOIS = 2
    TRES = 3
    QUATRO = 4
    CINCO = 5
    SEIS = 6 
    SETE = 7
    OITO = 8
    NOVE = 9
    DEZ = 10
    VALETE = 11
    DAMA = 12
    REI = 13    

class Carta: #recebe o valor da carta e do naipe
    def __init__(self, valor, naipe, visivel=True):
        self.valor = valor
        self.naipe = naipe
        self.visivel = visivel

    def valor_str(self): #retorna a apresentação visual das cartas
        mapa = {
            Valores.AS: 'A',
            Valores.VALETE: 'J',
            Valores.DAMA: 'Q',
            Valores.REI: 'K'
        }
        return mapa.get(self.valor, str(self.valor.value))

    def __repr__(self):# para quando digitar no teclado o numero ele jogara o naip da mesa 
        return f"{self.valor_str()}{self.naipe.value}"

    def __eq__(self, other): # ver se os naips sao compativel com a carta jogada 
        return isinstance(other, Carta) and self.valor == other.valor and self.naipe == other.naipe

    def __hash__(self): #permite que cartas sejam usadas como chaves em dicionários ou armazenadas em conjuntos
        return hash((self.valor, self.naipe))



