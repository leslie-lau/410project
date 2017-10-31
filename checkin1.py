import sys
import minic.minic_ast as mc
import minic.c_ast_to_minic as ctomc
from pycparser import parse_file
from pycparser.c_ast import *
sys.path.extend(['.','..'])



class VarPrinter(NodeVisitor):
    
    var_all = []
    var_written = []
    
    def visit_Assignment(self, assignment):
        
        lval = assignment.lvalue
        rval = assignment.rvalue
        
        if type(rval) == mc.ID and (not rval.name in self.var_all):
            self.var_all.append(rval.name)
            
        for node in rval.children():
            if type(node[1]) == mc.ID:
                if not node[1].name in self.var_all:
                    self.var_all.append(node[1].name)       
        
        if type(lval) == mc.ID and (not lval.name in self.var_all):
            self.var_all.append(lval.name)
        if type(lval) == mc.ID and (not lval.name in self.var_written):
            self.var_written.append(lval.name)
            
        for node in lval.children():
            if type(node[1]) == mc.ID:
                if not node[1].name in self.var_all:
                    self.var_all.append(node[1].name)
                if not node[1].name in self.var_written:
                    self.var_written.append(node[1].name)
        
    def visit_Decl(self, declaration):
        decl = declaration.name
        
    
    def getAllVariables(self):
        return self.var_all
        
    def getWrittenVariables(self):
        return self.var_written
        
    
if __name__=="__main__":
    
    filename = './project3inputs/p3_input1'
    txt = ''
    
    with open (filename) as f:
        txt = f.read()
    
    txt = 'void wrapper(){ \n' + txt + '\n}'
    
    c_filename = filename + '.c'
    c_file = open(c_filename, 'w')
    c_file.write(txt)
    c_file.close()

    ast = parse_file(c_filename)
    mc_ast = ctomc.transform(ast)
    
    varp = VarPrinter()
    varp.visit(mc_ast)
    print "All:", varp.getAllVariables(), ", Written:", varp.getWrittenVariables()