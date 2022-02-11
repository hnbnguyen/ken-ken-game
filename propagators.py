# =============================
# Student Names: Kaitlyn Hung, Ngoc Bao Han Nguyen, Jude Tear
# Group ID: 80
# Date: 02/08/2022
# =============================
# CISC 352 - W22
# propagators.py
# desc: 
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

from collections import deque

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    # If newly instantiated variable is None, for forward checking, we get all contraints
    if newVar == None:
        cons = csp.get_all_cons()
    # else we get only ones with newly instantiated variables
    else:
        cons= csp.get_cons_with_var(newVar)

    pruned = [] # values to be pruned from the domain choice

    for c in cons:
        if c.get_n_unasgn() == 1: # there is only 1 unassigned variable left
            unasgn_var = c.get_unasgn_vars().pop()

            # try out the all the different option from existing domains
            var_dom = unasgn_var.cur_domain()

            for val in var_dom:
                # assigning values from the domain to the unassigned variable
                unasgn_var.assign(val)
                variables = c.get_scope()
                values = []

                # checking with other variables to see if it makes a coherrent set
                for var in variables:
                    assigned_val = var.get_assigned_value()
                    values.append(assigned_val)

                if not c.check(values):
                    pruned.append((unasgn_var, val))
                    unasgn_var.prune_value(val)
                unasgn_var.unassign()

            if unasgn_var.cur_domain_size == 0: # there is no option left to try 
                return False, pruned

    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    pass
   
    
    # check all constraints
    if newVar == None:
        cons = csp.get_all_cons()
    # if there is input variable, check constraints involving the input variable
    else:
        cons = csp.get_cons_with_var(newVar)
    
    # keeping track of GAC queue and pruned
    pruned = []
    GAC_q = deque() # initialize queue
    for c in cons:
        GAC_q.append(c)
    
    # keeping running until no more element in queue left
    while GAC_q: 
        constraint = GAC_q.popleft()
        # going through all unassigned VARIABLES within CONSTRAINTS scope 
        # within those VARIABLES going through all VALUES it can be assigned to
        for var in constraint.get_unasgn_vars():
            for val in var.cur_domain():
                # finding an assignment that satisfy the constraint
                if not constraint.has_support(var, val): 
                    # prune it 
                    var.prune_value(val)
                    pruned.append((var, val))

                    # check for domain wipeout
                    if var.cur_domain_size() == 0:
                        return False, pruned
                    else: # queuing all the constraints that has the variable in scope
                        for c in cons:
                            if c not in GAC_q and var in c.get_scope():
                                GAC_q.append(c)
    return True, pruned


