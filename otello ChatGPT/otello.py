import numpy as np

# Definir el tablero y las posibles jugadas
board_size = 8
board = np.zeros((board_size, board_size))
board[3][3] = board[4][4] = 1
board[3][4] = board[4][3] = 2
possible_moves = []

# Función para obtener las posibles jugadas
def get_moves(player, board):
    moves = []
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                # Comprobar si el movimiento es legal
                if is_legal_move(player, board, i, j):
                    moves.append((i, j))
    return moves

# Función para comprobar si un movimiento es legal
def is_legal_move(player, board, row, col):
    # Comprobar si el movimiento está dentro del tablero
    if row < 0 or row >= board_size or col < 0 or col >= board_size:
        return False
    # Comprobar si la casilla ya está ocupada
    if board[row][col] != 0:
        return False
    # Comprobar si el movimiento captura fichas del oponente
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if r < 0 or r >= board_size or c < 0 or c >= board_size:
                continue
            if board[r][c] == 3 - player:
                while board[r][c] == 3 - player:
                    r += i
                    c += j
                    if r < 0 or r >= board_size or c < 0 or c >= board_size:
                        break
                if r < 0 or r >= board_size or c < 0 or c >= board_size:
                    continue
                if board[r][c] == player:
                    return True
    return False

# Función para realizar un movimiento
def make_move(player, board, row, col):
    board[row][col] = player
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if r < 0 or r >= board_size or c < 0 or c >= board_size:
                continue
            if board[r][c] == 3 - player:
                to_flip = []
                while board[r][c] == 3 - player:
                    to_flip.append((r, c))
                    r += i
                    c += j
                    if r < 0 or r >= board_size or c < 0 or c >= board_size:
                        break
                if r < 0 or r >= board_size or c < 0 or c >= board_size:
                    continue
                if board[r][c] == player:
                    for r, c in to_flip:
                        board[r][c] = player

# Función de evaluación del tablero
def evaluate_board(board):
    return np.sum(board == 1) - np.sum(board == 2)

# Función Minimax con poda
def minimax(player, board, depth, alpha, beta):
    # Comprobar si el juego ha terminado o si se ha alcanzado la profundidad máxima de búsqueda
    if depth == 0 or len(get_moves(player, board)) == 0:
        return None, evaluate_board(board)
    # Obtener las posibles jugadas
    moves = get_moves(player, board)
    # Establecer el mejor movimiento y su valor
    best_move = None
    if player == 1:
        best_value = -np.inf
    else:
        best_value = np.inf
    # Probar cada movimiento y actualizar el mejor valor
    for move in moves:
        # Realizar el movimiento
        new_board = np.copy(board)
        make_move(player, new_board, move[0], move[1])
        # Obtener el valor del nuevo tablero recursivamente
        move, value = minimax(3 - player, new_board, depth - 1, alpha, beta)
        # Actualizar el mejor valor y movimiento
        if player == 1:
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
        # Poda Alpha-Beta
        if alpha >= beta:
            break
    return best_move, best_value

# Juego Otello
player = 1
while len(get_moves(player, board)) > 0:
    if player == 1:
        # Movimiento del jugador humano
        print("Tablero actual:\n", board)
        row, col = input("Jugador 1 - Ingrese las coordenadas de su movimiento (fila, columna): ").split(',')
        row, col = int(row), int(col)
        if is_legal_move(player, board, row, col):
            make_move(player, board, row, col)
        else:
            print("Movimiento inválido, intenta de nuevo.")
            continue
    else:
        # Movimiento del jugador AI
        print("Tablero actual:\n", board)
        move, value = minimax(player, board, depth=4, alpha=-np.inf, beta=np.inf)
        print("Valor del movimiento AI:", value)
        make_move(player, board, move[0], move[1]())
    # Cambiar al siguiente jugador
    player = 3 - player
# Juego terminado
print("Tablero final:\n", board)
score = evaluate_board(board)
if score > 0:
    print("Jugador 1 ha ganado!")
elif score < 0:
    print("Jugador 2 ha ganado!")
else:
    print("El juego ha terminado en empate.")

