from gui import *
import pygame, os, rules, ai, copy

if __name__ == "__main__":
    WIDTH = 480
    HEIGHT = 800
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Draughts")

    playing = True
    possmoves = []

    takeMoves = [] #If this is not empty only these certain moves can be taken.

    lastselected = None

    mvAn = rules.MoveAnalyser()
    moveTaken = False

    board = Board()

    redPlayer = "Human"
    whitePlayer = "AI"
    
    gameOver = False

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                if event.button == 3:
                    board.undoLastMove()
                board.unHighlightAll()
                ref = board.selectTile(pygame.mouse.get_pos())

                'Catch error if no tile is returned'
                if ref == None:
                    lastselected = None
                    continue
                
                if board.getTile(ref).hasChecker() and board.getTile(ref).getChecker().getColour() == board.getTurn():
                    lastselected = ref
                    
                if possmoves != []:
                    for move in possmoves:
                        if move == ref:
                            if mvAn.take == True:
                                board.moveChecker(lastselected, move, True)
                                board.unHighlightAll()
                                checkMoves = mvAn.getMoves(board, move)   
                                if checkMoves == []:
                                    moveTaken = True
                                    board.changeTurn()
                                    screen.fill((0,0,0))
                                    board.draw(screen)
                                    pygame.display.flip()
                                    pygame.display.update() 
                                    
                            else:
                                
                                board.moveChecker(lastselected, move, False)
                                board.changeTurn()
                                board.unHighlightAll()
                                screen.fill((0,0,0))
                                board.draw(screen)
                                pygame.display.flip()
                                pygame.display.update() 
                                moveTaken = True
                                
                                
                if board.getTile(ref).hasChecker():
                    if board.getTile(ref).getChecker().getColour() == board.getTurn():
                        possmoves = mvAn.getMoves(board, ref)

                for y in range(len(board.board)):
                    for x in range(len(board.board[y])):
                        tile = board.board[y][x]

                        if tile.hasChecker():
                            if tile.getChecker().getColour() == board.getTurn():
                                temp = mvAn.getMoves(board, [y,x])
                                if mvAn.take == True:
                                    takeMoves += temp

                if takeMoves != []:
                    tempMoves = []
                    for move in possmoves:
                        if move in takeMoves:
                            tempMoves.append(move)

                    possmoves = tempMoves
                else:
                    mvAn.reset()
                
                if moveTaken == True:
                    possmoves = []
                    takeMoves = []
                    if board.getTurn() == "Red":
                        if redPlayer == "AI":
                            if board.getTurn() == "Red":
                                newBoard = copy.deepcopy(board)
                                move = ai.getAIMove(board, 5)
                                for i in range(1, len(move[0])):
                                    newBoard.moveChecker(move[0][i-1], move[0][i], move[1])

                                board = newBoard
                                if board.getTurn() == "Red":
                                    board.changeTurn()                 
                                    moveTaken = False
                            
                    else:
                        if whitePlayer == "AI":
                            if board.getTurn() == "White":
                                newBoard = copy.deepcopy(board)
                                move = ai.getAIMove(board, 5)
                                for i in range(1, len(move[0])):
                                    newBoard.moveChecker(move[0][i-1], move[0][i], move[1])
                                    
                                newBoard.highlightTile(move[0][-1])
                                board = newBoard
                                if board.getTurn() == "White":
                                    board.changeTurn()                 
                                    moveTaken = False

                    print(board.redCount)
                    print(board.getTurn())
                    moveTaken = False      
                                

                            
                    
        for move in possmoves:
            board.highlightTile(move)

        #Checking for states in the game
        for tile in board.board[0]:
            if tile.hasChecker():
                if tile.getChecker().getColour() == "Red":
                    tile.checker.setKing()

        for tile in board.board[7]:
            if tile.hasChecker():
                if tile.getChecker().getColour() == "White":
                    tile.checker.setKing()

        #Check count of checkers
        if board.whiteCount == 0:
            print("Red Player Wins!")
            gameOver = True
            board.draw(screen)
        elif board.redCount == 0:
            print("White Player Wins!")
            gameOver = True
            board.draw(screen)

        #Check that players can move
        whiteCanMove = False
        redCanMove = False
        saveState = mvAn.take        
        for row in range(len(board.board)):
            for tile in range(len(board.board[row])):
                mvAn.reset()
                if board.board[row][tile].hasChecker():
                    if board.board[row][tile].getChecker().getColour() == "White":
                        moves = mvAn.getMoves(board, (row,tile))
                        if moves != []:
                            whiteCanMove = True
                            break
                        
        for row in range(len(board.board)):
            for tile in range(len(board.board[row])):
                mvAn.reset()
                if board.board[row][tile].hasChecker():
                    if board.board[row][tile].getChecker().getColour() == "Red":
                        moves = mvAn.getMoves(board, (row,tile))
                        if moves != []:
                            redCanMove = True
                            break

        if whiteCanMove == False:
            print("Red Player Wins!")
        elif redCanMove == False:
            print("White Player Wins!")
        elif whiteCanMove == False and redCanMove == False:
            print("Stalemate!")

        mvAn.take = saveState
                     
        screen.fill((0,0,0))

        board.draw(screen)

        pygame.display.flip()
        pygame.display.update()           


os._exit(0)
