# just a python test file to debug 
from cspbase import Constraint, Variable
grid_size = 3
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

constraints =[]
for r in range(grid_size):
    for c in range(grid_size):
        for n in range(c + 1, grid_size):
            row_constraint = Constraint(name = "Cons(Var({},{}) and Var({},{}))".format(r + 1, c + 1, r + 1, n + 1), \
                scope= [variables[r][c], variables[r][n]])
            
            col_constraint = Constraint(name = "Cons(Var({},{}) and Var({},{}))".format(r + 1, c + 1, n + 1, r + 1), \
                scope = [variables[c][r], variables[n][r]])

            constraints.append(row_constraint)
            constraints.append(col_constraint)
            
for constraint in constraints:
    print(constraint)