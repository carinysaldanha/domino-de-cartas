from enum import Enum

class Naipe(Enum):
    COPAS = '♥'
    OUROS = '♦'
    ESPADAS = '♠'
    PAUS = '♣'
    
class Valores(Enum):
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

class Carta:
    def __init__(self, valor, naipe, visivel=True):
        self.valor = valor
        self.naipe = naipe
        self.visivel = visivel

    def valor_str(self):
        mapa = {
            Valores.AS: 'A',
            Valores.VALETE: 'J',
            Valores.DAMA: 'Q',
            Valores.REI: 'K'
        }
        return mapa.get(self.valor, str(self.valor.value))

    def __repr__(self):
        return f"{self.valor_str()}{self.naipe.value}"

    def __eq__(self, other):
        return isinstance(other, Carta) and self.valor == other.valor and self.naipe == other.naipe

    def __hash__(self):
        return hash((self.valor, self.naipe))



