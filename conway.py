# A program to run Conway's Game Of Life, by Owen Hiskey
# Features graphics with tkinter


# Import necessary libraries
import random
import tkinter as tk


class GameBoard:  # This class represents the GameBoard itself, and primarily consists of a 2D array
    # This constructor takes two arguments; one for rows and one for columns
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = [[0 for i in range(columns)] for i in range(rows)]
        self.generationCount = 0
        self.initialize()

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
        self.generationCount += 1
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

    def getIndex(self, row, column): # Method to retrieve the cell at a specific index
        return self.board[row - 1][column - 1]

    def setIndex(self, row, column, newValue): # Method to update the cell at a specific index
        self.board[row - 1][column - 1] = newValue

    def __repr__(self): # toString method; ensures that the cells are displayed in a grid rather than one line
        returnStr = ''
        for i in range(0, self.rows):
            returnStr += str(self.board[i]) + '\n'
        return returnStr
# End of GameBoard class


class Interface(tk.Frame):  # A class for the GUI component of the game

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        for i in range(4):
            self.columnconfigure(i, weight = 1)
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
        self.rowPrompt.grid(row = 0, column = 0)
        self.rowEntry.grid(row = 1, column = 0)
        self.colPrompt.grid(row = 2, column = 0)
        self.colEntry.grid(row = 3, column = 0)
        self.output.grid(row = 1, column = 1)
        self.submit.grid(row = 4, column = 0)
        self.exit.grid(row = 4, column = 4)

    def createGame(self):
        try:
            rows = int(self.rowEntry.get())
            cols = int(self.colEntry.get())
        except ValueError:
            self.output.configure(text = "Please only enter valid digits!")
        self.rowPrompt.destroy()
        self.rowEntry.destroy()
        self.colPrompt.destroy()
        self.colEntry.destroy()
        self.submit.destroy()
        self.output.destroy()
        board = GameBoard(rows, cols)
        self.livingcell = tk.PhotoImage(file = 'livingcell.png').subsample(4, 4)
        self.deadcell = tk.PhotoImage(file = 'deadcell.png').subsample(4, 4)
        photolist = []
        print(str(board))
        for row in range(rows):
            for col in range(cols):
                if board.getIndex(row + 1, col + 1) == 'A':
                    photolist.append(tk.Label(self.parent, image = self.livingcell))
                else:
                    photolist.append(tk.Label(self.parent, image = self.deadcell))
                photolist[-1].grid(row = row, column = col)
        newGameButton = tk.Button(self.parent, text = "New game", command = self.newGame)
        newGameButton.grid(column = 4, row = 5)
        genLabel = tk.Label(self.parent, text = str(board.generationCount) + ' generations', anchor = 'w')
        genLabel.grid(column = 2, row = 0)

    def newGame(self): # Creates a new game
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.initializeGui()

# End of the Interface class

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life")
    Interface(root)
    root.mainloop()
