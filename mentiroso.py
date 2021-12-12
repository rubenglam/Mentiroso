
import random
from random import seed
from random import randint

palos = ['Oros', 'Espadas', 'Bastos', 'Copas']

class Carta:
   
    def __init__(self, numero, palo):
        self.numero = numero
        self.palo = palo

class Baraja:
    
    def __init__(self):
        self.cartas = []
    
    def mezclar(self):
        random.shuffle(self.cartas)

class Jugador:
    
    def __init__(self, name, mesa):
        self.name = name
        self.mano = []
        self.mesa = mesa
        self.ganador = False

    def comer(self):
        size = self.mesa.cartas
        for i in range(size):
            self.mano.append(self.mesa.cartas[0])
            self.mesa.cartas.pop(0)
        self.descarte()

    def ordenar_mano(self):
        sorted(self.mano, key=lambda carta: carta.numero)

    def descarte(self):
        iguales = 0
        self.ordenar_mano()
        for i in range(len(self.mano) - 1):
            if self.mano[i + 1].numero == self.mano[i].numero:
                iguales += 1
                if iguales == 3:
                    #Cuando se borra se sigue sumando i y se queda fuera de rango, hay que borrar sin que interfiera con la i
                    if self.mano[i].numero != '0':
                        for j in range(1, 5):
                            self.mano.pop(i - 3)
            else:
                iguales == 0

class Jugada:
    
    def __init__(self, jugador, mesa):
        self.jugador = jugador
        self.verdad = True
        self.cartas_seleccionadas = []
        self.palabreo = None
        self.mesa = mesa

    def ejecutar(self):
        if self.turno == 0:
            self.jugada_inicial()
        else:
            self.jugada_no_inicial()
        self.turno += 1
        
    def jugada_inicial(self):
        self.seleccionar_cartas()
        self.palabrear()

    def jugada_no_inicial(self):
        self.adivinar()
        self.check_verdad()

    def seleccionar_cartas(self):
        print("Qué cartas quiere jugar?")
        carta = input()
        copia_mano = self.jugador.mano
        borrar = []
        while carta != 'jugar':
            if len(self.cartas_seleccionadas) < 3:
                self.cartas_seleccionadas.append(copia_mano[int(carta)])
                borrar.append(int(carta))
            else:
                print('No se pueden jugar más de 3 cartas.')
            carta = input()
        for i in range(len(borrar)):
            if i > 0:
                if borrar[i] > borrar[i -1]:
                    self.jugador.mano.pop(int(borrar[i]))
                else:
                    self.jugador.mano.pop(int(borrar[i]))
            else:
                self.jugador.mano.pop(int(borrar[i]))
  
    def palabrear(self):
        print('Qué número dice que es?')
        self.palabreo = input()
        self.check_verdad()

    def check_verdad(self):
        n_cartas = len(self.cartas_seleccionadas)
        for i in range(n_cartas):
            if self.cartas_seleccionadas[i].numero == '0':
                continue
            if self.cartas_seleccionadas[i].numero != self.palabreo:
                self.verdad = False

    def adivinar(self):
        print("Desea levantar?")
        respuesta = input()
        if respuesta == 's':
            self.mesa.levantar()
        elif respuesta == 'n':
            if len(self.mesa.jugador_anterior.mano) == 0:
                self.mesa.jugador_anterior.ganador = True
            self.seleccionar_cartas()
        else:
            print("Conteste: 's' / 'n'")
     
