import sys
import minic.minic_ast as mc
import minic.c_ast_to_minic as ctomc
from pycparser import parse_file
from pycparser.c_ast import *


class AllVariables(NodeVisitor):
    
    def __init__(self):
        self.var_all = []
        self.var_written = []
    
    def visit_ID(self, Id):
        if not Id.name in self.var_all:
            self.var_all.append(Id.name)
    
    def getAllVariables(self):
        return self.var_all
    
    def getWrittenVariables(self):
        return self.var_written 
    
    
class WrittenVariables(NodeVisitor):
    
    def __init__(self):
        self.var_all = []
        self.var_written = []
        
    def visit_Assignment(self, assignment):
        if isinstance(assignment.lvalue, mc.ID):
            self.var_written.append(assignment.lvalue.name)
            
        if isinstance(assignment.lvalue, mc.ArrayRef):
            self.var_written.append(assignment.lvalue.name.name)
        
        self.generic_visit(assignment)
    
    def getWrittenVariables(self):
        return self.var_written
    
    
class FunctionPrototype():
    
    def __init__(self, written, undef):
        self.wrt_list = written
        self.undef_list = undef
        
    def __str__(self):
        arg = ", ".join(self.wrt_list)
        out = ", ".join(self.undef_list)
        fp = "fun block_function(" + arg + ") " + "returns " + out
        return fp
    

if __name__=="__main__":
    
    filename = './project3inputs/p3_input4'
    #filename = sys.argv[1]
    txt = ''
    
    with open(filename) as f:
        txt = f.read()

    txt = 'void wrapper(){ \n' + txt + '\n}'
    
    c_filename = filename + '.c'
    c_file = open(c_filename, 'w')
    c_file.write(txt)
    c_file.close()

    ast = parse_file(c_filename)
    mc_ast = ctomc.transform(ast)
    
    allvar = AllVariables()
    allvar.visit(mc_ast)
    allvar_list = allvar.getAllVariables()
    print "All:", allvar_list
    
    writevar = WrittenVariables()
    writevar.visit(mc_ast)
    wrtvar_list = writevar.getWrittenVariables()
    print "Written:", wrtvar_list
    
    undef_list = []
    for var in allvar_list:
        if not var in wrtvar_list:
            undef_list.append(var)
    print "Undefined", undef_list
    
    print
    fp = FunctionPrototype(wrtvar_list, undef_list)
    print fp
    