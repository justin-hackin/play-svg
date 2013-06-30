#!/usr/bin/env python 

import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class LotusFlower(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-p", "--petals",
                        action="store", type="int", 
                        dest="petals", default=12,
                        help="Number of petals")
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=300,
                        help="Radius of flower")
	self.OptionParser.add_option("-l", "--petallength",
                        action="store", type="float", 
                        dest="petallength", default=50.0,
                        help="Petal length")
	self.OptionParser.add_option("-c", "--controldistance",
                        action="store", type="float", 
                        dest="controldistance", default=0.5,
                        help="Distance ratio for control points")

	
	
	
    def effect(self):
        path = playsvg.pathshapes.lotusPetalFlower(self.options.petals, self.options.radius, self.options.radius+self.options.petallength, self.options.controldistance)
        new = playsvg.element.buildPath(path, {'style':'stroke:black;fill:none'})
        self.current_layer.append(new)

e = LotusFlower()
e.affect()
