from playsvg import document
from playsvg.path import *
from playsvg.geom import *
from playsvg.element import *

def lotusPetalFlower(petals, baseRadius, tipRadius, ctrlDistanceRatio, spacingFract):
    """a flower shape similar to the lotus flower mandalas in Hindu/Yogic iconography"""
    lotusGroup = buildGroup(id="lotus")
    petalSpaceFraction = 1.0/petals
    spacingAngal = spacingFract*petalSpaceFraction
    petalFraction = petalSpaceFraction - 2*spacingAngal
    petalWidth = tipRadius - baseRadius
    pathData = PathData()
    pathData.moveTo(Point().polerInit(baseRadius,spacingAngal))
    for i in range(petals):
        pathData = PathData()
        startPoint = Point().polerInit(baseRadius,i*petalSpaceFraction + spacingAngal)
        pathData.moveTo(startPoint)
        ctrlPt1 = Point().polerInit(baseRadius+petalWidth*ctrlDistanceRatio, i*petalSpaceFraction+spacingAngal)
        
        tipPoint = Point().polerInit(tipRadius, (i+0.5)*petalSpaceFraction) 
        ctrlPt2 = Point().polerInit(baseRadius+petalWidth*(1-ctrlDistanceRatio), (i+0.5)*petalSpaceFraction)
        
        endPoint = Point().polerInit(baseRadius,(i+0.5)*petalSpaceFraction + petalFraction/2)
        ctrlPt3 = Point().polerInit(baseRadius+petalWidth*ctrlDistanceRatio, (i+0.5)*petalSpaceFraction + petalFraction/2)
        pathData.cubicBezier(ctrlPt1,ctrlPt2, tipPoint)
        pathData.cubicBezier(ctrlPt2, ctrlPt3, endPoint)
        pathData.SCRVBD((0.25,-1.0/32), startPoint )
        lotusGroup.append(buildPath(pathData))
        
    return lotusGroup 

docu = document.Document()
docu.append(lotusPetalFlower(16, 400, 475, 0.8, 0.0625))
docu.writeSVG('lotusFlowerSpacedPetals.svg')

