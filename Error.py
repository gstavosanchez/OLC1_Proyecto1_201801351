class Error_Lexico():
    linea = 1
    columna = 1
    caracter = ''
    posicion = 1

    def __init__(self,posicion,linea,columna,caracter):
        self.posicion = posicion
        self.linea = linea
        self.columna = columna
        self.caracter = caracter
    
    def getPosicion(self):
        return self.posicion
    
    def getLinea(self):
        return self.linea
    
    def getColumna(self):
        return self.columna
    
    def getCaracter(self):
        return self.caracter
