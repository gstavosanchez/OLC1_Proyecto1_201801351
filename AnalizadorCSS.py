from TokenCSS import TipoCSS
from TokenCSS import TokenCSS
from Error import Error_Lexico


class Anality_CSS():
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
        self.entrada = texto + ' $'
        self.caracterActual = ''
        
        x = 0
        while x < len(self.entrada):
            self.caracterActual = self.entrada[x]
        
            # qo -> q1(simbolos del lenguje)
            if self.caracterActual == '{':
                self.add_tokken(TipoCSS.LLABRE,'{',"")
            elif self.caracterActual == '}':
                self.add_tokken(TipoCSS.LLCIER,'}',"")
            elif self.caracterActual == '(':
                self.add_tokken(TipoCSS.PABRE,'(',"")
            elif self.caracterActual == ')':
                self.add_tokken(TipoCSS.PCIER,')',"")
            elif self.caracterActual == '"': 
                self.add_tokken(TipoCSS.COMIDOBLE,'"',"")
            elif self.caracterActual == ',':
                self.add_tokken(TipoCSS.COMA,',',"")
            elif self.caracterActual == ':':
                self.add_tokken(TipoCSS.DPUNTOS,':',"")
            elif self.caracterActual == ';':
                self.add_tokken(TipoCSS.PCOMA,';',"")
            
            elif self.caracterActual.isnumeric():
                size_lexema = self.get_size_lexema_asterisco(x)
                self.q2(x,x +size_lexema)
                x = x + size_lexema

            elif self.caracterActual.isalpha():
                pass

            elif self.caracterActual == '/' and self.entrada[x + 1] == '*':
                size_lexema = self.get_size_lexema_comentario(x)
                self.q6(x,x +size_lexema+2)
                x = x + size_lexema + 2  # PENDIENTE DE REVISAR URGE PORNER MAS size_lexema +2

            elif self.caracterActual == '#' or self.caracterActual == '.':
                pass
            
            elif self.caracterActual == "\n" or self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\t":
                if self.caracterActual == "\n":
                    self.linea += 1
                    self.columna = 1 

                x += 1
                self.columna += 1
                continue
            else:
                pass

            x += 1
            self.columna += 1


        self.imprimirToken()
        return self.lista_error

    # ----------------->ESTADO Q2 <-------------------------------------- 
    # Numero 
    def q2(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]
            # q2 -> q2 con numero (numero)
            
            if c.isnumeric():
                self.lexema += c
                if (actual + 1 == fin):
                   
                    self.add_tokken(TipoCSS.VALOR,self.lexema,"blue")

            # q2 -> q2 con  % (%)
            elif c == '%':
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_tokken(TipoCSS.VALOR,self.lexema,"blue")
            # q2 -> q2 con . (.)
            elif c == '.':
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_tokken(TipoCSS.VALOR,self.lexema,"blue")

            # q2 -> q3 con letra (letra)
            elif c.isalpha():
                self.q3(actual,fin)
                break

            else:
                #Caracter No Reconocido
                self.add_error(actual,self.linea,self.columna,c)            
            actual +=1
            self.columna +=1

    # ----------------->ESTADO Q3 <--------------------------------------
    # Letra
    def q3(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]
            # q3 -> q3 con letra (letra)
            if c.isalpha():
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_tokken(TipoCSS.VALOR,self.lexema,"blue")
            else:
                #Caracter No Reconocido
                self.add_error(actual,self.linea,self.columna,c)            
            actual +=1
            self.columna +=1
                
            
            

    # ----------------->ESTADO Q6 <--------------------------------------
    # Comentario

    def q6(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual];
            self.lexema += c
            if (actual +1 == fin):
                self.add_tokken(TipoCSS.COMENTARIO,self.lexema,"gray")
            self.columna += 1
            actual += 1

    def get_size_lexema_asterisco(self,incio):
        longitud = 0
        for j in range(incio,len(self.entrada) - 1):
        #while incio < len(self.entrada):
            if self.entrada[j] == " " or self.entrada[j] == "," or self.entrada[j] == ';' or self.entrada[j] == ':' or self.entrada[j] == "\n" or self.entrada[j] == '<' or self.entrada[j] == '>' or self.entrada[j] == '{' or self.entrada[j] == '}' or self.entrada[j] == "\t" or self.entrada == "\r":
                if self.entrada[j] == "\n":
                    self.linea += 1
                    self.columna = 1
                break
            longitud += 1
        return longitud
    
    def get_size_lexema_comentario(self,incio):
        longitud = 0
        for j in range(incio,len(self.entrada) - 1):
        #while inicio < len(self.entrada):
            if self.entrada[j] == "\n":
                self.linea += 1
                self.columna = 1
            if self.entrada[j] == "*" and self.entrada[j + 1] == '/':
                break
            longitud += 1
        return longitud


    def get_lexema(self,inicio,fin):
        palabra = ""
        for x in range(inicio,fin):
            palabra += self.entrada[x]
            self.columna += 1
        return palabra

    
    def add_tokken(self,tipo,valor,color):
        nuevo = TokenCSS(tipo,valor,color)
        self.lista_Tokens.append(nuevo)
        self.caracterActual = ''
        self.lexema = ""
    
    def add_error(self,posicion,linea,columna,caracter):
        newError = Error_Lexico(posicion,linea,columna,caracter)
        self.lista_error.append(newError)

    def imprimirToken(self):
        for valor in self.lista_Tokens:
            print(f"Tipo: {valor.getTipoToken()}; Valor: {valor.getValorToken()}")
            print("--------------------------------------------------------")
    
    def limpiarCarcateres(self):
        self.cacterActual = ""
        self.lexema = "" 
        self.entrada = ""
        self.linea = 1
        self.columan = 1
        self.lista_Tokens = list()
        self.lista_error = list()