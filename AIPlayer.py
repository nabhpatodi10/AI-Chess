import random
import numpy as np

pieceScore = {"K":900, "Q":90, "R":50, "B":30, "N":30, "p":10}

knightScores = np.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]])

whiteBishopScores = np.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                                [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                                [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                                [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                                [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]])

blackBishopScores = np.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                                [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                                [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                                [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                                [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]])

queenScores = np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]])

whiteRookScores = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]])

blackRookScores = np.array([[0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

whitePawnMoves = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

blackPawnMoves = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

whiteKingMoves = np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]])

blackKingMoves = np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]])

piecePositionScores = {"N":knightScores, "wB":whiteBishopScores, "bB":blackBishopScores, "Q":queenScores, "wR":whiteRookScores, "bR":blackRookScores, "bp":blackPawnMoves, "wp":whitePawnMoves, "wK":whiteKingMoves, "bK":blackKingMoves}

CHECKMATE = 10000
STALEMATE = 0
DEPTH = 4

def recursiveHelper(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    recursiveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove

def randomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def recursiveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -recursiveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.moveUndo()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1] == "K":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "p":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "B":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "R":
                    piecePositionScore = piecePositionScores[square][row][col]
                elif square[1] == "Q":
                    piecePositionScore = piecePositionScores[square[1]][row][col]
                elif square[1] == "N":
                    piecePositionScore = piecePositionScores[square[1]][row][col]
                if square[0] == "w":
                    score += pieceScore[square[1]] + (piecePositionScore * 0.1)
                elif square[0] == "b":
                    score -= pieceScore[square[1]] + (piecePositionScore * 0.1)
    return score