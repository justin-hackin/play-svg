#!/usr/bin/env python 
"""creates a pattern similar to the Flower of Life (circles on outer edges should be arcs and not full circles)  """
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class FlowerOfLife(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=30.0,
                        help="Radius of circle")
        self.OptionParser.add_option("-l", "--levels",
                        action="store", type="int", 
                        dest="levels", default=20,
                        help="Number of concentric levels ")
	
	
	
    def effect(self):
           new = playsvg.compshapes.buildFlowerOfLife( self.options.levels, self.options.radius)
           self.current_layer.append(new)
           

e = FlowerOfLife()
e.affect()
