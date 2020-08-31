'''Sudoku Solver Main Module'''

import tkinter
from tkinter import ttk # Used for scrollbar
from tkinter import messagebox # Used for message boxes 
from tkinter import filedialog # Used for opening the file dialog box

import copy # Used for creating copies of variables instead of instances

import threading # Multithreading module
import time # Time module for delays

import os # Module for opening system files
import json # Module for opening json files

class GraphicalInterface:
    'Creates the entire GUI'

    def __init__(self, parent): # Parent is the main window
        self.parent = parent # Parent root frame

        self.solutions = [] # Stores all solved grids
        self.empty_grid = [ # Empty grid used for resetting
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

        self.running = False # Sets the flag indicating whether the solver thread is running; needed for solver thread 
        self.modify = True # Sets the flag indicating whether the grid is allowed to be modified

        self.autosave = tkinter.IntVar() # Sets value indicating whether to save grid automatically (1 or 0)
        self.delay = tkinter.IntVar() # Sets value indicating whether to delay grid animation (1 or 0)

        self.margin = 20 # Margin size of the sudoku board
        self.side = 40 # Side length of each square in the grid
        self.width = self.height = (self.margin*2) + (self.side*9) # Defines the width and height of the canvas

        self.buttonfont = ('Helvetica', 8) # Font type of buttons
        self.statusfont = ('Helvetica', 7) # Font type for the status bar
        self.gridfont = ('Helvetica', 10, 'bold') # Font type of sudoku grid
        
        self.row = None  # Currently selected cell row and column
        self.col = None

        self.__widgets() # Initiates other widgets
        self.__load_settings() # Loads old settings

    ### PACKING WIDGETS

    def __widgets(self):
        'Initiates the widgets'

        ### MENUBAR 

        self.menubar = tkinter.Menu(root) # Creates the menubar object 
        root.config(menu=self.menubar) # Sets menubar object in root

        self.file_submenu = tkinter.Menu(self.menubar, tearoff=0) # Creates file submenu
        self.menubar.add_cascade(label='File', menu=self.file_submenu) # Places submenu inside menubar
        self.file_submenu.add_command(label='Load...', command=self.__load) # Adds load button
        self.file_submenu.add_separator() # Adds a line separator
        self.file_submenu.add_command(label='Save As...', state=tkinter.DISABLED, command=self.__save) # Adds save button which is disabled at the start
        self.file_submenu.add_checkbutton(label='Auto Save', variable=self.autosave, command=self.__save_settings) # Adds a checkbutton for autosave functionality binded to self.autosave
        self.file_submenu.add_separator() # Adds a line separator
        self.file_submenu.add_command(label='Exit', command=exit) # Adds exit button

        self.option_submenu = tkinter.Menu(self.menubar, tearoff=0) # Creates options submenu 
        self.menubar.add_cascade(label='Options', menu=self.option_submenu) # Places the submenu inside the menubar
        self.option_submenu.add_checkbutton(label='Delay Animations', variable=self.delay, command=self.__save_settings) # Adds a checkbutton for delaying animations functionality binded to self.delay

        self.help_submenu = tkinter.Menu(self.menubar, tearoff=0) # Creates help submenu 
        self.menubar.add_cascade(label='Help', menu=self.help_submenu) # Places the submenu inside the menubar
        self.help_submenu.add_command(label='About Sudoku Solver', command=self.__about) # About button that opens README.md
        self.help_submenu.add_separator() # Adds a line separator
        self.help_submenu.add_command(label='Licence', command=self.__licence) # Licence button that opens LICENCE.md

        ### SCROLLBAR & STATUS BAR

        self.scrollbar = tkinter.Scrollbar(root) # Scrollbar for the text widget
        self.scrollbar.grid(row=0, column=2, sticky=tkinter.NS) # sticky parameter makes scrollbar stretch from top to bottom; added on right side of GUI

        self.status_bar = tkinter.Label(root, text='Awaiting commands.', font=self.statusfont, bg='lightgrey', anchor=tkinter.E) # Status bar for displaying various status updates
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky=tkinter.EW) # sticky parameter makes the label stretch from left to right; added at the bottom of the GUI
        
        ### LEFT FRAME (Contains Sudoku Grid)

        self.left_frame = tkinter.Frame(self.parent) # Left frame placed inside the root widget
        self.canvas = tkinter.Canvas(self.left_frame, width=self.width, height=self.height) # Sudoku grid canvas

        self.left_frame.grid(row=0, column=0) # Positions the frame on the left of the GUI
        self.canvas.grid()

        ### RIGHT FRAME (Contains solutions display grid and execution buttons)

        self.right_frame = tkinter.Frame(self.parent) # Right frame placed inside the root widget
        self.solved_grids_display = tkinter.Text(self.right_frame, height=20, width=30, state=tkinter.DISABLED, yscrollcommand=self.scrollbar.set) # Text widget displaying all the solved solutions           

        self.right_frame.grid(row=0, column=1, padx=(0,20)) # Positions the frame on the right of the GUI
        self.solved_grids_display.grid(row=0, column=0)
        
        ###### RIGHT FRAME BUTTONS LABEL FRAME (Contains execution buttons)

        self.buttons_label_frame = tkinter.LabelFrame(self.right_frame, text='Configure') # Buttons sub frame inside right frame
        self.start_btn = tkinter.Button(self.buttons_label_frame, text='Start', font=self.buttonfont, command=self.__start) # Start button
        self.loading_bar = ttk.Progressbar(self.buttons_label_frame, orient=tkinter.HORIZONTAL, mode='indeterminate', maximum='20') # Indeterminate loading bar does not fill gradually but rather sweeps across
        self.stop_btn = tkinter.Button(self.buttons_label_frame, text='Stop', font=self.buttonfont, state=tkinter.DISABLED, command=self.__stop) # Stop button     
        self.reset_btn = tkinter.Button(self.buttons_label_frame, text='Reset', font=self.buttonfont, state=tkinter.DISABLED, command=self.__reset) # Reset button   

        self.buttons_label_frame.grid(row=1, column=0, columnspan=2) # Places label frame inside the right frame
        self.start_btn.grid(row=1, column=0)
        self.loading_bar.grid(row=1, column=1, sticky=tkinter.EW) # sticky parameter makes loading bar stretch from left to right
        self.stop_btn.grid(row=1, column=2) 
        self.reset_btn.grid(row=1, column=3)

        ### WIDGET CONFIGURATION

        self.scrollbar.config(command=self.solved_grids_display.yview) # Configures the scrolling of the text widget

        self.solved_grids_display.tag_configure('header', font=('Helvetica', 10, 'bold'), justify=tkinter.CENTER) # Configures the header font properties of the text widget
        self.solved_grids_display.tag_configure('subheader', font=('Helvetica', 7, 'bold italic'), justify=tkinter.CENTER) # Configures the subheader font properties of the text widget
        self.solved_grids_display.tag_configure('solutions', font=('Helvetica', 10, 'bold'), justify=tkinter.CENTER) # Configures the solution grids font properties of the text widget

        ### BINDING MOUSE AND KEYBOARD EVENTS

        self.__draw_grid() # Draws the empty grid

        self.canvas.bind('<Button-1>', self.__cell_clicked) # Binds left click to selecting a cell
        self.parent.bind('<Key>', self.__key_pressed) # Binds key pressed to entering a key; must be binded to root

    def __draw_grid(self):
        'Draws the Sudoku grid'

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

        Takes event as argument. Creates indicator only if self.modify is True'''

        x, y = event.x, event.y # Finds the x and y coordinate of the click
        print(f'Clicked at {x},{y}') # DEBUGGING PURPOSES

        if self.modify: # Box selection functionality only available if modify variable is True
            if (self.margin < x < self.width - self.margin) and (self.margin < y < self.height - self.margin): # Checks that the click is inside the grid
                row, col = (y-self.margin)//self.side, (x-self.margin)//self.side # Calculates what row and column the cursor is in
                print(f'Clicked at row {row}, column {col}') # DEBUGGING PURPOSES

                if (row, col) == (self.row, self.col): # If cell is already selected, deselect it
                    self.row, self.col = None, None

                else: # If it is not selected, select it
                    self.row, self.col = row, col

                self.__draw_border() # Handles the box selection

            else: # If the user clicks outside the canvas
                self.row, self.col = None, None # Resets the currently selected cell row and column
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
        '''Handles keyboard key presse
        
        Takes event as argument'''

        if (self.row, self.col) != (None, None): # Checks that a square is selected
            if event.char.isnumeric(): # If entered key is a digit
                self.__display_number(self.row, self.col, event.char, color='red') # Displays digit in canvas
                self.reset_btn.config(state=tkinter.NORMAL) # Enables the reset button
            elif event.keysym == 'BackSpace': # If backspace is pressed
                self.__display_number(self.row, self.col, None) # Resets the square

    ### START/STOP/RESET METHODS

    def __start(self):
        'Begins the dynamic solving of the grid'

        self.row, self.col = None, None # Resets the currently selected cell row and colunm
        self.canvas.delete('cursor') # Deletes the previous cursor

        self.grid = [ # Makes a new empty 8x8 grid which will store the user-entered values
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

        if not self.__validate_selected_grid(): # If the grid is not valid in format
            return None # Returns early
        else: # Grid is valid in format; GRID MAY NOT HAVE ANY SOLUTIONS
            self.__update_grid(self.grid) # Displays the grid
            threading.Thread(target=self.__solver_thread).start() # Initiates the solver thread   

    def __solver_thread(self):
        'Main solver thread that solves self.grid'

        self.running = True # Allows the solver thread to run
        self.modify = False # Grid modification feature must be disabled when grid is solving

        self.file_submenu.entryconfig(0, state=tkinter.DISABLED) # Disables the load functionality when program is running
        self.file_submenu.entryconfig(2, state=tkinter.DISABLED) # Disables the save as functionality when program is running
        self.start_btn.config(state=tkinter.DISABLED) # Disabled start button until execution is finished
        self.stop_btn.config(state=tkinter.NORMAL) # Enables the stop button until execution is finished
        self.reset_btn.config(state=tkinter.DISABLED) # Disables the reset button until execution is finished
        self.status_bar.config(text='Executing solve.', fg='black') # Updates status bar

        self.loading_bar.start() # Starts the loading bar animation

        self.interrupted = self.__solve_grid() # Solves the grid and returns True (was interrupted) or False (was not interrupted); used for displaying or auto saving

        self.running = False # Program is not running anymore

        if self.solutions: # If at least 1 solution has been found
            self.file_submenu.entryconfig(2, state=tkinter.NORMAL) # Re-enables the save as functionality 
        else: # If no solutions have been found
            self.__update_solved_grids() # Updates the solved solutions text widget
        self.stop_btn.config(state=tkinter.DISABLED) # Disables stop button at the end of execution
        self.reset_btn.config(state=tkinter.NORMAL) # Enables the reset button

        self.loading_bar.stop() # Stops the loading bar animation

        print(f'Exit value: {self.interrupted}') # DEBUGGING PURPOSES

        if not self.interrupted: # Displays all solutions only if it was not interrupted
            self.__display_solutions() # Prints out solutions
            self.status_bar.config(text='Execution successful. Please reset grid.', fg='black') # Updates status bar

            if self.autosave.get() and self.solutions: # If autosave is on and at least 1 solution has been found
                self.__save() # Save the results
        else: # If program was interrupted
            self.status_bar.config(text='Execution interrupted. Please reset grid.', fg='black') # Updates status bar             

    def __stop(self):
        'Interrupts the dynamic solving of the grid'

        self.running = False # Disallowes the solver thread from running

    def __reset(self):
        'Resets the graphical user interface to its initial state'

        self.file_submenu.entryconfig(0, state=tkinter.NORMAL) # Enables the load functionality when program is reset
        self.file_submenu.entryconfig(2, state=tkinter.DISABLED) # Disables the save as functionality when program is reset
        self.start_btn.config(state=tkinter.NORMAL) # Re-enables the start button
        self.reset_btn.config(state=tkinter.DISABLED) # Disables the reset ability

        self.solutions = [] # Resets all the found solutions
        self.loaded_grid = None # Forgets the loaded grid
        self.modify = True # Re-enables the modify flag to enable grid modification

        self.row, self.col = None, None # Resets the currently selected cell row and column
        self.canvas.delete('cursor') # Deletes the previous cursor

        self.solved_grids_display.config(state=tkinter.NORMAL) # Temporarily enables widget
        self.solved_grids_display.delete(1.0, 'end') # Clears the entire solved solutions text widget
        self.solved_grids_display.config(state=tkinter.DISABLED) # Disables widget again

        self.__update_grid(self.empty_grid) # Displays the empty grid

        self.status_bar.config(text='Reset complete.', fg='black') # Updates the status bar

    ### LOGIC HANDLING METHODS

    def __solve_grid(self):
        '''Solves the grid in self.grid and stores each solution as a list in self.solutions; displays each iteration of the solving algorithm
        
        Returns True if process was interrupted or False if process was not interrupted'''
        
        for ypos, row in enumerate(self.grid): # Goes through each row in the grid
            for xpos, position in enumerate(row): # Goes through each position in the row
                if position == 0: # Position must be empty
                    for num in range(1,10): # Tries all numbers from 1 to 9
                        if self.delay.get(): # If animation is set to be delayed
                            time.sleep(0.1) 
                        if not self.running: # If it was interrupted
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
        '''Returns True or False if a number can fit in a specific position in self.grid

        Takes x position, y position, and value of a possible number as arguments'''

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

    ### VALIDATION METHODS

    def __validate_selected_grid(self):
        'Validates self.grid by making sure the value placement is correct and that at least 17 values have been entered; returns True or False if grid is valid'

        count = 0 # Stores the valid grid clue count
        for ypos, row in enumerate(self.grid): # Goes through each row in the grid
            for xpos, position in enumerate(row): # Goes through each position in the row
                if position: # If the number is not 0
                    self.grid[ypos][xpos] = 0 # Sets the number to 0 temporarily so that self.__possible works
                    if not self.__possible(xpos, ypos, position): # If number cannot be placed in that position
                        # Note that number is not reset in the grid if it is invalid. Grid must be reset
                        self.status_bar.config(text=f'Conflict in clue positioning (Row:{ypos+1},Column:{xpos+1}). Invalid grid.', fg='darkred') # Updates status bar with dark red color
                        return False # Grid is invalid
                    self.grid[ypos][xpos] = position # Resets number in the grid after using __possible method
                    count += 1 # Number is valid
        
        if count < 17: # If there are less than 17 clues
            self.status_bar.config(text=f'Please enter at least 17 clues. ({17-count} remaining)', fg='darkred') # Updates status bar with dark red color
            return False # Grid is invalid
        
        return True # Grid is valid

    def __validate_loaded_grid(self, grid): # Used for validating an imported grid
        '''Validates the format of a LOADED grid by making sure only integer values between 0 to 9 are entered and that grid is of list type; returns True or False if grid format is valid
        
        Takes grid as argument'''

        if not isinstance(grid, list): # Checks that the grid is of type grid
            return False # Grid is not valid
        for row in grid: # For each row in the grid
            if len(row) != 9: # If exactly 9 items are not present in each row
                return False # Grid is not valid
            for position in row: # For each number in the grid
                if position not in range(0, 10): # Number must be in range [0,10)
                    return False # Grid is invalid
        
        return True # Grid is valid

    ### DISPLAYER METHODS

    def __update_grid(self, grid):
        '''Displays a grid in the Sudoku canvas
        
        Takes grid as argument'''

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

        self.solved_grids_display.insert('end', f'{len(self.solutions)} Solution(s) Found\n', 'header') # Adds header with header tag

        if len(self.solutions) == 1: # If only 1 solution has been found
            self.solved_grids_display.insert('end', f'(True Sudoku Grid)\n', 'subheader') # True Sudoku grid by definition
        else: # If more than 1 solutions are found
            self.solved_grids_display.insert('end', f'(False Sudoku Grid)\n', 'subheader') # False Sudoku grid by definition

        for grid in self.solutions: # For each solution
            self.solved_grids_display.insert('end', '\n') # Adds a separator between the solutions
            for row in grid: # For each row in the solution grid
                # print(row) DEBUGGING PURPOSES
                self.solved_grids_display.insert('end', f'{row}\n', 'solutions') # Appends the row to the text widget with solutions tag
            self.solved_grids_display.see('end') # Automatically scrolls to the end of the widget

        self.solved_grids_display.config(state=tkinter.DISABLED) # Deactivates the text widget

    def __display_number(self, row, column, n, color='black'): 
        '''Displays a given digit on the Sudoku canvas
        
        Takes the row number, column number, value of the number to display, and optional font color as arguments'''

        x = round(self.margin + self.side*column + self.side/2) # Finds x and y coords of the centre of the selected square
        y = round(self.margin + self.side*row + self.side/2) # Coordinates are rounded to nearest integer
        
        tag = (row,column) # Create a tag from 00 to 88 representing the row and column the selected square is in
        # print(f'Tag: {tag}') DEBUGGING PURPOSES
        
        self.canvas.delete(tag) # Deletes previous 
        self.canvas.create_text(x, y, text=n, tags=(tag,), fill=color, font=self.gridfont) # Places a number on the screen with tagged position
        # tags argument should be a tuple or string

    def __display_solutions(self):
        'Formats and displays all found solutions in the terminal'

        print(self.__solutions_formatter()) # Prints out the solutions

    def __solutions_formatter(self):
        '''Manipulates the solutions in self.solutions into a printable format
        
        Returns formatted string'''

        formatted = f'-----------------------{len(self.solutions)} Solutions Found-----------------------\n' # String storing formatted solutions

        if len(self.solutions) == 1: # If only 1 solution has been found
            formatted += f'(True Sudoku Grid)' # True Sudoku grid by definition
        else: # If more than 1 solutions are found
            formatted += f'(False Sudoku Grid)' # True Sudoku grid by definition
        
        for grid in self.solutions: # For each solution
            formatted += '\n' # Adds empty line between each solution
            for row in grid: # For each row in the grid
                formatted += f'\n{row}' 

        return formatted # Returns formatted solutions as a string

    ### MENUBAR SETTINGS METHODS

    def __load(self):
        'Loads a grid from a chosen json file'

        print('Loading file')

        try:
            filename = filedialog.askopenfilename(title='Select Load File', filetypes=(('Text Files', '*.json'),)) # Prompts user to select a load file (.json)
            if filename: # If a file has been chosen
                with open(filename, 'r') as f: # Opens the chosen file as read
                    loaded_grid = json.load(f) # Deserialize json file contents

                    if self.__validate_loaded_grid(loaded_grid): # If the grid is of valid format
                        self.row, self.col = None, None # Resets the currently selected cell row and column
                        self.canvas.delete('cursor') # Deletes the previous cursor

                        self.__update_grid(loaded_grid) # Displays the grid
                    else: # If grid is invalid
                        raise Exception('Incorrect grid format') # Raises exception
            else: # If program reaches this point, user has not chosen a file and has aborted load
                print('Load aborted')
                return None
        except Exception as e:
            messagebox.showerror(title='Fatal Error', message=f'An unexpected error has occurred: {e}') # Shows error
            self.status_bar.config(text=f'An error occurred. Load aborted.', fg='darkred') # Updates status bar
        else:
            messagebox.showinfo(title='File loaded successfully', message=f"Grid has been successfully loaded from '{filename}'") # Shows successful load info
            self.status_bar.config(text=f'Load successful.', fg='black') # Updates status bar

    def __save(self):
        'Saves all found solutions in chosen text file'

        print('Saving file')

        try:
            filename = filedialog.askopenfilename(title='Select Save File', filetypes=(('Text Files', '*.txt'),)) # Prompts user to select a save file (.txt)
            if filename: # If a file has been chosen
                with open(filename, 'w') as f: # Opens the chosen file
                    f.write(self.__solutions_formatter()) # Writes solutions into file
            else: # If program reaches this point, user has not chosen a file and has aborted save
                print('Save aborted')
                return None
        except Exception as e:
            messagebox.showerror(title='Fatal Error', message=f'An unexpected error has occurred: {e}') # Shows error
            self.status_bar.config(text=f'An error occurred. Save aborted.', fg='darkred') # Updates status bar
        else:
            messagebox.showinfo(title='File saved successfully', message=f"Solutions have been successfully saved in '{filename}'") # Shows successful save info
            self.status_bar.config(text=f'Save successful.', fg='black') # Updates status bar
    
    def __save_settings(self):
        'Updates settings in settings.json'

        print('Settings updated')

        try:
            with open('settings.json', 'w') as f: # Opens the chosen file as read
                self.settings = {'Autosave':self.autosave.get(), 'AnimationDelay':self.delay.get()} # Stores all the loadable settings as a dictionary
                json.dump(self.settings, f) # Dumps the settings into json file
        except Exception as e:
            messagebox.showerror(title='Fatal Error', message=f'An unexpected error has occurred: {e}') # Shows error
            exit() # Exits program if an error occurs when saving

    def __load_settings(self):
        'Loads the settings from settings.json'

        print('Settings loaded')

        try:
            with open('settings.json', 'r') as f: # Opens the chosen file as read
                self.settings = json.load(f) # Loads all the settings 
                self.autosave.set(self.settings['Autosave'])
                self.delay.set(self.settings['AnimationDelay'])
        except Exception as e:
            messagebox.showerror(title='Fatal Error', message=f'An unexpected error has occurred: {e}') # Shows error
            exit() # Exits program if settings are not found

    def __about(self):
        'Opens README.md'

        print('Opened README.md')

        if os.path.isfile('README.md'): # If file has not been deleted
            os.system('README.md') # Opens README.md with an adequate program like notepad
        else: # If file has been deleted or cannot be found
            messagebox.showerror(title='Fatal Error', message=f"File 'README.MD' not found.") # Shows error

    def __licence(self):
        'Opens the LICENCE.md'

        print('Opened LICENCE.md')

        if os.path.isfile('LICENCE.md'): # If file has not been deleted
            os.system('LICENCE.md') # Opens README.md with an adequate program like notepad
        else: # If file has been deleted or cannot be found
            messagebox.showerror(title='Fatal Error', message=f"File 'LICENCE.MD' not found.") # Shows error

root = tkinter.Tk() # Defines the main window
root.title('Sudoku Solver') # Sets the title of the window
root.iconbitmap('sudoku_icon.ico') # Sets the icon for the window
root.resizable('False', 'False') # Disables resizing

GraphicalInterface(root) # GUI instance is created

root.mainloop()
