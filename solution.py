import itertools

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
cols_rev = cols[::-1]

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# Definition of the boxes, units and peers that make up a sudoku puzzle
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
left_diagonal_units = [[rows[i]+cols[i] for i in range(len(rows))]]
right_diagonal_units = [[rows[i]+cols_rev[i] for i in range(len(rows))]]
unitlist = row_units + column_units + square_units + left_diagonal_units + right_diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    for unit in unitlist:
        # Find all pairs that could be considered naked twins
        pairs = [box for box in unit if len(values[box]) == 2]

        # Find all instances of naked twins
        twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
        for pair in twins:
            box1 = pair[0]
            box2 = pair[1]
            # Determine if box1 and box2 are twins: if yes, then continue checking peers
            # and removing the digits from peers; otherwise return values.
            if values[box1] == values[box2]:
                for box in unit:
                    # Eliminate the naked twins as possibilities for their peers
                    if box != box1 and box != box2:
                        for digit in values[box1]:
                            values[box] = values[box].replace(digit,'')
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
    """
    Look at peers and determine if we can eliminate possible values in a box.
    Args:
       values(dict): The sudoku in dictionary form
    Returns:
        The dictionary representation of the final sudoku grid.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Look at each box and determine if a number should be assigned because it is the most logical.
    Args:
       values(dict): The sudoku in dictionary form
    Returns:
        The dictionary representation of the final sudoku grid.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values

def reduce_puzzle(values):
    """
    Use multiple strategies to solve the Sudoku puzzle.
    Args:
       values(dict): The sudoku in dictionary form
    Returns:
        The dictionary representation of the final sudoku grid.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # The Eliminate Strategy
        values = eliminate(values)

        # The Only Choice Strategy
        values = only_choice(values)

        # The Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    Args:
       values(dict): The sudoku in dictionary form
    Returns:
        The dictionary representation of the final sudoku grid.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Get initial values from grid definition.
    values = grid_values(grid)

    # Search for solution to diagonal sudoku problem.
    diagonal_sudoku = search(values)
    
    # Check if diagonal_sudoku has values: if yes, then return diagonal_sudoku; otherwise return False.
    if diagonal_sudoku:
        return diagonal_sudoku
    else:
        return False

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
