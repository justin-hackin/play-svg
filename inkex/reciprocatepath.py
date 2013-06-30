#!/usr/bin/env python 
"""creates alternating reversed path duplicates """
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.path
class ReciprocatePath(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
       
        self.OptionParser.add_option("-r", "--reps",
                        action="store", type="int", 
                        dest="reps", default=6,
                        help="Number of reps")
	
	
	
    def effect(self):
         for id, node in self.selected.iteritems():
           if node.tag == inkex.addNS('path','svg'):
                thisPath = playsvg.path.PathData(text = node.get('d'))
                thisPath.backAndForth(self.options.reps)
                node.set('d', str(thisPath))
          
               
           

e = ReciprocatePath()
e.affect()
