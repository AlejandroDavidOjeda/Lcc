# -*- coding: utf-8 -*-
from sys import exit
import random

#Dimensiones del plano
MAX_X = 600
MAX_Y = 400

#Radio del nodo
NODO_R = 2

'''
Clase que representa un vertice de grafo
'''
class Nodo:

    '''
    Crea un vertice
    * etiqueta: etiqueta del nodo
    * x,y: posicion del nodo
    '''
    def __init__(self , etiqueta , x=0.0 , y=0.0):
        self.x = x
        self.y = y
        self.etiqueta = etiqueta

    '''
    Setea la posicion del vertice
    '''
    def configurarPosicion(self , x , y):
        self.x = x
        self.y = y

'''
Clase que representa un grafo
'''
class Grafo:

    '''
    Crea el grafo
    * ruta: ruta del archivo de grafo
    '''
    def __init__(self , ruta):
        #instancia componentes
        self.nodos = []
        self.aristas = []
        self.fuerzas = {}

        #parsea la entrada
        nodos, aristas = self.parsearGrafo(ruta)

        #Convierte el grafo temporal en un grafo valido para el sistema
        for p in nodos:
            temp = Nodo(p)
            self.nodos.append(temp)
            self.fuerzas[temp] = [float(0) , float(0)]
        for e in aristas:
            n1, n2 = e
            self.aristas.append((self.obtenerNodo(n1), self.obtenerNodo(n2)))

    '''
    Lee un grafo desde un archivo y devuelve su representacion como lista.
    Ejemplo Entrada:
        3
        A
        B
        C
        A B
        B C
        C B
    Ejemplo de retorno:
        ([A,B,C],[(A,B),(B,C),(C,B)])
    '''
    def parsearGrafo(self , ruta):
        try:
            # Abre el archivo
            with open(ruta, "r") as f:
                nodos = []
                aristas = []

                lineas = [x.rstrip("\n") for x in f.readlines()]

                cant_nodos = int(lineas.pop(0))

                #agrega los vertices a la lista
                for i in range(cant_nodos):
                    nodos.append(lineas.pop(0))

                #Agrega las aristas
                for dato in lineas:
                    temporal = dato.split(" ")
                    if len(temporal) < 2:
                        self._terminaProgramaPorError("Una arista tiene dos vértices!!")

                    if not self._validarnodos(temporal, nodos):
                        self._terminaProgramaPorError("Nodos %s no registrados" % temporal)
                    aristas.append((temporal[0], temporal[1]))

                return (nodos, aristas)
        except:
            self._terminaProgramaPorError("No se ha podido cargar ningún grafo")

    '''
    Termina el programa en caso de detectarse algún error irrecuperable XD
    * mensaje: Mensaje a imprimir
    '''
    def _terminaProgramaPorError(self, mensaje):
        print "ERROR > " + mensaje
        exit(0)

    '''
    Retorna true si la arista es variables
    Arguments:
    * dato: lista con los nodos
    * lista: Lista de nodos
    '''
    def _validarnodos(self, dato, lista):
        a = dato[0]
        b = dato[1]
        return (a in lista) and (b in lista)

    '''
    Imprime la informacion del grafo
    imprimirAristas esta en False por defecto para no imprimer en cada una de las iteraciones las
    aristas, ya que estas no cambian, con lo que imprimirlas la primera vez alcanza.
    '''
    def imprimeInformacion(self, imprimirAristas=False):
        #Imprime los nodos
        print "Nodos:"
        for nodo in self.nodos:
            print "*>{0}: X={1} - Y={2}".format(nodo.etiqueta, nodo.x, nodo.y)

        #Imprime las aristas
        if imprimirAristas:
            print "Aristas:"
            for (n1, n2) in self.aristas:
                print "*>{0} -> {1}".format(n1.etiqueta, n2.etiqueta)

    '''
    Posiciona los nodos de manera pseudo aleatoria en el plano
    '''
    def randomize(self):
        # Precalculos
        factor = 4
        tx = MAX_X / factor
        ty = MAX_Y / factor

        #Seteo de las posiciones
        for v in self.nodos:
            x = random.uniform(tx , MAX_X - tx)
            y = random.uniform(ty , MAX_Y - ty)
            v.configurarPosicion(x , y)


    '''
    Dada una etiqueta se obtiene un nodo
    '''
    def obtenerNodo(self , etiqueta):
        for n in self.nodos:
            if n.etiqueta == etiqueta:
                return n
        return None

    '''
    Dado un nodo retorna la fuerza que se le debe aplicar
    '''
    def obtenerFuerza(self , nodo):
        return self.fuerzas[nodo]

    '''
    Agrega una fuerza al verctor de fuerzas de un nodo
    * nodo: nodo al cual se aplica la fuerza
    * x, y: fuerza a aplicar
    '''
    def agregaFuerza(self, nodo, x, y):
        self.fuerzas[nodo][0] += x
        self.fuerzas[nodo][1] += y

    '''
    Reinicia las fuerzas
    '''
    def reiniciaFuerzas(self):
        for k in self.fuerzas.keys():
            self.fuerzas[k] = [0,0]
