'''Sudoku Solver Main Module'''

import tkinter
import copy # Used for creating copies of variables instead of instances
import threading # Multithreading module

# To retrieve the text from an item with object ID I on a canvas C, call C.itemcget(I, 'text').
# To replace the text in an item with object ID I on a canvas C with the text from a string S, call C.itemconfigure(I, text=S). 

class GraphicalInterface:
    'Creates the entire GUI'

    def __init__(self, parent): # Parent is the main window
        self.parent = parent # Parent root frame

        self.solutions = [] # Stores all solved grids
        self.allowed = False # Sets the flag indicating whether the solver thread is allowed to run

        self.margin = 20 # Margin size of the sudoku board
        self.side = 50 # Side length of each square in the grid
        self.width = self.height = (self.margin*2) + (self.side*9) # Defines the width and height of the canvas

        self.fonttype = ('Helvetica', 20, 'bold') # Stores the font type of the canvas text
        
        self.row = None  # Currently selected cell row and colunm
        self.col = None

        self.__widgets() # Initiates other widgets

    ### PACKING WIDGETS

    def __widgets(self):
        'Initiates the widgets in the grid'

        self.frame = tkinter.Frame(self.parent) # Creates a frame inside the parent 
        self.start_btn = tkinter.Button(self.parent, text='Start', command=self.__start) # Start button
        self.stop_btn = tkinter.Button(self.parent, text='Stop', command=self.__stop) # Stop button
        self.canvas = tkinter.Canvas(self.frame, bg='lightblue', width=self.width, height=self.height) # Sudoku grid

        self.frame.pack()
        self.start_btn.pack()
        self.stop_btn.pack() 
        self.canvas.pack()

        self.__draw_grid() # Draws the grid

        self.canvas.bind('<Button-1>', self.__cell_clicked) # Binds left click to selecting a cell
        self.parent.bind('<Key>', self.__key_pressed) # Binds key pressed to entering a key; must be binded to root

    def __draw_grid(self):
        'Draws the Suduku Grid'

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

    ### MOUSE AND KEYBOARD INPUT HANDLING

    def __cell_clicked(self, event):
        '''Handles mouse clicks

        Takes event as argument'''

        x, y = event.x, event.y # Finds the x and y coordinate of the click
        print(f'Clicked at {x},{y}') 

        if (self.margin < x < self.width - self.margin) and (self.margin < y < self.height - self.margin): # Checks that the click is inside the grid
            row, col = (y-self.margin)//self.side, (x-self.margin)//self.side # Calculates what row and column the cursor is in
            print(f'Clicked at row {row}, column {col}') 

            if (row, col) == (self.row, self.col): # If cell is already selected, deselect it
                self.row, self.col = None, None

            else: # If it is not selected, select it
                self.row, self.col = row, col

            self.__draw_border() # Handles the box selection

        else: # If the user clicks outside the canvas
            self.row, self.col = None, None # Resets the currently selected cell row and colunm
            self.canvas.delete('cursor') # Deletes the previous cursor

    def __draw_border(self):
        'Draws the border around the clicked square'

        self.canvas.delete('cursor') # Deletes the previous cursor

        if (self.row, self.col) != (None, None): # Checks that a box has not been deselected 
            x0 = self.margin + self.col*self.side # Defines the boundaries of the rectangle selection cursor
            y0 = self.margin + self.row*self.side
            x1 = self.margin + (self.col+1)*self.side 
            y1 = self.margin + (self.row+1)*self.side 
            self.canvas.create_rectangle(x0, y0, x1, y1, tags='cursor', outline='green', width=3) # Creates the cursor

    def __key_pressed(self, event):
        '''Handles keyboard key presses
        
        Takes event as argument'''

        if (self.row, self.col) != (None, None) and event.char.isnumeric(): # Checks that a square is selected and the entered key is a digit
            self.__display_number(self.row, self.col, event.char)

    ### START/STOP METHODS

    def __start(self):
        'Begins the dynamic solving of the grid'

        self.grid = [ # Grid representing the 8x8 sudoku grid which is initially empty
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # Places each user-entered number into self.grid
        for ypos, row in enumerate(self.grid): # Goes through each row in the grid
            for xpos, _ in enumerate(row): # Goes through each position in the row
                    grid_object = self.canvas.find_withtag((ypos,xpos),) # Gets the grid number object with tag at respective position (row, column)
                    value = self.canvas.itemcget(grid_object, 'text') # Gets the value of the specific grid number; 'text' argument specifies we want to extract the text

                    if value: # If the cell is filled in
                        self.grid[ypos][xpos] = int(value)
                    else: # If the cell is empty
                        self.grid[ypos][xpos] = 0

        self.grid = [ # A grid used as an example
        [1, 0, 6, 0, 0, 2, 0, 0, 0], 
        [0, 5, 0, 0, 0, 6, 0, 9, 1],
        [0, 0, 9, 5, 0, 1, 4, 6, 2],
        [0, 3, 7, 9, 0, 5, 0, 0, 0],
        [5, 8, 1, 0, 2, 7, 9, 0, 0],
        [0, 0, 0, 4, 0, 8, 1, 5, 7],
        [0, 0, 0, 2, 6, 0, 5, 4, 0],
        [0, 0, 4, 1, 5, 0, 6, 0, 9],
        [9, 0, 0, 8, 7, 4, 2, 1, 0]
        ]

        self.__update_grid() # Updates the grid
        threading.Thread(target=self.__solver_thread).start() # Initiates the solver thread                

    def __stop(self):
        'Interrupts the dynamic solving of the grid'

        self.allowed = False # Disallowes the solver thread from running

    def __solver_thread(self):
        'Thread that solves the grid and then displays the found solutions'

        self.allowed = True # Allows the solver thread to run

        exit_value = self.__solve_grid() # Solves the grid and returns True (was interrupted) or False (was not interrupted) as the exit code

        if not exit_value: # If it was not interrupted
            self.__display_solutions() # Displays the solutions

        print(f'Exit value: {exit_value}')

    ### LOGIC HANDLING METHODS

    def __solve_grid(self):
        'Solves the grid and stores each solution as a list in solutions list. Displays each iteration of the solving algorithm'
        
        for ypos, row in enumerate(self.grid): # Goes through each row in the grid
            for xpos, position in enumerate(row): # Goes through each position in the row
                if position == 0: # Position must be empty
                    for num in range(1,10): # Tries all numbers from 1 to 9
                        if not self.allowed: # Not allowed to run
                            return True # Returns True; it was interrupted
                        if self.__possible(xpos, ypos, num): # Check if the number is a possible
                            self.grid[ypos][xpos] = num # Puts possible number in empty space
                            self.__display_number(ypos, xpos, num)

                            self.__solve_grid() # Keeps solving

                            self.grid[ypos][xpos] = 0 # If program reaches here, no further numbers can be put into the grid and the square is reset
                            self.__display_number(ypos, xpos, 0)
                    
                    return False # No possible solution has been found for an empty position; Exits function by returning None as it was not interrupted

        # If program reaches this point, there are no more empty spaces in the grid and a solution has been found
        deepcopy_grid = copy.deepcopy(self.grid) # A copy of the original grid is made
        self.solutions.append(deepcopy_grid) # Solution added to list of solutions
    
    def __possible(self, x, y, n):
        '''Returns True or False if a number can fit in a specific position in the grid 

        Takes in x position, y position, and value of a possible number'''

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

    ### DISPLAYER METHODS

    def __update_grid(self):
        'Loads the grid and displays each number'

        for ypos, row in enumerate(self.grid): # Goes through each row in the grid
            for xpos, position in enumerate(row): # Goes through each position in the row
                    self.__display_number(ypos, xpos, position) # Displays the number

    def __display_number(self, row, column, n): 
        '''Displays a given number on the grid
        
        Takes in the row number, column number, and the value of the number to display'''

        x = round(self.margin + self.side*column + self.side/2) # Finds x and y coords of the centre of the selected square
        y = round(self.margin + self.side*row + self.side/2) # Coordinates are rounded to nearest integer
        
        tag = (row,column) # Create a tag from 00 to 88 representing the row and column the selected square is in
        # print(f'Tag: {tag}') DEBUGGING PURPOSES
        
        self.canvas.delete(tag) # Deletes previous 
        self.canvas.create_text(x, y, text=n, tags=(tag,), fill='black', font=self.fonttype) # Places a number on the screen with tagged position
        # tags argument should be a tuple or string

    def __display_solutions(self):
        'Formats and displays all found solutions'

        print(f'\n-----------------------{len(self.solutions)} Solutions Found.-----------------------')
        
        for grid in self.solutions: # Prints out each solution
            print('')
            for row in grid:
                print(row)
            
root = tkinter.Tk() # Defines the main window
root.title('Testing Grid')
root.resizable('False', 'False')

GraphicalInterface(root) # GUI instance is created

root.mainloop()