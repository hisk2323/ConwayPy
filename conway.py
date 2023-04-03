# A program to run Conway's Game Of Life, by Owen Hiskey
# Features graphics


# Import necessary libraries
import random
import tkinter as tk


class GameBoard:  # This class represents the GameBoard itself, and primarily consists of a 2D array
    # This constructor takes two arguments; one for rows and one for columns
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = [[0 for i in range(columns)] for i in range(rows)]

    # This method instantiates the game board with a randomly chosen population of cells
    def initialize(self):
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                if random.randint(0, 1) == 1:
                    self.board[row][column] = 'D'
                else:
                    self.board[row][column] = 'A'

    def countLiveNeighbors(self, row, column):
        rowIndex = row - 1
        # Subtract one from each so that they can be used as array indices
        columnIndex = column - 1
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
        # Use a copy of the board to ensure that later cells aren't affected by changes made to earlier cells
        tempBoard.board = self.board
        for row in range(1, self.rows + 1):
            for column in range(1, self.columns + 1):
                liveNeighbors = tempBoard.countLiveNeighbors(row, column)
                currentValue = tempBoard.getIndex(row, column)
                # This allows us to update the current board based only on the unaltered copy that exists inside tempBoard

                # Rules section

                # Rule 1: Any live cell with fewer than two live neighbors dies, as if caused by under-population
                if currentValue == 'A' and liveNeighbors < 2:
                    self.setIndex(row, column, 'D')
                # Rule 2: Any live cell with two or three live neighbors lives on to the next generation
                elif currentValue == 'A' and (liveNeighbors == 2 or liveNeighbors == 3):
                    continue
                # Rule 3: Any live cell with more than three live neighbors dies, as if by over-population
                elif currentValue == 'A' and liveNeighbors > 3:
                    self.setIndex(row, column, 'D')
                # Rule 4: Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction
                elif currentValue == 'D' and liveNeighbors == 3:
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


class Interface(tk.Frame):  # A class for the GUI component of the game

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initializeGui()

    def initializeGui(self):
        self.rowPrompt = tk.Label(self.parent, text="Enter a number of rows: ", anchor='w')
        self.rowEntry = tk.Entry(self.parent)
        self.colPrompt = tk.Label(self.parent, text = "Enter a number of columns: ", anchor = 'w')
        self.colEntry = tk.Entry(self.parent)
        self.submit = tk.Button(self.parent, text = "Submit", command = self.createGame)
        self.exit = tk.Button(self.parent, text = "Quit", command = self.parent.destroy)
        self.output = tk.Label(self.parent, text = '')

        # Lay the widgets on the screen
        self.rowPrompt.pack(side = "top", fill = "x")
        self.rowEntry.pack(side = "top", fill = "x")
        self.colPrompt.pack(side = "top", fill = "x")
        self.colEntry.pack(side = "top", fill = "x")
        self.output.pack(side = "top", fill = "x", expand = True)
        self.submit.pack(side = "left")
        self.exit.pack(side = "right")

    def createGame(self):
        try:
            rows = int(self.rowEntry.get())
            cols = int(self.colEntry.get())
            result = "%s rows, %s columns" % (rows, cols)
        except ValueError:
            result = "Please only enter valid digits!"
        self.output.configure(text = result) 

# End of the Interface class

if __name__ == "__main__":
    root = tk.Tk()
    Interface(root)
    root.mainloop()
