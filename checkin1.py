import sys
import minic.minic_ast as mc
import minic.c_ast_to_minic as ctomc
from pycparser import parse_file
from pycparser.c_ast import *


class VarPrinter(NodeVisitor):
    
    def __init__(self):
        
        self.var_all = []
        self.var_written = []
        
    
    def visit_Assignment(self, assignment):
        ''' Visit all assignment statements and calls insertVariables to build 
            the list of variables. Handles the general cases. 
            (ie. a = b + 1)
        '''
        lval = assignment.lvalue
        rval = assignment.rvalue

        self.insertVariables(lval, write=True)
        self.insertVariables(rval, write=False)
                    
        
    def visit_BinaryOp(self, binop):
        ''' Visit all binary operators and calls insertVariables to include it's
            list of variables. Handles the ops in if statements. 
            (ie. if (foo == bar){})
        '''
        lvar = binop.left
        rvar = binop.right
        
        self.insertVariables(lvar, write=False)
        self.insertVariables(rvar, write=False)
        
        
    #def visit_If(self, ifstmt):
        #''' Visit all If statements and adds variables to self.var_all if the 
            #if statement contains a single variable.
            #(ie. if (condition))
        #'''
        #if isinstance(ifstmt.cond, mc.ID) and not ifstmt.cond.name in self.var_all:
            #self.var_all.append(ifstmt.cond.name)
        
        
    def insertVariables(self, node, write):
        ''' Builds the list of all variables and written variables by visiting
            the supplied node and it's children.
        '''
        if isinstance(node, mc.ID) and not node.name in self.var_all:
            self.var_all.append(node.name)
            
        if isinstance(node, mc.ID) and not node.name in self.var_written and write:
            self.var_written.append(node.name)
            
        elif isinstance(node, mc.ArrayRef):
            if isinstance(node.name, mc.ID) and not node.name.name in self.var_all:
                self.var_all.append(node.name.name)
          
        for child in node.children():
            if isinstance(child[1], mc.ArrayRef):
                if isinstance(child[1].name, mc.ID) and not child[1].name.name in self.var_all:
                    self.var_all.append(child[1].name.name)
                    
                if isinstance(child[1].subscript, mc.ID) and not child[1].subscript.name in self.var_all:
                    self.var_all.append(child[1].subscript.name)

            if not child[0] == "subscript" and isinstance(child[1], mc.ID):
                if not child[1].name in self.var_all:
                    self.var_all.append(child[1].name)
                    
                if not child[1].name in self.var_written and write:
                    self.var_written.append(child[1].name)
                    
    
    def getAllVariables(self):
        return self.var_all
    
        
    def getWrittenVariables(self):
        return self.var_written
    
    
if __name__=="__main__":
    
    filename = './project3inputs/p3_input2'
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
    
    varp = VarPrinter()
    varp.visit(mc_ast)
    print "All:", varp.getAllVariables()
    print "Written:", varp.getWrittenVariables()