
import random
from random import seed
from random import randint

palos = ['Oros', 'Espadas', 'Bastos', 'Copas']

class Carta:
   
    def __init__(self, numero, palo):
        self.numero = numero
        self.palo = palo

class Baraja:
    
    def __init__(self, n_jugadores):
        self.cartas = []
        self.n_jugadores = n_jugadores
        self.constructor()

# Crea una baraja ya mezclada
    def constructor(self): 
        self.crear_baraja()
        self.ajustar()
        self.mezclar()
    
    def mezclar(self):
        random.shuffle(self.cartas)

# Crea una baraja española ordenada con 4 Jokers
    def crear_baraja(self):
        for i in range(1, 5):
            carta = Carta(0, 'Joker')
            self.cartas.append(carta)
        for i in range(1, 13):
            for j in range(4):
                carta = Carta(i, palos[j])
                self.cartas.append(carta)


# Ajusta el numero de cartas de la baraja dependiendo del numero de jugadores para que todos tengan el mismo numero de cartas
    def ajustar(self):
        sobrante = len(self.cartas) % self.n_jugadores
        for i in range(sobrante):
            self.cartas.pop(0)    

class Jugador:
    
    def __init__(self, name, mesa):
        self.name = name
        self.mano = []
        self.mesa = mesa
        self.ganador = False
        self.ha_comido = False

    # A un jugador se le añaden a su mano todas las cartas que haya jugadas en la mesa
    def comer(self):
        for i in self.mesa.cartas:
            self.mano.append(i)
        self.mesa.cartas.clear()
        self.descarte()
        self.ha_comido = True

    def ordenar_mano(self):
        self.mano = sorted(self.mano, key=lambda carta: carta.numero)

    # Cuando hay 4 cartas iguales en la mano que no sean Joker, las descarta de la mano y las elimina
    def descarte(self):
        repetidos = 0
        localizador = 0
        numero = None
        self.ordenar_mano()
        for i in range(len(self.mano) - 1):
            if self.mano[i + 1].numero == self.mano[i].numero:
                repetidos += 1
                if repetidos > 2:
                    localizador = i
                    numero = self.mano[localizador].numero
            else:
                repetidos = 0
        if repetidos > 2 and numero != '0':
            for i in range(len(self.mano) - 1, 0):
                if self.mano[i] == numero:
                   self.mano.pop(i)

