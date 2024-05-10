import random
import chess
import networkx as nx
import matplotlib.pyplot as plt
import pygame

WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY = (211, 211, 211)
BLUE = (0,0,255)
GREEN = (170,255,0)

# Letras de las columnas
COLUMN_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Función para dibujar el tablero de ajedrez
def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            

def get_column_letter(col):
    return COLUMN_LETTERS[col]

def get_column_index(letra):
    return COLUMN_LETTERS.index(letra)

def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            square = col, 7-row
            piece = board.piece_at(chess.square(*square))
            if piece is not None:
                if piece.color:
                    img = pygame.image.load(f"assets/_{piece.symbol()}.png")
                    img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                else:
                    img = pygame.image.load(f"assets/{piece.symbol()}.png")
                    img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def GetNameNodo(square):
    to_row = chess.square_rank(square)
    to_col = chess.square_file(square)
    col = get_column_letter(to_col)
    return str(col)+str(to_row)


def crear_grafo():
    return nx.Graph()

def agregar_nodo(grafo, nodo):
    grafo.add_node(nodo)

def agregar_arista(grafo, nodo1, nodo2):
    grafo.add_edge(nodo1, nodo2)

def mostrar_grafo(grafo):
    nx.draw(grafo, with_labels=True, node_color='lightblue', node_size=800, font_size=10)
    plt.show()


def grafoManager(grafo,move):
    FromNodo = str(GetNameNodo(move.from_square))
    ToNodo = str(GetNameNodo(move.to_square))
    if not grafo.has_node(FromNodo):
        agregar_nodo(grafo,FromNodo)
    if not grafo.has_node(ToNodo):
        agregar_nodo(grafo,ToNodo)
        agregar_arista(grafo,FromNodo,ToNodo)
    

def pos_inicial(board, ficha):
    casillas_con_piezas = board.piece_map()
    for casilla, pieza in casillas_con_piezas.items():
        if pieza.symbol() == ficha.symbol():
            return chess.square_name(casilla)


def movimientos_ficha(board):
    mov_posibles = []
    for move in board.legal_moves:
        to_square = move.to_square
        # Obtener el índice de fila y columna de la casilla de destino
        to_row = chess.square_rank(to_square)
        to_col = chess.square_file(to_square)
        mov_posibles.append((to_row, to_col))
    return mov_posibles

def mover_pieza(grafo,board, row, col):
    dest_square = chess.square(col, 7 - row)  # Convertir las coordenadas de fila y columna a un índice de casilla
    move = chess.Move.null()  # Inicializar un movimiento nulo por defecto
    for legal_move in board.legal_moves:
        if legal_move.to_square == dest_square:
            move = legal_move
            break
    if move != chess.Move.null():
        board.push(move)  # Aplicar el movimiento si es legal
        grafoManager(grafo,move)
        return True

def ganador(board):
    if len(board.piece_map()) == 1:
        return True

def mostrar_victoria(screen, ganador):
    font = pygame.font.Font(None, 36)  # Definir la fuente y el tamaño del texto
    text = font.render(f"Ganan las {ganador}", True, BLACK)  # Renderizar el texto en una superficie
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) 
    screen.blit(text, text_rect)  

def mostrar_stalemate(screen):
    font = pygame.font.Font(None, 36)  # Definir la fuente y el tamaño del texto
    text = font.render("No hay más movimientos", True, BLACK)  # Renderizar el texto en una superficie
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) 
    screen.blit(text, text_rect)  

def stalemate(board):
    return board.is_stalemate()

def GetNewPosicion():
    posicionesCaballo = ["n7","1n6", "2n5", "3n4", "4n3", "5n2", "6n1", "7n"]
    posicionesPeon = ["P7", "1P6", "2P5", "3P4", "4P3", "5P2", "6P1", "7P"]
    return random.choice(posicionesCaballo), random.choice(posicionesPeon) 


def main():
    pygame.init()
    grafo = crear_grafo()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Ajedrez')
    ficha_seleccionada = None
    seleccionado = 0
    n, p = GetNewPosicion()
    pos = n+"/8/8/8/8/8/"+ p +"/8 w KQkq - 0 1"
    board = chess.Board(pos)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Calcular la posición de la casilla en el tablero
                    col = mouse_x // SQUARE_SIZE
                    row = mouse_y // SQUARE_SIZE
                    column_letter = get_column_letter(col)
                    row_number = 8 - row
                    cuadrado = str(column_letter) + str(row_number)
                    ficha = board.piece_at(chess.parse_square(cuadrado))
                    if ficha_seleccionada is None:
                        if ficha is not None:
                            if ficha.color == board.turn:
                                if seleccionado == 0:
                                    pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                                    posibles = movimientos_ficha(board)
                                    for rows, cols in posibles:
                                        pygame.draw.rect(screen, GREEN , ((cols )* SQUARE_SIZE, (7-rows) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                                        pygame.draw.rect(screen, BLACK , ((cols )* SQUARE_SIZE, (7-rows) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                                    ficha_seleccionada = ficha
                                    seleccionado = 1
                                elif seleccionado == 1:
                                    pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                                    seleccionado = 0
                                    ficha_seleccionada = None
                    else:
                        if ficha == ficha_seleccionada:
                            pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                            seleccionado = 0
                            ficha_seleccionada = None
                        else:
                            if mover_pieza(grafo,board,row,col):
                                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                                seleccionado = 0
                                ficha_seleccionada = None

        if seleccionado == 0:
            screen.fill(WHITE)
            draw_board(screen)
        draw_pieces(screen, board)
        pygame.display.flip()
        if ganador(board):
            ganadores = "Negras"
            if not board.turn:
                ganadores = "Blancas"
            mostrar_victoria(screen, ganadores)
            pygame.display.flip()  
            pygame.time.delay(2000)  
            running = False
        elif stalemate(board):
            mostrar_stalemate(screen)
            pygame.display.flip()  
            pygame.time.delay(2000) 
            running = False
    pygame.quit()
    mostrar_grafo(grafo)
    

if __name__ == "__main__":
    main()