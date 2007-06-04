#!/usr/bin/env python
"""an alternative version of the Envelope function that supports groups of paths as well as paths with control points outside the object's bounding box"""
import inkex, os, copy, re
import xml.xpath
import playsvg.geom, playsvg.element, playsvg.document, playsvg.path

#FIXME: unlinking clones,
#FIXME: converting objects to paths
#FIXME: supporting multiply nested groups,
#FIXME: move gradients
#FIXME: bounding box envelopes line caps that aren't there, any tile with lines or paths that touch bounding box get spaced apart
#FIXME: will not work as expected if any elements to be tiled have translations, for now can fix by removing translations (grouping and ungrouping objects in Inkscape does this automatically, else use XML editor)

def getTransformLambda( bb, envPts):
    """returns a lambda to transform a set of co-ordinates into an envelope using the prarameters of envPts """
    def fn(targetPoint):
        #Transform algorithm from summernight.py modified to suit playsvg
        vector = playsvg.geom.Point(targetPoint.x,targetPoint.y) - playsvg.geom.Point(bb['x'],bb['y']) 
        xratio = vector.x/bb['width']
        yratio = vector.y/bb['height']
        xp1 =  playsvg.geom.getLineDivision(envPts[0], envPts[1], xratio)  
        xp2 = playsvg.geom.getLineDivision(envPts[3], envPts[2], xratio)
        yp1 = playsvg.geom.getLineDivision(envPts[1], envPts[2], yratio)
        yp2 = playsvg.geom.getLineDivision(envPts[0], envPts[3], yratio)
        transformedPoint = playsvg.geom.intersectLineLine(xp1, xp2, yp1, yp2)
        return transformedPoint
    return lambda x : fn(x)


class FitInBox(inkex.Effect):
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
        self.OptionParser.add_option("-o","--offset",
                        action="store", type="inkbool", 
                        dest="offset", default=False,
                        help="offsets the layers of the grid such that it forms a pattern similar to a dreamcatcher")    
    
    def effect(self):
        id = self.options.ids[0]
        
        #query inkscape about the bounding box of obj
        bb = {'x':0,'y':0,'width':0,'height':0}
        file = self.args[-1]
        for query in bb.keys():
            _,f,err = os.popen3("inkscape --query-%s --query-id=%s %s" % (query,id,file))
            bb[query] = float(f.read())
            f.close()
            err.close()
           
        
        docu = playsvg.document.Document(document=self.document)
        grid = None
        envCord = None
        rangeEnd = None
        numGridLayers = None
        
   

        obj = self.selected[self.options.ids[0]]
        box = self.selected[self.options.ids[1]]
        objCopy = obj.cloneNode(1)
        objCopy.attributes.getNamedItem('id').value += 'copy'
        docu.xdoc.documentElement.appendChild(objCopy)
        selectedObjectPaths = xml.xpath.Evaluate("descendant-or-self::path", objCopy)
        envPts = playsvg.path.PathData(text = box.attributes.getNamedItem('d').value).getNodes()
        
        for path in selectedObjectPaths:
            
            pathData = playsvg.path.PathData(text=path.attributes.getNamedItem('d').value)
            pathData.transformPoints(getTransformLambda(bb, envPts))
            path.attributes.getNamedItem('d').value = str(pathData)
        
    

e = FitInBox()
e.affect()