class Mesa:
    def __init__(self):
        self.jugadas = []
        self.cartas = []
        self.turno = 0
        self.jugador = None
        self.jugador_anterior = None

    def reset(self):
        self.jugadas = []
        self.cartas = []
        self.turno = 0
    
    def hacer_jugada(self, jugador):
        jugada = Jugada(jugador, self)
        self.jugador = jugador
        self.jugadas.append(jugada)
        if self.turno == 0:
            jugada.jugada_inicial()
        else:
            jugada.jugada_no_inicial()
            ultima_jugada = self.jugadas[len(self.jugadas) - 1]
            self.jugador_anterior = ultima_jugada.jugador
        self.dejar_cartas()            
        self.turno += 1
        
    def levantar(self):
        ultima_jugada = self.jugadas[len(self.jugadas) - 1]
        if ultima_jugada.verdad:
            self.jugador.comer()
            if len(ultima_jugada.jugador.mano) == 0:
                ultima_jugada.jugador.ganador = True
        else:
            ultima_jugada.jugador.comer()
        self.reset()

    def dejar_cartas(self): 
        ultima_jugada = self.jugadas[len(self.jugadas) - 1]
        n_cartas = len(ultima_jugada.cartas_seleccionadas) 
        for i in range(n_cartas):
            self.cartas.append(ultima_jugada.cartas_seleccionadas[0]) 
            ultima_jugada.cartas_seleccionadas.pop(0)       

class Partida:
    
    def __init__(self):
        self.jugadores = []
        self.baraja = None 
        self.mesa = None
        self.crear_partida()

    def crear_partida(self):
        self.crear_mesa()
        self.init_jugadores()
        self.crear_baraja()
        self.baraja.mezclar()
        self.repartir()
        self.mostrar_manos()
        self.empezar()

    def init_jugadores(self):
        i = 1
        print('Jugador', str(i) + ':')
        nombre = input()
        while nombre != 'stop':
            jugador = Jugador(nombre, self.mesa)
            self.jugadores.append(jugador)
            i += 1
            print('Jugador', str(i) + ':')
            nombre = input()

    def repartir(self):
        numero = len(self.jugadores)
        while len(self.baraja.cartas) > 0:
            for i in range(numero):
                self.jugadores[i].mano.append(self.baraja.cartas[0])
                self.baraja.cartas.pop(0)
        for i in range(numero):
            self.jugadores[i].descarte()

    def crear_baraja(self):
        self.baraja = Baraja()
        for i in range(1, 5):
            carta = Carta(0, 'Joker')
            self.baraja.cartas.append(carta)
        for i in range(1, 13):
            for j in range(4):
                carta = Carta(i, palos[j])
                self.baraja.cartas.append(carta)
        self.ajustar()

    def crear_mesa(self):
        self.mesa = Mesa()

    def ajustar(self):
        sobrante = len(self.baraja.cartas) % len(self.jugadores)
        for i in range(sobrante):
            self.baraja.cartas.pop(0)

    def mostrar_baraja(self):
        length = len(self.baraja.cartas)   
        for i in range(length):
            print(self.baraja.cartas[i].numero, self.baraja.cartas[i].palo)

    def mostrar_manos(self):
        n_jugadores = len(self.jugadores)
        for i in range(n_jugadores):
            print(self.jugadores[i].name + ':')
            for j in range(len(self.jugadores[i].mano)):
                print(self.jugadores[i].mano[j].numero, self.jugadores[i].mano[j].palo)
            print(' ')

    def empezar(self):
        seed(1)
        j = len(self.jugadores)
        indice = randint(0, j)
        if indice > (len(self.jugadores) - 1):
            indice = - 1
        print("Empieza " + self.jugadores[indice + 1].name + '!')
        self.jugar(indice)
    
    def jugar(self, indice):
        while not self.hay_ganador():
            if indice + 1 > (len(self.jugadores) - 1):
                indice = -1
            self.mesa.hacer_jugada(self.jugadores[indice + 1])
            self.mostrar_manos()
            indice += 1
        if self.hay_ganador():
            self.declarar_ganador()
                
    def hay_ganador(self):
        size = len(self.jugadores)
        encontrado = False
        for i in range(size):
            if self.jugadores[i].ganador:
                encontrado = True
        return encontrado
            
    def declarar_ganador(self):
        print("Ha ganado" + self.mesa.jugador_anterior.name + '!')

    def encontrar_indice_jugador(self, jugador):
        return self.jugadores.index(jugador)

def main():
    partida = Partida()

main()
