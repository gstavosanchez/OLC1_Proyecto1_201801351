import sys

class Report():
    def __init__(self):
        pass

    def genenarte_Graphivz(self,dic_tranciones):
        bloqueUno = "R[shape=point] \n"
        bloqueDos = ' R -> q0 [arrowhead="dot",color="#832561"] \n'
        for key,values in dic_tranciones.items():
            bloqueUno += '%s [label = "%s"]     \n'%(key,key)
        
        for key,values in dic_tranciones.items():
            for valor in values:
                transicion = valor.split(",")
                bloqueDos += ' %s -> %s [arrowhead="vee",color="#832561", label="%s"] \n'%(key,transicion[1],transicion[0])

        texto = 'digraph G{ \n rankdir=LR; \n node[shape="circle",fontcolor="#832561",color="#B965AE"];\n %s \n %s \n}'%(bloqueUno,bloqueDos)
        print(texto)

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

    def writeReporte(self,ruta,texto,lista_error):
        #print(f"Generando Reporte en :{ruta}")
        try:
            report = self.reporteHTMLCSS(texto,lista_error)
            archivo  = open(f"{ruta}","a",encoding="utf-8")
            report = f"{report}\n"
            archivo.writelines(report)
            archivo.close()
        except OSError as e:
            print("Os error:{0}".format(e))
        
