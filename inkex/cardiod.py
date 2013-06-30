#!/usr/bin/env python 
"""creates a pattern similar to the Flower of Life (circles on outer edges should be arcs and not full circles)  """
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class Cardiod(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=30.0,
                        help="Radius of circle")
        self.OptionParser.add_option("-c", "--circles",
                        action="store", type="int", 
                        dest="circles", default=20,
                        help="Number of circles ")
	
	
	
    def effect(self):
           new = playsvg.compshapes.buildCircleCardioid(self.options.circles, self.options.radius)
           self.current_layer.append(new)
           

e = Cardiod()
e.affect()
