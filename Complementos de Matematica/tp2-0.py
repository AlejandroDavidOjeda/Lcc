#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Complementos Matematicos I
# Trabajo practico final


import argparse
from grafo import *
import math
import Gnuplot
import time

'''
Clase utilizada para graficar un grafo
'''
class LayoutGraph():

    '''
    * rutaGrafo: Ruta del archivo de grafo
    * iters: Iteraciones a realizar
    * refresh: Indica cada cuantas iteraciones se debe dibujar el grafo, 0 para no imprimir intermedios
    * c_fuerza: constante usada para calculo de fuerzas
    * c_grav: constante de la gravedad
    * t_init: temperatura inicial
    * t_factor: factor de disminucion de la temperatura
    * verbose: indica si debe imrpimirse informacion extra durante el funcionamiento
    '''
    def __init__(self , rutaGrafo , iters , refresh , c_fuerza , c_grav , t_init , temp_factor , verbose):
        #Instancia el graficador
        self.g = Gnuplot.Gnuplot()

        # Crea el grafo
        self.grafo = Grafo(rutaGrafo)

        # Guarda opciones
        self.iters = iters
        self.verbose = verbose
        self.refresh = refresh
        self.c_fuerza = c_fuerza
        self.c_grav = c_grav
        self.temp = t_init
        self.t_factor = temp_factor

        #Calculos extras
        self.k = c_fuerza * math.sqrt((MAX_X*MAX_Y) / len(self.grafo.nodos));


    '''
    Inicializa en forma aleatoria las posiciones de los nodos
    Al parsear intenta abrir el archivo en caso de no poder Falla
    Para mas informacion revisar el archivo grafo.py
    '''
    def randomize(self):
        self.grafo.randomize()

    '''
    Calcula la fuerza de repulsion entre dos nodos
    * n1, n2: Nodos a aplicar la fuerza de repulsion (solo lo aplica a la primera)
    '''
    def fuerza_repulsion(self , n1 , n2):
        # Distancia entre los vectores
        distancia = math.sqrt((n2.x - n1.x)**2 + (n2.y - n1.y)**2)

        #Magnitud del vector
        f = (self.k**2) / distancia

        #Hace la diferencia de vectores
        x = n1.x - n2.x
        y = n1.y - n2.y

        # Normaliza el vector
        x /= distancia
        y /= distancia

        #Controla la magnitud del vector
        x *= f
        y *= f

        #Actualiza fuerza
        self.grafo.agregaFuerza(n1 , x , y)

    '''
    Calcula la fuerza de atraccion entre dos nodos
    '''
    def fuerza_atraccion(self, n1, n2):
        # Distancia entre los nodos
        distancia = math.sqrt((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2)

        # Constante para la fuerza
        f = (distancia ** 2) / self.k

        # Calcula el vector direccion
        x = n2.x - n1.x
        y = n2.y - n1.y
        mod = math.sqrt(distancia)

        #Normaliza el vector
        x /= mod
        y /= mod

        # Regula el modulo del vector
        x *= f
        y *= f

        # Actualiza las fuerzas
        self.grafo.agregaFuerza(n1 , x , y)
        self.grafo.agregaFuerza(n2 , -x , -y)


    '''
    Calcula la fuerza de la gravedad
    * nodo: Nodo a aplicar la fuerza de gravedad
    '''
    def fuerza_grav(self , nodo):
        #Punto del centro
        cx = MAX_X / 2
        cy = MAX_Y / 2

        # Calcula el cector de gravedad
        x = cx - nodo.x
        y = cy - nodo.y
        mod = math.sqrt((x**2) + (y**2))

        #Normaliza
        x /= mod
        y /= mod

        #Calcula magnitud del vector de fuerza
        f = self.c_grav * mod**2

        #Controla la magnitud del vector
        x *= f
        y *= f

        #Actualiza la fuerza
        self.grafo.agregaFuerza(nodo , x , y)

    '''
    Actualiza las fuerzas
    * nodo: nodo a aplicar la fuerza
    '''
    def actualizaFuerzas(self , nodo):
        fuerza = self.grafo.obtenerFuerza(nodo)

        # Precalcula variables
        x = fuerza[0]
        y = fuerza[1]
        mag = math.sqrt(x**2 + y**2)

        # Limita las magnitudes con la temperatura
        if mag > self.temp:
            x = (x / mag) * self.temp
            y = (y / mag) * self.temp

        # Actualiza la posicion
        x += nodo.x
        y += nodo.y
        nodo.configurarPosicion(x , y)
        return


    '''
    Efectua un paso de la simulacion fisica y actualiza las posiciones de los nodos
    '''
    def paso(self):
        #Variables temporales
        nodos = self.grafo.nodos
        aristas = self.grafo.aristas

        # 1: Calcula las fuerzas de atraccion
        for n1 in nodos:
            for n2 in nodos:
                if n1 != n2:
                    self.fuerza_repulsion(n1 , n2)


        # 2: Calcular atracciones de aristas
        for arc in aristas:
            self.fuerza_atraccion(arc[0], arc[1])

        # 3: Calcular fuerza de gravedad (opcional)
        for n in nodos:
            self.fuerza_grav(n)

        # 4: En base a fuerzas, actualizar posiciones
        for n in nodos:
            self.actualizaFuerzas(n)

        # 5: Actualiza el valor de la temperatura y reinicia las fuerzas
        self.temp -= self.t_factor
        self.grafo.reiniciaFuerzas()

        #Imprime las posiciones de los nodos
        if self.verbose:
            self.grafo.imprimeInformacion()
        return


    '''
    Dibuja (o actualiza) el estado del grafo gr en pantalla
    '''
    def dibujar(self):
        #Setea el tamano del plano
        if MAX_X == MAX_Y:
            self.g('set size square')
            self.g('set xrange [0:{0}]; set yrange [0:{0}]'.format(MAX_X))
        else:
            self.g('set xrange [0:{0}]; set yrange [0:{1}]'.format(MAX_X , MAX_Y))

        #Titulo de la ventana
        self.g('set title "Graph"')

        #Grafica los nodos
        i = 1
        for nodo in self.grafo.nodos:
            self.g('set object {0} circle center {1},{2} size {3} fc rgb "black"'.format(i, nodo.x, nodo.y, NODO_R))
            i = i + 1

        #Grafica las aristas
        i = 1
        for (n1 , n2) in self.grafo.aristas:
            self.g('set arrow {0} nohead from {1},{2} to {3},{4}'.format(i, n1.x, n1.y, n2.x, n2.y))
            i = i + 1

        # Borra leyenda
        self.g('unset key')
        # Dibujar
        self.g('plot NaN')

        time.sleep(2)
        self.g('replot')

        #Imprime las posiciones de los nodos
        if self.verbose:
            self.grafo.imprimeInformacion()
        return


    '''
    Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
    un layout
    '''
    def layout(self):

        # Inicializamos las posiciones
        if self.verbose:
            print "Randomize:"
        self.randomize()

        #Imprime la informacion del grafo inicial
        if self.verbose:
            self.grafo.imprimeInformacion(imprimirAristas=True)

        # Si es necesario, lo mostramos por pantalla
        if (self.refresh > 0):
            if self.verbose:
                print "Primer Dibujo:"
            self.dibujar()


        # Bucle principal
        for i in range(self.iters):
            # Realizar un paso de la simulacion
            if self.verbose:
                print "Paso %s" % (i + 1)
            self.paso()

            # Si es necesario, lo mostramos por pantalla
            if (self.refresh > 0 and i % self.refresh == 0):

                if self.verbose:
                    print "Dibujo"
                self.dibujar()

        # Ultimo dibujado al final
        if self.verbose:
            print "Dibujo Final"
        self.dibujar()


'''
Metodo que lanza el graficador
'''
def main():
    # Definimos los argumentos de lina de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Ruta del archivo de grafo
    parser.add_argument('--ruta' ,
                        type=str,
                        help='Ruta del archivo de grafo',
                        required= True)

    # Verbosidad, opcional
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Imprime toda la información del proceso')

    # Cantidad de iteraciones
    parser.add_argument('--iters',
                        type=int,
                        help='Cantidad de iteraciones a efectuar',
                        default=50)

    # Indica cada cuantas iteraciones debe graficarse el grafo
    parser.add_argument('--refresh' ,
                        type=int,
                        help='Indica cada cuantas iteraciones debe dibujarse el grafo',
                        default=25)

    # Constante de fuerzas
    parser.add_argument('--c_fuerza' ,
                        type=float,
                        help='Constante de fuerza',
                        default=0.5)

    # Constante de gravedad
    parser.add_argument('--c_grav' ,
                        type=float,
                        help='Constante de fuerza de gravedad',
                        default=0.003)

    # Temperatura inicial
    parser.add_argument('--t_init' ,
                        type=int,
                        help='Temperatura inicial',
                        default=50)

    #Constante de decremento de Temperatura
    parser.add_argument('--t_factor' ,
                        type=int,
                        help='Constante de disminucion de temperatura',
                        default=1)

    # Parsea
    args = parser.parse_args()


    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        rutaGrafo=args.ruta,
        iters=args.iters,
        refresh = args.refresh,
        verbose=args.verbose,
        c_fuerza=args.c_fuerza,
        c_grav=args.c_grav,
        t_init=args.t_init,
        temp_factor=args.t_factor
        )

    # Ejecutamos el layout
    layout_gr.layout()
    return

'''
Lanza el script
'''
if __name__ == '__main__':
    main()
