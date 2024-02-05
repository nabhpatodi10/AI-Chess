import numpy as np

class GameState():

    def __init__(self):

        self.board = np.array([["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])

        self.moveFunctions = {"p":self.getPawnMoves, "R":self.getRookMoves, "N":self.getKnightMoves, "B":self.getBishopMoves, "Q":self.getQueenMoves, "K":self.getKingMoves}

        self.whiteToMove = True

        self.moveLog = []

        self.wKlocation = (7,4)
        self.bKlocation = (0,4)

        self.Check = False
        self.pins = []
        self.checks = []

        self.checkmate = False
        self.stalemate = False

        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]

        self.currentCastlingRight = CastlingRights(True, True, True, True)
        self.castleRightsLog = [CastlingRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)

        if move.pieceMoved == "wK":
            wKlocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            bKlocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            #promote = input("Promote to [p, R, N, B, Q]: ")
            promote = "Q"
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promote

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()
        
        self.enpassantPossibleLog.append(self.enpassantPossible)

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastlingRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        self.whiteToMove = not self.whiteToMove

    def moveUndo(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            if move.pieceMoved == "wK":
                wKlocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                bKlocation = (move.startRow, move.startCol)

            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastlingRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"

            self.checkmate = False
            self.stalemate = False

            self.whiteToMove = not self.whiteToMove

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False
        
        if move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    def getValidMoves(self):
        moves = []
        self.Check, self.pins, self.checks = self.checkForPinsandCheck()
        if self.whiteToMove:
            kingRow = self.wKlocation[0]
            kingCol = self.wKlocation[1]
        else:
            kingRow = self.bKlocation[0]
            kingCol = self.bKlocation[1]
        if self.Check:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.wKlocation[0], self.wKlocation[1], moves, "w")
        else:
            self.getCastleMoves(self.bKlocation[0], self.bKlocation[1], moves, "b")
        if len(moves) == 0:
            if self.Check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        moves = np.array(moves)
        return moves

    def checkForPinsandCheck(self):
        pins = []
        checks = []
        Check = False
        if self.whiteToMove:
            enemy = "b"
            ally = "w"
            startRow = self.wKlocation[0]
            startCol = self.wKlocation[1]
        else:
            enemy = "w"
            ally = "b"
            startRow = self.bKlocation[0]
            startCol = self.bKlocation[1]
        
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    end = self.board[endRow][endCol]
                    if end[0] == ally and end[1] != "K":
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif end[0] == enemy:
                        type = end[1]
                        if (0 <= j <= 3 and type == "R") or (4 <= j <= 7 and type == "B") or (i == 1 and type == "p" and ((enemy == "w" and 6 <= j <= 7) or (enemy == "b" and 4 <= j <= 5))) or (type == "Q") or (i==1 and type == "K"):
                            if possiblePin == ():
                                Check = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break

        knightMoves = ((-1,-2), (-1,2), (1,2), (1,-2), (-2,-1), (-2,1), (2,-1), (2,1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                end = self.board[endRow][endCol]
                if end[0] == enemy and end[1] == "N":
                    Check = True
                    checks.append((endRow, endCol, m[0], m[1]))
        
        return Check, pins, checks

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for m in oppMoves:
            if m.endRow == r and m.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece =  self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            kRow, kCol = self.wKlocation
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c), (r-1,c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((6,c), (r-2,c), self.board))

            if c > 0 and self.board[r-1][c-1] != "--" and self.board[r-1][c-1][0] == "b":
                if not piecePinned or pinDirection == (-1,-1):
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c > 0 and (r-1, c-1) == self.enpassantPossible:
                attackingPiece = blockingPiece = False
                if kRow == r:
                    if kCol < c:
                        insideRange = range(kCol+1, c-1)
                        outsideRange = range(c+1, 8)
                    else:
                        insideRange = range(kCol-1, c, -1)
                        outsideRange = range(c-2, -1, -1)
                    for i in insideRange:
                        if self.board[r][i] != "--":
                            blockingPiece = True
                    for i in outsideRange:
                        square = self.board[r][i]
                        if square[0] == "b" and (square[1] == "Q" or square[1] == "R"):
                            attackingPiece = True
                        elif square != "--":
                            blockingPiece = True
                if not attackingPiece or blockingPiece:
                    moves.append(Move((r,c), (r-1,c-1), self.board, isEnpassantMove=True))

            if c < 7 and self.board[r-1][c+1] != "--" and self.board[r-1][c+1][0] == "b":
                if not piecePinned or pinDirection == (-1,1):
                    moves.append(Move((r,c), (r-1,c+1), self.board))
            if c < 7 and (r-1, c+1) == self.enpassantPossible:
                attackingPiece = blockingPiece = False
                if kRow == r:
                    if kCol < c:
                        insideRange = range(kCol+1, c)
                        outsideRange = range(c+2, 8)
                    else:
                        insideRange = range(kCol-1, c+1, -1)
                        outsideRange = range(c-1, -1, -1)
                    for i in insideRange:
                        if self.board[r][i] != "--":
                            blockingPiece = True
                    for i in outsideRange:
                        square = self.board[r][i]
                        if square[0] == "b" and (square[1] == "Q" or square[1] == "R"):
                            attackingPiece = True
                        elif square != "--":
                            blockingPiece = True
                if not attackingPiece or blockingPiece:
                    moves.append(Move((r,c), (r-1,c+1), self.board, isEnpassantMove=True))

        else:
            kRow, kCol = self.bKlocation
            if self.board[r+1][c] == "--":
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c), (r+1,c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((1,c), (r+2,c), self.board))

            if c > 0 and self.board[r+1][c-1] != "--" and self.board[r+1][c-1][0] == "w":
                if not piecePinned or pinDirection == (1,-1):
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            elif c > 0 and (r+1, c-1) == self.enpassantPossible:
                attackingPiece = blockingPiece = False
                if kRow == r:
                    if kCol < c:
                        insideRange = range(kCol+1, c-1)
                        outsideRange = range(c+1, 8)
                    else:
                        insideRange = range(kCol-1, c, -1)
                        outsideRange = range(c-2, -1, -1)
                    for i in insideRange:
                        if self.board[r][i] != "--":
                            blockingPiece = True
                    for i in outsideRange:
                        square = self.board[r][i]
                        if square[0] == "w" and (square[1] == "Q" or square[1] == "R"):
                            attackingPiece = True
                        elif square != "--":
                            blockingPiece = True
                if not attackingPiece or blockingPiece:
                    moves.append(Move((r,c), (r+1,c-1), self.board, isEnpassantMove=True))

            if c < 7 and self.board[r+1][c+1] != "--" and self.board[r+1][c+1][0] == "w":
                if not piecePinned or pinDirection == (1,1):
                    moves.append(Move((r,c), (r+1,c+1), self.board))
            elif c < 7 and (r+1, c+1) == self.enpassantPossible:
                attackingPiece = blockingPiece = False
                if kRow == r:
                    if kCol < c:
                        insideRange = range(kCol+1, c)
                        outsideRange = range(c+2, 8)
                    else:
                        insideRange = range(kCol-1, c+1, -1)
                        outsideRange = range(c-1, -1, -1)
                    for i in insideRange:
                        if self.board[r][i] != "--":
                            blockingPiece = True
                    for i in outsideRange:
                        square = self.board[r][i]
                        if square[0] == "w" and (square[1] == "Q" or square[1] == "R"):
                            attackingPiece = True
                        elif square != "--":
                            blockingPiece = True
                if not attackingPiece or blockingPiece:
                    moves.append(Move((r,c), (r+1,c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemy = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        end = self.board[endRow][endCol]
                        if end == "--":
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        elif end[0] == enemy:
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        directions = ((-1,-2), (-1,2), (1,2), (1,-2), (-2,-1), (-2,1), (2,-1), (2,1))
        ally = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    end = self.board[endRow][endCol]
                    if end[0] != ally:
                        moves.append(Move((r,c), (endRow,endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemy = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        end = self.board[endRow][endCol]
                        if end == "--":
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        elif end[0] == enemy:
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                end = self.board[endRow][endCol]
                if end[0] != ally:
                    if ally == "w":
                        self.wKlocation = (endRow, endCol)
                    else:
                        self.bKlocation = (endRow, endCol)
                    Check, pins, checks = self.checkForPinsandCheck()
                    if not Check:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    if ally == "w":
                        self.wKlocation = (r, c)
                    else:
                        self.bKlocation = (r, c)

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    
    def getCastleMoves(self, r, c, moves, ally):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves, ally)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves, ally)

    def getKingSideCastleMoves(self, r, c, moves, ally):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--" and not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
            moves.append(Move((r,c), (r,c+2), self.board, isCastleMove=True))
    
    def getQueenSideCastleMoves(self, r, c, moves, ally):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--" and not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
            moves.append(Move((r,c), (r,c-2), self.board, isCastleMove=True))

class CastlingRights():

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():

    def __init__(self, startSquare, endSquare, board, isEnpassantMove=False, isCastleMove=False):

        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.isPawnPromotion = ((self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7))

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

        self.isCastleMove = isCastleMove

        self.moveID = self.pieceMoved + str(self.startRow) + str(self.startCol) + str(self.endRow) + str(self.endCol)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False