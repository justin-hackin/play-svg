"""
Module for method graphs 
Copyright Rick van der Meiden, 2003, 2004
Created: 1 Nov 2003.

A method graph contains variables and methods. Methods are objects that
specify input and output variables and an 'execute' method. Whenever the
value of a variable is changed, one or more methods are executed to update
the value of 'upstream' variables. 

Changes:
23 Nov 2004 - added Error classes, updated naming and doc conventions (PEP 8, 257)
"""

from graph import Graph

# ----------- misc stuff -----------

def _strseq(seq):
    """print string rep of items in a sequence, seperated by commas. 
    
       It realy sucks that str(list/dict) uses the __repr__ method of items
       in the list/dict. Ergo, this function. 
    """
    s = ""
    for el in seq:
        s += str(el)
        s += ','
    if len(s) > 0:
        s = s[:-1]
    return s


# ----------- Exceptions -----------

class ValidityError(Exception):
    """Error indicating operation violated MethodGraph validity"""

    def __init__(self, message):
        """Constructor for ValidityError
        
           arguments:
               message - message to be displayed
        """
        self._message = message
    
    def __str__(self):
        return "ValidityError: " + self._message

# ----------- class Method -----------

class Method:
    """Abstract method
    
       A Method is an object that defines input variables, output variables
       and an execute method. This class should be considered abstract.
       Instances (of subclasses of) Method must be non-mutable, hashable objects.
    """
 
    def inputs(self):
        """return a list of input variables
        
           If an attribute '_inputs' has been defined, a new list
           with the contents of that attribute will be returned. 
           Subclasses may choose to initialise this variable or to 
           override this function. 
        """
        if hasattr(self, "_inputs"):
            return list(self._inputs)
        else:
            raise NotImplementedError
    
    def outputs(self):
        """return a list of output variables
        
           If an attribute '_outputs' has been defined, a new list
           with the contents of that attribute will be returned. 
           Subclasses may choose to initialise this variable or to 
           override this function. 
        """
        if hasattr(self, "_outputs"):
            return list(self._outputs)
        else:
            raise NotImplementedError
   
    def execute(self, inmap):
        """Execute method.

        Returns a mapping (dictionary) of output variables to values, 
        given an input map, mapping input variables to values (dictionary)
        The previous value of the output variable should also be in inmap.
        If the method cannot be executed, it should return an empty map.
        """
        raise NotImplementedError

# ----------- class MethodGraph -------

class MethodGraph:
    """Implementation of a method graph

    A method graph is represented by 
    a directed bi-partite graph: nodes are either varables or methods. 
    Edges run from input variables to methods and from methods to ouput
    variables. 
    
    A method graph may not contain cycles. Every variable must be 
    determined by at most one constraint.

    Methods must be instances of (subclasses of) class Method.
    Variables are basically just names, and may be any 
    non-mutable, hashable object, e.g. strings.
    Values associated with variables may be of any type.

    If no value is explicitly associated with a variable, it defaults to None.
    """

    def __init__(self):
        self._map = {}
        """A map from variable names to values"""
        self._methods = {}
        """A set of methods"""
        self._graph = Graph()
        """A graph for fast navigation"""
        self._changed = {}
        """Set of changed variables since last propagation"""

    def variables(self):
        """return a list of variables"""
        return self._map.keys()

    def methods(self):
        """return a list of methods"""
        return self._methods.keys()

    def add_variable(self, varname, value = None):
        """Add a variable, optionally with a value"""
        if not varname in self._map:
            self._map[varname] = value
            self._graph.add_vertex(varname)
    
    def rem_variable(self, varname):
        """Remove a variable and all methods on that variable"""
        if varname in self._map:
            del self._map[varname]
            if varname in self._changed:
                del self._changed[varname]
            # delete al methods on it
            for met in self._graph.ingoing_vertices(varname):
                self.rem_method(met)
            for met in self._graph.outgoing_vertices(varname):
                self.rem_method(met)
            # remove it from graph
            self._graph.rem_vertex(varname)
        else:
            raise StandardError, "variable not in graph"
    # end rem variable

    def get(self,varname):
        """get the value of a variable"""
        return self._map[varname]

    def set(self, varname, value, prop = True):
        """Set the value of a variable.
        
           Iff prop is true then this change and any pending
           changes will be propagated. 
        """
        self._map[varname] = value
        self._changed[varname] = 1
        if prop:
            self.propagate()

    def add_method(self, met, prop = True):
        """Add a method.
        
           Iff prop is true then this change and any pending
           changes will be propagated. 
        """

        if met in self._methods:
            return 
        self._methods[met] = 1
        # update graph    
        for var in met.inputs():
            self.add_variable(var)
            self._graph.add_edge(var, met)
        for var in met.outputs():
            self.add_variable(var)
            self._graph.add_edge(met, var)
        
        # check validity of graph
        for var in met.outputs():
            if len(self._graph.ingoing_vertices(var)) > 1: 
                self.rem_method(met)
                raise ValidityError, "variable "+str(var)+" determined by multiple methods"
            elif len(self._graph.path(var, var)) != 0:
                self.rem_method(met)
                raise ValidityError, "cylce in graph not allowed (variable "+str(var)+")"
        # end for    
        
        if prop:
            self._execute(met)
            self.propagate()
        
    def rem_method(self, met):
        """Remove a method"""
        if met in self._methods:
            del self._methods[met]
            self._graph.rem_vertex(met)
        else:
            raise StandardError, "method not in graph"

    def propagate(self):
        """Propagate any pending changes.
        
        Changes are propagated until no changes are left or until
        no more changes can be propagated. This method is called
        from set() and add_method() by default. However, if the
        user so chooses, the methods will not call propagate, and
        the user should call this fucntion at a convenient time. 
        """
        while len(self._changed) != 0:
            pick = self._changed.keys()[0]
            methods = self._graph.outgoing_vertices(pick)
            for met in methods:
                self._execute(met)
            #end for
            if pick in self._changed:
                del self._changed[pick]
        #end while
    #end def propagate
    
    def clear(self):
        """clear methodgraph by removing all variables"""
        while (len(self._map) > 0):    
            var = self._map.keys()[0]
            self.rem_variable(var)
        #wend
    #def
    
    def execute(self, met):
        """Execute a method and proagate changes. Method must be in Methodgraph"""
        if met in self._methods:
            self._execute(met)
            self.propagate()
        else:
            raise StandardError, "method not in graph"

    def _execute(self, met):
        """Execute a method. 
        Method is executed only if all inputvariable values are not None
        Updates mapping and change flags.  
        """
        # create input map and check for None-values
        inmap = {}
        hasNoneValues = False
        for var in met.inputs():
            value = self._map[var]
            if value == None:
                hasNoneValues = True
            inmap[var] = value
        for var in met.outputs():
            inmap[var] = self._map[var]
        # call method.execute
        if hasNoneValues:
            outmap = {}
        else:
            outmap = met.execute(inmap)
        # update values in self._map
        # set output variables changed
        for var in met.outputs():
            if var in outmap:
                self._map[var] = outmap[var]
                self._changed[var] = 1
            else:
                if self._map[var] != None:
                    self._changed[var] = 1
                    self._map[var] = None
                
        #end for
        # clear change flag on input variables 
        for var in met.inputs():
            if var in self._changed:
                del self._changed[var]
        #end for

    # end def execute

    def __str__(self):
        s = "MethodGraph(variables=["
        s += _strseq(self._map.keys())
        s += "], methods=["
        s += _strseq(self._methods.keys())
        s += "])"
        return s;

