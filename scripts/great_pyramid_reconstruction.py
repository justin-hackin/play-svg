from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg.geom import *


ln = 115.0544
le = 115.1761
ls = 115.1828
lw = 115.3201

rn = 115.2014
re = 115.2183
rs = 115.2739
rw = 115.0397

nap=185.9205
eap=185.8088
sap=185.7585
wap=185.8368

ndtc=114.7261
edtc=114.5449
sdtc=114.4634
wdtc=114.5904

nw=163.0012
ne=162.8968
se=162.8668
sw=162.8019

nnw=219.0291
nne=218.9514
sse=218.9291
ssw=218.8809

def pairUpperToLower(points):
    if (len(points) != 2 ): raise Exception("pair length not 2, it's "+ len(points))
    else: 
        if points[0].y > points[1].y : return points
        else : return [points[1], points[0] ]   

def pairLeftToRight(points):
    if (len(points) != 2 ): raise Exception("pair length not 2, it's "+ len(points))
    else: 
        if points[0].x < points[1].x : return points
        else : return [points[1], points[0] ]   
        
def intersectCircleCircleLR(c1c, c1r, c2c, c2r):
    return pairLeftToRight(intersectCircleCircle(c1c, c1r, c2c, c2r))

def intersectCircleCircleUD(c1c, c1r, c2c, c2r):
    return pairUpperToLower(intersectCircleCircle(c1c, c1r, c2c, c2r))
#search: (\w+)(\=.+\n)
#replace: $1$2print \"$1\ = \"  \+ $1\.strOnPlane\(\)\+\"\;\"\n
center=Point(0,0)
faceSpace = 400
nCenter=center+Point(0,ndtc)
print "nCenter = "  + nCenter.strOnPlane()+";"
neCorner=intersectCircleCircleLR(center, ne, nCenter, ln)[1]
print "neCorner = "  + neCorner.strOnPlane()+";"
eCenter=intersectCircleCircleUD(neCorner, re, center, edtc)[1]
print "eCenter = "  + eCenter.strOnPlane()+";"
seCorner=intersectCircleCircleUD(center, se, eCenter, le)[1]
print "seCorner = "  + seCorner.strOnPlane()+";"
sCenter=intersectCircleCircleUD(seCorner, rs, center, sdtc)[1]
print "sCenter = "  + sCenter.strOnPlane()+";"
swCorner=intersectCircleCircleLR(center, sw, sCenter, ls)[0]     
print "swCorner = "  + swCorner.strOnPlane()+";"
wCenter=intersectCircleCircleUD(swCorner, rw, center, wdtc)[0]
print "wCenter = "  + wCenter.strOnPlane()+";"
nwCorner=intersectCircleCircleUD(center, nw, wCenter, lw)[0]
print "nwCorner = "  + nwCorner.strOnPlane()+";"
napApex=center+Point(0,faceSpace)
napBase=napApex-Point(0,nap)
rnCorner=intersectCircleCircleLR(napBase, rn, napApex, nnw)[0]
lnCorner=intersectCircleCircleLR(napBase, ln, napApex, nne)[1]
eapApex=center+Point(faceSpace,0)
eapBase=eapApex-Point(eap,0)
reCorner=intersectCircleCircleUD(eapBase, re, eapApex, nne)[0]
leCorner=intersectCircleCircleUD(eapBase, ln, eapApex, sse)[1]
sapApex=center-Point(0, faceSpace)
sapBase=sapApex+Point(0, sap)
rsCorner=intersectCircleCircleLR(sapBase, rs, sapApex, sse)[1]
lsCorner=intersectCircleCircleLR(sapBase, ls, sapApex, ssw)[0]
wapApex=center-Point(faceSpace, 0)
wapBase=wapApex+Point(wap,0)
rwCorner=intersectCircleCircleUD(wapBase, rw, wapApex, ssw)[1]
lwCorner=intersectCircleCircleUD(wapBase, lw, wapApex, nnw)[0]

cutStyle =  {'style':' stroke:blue ;fill:blue; fill-opacity:0'}
scoreStyle =  {'style':' stroke:red ;fill:red; fill-opacity:0'}

docu = Document(gridSize=900)

basePathOuter = PathData().moveTo(nCenter).lineTo(neCorner).lineTo(eCenter).lineTo(seCorner).lineTo(sCenter).lineTo(swCorner).lineTo(wCenter).lineTo(nwCorner).lineTo(nCenter)
basePathInner = deepcopy(basePathOuter)
basePathInner.transformPoints(lambda x : x.getMultiple(phi - 1))

baseLines = etree.Element("g")
baseLines.append(buildPath(basePathOuter,cutStyle ))
baseLines.append(buildPath(basePathInner,cutStyle ))
docu.append(baseLines)

northFace = PathData().makeHull([napApex, rnCorner, napBase, lnCorner])
northScore = PathData().moveTo(napApex).lineTo(napBase)
northLines = etree.Element("g")
northLines.append(buildPath(northFace,cutStyle ))
northLines.append(buildPath(northScore,scoreStyle ))
docu.append(northLines)

eastFace = PathData().makeHull([eapApex, reCorner, eapBase, leCorner])
eastScore = PathData().moveTo(eapApex).lineTo(eapBase)
eastLines = etree.Element("g")
eastLines.append(buildPath(eastFace,cutStyle ))
eastLines.append(buildPath(eastScore,scoreStyle ))
docu.append(eastLines)

southFace = PathData().makeHull([sapApex, rsCorner, sapBase, lsCorner])
southScore = PathData().moveTo(sapApex).lineTo(sapBase)
southLines = etree.Element("g")
southLines.append(buildPath(southFace,cutStyle ))
southLines.append(buildPath(southScore,scoreStyle ))
docu.append(southLines)

westFace = PathData().makeHull([wapApex, rwCorner, wapBase, lwCorner])
westScore = PathData().moveTo(wapApex).lineTo(wapBase)
westLines = etree.Element("g")
westLines.append(buildPath(westFace,cutStyle ))
westLines.append(buildPath(westScore,scoreStyle ))
docu.append(westLines)


docu.writeSVG("great_pyramid_reconstruction.svg")
