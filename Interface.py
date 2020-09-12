from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from io import open
import os
import sys
import msvcrt


from CustomText import CustomText
from Analizador import Analicis
from AnalizadorCSS import Anality_CSS
from AnalizadorHTML import Anality_HTML

class Interface():
    def __init__(self,window):
        self.wind = window
        self.rutaHTML = ''
        self.wind.title('Analysis Application')
        self.wind.geometry("1000x700")
        self.wind.configure(bg = '#0A010B')
        self.textArea = CustomText(self.wind,width = 100,height = 25, bg ="#453B46", foreground = "#FFFFFF")
        self.txtConsola = Entry(self.wind, width = 10)
        self.play_button = PhotoImage(file = 'resource/js.png')
        self.play_css = PhotoImage(file = 'resource/css.png')
        self.play_html = PhotoImage(file = 'resource/HTML.png')
        self.play_button = self.play_button.subsample(10,10)
        self.play_css = self.play_css.subsample(10,10)
        self.play_html = self.play_html.subsample(10,10)
        self.buttonOk = Button(self.wind,image = self.play_button, command = self.getText, bg = "#0A010B", highlightbackground = "#0A010B", highlightcolor= "#0A010B")
        self.buttonOkCSS = Button(self.wind,image = self.play_css, command = self.getTextCSS, bg = "#0A010B", highlightbackground = "#0A010B", highlightcolor= "#0A010B")
        self.buttonOkHTML = Button(self.wind,image = self.play_html, command = self.getTextHTML, bg = "#0A010B", highlightbackground = "#0A010B", highlightcolor= "#0A010B")

        self.lexema = ""
        self.analizador = Analicis()
        self.analizadorCSS = Anality_CSS()
        self.analizadorHTML = Anality_HTML()
        
        self.menu = Menu(self.wind) # Menu Bar
        self.file_item = Menu(self.menu,bg='#374140',activebackground = '#84407B', tearoff=0)
        self.file_item.add_command(label = 'Open File...',command=self.open_File)
        

        self.file_item.add_separator()
        self.file_item.add_command(label = 'Save As JS',command=self.generar_reportJS)
        self.file_item.add_command(label = 'Save As CSS',command=self.generar_reportCSS)
        self.file_item.add_command(label = 'Save As HTML',command=self.generar_reportHTML)

        self.file_item.add_separator()
        self.file_item.add_command(label = 'Exit',command=self.exit_program)

        self.menu.add_cascade(label = 'File',menu=self.file_item)
        self.wind.config(menu = self.menu)

        #TextArea de la entrada
        self.textArea.tag_configure("red", foreground="#ff0000")
        self.textArea.tag_configure("blue", foreground="#004DFF")
        self.textArea.tag_configure("yellow", foreground="#FFF000")
        self.textArea.tag_configure("green", foreground="#00A817")
        self.textArea.tag_configure("gray", foreground="#ABAAAA")
        self.textArea.tag_configure("white", foreground="#FFFFFF")
        self.textArea.tag_configure("anaranjado", foreground="#FF8000")
        self.textArea.place(x = 40, y = 35)
        

        #TextArea de la consola 
        self.txtConsola = scrolledtext.ScrolledText(self.wind,width = 100,height = 10, bg ="#453B46", foreground = "#FFFFFF")
        self.txtConsola.place(x = 40, y =490)
        
        
        


        self.buttonOk.place(x = 900, y =15)
        self.buttonOkCSS.place(x = 900, y = 80)
        self.buttonOkHTML.place(x = 900, y = 145)
        

    def getText(self):
        self.txtConsola.delete("1.0","end")
        entrada = self.textArea.get("1.0",END)

        #self.txtConsola.delete("1.0",END)
        
    
        analizado = self.analizador._incio(entrada)
        self.setConsola(analizado)
        self.set_color_palabra(entrada)
        self.analizador.clear_data()
    
    def getTextCSS(self):
        self.txtConsola.delete("1.0","end")
        entrada = self.textArea.get("1.0",END)

        analizado = self.analizadorCSS.read_caracter(entrada)
        self.setConsolaCSS(analizado)
        self.analizadorCSS.limpiarCarcateres()



    def getTextHTML(self):
        self.txtConsola.delete("1.0","end")
        entrada = self.textArea.get("1.0",END)

        analizado  = self.analizadorHTML.read_caracter(entrada)
        self.setConsolaHTML(analizado)
        #self.analizadorHTML.limpiarCaracter()
        
        # ---------------------------
    
        
 
    
    def setConsola(self,errores):
        self.txtConsola.insert("2.0","")
        texto = ''
        for key,values in errores.items():
            for caracter in values:
                texto += f"Error Lexico in Line:{key}, Carcater:{caracter} \n"
        
        self.txtConsola.insert("2.0",texto)

    def setConsolaCSS(self,listError):
        self.txtConsola.delete("1.0","end")
        texto = ""
        for value in listError:
            texto += f"Error in [ Ln {value.getLinea()} ] , Carcater:{value.getCaracter()} \n"
        self.txtConsola.insert("2.0",texto)


    def setConsolaHTML(self,listaError):
        self.txtConsola.delete("1.0","end")
        texto = ""
        for value in listaError:
            texto += f"Error in [ Ln {value.getLinea()}, Pos {value.getPosicion()} ] , Carcater:{value.getCaracter()} \n"
        self.txtConsola.insert("2.0",texto)
    
    def color_sintaxisJS(self,palabra):
        listaToken = self.analizador.getListTokens()
        for valor in listaToken:
            if palabra == valor.getValorToken():
                #print(f"token {valor.getValorToken()},color {valor.getColorToken()}")
                self.textArea.highlight_pattern(palabra, valor.getColorToken())
    

        

    def open_File(self):
        try:
            ruta =  ""
            #root = Tk()
            filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("JS files","*.js"),("CSS files","*.css"),("HTML files","*.html"),("all files","*.*")))
            ruta = filename
            if ruta != "":
                self.write_consola(ruta)
                return ruta
            else:
                
                return None

        except IndexError as e:
            print(e)

    #Metodo de lectura y escritura de archivo
    def write_consola(self,ruta):
        try:
            archivo = open(f"{ruta}","r")
            texto = archivo.read()
            archivo.close()
            self.textArea.insert("2.0",texto)
            
        except (FileNotFoundError, IOError):
            print("Error en la lectura")
    
    #--------------->Metodo Guardar Reporte<--------------------------------

    def generar_reportJS(self):
        pass
    def generar_reportHTML(self):
        ruta = self.analizadorHTML.get_pathComentario()
        if ruta != ''  and ruta != ' ':
            self.show_windowAux(ruta)
            
        else:
            messagebox.showwarning("ERROR","No se encontro la ruta")
        

    def generar_reportCSS(self):
        pass


    def show_windowAux(self,ruta):
        self.windowAux = Tk()
        self.windowAux.title("Confirmar")
        self.windowAux.geometry('200x120')

        l1 = Label(self.windowAux,text='Ruta',font=(14))
        l1.grid(row = 0,column = 0)

        entradaTxt = Entry(self.windowAux,font=(14))
        entradaTxt.grid(row = 1,column = 0,padx = 5,pady = 5)
        entradaTxt.insert(0,ruta)
        
        
        button = Button(self.windowAux,text=" Ok ",font=(14), command = lambda: self.setRutaHTML(f"{entradaTxt.get()}"))
        button.grid(row=2,column = 0)        

        self.windowAux.mainloop()

    def setRutaHTML(self,ruta):
        self.rutaHTML = ruta
        print(self.rutaHTML)
        self.windowAux.destroy()
        self.analizadorHTML.enviarReporte(self.rutaHTML)
        
        

    #-------------------------><--------------------------------
    
    def exit_program(self):
        sys.exit()

    def set_color_palabra(self,texto):
        self.entrada  = texto + '$'
        self.cacterActual = ''
        posicion = 0

        while posicion < len(self.entrada):
            self.cacterActual = self.entrada[posicion]

            if self.cacterActual == '/' and self.entrada[posicion + 1] == '*':
                caracterDoble = self.cacterActual + self.entrada[posicion + 1]
                self.color_sintaxisJS(caracterDoble)
                self.lexema = ""
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
            elif self.cacterActual == '//':
                self.lexema = ""
            elif self.cacterActual == ">":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == "<":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == '"':
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == '.':
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == '*':
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == "'":
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == '&' and self.entrada[posicion + 1] == '&':
                caracterDoble = self.cacterActual + self.entrada[posicion + 1]
                self.color_sintaxisJS(caracterDoble)
                self.lexema = ""
            elif self.cacterActual == '!':
                self.color_sintaxisJS(self.cacterActual)
                self.lexema = ""
            elif self.cacterActual == '|' and self.entrada[posicion + 1 ] == '|':
                caracterDoble = self.cacterActual + self.entrada[posicion + 1]
                self.color_sintaxisJS(caracterDoble)
                self.lexema = ""

            if self.entrada[posicion - 1] == '"' or self.entrada[posicion - 1] == "'" :
                sizeLexema = self.get_size_lexemaEspecial(posicion)
                palabra = self.get_lexema(posicion,posicion +(sizeLexema -1))
                self.color_sintaxisJS(palabra)
                posicion = posicion + sizeLexema
            

            # q0 -> q1 Si es numero 
            elif self.cacterActual.isnumeric():
                sizeLexema = self.get_size_lexema(posicion)
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
            if self.entrada[i] == "(" or self.entrada[i] == ")" or self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r"  or self.entrada[i] == "=" or self.entrada[i] == '"' or self.entrada[i] == "//" or self.entrada[i] == "/*" or self.entrada[i] == "*/" or self.entrada[i] == ".":
                break
            longitud +=1
        return longitud

    # devuelve la longitul del lexima si esta en "sdf dfad" 
    def get_size_lexemaEspecial(self,inicial):
        longitud = 0
        for i in range(inicial,len(self.entrada) -1 ):
            if self.entrada[i] == '"' or self.entrada[i] == "'":
                break
            longitud +=1
        return longitud + 1
    
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



    