class Jugada:
    
    def __init__(self, jugador, mesa):
        self.jugador = jugador
        self.verdad = True
        self.cartas_seleccionadas = []
        self.palabreo = None
        self.mesa = mesa

    # Se elije si se hace una jugada inicial o jugada no inicial dependiendo del turno que sea
    def ejecutar(self):
        if self.turno == 0:
            self.jugada_inicial()
        else:
            self.jugada_no_inicial()
        self.turno += 1

    # Primero selecciona las cartas que quiere jugar y luego dice que numero es al resto de jugadores 
    def jugada_inicial(self):
        self.seleccionar_cartas()
        self.palabrear()
        self.check_verdad()

    def jugada_no_inicial(self):
        self.adivinar()
        self.check_verdad()

    # Se seleccionan las cartas que se quieren jugar y se guardan en un array. Esas cartas se quitan de la mano del jugador
    # ! ESTE METODO ES DEL DIABLO. LEERLO ES PELIGROSO
    def seleccionar_cartas(self):
        copia_mano = self.jugador.mano
        borrar = []
        print("Qué cartas quiere jugar?")        
        carta = input()
        while carta != 'jugar':
            if len(self.cartas_seleccionadas) < 3:
                if int(carta) < 0 or int(carta) >= len(self.jugador.mano):
                    print("Debe introducir un número entre 0 y", str(len(self.jugador.mano) - 1))
                    print("Qué cartas quiere jugar?")
                    carta = input()
                    continue
                if len(borrar) > 0:
                    for i in borrar:
                        if int(carta) == i:
                            print("Ya se ha seleccionado esta carta, pruebe con otra")
                            print("Qué cartas quiere jugar?")
                            carta = input()
                            break 
                    continue
                self.cartas_seleccionadas.append(copia_mano[int(carta)])
                borrar.append(int(carta))
            else:
                print('No se pueden jugar más de 3 cartas.')
            print("Qué cartas quiere jugar?")
            carta = input()
        restador = 0
        for i in range(len(borrar)):
            if i > 0:
                if borrar[i] > borrar[i - 1]:
                    restador += 1
                    self.jugador.mano.pop(int(borrar[i - restador]))
                else:
                    self.jugador.mano.pop(int(borrar[i]))
            else:
                self.jugador.mano.pop(int(borrar[i]))
        self.mesa.dejar_cartas()
  
    def palabrear(self):
        self.palabreo = input('Qué número dice que es? ')

    def check_verdad(self):
        n_cartas = len(self.cartas_seleccionadas)
        for i in range(n_cartas):
            if self.cartas_seleccionadas[i].numero == '0':
                continue
            if self.verdad and (self.cartas_seleccionadas[i].numero != self.palabreo):
                self.verdad = False

    def adivinar(self):
        respuesta = input("Desea levantar? ")
        if respuesta == 's':
            self.mesa.levantar()
            if not self.jugador.ha_comido:    
                self.jugada_inicial()
            else:
                self.jugador.ha_comido = False
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
        self.jugadas = [self.jugadas[len(self.jugadas) - 1]]
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
            if len(self.jugadas) != 0:
                ultima_jugada = self.jugadas[len(self.jugadas) - 1]
                self.jugador_anterior = ultima_jugada.jugador
        self.pasar_turno()
        
    def pasar_turno(self):
        self.jugador_anterior = self.jugador            
        self.turno += 1

    def levantar(self):
        ultima_jugada = self.jugadas[len(self.jugadas) - 2]
        if ultima_jugada.verdad:
            self.jugador.comer()
            if len(ultima_jugada.jugador.mano) == 0:
                ultima_jugada.jugador.ganador = True
        else:
            ultima_jugada.jugador.comer()
        self.reset()

    def dejar_cartas(self): 
        ultima_jugada = self.jugadas[len(self.jugadas) - 1]
        for i in ultima_jugada.cartas_seleccionadas:
            self.cartas.append(i)   

class Partida:
    
    def __init__(self):
        self.jugadores = []
        self.baraja = None
        self.mesa = None
        self.crear_partida()

    def crear_partida(self):
        self.crear_mesa()
        # self.init_jugadores()
        self.autoseleccionar_jugadores(3)
        self.baraja = Baraja(len(self.jugadores))
        self.repartir()
        self.mostrar_manos()
        self.empezar()

    # ** Esta función solo es para pruebas. Selecciona automaticamente n jugadores.
    def autoseleccionar_jugadores(self, n):
        nombre = 'A'
        for i in range(n):
            jugador = Jugador(chr(ord(nombre) + i), self.mesa)
            self.jugadores.append(jugador)

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
        numero_jugadores = len(self.jugadores)
        while len(self.baraja.cartas) > 0:
            for i in range(numero_jugadores):
                self.jugadores[i].mano.append(self.baraja.cartas[0])
                self.baraja.cartas.pop(0)
        for i in range(numero_jugadores):
            self.jugadores[i].descarte()

    def crear_mesa(self):
        self.mesa = Mesa()

    def mostrar_baraja(self):
        length = len(self.baraja.cartas)   
        for i in range(length):
            print(self.baraja.cartas[i].numero, self.baraja.cartas[i].palo)

    def mostrar_manos(self):
        n_jugadores = len(self.jugadores)
        for i in range(n_jugadores):
            print(self.jugadores[i].name + ':')
            for j in range(len(self.jugadores[i].mano)):
                print(j, '-', self.jugadores[i].mano[j].numero, self.jugadores[i].mano[j].palo)
            print(' ')

    def empezar(self):
        j = len(self.jugadores)
        indice = randint(0, j - 1)
        if indice >= (j - 1):
            indice = - 1
        print("Empieza " + self.jugadores[indice].name + '!')
        self.jugar(indice)
    
    def jugar(self, indice):
        while not self.hay_ganador(): 
            print('Es el turno de', self.jugadores[indice].name)
            self.mesa.hacer_jugada(self.jugadores[indice])
            self.mostrar_manos()
            if indice + 1 > (len(self.jugadores) - 1):
                indice = -1
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
