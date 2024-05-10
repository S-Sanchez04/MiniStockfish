import random
import chess
import networkx as nx
import matplotlib.pyplot as plt
import pygame

WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
BLUE = (0, 0, 255)
GREEN = (170, 255, 0)

# Letters of the columns
COLUMN_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Function to draw the chess board
def drawBoard(screen):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def getColumnLetter(col):
    return COLUMN_LETTERS[col]

def getColumnIndex(letra):
    return COLUMN_LETTERS.index(letra)

def drawPieces(screen, board):
    for row in range(8):
        for col in range(8):
            square = col, 7 - row
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

def grafoManager(grafo, move):
    fromNodo = getNameNodo(move.from_square)
    toNodo = getNameNodo(move.to_square)
    if not grafo.has_node(fromNodo):
        addNodo(grafo, fromNodo)
    if not grafo.has_node(toNodo):
        addNodo(grafo, toNodo)
        addArista(grafo, fromNodo, toNodo)

def getNameNodo(square):
    to_row = chess.square_rank(square)
    to_col = chess.square_file(square)
    col = getColumnLetter(to_col)
    return str(col) + str(to_row)

def crearGrafo():
    return nx.Graph()

def addNodo(grafo, nodo):
    grafo.add_node(nodo)

def addArista(grafo, nodo1, nodo2):
    grafo.add_edge(nodo1, nodo2)

def mostrarGrafo(grafo):
    nx.draw(grafo, with_labels=True, node_color='lightblue', node_size=800, font_size=10)
    plt.show()

def posInicial(board, ficha):
    casillasConPiezas = board.piece_map()
    for casilla, pieza in casillasConPiezas.items():
        if pieza.symbol() == ficha.symbol():
            return chess.square_name(casilla)

def movimientosFicha(board):
    movPosibles = []
    for move in board.legal_moves:
        to_square = move.to_square
        # Obtain the row and column index of the destination square
        to_row = chess.square_rank(to_square)
        to_col = chess.square_file(to_square)
        movPosibles.append((to_row, to_col))
    return movPosibles

def moverPieza(grafo, board, row, col):
    destSquare = chess.square(col, 7 - row)  # Convert the row and column to a square index
    move = chess.Move.null()  # Initialize a null move by default
    for legalMove in board.legal_moves:
        if legalMove.to_square == destSquare:
            move = legalMove
            break
    if move != chess.Move.null():
        board.push(move)  # Apply the move if it's legal
        grafoManager(grafo, move)
        return True

def ganador(board):
    if len(board.piece_map()) == 1:
        return True

def mostrarVictoria(screen, ganador):
    font = pygame.font.Font(None, 36)  # Define the font and size of the text
    text = font.render(f"Ganan las {ganador}", True, BLACK)  # Render the text into a surface
    textRect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, textRect) 

def mostrarStalemate(screen):
    font = pygame.font.Font(None, 36)  # Define the font and size of the text
    text = font.render("No hay más movimientos", True, BLACK)  # Render the text into a surface
    
    textRect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, textRect) 

def stalemate(board):
    return board.is_stalemate()

def getNewPosicion():
    posicionesCaballo = ["n7", "1n6", "2n5", "3n4", "4n3", "5n2", "6n1", "7n"]
    posicionesPeon = ["P7", "1P6", "2P5", "3P4", "4P3", "5P2", "6P1", "7P"]
    return random.choice(posicionesCaballo) + "/8/8/8/8/8/" + random.choice(posicionesPeon) + "/8 w KQkq - 0 1"

def main():
    pygame.init()
    grafo = crearGrafo()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Ajedrez')
    fichaSeleccionada = None
    seleccionado = 0
    board = chess.Board(getNewPosicion())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Calculate the position of the square on the board
                    col = mouse_x // SQUARE_SIZE
                    row = mouse_y // SQUARE_SIZE
                    columnLetter = getColumnLetter(col)
                    rowNumber = 8 - row
                    square = str(columnLetter) + str(rowNumber)
                    ficha = board.piece_at(chess.parse_square(square))
                    if fichaSeleccionada is None:
                        if ficha is not None:
                            if ficha.color == board.turn:
                                if seleccionado == 0:
                                    pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                                    posibles =movimientosFicha(board)
                                    seleccionado = 1
                                    fichaSeleccionada = ficha
                                elif seleccionado == 1:
                                    if (row, col) in posibles:
                                        moverPieza(grafo, board, row, col)
                                        seleccionado = 0
                                        fichaSeleccionada = None
                                        posibles = []
                                    else:
                                        seleccionado = 0
                                        fichaSeleccionada = None
                                        posibles = []
                    else:
                        if (row, col) in posibles:
                            moverPieza(grafo, board, row, col)
                            seleccionado = 0
                            fichaSeleccionada = None
                            posibles = []
                        else:
                            seleccionado = 0
                            fichaSeleccionada = None
                            posibles = []

        screen.fill(WHITE)
        drawBoard(screen)
        drawPieces(screen, board)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()