#Game Tree Creation
import rules, gui, copy, ai

def printBoard(board):
    #Used for testing! :D
    array = []
    for i in range(8):
        array.append([])

    for row in range(len(board.board)):
        for tile in board.board[row]:
            if tile.hasChecker():
                if tile.getChecker().getColour() == "Red":
                    array[row].append("R")
                else:
                    array[row].append("W")
            else:
                array[row].append("B")

        print(array[row])

    print("\n")
    print("\n")
    print("\n")

class TakeMoves:
    def __init__(self):
        self.moves = []

    def generateMoves(self, board, ref):
        moveGen = rules.MoveAnalyser()
        mvs = moveGen.getMoves(board, ref[-1])

        if moveGen.take == True:
            for mv in mvs:
                board.moveChecker(ref[-1], mv, True)
                temp = list(ref)
                temp.append(mv)
                self.generateMoves(board, temp)
                board.undoLastMove()
                
        else:
            self.moves.append(ref)

        
def getAllMoves(board):
    theMoves = []
    
    takeBefore = False
    for row in range(len(board.board)):
        for tile in range(len(board.board[row])):      
            if board.getTile((row,tile)).hasChecker() and board.getTile((row,tile)).getChecker().getColour() == board.getTurn():
                moveGen = rules.MoveAnalyser()
                moves = moveGen.getMoves(board, (row,tile))
                if takeBefore == False or (takeBefore == True and moveGen.take == True):
                    for move in moves:
                        if moveGen.take == False:
                            theMoves.append(((row,tile),move))
                        else:
                            if takeBefore == False:
                                theMoves = []
                                takeBefore = True
                                
                            moveGet = TakeMoves()
                            moveGet.generateMoves(board, [(row,tile)])
                            extraMoves = moveGet.moves
                            theMoves += extraMoves
                        
    return (theMoves, takeBefore)

class Node:
    def __init__(self):
        self.nodes = []

    def genTree(self, board, depth, alpha, beta, maximum):
        allMoves = getAllMoves(board)
        if depth == 0:
            return ai.evaluateMove(board)
        
        if maximum == True:
            for moves in allMoves[0]:
                undos = 0
                
                for i in range(1,len(moves)):
                    board.moveChecker(moves[i-1], moves[i], allMoves[1])
                    undos+=1

                board.changeTurn()
                alpha = max(alpha, self.genTree(board, depth-1, alpha, beta, not(maximum)))

                for i in range(undos):
                    board.undoLastMove()
                
                if beta <= alpha:
                    break

            return alpha
        else:
            for moves in allMoves[0]:
                undos = 0
                for i in range(1,len(moves)):
                    board.moveChecker(moves[i-1], moves[i], allMoves[1])
                    undos+=1

                board.changeTurn()
                beta = min(beta, self.genTree(board, depth-1, alpha, beta, not(maximum)))

                for i in range(undos):
                    board.undoLastMove()
                    
                if beta <= alpha:
                    break
            
            
            return beta

