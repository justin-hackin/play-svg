"""demonstrating an algorithmic approach to a technique of recursive polygon drawing demonstrated by Naked Geometry `here <http://goo.gl/uvZYj>`_"""

from playsvg.document import *
from playsvg.element import *
from playsvg.path import *

#number of sides
n = 11
iters = 2
initRadius = 260
#based upon the internal angal of the n-gon
bendAngal = 0.5 - 0.5*(n-2)/n
gonDepthGroup = []
docu = Document()

for i in range(iters):
    gonDepthGroup.append(docu.makeGroup(id=str(n)+"-gon_depth-"+str(i)))


def gonHelper(gonPoints, depth):
    for i in range(n):
        thisGonPoints = [gonPoints[i], getMidpoint(gonPoints[i], gonPoints[(i+1)%n]) ]
        sideLength = distanceBetween(thisGonPoints[0],thisGonPoints[1])
                 
        for i in range(2,n):
            thisGonPoints.append( extendBendPoint(thisGonPoints[-2], thisGonPoints[-1],sideLength,bendAngal ) )
        
        gonDepthGroup[depth].append(buildPath(PathData().makeHull(thisGonPoints), {'style':'fill:none;stroke:black;stroke-width:0.5'}) )
                
        if depth < iters-1:
            gonHelper(thisGonPoints, depth+1)

gonHelper(createRadialPlots(Point(), initRadius, n) , 0)



for i in range(0, iters):
    docu.append(gonDepthGroup[i])

docu.writeSVG("recursive_" +str(n) + "-gon_iter-"+str(iters) + ".svg" )
print "done"



