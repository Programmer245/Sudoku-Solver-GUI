-------------------
Changelog:
-------------------

28/05/2020 - v0.1 ALPHA:
+ Set up development environment
+ Created .gitignore
+ Created Changelog.txt
+ Created README.txt
+ Created sudoku_logic.py and sudoku_main.py
+ Added basic logic in sudoku_logic.py with yield statement
+ Imported basic modules in main.py

- sudoku_logic.py solve function does not yield correctly due to function returning early (solve may need to be put into same module)
/UNSTABLE BUILD/

02/06/2020 - v0.1.1 ALPHA:
+ Incorporated logic into main.py to fix cross-module problems
+ Deleted sudoku_logic.py
+ Renamed sudoku_main.py to main.py
+ Class-oriented approach over module-orented approach preferred 

/UNSTABLE BUILD/

02/06/2020 - v0.1.2 ALPHA:
+ Added SudokuGrid Class
+ Added private methods
+ Added logic to SudokuGrid class
+ Added global variables to SudokuGrid class

- Additional documentation needed
- solutions list and grid must be attributes of SudokuGrid class
/UNSTABLE BUILD/

03/06/2020 - v0.1.3 ALPHA:
+ Added documentation
+ Added solutions list and grid to SudokuGrid class
+ Added button to test functionality of solving function

- Needs to display all iterations on the grid
/UNSTABLE BUILD/

03/06/2020 - v0.1.4 ALPHA:
+ Added __display_numbers method to Grid class to represent the numbers in self.grid into the grid

- Need to finish coding __display_numbers method
- Key presses should not be recorded if a square is not highlighted
- Needs to display all iterations on the grid
/UNSTABLE BUILD/

04/06/2020 - v0.2 ALPHA:
+ Renamed __testing method to __start method
+ Added some documentation
+ Tags for numbers in grid now in form of (row, column)
+ tags argument in self.canvas must be in form of (tag,) to prevent issues
+ When __solve method called, user-entered numbers are inserted into self.grid

- Need to finish coding __display_numbers method
- Key presses should not be recorded if a square is not highlighted
- Needs to display all iterations on the grid
/UNSTABLE BUILD/

28/07/2020 - v0.2.1 ALPHA:
+ Renamed SudokuGrid class to GraphicalInterface
+ Retweaked code
+ Added some documentation
+ Key presses not recorded if square is not highlighted

- Need to finish coding __display_numbers method (must take in tag and number)
- Need to finish coding __stop method
- Needs to display all iterations on the grid
- Needs multithreading
- Needs to integrate __display_numbers method in __key_pressed method
/UNSTABLE BUILD/

29/07/2020 - v0.2.2 ALPHA:
+ Retweaked some code
+ Integrated __display_numbers method in __key_pressed method
+ Added __update_grid method to load in an old grid

- Need to finish coding __stop method
- Needs to display all iterations on the grid
- Needs multithreading/root.update method (multithreading may be harder to implement)
- Grid goes back to initial state if it cannot find any other solutions (what we want)
/UNSTABLE BUILD/

01/08/2020 - Testing Session:
+ Using threads vs using root.update method tested
+ Threads were chosen to be the most effective method to prevent GUI from freezing
+ A single thread can be used for the __solve_grid method and another checker thread can be used to check if the thread is alive or not

01/08/2020 - v0.3 ALPHA:
+ Implemented multithreading
+ All iterations displayed on grid
+ Added self.allowed flag to control if solver method can returning
+ __solve_grid method returns an exit code; either True or False depending if it was interrupted or not
+ Added stop button functionality

- Need to update documentation and ensure everything works as expected
- Add title to application
- Solver thread does not end immediately upon pressing stop button
/UNSTABLE BUILD/

03/08/2020 - v0.3.1 ALPHA:
+ Added title to application
+ Added documentation

- Solver thread does not end immediately upon pressing stop button (not an issue)
- Need to add listbox, buttons, loading bar
- Test grids needed
/UNSTABLE BUILD/

06/08/2020 - v0.4 ALPHA:
+ Added reset button, solved grid text widget, and scrollbar
+ Added indeterminate loading bar
+ ttk module imported
+ Added __reset and __update_loading_bar methods

