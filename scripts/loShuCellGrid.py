import base
import pathshapes
import math
import color
from geom import *
from elements import *
import trigramaton
from copy import *
import permutations

abase = base.Base()
startPoint = Point(0,0)
sideLength = 80
trigridRadius = sideLength /  (math.sin(1.0/3*tewpi)*math.sin(1.0/12*tewpi)*4.0)
middleToBaseDistance = trigridRadius*math.sin(1.0/12*tewpi)
centerStart = startPoint - Point(0,trigridRadius)
triangleMidpoints=createTriangleCentreGrid(centerStart, sideLength, 3)
triangleVertices = createTriangularGrid(startPoint, sideLength, 4)
counter = 0
numberPositions = {}
##for permute in range(len(permutationsOfSquare)):
permute = []
#permute = [5,4,7,8,1,6,3,2,9]

#permute = [1,2,3,9,4,6,5,8,7]
#permute = [1,6,5,3,4,8,9,2,7]
# symetry 2 : [5, 4, 3, 8, 9, 6, 7, 2, 1 ]
# symetry 3 : [5, 8, 7, 4, 9, 6, 3, 2, 1]
# symetry 4 : [5, 6, 7, 2, 9, 4, 3, 8, 1]
#symetry 5: [5, 6, 3, 2, 9, 4, 7, 8, 1]
# symetry 6 [5, 6, 3 ,2 , 9, 8, 7, 4, 1]
# symetry 7 [5, 2, 7, 6, 9, 4, 3, 8, 1]
#symetry 8 [5, 2, 7, 6, 9, 8, 3, 4, 1]
#symetry 9 [5, 2, 3, 6, 9, 4, 7, 8, 1]
#symetry 10 [5, 2, 3, 6, 9, 8, 7, 4, 1]
permuteAr = [\
[5, 4, 3, 8, 9, 6, 7, 2, 1 ], \
[5, 4, 3, 8, 9, 2, 7, 6, 1 ], \
[5, 8, 3, 4, 9, 6, 7, 2, 1 ], \
[5, 8, 3, 4, 9, 2, 7, 6, 1 ], \
[5, 2, 7, 6, 9, 8, 3, 4, 1], \
[5, 2, 7, 6, 9, 4, 3, 8, 1], \
[5, 6, 7, 2, 9, 8, 3, 4, 1], \
[5, 6, 7, 2, 9, 4, 3, 8, 1], \
[5, 8, 7, 4, 9, 6, 3, 2, 1], \
[5, 8, 7, 4, 9, 2, 3, 6, 1], \
[5, 4, 7, 8, 9, 6, 3, 2, 1], \
[5, 4, 7, 8, 9, 2, 3, 6, 1], \
[5, 2, 3, 6, 9, 4, 7, 8, 1], \
[5, 2, 3, 6, 9, 8, 7, 4, 1], \
[5, 6, 3, 2, 9, 4, 7, 8, 1], \
[5, 6, 3, 2, 9, 8, 7, 4, 1]
]\




# m1thr0s post : [4, 9, 5, 1, 8, 3, 6, 7, 2 ]
# oak post [

 
def setPermutation(permutation):
    permute = permutation
    counter = 0
    for i in range(3):
        for j in range(i*2+1):
            numberPositions[permute[counter]] = triangleMidpoints[i][j]
            counter += 1
    
setPermutation( [4, 9, 5, 1, 8, 3, 6, 7, 2 ])
def setPermutationFromLeftovers(permutee):
    permute = copy(permutee)
    permute.insert(0, 5)
    permute.insert(4, 9)
    permute.append(1)
    setPermutation(permute)
    
    
def makeAbraGrid(abase):
    levels = 4
    tetractysArray = []
    abraGroup = abase.dok.xml_element(u'g')
    apexArray = []
    apexArray.append(startPoint)
    tetractysArray.append(apexArray)
    
    #create array of the grid with each level being an array of points [[pt1], [pt2, pt3], [pt4, pt5, pt6]....]
    for i in range(1,levels):
        tetractysArray.append([])
        
        for j in range(i):
            overarchPoint = tetractysArray[-2][j]
            leftRef = overarchPoint + Point(-10, 0)
            
            tetractysArray[-1].append(extendBendPoint(leftRef, overarchPoint, sideLength, 1.0/3.0))   
            
        tetractysArray[-1].append(extendBendPoint( tetractysArray[-2][-1] + Point(-10 ,0) ,tetractysArray[-2][-1], sideLength,1.0/6.0))
    
    numTriangles = (levels+1)/3
    
    upTriangles = abase.dok.xml_element(u'g')
    for i in range(levels-1):
        for j in range(i+1):
            triangulatePath = PathData()
            apex = tetractysArray[i][j]
            leftBase = tetractysArray[i+1][j]
            rightBase = tetractysArray[i+1][j+1]
            triangulatePath.moveTo(apex).lineTo(leftBase).lineTo(rightBase).closePath()
            upTriangles.xml_append(buildPath(abase, triangulatePath, attributes={u'style':u'fill:none;stroke:black;stroke-width:1; fill-opacity:0.3'}))
    abraGroup.xml_append(upTriangles)
    
    downTriangles = abase.dok.xml_element(u'g')
    for i in range(1, levels-1):
        for j in range(i):
            triangulatePath = PathData()
            leftArm = tetractysArray[i][j]
            rightArm = tetractysArray[i][j+1]
            balance = tetractysArray[i+1][j+1]
            triangulatePath.moveTo(leftArm).lineTo(rightArm).lineTo(balance).closePath()
            downTriangles.xml_append(buildPath(abase, triangulatePath, attributes={u'style':u'fill:none;stroke:black;stroke-width:1; fill-opacity:0.3'}))
    abase.canvas.xml_append(downTriangles)
    contPath = PathData().moveTo(startPoint).lineTo(tetractysArray[-1][0]).lineTo(tetractysArray[-1][-1]).closePath()
    
    return abraGroup
        
        
