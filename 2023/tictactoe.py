from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax 
from busquedas_adversarios import alpha_beta

class Gato(JuegoSumaCeros2T):
    """
    El juego del gato para ilustrar los modelos de juegos

    """
    def __init__(self):
        """
        Inicializa el juego del gato

        """
        super().__init__(9 * [0])

    def jugadas_legales(self):
        """ 
        Devuelve un iterable con las jugadas legales del jugador actual
        
        """
        return (
            posicion for posicion in range(9) 
            if self.estado[posicion] == 0
        )
    
    def es_terminal(self):
        """ 
        Devuelve True si el juago está en una posición terminal
        
        """
        x = self.estado
        if 0 not in x:
            return True
        if x[4] != 0 and (x[0] == x[4] == x[8] or x[2] == x[4] == x[6]):
            return True
        for i in range(3):
            if x[3 * i] != 0 and x[3 * i] == x[3 * i + 1] == x[3 * i + 2]:
                return True
            if x[i] != 0 and x[i] == x[i + 3] == x[i + 6]:
                return True
        return False
        
    def utilidad(self):
        """ 
        Devuelve la utilidad (final) del juador 1

        """
        x = self.estado
        if x[4] != 0 and (x[0] == x[4] == x[8] or x[2] == x[4] == x[6]):
            return x[4]
        for i in range(3):
            if x[3 * i] != 0 and x[3 * i] == x[3 * i + 1] == x[3 * i + 2]:
                return x[3 * i]
            if x[i] != 0 and x[i] == x[i + 3] == x[i + 6]:
                return x[i]
        return 0

    def hacer_jugada(self, jugada):
        """ 
        Realiza la juagada, cambia self.estado y self.jugador, devuelve None
        
        Recuerda que el estado es una lista, para poder hacer cambios
        por referencia y ahorrar un poco de tiempo en cada nodo
        
        """
        self.estado[jugada] = self.jugador
        self.jugador *= -1
        
    def __str__(self):
        """ 
        Para imprimir el gato de forma bonita
        
        """
        x = self.estado
        y = [
            ('X' if x[i] > 0 else 'O' if x[i] < 0 else str(i))
            for i in range(9)
        ]
        return (
            "\n" +
           f" {y[0]} | {y[1]} | {y[2]} ".center(60) + "\n" +
           "---+---+---".center(60) + "\n" +
           f" {y[3]} | {y[4]} | {y[5]} ".center(60) + "\n" +
           "---+---+---".center(60) + "\n" +
           f" {y[6]} | {y[7]} | {y[8]} ".center(60) + "\n"
        )
    

def juega_gato(jugador='X'):

    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = Gato()

    print("El juego del gato".center(60))
    print(f"las 'X' siempre empiezan, y tu juegas con {jugador}".center(60))

    if jugador == 'O':
        jugada = alpha_beta(juego)
        juego.hacer_jugada(jugada)

    while True:
        print(juego)
        print("Escoge tu jugada (uno de los números que quedan en el gato)")
        try:
            jugada = int(input(f"Jugador {jugador}: "))
            print(jugada)
        except:
            print("¡No seas macana y pon un número!")
            continue
        if jugada < 0 or jugada > 8 or juego.estado[jugada] != 0:
            print("¡No seas macana, pon un número válido!")
            continue

        juego.hacer_jugada(jugada)

        if juego.es_terminal():
            break
        else:
            jugada = alpha_beta(juego)
            juego.hacer_jugada(jugada)
            if juego.es_terminal():
                break
    print(juego)
    ganador = juego.utilidad()
    if ganador == 0:
        print("UN ASQUEROSO EMPATE".center(60))
    elif (ganador < 0 and jugador == 'X') or (ganador > 0 and jugador == 'O'):
        print("¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?".center(60))
    else:
        print("Ganaste, bye.")
    print("\n\nFin del juego")


if __name__ == '__main__':
    juega_gato('O')

