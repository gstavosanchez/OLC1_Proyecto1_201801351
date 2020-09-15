class Sintactico():
    listado_tokens = list()
    pila = list()
    pop_pila = ''
    entrada = ''
    lista_Token = list()
    
    def __init__(self):
        self.listado_tokens = list()
        self.pila = list()
        self.pop_pila = ''
        self.entrada = ''
        self.lista_Token = list()

    def q0(self,texto):
        print(texto)
        self.entrada = f"{texto}$"
        self.caracterActual = ''
        self.pila.append('#')
        x = 0
        self.q1(x)
        self.reset_analicis()
        
  
    def q1(self,actual):
        x = actual 
        while x < len(self.entrada):
            self.caracterActual = self.entrada[x]

            if self.caracterActual == '(':
                self.pila.append(self.caracterActual)
            elif self.caracterActual == ')':
                bandera = self.get_pilaPop()
                if bandera != None:
                    self.q3(x+1)
                else:
                    print("Cadena invalida :(")
                break
            elif self.caracterActual.isalpha():
                pass
            elif self.caracterActual.isnumeric():
                pass
            elif self.caracterActual == '*'or self.caracterActual == '/'or self.caracterActual == '+'or self.caracterActual == '-':
                pass

            elif self.caracterActual == '$' and x == len(self.entrada) -1:
                bandera = self.get_pilaPop()
                if bandera != None:
                    if self.pop_pila == '#':
                        print('Cadena valida (:')
                        
                    else:
                        print("Cadena invalida :(")
                else:
                    print("Cadena invalida :(")
                break
            x += 1
        

    def q3(self,actual):
        
        while actual < len(self.entrada):
            self.caracterActual = self.entrada[actual]

            if self.caracterActual == ')':
                bandera = self.get_pilaPop()
                if bandera == None:
                    print("Cadena invalida :(")
                    break
            elif self.caracterActual == '(':
                self.pila.append(self.caracterActual)
                self.q1(actual + 1)
                break
            elif self.caracterActual == '*'or self.caracterActual == '/'or self.caracterActual == '+'or self.caracterActual == '-':
                pass
            elif self.caracterActual == '$' and actual == len(self.entrada) -1:
                bandera = self.get_pilaPop()
                if bandera != None:
                    if self.pop_pila == '#':
                        print('Cadena Valida (:')
                    else:
                        print('Cadena Invalida :c')
                else:
                    print('Cadena Invalida :c')
                break

            actual += 1


    def q4(self):
        pass


    def get_pilaPop(self):
        size = len(self.pila)
        print(size)
        if size != 0:
            self.pop_pila = self.pila.pop()
            return self.pop_pila
        else:
            return None
    
    def reset_analicis(self):
        self.caracterActual = ''
        self.pop_pila = ''
        self.pila = list()
            
        