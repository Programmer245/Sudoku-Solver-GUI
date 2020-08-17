'''Sudoku Solver Main Module'''

import tkinter
from tkinter import ttk # Used for scrollbar
from tkinter import messagebox # Used for message boxes 

import copy # Used for creating copies of variables instead of instances

import threading # Multithreading module

import os # Module for opening files

import time # Time module for delays

# To retrieve the text from an item with object ID I on a canvas C, call C.itemcget(I, 'text').
# To replace the text in an item with object ID I on a canvas C with the text from a string S, call C.itemconfigure(I, text=S). 

class GraphicalInterface:
    'Creates the entire GUI'

    def __init__(self, parent): # Parent is the main window
        self.parent = parent # Parent root frame

        self.empty_grid = [ # Empty grid used to reset program
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

        self.solutions = [] # Stores all solved grids
        self.allowed = False # Sets the flag indicating whether the solver thread is allowed to run

        self.margin = 20 # Margin size of the sudoku board
        self.side = 40 # Side length of each square in the grid
        self.width = self.height = (self.margin*2) + (self.side*9) # Defines the width and height of the canvas

        self.buttonfont = ('Helvetica', 10, 'bold') # Font type of buttons
        self.statusfont = ('Helvetica', 7) # Font type for the status bar
        self.gridfont = ('Helvetica', 20, 'bold') # Font type of sudoku grid
        
        self.row = None  # Currently selected cell row and colunm
        self.col = None

        self.__widgets() # Initiates other widgets

    ### PACKING WIDGETS

    def __widgets(self):
        'Initiates the widgets in the grid'

        ### MENUBAR 

        menubar = tkinter.Menu(root) # Creates the menubar object 
        root.config(menu=menubar) # Sets menubar object in root

        option_submenu = tkinter.Menu(menubar, tearoff=0) # Creates options submenu 
        menubar.add_cascade(label='Options', menu=option_submenu) # Places the submenu inside the menubar
        option_submenu.add_checkbutton(label='Auto Save') # Adds a checkbutton to the option submenu
        option_submenu.add_separator() # Adds a line separator
        option_submenu.add_command(label='Exit', command=exit) # Adds exit button

        help_submenu = tkinter.Menu(menubar, tearoff=0) # Creates help submenu 
        menubar.add_cascade(label='Help', menu=help_submenu) # Places the submenu inside the menubar
        help_submenu.add_command(label='About Sudoku Solver', command=self.__about) # About button that opens README.md
        help_submenu.add_separator() # Adds a line separator
        help_submenu.add_command(label='Licence', command=self.__licence) # Licence button that opens LICENCE.md

        ### SCROLLBAR & STATUS LABEL

        self.scrollbar = tkinter.Scrollbar(root) # Scrollbar for the text widget
        self.scrollbar.grid(row=0, column=2, sticky=tkinter.NS) # sticky parameter makes scrollbar stretch from top to bottom; added on right side of GUI

        self.status_bar = tkinter.Label(root, text='Awaiting commands.', font=self.statusfont, bg='lightgrey', anchor=tkinter.E) # Status bar for displaying various status updates
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky=tkinter.EW) # sticky parameter makes the label stretch from left to right; added at the bottom of the GUI
        
        ### LEFT FRAME (Contains Sudoku Grid)

        self.left_frame = tkinter.Frame(self.parent) # Left frame placed inside the root widget
        self.canvas = tkinter.Canvas(self.left_frame, bg='lightblue', width=self.width, height=self.height) # Sudoku grid canvas

        self.left_frame.grid(row=0, column=0) # Positions the frame on the left of the GUI
        self.canvas.grid()

        ### RIGHT FRAME (Contains solutions display grid and execution buttons)

        self.right_frame = tkinter.Frame(self.parent) # Right frame placed inside the root widget
        self.solved_grids_display = tkinter.Text(self.right_frame, height=20, width=40, font=self.buttonfont, state=tkinter.DISABLED, yscrollcommand=self.scrollbar.set) # Text widget displaying all the solved solutions           

        self.right_frame.grid(row=0, column=1) # Positions the frame on the right of the GUI
        self.solved_grids_display.grid(row=0, column=0)
        
        ###### RIGHT FRAME BUTTONS LABEL FRAME (Contains execution buttons)

        self.buttons_label_frame = tkinter.LabelFrame(self.right_frame, text='Configure') # Buttons sub frame inside right frame
        self.start_btn = tkinter.Button(self.buttons_label_frame, text='Start', font=self.buttonfont, command=self.__start) # Start button
        self.loading_bar = ttk.Progressbar(self.buttons_label_frame, orient=tkinter.HORIZONTAL, mode='indeterminate', maximum='20') # Indeterminate loading bar does not fill gradually but rather sweeps across
        self.stop_btn = tkinter.Button(self.buttons_label_frame, text='Stop', font=self.buttonfont, state=tkinter.DISABLED, command=self.__stop) # Stop button     
        self.reset_btn = tkinter.Button(self.buttons_label_frame, text=u'\u21BA', font=self.buttonfont, state=tkinter.DISABLED, command=self.__reset) # Reset button   

        self.buttons_label_frame.grid(row=1, column=0, columnspan=2) # Places label frame inside the right frame
        self.start_btn.grid(row=1, column=0)
        self.loading_bar.grid(row=1, column=1, sticky=tkinter.EW) # sticky parameter makes loading bar stretch from left to right
        self.stop_btn.grid(row=1, column=2) 
        self.reset_btn.grid(row=1, column=3)

        ### WIDGET CONFIGURATION

        self.scrollbar.config(command=self.solved_grids_display.yview) # Configures the scrolling of the text widget

        ### BINDING MOUSE AND KEYBOARD EVENTS

        self.__draw_grid() # Draws the empty grid

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
        # print(f'Clicked at {x},{y}') DEBUGGING PURPOSES

        if (self.margin < x < self.width - self.margin) and (self.margin < y < self.height - self.margin): # Checks that the click is inside the grid
            row, col = (y-self.margin)//self.side, (x-self.margin)//self.side # Calculates what row and column the cursor is in
            # print(f'Clicked at row {row}, column {col}') DEBUGGING PURPOSES

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
            self.__display_number(self.row, self.col, event.char, color='red')
            self.reset_btn.config(state=tkinter.NORMAL) # Enables the reset button

    ### START/STOP METHODS

    def __solver_thread(self):
        'Main solver thread'

        self.allowed = True # Allows the solver thread to run
        self.start_btn.config(state=tkinter.DISABLED) # Disabled start button until execution is finished
        self.stop_btn.config(state=tkinter.NORMAL) # Enables the stop button until execution is finished
        self.status_bar.config(text='Executing solve.') # Updates status bar

        self.loading_bar.start() # Starts the loading bar animation

        exit_value = self.__solve_grid() # Solves the grid and returns True (was interrupted) or False (was not interrupted) as the exit code

        self.stop_btn.config(state=tkinter.DISABLED) # Disables stop button at the end of execution
        self.reset_btn.config(state=tkinter.NORMAL) # Enables the reset button

        self.loading_bar.stop() # Stops the loading bar animation

        print(f'Exit value: {exit_value}') # DEBUGGING PURPOSES

        if not exit_value: # Displays all solutions only if it was not interrupted
            self.__display_solutions() 
            self.status_bar.config(text='Execution successful.') # Updates status bar
        else: # If program was interrupted
            self.status_bar.config(text='Execution interrupted.') # Updates status bar

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

        # Stores each user-entered number in self.grid
        for ypos, row in enumerate(self.grid): # Goes through each row in the grid
            for xpos, _ in enumerate(row): # Goes through each position in the row
                    grid_object = self.canvas.find_withtag((ypos,xpos),) # Gets the grid number object with tag at respective position (row, column)
                    value = self.canvas.itemcget(grid_object, 'text') # Gets the value of the specific grid number; 'text' argument specifies we want to extract the text
                    # Note that value could be None

                    if value: # If the cell is filled in
                        self.grid[ypos][xpos] = int(value)
                    else: # If the cell is empty
                        self.grid[ypos][xpos] = 0

        self.grid = [ # A temporary grid used for debugging purposes
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

        self.__update_grid(self.grid) # Displays the grid
        threading.Thread(target=self.__solver_thread).start() # Initiates the solver thread                

    def __stop(self):
        'Interrupts the dynamic solving of the grid'

        self.allowed = False # Disallowes the solver thread from running

        # Missing additional logic

    def __reset(self):
        'Resets the graphical user interface'

        self.start_btn.config(state=tkinter.NORMAL) # Renables the start button
        self.reset_btn.config(state=tkinter.DISABLED) # Disables the reset ability

        self.solutions = [] # Resets all the found solutions

        self.solved_grids_display.config(state=tkinter.NORMAL) # Temporarily enables widget
        self.solved_grids_display.delete(1.0, 'end') # Clears the entire solved solutions text widget
        self.solved_grids_display.config(state=tkinter.DISABLED) # Disables widget again

        self.__update_grid(self.empty_grid) # Displays the empty grid

        self.status_bar.config(text='Reset complete.') # Updates the status bar

    ### LOGIC HANDLING METHODS

    def __solve_grid(self):
        'Solves the grid in self.grid and stores each solution as a list in solutions list. Displays each iteration of the solving algorithm'
        
        for ypos, row in enumerate(self.grid): # Goes through each row in the grid
            for xpos, position in enumerate(row): # Goes through each position in the row
                if position == 0: # Position must be empty
                    for num in range(1,10): # Tries all numbers from 1 to 9
                        # time.sleep(0.1) ######################################################################################################################
                        if not self.allowed: # Not allowed to run
                            return True # Returns True; it was interrupted
                        if self.__possible(xpos, ypos, num): # Check if the number is a possible
                            self.grid[ypos][xpos] = num # Puts possible number in empty space
                            self.__display_number(ypos, xpos, num)

                            self.__solve_grid() # Keeps solving

                            self.grid[ypos][xpos] = 0 # If program reaches here, no further numbers can be put into the grid and the square is reset
                            self.__display_number(ypos, xpos, None) # Empties the sudoku square
                    
                    return False # No possible solution has been found for an empty position; Exits function by returning None as it was not interrupted

        # If program reaches this point, there are no more empty spaces in the grid and a solution has been found
        deepcopy_grid = copy.deepcopy(self.grid) # A copy of the original grid is made
        self.solutions.append(deepcopy_grid) # Solution added to list of solutions

        self.__update_solved_grids() # Updates the solved solutions text widget
    
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

    def __update_grid(self, grid):
        'Loads a particular grid'

        for ypos, row in enumerate(grid): # Goes through each row in the grid
            for xpos, position in enumerate(row): # Goes through each position in the row
                if position: # If the number does not equal to 0
                    self.__display_number(ypos, xpos, position, color='red') # Displays the number
                else: # If the number is 0, square is supposed to be empty
                    self.__display_number(ypos, xpos, None) # Empties square
                    
    def __update_solved_grids(self):
        'Updates solved grids text widget by displaying all the found solutions from self.solutions'

        self.solved_grids_display.config(state=tkinter.NORMAL) # Temporarily activates the text widget

        self.solved_grids_display.delete(1.0, 'end') # Clears entire widget

        self.solved_grids_display.insert('end', f'---------{len(self.solutions)} Solutions Found---------\n') # Adds header

        for grid in self.solutions: # For each solution
            for row in grid: # For each row in the solution grid
                # print(row) DEBUGGING PURPOSES
                self.solved_grids_display.insert('end', f'\n{row}') # Appends the row to the text widget
            self.solved_grids_display.insert('end', '\n') # Adds a separator between the solutions

        self.solved_grids_display.config(state=tkinter.DISABLED) # Deactivates the text widget

    def __display_number(self, row, column, n, color='black'): 
        '''Displays a given number on the grid
        
        Takes in the row number, column number, value of the number to display, and optional font color'''

        x = round(self.margin + self.side*column + self.side/2) # Finds x and y coords of the centre of the selected square
        y = round(self.margin + self.side*row + self.side/2) # Coordinates are rounded to nearest integer
        
        tag = (row,column) # Create a tag from 00 to 88 representing the row and column the selected square is in
        # print(f'Tag: {tag}') DEBUGGING PURPOSES
        
        self.canvas.delete(tag) # Deletes previous 
        self.canvas.create_text(x, y, text=n, tags=(tag,), fill=color, font=self.gridfont) # Places a number on the screen with tagged position
        # tags argument should be a tuple or string

    def __display_solutions(self):
        'Formats and displays all found solutions on the terminal'

        print(f'\n-----------------------{len(self.solutions)} Solutions Found-----------------------')
        
        for grid in self.solutions: # Prints out each solution
            print('')
            for row in grid:
                print(row)

    ### MENUBAR SETTINGS METHODS

    def __about(self):
        'Opens the README for the program'

        os.system('README.md') # Opens README.md with an adequate program like notepad

    def __licence(self):
        'Opens the LICENCE for the program'

        os.system('LICENCE.md') # Opens README.md with an adequate program like notepad

root = tkinter.Tk() # Defines the main window
root.title('Sudoku Solver') # Sets the title of the window
root.iconbitmap('sudoku_icon.ico') # Sets the icon for the window
root.resizable('False', 'False') # Disables resizing

GraphicalInterface(root) # GUI instance is created

root.mainloop()