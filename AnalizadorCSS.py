from TokenCSS import TipoCSS
from TokenCSS import TokenCSS
from datetime import datetime

from Error import Error_Lexico
from Reporte import Report


class Anality_CSS():
    lista_Tokens = list()
    lista_error = list()
    linea = 1
    columna = 1
    lexema = ""
    bandera = False
    actibarBandera = False
    recorrido_automata = {}
    _reporte = Report()
    bitacora = ""
    now = datetime.now()

    def __init__(self):
        self.lista_Tokens = list()
        self.lista_error = list()
        self.linea = 1
        self.columna = 1
        self.lexema = ""
        self.bandera = False
        self.actibarBandera = False
        self.recorrido_automata = {}
        self._reporte = Report()
        self.now = datetime.now()
        self.bitacora = ""

    def read_caracter(self,texto):
        self.bitacora = f"---------->Bitacora CSS <---------- [{self.getTime()}] \n"
        self.entrada = texto + '$'
        self.caracterActual = ''
        self.newEntrada = texto
        
        x = 0
        while x < len(self.entrada):
            self.caracterActual = self.entrada[x]
            #print(self.caracterActual)
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
                size_lexema = self.get_size_lexema_asterisco(x)
                self.q4(x, x+ size_lexema)
                x = x + size_lexema

            elif self.caracterActual == '/' and self.entrada[x + 1] == '*':
                size_lexema = self.get_size_lexema_comentario(x)
                if (x + size_lexema + 2  <=   len(self.entrada)):
                    self.q6(x,x +size_lexema+2)
                    x = x + size_lexema + 2  # PENDIENTE DE REVISAR URGE PORNER MAS size_lexema +2
                else:
                    self.q6(x,x +size_lexema)
                    x = x + size_lexema
                    self.add_error(x,self.linea,self.columna,'*/')
                    break

            elif self.caracterActual == '#' or self.caracterActual == '.':
                if (self.bandera == False):
                    self.actibarBandera = True

                    _trasBitacora = f"[q0 -> q4;{self.caracterActual}] - [{self.getHora()}] \n"
                    self.bitacora += _trasBitacora

                    transicion = f"{self.caracterActual},q4"
                    self.add_diccionario('q0',transicion)
                    

                size_lexema = self.get_size_lexema_asterisco(x)
                self.q4(x, x+ size_lexema)
                x = x + size_lexema
            
            elif self.caracterActual == '-':
                size_lexema = self.get_size_lexema_asterisco(x)
                self.q2(x,x + size_lexema)
                x = x + size_lexema
            
            #elif self.caracterActual == "\n":
                #print("Salto de linea")

            elif self.caracterActual == "\n" or self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\t":
                if self.caracterActual == "\n":
                    self.linea += 1
                    self.columna = 1 
                    #print("Salto de linea principal")

                x += 1
                self.columna += 1
                continue

            else:
                if self.caracterActual == "$" and x == len(self.entrada) -1 :
                    print("Analicis Terminado")
                else:
                    self.add_error(x,self.linea,self.columna,self.caracterActual)

            x += 1
            self.columna += 1


        
        return self.lista_error

    # ----------------->ESTADO Q2 <-------------------------------------- 
    # Numero 
    def q2(self,actual,fin):
        c = ''
        inicio = actual
        while actual < fin:
            c = self.entrada[actual]
            # q2 -> q2 con numero (numero)
            
            if c.isnumeric():
                self.lexema += c
                #transicion = f"{c},q2"
                #self.add_diccionario('q2',transicion)
                if (actual + 1 == fin):
                    self.add_tokken(TipoCSS.VALOR,self.lexema,"blue")

            # q2 -> q2 con  % (%)
            elif c == '%':
                self.lexema += c
                #transicion = f"{c},q7"
                #self.add_diccionario('q2',transicion)
                if (actual + 1 == fin):
                    self.add_tokken(TipoCSS.VALOR,self.lexema,"blue")
            # q2 -> q2 con . (.)
            elif c == '.':
                self.lexema += c
                #transicion = f"{c},q2"
                #self.add_diccionario('q2',transicion)
                if (actual + 1 == fin):
                    self.add_tokken(TipoCSS.VALOR,self.lexema,"blue")
            
            elif c == '-' and actual == inicio:
                self.lexema += c
                #transicion = f"{c},q2"
                #self.add_diccionario('q2',transicion)
            
            # q2 -> q3 con letra (letra)
            elif c.isalpha():
                #transicion = f"{c},q3"
                #self.add_diccionario('q2',transicion)
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

    # ----------------->Estado Q4 <--------------------------------------
    #  Reservadas 
    def q4(self,actual,fin):
        self.lexema = self.get_lexema(actual,fin)

        if self.lexema == "color":
            self.add_tokken(TipoCSS.COLOR,'color','red')
            return
        elif self.lexema == "border":
            self.add_tokken(TipoCSS.BORDER,"border","red")
            return
        elif self.lexema == "text-align":
            self.add_tokken(TipoCSS.TEXT_ALIGN,"text-align","red")
            return
        elif self.lexema == "font-weight":
            self.add_tokken(TipoCSS.FONT_WEIGHT,"font-weight","red")
            return
        elif self.lexema == "padding-left":
            self.add_tokken(TipoCSS.PADDING_LEFT,"padding-left","red")
            return
        elif self.lexema == "padding-top":
            self.add_tokken(TipoCSS.PADDING_TOP,"padding-top","red")
            return
        elif self.lexema == "line-height":
            self.add_tokken(TipoCSS.LINE_HEIGHT,"line-height","red")
            return
        elif self.lexema == "margin-top":
            self.add_tokken(TipoCSS.MARGIN_TOP,"margin-top","red")
            return
        elif self.lexema == "margin-left":
            self.add_tokken(TipoCSS.MARGIN_LEFT,"margin-left","red")
            return
        elif self.lexema == "display":
            self.add_tokken(TipoCSS.DISPLAY,"display","red")
            return
        elif self.lexema == "top":
            self.add_tokken(TipoCSS.TOP,"top","red")
            return
        elif self.lexema == "float":
            self.add_tokken(TipoCSS.FLOAT,"float","red")
            return
        elif self.lexema == "min-width":
            self.add_tokken(TipoCSS.MIN_WIDTH,"min-width","red")
            return
        elif self.lexema == "background-color":
            self.add_tokken(TipoCSS.BACKGROUND_COLOR,"background-color","red")
            return 
        elif self.lexema == "background":
            self.add_tokken(TipoCSS.BACKGROUND,"background","red")
            return
        elif self.lexema == "font-family":
            self.add_tokken(TipoCSS.FONT_FAMILY,"font-family","red")
            return
        elif self.lexema == "font-size":
            self.add_tokken(TipoCSS.FONT_SIZE,"font-size","red")
            return
        elif self.lexema == "padding-right":
            self.add_tokken(TipoCSS.PADDING_RIGHT,"padding-right","red")
            return
        elif self.lexema == "padding":
            self.add_tokken(TipoCSS.PADDING,"padding","red")
            return
        elif self.lexema == "width":
            self.add_tokken(TipoCSS.WIDTH,"width","red")
            return
        elif self.lexema == "margin-right":
            self.add_tokken(TipoCSS.MARGIN_RIGHT,"margin-right","red")
            return
        elif self.lexema == "margin":
            self.add_tokken(TipoCSS.MARGIN,"margin","red")
            return
        elif self.lexema == "bottom":
            self.add_tokken(TipoCSS.BOTTOM,"bottom","red")
            return
        elif self.lexema == "right":
            self.add_tokken(TipoCSS.RIGHT,"right","red")
            return
        elif self.lexema == "clear":
            self.add_tokken(TipoCSS.CLEAR,"clear","red")
            return
        elif self.lexema == "max-height":
            self.add_tokken(TipoCSS.MAX_HEIGHT,"max-height","red")
            return 
        elif self.lexema == "background-image":
            self.add_tokken(TipoCSS.BACKGROUND_IMAGE,"background-image","red")
            return
        elif self.lexema == "font-style":
            self.add_tokken(TipoCSS.FONT_STYLE,"font-style","red")
            return
        elif self.lexema == "font":
            self.add_tokken(TipoCSS.FONT,"font","red")
            return 
        elif self.lexema == "padding-bottom":
            self.add_tokken(TipoCSS.PADDING_BOTTOM,"padding-bottom","red")
            return 
        elif self.lexema == "margin-bottom":
            self.add_tokken(TipoCSS.MARGIN_BOTTOM,"margin-bottom","red")
            return 
        elif self.lexema == "border-style":
            self.add_tokken(TipoCSS.BORDER_STYLE,"border-style","red")
            return
        elif self.lexema == "position":
            self.add_tokken(TipoCSS.POSITION,"position","red")
            return
        elif self.lexema == "left":
            self.add_tokken(TipoCSS.LEFT,"left","red")
            return
        elif self.lexema == "max-width":
            self.add_tokken(TipoCSS.MAX_WIDTH,"max-width","red")
            return
        elif self.lexema == "min-height":
            self.add_tokken(TipoCSS.MIN_HEIGHT,"min-height","red")
            return


        self.lexema = ""
        c = ''
        while actual< fin:
            c = self.entrada[actual]
            # q4 -> q5 (letra | numero)
            if c == '#':
                self.lexema += c

                if(self.bandera == False and self.actibarBandera == True):
                    _trasBitacora = f"[q4 -> q5;{self.entrada[actual + 1]}] - [{self.getHora()}] \n"
                    self.bitacora += _trasBitacora

                    transicion = f"{self.entrada[actual + 1]},q5"
                    self.add_diccionario('q4',transicion)

                self.q5(actual + 1,fin)
                break

            # q4 -> q5 (letra | numero)
            elif c == '.':
                self.lexema += c

                if (self.bandera == False and self.actibarBandera == True):
                    _trasBitacora = f"[q4 -> q5;{self.entrada[actual + 1]}] - [{self.getHora()}] \n"
                    self.bitacora += _trasBitacora

                    transicion = f"{self.entrada[actual + 1]},q5"
                    self.add_diccionario('q4',transicion)
        
                self.q5(actual + 1,fin)
                break

            # q4 -> q5 (letra | numero)
            elif c.isalpha():
                self.q5(actual,fin)
                break
            else:
                self.add_error(actual,self.linea,self.columna,c)

            actual += 1
            self.columna += 1


    # --------------------------> <--------------------------------------
    # ----------------->ESTADO Q5 <--------------------------------------
    def q5(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]
            # q5 -> q5 (letra)
            if c.isalpha():
                self.lexema += c
                
                if (self.bandera == False and self.actibarBandera == True):
                    _trasBitacora = f"[q5 -> q5;{c}] - [{self.getHora()}] \n"
                    self.bitacora += _trasBitacora
                    transicion = f"{c},q5"
                    self.add_diccionario('q5',transicion)

                if(actual + 1 == fin):
                    self.add_tokken(TipoCSS.ID,self.lexema,"green")

                    if(self.actibarBandera == True):
                        self.bandera = True
                        self.actibarBandera == False

            elif c.isnumeric():
                self.lexema += c

                if (self.bandera == False and self.actibarBandera == True):
                    _trasBitacora = f"[q5 -> q5;{c}] - [{self.getHora()}] \n"
                    self.bitacora += _trasBitacora
                    transicion = f"{c},q5"
                    self.add_diccionario('q5',transicion)

                if(actual +1 == fin):
                    self.add_tokken(TipoCSS.ID,self.lexema,"green")

                    if(self.actibarBandera == True):
                        self.bandera = True
                        self.actibarBandera == False
                
            elif c == '-':
                self.lexema += c
                if(actual +1 == fin):
                    self.add_tokken(TipoCSS.ID,self.lexema,"green")
            # q5 -> q4 (#)
            elif c == '#' or c == '(' or c == ')' or c == '"' or c == '.'  or  c == '/':
                self.lexema += c
                if(actual +1 == fin):
                    self.add_tokken(TipoCSS.ID,self.lexema,"green")
                
            else:
                #print(self.linea)
                self.add_error(actual,self.linea,self.columna,c)
            
            actual += 1
            self.columna += 1


    # --------------------------> <--------------------------------------


    def get_size_lexema_asterisco(self,incio):
        longitud = 0
        for j in range(incio,len(self.entrada) - 1):
            if self.entrada[j] == "\n":
                self.linea += 1
                self.columna = 1
                #print("Salto de linea get_size_lexema")
            if self.entrada[j] == " " or self.entrada[j] == "," or self.entrada[j] == ';' or self.entrada[j] == ':' or self.entrada[j] == "\n" or self.entrada[j] == '<' or self.entrada[j] == '>' or self.entrada[j] == '{' or self.entrada[j] == '}' or self.entrada[j] == "\t" or self.entrada == "\r":
                break
            longitud += 1
        return longitud
    
    def get_size_lexema_comentario(self,incio):
        longitud = 0
        for j in range(incio,len(self.entrada) - 1):
            if self.entrada[j] == "\n":
                self.linea += 1
                self.columna = 1
                #print("Salto de linea comentraio")
            if self.entrada[j] == "*" and self.entrada[j + 1] == '/':
                break
            longitud += 1
        return longitud


    def get_lexema(self,inicio,fin):
        palabra = ""
        for x in range(inicio,fin):
            palabra += self.entrada[x]
            if self.entrada[x] == "\n":
                self.linea += 1
                self.columna = 1
                print("Salto de linea en get_lexema")
            self.columna += 1
        return palabra.lower()

    
    def add_tokken(self,tipo,valor,color):
        nuevo = TokenCSS(tipo,valor,color)
        self.lista_Tokens.append(nuevo)
        self.caracterActual = ''
        self.lexema = ""
    
    def add_error(self,posicion,linea,columna,caracter):
        if(caracter == '/' or caracter == '*' or caracter == '{' or caracter == '}' or caracter == '"' or caracter == ';' or caracter == ':' or caracter == ',' or caracter == '<' or caracter == '>' or caracter == '(' or caracter == ')'):
            pass
        else:
            newError = Error_Lexico(posicion,linea,columna,caracter)
            self.lista_error.append(newError)

    def imprimirToken(self):
        for valor in self.lista_Tokens:
            print(f"Tipo: {valor.getTipoToken()}; Valor: {valor.getValorToken()}")
            print("--------------------------------------------------------")
    
    def limpiarCarcateres(self):
        self.caracterActual = ''
        self.lexema = "" 
        self.entrada = ""
        self.linea = 1
        self.columna = 1
        self.lista_Tokens = list()
        self.lista_error = list()

    def get_pathComenatrio(self):
        ruta = ''
        for valor in self.lista_Tokens:                
            if TipoCSS.COMENTARIO == valor.getTipoToken():
                tokenValor =  valor.getValorToken()
                if(tokenValor.find("PATHW")) != -1:
                    if(tokenValor.find("c:") != -1):
                        ruta = tokenValor[tokenValor.find('c:'):tokenValor.find('*/')].strip()
                        break
                    elif (tokenValor.find("C:") != -1):
                        ruta = tokenValor[tokenValor.find('C:'):tokenValor.find('*/')].strip()
                        break
                    
        
        return ruta
        
    def add_diccionario(self,clave,trancison):
        listaTrancision = self.get_estadoDiccionario(clave)
        if listaTrancision == None:
            listaTrancision = list()
            listaTrancision.append(trancison)
        else:
            listaTrancision.append(trancison)
        
        self.recorrido_automata[clave] = listaTrancision

    def get_estadoDiccionario(self,clave):
        for key,value in self.recorrido_automata.items():
            if key == clave:
                return value
        return None
    
    def enviarReporte(self,ruta):
        #self._reporte.genenarte_Graphivz(self.recorrido_automata)
        self._reporte.writeReporte(ruta,self.newEntrada,self.lista_error)
        self.newEntrada = ''
        
    def getTime(self):
        time = ""
        time = f"{self.getHora()} - {self.now.day}/{self.now.month}/{self.now.year}"
        return time

    def getBitacora(self):
        return self.bitacora
    
    def getHora(self):
        time = ""
        minuto = self.now.minute
        if (minuto <= 9):
            minuto = f"0{self.now.minute}"
            time = f"{self.now.hour}:{minuto}.{self.now.second} "
        else:
            time = f"{self.now.hour}:{self.now.minute}.{self.now.second} "

        return time