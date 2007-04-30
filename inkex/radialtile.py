#!/usr/bin/env python
"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
import inkex, os, copy
import xml.xpath
import playsvg.geom, playsvg.element, playsvg.document, playsvg.path

#FIXME: unlinking clones, converting paths to objects, supporting multiply nested groups, move gradients
#FIXME: points on bounding box not transformed properly --> Envelope in summernight does not suffer this same problem
#FIXME: points outside bounding box (with control points): how to deal ? 
#FIXME: need "bounding box of all nodes and control points" rather than "bounding box"; bug example: stroked squares tiled get spaced apart as radius increases

def getTransformLambda( bb, envPts):
    """returns a lambda to transform a set of co-ordinates into an envelope using the prarameters of envPts """
    def fn(targetPoint):
        #Transform algorithm from summernight.py modified to suit playsvg
        vector = playsvg.geom.Point(targetPoint.x,targetPoint.y) - playsvg.geom.Point(bb['x'],bb['y']) 
        xratio = abs(vector.x)/bb['width']
        yratio = abs(vector.y)/bb['height']
        xp1 =  playsvg.geom.getLineDivision(envPts[0], envPts[1], xratio)  
        xp2 = playsvg.geom.getLineDivision(envPts[3], envPts[2], xratio)
        yp1 = playsvg.geom.getLineDivision(envPts[1], envPts[2], yratio)
        yp2 = playsvg.geom.getLineDivision(envPts[0], envPts[3], yratio)
        transformedPoint = playsvg.geom.intersectLineLine(xp1, xp2, yp1, yp2)
        return transformedPoint
    return lambda x : fn(x)

   



class RadialTile(inkex.Effect):
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
        #query inkscape about the bounding box of obj
        bb = {'x':0,'y':0,'width':0,'height':0}
        file = self.args[-1]
        id = self.options.ids[0]
       
        for query in bb.keys():
            _,f,err = os.popen3("inkscape --query-%s --query-id=%s %s" % (query,id,file))
            bb[query] = float(f.read())
            f.close()
            err.close()
           
        numGridLayers =  self.options.layers +3
        docu = playsvg.document.Document(document=self.document)
        grid = None
        envCord = None
        rangeEnd = None
        if self.options.offset:
            grid = playsvg.geom.createOffsetRadialGrid(numGridLayers, self.options.spokes,  self.options.layerradius, self.options.beginradius)
            envCord = [(0,0), (-1, 1), (-2, 1), (-1, 0)]
            rangeEnd =  1 
        else:
            grid = playsvg.geom.createRadialGrid(numGridLayers, self.options.spokes,  self.options.layerradius, self.options.beginradius)
            envCord = [(0,0), (-1, 0), (-1, 1), (0, 1)]
            rangeEnd = 0 
            


        obj = self.selected[self.options.ids[0]]
        tileGroup = docu.makeGroup('tilegroup')
        envPts = None
        
        
        for layer in range(numGridLayers-1,rangeEnd,-1):
            for spoke in range(self.options.spokes):
                objCopy = obj.cloneNode(1)
                objCopy.attributes.getNamedItem('id').value += 'copy'+str(layer)+'-'+str(spoke)
                selectedObjectPaths = xml.xpath.Evaluate("descendant-or-self::path", objCopy)
                envPts = []
                for i in range(4):
                    envPts.append(grid[(layer+envCord[i][0]) %self.options.spokes][(spoke+envCord[i][1])%self.options.spokes ] )
                    
                for path in selectedObjectPaths:
                    
                    pathData = playsvg.path.PathData(text=path.attributes.getNamedItem('d').value)
                    pathData.transformPoints(getTransformLambda(bb, envPts))
                    path.attributes.getNamedItem('d').value = str(pathData)
                tileGroup.appendChild(objCopy)
        docu.xdoc.documentElement.appendChild(tileGroup)
    

e = RadialTile()
e.affect()

