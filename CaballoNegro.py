import random
import chess
import networkx as nx
import matplotlib.pyplot as plt
import pygame

Width, Height = 800, 800
SquareSize = Width // 8
White = (255, 255, 255)
Black = (0, 0, 0)
Gray = (211, 211, 211)
Blue = (0, 0, 255)
Green = (170, 255, 0)
Yellow = (0,255,255)
# Letras de las columnas
ColumnLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Función para dibujar el tablero de ajedrez
def drawBoard(screen):
    for row in range(8):
        for col in range(8):
            color = White if (row + col) % 2 == 0 else Gray
            pygame.draw.rect(screen, color, (col * SquareSize, row * SquareSize, SquareSize, SquareSize))
            if col == 0:
                font = pygame.font.SysFont("Arial", 20)
                text = font.render(str(8 - row), True, Black)
                screen.blit(text, (col * SquareSize + 5, row * SquareSize + 5))
            if row == 7:
                font = pygame.font.SysFont("Arial", 20)
                text = font.render(ColumnLetters[col], True, Black)
                screen.blit(text, (col * SquareSize + 80, row * SquareSize + 80))

def getColumnLetter(col):
    return ColumnLetters[col]

def getColumnIndex(letra):
    return ColumnLetters.index(letra)

def drawPieces(screen, board):
    for row in range(8):
        for col in range(8):
            square = col, 7-row
            piece = board.piece_at(chess.square(*square))
            if piece is not None:
                if piece.color:
                    img = pygame.image.load(f"assets/_{piece.symbol()}.png")
                    img = pygame.transform.scale(img, (SquareSize, SquareSize))
                    screen.blit(img, (col * SquareSize, row * SquareSize))
                else:
                    img = pygame.image.load(f"assets/{piece.symbol()}.png")
                    img = pygame.transform.scale(img, (SquareSize, SquareSize))
                    screen.blit(img, (col * SquareSize, row * SquareSize))

def GetNameNodo(square):
    to_row = chess.square_rank(square)
    to_col = chess.square_file(square)
    col = getColumnLetter(to_col)
    return str(col)+str(to_row+1)

def crearGrafo():
    return nx.Graph()

def agregarNodo(grafo, nodo):
    grafo.add_node(nodo)

def agregarArista(grafo, nodo1, nodo2):
    grafo.add_edge(nodo1, nodo2)
    
def mostrarGrafo(grafo, posIn, colPeon):
    node_color = [(.85, .3, .3) if node == posIn else 'green' if node[0] == colPeon else 'lightblue' for node in grafo.nodes()]
    nx.draw(grafo, with_labels=True, node_color=node_color, node_size=800, font_size=10)
    plt.show()

def grafoManager(grafo, move):
    FromNodo = str(GetNameNodo(move.from_square))
    ToNodo = str(GetNameNodo(move.to_square))
    #if not grafo.has_node(FromNodo):
    agregarNodo(grafo, FromNodo)
    #if not grafo.has_node(ToNodo):
    agregarNodo(grafo, ToNodo)
    agregarArista(grafo, FromNodo, ToNodo)

def posInicial(board, ficha):
    casillasConPiezas = board.piece_map()
    for casilla, pieza in casillasConPiezas.items():
        if pieza.symbol() == ficha.symbol():
            return chess.square_name(casilla)

def movimientosFicha(board):
    movPosibles = []
    for move in board.legal_moves:
        to_square = move.to_square
        # Obtener el índice de fila y columna de la casilla de destino
        to_row = chess.square_rank(to_square)
        to_col = chess.square_file(to_square)
        movPosibles.append((to_row, to_col))
    return movPosibles

def moverPieza(board, row, col):
    dest_square = chess.square(col, 7 - row)  # Convertir las coordenadas de fila y columna a un índice de casilla
    move = chess.Move.null()  # Inicializar un movimiento nulo por defecto
    for legal_move in board.legal_moves:
        if legal_move.to_square == dest_square:
            move = legal_move
            break
    if move != chess.Move.null():
        board.push(move)  # Aplicar el movimiento si es legal
        return True

def ganador(board):
    if len(board.piece_map()) == 1:
        return True

