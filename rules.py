class MoveAnalyser:
    def __init__(self):
        self.take = False
        
    def getMoves(self, board, ref, reverse = False, end = False):
        moves = []
        tile = board.board[ref[0]][ref[1]]

        'Check if the tile has a checker present'
        if tile.hasChecker():
            checker = tile.getChecker()
        else:
            return moves

        'Get the direction of the move by the colour'
        colour = tile.getChecker().getColour()
        if colour == "Red":
            step = -1
        else:
            step = 1

        if reverse == True:
            step = step * -1

        'Check each movement direction'
        for i in range(-1,2,2):
            if ref[1]+i > 7 or ref[1]+i < 0:
                continue

            if ref[0]+step > 7 or ref[0]+step < 0:
                continue

            target = board.board[ref[0]+step][ref[1]+i]

            if not target.hasChecker():
                if self.take == False:
                    moves.append([ref[0]+step, ref[1]+i])
            else:
                if ref[1]+2*i > 7 or ref[1]+2*i < 0:
                    continue
                if ref[0]+step*2 > 7 or ref[0]+step*2 < 0:
                    continue
                
                targcol = target.getChecker().getColour()
                nexttarget = board.board[ref[0]+step*2][ref[1]+i*2].hasChecker()

                if nexttarget == False:
                    if (targcol != colour):
                        moves.append([ref[0]+step*2,ref[1]+i*2])
                        self.take = True

                        
        if tile.getChecker().king() and end != True:
            #if ref[1]+2*i <= 7 and ref[1]+2*i >= 0:
                #if ref[0]+step*2 >= 7 and ref[0]+step*2 <= 0:
            othermoves = self.getMoves(board, ref, True, True)
            moves = moves + othermoves

        'Remove moves if takeing is required'
        if self.take == True:
            for move in moves:
                if move[0] - 2 != ref[0] and move[0] + 2 != ref[0]:
                    moves.remove(move)
        
        return moves
    
    def reset(self):
        self.take = False
