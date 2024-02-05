import pygame as p
import ChessEngine, AIPlayer

WIDTH = HEIGHT = 512
DIMENTIONS = 8
SQUARE = HEIGHT//DIMENTIONS
MAX_FPS = 60
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"Images/{piece}.png"), (SQUARE, SQUARE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    selectedSquare = ()
    playerClicks = []
    gameOver = False
    playerWhite = True
    playerBlack = False

    while running:
        humanTurn = (gs.whiteToMove and playerWhite) or (not gs.whiteToMove and playerBlack)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQUARE
                    row = location[1]//SQUARE
                    if selectedSquare == (row, col):
                        selectedSquare = ()
                        playerClicks = []
                    else:
                        selectedSquare = (row, col)
                        playerClicks.append(selectedSquare)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                selectedSquare = ()
                                playerClicks = []

                        if not moveMade:
                            playerClicks = [selectedSquare]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.moveUndo()
                    if not playerWhite or not playerBlack and humanTurn:
                        gs.moveUndo()
                    moveMade = True
                    animate = False
                    gameOver = False

                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    selectedSquare = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        
        if not gameOver and not humanTurn:
                AIMove = AIPlayer.recursiveHelper(gs, validMoves)
                if AIMove is None:
                    AIMove = AIPlayer.randomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, selectedSquare)

        if gs.checkmate or gs.stalemate:
            gameOver = True
            drawEndGameText(screen, "Stalemate" if gs.stalemate else "Black Wins by Checkmate" if gs.whiteToMove else "White Wins by Checkmate")

        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, selectedSquare):
    if selectedSquare!=():
        r, c = selectedSquare
        s = p.Surface((SQUARE, SQUARE))
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s.set_alpha(200)
            s.fill(p.Color("#1957CC"))
            screen.blit(s, (c*SQUARE, r*SQUARE))
            s.set_alpha(100)
            s.fill(p.Color("#FDFF59"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQUARE, move.endRow*SQUARE))

def drawGameState(screen, gs, validMoves, selectedSquare):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, selectedSquare)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("#C88775")]
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))

def drawPieces(screen, board):
    for r in range(DIMENTIONS):
        for c in range(DIMENTIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQUARE, move.endRow*SQUARE, SQUARE, SQUARE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == "b" else move.endRow - 1
                endSquare = p.Rect(move.endCol*SQUARE, enPassantRow*SQUARE, SQUARE, SQUARE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE))
        p.display.flip()
        clock.tick(MAX_FPS)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 50, False, False)
    textObject = font.render(text, 0, p.Color("Red"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()