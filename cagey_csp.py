# =============================
# Student Names: Kaitlyn Hung, Ngoc Bao Han Nguyen, Jude Tear

# Group ID: 80 
# Date: 02/08/2022
# =============================
# CISC 352 - W22
# cagey_csp.py
# desc: 
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):
    # getting the grid size
    grid_size = cagey_grid[0]

    # populating a domain list from 1 to n, this is all the values a variable square can have
    value_domain = [ _ for _ in range(1, grid_size + 1)] # [1,2,3] ie

    # initialize a variable matrix
    variables = []
    # variables = [[Variable("{},{}".format(r,c), domain= value_domain) for c in range(grid_size)] for r in range(grid_size)]
    # going through all the colummns and rows to populate the var matrix
    for r in range(1, grid_size + 1) :
        cur_row = []
        for c in range(1, grid_size + 1):
            cur_var = Variable("Var({},{})".format(r,c), domain=value_domain)
            cur_row.append(cur_var)
        variables.append(cur_row)

    # creating a Constraint matrix
    constraints = []

    # going through cell (by traversing through every rows and cols)
    # when at that cell, traversing through all the next cell that is in the SAME row and col
    # to update the contraints that they hold
    sat_tuples = []
    for i in itertools.product(value_domain, value_domain):
        if i[0] != i[1]:
            sat_tuples.append(i)
    for r in range(grid_size):
        for c in range(grid_size):
            for n in range(c + 1, grid_size):
                # adding the constraint of a pair in the same row
                row_constraint = Constraint(name = "Cons(Var({},{}) and Var({},{}))".format(r + 1, c + 1, r + 1, n + 1), \
                    scope= [variables[r][c], variables[r][n]])
                row_constraint.add_satisfying_tuples(sat_tuples)
                # adding the constraint of a pair in the same column
                col_constraint = Constraint(name = "Cons(Var({},{}) and Var({},{}))".format(r + 1, c + 1, n + 1, r + 1), \
                    scope = [variables[c][r], variables[n][r]])
                col_constraint.add_satisfying_tuples(sat_tuples)

                constraints.append(row_constraint)
                constraints.append(col_constraint)

    variables_csp = []

    for i in range(grid_size):
        for j in range(grid_size):
            variables_csp.append(variables[i][j])
    csp = CSP("binary_grid_csp", variables_csp)

    for cons in constraints:
        csp.add_constraint(cons)
    return csp, variables


def nary_ad_grid(cagey_grid):
    # getting the grid size
    grid_size = cagey_grid[0]

    # populating a domain list from 1 to n, this is all the values a variable square can have
    value_domain = [ _ for _ in range(1, grid_size + 1)] # [1,2,3] ie

    # initialize a variable matrix
    variables = []
    # variables = [[Variable("{},{}".format(r,c), domain= value_domain) for c in range(grid_size)] for r in range(grid_size)]
    # going through all the colummns and rows to populate the var matrix
    for r in range(1, grid_size + 1) :
        cur_row = []
        for c in range(1, grid_size + 1):
            cur_var = Variable("Var({},{})".format(r,c), domain=value_domain)
            cur_row.append(cur_var)
        variables.append(cur_row)

    # creating a Constraint matrix
    constraints = []
    
    for r in range(grid_size):
        # no variable should have the same value in a row
        row_constraint = Constraint(name = "Cons(row {})".format(r + 1),\
            scope = [variables[r][i] for i in range(grid_size)])
        
        variable_col = []
        for c in range(grid_size):
            variable_col.append(variables[c][r])
        # no variable should have the same value in a column
        col_constraint = Constraint(name = "Cons(col {})".format(r + 1),\
            scope = [variable_col[i] for i in range(grid_size)])

        sat_tuples = []
        # grid_size * (grid_size - 1) * (grid_size - 2) * .... = num of all possible permutations
        for i in itertools.permutations(value_domain, len(value_domain)):
            sat_tuples.append(i)
        row_constraint.add_satisfying_tuples(sat_tuples)
        col_constraint.add_satisfying_tuples(sat_tuples)
        constraints.append(row_constraint)
        constraints.append(col_constraint)
    
    # initializing a CSP constraint and add all cons to it
    variables_csp = []
    for i in range(grid_size):
        for j in range(grid_size):
            variables_csp.append(variables[i][j])
    csp = CSP("nary_grid_csp", variables_csp)
    for cons in constraints:
        csp.add_constraint(cons)
    
    return csp, variables

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass
