# Import necessary libraries
import random

class GameBoard: # This class represents the GameBoard itself, and primarily consists of a 2D array
    def __init__(self, rows, columns): # This constructor takes two arguments; one for rows and one for columns
        self.rows = rows
        self.columns = columns
        self.board = [[0 for i in range(columns)] for i in range(rows)]

    def initialize(self): # This method instantiates the game board with a randomly chosen population of cells
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                if random.randint(0, 1) == 1:
                    self.board[row][column] = 'D'
                else:
                    self.board[row][column] = 'A'

    def countLiveNeighbors(self, row, column):
        rowIndex = row - 1
        columnIndex = column - 1 # Subtract one from each so that they can be used as array indices
        liveNeighborCount = 0

        for i in range(rowIndex - 1, rowIndex + 2):
            for j in range(columnIndex - 1, columnIndex + 2):
                if (i >= self.rows or j >= self.columns or i < 0 or j < 0 or (i == rowIndex and j == columnIndex)):
                    # Ensure we don't go out of array bounds or count the cell as its own neighbor
                    continue
                elif self.board[i][j] == 'A':
                    liveNeighborCount += 1
        return liveNeighborCount
    
    def doGameTick(self):
        tempBoard = GameBoard(self.rows, self.columns) 
        tempBoard.board = self.board # Use a copy of the board to ensure that later cells aren't affected by changes made to earlier cells
        for row in range(1, self.rows + 1):
            for column in range(1, self.columns + 1):
                liveNeighbors = tempBoard.countLiveNeighbors(row, column)
                currentValue = tempBoard.getIndex(row, column)
                # This allows us to update the current board based only on the unaltered copy that exists inside tempBoard

                # Rules section

                if currentValue == 'A' and liveNeighbors < 2: # Rule 1: Any live cell with fewer than two live neighbors dies, as if caused by under-population
                    self.setIndex(row, column, 'D')
                elif currentValue == 'A' and (liveNeighbors == 2 or liveNeighbors == 3): # Rule 2: Any live cell with two or three live neighbors lives on to the next generation
                    continue
                elif currentValue == 'A' and liveNeighbors > 3: # Rule 3: Any live cell with more than three live neighbors dies, as if by over-population
                    self.setIndex(row, column, 'D')
                elif currentValue == 'D' and liveNeighbors == 3: # Rule 4: Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction
                    self.setIndex(row, column, 'A')

    def getIndex(self, row, column):
        return self.board[row - 1][column - 1]
    
    def setIndex(self, row, column, newValue):
        self.board[row - 1][column - 1] = newValue
    
    def getSize(self):
        return self.size
    
    def __repr__(self):
        returnStr = ''
        for i in range(0, self.rows):
            returnStr += str(self.board[i]) + '\n'
        return returnStr
# End of GameBoard class
    
myBoard = GameBoard(3, 2)
myBoard.initialize()
print(str(myBoard) + '\n')
myBoard.doGameTick()
print(str(myBoard))