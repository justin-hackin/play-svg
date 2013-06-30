#!/usr/bin/env python 
"""creates a series of vertically-stacked boxes with a fill color changing incrementally from one color to another"""
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class DiscreteColorGrad(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-i", "--intervals",
                        action="store", type="int", 
                        dest="intervals", default=10,
                        help="Number of colors in palette")
        self.OptionParser.add_option("-s", "--startcolor",
                        action="store", type="string", 
                        dest="startcolor", default="#ff0000",
                        help="Starting color")
        self.OptionParser.add_option("-e", "--endcolor",
                        action="store", type="string", 
                        dest="endcolor", default="#0000ff",
                        help="Ending color")
        self.OptionParser.add_option("-z", "--size",
                        action="store", type="int", 
                        dest="size", default=300,
                        help="Palette size")


    def effect(self):
        docu = None
        new = playsvg.compshapes.buildDiscreteColorGrad(self.options.intervals, self.options.startcolor, self.options.endcolor, self.options.size)
        self.current_layer.append(new)

e = DiscreteColorGrad()
e.affect()
