'''Sudoku Solver Main Module'''

import tkinter
import copy # Used for creating copies of variables instead of instances

class SudokuGrid():
    'Creates the sudoku grid'

    def __init__(self, parent): # Parent is the main window
        self.parent = parent
        self.solutions = [] # Stores all the solved grids

        self.grid = [ # Grid representing the 8x8 sudoku grid
        [1,0,6,0,0,2,0,0,0], 
        [0,5,0,0,0,6,0,9,1],
        [0,0,9,5,0,1,4,6,2],
        [0,3,7,9,0,5,0,0,0],
        [5,8,1,0,2,7,9,0,0],
        [0,0,0,4,0,8,1,5,7],
        [0,0,0,2,6,0,5,4,0],
        [0,0,4,1,5,0,6,0,9],
        [9,0,0,8,7,4,2,1,0]
        ]

        self.margin = 20 # Margin size of the sudoku board
        self.side = 50 # Side length of each square in the grid
        self.width = self.height = (self.margin*2) + (self.side*9) # Defines the width and height of the canvas
        self.fonttype = ('Helvetica', 20, 'bold') # Font size in canvas grid
        
        self.row = -1  # Currently selected cell row and colunm
        self.col = -1

        self.__initUI() # Initiates other widgets

    def __initUI(self):
        'Initiates the elements in the grid'

        self.frame = tkinter.Frame(self.parent) # Creates a frame inside the parent 
        self.button = tkinter.Button(self.parent, text='Testing', command=self.__testing) ################################################################################################################################################################
        self.canvas = tkinter.Canvas(self.frame, bg='lightblue', width=self.width, height=self.height) # Sudoku grid

        self.frame.pack()
        self.button.pack() ################################################################################################################################################################
        self.canvas.pack()

        self.__draw_grid() # Draws the grid

        self.canvas.bind('<Button-1>', self.__cell_clicked) # Binds left click to selecting a cell
        self.parent.bind('<Key>', self.__key_pressed) # Binds key pressed to entering a key; must be binded to root

    def __draw_grid(self):
        'Draws the suduku grid'

        for i in range(10):
            if i % 3 == 0: # Every 3 lines switches to black
                color = 'black'
            else:
                color = 'grey'
            
            # Vertical lines
            x0 = self.margin + (i*self.side)
            y0 = self.margin
            x1 = self.margin + (i*self.side)
            y1 = self.height - self.margin
            self.canvas.create_line(x0,y0,x1,y1, fill=color)

            # Horizontal lines
            x0 = self.margin
            y0 = self.margin + (i*self.side)
            x1 = self.height - self.margin
            y1 = self.margin + (i*self.side)
            self.canvas.create_line(x0,y0,x1,y1, fill=color)

    def __cell_clicked(self, event):
        '''Handles mouse events

        Takes event as argument'''

        x, y = event.x, event.y # Finds the x and y coordinate of the click
        print(f'Clicked at {x},{y}') ################################################################################################################################################################

        if (self.margin < x < self.width - self.margin) and (self.margin < y < self.height - self.margin): # Checks that the click is inside the grid
            row, col = (y-self.margin)//self.side, (x-self.margin)//self.side # Calculates what row and column the cursor is in
            print(f'Clicked at row {row}, column {col}') ################################################################################################################################################################

            if (row, col) == (self.row, self.col): # If cells is already selected, deselect it
                self.row, self.col = -1, -1

            else: # If it is not selected, select it
                self.row, self.col = row, col

            self.__draw_cursor() # Handles the box selection

        else: # If the user clicks outself.side the canvas
            self.row, self.col = -1, -1 # Resets the currently selected cell row and colunm
            self.canvas.delete('cursor') # Deletes the previous cursor

    def __draw_cursor(self):
        'Draws the border around the clicked square'

        self.canvas.delete('cursor') # Deletes the previous cursor

        if (self.row, self.col) != (-1, -1): # Checks that a box has not been deselected (-1, -1 only occur if deselected)
            x0 = self.margin + self.col*self.side # Defines the boundaries of the rectangle selection cursor
            y0 = self.margin + self.row*self.side
            x1 = self.margin + (self.col+1)*self.side 
            y1 = self.margin + (self.row+1)*self.side 
            self.canvas.create_rectangle(x0, y0, x1, y1, tags='cursor', outline='green', width=3)

    def __key_pressed(self, event):
        '''Handles keyboard events
        
        Takes event as argument'''

        if event.char.isnumeric(): # Only puts number in if it is numberic
            print(self.row, self.col)
            x = self.margin + self.side*self.col + self.side/2 # Finds x and y coords of the centre of the selected square
            y = self.margin + self.side*self.row + self.side/2
            
            tag = f'{x}{y}' # Create a tag depending on the x and y coords of the centre of the selected square
            
            self.canvas.delete(tag) # Deletes previous 
            self.canvas.create_text(x, y, text=event.char, tags=tag, fill='black', font=self.fonttype) # Places a number on the screen

    def __solve_grid(self):
        'Solves the grid and stores each solution as a list in solutions list'
        
        for ypos, row in enumerate(self.grid): # Goes through each row in the column
            for xpos, position in enumerate(row): # Goes through each position in the row
                if position == 0: # Position must be empty
                    for num in range(1,10): # Tries all numbers from 1 to 9
                        if self.__possible(xpos, ypos, num): # Check if the number is a possible
                            self.grid[ypos][xpos] = num # Puts possible number in empty space
                            self.__solve_grid() # Keeps solving
                            self.grid[ypos][xpos] = 0 # If program reaches here, no further numbers can be put into the grid and the square is reset
                    
                    return False # No possible solution has been found for an empty position; exits functions

        # If program reaches this point, there are no more empty spaces in the grid and a solution has been found

        deepcopy_grid = copy.deepcopy(self.grid) # A copy of the original grid is made
        self.solutions.append(deepcopy_grid)
    
    def __possible(self, x, y, n):
        '''Returns True or False if a number can fit in a specific position in the grid 

        Takes in the grid, x position, y position, and value of a possible number'''

        # Checks row
        for position in self.grid[y]:
            if position == n:
                return False

        # Checks column
        for row in self.grid:
            if row[x] == n: 
                return False

        # Checks square
        ranges = [range(0,3), range(3,6), range(6,9)] # Possible grid ranges

        xrange = None # Stores the ranges that x and y are in
        yrange = None

        for possible_range in ranges:
            if x in possible_range:
                xrange = possible_range # If x fits in the range, the range is stored
            if y in possible_range:
                yrange = possible_range # If y fits in the range, the range is stored

        for row in self.grid[yrange[0]:yrange[-1]+1]:
            for position in row[xrange[0]:xrange[-1]+1]:
                if position == n: # Checks every position in the square
                    return False

        return True # No doubles detected

    def __display_solutions(self):
        'Formats and displays all found solutions'

        print(f'\n-----------------------{len(self.solutions)} Solutions Found.-----------------------')
        
        for grid in self.solutions: # Prints out each solution
            print('')
            for row in grid:
                print(row)

    def __testing(self): ################################################################################################################################################################
        'Temporary testing function for button'

        self.__solve_grid() 
        self.__display_solutions()
            
root = tkinter.Tk() # Defines the main window
root.title('Testing Grid')
root.resizable('False', 'False')

sudokugrid = SudokuGrid(root) # Interactive Sudoku Grid is created

root.mainloop()