- Need menu widget
- Logic in __reset method needed
- Logic in __update_loading_bar method needed (use start method)
- Update fonts
- Add pictures for buttons
- Resize loading bar
/UNSTABLE BUILD/

11/08/2020 - v0.4.1 ALPHA:
+ Resized loading bar
+ Removed __update_loading_bar method and replaced with tkinter start and stop methods
+ Added label frame to store buttons

- Need menubar widget
- Logic in __reset method needed
- Update fonts
- Add pictures for buttons
/UNSTABLE BUILD/

11/08/2020 - v0.5 ALPHA:
+ Added menubar
+ Added 'Options' and 'Help' sections to menubar
+ Separated scollbar from right frame
+ Added status bar at bottom of GUI

- Bind menubar buttons to respective methods
- Need status bar methods
- Missing documentation
- Logic in __reset method needed
- Update fonts
- Add pictures for buttons
/UNSTABLE BUILD/

12/08/2020 - v0.5.1 ALPHA:
+ Added LICENCE.md

- Need status bar methods
- Missing documentation
- Logic in __reset method needed
- Update fonts
- Add pictures for buttons
/UNSTABLE BUILD/

12/08/2020 - v0.5.2 ALPHA:
+ Added README.md

- Missing documentation
- Logic in __reset method needed
- Update fonts
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

12/08/2020 - v0.5.3 ALPHA:
+ Added functionality for some menubar buttons
+ Added window icon
+ Added status bar font
+ Documentation fixed
+ Some fonts updated

- Logic in __reset method needed
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

12/08/2020 - v0.6 ALPHA:
+ Added __update_solved_grids method for updating the solved grids text widget

- Need to convert .py file into .pyw
- Need to disable start button until execution is finished
- Logic in __reset method needed
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

13/08/2020 - v0.6.1 ALPHA:
+ Converted .py file to .pyw
+ Button enabling/disabling added
+ __update_grid method now takes in the grid to display
+ When grid is displayed, 0s are not shown

- Try/except needed to see if files to open exist
- When stopped, 0s are displayed
- When stopped, program converts every square to 0
- Reset button must clear entire grid
- Reset button must be enabled whenever a grid is imported or a number is inserted in the grid
- Logic in __reset method needed
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

17/08/2020 - v0.6.2 ALPHA:
+ Added color functionality to __display_number method
+ Fixed 0s being displayed
+ Reset button clears the grid
+ Some status bar events added
+ Reset button enables when user types a number inside the grid
+ Text in found solutions widget formatted

- Text in found solutions widget must be centred
- When stopped, the program retraces its steps and tries to delete all the clues it has inserted
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

17/08/2020 - v0.6.3 ALPHA:
+ Added better formatting in text widget; tags added
+ Resized text widget
+ Disabled ability to click on a square if program is running

- When program starts/ends/resets, any selected square must be deselected
- Add movement detection in status label?
- Must check at least 17 clues have been inserted
- Format text widget better
- When stopped, the program retraces its steps and tries to delete all the clues it has inserted
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

18/08/2020 - v0.6.4 ALPHA:
+ When program starts/ends/resets, any selected square is now deselected
+ Formatted text in text widget

- Needs to implement 17 clues minimum functionality using self.count attribute
- Add movement detection in status label?
- When stopped, the program retraces its steps and tries to delete all the clues it has inserted
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

18/08/2020 - v0.6.5 ALPHA:
+ Changed self.allowed to self.running
+ Changed self.exit_code to self.interrupted
+ Refactored code
+ Program has to retrace its steps and delete all clues to return True
+ Added self.interrupted to __init__ method

- Dark theme needed
- Loading functionality needed
- Needs to implement 17 clues minimum functionality using self.count attribute
- Add movement detection in status label?
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

18/08/2020 - v0.6.6 ALPHA:
+ Added __load method for loading files
+ Added __configure method for settings
+ Added 'File' section in menubar

- Dark theme needed
- Loading functionality needed (only 1 grid per document)
- Needs to implement 17 clues minimum functionality using self.count attribute
- Add movement detection in status label?
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