def mostrarVictoria(screen, ganador):
    font = pygame.font.Font(None, 36)  # Definir la fuente y el tamaño del texto
    text = font.render(f"Ganan las {ganador}", True, Black)  # Renderizar el texto en una superficie
    text_rect = text.get_rect(center=(Width // 2, Height // 2)) 
    screen.blit(text, text_rect)  

def mostrarStalemate(screen):
    font = pygame.font.Font(None, 36)  # Definir la fuente y el tamaño del texto
    text = font.render("No hay más movimientos", True, Black)  # Renderizar el texto en una superficie
    text_rect = text.get_rect(center=(Width // 2, Height // 2)) 
    screen.blit(text, text_rect)  

def stalemate(board):
    return board.is_stalemate()

def GetNewPosicion():
    posicionesCaballo = ["n7", "1n6", "2n5", "3n4", "4n3", "5n2", "6n1", "7n"]
    posicionesPeon = ["P7", "1P6", "2P5", "3P4", "4P3", "5P2", "6P1", "7P"]
    return random.choice(posicionesCaballo), random.choice(posicionesPeon) 

def Grafo_Caballo(board):
    for move in board.legal_moves:
        tempBoard = board.copy()
        tempBoard.push(move)
        grafoManager(GRAFO_CABALLO, move)

def GetPos(board, symbol):
    for square, piece in board.piece_map().items():
        if piece.symbol() == symbol:  
            return chess.square_name(square)
    return None

def MoveInGraph(move):
    FromNodo = str(GetNameNodo(move.from_square))
    ToNodo = str(GetNameNodo(move.to_square))
    return GRAFO_CABALLO.has_edge(FromNodo, ToNodo)

'''
def GrafoGenerator(board):
    posPeon = GetPos(board, 'P')
    depth = (8 - int(posPeon[1]))
    TempBoard = board.copy()
    Grafo_Caballo(TempBoard)
    for move1 in TempBoard.legal_moves:
        TempBoard1 = TempBoard.copy()
        TempBoard1.push(move1)
        Grafo_Caballo(TempBoard1)
        for move2 in TempBoard1.legal_moves:
            TempBoard2 = TempBoard1.copy()
            TempBoard2.push(move2)
            Grafo_Caballo(TempBoard2)
            for move3 in TempBoard2.legal_moves:
                TempBoard3 = TempBoard2.copy()
                TempBoard3.push(move3)
                Grafo_Caballo(TempBoard3)
                for move4 in TempBoard3.legal_moves:
                    TempBoard4 = TempBoard3.copy()
                    TempBoard4.push(move4)
                    Grafo_Caballo(TempBoard4)
                    for move5 in TempBoard4.legal_moves:
                        TempBoard5 = TempBoard4.copy()
                        TempBoard5.push(move5)
                        Grafo_Caballo(TempBoard5) --- version antigua, sin recursion
'''

def GrafoGenerator(board, depth=7, level=1):
    TempBoard = board.copy()
    if not TempBoard.turn:
        Grafo_Caballo(TempBoard)
    if level < depth:
        for move in TempBoard.legal_moves:
            TempBoard1 = TempBoard.copy()
            TempBoard1.push(move)
            GrafoGenerator(TempBoard1, depth, level+1)
            TempBoard1.pop()
def ComoStalemate(posInCaballo, posPeon):
    depth = 8-int(posPeon[1])
    for i in range(depth):
        turnos = 0
        try:
            Target = posPeon[0]+str(int(posPeon[1])+1+i)
            shortestPath = nx.shortest_path(GRAFO_CABALLO, source=posInCaballo, target= Target)
            if shortestPath is not None:
                shortestPath = shortestPath[1:] #Eliminar el nodo inicial
                turnos += len(shortestPath) + int(posPeon[1])
                print(turnos, Target[1], turnos == int(Target[1]))
                if turnos == int(Target[1]):
                    print("Stalemate ",shortestPath)
                    break
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            shortestPath = None
    return shortestPath

def ComoGanar(posInCaballo, posPeon):  
    depth = 8-int(posPeon[1])
    for i in range(depth):
        turnos = -1
        try:
            Target = posPeon[0]+str(int(posPeon[1])+i)
            shortestPath = nx.shortest_path(GRAFO_CABALLO, source=posInCaballo, target= Target)
            if shortestPath is not None:
                shortestPath = shortestPath[1:] #Eliminar el nodo inicial
                turnos += len(shortestPath) + int(posPeon[1])
                print(turnos, Target[1], turnos == int(Target[1]))
                if turnos == int(Target[1]):
                    print("Shortest ",shortestPath)
                    return shortestPath
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            shortestPath = None
    return None

def MejoresMovimientos(screen, posInCaballo, posPeon):
    shortestPath = ComoGanar(posInCaballo, posPeon)
    if shortestPath is None : 
        shortestPath = ComoStalemate(posInCaballo, posPeon)
    return shortestPath

    

def main():
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('Ajedrez')
    ficha_seleccionada = None
    seleccionado = 0
    n, p = GetNewPosicion()
    pos = n+"/8/8/8/8/8/"+ p +"/8 w KQkq - 0 1"
    #pos = "7n" + "/8/8/8/8/8/" + "1P6" + "/8 w KQkq - 0 1"
    board = chess.Board(pos)
    firstMove = True
    caminoFinal = False
    drawBoard(screen)
    posInCaballo = GetPos(board, 'n')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Calcular la posición de la casilla en el tablero
                    col = mouse_x // SquareSize
                    row = mouse_y // SquareSize
                    column_letter = getColumnLetter(col)
                    row_number = 8 - row
                    cuadrado = str(column_letter) + str(row_number)
                    ficha = board.piece_at(chess.parse_square(cuadrado))
                    if ficha_seleccionada is None:
                        if ficha is not None:
                            if ficha.color == board.turn:
                                if seleccionado == 0:
                                    pygame.draw.rect(screen, Blue, (col * SquareSize, row * SquareSize, SquareSize, SquareSize))
                                    posibles = movimientosFicha(board)
                                    for rows, cols in posibles:
                                        pygame.draw.rect(screen, Green , ((cols )* SquareSize, (7-rows) * SquareSize, SquareSize, SquareSize))
                                        pygame.draw.rect(screen, Black , ((cols )* SquareSize, (7-rows) * SquareSize, SquareSize, SquareSize), 1)
                                    ficha_seleccionada = ficha
                                    seleccionado = 1
                                elif seleccionado == 1:
                                    pygame.draw.rect(screen, White, (col * SquareSize, row * SquareSize, SquareSize, SquareSize))
                                    seleccionado = 0
                                    ficha_seleccionada = None
                    else:
                        if ficha == ficha_seleccionada:
                            pygame.draw.rect(screen, White, (col * SquareSize, row * SquareSize, SquareSize, SquareSize))
                            seleccionado = 0
                            ficha_seleccionada = None
                        else:
                            if moverPieza(board,row,col):
                                pygame.draw.rect(screen, White, (col * SquareSize, row * SquareSize, SquareSize, SquareSize))
                                seleccionado = 0
                                ficha_seleccionada = None
                                if firstMove :
                                    posPeon =  GetPos(board,'P')
                                    colPeon =posPeon[0]
                                    GrafoGenerator(board)
                                    shortestPath = MejoresMovimientos(screen, posInCaballo, posPeon)
                                    caminoFinal = True
                                    pygame.display.flip()
                                    firstMove = False
                                screen.fill(White)
                                drawBoard(screen)
                                drawPieces(screen, board)
                                for square in shortestPath:
                                    column = getColumnIndex(square[0])
                                    row = int(square[1])-1
                                    pygame.draw.rect(screen, Yellow , ((column)* SquareSize, (7-row) * SquareSize, SquareSize, SquareSize))
        if seleccionado == 0:
            if not caminoFinal:
                screen.fill(White)
                drawBoard(screen)
        drawPieces(screen, board)
        pygame.display.flip()
        if ganador(board):
            ganadores = "Negras"
            if not board.turn:
                ganadores = "Blancas"
            mostrarVictoria(screen, ganadores)
            pygame.display.flip()  
            pygame.time.delay(2000)  
            running = False
        elif stalemate(board):
            mostrarStalemate(screen)
            pygame.display.flip()  
            pygame.time.delay(2000) 
            running = False
    mostrarGrafo(GRAFO_CABALLO, posInCaballo, colPeon)
    pygame.quit()
GRAFO_CABALLO = crearGrafo()
main()