# end class MethodGraph

# ----------- various Methods ---------

class AddMethod(Method):
    def __init__(self, a, b, c):
        """new method c := a + b"""
        self._inputs = [a,b]
        self._outputs = [c]

    def execute(self, inmap):
        outmap = {}
        a = self._inputs[0]
        b = self._inputs[1]
        c = self._outputs[0]
        if a in inmap and b in inmap and \
           inmap[a] != None and inmap[b] != None:
            outmap[c] = inmap[a] + inmap[b]
        #fi
        return outmap

    def __str__(self):
        s = "AddMethod("
        s += str(self._inputs[0])
        s += ','
        s += str(self._inputs[1])
        s += ','
        s += str(self._outputs[0])
        s += ')' 
        return s

class SubMethod(Method):
    def __init__(self, a, b, c):
        """new method c := a - b"""
        self._inputs = [a,b]
        self._outputs = [c]
 
    def execute(self, inmap):
        outmap = {}
        a = self._inputs[0]
        b = self._inputs[1]
        c = self._outputs[0]
        if a in inmap and b in inmap and \
           inmap[a] != None and inmap[b] != None:
            outmap[c] = inmap[a] - inmap[b]
        #fi
        return outmap
 
    def __str__(self):
        s = "SubMethod("
        s += str(self._inputs[0])
        s += ','
        s += str(self._inputs[1])
        s += ','
        s += str(self._outputs[0])
        s += ')' 
        return s

class SetMethod(Method):
    def __init__(self, var, value):
        """new method var := value
       
           keyword arguments:
               var - variable name
               value - any object to be associated with var
               
        """
        self._inputs = []
        self._outputs = [var]
        self._value = value
 
    def execute(self, inmap):
        return {self._outputs[0]:self._value}
 
    def __str__(self):
        s = "SetMethod("
        s += str(self._outputs[0])
        s += ','
        s += str(self._value)
        s += ')' 
        return s

class AssignMethod(Method):
    def __init__(self, a, b):
        """new method a := b
       
           keyword arguments:
               a - variable name
               b - variable name
        """
        self._inputs = [b]
        self._outputs = [a]
 
    def execute(self, inmap):
        if self._inputs[0] in inmap:
           return {self._outputs[0]:inmap(self._inputs[0])}
        else: 
           return {}
 
    def __str__(self):
        s = "SetMethod("
        s += str(self._inputs[0])
        s += ','
        s += str(self._value)
        s += ')' 
        return s


# ---------- test ----------

def test():
    print "-- testing method graph"
    mg = MethodGraph()
    print "set a = 3"
    mg.add_variable('a', 3)
    print "set b = 4"
    mg.add_variable('b', 4)
    print "c := a + b"
    mg.add_method(AddMethod('a','b','c'))
    print "c = "+str(mg.get('c'))
    print "set a = 10"
    mg.set('a', 10)
    print "c = "+str(mg.get('c'))
    mg.add_method(AddMethod('a','c','d'))
    print "d := a + c"
    mg.add_method(AddMethod('b','d','e'))
    print "e := b + d"
    print "d = "+str(mg.get('d'))
    print "e = "+str(mg.get('e'))
    print "a := d + e"
    import sys, traceback
    try:
        mg.add_method(AddMethod('d','e','a'))
        print "success: should not be possible"
    except Exception, e:
        print e 
    print "e := a + b"
    try:
        mg.add_method(AddMethod('a','b','e'))
        print "success: should not be possible"
    except Exception, e:
        print e 

if __name__ == "__main__": 
    test()


