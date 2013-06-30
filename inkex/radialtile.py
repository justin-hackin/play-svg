#!/usr/bin/env python
"""tiles an object into a Radial Grid or an Offset Radial Grid as generated in compshapes.py"""
import inkex, os, copy, re
import playsvg.geom, playsvg.element, playsvg.document, playsvg.path
import pathmodifier
from copy import deepcopy

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


class RadialTile(pathmodifier.PathModifier):
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
           
        
       
        grid = None
        envCord = None
        rangeEnd = None
        numGridLayers = None
        idCounter = 1
        
        #initialized values based on offset option
        if self.options.offset:
            numGridLayers =  self.options.layers +3
            grid = playsvg.geom.createOffsetRadialGrid(numGridLayers, self.options.spokes,  self.options.layerradius, self.options.beginradius)
            envCord = [(0,0), (-1, 1), (-2, 1), (-1, 0)]
            rangeEnd =  1 
            
        else:
            numGridLayers =  self.options.layers +1
            grid = playsvg.geom.createRadialGrid(numGridLayers, self.options.spokes,  self.options.layerradius, self.options.beginradius)
            envCord = [(0,0), (-1, 0), (-1, 1), (0, 1)]
            rangeEnd = 0 
                         


        obj = self.selected[self.options.ids[0]]
        
        tileGroup = inkex.etree.SubElement(self.current_layer, 'g')
        
        envPts = None
        
        #create copies of the tile enveloped to the grid
        for layer in range(numGridLayers-1,rangeEnd,-1):
            for spoke in range(self.options.spokes):
                
                #inkex.debug("Length of duplicate list:" + len(self.duplicateNodes({obj.attributes.getNamedItem('id').value:obj})))
                #pathmodifier.fuseTransform(obj)
                
                objCopy = deepcopy(obj)
                tileGroup.append(objCopy)
                
                #FIXME: add support for gradients
                
##                #check if fill is gradient
##                styleDict = simplestyle.parseStyle(objCopy.attributes.getNamedItem('style').value)
##                gradre= re.compile('url\(*\)')
##                if gradre.match(styleDict['fill']) != None:
##                    
##                    #get url of gradient
##                    #duplicate gradient in defs
##                    #transform control points in new gradient (control points likely outside of bounding box ????)
##                    #set color to new gradient
                #FIXME: only paths and not convertible objects get selected and properly tiled
                selectedObjectPaths = objCopy.iter()
                
                selectedObjectPaths = [i for i in selectedObjectPaths if (inkex.etree.QName(i).localname   == 'path')]
                
                #inkex.debug("objectPathsLen"+str(len(selectedObjectPaths)))
                
                
                envPts = []
                for i in range(4):
                    envPts.append(grid[(layer+envCord[i][0])][(spoke+envCord[i][1])%self.options.spokes ] )
                    
                for path in selectedObjectPaths:
                    
                    pathData = playsvg.path.PathData(text=path.get('d'))
                    pathData.transformPoints(getTransformLambda(bb, envPts))
                    inkex.debug("this"+str(pathData))
                    path.set('d',str(pathData))
        
            
       

    

e = RadialTile()
e.affect()