def makeTetractysPoints(abase):
    tetractysPointsGroup  = abase.dok.xml_element(u'g')
    for i in range(len(triangleVertices)):
        for j in range(len(triangleVertices[i])):
            tetractysPointsGroup.xml_append(buildCircle(abase, triangleVertices[i][j], 10, attributes = {u'fill':u'black', u'stroke':u'black'}))
    return tetractysPointsGroup

def makeBigrams(abase):
   
        #bigram placement
    ##permutationsOfSquare = permutations.xpermutations(range(1,10))
    
    trigramGroup= abase.dok.xml_element(u'g')
    
    for i in range(1,10):
        trigramGroup.xml_append(trigramaton.digramCentred(abase, i, numberPositions[i], 30))
        
    return trigramGroup

def makeGroupings(abase):    
    groupingsGroup = abase.dok.xml_element(u'g')
    groupings = ( (6,1,8), (7,5,3),(2,9,4),(6,7,2),(1,5,9), (8,3,4), (6,5,4), (8,5,2)  )
    colorCodings = ('black', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'gold')
    #colorCodings = ('red', 'red', 'red','blue', 'black', 'green' ,'yellow', 'yellow')
    widthArray = [i*0.5 for i in range(1,11) ]
                       
    for groupingNum in range(len(groupings)):
        
        connectionPath = PathData().moveTo(numberPositions[groupings[groupingNum][0]])
        for member in groupings[groupingNum]:
            connectionPath.lineTo(numberPositions[member])  
        connectionPath.closePath()
        groupingsGroup.xml_append(buildPath(abase, connectionPath, attributes = {u'stroke':unicode(colorCodings[groupingNum]),u'stroke-width':u'5', u'stroke-opacity':u'0.3', u'fill':u'none'}))
    return groupingsGroup

def makeTraceGroupings(abase):    
    groupingsGroup = abase.dok.xml_element(u'g')
    groupings = ( (6,1,8), (7,5,3),(2,9,4),(6,7,2),(1,5,9), (8,3,4), (6,5,4), (8,5,2)  )
       
    for groupingNum in range(len(groupings)):
        
        connectionPath = PathData().moveTo(numberPositions[groupings[groupingNum][0]])
        for member in groupings[groupingNum]:
            connectionPath.lineTo(numberPositions[member])  
        connectionPath.closePath()
        groupingsGroup.xml_append(buildPath(abase, connectionPath, attributes = {u'stroke':u'black',u'stroke-width':u'4', u'stroke-opacity':u'0.8', u'fill':u'none'}))
    return groupingsGroup
    
def makeCronoPath(abase):
    cronoPath = PathData().moveTo(numberPositions[1])
    for i in range(2,10):
        cronoPath.lineTo(numberPositions[i])
    cronoPath.closePath()
    return buildPath(abase, cronoPath, attributes={u'style':u'fill:none;stroke:black;stroke-width:5; stroke-opacity:0.5'})
    
def generatePossibilities():
    leftovers = [4,7,8,6,3,2]
    possiblePermutations = permutations.xpermutations(leftovers)
    print possiblePermutations
    counter = 0
    for permutation in possiblePermutations:
        setPermutationFromLeftovers(permutation)
        abase = base.Base()
        abase.appendElement(makeAbraGrid(abase))
        abase.appendElement(makeTetractysPoints(abase))
        abase.appendElement(makeBigrams(abase) )
        #abase.appendElement(makeTraceGroupings(abase) )
        abase.appendElement(makeCronoPath(abase))
        abase.writeSVG('abrachamb/abrachambersAr' + str(counter).zfill(3) +'.svg')
        counter += 1

def generateDefinedPossibilities():
    
    counter = 0
    for permutation in permuteAr:
        setPermutation(permutation)
        abase = base.Base()
        abase.appendElement(makeAbraGrid(abase))
        abase.appendElement(makeTetractysPoints(abase))
        abase.appendElement(makeBigrams(abase) )
        abase.appendElement(makeGroupings(abase) )
        abase.appendElement(makeTraceGroupings(abase) )
        
        #abase.appendElement(makeCronoPath(abase))
        #abase.appendElement(makeCronoPath(abase))
        abase.writeSVG('abrachamba/abrachambersAr' + str(counter).zfill(3) +'.svg')
        counter += 1

def generateOnePossibility():
    abase.appendElement(makeAbraGrid(abase))
    abase.appendElement(makeTetractysPoints(abase))
    abase.appendElement(makeBigrams(abase) )
    abase.appendElement(makeGroupings(abase) )
    abase.appendElement(makeCronoPath(abase))
    abase.writeSVG('abrachambersAr_M10.svg')
#generateOnePossibility()
generatePossibilities()
#generateDefinedPossibilities()
print "done01"

