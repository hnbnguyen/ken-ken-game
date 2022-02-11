# =============================
# Student Names: Kaitlyn Hung, Ngoc Bao Han Nguyen, Jude Tear
# Group ID: 80
# Date: Feb 10th, 2022
# =============================
# CISC 352 - W22
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # since there is no test code for his function in test.py
    # im still playing around with it at the moment
    vars = csp.get_all_unasgn_vars()
    max_degrees = -1
    for v in vars:
        degree = 0
        cons = csp.get_cons_with_var(v)
        for c in cons:
            unasgn_c = c.get_n_unasgn()
            if unasgn_c > 1:
                degree += 1
        if degree > max_degrees:
            var_dh = v
            max_degrees = degree
    return var_dh

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # Idea behind MRV: assigned most constrainted variable first, one with fewest possible values
    all_var = csp.get_all_unasgn_vars()
    size_domain = []
    # adding all the var and their domain size into the list
    for var in all_var:
        size_domain.append([var, var.cur_domain_size()])
    # sort the list from the var with largest domain size to smaller
    size_domain.sort(key = lambda x: -x[1])

    # return the variable with smallest domain
    return size_domain.pop()[0]
    


    
