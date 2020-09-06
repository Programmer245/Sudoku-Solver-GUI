README:
===

***

*Important:*
---

For proper usage, LICENCE.md, README.md, and any other provided resources must **NOT** be renamed, modified, or moved from their respective locations. This software has been made using Python 3.8 and is optimized for Windows 10; usage on other OS type may result in the unexpected failure of the program due to incompatibility issues.

*About Sudoku Solver:*
---

Using a combination of libraries, this software aims to facilitate the asynchronous solving of Sudoku grids through the use of the [backtracking algorithm](https://en.wikipedia.org/wiki/Backtracking) and multithreading implemented in a graphical user interface.

By definition,
> A Sudoku has only one solution. Anything else is just a grid of numbers.

however, for efficiency, the program will allow users to enter any grid as long as at least 17 clues have been entered, and that the clues are correctly positioned so that each number only appears once in each row, column, and square.

A sample grid has been provided for easy manipulation.

*Usage:*
---

+ To prepare an external grid for importing, modify the provided sample_grid.json file by changing the preset grid clues (it is also possible to provide a custom .json file as long as the format is the same as that of sample_grid.json).
+ To save a set of solutions to a .txt file, press 'Save as' or enable 'Auto-Save' before completion of execution and either select an empty .txt file or create a new .txt file for storing solutions. **NOTE THAT SAVE FUNCTIONALITY OVERWRITES ANY PREVIOUS DATA; USE WITH CAUTION**. 

*(Advanced)*

+ To manually modify the settings, open settings.json and change Autosave or AnimationDelay to 0 (Off) or 1 (On).