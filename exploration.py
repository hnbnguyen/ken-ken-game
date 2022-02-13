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
# for r in range(grid_size):
#     for c in range(grid_size):
#         for n in range(c + 1, grid_size):
#             row_constraint = Constraint(name = "Cons(Var({},{}) and Var({},{}))".format(r + 1, c + 1, r + 1, n + 1), \
#                 scope= [variables[r][c], variables[r][n]])
            
#             col_constraint = Constraint(name = "Cons(Var({},{}) and Var({},{}))".format(r + 1, c + 1, n + 1, r + 1), \
#                 scope = [variables[c][r], variables[n][r]])

#             constraints.append(["Cons1", row_constraint])
#             constraints.append(["Cons2", col_constraint])
for r in range(0, grid_size):
    for c in range(0, grid_size):
        for a in range(c + 1, grid_size):
            con1 = Constraint("C(V{}{},V{}{})".format(r+1, c+1, r+1, a+1),\
                                [variables[r][c], variables[r][a]])
            con2 = Constraint("C(V{}{},V{}{})".format(c+1, r+1, a+1, r+1),\
                                [variables[c][r], variables[a][r]])
            constraints.append(["Cons1", con1])
            constraints.append(["Cons2", con2])

for constraint in constraints:
    print(constraint[0], constraint[1])