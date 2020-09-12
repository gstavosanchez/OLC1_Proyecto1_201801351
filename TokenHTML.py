from enum import Enum

class TipoHTML(Enum):
    
    #Simbolos del lenguaje
    MENOR = 1
    MAYOR = 2
    IGUAL = 3
    
    
    RESERVADA = 4


    #Expresiones Regular
    NINGUNO = 58
    VALOR  = 59
    ID = 60
    COMENTARIO = 61


class TokenHTML():
    tipoToken = TipoHTML.NINGUNO
    valorToken = ""
    color = ""

    def __init__(self,tipo, valor,color):
        self.tipoToken = tipo
        self.valorToken = valor
        self.color = color

    def setTipoToken(self,tipo):
        self.tipoToken = tipo
    def getTipoToken(self):
        return self.tipoToken

    def setValorToken(self,valor):
        self.valorToken = valor
    def getValorToken(self):
        return self.valorToken

    def setColorToken(self,color):
        self.color = color
    def getColorToken(self):
        return self.color    