18/08/2020 - v0.6.7 ALPHA:
+ Updated menubar
+ __save method added
+ tkinter filedialog module imported for opening files
+ Only able to modify grid before execution or after reset

- Refactoring needed
- Is running, modified, interrupted necessary?
- Dark theme needed
- Loading functionality needed (only 1 grid per document)
- Needs to implement 17 clues minimum functionality using self.count attribute
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

19/08/2020 - v0.7 ALPHA:
+ Added __solutions_formatter method for formatting solutions; used for __display_solutions method and __save method
+ Refactored code
+ Saving functionality fully implemented
+ Formatted text in text widget once again

- Loading functionality needed (only 1 grid per document)
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Needs to implement 17 clues minimum functionality using self.count attribute
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

20/08/2020 - v0.8 ALPHA:
+ Added sample_grid.txt
+ Imported json library for json file manipulation
+ Load functionality partially implemented

- Loading functionality needed (only 1 grid per document)
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Needs to implement 17 clues minimum functionality using self.count attribute
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

20/08/2020 - v0.8.1 ALPHA:
+ Added __validate_grid method for validating that a loading grid is in the correct format
+ Finished __validate_grid method
+ Updated documentation

- Finish loading functionality
- Need to handle if grid has no solutions in __validate_grid method
- Loading functionality needed (only 1 grid per document)
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Needs to implement 17 clues minimum functionality using self.count attribute
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

25/08/2020 - v0.8.2 ALPHA:
+ Refactored code
+ Optimisations made
+ Deleted self.count variable as it is not needed
+ Added documentation
+ Grid can be modified after being loaded
+ Loading functionality finished

- Must be able to clear a number from a cell using backspace
- Need to handle if grid has no solutions method (grid is not valid if it has no solutions)
- Needs to implement 17 clues minimum functionality in __validate_grid method
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

26/08/2020 - v0.8.3 ALPHA:
+ Number can now be cleared from cell using backspace
+ Renamed __validate_grid to __validate_grid_format as it only validates the input values of the cells and its format
+ Made new placeholder method __validate_grid that validates if the grid is solvable
+ Updated documentation

- Need to handle if grid has no solutions method (grid is not valid if it has no solutions)
- Needs to implement 17 clues minimum functionality in __validate_grid method
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

27/08/2020 - v0.8.4 ALPHA:
+ Renamed __validate_grid_format to __validate_loaded_grid
+ Renamed __validate_grid to __validate_selected_grid
+ Added logic into __validate_selected_grid

- __validate_selected_grid does not validate correctly (when using __possible method, it checks if there is a copy of the possible number already in the grid;
when using it in the solver thread, the number has not already been placed, however, when using it in the validator method, the number has already been placed)
- Cleanup __possible method
- Need to handle if grid has no solutions method (grid is not valid if it has no solutions)
- Needs to implement 17 clues minimum functionality in __validate_grid method
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

27/08/2020 - v0.8.5 ALPHA:
+ Refactored code
+ Cleaned up __possible method
+ __validate_selected_grid method works properly
+ Validation implemented fully

- Remove debugging statements
- Needs to display what the invalid number is
- Need to handle if grid has no solutions method (grid is not valid if it has no solutions)
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Try/except needed to see if files to open exist
- Add pictures for buttons
- Fill README.md
/UNSTABLE BUILD/

30/08/2020 - v0.8.6 ALPHA:
+ Removed some debugging statements
+ Handles if no solutions are found
+ Does not crash if load or save functionality is aborted
+ Autosave aborted if no solutions are found
+ Updated status label functinality; colors added to display error messages

- Must validate grid has only 1 solution
- Needs to display what the invalid number is
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Try/except needed to see if files to open exist
- Fill README.md
/UNSTABLE BUILD/

30/08/2020 - v0.8.7 ALPHA:
+ Added CHANGELOG.md (Converted from changelog.txt)

- Format CHANGELOG.md properly
- Must validate grid has only 1 solution
- Needs to display what the invalid number is
- Saving settings needed (use thread to save?)
- Dark theme needed (light or dark mode radio button in drop down menu)
- Try/except needed to see if files to open exist
- Fill README.md
/UNSTABLE BUILD/
