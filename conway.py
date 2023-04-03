import random

class GameBoard: # This class represents the GameBoard itself, and primarily consists of a 2D array
    def __init__(self, size): # This constructor only takes a size argument
        self.size = size
        self.board = [[0 for i in range(size)] for i in range(size)]

    def __init__(self, size, board): # This constructor takes an argument for both size and a pre-existing board 2D array
        self.size = size
        self.board = board

    def __init__(self): # The default constructor; will always initialize with size 10
        self.size = 10
        self.board = [[0 for i in range(self.size)] for i in range(self.size)]

    def initialize(self): # This method instantiates the game board with a randomly chosen population of cells
        for row in range(0, self.board.length):
            for column in range(0, self.board[row].length):
                if random.randint(0, 1) == 1:
                    self.board[row][column] = 'D'
                else:
                    self.board[row][column] = 'A'

    def countLiveNeighbors(self, row ,column):
        rowIndex = row - 1
        columnIndex = column - 1 # Subtract one from each so that they can be used as array indices
        liveNeighborCount = 0

        for i in range(rowIndex, rowIndex + 1):
            for j in range(columnIndex, columnIndex + 1):
                if (i >= self.board.length or j >= self.board[row].length or i < 0 or j < 0 or (i == rowIndex and j == columnIndex)):
                    # Ensure we don't go out of array bounds or count the cell as its own neighbor
                    continue
                elif self.board[i][j] == 'A':
                    liveNeighborCount += 1
        return liveNeighborCount
    
    def doGameTick(self):
        tempBoard = GameBoard(self.size, self.board) # Use a copy of the board to ensure that later cells aren't affected by changes made to earlier cells
        for row in range(1, self.size):
            for column in range(1, self.size):
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


