from enum import Enum

class Tipo(Enum):
    
    #simbolos  de lenguaje

    llAbre = 1
    llCier = 2
    paAbre = 3
    paCierr = 4
    dpuntos = 5
    pcoma = 6
    mas = 6
    menos = 7
    divison = 8
    mayor  = 9
    menor = 10
    comiAbre = 11 
    comiCier = 12
    igual = 13
    punto = 57
    comiSimple = 58
    coma = 59
    conjuncion = 60
    negacion = 61
    disyuncion = 62
    por = 63
    comenPor = 64



    #Palabras reservadas 

    _await = 14
    _break = 15
    _case = 16
    _catch = 17
    _class = 18
    _const = 19
    _continue = 20
    _debugger = 21
    _default = 22
    _delete =  23
    _do = 24
    _else = 25
    _export = 26
    _extends = 27
    _finally = 28
    _for = 29
    _function =30
    _if = 31
    _import = 32
    _in = 33
    _instanceof = 34
    _new = 35
    _return = 36
    _super = 37
    _switch = 38
    _this = 39
    _throw = 40
    _try = 41
    _typeof = 42
    _void = 43
    _while = 44
    _with = 45
    _yield = 46
    _let = 47
    _int  = 48
    _string = 49
    _char = 50
    _boolean = 51
    _var = 52

    # Expresion Regular 
    valor = 53
    _id = 54
    ninguno = 55
    comentario = 56

class Token():
    tipoToken = Tipo.ninguno
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
