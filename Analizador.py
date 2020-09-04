from Token import Tipo
from Token import Token


class Analicis():

    lista_token = list()
    lista_error = list()
    pos_error = {} 
    lexema = "" 
    linea = 1
    columan = 1

    def __init__(self):
        self.lista_token = list()
        self.lista_error = list()
        self.pos_error = {}
        self.lexema = ""
        self.linea = 1
        self.columan = 1

    def _incio(self,texto):
        self.entrada  = texto + '$'
        self.cacterActual = ''
        posicion = 0

        while posicion < len(self.entrada):
            self.cacterActual = self.entrada[posicion]
            
            
            #q0 -> q1 por que es simbolo :V
            #print(f"Pos{posicion} letra:{self.cacterActual}")
            
            if self.cacterActual == '/' and self.entrada[posicion + 1] == '*':
                self.add_token(Tipo.comenPor,'/*',"gray")
                sizeLexema = self.get_size_lexemaComentario_mul(posicion)
                self.q6(posicion+2,posicion+sizeLexema)
                posicion = posicion + sizeLexema
                

            if self.cacterActual == "{":
                self.add_token(Tipo.llAbre,"{","")
            elif self.cacterActual == "}":
                self.add_token(Tipo.llCier,"}","")
            elif self.cacterActual == "=":
                self.add_token(Tipo.igual,"=","anaranjado")
            elif self.cacterActual == '(':
                self.add_token(Tipo.paAbre,"(","")
            elif self.cacterActual == ")":
                self.add_token(Tipo.paCierr,')',"")
            elif self.cacterActual  == ":":
                self.add_token(Tipo.dpuntos,":","")
            elif self.cacterActual == ";":
                self.add_token(Tipo.pcoma,";","")
            elif self.cacterActual == "+":
                self.add_token(Tipo.mas, "+","anaranjado")
            elif self.cacterActual == "-":
                self.add_token(Tipo.menos, "-","anaranjado")
            #elif self.cacterActual == "/":
                #self.add_token(Tipo.division,"/","white")
            elif self.cacterActual == ">":
                self.add_token(Tipo.mayor,">","anaranjado")
            elif self.cacterActual == "<":
                self.add_token(Tipo.menor,"<","anaranjado")
            elif self.cacterActual == '"':
                self.add_token(Tipo.comiAbre,'"',"yellow")
            elif self.cacterActual == '.':
                self.add_token(Tipo.punto,'.',"")
            elif self.cacterActual == ',':
                self.add_token(Tipo.coma,',',"")
            elif self.cacterActual == "'":
                self.add_token(Tipo.comiSimple,'\'',"yellow")
            elif self.cacterActual == '&' and self.entrada[posicion + 1] == '&':
                self.add_token(Tipo.conjuncion,"&&" ,"anaranjado")
            elif self.cacterActual == '!':
                self.add_token(Tipo.negacion,'!' ,"anaranjado")
            elif self.cacterActual == '|' and self.entrada[posicion + 1 ] == '|':
                self.add_token(Tipo.negacion,'||' ,"anaranjado")
            elif self.cacterActual == '*':
                self.add_token(Tipo.por,'*',"")


            
        
            if self.entrada[posicion - 1] == '"' or self.entrada[posicion - 1] == "'"  or self.cacterActual == "'" or self.cacterActual == '"' :
                sizeLexema = self.get_size_lexemaEspecial(posicion)
                #print(f"SizeLexema en ' :{sizeLexema}")
                self.q5(posicion,posicion+sizeLexema)
                posicion = posicion + sizeLexema
                if (self.entrada[posicion] == "\n"):
                    self.linea += 1
                #print(f"Caracter Actual: {self.cacterActual}")
                #print(f"Anterior:{self.entrada[posicion -1]}  Actual:{self.entrada[posicion]}  siguinte:{self.entrada[posicion + 1]}")



            # q0 -> q1 Si es numero 
            elif self.cacterActual.isnumeric():
                sizeLexema = self.get_size_lexema(posicion)
                self.q2(posicion,posicion +sizeLexema)
                posicion = posicion + sizeLexema


            
            elif self.entrada[posicion - 1] == '/' and self.cacterActual == '/':
                #print(self.cacterActual)
                sizeLexema = self.get_size_lexemaComentario_un(posicion)
                self.q6(posicion+1,posicion+sizeLexema)
                posicion = posicion + sizeLexema
            
            elif self.entrada[posicion - 1] == '/' and self.cacterActual == '*':
                print(f"actaul:{self.cacterActual}")
                sizeLexema = self.get_size_lexemaComentario_mul(posicion)
                self.q6(posicion+1,posicion+sizeLexema)
                posicion = posicion + sizeLexema
             
            elif self.cacterActual.isalpha():
                sizeLexema  = self.get_size_lexema(posicion)
                self.analizador_id_reservada(posicion,posicion + sizeLexema);
                posicion = posicion + sizeLexema

            elif self.cacterActual == "\n":
                self.linea += 1
                #print(f" 1 if Salto de linea en :{self.linea}")

            else:
                if self.cacterActual == "$" and posicion == len(self.entrada) -1:
                    print("analicis terminado ..")
                else:
                    if self.cacterActual != " " and self.cacterActual != "\n"  and self.cacterActual != "\t" and self.cacterActual != "\r":
                        if (self.cacterActual != '/'):
                            if(self.cacterActual.isspace() == False and self.is_empty(self.cacterActual) == False):
                                if(self.cacterActual == '&' and self.entrada[posicion - 1] == '&'):
                                    pass
                                elif(self.cacterActual == '|' and self.entrada[posicion - 1] == '|'):
                                    pass
                                else:
                                    self.pos_error[self.linea] = self.insert_error(posicion,self.cacterActual)
            #print(posicion)
            posicion +=1 

        #self.imprimir()
            
        return self.pos_error;

        


    #-----> Estado3 (q2) -------------------

    def q2(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]

            if c.isnumeric():
                self.lexema += c
                if(actual + 1 == fin):
                    self.add_token(Tipo.valor,self.lexema,"blue")

            else:
                self.pos_error[self.linea] = self.insert_error(actual,c)
            actual +=1
                
    
    #-----> Estado3 (q3) -------------------
    
    def q3(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]
            if c.isalpha():
                self.lexema += c
                if(actual +1 == fin):
                    self.add_token(Tipo.valor,self.lexema,"blue")
            else:
                self.pos_error[self.linea] = self.insert_error(actual,c)
    

    def analizador_id_reservada(self,actual, fin):
        self.lexema = self.get_lexema(actual,fin).lower()
        
        # q0 -> q3
        if(self.lexema == "var"):
            self.add_token(Tipo._var,"var","red")
            return
        elif(self.lexema == "for"):
            self.add_token(Tipo._for,"for","red")
            return 
        elif(self.lexema == "if"):
            self.add_token(Tipo._if,"if","red")
            return 
        elif(self.lexema == "class"):
            self.add_token(Tipo._class,"class","red")
            return 
        elif(self.lexema == "else"):
            self.add_token(Tipo._else,"else","red")
            return
        elif(self.lexema == "break"):
            self.add_token(Tipo._break,"break","red")
            return 
        elif(self.lexema == "await"):
            self.add_token(Tipo._await,"await","red")
            return
        elif(self.lexema == "case"):
            self.add_token(Tipo._case,"case","red")
            return 
        elif(self.lexema == "catch"):
            self.add_token(Tipo._catch,"catch","red")
            return 
        elif self.lexema == "const":
            self.add_token(Tipo._const,"const","red")
            return 
        elif self.lexema == "continue":
            self.add_token(Tipo._const,"continue","red")
            return
        elif self.lexema == "debugger":
            self.add_token(Tipo._debugger,"debugger","red")
            return
        elif self.lexema == "default":
            self.add_token(Tipo._default,"default","red")
            return
        elif self.lexema == "delete":
            self.add_token(Tipo._delete,"delete","red")
            return
        elif self.lexema == "do":
            self.add_token(Tipo._do,"do","red")
            return
        elif self.lexema == "export":
            self.add_token(Tipo._export,"export","red")
            return
        elif self.lexema == "extends":
            self.add_token(Tipo._extends,"extends","red")
            return
        elif self.lexema == "finally":
            self.add_token(Tipo._finally,"finally","red")
            return
        elif self.lexema == "function":
            self.add_token(Tipo._function,"function","red")
            return
        elif self.lexema == "if":
            self.add_token(Tipo._if,"if","red")
            return
        elif self.lexema == "import":
            self.add_token(Tipo._import,"import","red")
            return 
        elif self.lexema == "in":
            self.add_token(Tipo._in,"in","red")
            return
        elif self.lexema == "instanceof":
            self.add_token(Tipo._instanceof,"instanceof","red")
            return
        elif self.lexema == "new":
            self.add_token(Tipo._new,"new","red")
            return
        elif self.lexema == "return":
            self.add_token(Tipo._return,"return","red")
            return
        elif self.lexema == "super":
            self.add_token(Tipo._super,"super","red")
            return
        elif self.lexema == "switch":
            self.add_token(Tipo._switch,"switch","red")
            return
        elif self.lexema == "this":
            self.add_token(Tipo._this,"this","red")
            return
        elif self.lexema == "throw":
            self.add_token(Tipo._throw,"this","red")
            return
        elif self.lexema == "try":
            self.add_token(Tipo._try,"try","red")
            return
        elif self.lexema == "typeof":
            self.add_token(Tipo._typeof,"typeof","red")
            return
        elif self.lexema == "void":
            self.add_token(Tipo._void,"void","red")
            return
        elif self.lexema == "while":
            self.add_token(Tipo._while,"while","red")
            return
        elif self.lexema == "with":
            self.add_token(Tipo._with,"with","red")
            return
        elif self.lexema == "yield":
            self.add_token(Tipo._yield,"yield","red")
            return
        elif self.lexema == "let":
            self.add_token(Tipo._let,"let","red")
            return
        
        self.lexema = ""
        c = ''
        while actual < fin:
            c = self.entrada[actual]
            
            if c.isalpha():
                #print("Entro para q4")
                self.q4(actual,fin)
                break
            
            else:
                self.pos_error[self.linea] = self.insert_error(actual,c)
                print(f"Error lexico :C :{c} in line:{self.linea}")
            actual +=1

    

    def q4(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]
    
            if c.isalpha():
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(Tipo._id,self.lexema,"green")
            
            elif c.isnumeric():
                self.lexema += c
                if (actual + 1 == fin):
                    self.add_token(Tipo._id,self.lexema,"green")

            elif c == "_":
                self.lexema +=c
                if(actual + 1 == fin):
                    self.add_token(Tipo._id,self.lexema,"green")
            else:
                self.pos_error[self.linea] = self.insert_error(actual,c)
                print(f"Error lexico :C :{c} in line:{self.linea}")
            actual += 1


    def q5(self,actual,fin):
        c = ''
        fin = fin - 1 
        while actual < fin:
            c = self.entrada[actual]
            self.lexema += c

            if(actual + 1 == fin):
                self.add_token(Tipo.valor,self.lexema,"yellow")
            actual +=1
    
    def q6(self,actual,fin):
        c = ''
        while actual < fin:
            c = self.entrada[actual]
            self.lexema += c
            if(actual + 1 == fin):
                self.add_token(Tipo.comentario,self.lexema,"gray")
            
            actual +=1

        

    def get_lexema(self,actual,fin):
        return (self.entrada[actual:fin])


    def add_token(self,tipo,valor,color):
        new  = Token(tipo,valor,color)
        self.lista_token.append(new)
        self.cacterActual = ""
        self.estado = 0
        self.lexema = ""    

    def imprimir(self):
        for valor in self.lista_token:
            print(f"Tipo:{valor.getTipoToken()}, Valor:{valor.getValorToken()}")
            print("--------------")

    


    def get_size_lexema(self, posInicial):
        longitud = 0
        for i in range(posInicial,len(self.entrada) -1 ):
                #if self.entrada[i] == "(" or self.entrada[i] == ")" or self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r"  or self.entrada[i] == "=" or self.entrada[i] == '"' or self.entrada[i] == "//" or self.entrada[i] == "/*" or self.entrada[i] == "*/":
            if  self.entrada[i] == "," or self.entrada[i] == "(" or self.entrada[i] == ")" or self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r"  or self.entrada[i] == "=" or self.entrada[i] == "//" or self.entrada[i] == "/*" or self.entrada[i] == "*/" or self.entrada[i] == '.':
                if self.entrada[i] == "\n":
                    self.linea +=1 
                    #print(f" size_lexema if Salto de linea en :{self.linea}")
                break
            longitud +=1
        return longitud

    # devuelve la longitul del lexima si esta en "sdf dfad" 
    def get_size_lexemaEspecial(self,inicial):
        longitud = 0
        for i in range(inicial,len(self.entrada) -1 ):
            if self.entrada[i] == "\n":
                self.linea +=1 
                #print(f" size_lexema_Especial if Salto de linea en :{self.linea}")
            if self.entrada[i] == '"' or self.entrada[i] == "'":
                break
            longitud +=1
        return longitud+1
    
    # devuelve la longitul del lexema si esta en un --> comentario uniliniea
    def get_size_lexemaComentario_un(self,inicial):
        longitud = 0
        for i in range(inicial,len(self.entrada) -1 ):
            if self.entrada[i] == "\n":
                self.linea += 1
                #print(f" size_lexema_COmentarioUni if Salto de linea en :{self.linea}")
                break
            longitud +=1
        return longitud

    # devuelve la longitul del lexema si esta en un --> comentario multilinea
    def get_size_lexemaComentario_mul(self,inicial):
        longitud = 0
        for i in range(inicial,len(self.entrada) -1 ):
            if self.entrada[i] == "\n":
                self.linea +=1 
                #print(f" size_lexema_COmentarioMulti if Salto de linea en :{self.linea}")
            if self.entrada[i] == '*' and self.entrada[i + 1] == '/':
                break
            longitud +=1
        return longitud


    def insert_error(self,poscion,letra):
        listaError = self.getListError(self.linea)
        if listaError == None:
            listaError = list()
            listaError.append(letra)
        else:
            listaError.append(letra)

        return listaError;

    def getListError(self,clave):
        for key,value  in self.pos_error.items():
            if clave == key:
                return value
        return None
    
    def getListTokens(self):
        listaClonada = []
        listaClonada = self.lista_token;
        return listaClonada;

    def is_empty(self,data_structure):
        if data_structure:
            #print("No está vacía")
            return False
        else:
            #print("Está vacía")
            return True
    

    #limpia las variables globales para otra ejecucion
    def clear_data(self):
        self.cacterActual = ""
        self.estado = 0
        self.lexema = "" 
        self.entrada = ""
        self.linea = 1
        self.columan = 1
        self.lista_token = list()
        self.lista_error = list()
        self.pos_error = {}