import sys
import os
class Report():
    rutaJs = ''
    text_RecuperacionError = ''
    ruta_generica = ''
    def __init__(self):
        self.rutaJs = ''
        self.ruta_generica = ''
        self.text_RecuperacionError = ''

    def genenarte_Graphivz(self,dic_tranciones):
        bloqueUno = "R[shape=point] \n"
        bloqueDos = ' R -> q0 [arrowhead="dot",color="#832561"] \n'
        caracter = ''
        for key,values in dic_tranciones.items():
            bloqueUno += '%s [label = "%s"]     \n'%(key,key)
        
        for key,values in dic_tranciones.items():
            for valor in values:
                transicion = valor.split(",")
                caracter = transicion[0]
                if caracter.find("\\") != -1:
                    caracter = caracter.replace("\\",'/')
                    #print(f"entra al primer if:{caracter}")
                if caracter.find('"') != -1:
                    caracter = caracter.replace('"',"'")
                    #print(f"entra al 2 if:{caracter}")

                
                bloqueDos += ' %s -> %s [arrowhead="vee",color="#832561", label="%s"] \n'%(key,transicion[1],caracter)

        texto = 'digraph G{ \n rankdir=LR; \n node[shape="circle",fontcolor="#832561",color="#B965AE"];\n %s \n %s \n}'%(bloqueUno,bloqueDos)
        return texto

    def genearete_bitacora(self,dic_tranciones):
        for kye,values in dic_tranciones.items():
            for valor in values:
                pass

    def solunionarError(self,texto,listaError):
        x = 0
        self.cActual = ''
        self.entrada = texto
        newTexto = ''
        while x < len(self.entrada):
            self.cActual = self.entrada[x]
            if (self.exist_error(x,listaError) == False):
                newTexto += self.cActual

            x += 1
        return newTexto
    
    def exist_error(self,posicion,listaError):
        for error in listaError:
            if (posicion ==  error.getPosicion()):
                return True
        return False
    
    def reporteHTMLCSS(self,texto,lista_Error):
        x = 1
        newTexto = self.solunionarError(texto,lista_Error)
        self.text_RecuperacionError = newTexto
        head = '<head> \n \t<meta charset="UTF-8">\n \t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n \t<title>Report</title>\n \t <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/minty/bootstrap.min.css" integrity="sha384-H4X+4tKc7b8s4GoMrylmy2ssQYpDHoqzPa9aKXbDwPoPUA3Ra8PA5dGzijN+ePnH" crossorigin="anonymous">\n </head>\n'
        bloqueUno = '\t<table class="table table-hover">\n \t \t <tr> \n \t \t \t <td scope="col"><strong>No.</strong></td>\n \t \t \t <td scope="col"><strong>Linea</strong></td>\n \t \t \t <td scope="col"><strong>Caracter</strong></td> \n \t \t </tr>\n'
        bloqueDos = ''
        for error in lista_Error:
            caracter = f"El carcter '{error.getCaracter()}' no pertenece al lenguaje."
            bloqueUno += '\t \t<tr>\n \t \t \t<td scope="col">%s</td>\n \t \t \t<td>%s</td>\n \t \t \t<td>%s</td> \n \t \t </tr>\n \n'%(x,error.getLinea(),caracter)
            x += 1
        bloqueUno += '\t</table>\n'
        bloqueDos += '\t<h2>Recuperacion de Error</h2>\n \t <p>%s</p>\n </br>\n </br>\n </br>\n </br>\n </br> \n \t <footer> \n \t \t <p><strong>Author: Elmer Gustavo Sanchez Garcia </strong></p>\n \t \t <p><a href="https://github.com/gstavosanchez/OLC1_Proyecto1_201801351"><em>Repo GitHub </em></a></p>\n \t </footer>'%(newTexto)
        bloquePrincipal = '<!DOCTYPE html>\n <html lang="en">\n %s \n <body>\n <h1>Listado Errores lexicos</h1>\n %s \n %s \n </body>\n </html>\n'%(head,bloqueUno,bloqueDos)

        #print(bloquePrincipal)
        return bloquePrincipal

    def writeReporte(self,ruta,texto,lista_error,tipo):
        #print(f"Generando Reporte en :{ruta}")
        name = os.path.split(ruta)
        if(name[1] != ""):
            if (os.path.isdir(name[0]) == False):
                os.makedirs(name[0])

            try:
                report = self.reporteHTMLCSS(texto,lista_error)
                archivo  = open(f"{ruta}","w",encoding="utf-8")
                report = f"{report}\n"
                archivo.writelines(report)
                archivo.close()
            except OSError as e:
                print("Os error:{0}".format(e))
                os.makedirs(name[0])
                self.writeReporte(ruta,texto,lista_error,tipo)
                #return

            #----------------Rutas------------------------------------
            #----------------JS------------------------------------
            if tipo == 'js':
                self.rutaJs = ruta
            #----------------CSS------------------------------------
            elif tipo == 'css':
                self.ruta_generica = ruta
                pathCSS = self.get_path(tipo)
                self.write_Any_Archivo(self.text_RecuperacionError,pathCSS)
                self.text_RecuperacionError = ''

            #----------------HTML------------------------------------    
            elif tipo == 'html':
                self.ruta_generica = ruta
                pathHTML = self.get_path(tipo)
                self.write_Any_Archivo(self.text_RecuperacionError,pathHTML)
                self.text_RecuperacionError = ''
            #--------------------------------------------------------
            
        else:
            print("No existe el nombre el archivo")

    #----------------Reportes JS------------------------------------

    def generate_ReportGraphiv(self,dic_tranciones):
        #--------------Rutas---------------------------
        path = os.path.split(self.rutaJs)
        path_name = path[1].split('.')
        path_name = path_name[0]

        path_imagen = f"{path[0]}\{path_name}.png"
        path_dot = f"{path[0]}\{path_name}.dot"
        path_js = f"{path[0]}\{path_name}_SE.js"

        comando = 'dot -Tpng "%s" -o "%s"'%(path_dot,path_imagen)

        #--------------Recuperacion de errores---------------------------
        self.write_Any_Archivo(self.text_RecuperacionError,path_js)
        self.text_RecuperacionError = ''
        #--------------Generar Graphviz---------------------------
        text_Graphiv = self.genenarte_Graphivz(dic_tranciones)
        self.write_Any_Archivo(text_Graphiv,path_dot)
        #--------------------Ejecutar Comanod del .dot---------------
        self.ejecutar_Comando(comando)
        self.rutaJs = ''

    #----------------Retorno Rutas------------------------------------
    def get_path(self,tipo):
        path = os.path.split(self.ruta_generica)
        path_name = path[1].split('.')
        path_name = path_name[0]
        path_generica = f"{path[0]}\{path_name}_SE.{tipo}"
        self.ruta_generica = ''
        return path_generica


    #----------------Escribir cualquier tipo de archivo------------------------------------
    def write_Any_Archivo(self,texto,ruta):
        archivo  = open(f"{ruta}","w",encoding="utf-8")
        texto = f"{texto}\n"
        archivo.writelines(texto)
        archivo.close()

    def ejecutar_Comando(self,commando):
        os.system (commando)


    def reporte_sintactico(self,ruta,estado,cadena):
        reporte = self.generate_report_sintac(estado,cadena)
        self.write_Any_Archivo(reporte,ruta)
            
    def generate_report_sintac(self,estado,cadena):
        x = 1
        head = '<head> \n \t<meta charset="UTF-8">\n \t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n \t<title>Report</title>\n \t <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/minty/bootstrap.min.css" integrity="sha384-H4X+4tKc7b8s4GoMrylmy2ssQYpDHoqzPa9aKXbDwPoPUA3Ra8PA5dGzijN+ePnH" crossorigin="anonymous">\n </head>\n'
        bloqueUno = '\t<table class="table table-hover">\n \t \t <tr> \n \t \t \t <td scope="col"><strong>No.</strong></td>\n \t \t \t <td scope="col"><strong>Cadena</strong></td>\n \t \t \t <td scope="col"><strong>Estado</strong></td> \n \t \t </tr>\n'
        bloqueDos = ''
        
        caracter = estado
        bloqueUno += '\t \t<tr>\n \t \t \t<td scope="col">%s</td>\n \t \t \t<td>%s</td>\n \t \t \t<td>%s</td> \n \t \t </tr>\n \n'%(x,cadena,caracter)
        x += 1
        bloqueUno += '\t</table>\n'
        bloqueDos += '\t</br>\n </br>\n </br>\n </br>\n </br> \n \t <footer> \n \t \t <p><strong>Author: Elmer Gustavo Sanchez Garcia </strong></p>\n \t \t <p><a href="https://github.com/gstavosanchez/OLC1_Proyecto1_201801351"><em>Repo GitHub </em></a></p>\n \t </footer>'
        bloquePrincipal = '<!DOCTYPE html>\n <html lang="en">\n %s \n <body>\n <h1>Listado Errores Sintactico</h1>\n %s \n %s \n </body>\n </html>\n'%(head,bloqueUno,bloqueDos)

        #print(bloquePrincipal)
        return bloquePrincipal
