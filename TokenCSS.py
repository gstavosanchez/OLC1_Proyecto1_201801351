from enum import Enum

class TipoCSS(Enum):
    
    #simbolos del sistema
    LLABRE = 1
    LLCIER = 2
    DPUNTOS = 3
    PCOMA = 4
    COMA = 5
    ASTERISCO = 6
    NUMERAL = 7
    COMIDOBLE = 8
    XCENTAJE = 9
    PUNTO = 10
    PABRE = 62
    PCIER =  63

    # Unidad de MEDIDA
    _PX = 11
    _EM = 12
    _VH = 13
    _VW = 14
    _IN = 15
    _CM = 16
    _MM = 17
    _PT = 18
    _PC = 19

    #Resrevadas 
    
    COLOR = 20
    BORDER = 21
    TEXT_ALIGN = 22
    FONT_WEIGHT = 23
    PADDING_TOP = 24
    PADDING_LEFT = 25
    LINE_HEIGHT = 26
    MARGIN_TOP = 27
    MARGIN_LEFT = 28
    DISPLAY = 29
    TOP = 30
    FLOAT = 31
    MIN_WIDTH = 32
    BACKGROUND_COLOR = 33
    OPACITY = 34
    FONT_FAMILY = 35
    FONT_SIZE  = 36
    PADDING_RIGHT = 37
    PADDING = 38
    WIDTH = 39
    MARGIN_RIGHT = 40
    MARGIN = 41
    POSITION = 42
    RIGHT = 43
    CLEAR = 44
    MAX_HEIGHT = 45
    BACKGROUND_IMAGE = 46
    BACKGROUND = 47
    FONT_STYLE = 48
    FONT = 49
    PADDING_BOTTOM = 50
    HEIGHT = 51
    MARGIN_BOTTOM = 52
    BORDER_STYLE = 53
    BOTTOM = 54
    LEFT = 55
    MAX_WIDTH = 56
    MIN_HEIGHT = 57
    

    #Expresion Regular
    NINGUNO = 58
    VALOR  = 59
    ID = 60
    COMENTARIO = 61





class TokenCSS():
    tipoToken = TipoCSS.NINGUNO
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
