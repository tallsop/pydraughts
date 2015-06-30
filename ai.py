import rules, random, tree

def evaluateMove(board):
    value = 0
    weights = [1.3, 4, 6, 2, 10]
    terms = []

    #Get variables
    adv = 0
    kingcount = 0
    takecount = 0

    free = 0
    for row in range(len(board.board)):
        for tile in range(len(board.board[row])):
            if board.board[row][tile].hasChecker():
                checker = board.board[row][tile].getChecker()
                
                #Check if it is a king
                if checker.king():
                    kingcount += 1
                    
                #Get advancement
                if checker.getColour() == board.getTurn() and not(checker.king()):
                    if checker.getColour() == "Red":
                        if row > 2:
                            adv += 1
                    else:
                        if row < 5:
                            adv += 1
                            
                #Get if it is free
                isFree = True
                positions = [[row+1,tile+1], [row+1,tile-1], [row-1,tile+1],
                             [row-1,tile-1]]

                for pos in positions:
                    if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
                        continue

                    if board.board[pos[0]][pos[1]].hasChecker() == True:
                        isFree = False
                        break

                if isFree == True:
                    free += 1

    terms.append(adv)

    #Get the number of man pieces
    if board.getTurn() == "Red":
        terms.append(board.redCount - kingcount)
        terms.append(kingcount)
    else:
        terms.append(board.whiteCount - kingcount)
        terms.append(kingcount)

    if board.getTurn() == "Red" and board.redCount == 0:
        return float("-inf")
    elif board.getTurn() == "Red" and board.whiteCount == 0:
        return float("inf")
    elif board.getTurn() == "White" and board.whiteCount == 0:
        return float("-inf")
    elif board.getTurn() == "White" and board.redCount == 0:
        return float("inf")

    terms.append(free)

    if board.getTurn() == "Red":
        terms.append(board.redCount - board.whiteCount)
    else:
        terms.append(board.whiteCount - board.redCount)
       
    #Summation of terms and weights
    for weight in weights:
        for term in terms:
            value += weight*term

    return value

def getAIMove(board, depth):
    maxValue = 0
    bestMove = None
    allMoves = tree.getAllMoves(board)
    print("Thinking...")
    for move in allMoves[0]:
        undos = 0
        for i in range(1, len(move)):
            board.moveChecker(move[i-1], move[i], allMoves[1])
            undos+=1
            
        root = tree.Node()
        
        tempScore = root.genTree(board, depth, float("-inf"), float("inf"), True)
        if tempScore > maxValue:
            maxValue = tempScore
            bestMove = move
            
        for i in range(undos):
            board.undoLastMove()

    print("Your Turn.")
            
    return (bestMove, allMoves[1])

