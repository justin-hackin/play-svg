#!/usr/bin/env python 
"""creates 2 waves weaving around each other weaving around a circle   """
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class RoundWeave(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        
        self.OptionParser.add_option("-c", "--crosses",
                        action="store", type="int", 
                        dest="crosses", default=20,
                        help="Number of crosses ")
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=30.0,
                        help="Radius of circle")
        self.OptionParser.add_option("-g", "--gap",
                        action="store", type="float", 
                        dest="gap", default=30.0,
                        help="Gap")
        self.OptionParser.add_option("-e", "--extent",
                        action="store", type="float", 
                        dest="extent", default=30.0,
                        help="Extent")
	
	
	
    def effect(self):
           new = playsvg.compshapes.buildCircularWeave(self.options.crosses, self.options.radius, self.options.gap, self.options.extent)
           self.current_layer.append(new)
           

e = RoundWeave()
e.affect()
