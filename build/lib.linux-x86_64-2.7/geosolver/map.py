class Map(dict):
    """A dictionary than can be used in dictionaries and sets. 
       Defines equality and a hash function.
       Recommended to be used as an immutable. 
       Call makehash() after mutations (but not if used in a set or other map!)
    """ 

    def __init__(self, d=None):
        if d:
            dict.__init__(self, d)
        else:
            dict.__init__(self)
        self.makehash()

    def __eq__(self, other):
        if hash(self) != hash(other):
            return False
        elif len(self) != len(other):
            return False
        else:
            if not isinstance(other, Map): 
                return False
            for key in self:
                if key not in other:
                    return False
                elif self[key] != other[key]:
                    return False
            return True 
    
    def makehash(self):
        val = 0
        for var in self:
            val = val + hash(var) + hash(self[var])
        self.hashvalue = hash(val)
        
    def __hash__(self):
        return self.hashvalue

    def __repr__(self):
        return "Map("+dict.__repr__(self)+")"


