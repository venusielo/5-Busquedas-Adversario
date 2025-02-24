import pygame
import numpy as np

# Tamaño de la ventana del juego
WINDOW_SIZE = [500, 500]

# Colores utilizados en la interfaz gráfica
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Iniciar Pygame
pygame.init()

# Crear la ventana del juego
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Otello")

# Función para dibujar el tablero
def draw_board(board):
    # Dibujar el fondo
    screen.fill(GREEN)
    # Dibujar las líneas del tablero
    for i in range(9):
        pygame.draw.line(
            screen, BLACK, (i * 50 + 50, 50), (i * 50 + 50, 450), 2
        )
        pygame.draw.line(
            screen, BLACK, (50, i * 50 + 50), (450, i * 50 + 50), 2
        )
    # Dibujar las fichas
    for i in range(8):
        for j in range(8):
            if board[i, j] == 1:
                pygame.draw.circle(
                    screen, BLACK, (j * 50 + 75, i * 50 + 75), 20
                )
            elif board[i, j] == 2:
                pygame.draw.circle(
                    screen, WHITE, (j * 50 + 75, i * 50 + 75), 20
                )
    # Actualizar la pantalla
    pygame.display.update()

# Función para obtener las coordenadas de la casilla del tablero correspondiente a la posición del mouse
def get_square(mouse_pos):
    row = (mouse_pos[1] - 50) // 50
    col = (mouse_pos[0] - 50) // 50
    if row < 0 or row > 7 or col < 0 or col > 7:
        return None
    else:
        return row, col

# Función principal del juego
def main():
    # Inicializar el tablero
    board = np.zeros((8, 8), dtype=int)
    board[3, 3] = 1
    board[3, 4] = 2
    board[4, 3] = 2
    board[4, 4] = 1
    player = 1
    # Dibujar el tablero
    draw_board(board)
    # Bucle principal del juego
    running = True
    while running:
        # Esperar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtener la casilla del tablero correspondiente a la posición del mouse
                pos = pygame.mouse.get_pos()
                square = get_square(pos)
                if square is None:
                    continue
                # Comprobar si el movimiento es legal
                if is_legal_move(player, board, square[0], square[1]):
                    # Hacer el movimiento
                    make_move(player, board, square)
                    # Dibujar el tablero
                    draw_board(board)
                    # Cambiar el turno
                    player = 3 - player
                    # Comprobar si hay jugadas legales disponibles para el siguiente jugador
                    if not has_legal_moves(3 - player, board):
                        # Si no hay jugadas legales, terminar el juego
                        winner = get_winner(board)
                        if winner == 1:
                            print("Ganó el jugador negro")
                        elif winner == 2:
                            print("Ganó el jugador blanco")
                        else:
                            print("Empate")
                        running = False
        # Actualizar la pantalla
        pygame.display.update()

    # Salir de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
