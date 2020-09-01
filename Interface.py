from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext

from CustomText import CustomText

from Analizador import Analicis

class Interface():
    def __init__(self,window):
        self.wind = window
        self.wind.title('Analysis Application')
        self.wind.geometry("1000x700")
        self.wind.configure(bg = '#0A010B')
        self.textArea = CustomText(self.wind,width = 100,height = 25, bg ="#453B46", foreground = "#FFFFFF")
        self.txtConsola = Entry(self.wind, width = 10)
        self.play_button = PhotoImage(file = 'play2.png')
        self.play_button = self.play_button.subsample(10,10)
        self.buttonOk = Button(self.wind,image = self.play_button, command = self.getText, bg = "#0A010B", highlightbackground = "#0A010B", highlightcolor= "#0A010B")
        self.lexema = ""
        self.analizador = Analicis()

        self.menu = Menu(self.wind) # Menu Bar
        self.file_item = Menu(self.menu,bg='#374140',activebackground = '#84407B', tearoff=0)
        self.file_item.add_command(label = 'Open file',command=self.open_File)

        self.file_item.add_separator()
        self.file_item.add_command(label = 'Exit',command=self.exit_program)

        self.menu.add_cascade(label = 'File',menu=self.file_item)
        self.wind.config(menu = self.menu)

        #TextArea de la entrada
        #self.textArea = scrolledtext.ScrolledText(self.wind,width = 100,height = 25, bg ="#453B46", foreground = "#FFFFFF")
        self.textArea.tag_configure("red", foreground="#ff0000")
        self.textArea.tag_configure("blue", foreground="#004DFF")
        self.textArea.tag_configure("yellow", foreground="#FFF000")
        self.textArea.tag_configure("green", foreground="#00A817")
        self.textArea.tag_configure("gray", foreground="#ABAAAA")
        self.textArea.tag_configure("white", foreground="#FFFFFF")
        self.textArea.place(x = 40, y = 35)
        

        #TextArea de la consola 
        self.txtConsola = scrolledtext.ScrolledText(self.wind,width = 100,height = 10, bg ="#453B46", foreground = "#FFFFFF")
        self.txtConsola.place(x = 40, y =490)
        
        
        


        self.buttonOk.place(x = 900, y =15)
        

    def getText(self):
        entrada = self.textArea.get("1.0",END)

        #self.txtConsola.delete("1.0",END)
        
    
        analizado = self.analizador._incio(entrada)
        self.set_color_palabra(entrada)
        self.setConsola(analizado)
    
        

        
    def setConsola(self,errores):
        self.txtConsola.insert("2.0","")
        texto = ''
        for key,values in errores.items():
            for caracter in values:
                texto += f"Error Lexico in Line:{key}, Carcater:{caracter} \n"
        
        self.txtConsola.insert("2.0",texto)

    
    def color_sintaxisJS(self,palabra):
        listaToken = self.analizador.getListTokens()
        for valor in listaToken:
            if palabra == valor.getValorToken():
                #print(f"token {valor.getValorToken()},color {valor.getColorToken()}")
                self.textArea.highlight_pattern(palabra, valor.getColorToken())
        
    
    
    def open_File(self):
        print('Hola mundo')
        return True
    
    def exit_program(self):
        pass

    def set_color_palabra(self,texto):
        self.entrada  = texto + '$'
        self.cacterActual = ''
        posicion = 0

        while posicion < len(self.entrada):
            self.cacterActual = self.entrada[posicion]

            if self.cacterActual == "{":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == "}":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == "=":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == '(':
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == ")":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual  == ":":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == ";":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == "+":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == "-":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            #elif self.cacterActual == "/":
                #self.add_token(Tipo.division,"/","white")
            elif self.cacterActual == ">":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == "<":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == '"':
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""

            
            # q0 -> q1 Si es numero 
            elif self.cacterActual.isnumeric():
                sizeLexema = self.get_size_lexema(posicion)
                palabra = self.get_lexema(posicion,posicion +sizeLexema)
                self.color_sintaxisJS(palabra)
                posicion = posicion + sizeLexema


            if self.entrada[posicion - 1] == '"':
                sizeLexema = self.get_size_lexemaEspecial(posicion)
                palabra = self.get_lexema(posicion,posicion +sizeLexema)
                self.color_sintaxisJS(palabra)
                posicion = posicion + sizeLexema

            if self.entrada[posicion - 1] == '/' and self.cacterActual == '/':
                sizeLexema = self.get_size_lexemaComentario_un(posicion)
                palabra = self.get_lexema(posicion+1,posicion+sizeLexema)
                self.color_sintaxisJS(palabra)
                posicion = posicion + sizeLexema
            
            if self.entrada[posicion - 1] == '/' and self.cacterActual == '*':
                sizeLexema = self.get_size_lexemaComentario_mul(posicion)
                palabra = self.get_lexema(posicion+1,posicion+sizeLexema)
                self.color_sintaxisJS(palabra)
                posicion = posicion + sizeLexema
             
            if self.cacterActual.isalpha():
                sizeLexema  = self.get_size_lexema(posicion)
                palabra = self.get_lexema(posicion,posicion + sizeLexema);
                #print(palabra)
                self.color_sintaxisJS(palabra)
                posicion = posicion + sizeLexema


            posicion +=1 

        
    def get_size_lexema(self, posInicial):
        longitud = 0
        for i in range(posInicial,len(self.entrada) -1 ):
            if self.entrada[i] == "(" or self.entrada[i] == ")" or self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r"  or self.entrada[i] == "=" or self.entrada[i] == '"' or self.entrada[i] == "//" or self.entrada[i] == "/*" or self.entrada[i] == "*/":
                break
            longitud +=1
        return longitud

    # devuelve la longitul del lexima si esta en "sdf dfad" 
    def get_size_lexemaEspecial(self,inicial):
        longitud = 0
        for i in range(inicial,len(self.entrada) -1 ):
            if self.entrada[i] == "\n" or self.entrada[i] == '"':
                break
            longitud +=1
        return longitud
    
    # devuelve la longitul del lexema si esta en un --> comentario uniliniea
    def get_size_lexemaComentario_un(self,inicial):
        longitud = 0
        for i in range(inicial,len(self.entrada) -1 ):
            if self.entrada[i] == "\n":
                break
            longitud +=1
        return longitud

    # devuelve la longitul del lexema si esta en un --> comentario multilinea
    def get_size_lexemaComentario_mul(self,inicial):
        longitud = 0
        for i in range(inicial,len(self.entrada) -1 ):
            if self.entrada[i] == '*' and self.entrada[i + 1] == '/':
                break
            longitud +=1
        return longitud

        
    def get_lexema(self,actual,fin):
        self.cacterActual = ""
        self.lexema = ""  
        #print(self.entrada[actual:fin])
        return (self.entrada[actual:fin])