from TokenHTML import TipoHTML
from TokenHTML import TokenHTML
from Error import Error_Lexico

class Anality_HTML():
    lista_Tokens = list()
    lista_error = list()
    linea = 1
    columna = 1
    lexema = ""

    def __init__(self):
        self.lista_Tokens = list()
        self.lista_error = list()
        self.linea = 1
        self.columna = 1 
        self.lexema = ""

    def read_caracter(self,texto):
        self.entrada = texto + '$'
        self.cActual = ''
        
        x = 0
        #print("inicio a leer")
        while x < len(self.entrada):
            self.cActual = self.entrada[x]
            print(self.cActual)

            if self.cActual == '<' and self.entrada[x + 1] == '!' and self.entrada[x + 2] == '-':
                if self.entrada[x+3] == '-':
                    size_lexama = self.get_size_lexemaComentario(x)
                    self.q4(x,x+size_lexama+3)
                    x = x + size_lexama

            elif self.cActual == '<' and self.entrada[x+ 1] == '!':
                size_lexema = self.get_size_lexema(x)
                self.q1(x,x+size_lexema)
                x = x + size_lexema

            elif self.cActual == '<':
                size_lexema = self.get_size_lexema(x)
                self.q1(x,x+size_lexema)
                x = x + size_lexema

    
            
                
            elif self.cActual.isalpha() or self.cActual.isnumeric():
                size_lexema = self.get_size_lexemaValor(x)
                self.q3(x,x+size_lexema)
                print(f"antes de la suma:{x}")
                x = x + (size_lexema - 1)
                

            elif self.cActual == "\n" or self.cActual == " " or self.cActual== "\t" or self.cActual == "\t":
                if self.cActual == "\n":
                    self.linea += 1
                    self.columna = 1 
                    #print("Salto de linea principal")

                x += 1
                self.columna += 1
                continue

            else:
                if self.cActual == "$" and x == len(self.entrada) -1 :
                    print("Analicis Terminado")
                else:
                    pass

            x += 1
            self.columna += 1
        
        self.imprimir_token()
        return True

    
    def q1(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]
            if c.isnumeric():
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")
            elif c == '!':
                self.lexema +=c
            elif c.isalpha():
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")
            elif c == '/':
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")
            elif c == '=':
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")
            elif c == '\n' or c == ' ' or c == "\t":
                self.lexema +=c
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")
            elif c == '"' or c == "'":
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")
                else:
                    self.q2(actual+ 1,fin)
                    break
            else:
                self.add_error(actual,self.linea,self.columna,c)
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")

            actual +=1 
            self.columna += 1

    def q2(self,actual,fin):
        while actual < fin:
            c = self.entrada[actual]

            if c == '"' or c == "'":
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(TipoHTML.ID,self.lexema,"")
                else:
                    self.q1(actual + 1, fin)
                    break
            else:
                self.lexema += c

            actual += 1
            self.columna += 1

    def q3(self,actual,fin):
        while actual < fin:
            c = self.entrada[actual]
            self.lexema += c
            if (actual + 1 == fin):
                self.add_token(TipoHTML.VALOR,self.lexema,'')
            
            actual += 1
    
    
    def q4(self,actual,fin):
        while actual < fin:
            c = self.entrada[actual]
            self.lexema += c
            if (actual + 1 == fin):
                self.add_token(TipoHTML.COMENTARIO,self.lexema,'gray')
            
            actual += 1

            



    def add_token(self,tipo,valor,color):
        nuevo = TokenHTML(tipo,valor,color)
        self.lista_Tokens.append(nuevo)
        self.cActual = ''
        self.lexema = ""
    
    def add_error(self,posicion,linea,columna,caracter):
        newError = Error_Lexico(posicion,linea,columna,caracter)
        self.lista_error.append(newError)
        


    def imprimir_token(self):
         for valor in self.lista_Tokens:
            print(f"Tipo: {valor.getTipoToken()}; Valor: {valor.getValorToken()}")
            print("--------------------------------------------------------")


    


    def get_size_lexema(self,incio):
        longitud = 0
        for j in range(incio,len(self.entrada) - 1):
            if self.entrada[j] == '>':
                if self.entrada[j] == "\n":
                    self.linea += 1
                    self.columna = 1
                break
            longitud += 1
        return longitud

    def get_size_lexemaComentario(self,incio):
        longitud = 0
        for j in range(incio,len(self.entrada) - 1):
            if self.entrada[j] == '-' and self.entrada[j+1] == '-' and self.entrada[j + 2] == '>':
                if self.entrada[j] == "\n":
                    self.linea += 1
                    self.columna = 1
                break
            longitud += 1
        return longitud

    def get_size_lexemaValor(self,inicio):
        longitud = 0
        for j in range(inicio,len(self.entrada) - 1):
            if self.entrada[j] == '<':
                if self.entrada[j] == "\n":
                    self.linea += 1
                    self.columna = 1
                break
            longitud += 1
        return longitud
    
