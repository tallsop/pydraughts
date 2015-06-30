import pygame, copy

class Board:
    def __init__(self):
        self.board = []
        self.turn = "Red"

        self.redCount = 12
        self.whiteCount = 12

        #Things for redoing
        self.delete = []
        self.add = []

        #Make board
        colour1 = (238,224,176)
        colour2 = (101,73,44)
        
        currentCol = colour1
        
        for i in range(8):
            temp = []
            for n in range(8):
                temp.append(Tile([60*n, 60*i], currentCol))
                if currentCol == (238,224,176):
                    currentCol = colour2
                else:
                    currentCol = colour1
            
            if currentCol == (238,224,176):
                currentCol = colour2
            else:
                currentCol = colour1

            self.board.append(temp)

        #Setup board matrix
        start = 1

        for row in range(len(self.board)):
            for tile in range(start, len(self.board[row]), 2):
                if row < 3:
                    self.board[row][tile].addChecker(Checker((255,255,255), True))
                elif row > 4:
                    self.board[row][tile].addChecker(Checker((132,0,0), False))
                else:
                    break

            if start == 1:
                start = 0
            else:
                start = 1

    def moveChecker(self, start, end, take = False):
        self.add.append([])
        temp = self.board[start[0]][start[1]].getChecker()

        if temp.getColour() == "Red":
            newCheck = Checker((132,0,0), False)
        else:
            newCheck = Checker((255,255,255), True)

        if temp.king() == True:
            newCheck.setKing()

        self.add[-1].append((newCheck, start))

        self.board[start[0]][start[1]].removeChecker()
        self.delete.append(end)
        self.board[end[0]][end[1]].addChecker(temp)
        
        if take == True:
            checkx = start[0] - end[0]
            checky = start[1] - end[1]

            if checkx > 0:
                checkx -= 1
            else:
                checkx += 1

            if checky > 0:
                checky -= 1
            else:
                checky += 1
                
            checkP = [end[0] + checkx, end[1] + checky]
            
            if self.getTile(checkP).getChecker().getColour() == "White":
                colour = "Red"
                self.redCount -= 1
            else:
                colour = "White"
                self.whiteCount -= 1


            temp = self.board[checkP[0]][checkP[1]].getChecker()

            if temp.getColour() == "Red":
                newCheck = Checker((132,0,0), False)
            else:
                newCheck = Checker((255,255,255), True)
                
            if temp.king() == True:
                newCheck.setKing()
                    
            self.add[-1].append((newCheck, checkP))
            self.deleteChecker(checkP)



    def deleteChecker(self, tile):
        self.board[tile[0]][tile[1]].removeChecker()

    def getTile(self, ref):
        return self.board[ref[0]][ref[1]]

    def draw(self, target):
        for row in self.board:
            for tile in row:
                tile.draw(target)

    def undoLastMove(self):
        self.deleteChecker(self.delete[-1])
        for item in self.add[-1]:
            self.board[item[1][0]][item[1][1]].addChecker(item[0])

        self.recountScores()

        self.add.pop(-1)
        self.delete.pop(-1)
                         
    def unHighlightAll(self):
        for row in self.board:
            for tile in row:
                tile.unhighlight()
                if tile.hasChecker():
                    tile.unhighlightChecker()

    def highlightTile(self, ref):
        self.board[ref[0]][ref[1]].highlight()

    def selectTile(self, mousepos):
        self.unHighlightAll()
        
        for row in range(len(self.board)):
            for tile in range(len(self.board[row])):
                pos = self.board[row][tile].getPos()
                if mousepos[0] >= pos[0] and mousepos[0] <= pos[0]+60:
                    if mousepos[1] >= pos[1] and mousepos[1] <= pos[1]+60:
                        if self.board[row][tile].hasChecker() == True:
                            if self.board[row][tile].getChecker().getColour() == self.turn:
                                self.board[row][tile].highlightChecker()
                        return [row,tile]

    def changeTurn(self):
        if self.turn == "Red":
            self.turn = "White"
        else:
            self.turn = "Red"

    def getTurn(self):
        return self.turn

    def recountScores(self):
        self.redCount = 0
        self.whiteCount = 0

        for row in self.board:
            for tile in row:
                if tile.hasChecker():
                    if tile.getChecker().getColour() == "Red":
                        self.redCount += 1
                    else:
                        self.whiteCount += 1
        
class Tile:
    def __init__(self, pos, colour):
        self.pos = pos
        self.colour = colour
        self.checker = None
        self.hlight = False

    def getPos(self):
        return self.pos
    
    def draw(self, target):
        if self.hlight == False:
            pygame.draw.rect(target, self.colour, (self.pos[0], self.pos[1],
                                             60,60))
        else:
            pygame.draw.rect(target, (23,121,53), (self.pos[0], self.pos[1],
                                             60,60))
            
        if self.checker != None:
            if not self.checker.king():
                if self.checker.hlight == False:
                    pygame.draw.circle(target, self.checker.colour,
                                   (self.pos[0]+30,self.pos[1]+30),20)
                else:
                    pygame.draw.circle(target, (192,192,192),
                                   (self.pos[0]+30,self.pos[1]+30),20)

            else:
                if self.checker.hlight == False:
                    pygame.draw.circle(target, self.checker.colour,
                                   (self.pos[0]+30,self.pos[1]+30),20)
                    pygame.draw.circle(target, (255,168,0),
                                (self.pos[0]+30,self.pos[1]+30), 10)
                else:
                    pygame.draw.circle(target, (192,192,192),
                                   (self.pos[0]+30,self.pos[1]+30),20)
                    pygame.draw.circle(target, (100,100,100),
                                (self.pos[0]+30,self.pos[1]+30), 10)
        
    def addChecker(self, obj):
        self.checker = obj

    def removeChecker(self):
        self.checker = None

    def getChecker(self):
        return self.checker

    def hasChecker(self):
        if self.checker != None:
            return True
        else:
            return False

    def highlightChecker(self):
        self.checker.highlight()

    def unhighlightChecker(self):
        self.checker.unhighlight()

    def highlight(self):
        self.hlight = True

    def unhighlight(self):
        self.hlight = False

class Checker():
    def __init__(self, colour, isWhite):
        self.colour = colour
        self.isKing = False
        self.hlight = False
        self.isWhite = isWhite

    def setKing(self):
        self.isKing = True

    def highlight(self):
        self.hlight = True

    def unhighlight(self):
        self.hlight = False
        
    def getColour(self):
        if self.isWhite == True:
            return "White"
        else:
            return "Red"

    def king(self):
        return self.isKing
