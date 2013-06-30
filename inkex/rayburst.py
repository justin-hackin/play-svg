#!/usr/bin/env python 
"""creates a pattern similar to the Flower of Life (circles on outer edges should be arcs and not full circles)  """
import inkex
from playsvg import element, geom, path


class RayBurst(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--rays",
                        action="store", type="int", 
                        dest="rays", default=20,
                        help="Number of rays ")
        self.OptionParser.add_option("-a", "--radius",
                        action="store", type="float", 
                        dest="radius", default=30.0,
                        help="Radius of circle")
        self.OptionParser.add_option("-c","--isCentered",
                        action="store", type="inkbool", 
                        dest="centered", default=True,
                        help="Determines whether or not upward ray is centered (or instead its border is)")    
	
    def buildRayBurst(self, rays, radius, rayIsCentered):
        rayGroup = inkex.etree.Element('g', id='rays')
        whiteRays = inkex.etree.Element('g', id='whiterays')
        blackRays = inkex.etree.Element('g', id='blackrays')
       
        rayGroup.append(whiteRays)
        rayGroup.append(blackRays)
        
        rayStyle = None
        vertices = geom.createRadialPlots(geom.Point(0,0), radius, rays*2, rayIsCentered)
        for i in range(rays*2):
            rayPath = path.PathData("").moveTo(geom.Point(0,0)).lineTo(vertices[i]).lineTo(vertices[(i+1)%(rays*2)])
            if i%2 == 1:
                whiteRays.append(element.buildPath(rayPath, {'style':' stroke:none; fill:white' }))
            else:
                blackRays.append(element.buildPath(rayPath, {'style':' stroke:none; fill:black' }))
        return rayGroup
    
    
    def effect(self):
        new = self.buildRayBurst(self.options.rays, self.options.radius, self.options.centered)
        self.current_layer.append(new)
           

e = RayBurst()
e.affect()
