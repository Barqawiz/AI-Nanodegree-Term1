"""common"""
rows = 'ABCDEFGHI'
cols = '123456789'
def cross(A, B):
    return [s+t for s in A for t in B]
boxes = cross(rows, cols)

def diagonal(rows, cols):
    return [[rows[index]+cols[index] for index in range(9)],[rows[index]+cols[8-index] for index in range(9)]]

diagonal_units = diagonal(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

"""solution"""
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for box in boxes:
        vertixValue = values[box]
        if (len(vertixValue) == 2):
            for unit in units[box]:
                    """ check if there is same """
                    mysame = [item for item in unit if values[item] == vertixValue]
                    "print('vertixValue: ' + vertixValue + ' from unit: ', unit)"
                    "print('same me : '    , mysame)"
                    """ remove same from values """
                    if (len(mysame) == 2):
                        for item in unit:
                            "loop on digits to remove"
                            for num in vertixValue:
                                if (num in values[item] and vertixValue != values[item] and len(values[item]) > 1):
                                    values[item] = values[item].replace(num,"")
    return values
                        

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    keyToCheck = [item for item in values if len(values[item]) == 1]
    
    for item in keyToCheck:
	           myPeer = peers[item]
	           for peer in myPeer:
	               values[peer] = values[peer].replace(values[item],'')
 
    return values

def only_choice(values):
    for unit in unitlist:
        
        for d in '123456789':
            myKeys = []
            for key in unit:
                if d in values[key]:
                    myKeys.append(key)
                    
            if len(myKeys) == 1:
                values[myKeys[0]] = d
                    
                

    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)
        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    
    if values is False or all(len(values[box]) == 1 for box in boxes):
        "print('stop case')"
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    minValue = 10
    selectedItem = -1
    for box in boxes:
         if (len(values[box]) > 1 and len(values[box]) < minValue):
             minValue = len(values[box])
             selectedItem = box
    
    "print ('min value is: ', minValue, ' and selected item is: ', selectedItem)"
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    if (selectedItem != -1):
        for digit in values[selectedItem]:
            tempValues = values.copy()
            tempValues[selectedItem] = digit
            answer = search(tempValues)
            if answer:
                return answer

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sodukoDic = grid_values(grid)

    sodukoDic = eliminate(sodukoDic)
    sodukoDic = only_choice(sodukoDic)
    sodukoDic = search(sodukoDic)

    return sodukoDic;

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
