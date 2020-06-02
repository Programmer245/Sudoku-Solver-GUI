'''Sudoku Solver Logic Module'''

import copy # Used for creating copies of variables instead of instances

def possible(grid, x, y, n):
    '''Takes in the grid, x position, y position, and value of a possible number

    Returns True or False if a number can fit in a specific position in the grid'''

    # Checks row
    for position in grid[y]:
        if position == n:
            return False

    # Checks column
    for row in grid:
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

    for row in grid[yrange[0]:yrange[-1]+1]:
        for position in row[xrange[0]:xrange[-1]+1]:
            if position == n: # Checks every position in the square
                return False

    return True # No doubles detected

def solve(grid):
    '''Yields each solution in order'''
    
    for ypos, row in enumerate(grid): # Goes through each row in the column
        for xpos, position in enumerate(row): # Goes through each position in the row
            if position == 0: # Position must be empty
                for num in range(1,10): # Tries all numbers from 1 to 9
                    if possible(grid, xpos, ypos, num): # Check if the number is a possible
                        grid[ypos][xpos] = num # Puts possible number in empty space
                        yield grid
                        solve(grid) # Keeps solving
                        grid[ypos][xpos] = 0 # If program reaches here, no further numbers can be put into the grid and the square is reset
                        yield grid
                
                return False # No possible solution has been found for an empty position; exits functions

    # If program reaches this point, there are no more empty spaces in the grid and a solution has been found

    deepcopy_grid = copy.deepcopy(grid) # A copy of the original grid is made
    yield deepcopy_grid # New solution is yielded