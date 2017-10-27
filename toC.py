import sys


if __name__ == "__main__":
    
    filename = sys.argv[1]
    input_file = open(filename, "r")   
    varlist = []
    l = []
    written_vars = []
    operators = ["+", "-", "=", "*", "%", "/", "&&", "||", 
                 ">>", "<<", ">", "<", ">=", "<=", "!=", "==", "?", ":"]
    
    with open(filename) as f:
        for line in f:
            # Remove semicolons
            if ";" in line:
                line = line.rstrip()
                line = line[:-1]
            l = line.split()
            
            # Add all variables/expressions/numbers/strings/etc into varlist
            # by taking all things surrounding operators
            for i in range(len(l)):
                if l[i] in operators:
                    if not l[i - 1] in varlist:
                        if l[i] == "=":
                            if not "[" in l[i - 1]:
                                written_vars.append(l[i - 1])                            
                        if not "[" in l[i - 1]:
                            varlist.append(l[i - 1])
                    if not l[i + 1] in varlist:
                        if not "[" in l[i + 1]:
                            varlist.append(l[i + 1])
                # Deal with square and round bracket cases        
                if "[" in l[i]:
                    if not l[i].split("[")[0] in varlist:                       
                        varlist.append(l[i].split("[")[0])
                        
                if "(" in l[i]:
                    if not l[i].split("(")[1].split(")")[0] in varlist:                    
                        varlist.append(l[i].split("(")[1].split(")")[0])
    # Go through varlist, if there are operators in a var, add all the variables
    # involved in that var to varlist
    ind_to_del = [] 
    for i in range(len(varlist)):
        for o in operators:
            if o in varlist[i]:
                varlist[i] = varlist[i].replace(o, "*")
        char_list = list(varlist[i])
        for j in range(len(char_list)):
            if char_list[j] in operators:
                oper_ind = j
                operator = char_list[j]
                vars = varlist[i].split(operator)
                for var in vars:
                    if var not in varlist:
                        varlist.append(var)
                        if i not in ind_to_del:
                            ind_to_del.append(i)
    # Delete vars with operators in them    
    for ind in ind_to_del:
        del varlist[ind]
    
    # Delete numbers and strings from varlist
    ind_to_del = []
    for i in range(len(varlist)):
        try:
            if int(varlist[i]):
                ind_to_del.append(i)
        except:
            continue
                    
    for ind in ind_to_del:
        del varlist[ind]
        
    print "Printing all variables"
    print varlist
    print "Printing written variables"
    print written_vars