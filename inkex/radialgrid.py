#!/usr/bin/env python 
"""draws a Radial Grid as explained in compshapes.py"""
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class RadialGrid(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        
        self.OptionParser.add_option("-l", "--layers",
                        action="store", type="int", 
                        dest="layers", default=16,
                        help="Number of concentric layers")
        self.OptionParser.add_option("-s", "--spokes",
                        action="store", type="int", 
                        dest="spokes", default=20,
                        help="Number of radial divisions")
        self.OptionParser.add_option("-r", "--layerradius",
                        action="store", type="float", 
                        dest="layerradius", default=50.0,
                        help="Radius of a layer")
        self.OptionParser.add_option("-b", "--beginradius",
                        action="store", type="float", 
                        dest="beginradius", default=50.0,
                        help="Starting radius")
        

    def effect(self):
        docu = playsvg.document.Document(document=self.document)
	new = playsvg.compshapes.buildRadialGrid(docu, self.options.layers, self.options.spokes, self.options.beginradius, self.options.layerradius)
	self.document.documentElement.appendChild(new)

e = RadialGrid()
e.affect()
