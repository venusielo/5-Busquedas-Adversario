import numpy as np

# Tamaño del tablero
ROWS = 6
COLS = 7

# Valores de los jugadores
PLAYER_1 = 1
PLAYER_2 = -1

# Valor para la casilla vacía
EMPTY = 0

# Valor para la victoria del jugador 1
WIN_1 = 1000000

# Valor para la victoria del jugador 2
WIN_2 = -1000000

# Profundidad máxima de la búsqueda
MAX_DEPTH = 5

def create_board():
    """Crea un nuevo tablero vacío."""
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    """Coloca una ficha en una columna del tablero."""
    board[row][col] = piece

def is_valid_location(board, col):
    """Comprueba si una columna del tablero está disponible."""
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    """Devuelve la siguiente fila disponible en una columna del tablero."""
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    """Comprueba si un jugador ha ganado el juego."""
    # Comprobar horizontalmente
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Comprobar verticalmente
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Comprobar diagonalmente (hacia la derecha)
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Comprobar diagonalmente (hacia la izquierda)
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def evaluate_window(window, piece):
    """Evalúa una ventana de 4 casillas en el tablero."""
    score = 0
    opp_piece = PLAYER_2 if piece == PLAYER_1 else PLAYER_1

    if window.count(piece) == 4:
        score += WIN_1 if piece == PLAYER_1 else WIN_2
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 100

    return score

def score_position(board, piece):
    """Evalúa la posición actual del tablero."""
    score = 0

    # Evaluar las ventanas horizontales
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Evaluar las ventanas verticales
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Evaluar las ventanas diagonales (hacia la derecha)
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Evaluar las ventanas diagonales (hacia la izquierda)
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    """Comprueba si el juego ha terminado."""
    return winning_move(board, PLAYER_1) or winning_move(board, PLAYER_2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    """Implementa el algoritmo minimax con poda alpha-beta."""
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER_1):
                return (None, WIN_1)
            elif winning_move(board, PLAYER_2):
                return (None, WIN_2)
            else: # No quedan casillas disponibles
                return (None, 0)
        else: # Profundidad máxima alcanzada
            return (None, score_position(board, PLAYER_1))

    if maximizingPlayer:
        value = float('-inf')
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_1)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = float('inf')
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_2)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    """Devuelve las columnas donde es posible colocar una fich
