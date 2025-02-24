import copy

class JuegoZeroSuma(object):
    
    def __init__(self) -> None:
        """
        Inicializa el juego es importante establecer:
        
            1. Estado inicial (tablero, None por default)
            2. Jugador (1 o -1, 1 por default)
        
        """
        self.jugador = 1
        self.estado = None
        
    def jugadas_legales(self) -> tuple:
        """
        Devuelve las posiciones de las jugadas legales
        
        De preferencia un generador, pero una tupla 
        o una lista tambien está bien
        
        """
        pass
    
    def terminal(self) -> bool:
        """
        Regresa True si es un estado de fin de juego
        
        """
        pass
    
    def ganador(self) -> int:
        """
        Regresa el jugador ganador o empate (-1000, 0 o 1000)
        
        """
        pass
    
    def aplica_jugada(self, jugada):
        """
        Aplica la juagada cambiando tablero y jugador si la jugada es legal
        
        Devuelve el tablero anterior
        """
        if jugada not in self.jugadas_legales():
            raise ValueError(f"La jugada \n{jugada}\n no es válida")
        anterior = copy.deepcopy(self.estado)
        
        self.jugador *= -1 
        
        return anterior
    
    def regresa_jugada(self, anterior):
        self.jugador *= -1
        self.estado = copy.deepcopy(anterior)
        

def minimax(juego, alfa=-1e10, beta=1e10, max_d=4, arregla=None, heuristica=None):
    return max_val(juego, alfa, beta, max_d, arregla, heuristica)

def max_val(juego, alfa, beta, max_d, arregla, heuristica):
    if juego.terminal():
        return juego.ganador()
    if max_d == 0:
        return heuristica(juego)
    if arregla != None:
        jugadas_legales = arregla(juego.jugadas_legales())
    
    
    