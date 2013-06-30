from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string

def inchesToPx(inches):
    return inches*90

def cmToPx(cm):
    return cm*90/2.54
    
def initializeVariables(l, w, h, g, h1, k4, kr, bottomDustFlapGap, topDustFlapGap, x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c):
    global frontTopLeft
    frontTopLeft = Point(0,0)
    
    global frontTopRight
    frontTopRight = Point(w, 0)
    
    global frontBottomLeft
    frontBottomLeft = Point(0, h*-1)
    
    global frontBottomRight
    frontBottomRight = Point(w, h*-1)
    
    global leftTopLeft 
    leftTopLeft = frontTopLeft+Point(-1*l, 0) 
    
    global leftBottomLeft
    leftBottomLeft = frontBottomLeft+Point(-1*l, 0) 
    
    global backTopLeft
    backTopLeft = leftTopLeft + Point(-1*w, 0) 
    
    global backBottomLeft
    backBottomLeft = leftBottomLeft + Point(-1*w, 0) 
    
    global rightTopRight 
    rightTopRight = frontTopRight + Point(l, 0) 
    
    global rightBottomRight 
    rightBottomRight = frontBottomRight + Point(l, 0) 
    
    global glueTabEdgeTop 
    glueTabEdgeTop = backTopLeft + Point(-1*g, -1*g)
    
    global glueTabEdgeBottom 
    glueTabEdgeBottom = backBottomLeft + Point(-1*g, g)
    
    global glueTab2EdgeTop 
    glueTab2EdgeTop = frontTopLeft + Point(g, -1*g)
    
    global glueTab2EdgeBottom 
    glueTab2EdgeBottom = frontBottomLeft + Point(g, g)
    
    global backBottomFlapLeftTop
    backBottomFlapLeftTop = backBottomLeft + Point(h1, -1*l/2 )
    
    global backBottomFlapLeftBottom
    backBottomFlapLeftBottom = backBottomFlapLeftTop + Point(0,-1*k4)
    
    global backBottomFlapLeftBottomStart 
    backBottomFlapLeftBottomStart = backBottomFlapLeftBottom + Point(0, kr)
    
    global backBottomFlapLeftBottomEnd
    backBottomFlapLeftBottomEnd = backBottomFlapLeftBottom + Point(kr, 0)
    
    
    global backBottomFlapRightTop 
    backBottomFlapRightTop = leftBottomLeft + Point(-1*h1, -1*l/2 )
    
    global backBottomFlapRightBottom 
    backBottomFlapRightBottom = backBottomFlapRightTop + Point(0,-1*k4)
    
#    global backBottomFlapRightBottomStart
#    backBottomFlapRightBottomStart = backBottomFlapRightBottom + Point(0, kr)
#    
#    global backBottomFlapRightBottomEnd
#    backBottomFlapRightBottomEnd = backBottomFlapRightBottom + Point(-1*kr, 0)
    
    global leftBottomFlapLeftBottom
    leftBottomFlapLeftBottom = leftBottomLeft + Point(0, -1*w/2 + bottomDustFlapGap)
    
    
    global leftBottomFlapRightBottom 
    leftBottomFlapRightBottom =  leftBottomFlapLeftBottom + Point(l/2, 0)
    
    #leftBottomFlapRightBottomStart = leftBottomFlapRightBottom + Point(-1*kr, 0)
    #leftBottomFlapRightBottomEnd = leftBottomFlapRightBottom + Point(0, kr)
    global leftBottomFlapRightTop
    leftBottomFlapRightTop = leftBottomFlapRightBottom + Point(0, (w-h1*2)/2-bottomDustFlapGap)
    
    global rightBottomFlapRightBottom 
    rightBottomFlapRightBottom = rightBottomRight + Point(0, -1*w/2 + bottomDustFlapGap)
    
    global rightBottomFlapLeftBottom 
    rightBottomFlapLeftBottom = rightBottomFlapRightBottom + Point(-1*l/2, 0)
    
    global rightBottomFlapLeftTop 
    rightBottomFlapLeftTop = rightBottomFlapLeftBottom + Point(0, (w-h1*2)/2-bottomDustFlapGap)
    
    global frontBottomFlapLeftBottom
    frontBottomFlapLeftBottom = frontBottomLeft + Point(0,-1*(l/2+k4))

    global frontBottomFlapLeftBottomRight
    frontBottomFlapLeftBottomRight = frontBottomFlapLeftBottom + Point(h1, 0)

    global frontBottomFlapLeftBottomRightTop
    frontBottomFlapLeftBottomRightTop = frontBottomFlapLeftBottomRight + Point(0,k4)
    
    
    global frontBottomFlapRightBottom 
    frontBottomFlapRightBottom = frontBottomRight + Point(0,-1*(l/2+k4))

    global frontBottomFlapRightBottomLeft
    frontBottomFlapRightBottomLeft = frontBottomFlapRightBottom + Point(-1*h1, 0)

    global frontBottomFlapRightBottomLeftTop 
    frontBottomFlapRightBottomLeftTop = frontBottomFlapRightBottomLeft + Point(0,k4)
    
    global leftTopFlapLeftBottom
    leftTopFlapLeftBottom = leftTopLeft+Point(x2,0)

    global leftTopFlapLeftMid1 
    leftTopFlapLeftMid1 = leftTopFlapLeftBottom + Point(0,s2)

    global leftTopFlapLeftMid2
    leftTopFlapLeftMid2 = leftTopFlapLeftMid1 + Point(n,n)

    global leftTopFlapLeftTop 
    leftTopFlapLeftTop = leftTopFlapLeftBottom  + Point(t2,w/2-topDustFlapGap)

    global leftTopFlapRightBottom
    leftTopFlapRightBottom = frontTopLeft+Point(-1*x3,0)

    global leftTopFlapRightTop 
    leftTopFlapRightTop = leftTopFlapRightBottom + Point(0,w/2-topDustFlapGap)
    
    global rightTopFlapRightBottom 
    rightTopFlapRightBottom = rightTopRight+Point(-1*x2,0)

    global rightTopFlapRightMid1
    rightTopFlapRightMid1 = rightTopFlapRightBottom + Point(0,s2)

    global rightTopFlapRightMid2
    rightTopFlapRightMid2 = rightTopFlapRightMid1 + Point(-1*n,n)

    global rightTopFlapRightTop 
    rightTopFlapRightTop = rightTopFlapRightBottom  + Point(-1*t2,w/2-topDustFlapGap)

    global rightTopFlapLeftBottom 
    rightTopFlapLeftBottom = frontTopRight+Point(x3,0)

    global rightTopFlapLeftTop 
    rightTopFlapLeftTop = rightTopFlapLeftBottom + Point(0,w/2-topDustFlapGap)
     
    global frontTopFlapLeftEdge
    frontTopFlapLeftEdge = frontTopLeft + Point(0,l+overhangTabCloser)
    
    global frontTopFlapRightEdge
    frontTopFlapRightEdge = frontTopRight + Point(0,l+overhangTabCloser)
    
    global frontTopFlapLeftEdgeIn 
    frontTopFlapLeftEdgeIn = frontTopFlapLeftEdge + Point(e,0)

    global frontTopFlapRightEdgeIn 
    frontTopFlapRightEdgeIn = frontTopFlapRightEdge + Point(-1*e,0)
    
    global frontTopFlapLeftEdgeInDown 
    frontTopFlapLeftEdgeInDown = frontTopFlapLeftEdgeIn + Point(0, -2*overhangTabCloser)

    global frontTopFlapRightEdgeInDown 
    frontTopFlapRightEdgeInDown = frontTopFlapRightEdgeIn + Point(0, -2*overhangTabCloser)
    
    global frontTopFlapLeftEdgeInFold 
    frontTopFlapLeftEdgeInFold = frontTopFlapLeftEdgeIn + Point(0, -1*overhangTabCloser)

    global frontTopFlapRightEdgeInFold 
    frontTopFlapRightEdgeInFold = frontTopFlapRightEdgeIn + Point(0, -1*overhangTabCloser)
    
    global frontTopFlapLeftTabStart 
    frontTopFlapLeftTabStart = frontTopFlapLeftEdge + Point(overhangTabCloser, 0)

    global frontTopFlapRightTabStart 
    frontTopFlapRightTabStart = frontTopFlapRightEdge + Point( -1*overhangTabCloser, 0)
    
    global frontTopFlapLeftTabMid 
    frontTopFlapLeftTabMid = frontTopFlapLeftTabStart + Point(0, c-cr)

    global frontTopFlapRightTabMid 
    frontTopFlapRightTabMid = frontTopFlapRightTabStart+ Point(0, c-cr)
    
    global frontTopFlapLeftTabTop 
    frontTopFlapLeftTabTop = frontTopFlapLeftTabMid + Point(cr, cr)

    global frontTopFlapRightTabTop 
    frontTopFlapRightTabTop = frontTopFlapRightTabMid + Point(-1*cr, cr)
    

def makeBox(plotTestPoints=False, plotOverlaps=0, glueTab=False, twoPart=False, ):    
    if (not twoPart):
        cutLines = etree.Element("g")
        pathStyle =  {'style':' stroke:blue ;fill:blue; fill-opacity:0'}
        cutPaths = []
        cutPaths.append(PathData().moveTo(frontTopLeft).lineTo(frontTopFlapLeftEdge))
        cutPaths.append(PathData().moveTo(frontTopRight).lineTo(frontTopFlapRightEdge))
        cutPaths.append(PathData().moveTo(frontTopFlapLeftEdge).lineTo(frontTopFlapLeftEdgeIn).lineTo(frontTopFlapLeftEdgeInDown))
        cutPaths.append(PathData().moveTo(frontTopFlapRightEdge).lineTo(frontTopFlapRightEdgeIn).lineTo(frontTopFlapRightEdgeInDown))
        cutPaths.append(PathData().moveTo(frontTopFlapLeftTabStart).
                                  lineTo(frontTopFlapLeftTabMid).
                                  cubicBezier(frontTopFlapLeftTabMid+Point(0,cr/2),frontTopFlapLeftTabTop+Point(cr/-2,0), frontTopFlapLeftTabTop  )
                                  .lineTo(frontTopFlapRightTabTop).cubicBezier(frontTopFlapRightTabTop+Point(cr/2,0), frontTopFlapRightTabMid+Point(0,cr), frontTopFlapRightTabMid ).lineTo(frontTopFlapRightTabStart) )
        cutPaths.append(PathData().moveTo(frontTopRight).
                                  cubicBezier(frontTopRight-Point(0, x3),rightTopFlapLeftBottom-Point(0,x3), rightTopFlapLeftBottom ).                          
                                  lineTo(rightTopFlapLeftTop).
                                  lineTo(rightTopFlapRightTop).
                                  lineTo(rightTopFlapRightMid2).lineTo(rightTopFlapRightMid1).
                                  lineTo(rightTopFlapRightBottom).
                                  lineTo(rightTopRight))
        cutPaths.append(PathData().moveTo(rightTopRight).
                  lineTo(rightBottomRight).
                  lineTo(rightBottomFlapRightBottom).
                  lineTo(rightBottomFlapLeftBottom).
                  lineTo(rightBottomFlapLeftTop).
                  lineTo(frontBottomRight))
        cutPaths.append(PathData().moveTo(frontBottomRight).
                  lineTo(frontBottomFlapRightBottom).
                  lineTo(frontBottomFlapRightBottomLeft).
                  lineTo(frontBottomFlapRightBottomLeftTop).
                  lineTo(frontBottomFlapLeftBottomRightTop).
                  lineTo(frontBottomFlapLeftBottomRight).
                  lineTo(frontBottomFlapLeftBottom).
                  lineTo(frontBottomLeft))
        cutPaths.append(PathData().moveTo(frontBottomLeft).
                  lineTo(leftBottomFlapRightTop).
                  lineTo(leftBottomFlapRightBottom).
                  lineTo(leftBottomFlapLeftBottom).
                  lineTo(leftBottomLeft))
        cutPaths.append(PathData().moveTo(leftBottomLeft).
                  lineTo(backBottomFlapRightTop).
                  lineTo(backBottomFlapRightBottom).
                  lineTo(backBottomFlapLeftBottom).
                  lineTo(backBottomFlapLeftTop).
                  lineTo(backBottomLeft))
        if (glueTab): 
            cutPaths.append(PathData().moveTo(backBottomLeft).
                      lineTo(glueTabEdgeBottom).
                      lineTo(glueTabEdgeTop).
                      lineTo(backTopLeft))
        else:
            cutPaths.append(PathData().moveTo(backBottomLeft).lineTo(backTopLeft))
            
            
        cutPaths.append(PathData().moveTo(backTopLeft).
                  lineTo(leftTopLeft))
        
        cutPaths.append(PathData().moveTo(leftTopLeft).                                                   
                                  lineTo( leftTopFlapLeftBottom).
                                  lineTo(leftTopFlapLeftMid1).
                                  lineTo(leftTopFlapLeftMid2).
                                  lineTo(leftTopFlapLeftTop).
                                  lineTo(leftTopFlapRightTop).
                                  lineTo(leftTopFlapRightBottom).
                                  cubicBezier(leftTopFlapRightBottom-Point(0,x3), frontTopLeft-Point(0,x3), frontTopLeft))
        for cutPath in cutPaths:
            if plotOverlaps : cutPath.backAndForth(plotOverlaps)
            cutLines.append(buildPath(cutPath,pathStyle ))
        
    
    #   
        docu.append(cutLines)
        
        scoreLines = etree.Element("g")
        pathStyle =  {'style':' stroke:red ;fill:red;fill-opacity:0'}
        
        scoreLines.append(buildPath(PathData().moveTo(rightTopFlapLeftBottom).lineTo(rightTopFlapRightBottom),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(rightBottomRight),pathStyle ))
        
        scoreLines.append(buildPath(PathData().moveTo(frontTopFlapLeftEdgeInFold).lineTo(frontTopFlapRightEdgeInFold),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(frontTopLeft).lineTo(frontTopRight),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(frontBottomLeft),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(frontBottomLeft),pathStyle ))
        
        scoreLines.append(buildPath(PathData().moveTo(leftTopFlapLeftBottom).lineTo(leftTopFlapRightBottom),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(frontBottomLeft).lineTo(leftBottomLeft),pathStyle ))
        
        scoreLines.append(buildPath(PathData().moveTo(leftBottomLeft).lineTo(backBottomLeft),pathStyle ))
    
    
        if (glueTab):
            scoreLines.append(buildPath(PathData().moveTo(backBottomLeft).lineTo(backTopLeft),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(leftTopLeft).lineTo(leftBottomLeft),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(frontBottomLeft).lineTo(frontTopLeft),pathStyle ))
        scoreLines.append(buildPath(PathData().moveTo(frontTopRight).lineTo(frontBottomRight),pathStyle ))
        docu.append(scoreLines)
    
    # ************************************TWO PART BOX**************************************** 
    else:
        cutLines1 = etree.Element("g")
        cutLines2 = etree.Element("g")
        pathStyle =  {'style':' stroke:blue ;fill:blue; fill-opacity:0'}
        cutPaths1 = []
        cutPaths2 = []
        
        cutPaths1.append(PathData().moveTo(frontBottomLeft).lineTo(frontTopLeft))
        cutPaths1.append(PathData().moveTo(frontTopLeft).lineTo(frontTopFlapLeftEdge))
        cutPaths1.append(PathData().moveTo(frontTopFlapLeftEdge).lineTo(frontTopFlapLeftEdgeIn).lineTo(frontTopFlapLeftEdgeInDown))
        cutPaths1.append(PathData().moveTo(frontTopFlapLeftTabStart).
                                  lineTo(frontTopFlapLeftTabMid).
                                  cubicBezier(frontTopFlapLeftTabMid+Point(0,cr/2),frontTopFlapLeftTabTop+Point(cr/-2,0), frontTopFlapLeftTabTop  )
                                  .lineTo(frontTopFlapRightTabTop).cubicBezier(frontTopFlapRightTabTop+Point(cr/2,0), frontTopFlapRightTabMid+Point(0,cr), frontTopFlapRightTabMid ).lineTo(frontTopFlapRightTabStart) )
        cutPaths1.append(PathData().moveTo(frontTopFlapRightEdge).lineTo(frontTopFlapRightEdgeIn).lineTo(frontTopFlapRightEdgeInDown))
        cutPaths1.append(PathData().moveTo(frontTopRight).lineTo(frontTopFlapRightEdge))
               
        cutPaths1.append(PathData().moveTo(frontTopRight).
                                  cubicBezier(frontTopRight-Point(0, x3),rightTopFlapLeftBottom-Point(0,x3), rightTopFlapLeftBottom ).                          
                                  lineTo(rightTopFlapLeftTop).
                                  lineTo(rightTopFlapRightTop).
                                  lineTo(rightTopFlapRightMid2).
                                  lineTo(rightTopFlapRightMid1).
                                  lineTo(rightTopFlapRightBottom).
                                  lineTo(rightTopRight))
        
        
        cutPaths1.append(PathData().moveTo(rightTopRight).lineTo(rightBottomRight))
        
        
        
        cutPaths1.append(PathData().moveTo(rightBottomRight).          
                  lineTo(rightBottomFlapRightBottom).
                  lineTo(rightBottomFlapLeftBottom).
                  lineTo(rightBottomFlapLeftTop).
                  lineTo(frontBottomRight))
        
        cutPaths1.append(PathData().moveTo(frontBottomRight).
                  lineTo(frontBottomFlapRightBottom).
                  lineTo(frontBottomFlapRightBottomLeft).
                  lineTo(frontBottomFlapRightBottomLeftTop).
                  lineTo(frontBottomFlapLeftBottomRightTop).
                  lineTo(frontBottomFlapLeftBottomRight).
                  lineTo(frontBottomFlapLeftBottom).
                  lineTo(frontBottomLeft))
       
        
        
          
        cutPaths2.append(PathData().moveTo(frontBottomLeft).
                  lineTo(leftBottomFlapRightTop).
                  lineTo(leftBottomFlapRightBottom).
                  lineTo(leftBottomFlapLeftBottom).
                  lineTo(leftBottomLeft))
        cutPaths2.append(PathData().moveTo(leftBottomLeft).
                  lineTo(backBottomFlapRightTop).
                  lineTo(backBottomFlapRightBottom).
                  lineTo(backBottomFlapLeftBottom).
                  lineTo(backBottomFlapLeftTop).
                  lineTo(backBottomLeft))
        if (glueTab): 
            cutPaths2.append(PathData().moveTo(backBottomLeft).
                      lineTo(glueTabEdgeBottom).
                      lineTo(glueTabEdgeTop).
                      lineTo(backTopLeft))
            cutPaths2.append(PathData().moveTo(frontBottomLeft).
                      lineTo(glueTab2EdgeBottom).
                      lineTo(glueTab2EdgeTop).
                      lineTo(frontTopLeft))
            
        else:
            cutPaths2.append(PathData().moveTo(backBottomLeft).lineTo(backTopLeft))
            cutPaths2.append(PathData().moveTo(frontBottomLeft).lineTo(frontTopLeft))
            
            
        cutPaths2.append(PathData().moveTo(backTopLeft).
                  lineTo(leftTopLeft))
        
        cutPaths2.append(PathData().moveTo(leftTopLeft).                                                   
                                  lineTo( leftTopFlapLeftBottom).
                                  lineTo(leftTopFlapLeftMid1).
                                  lineTo(leftTopFlapLeftTop).
                                  lineTo(leftTopFlapRightTop).
                                  lineTo(leftTopFlapRightBottom).
                                  cubicBezier(leftTopFlapRightBottom-Point(0,x3), frontTopLeft-Point(0,x3), frontTopLeft))
        for cutPath in cutPaths1:
            if plotOverlaps : cutPath.backAndForth(plotOverlaps)
            cutLines1.append(buildPath(cutPath,pathStyle ))
        for cutPath in cutPaths2:
            if plotOverlaps : cutPath.backAndForth(plotOverlaps)
            cutLines2.append(buildPath(cutPath,pathStyle ))
        
        scoreLines1 = etree.Element("g")
        scoreLines2 = etree.Element("g")
        pathStyle =  {'style':' stroke:red ;fill:red;fill-opacity:0'}
        
        scoreLines1.append(buildPath(PathData().moveTo(rightTopFlapLeftBottom).lineTo(rightTopFlapRightBottom),pathStyle ))
        scoreLines1.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(rightBottomRight),pathStyle ))
        
        scoreLines1.append(buildPath(PathData().moveTo(frontTopFlapLeftEdgeInFold).lineTo(frontTopFlapRightEdgeInFold),pathStyle ))
        scoreLines1.append(buildPath(PathData().moveTo(frontTopLeft).lineTo(frontTopRight),pathStyle ))
        scoreLines1.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(frontBottomLeft),pathStyle ))
        scoreLines1.append(buildPath(PathData().moveTo(frontTopRight).lineTo(frontBottomRight),pathStyle ))
        
        
        scoreLines2.append(buildPath(PathData().moveTo(leftTopFlapLeftBottom).lineTo(leftTopFlapRightBottom),pathStyle ))
        scoreLines2.append(buildPath(PathData().moveTo(frontBottomLeft).lineTo(leftBottomLeft),pathStyle ))
        
        scoreLines2.append(buildPath(PathData().moveTo(leftBottomLeft).lineTo(backBottomLeft),pathStyle ))
    
    
        if (glueTab):
            scoreLines2.append(buildPath(PathData().moveTo(backBottomLeft).lineTo(backTopLeft),pathStyle ))
            scoreLines2.append(buildPath(PathData().moveTo(frontTopLeft).lineTo(frontBottomLeft),pathStyle ))
        
        scoreLines2.append(buildPath(PathData().moveTo(leftTopLeft).lineTo(leftBottomLeft),pathStyle ))  
        
        return [cutLines1, scoreLines1, cutLines2, scoreLines2]
   
    
    def drawTestPoints():
        tr = 1
        testPoints = etree.Element("g")
        
        testPoints.append(buildCircle( frontTopLeft, tr, {'style':' stroke:none ;fill:black'}))
        testPoints.append(buildCircle( frontTopRight, tr, {'style':' stroke:none ;fill:blue'}))
        testPoints.append(buildCircle( frontBottomLeft, tr, {'style':' stroke:none ;fill:red'}))
        testPoints.append(buildCircle( frontBottomRight, tr, {'style':' stroke:none ;fill:green'}))
        testPoints.append(buildCircle( leftTopLeft, tr, {'style':' stroke:none ;fill:purple'}))
        testPoints.append(buildCircle( leftBottomLeft, tr, {'style':' stroke:none ;fill:magenta'}))
        testPoints.append(buildCircle( backTopLeft, tr, {'style':' stroke:none ;fill:Indigo'}))
        testPoints.append(buildCircle( backBottomLeft, tr, {'style':' stroke:none ;fill:LightGreen'}))
        testPoints.append(buildCircle( rightTopRight, tr, {'style':' stroke:none ;fill:cyan'}))
        testPoints.append(buildCircle( rightBottomRight, tr, {'style':' stroke:none ;fill:HotPink'}))
        testPoints.append(buildCircle( glueTabEdgeTop, tr, {'style':' stroke:none ;fill:LightSeaGreen'}))
        testPoints.append(buildCircle( glueTabEdgeBottom, tr, {'style':' stroke:none ;fill:Lime'}))
        testPoints.append(buildCircle( backBottomFlapLeftTop, tr, {'style':' stroke:none ;fill:Navy'}))
        testPoints.append(buildCircle( backBottomFlapLeftBottom, tr, {'style':' stroke:none ;fill:Orange'}))
        #testPoints.append(buildCircle( backBottomFlapLeftBottomStart, tr, {'style':' stroke:none ;fill:Orange'}))
        #testPoints.append(buildCircle( backBottomFlapLeftBottomEnd, tr, {'style':' stroke:none ;fill:OrangeRed'}))
        testPoints.append(buildCircle( backBottomFlapRightTop, tr, {'style':' stroke:none ;fill:Olive'}))
        testPoints.append(buildCircle( backBottomFlapRightBottom, tr, {'style':' stroke:none ;fill:OrangeRed'}))
        testPoints.append(buildCircle( leftBottomFlapRightTop, tr, {'style':' stroke:none ;fill:Orange'}))
        #testPoints.append(buildCircle( backBottomFlapRightBottomStart, tr, {'style':' stroke:none ;fill:OrangeRed'}))
        #testPoints.(buildCircle( backBottomFlapRightBottomEnd, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( leftBottomFlapLeftBottom, tr, {'style':' stroke:none ;fill:PeachPuff'}))
        testPoints.append(buildCircle( leftBottomFlapRightBottom, tr, {'style':' stroke:none ;fill:Yellow'}))
        testPoints.append(buildCircle( rightBottomFlapRightBottom, tr, {'style':' stroke:none ;fill:PeachPuff'}))
        testPoints.append(buildCircle( rightBottomFlapLeftBottom, tr, {'style':' stroke:none ;fill:Yellow'}))
        testPoints.append(buildCircle( rightBottomFlapLeftTop, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( frontBottomFlapLeftBottom, tr, {'style':' stroke:none ;fill:blue'}))
        testPoints.append(buildCircle( frontBottomFlapLeftBottomRight, tr, {'style':' stroke:none ;fill:red'}))
        testPoints.append(buildCircle( frontBottomFlapLeftBottomRightTop, tr, {'style':' stroke:none ;fill:yellow'}))
        testPoints.append(buildCircle( frontBottomFlapRightBottom, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( frontBottomFlapRightBottomLeft, tr, {'style':' stroke:none ;fill:purple'}))
        testPoints.append(buildCircle( frontBottomFlapRightBottomLeftTop, tr, {'style':' stroke:none ;fill:green'}))
        testPoints.append(buildCircle( leftTopFlapLeftBottom, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( leftTopFlapLeftMid1, tr, {'style':' stroke:none ;fill:Orchid'}))
        testPoints.append(buildCircle( leftTopFlapLeftMid2, tr, {'style':' stroke:none ;fill:Maroon'}))
        testPoints.append(buildCircle( leftTopFlapLeftTop, tr, {'style':' stroke:none ;fill:Plum'}))
        testPoints.append(buildCircle( leftTopFlapRightBottom, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( leftTopFlapRightTop, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( rightTopFlapRightBottom, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( rightTopFlapRightMid1, tr, {'style':' stroke:none ;fill:Orchid'}))
        testPoints.append(buildCircle( rightTopFlapRightMid2, tr, {'style':' stroke:none ;fill:Maroon'}))
        testPoints.append(buildCircle( rightTopFlapRightTop, tr, {'style':' stroke:none ;fill:Plum'}))
        testPoints.append(buildCircle( rightTopFlapLeftBottom, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( rightTopFlapLeftTop, tr, {'style':' stroke:none ;fill:Orange'}))
        testPoints.append(buildCircle( frontTopFlapLeftEdge, tr, {'style':' stroke:none ;fill:Turquoise'}))
        testPoints.append(buildCircle( frontTopFlapRightEdge, tr, {'style':' stroke:none ;fill:Turquoise'}))
        testPoints.append(buildCircle( frontTopFlapLeftEdgeIn, tr, {'style':' stroke:none ;fill:SlateBlue'}))
        testPoints.append(buildCircle( frontTopFlapRightEdgeIn, tr, {'style':' stroke:none ;fill:SlateBlue'}))
        testPoints.append(buildCircle( frontTopFlapLeftEdgeInDown, tr, {'style':' stroke:none ;fill:Salmon'}))
        testPoints.append(buildCircle( frontTopFlapRightEdgeInDown, tr, {'style':' stroke:none ;fill:Salmon'}))
        testPoints.append(buildCircle( frontTopFlapLeftEdgeInFold, tr, {'style':' stroke:none ;fill:OliveDrab'}))
        testPoints.append(buildCircle( frontTopFlapRightEdgeInFold, tr, {'style':' stroke:none ;fill:OliveDrab'}))
        testPoints.append(buildCircle( frontTopFlapLeftTabStart, tr, {'style':' stroke:none ;fill:Khaki'}))
        testPoints.append(buildCircle( frontTopFlapRightTabStart, tr, {'style':' stroke:none ;fill:Khaki'}))
        testPoints.append(buildCircle( frontTopFlapLeftTabMid, tr, {'style':' stroke:none ;fill:Khaki'}))
        testPoints.append(buildCircle( frontTopFlapRightTabMid, tr, {'style':' stroke:none ;fill:Khaki'}))
        testPoints.append(buildCircle( frontTopFlapLeftTabTop, tr, {'style':' stroke:none ;fill:HotPink'}))
        testPoints.append(buildCircle( frontTopFlapRightTabTop, tr, {'style':' stroke:none ;fill:HotPink'}))
        return testPoints
    if plotTestPoints : docu.append(drawTestPoints())

#def drawBoxConnected(docu, l, w, h, g, h1, k4, kr, bottomDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c, plotTestPoints=False):
#
#    frontTopLeft = Point(0,0)
#    frontTopRight = Point(w, 0)
#    frontBottomLeft = Point(0, h*-1)
#    frontBottomRight = Point(w, h*-1)
#    leftTopLeft = frontTopLeft+Point(-1*l, 0) 
#    leftBottomLeft = frontBottomLeft+Point(-1*l, 0) 
#    
#    backTopLeft = leftTopLeft + Point(-1*w, 0) 
#    
#    backBottomLeft = leftBottomLeft + Point(-1*w, 0) 
#    
#    
#    rightTopRight = frontTopRight + Point(l, 0) 
#    rightBottomRight = frontBottomRight + Point(l, 0) 
#    
#    glueTabEdgeTop = backTopLeft + Point(-1*g, -1*g)
#    
#    glueTabEdgeBottom = backBottomLeft + Point(-1*g, g)
#    
#    backBottomFlapLeftTop = backBottomLeft + Point(h1, -1*l/2 )
#    
#    backBottomFlapLeftBottom = backBottomFlapLeftTop + Point(0,-1*k4)
#    
#    #backBottomFlapLeftBottomStart = backBottomFlapLeftBottom + Point(0, kr)
#    #
#    #backBottomFlapLeftBottomEnd = backBottomFlapLeftBottom + Point(kr, 0)
#    
#    
#    backBottomFlapRightTop = leftBottomLeft + Point(-1*h1, -1*l/2 )
#    
#    backBottomFlapRightBottom = backBottomFlapRightTop + Point(0,-1*k4)
#    #backBottomFlapRightBottomStart = backBottomFlapRightBottom + Point(0, kr)
#    
#    #backBottomFlapRightBottomEnd = backBottomFlapRightBottom + Point(-1*kr, 0)
#    
#    leftBottomFlapLeftBottom = leftBottomLeft + Point(0, -1*w/2 + bottomDustFlapGap)
#    
#    
#    leftBottomFlapRightBottom =  leftBottomFlapLeftBottom + Point(l/2, 0)
#    
#    #leftBottomFlapRightBottomStart = leftBottomFlapRightBottom + Point(-1*kr, 0)
#    #leftBottomFlapRightBottomEnd = leftBottomFlapRightBottom + Point(0, kr)
#    leftBottomFlapRightTop = leftBottomFlapRightBottom + Point(0, (w-h1*2)/2-bottomDustFlapGap)
#    
#    rightBottomFlapRightBottom = rightBottomRight + Point(0, -1*w/2 + bottomDustFlapGap)
#    
#    rightBottomFlapLeftBottom = rightBottomFlapRightBottom + Point(-1*l/2, 0)
#    
#    rightBottomFlapLeftTop = rightBottomFlapLeftBottom + Point(0, (w-h1*2)/2-bottomDustFlapGap)
#    
#    frontBottomFlapLeftBottom = frontBottomLeft + Point(0,-1*(l/2+k4))
#    frontBottomFlapLeftBottomRight = frontBottomFlapLeftBottom + Point(h1, 0)
#    frontBottomFlapLeftBottomRightTop = frontBottomFlapLeftBottomRight + Point(0,k4)
#    
#    
#    frontBottomFlapRightBottom = frontBottomRight + Point(0,-1*(l/2+k4))
#    frontBottomFlapRightBottomLeft = frontBottomFlapRightBottom + Point(-1*h1, 0)
#    frontBottomFlapRightBottomLeftTop = frontBottomFlapRightBottomLeft + Point(0,k4)
#    
#    leftTopFlapLeftBottom = leftTopLeft+Point(x2,0)
#    leftTopFlapLeftMid1 = leftTopFlapLeftBottom + Point(0,s2)
#    leftTopFlapLeftMid2 = leftTopFlapLeftMid1 + Point(n,n)
#    leftTopFlapLeftTop = leftTopFlapLeftBottom  + Point(t2,w/2)
#    leftTopFlapRightBottom = frontTopLeft+Point(-1*x3,0)
#    leftTopFlapRightTop = leftTopFlapRightBottom + Point(0,w/2)
#    
#    rightTopFlapRightBottom = rightTopRight+Point(-1*x2,0)
#    rightTopFlapRightMid1 = rightTopFlapRightBottom + Point(0,s2)
#    rightTopFlapRightMid2 = rightTopFlapRightMid1 + Point(-1*n,n)
#    rightTopFlapRightTop = rightTopFlapRightBottom  + Point(-1*t2,w/2)
#    rightTopFlapLeftBottom = frontTopRight+Point(x3,0)
#    rightTopFlapLeftTop = rightTopFlapLeftBottom + Point(0,w/2)
#     
#    frontTopFlapLeftEdge = frontTopLeft + Point(0,l+overhangTabCloser)
#    frontTopFlapRightEdge = frontTopRight + Point(0,l+overhangTabCloser)
#    
#    frontTopFlapLeftEdgeIn = frontTopFlapLeftEdge + Point(e,0)
#    frontTopFlapRightEdgeIn = frontTopFlapRightEdge + Point(-1*e,0)
#    
#    frontTopFlapLeftEdgeInDown = frontTopFlapLeftEdgeIn + Point(0, -2*overhangTabCloser)
#    frontTopFlapRightEdgeInDown = frontTopFlapRightEdgeIn + Point(0, -2*overhangTabCloser)
#    
#    frontTopFlapLeftEdgeInFold = frontTopFlapLeftEdgeIn + Point(0, -1*overhangTabCloser)
#    frontTopFlapRightEdgeInFold = frontTopFlapRightEdgeIn + Point(0, -1*overhangTabCloser)
#    
#    frontTopFlapLeftTabStart = frontTopFlapLeftEdge + Point(overhangTabCloser, 0)
#    frontTopFlapRightTabStart = frontTopFlapRightEdge + Point( -1*overhangTabCloser, 0)
#    
#    frontTopFlapLeftTabMid = frontTopFlapLeftTabStart + Point(0, c-cr)
#    frontTopFlapRightTabMid = frontTopFlapRightTabStart+ Point(0, c-cr)
#    
#    frontTopFlapLeftTabTop = frontTopFlapLeftTabMid + Point(cr, cr)
#    frontTopFlapRightTabTop = frontTopFlapRightTabMid + Point(-1*cr, cr)
#    
#    cutLines = etree.Element("g")
#    pathStyle =  {'style':' stroke:blue ;fill:blue; fill-opacity:0'}
#    
#    docu.append(buildPath(PathData().moveTo(frontTopLeft).lineTo(frontTopFlapLeftEdge).
#                              moveTo(frontTopRight).lineTo(frontTopFlapRightEdge).
#                              moveTo(frontTopFlapLeftEdge).lineTo(frontTopFlapLeftEdgeIn).lineTo(frontTopFlapLeftEdgeInDown).
#                              moveTo(frontTopFlapRightEdge).lineTo(frontTopFlapRightEdgeIn).lineTo(frontTopFlapRightEdgeInDown).
#                              moveTo(frontTopFlapLeftTabStart).
#                              lineTo(frontTopFlapLeftTabMid).
#                              cubicBezier(frontTopFlapLeftTabMid+Point(0,cr/2),frontTopFlapLeftTabTop+Point(cr/-2,0), frontTopFlapLeftTabTop  ).
#                              lineTo(frontTopFlapRightTabTop).cubicBezier(frontTopFlapRightTabTop+Point(cr/2,0), frontTopFlapRightTabMid+Point(0,cr), frontTopFlapRightTabMid ).
#                              lineTo(frontTopFlapRightTabStart).
#                              moveTo(frontTopRight).
#                              cubicBezier(frontTopRight-Point(0, x3),rightTopFlapLeftBottom-Point(0,x3), rightTopFlapLeftBottom ).                          
#                              lineTo(rightTopFlapLeftTop).
#                              lineTo(rightTopFlapRightTop).
#                              lineTo(rightTopFlapRightMid2).
#                              lineTo(rightTopFlapRightMid1).
#                              lineTo(rightTopFlapRightBottom).
#                              lineTo(rightTopRight).
#                              lineTo(rightBottomRight).
#                              lineTo(rightBottomFlapRightBottom).
#                              lineTo(rightBottomFlapLeftBottom).
#                              lineTo(rightBottomFlapLeftTop).
#                              lineTo(frontBottomRight).
#                              lineTo(frontBottomFlapRightBottom).
#                              lineTo(frontBottomFlapRightBottomLeft).
#                              lineTo(frontBottomFlapRightBottomLeftTop).
#                              lineTo(frontBottomFlapLeftBottomRightTop).
#                              lineTo(frontBottomFlapLeftBottomRight).
#                              lineTo(frontBottomFlapLeftBottom).
#                              lineTo(frontBottomLeft).
#                              lineTo(leftBottomFlapRightTop).
#                              lineTo(leftBottomFlapRightBottom).
#                              lineTo(leftBottomFlapLeftBottom).
#                              lineTo(leftBottomLeft).
#                              lineTo(backBottomFlapRightTop).
#                              lineTo(backBottomFlapRightBottom).
#                              lineTo(backBottomFlapLeftBottom).
#                              lineTo(backBottomFlapLeftTop).
#                              lineTo(backBottomLeft).
#                              lineTo(glueTabEdgeBottom).
#                              lineTo(glueTabEdgeTop).
#                              lineTo(backTopLeft).
#                              lineTo(leftTopLeft).
#                              lineTo( leftTopFlapLeftBottom).
#                              lineTo(leftTopFlapLeftMid1).
#                              lineTo(leftTopFlapLeftMid2).
#                              lineTo(leftTopFlapLeftTop).
#                              lineTo(leftTopFlapRightTop).
#                              lineTo(leftTopFlapRightBottom).
#                              cubicBezier(leftTopFlapRightBottom-Point(0,x3), frontTopLeft-Point(0,x3), frontTopLeft)
#                              
#                              ,pathStyle ))
#    
#    
#
#    
#    
#    scoreLines = etree.Element("g")
#    pathStyle =  {'style':' stroke:red ;fill:red; fill-opacity:0'}
#    
#    scoreLines.append(buildPath(PathData().moveTo(rightTopFlapLeftBottom).lineTo(rightTopFlapRightBottom),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(rightBottomRight),pathStyle ))
#    
#    scoreLines.append(buildPath(PathData().moveTo(frontTopFlapLeftEdgeInFold).lineTo(frontTopFlapRightEdgeInFold),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(frontTopLeft).lineTo(frontTopRight),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(frontBottomLeft),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(frontBottomRight).lineTo(frontBottomLeft),pathStyle ))
#    
#    scoreLines.append(buildPath(PathData().moveTo(leftTopFlapLeftBottom).lineTo(leftTopFlapRightBottom),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(frontBottomLeft).lineTo(leftBottomLeft),pathStyle ))
#    
#    scoreLines.append(buildPath(PathData().moveTo(leftBottomLeft).lineTo(backBottomLeft),pathStyle ))
#    
#    
#    scoreLines.append(buildPath(PathData().moveTo(backBottomLeft).lineTo(backTopLeft),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(leftTopLeft).lineTo(leftBottomLeft),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(frontBottomLeft).lineTo(frontTopLeft),pathStyle ))
#    scoreLines.append(buildPath(PathData().moveTo(frontTopRight).lineTo(frontBottomRight),pathStyle ))
#    docu.append(scoreLines)
#
##
##l = inchesToPx(6+55.0/64)
##w = l
##h = l
##g = inchesToPx(.5) # pm: g
##h1 = inchesToPx(2)   #pm: h1
##k4 = inchesToPx(1.5)   #pm:k4
##kr = inchesToPx(1.0/16) #pm: kr*
##bottomDustFlapGap = inchesToPx(.25)
##
##x2 = inchesToPx(1.0/16)
##x3 = inchesToPx(1.0/8)
##s2 = inchesToPx(1) #s2
##n =  inchesToPx(1.0/4)
##t2 = inchesToPx(1)
##tabCrack = inchesToPx(1.0/16)
##e = inchesToPx(7.0/16)
##overhangTabCloser = inchesToPx(1.0/32)
##cr = inchesToPx(.5)
##c = inchesToPx(29.0/32)    
##
##docu = document.Document()
##drawBox(docu, l, w, h, g, h1, k4, kr, bottomDustFlapGap, 
##            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c)
##
##docu.writeSVG("box_sd.svg" )


#l =  inchesToPx(6+55.0/64+16.0/16)
#w = inchesToPx(6+55.0/64) 
#h = inchesToPx(6+55.0/64-10.0/16)
#g = inchesToPx(.5) # pm: g
#h1 = inchesToPx(2)   #pm: h1
#k4 = inchesToPx(1.5)   #pm:k4
#kr = inchesToPx(1.0/16) #pm: kr*
#bottomDustFlapGap = inchesToPx(.25)
#
#x2 = inchesToPx(1.0/32)
#x3 = inchesToPx(1.0/8)
#s2 = inchesToPx(1) #s2
#n =  inchesToPx(1.0/4)
#t2 = inchesToPx(1)
#tabCrack = inchesToPx(1.0/16)
#e = inchesToPx(7.0/16)
#overhangTabCloser = inchesToPx(1.0/32)
#cr = inchesToPx(.5)
#c = inchesToPx(29.0/32) 
#
#docu = document.Document()
#drawBox(docu, l, w, h, g, h1, k4, kr, bottomDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c, plotOverlaps=True, twoPart=True)
#
#
#docu.writeSVG("box_ssd_overlapd.svg" )
#
#l =  inchesToPx(6+55.0/64)
#w = inchesToPx(6+55.0/64) 
#h = inchesToPx(6+55.0/64-29.0/32)
#g = inchesToPx(.5) # pm: g
#h1 = inchesToPx(2)   #pm: h1
#k4 = inchesToPx(1.5)   #pm:k4
#kr = inchesToPx(1.0/16) #pm: kr*
#bottomDustFlapGap = inchesToPx(.25)
#
#x2 = inchesToPx(1.0/32)
#x3 = inchesToPx(1.0/8)
#s2 = inchesToPx(1) #s2
#n =  inchesToPx(1.0/4)
#t2 = inchesToPx(1)
#tabCrack = inchesToPx(1.0/16)
#e = inchesToPx(7.0/16)
#overhangTabCloser = inchesToPx(1.0/32)
#cr = inchesToPx(.5)
#c = inchesToPx(29.0/32) 
#
#docu = document.Document()
#drawBox(docu, l, w, h, g, h1, k4, kr, bottomDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c, plotTestPoints=True)
#
#docu.writeSVG("box_gsd.svg" )

#
#l =  inchesToPx(3.893)
#w = l
#h = l
#g = inchesToPx(.5) # pm: g
#h1 = inchesToPx(1)   #pm: h1
#k4 = inchesToPx(.75)   #pm:k4
#kr = inchesToPx(1.0/16) #pm: kr*
#bottomDustFlapGap = inchesToPx(.25)
#
#x2 = inchesToPx(1.0/32)
#x3 = inchesToPx(1.0/8)
#s2 = inchesToPx(1) #s2
#n =  inchesToPx(1.0/4)
#t2 = inchesToPx(1)
#tabCrack = inchesToPx(1.0/16)
#e = inchesToPx(7.0/16)
#overhangTabCloser = inchesToPx(1.0/32)
#cr = inchesToPx(.5)
#c = inchesToPx(29.0/32) 
#
#docu = document.Document()
#drawBox(docu, l, w, h, g, h1, k4, kr, bottomDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c)
#
#docu.writeSVG("box_st_conn.svg" )

#l =  inchesToPx(6+55.0/64+16.0/16)
#w = inchesToPx(6+55.0/64) 
#h = inchesToPx(6+55.0/64-10.0/16)
#g = inchesToPx(.5) # pm: g
#h1 = inchesToPx(2)   #pm: h1
#k4 = inchesToPx(.75)   #pm:k4
#kr = inchesToPx(1.0/16) #pm: kr*
#bottomDustFlapGap = inchesToPx(.25)
#topDustFlapGap = inchesToPx(1.25+3.0/8)
#
#x2 = inchesToPx(1.0/32)
#x3 = inchesToPx(1.0/8)
#s2 = inchesToPx(.5) #s2
#n =  inchesToPx(1.0/4)
#t2 = inchesToPx(1)
#tabCrack = inchesToPx(1.0/16)
#e = inchesToPx(7.0/16)
#overhangTabCloser = inchesToPx(1.0/32)
#cr = inchesToPx(.5)
#c = inchesToPx(29.0/32) 
#
#docu = document.Document()
#initializeVariables(l, w, h, g, h1, k4, kr, bottomDustFlapGap,topDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c)
#elem = makeBox(plotOverlaps=4, twoPart=True)
#docu.append(elem[0])
#docu.append(elem[1])
#docu.writeSVG("box_ssd_overlapd_p1.svg" )
#
#docu = document.Document()
#docu.append(elem[2])
#docu.append(elem[3])
#docu.writeSVG("box_ssd_overlapd_p2.svg" )


#l =  inchesToPx(6+55.0/64)
#w = inchesToPx(6+55.0/64) 
#h = inchesToPx(6+55.0/64-29.0/32)
#g = inchesToPx(.5) # pm: g
#h1 = inchesToPx(2)   #pm: h1
#k4 = inchesToPx(.75)   #pm:k4
#kr = inchesToPx(1.0/16) #pm: kr*
#bottomDustFlapGap = inchesToPx(.25)
#topDustFlapGap = inchesToPx(1.25+3.0/8)
#
#x2 = inchesToPx(1.0/32)
#x3 = inchesToPx(1.0/8)
#s2 = inchesToPx(.5) #s2
#n =  inchesToPx(1.0/4)
#t2 = inchesToPx(1)
#tabCrack = inchesToPx(1.0/16)
#e = inchesToPx(7.0/16)
#overhangTabCloser = inchesToPx(1.0/32)
#cr = inchesToPx(.5)
#c = inchesToPx(29.0/32) 
#
#docu = document.Document()
#initializeVariables(l, w, h, g, h1, k4, kr, bottomDustFlapGap,topDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c)
#elem = makeBox(plotOverlaps=True, twoPart=True)
#docu.append(elem[0])
#docu.append(elem[1])
#docu.writeSVG("box_gsd_overlapd_p1.svg" )
#
#docu = document.Document()
#docu.append(elem[2])
#docu.append(elem[3])
#docu.writeSVG("box_gsd_overlapd_p2.svg" )
#outputFolder ="/home/cosmo/SpaceCraft Cutpaths/ProBoxes/"
#
#l =  cmToPx(9)
#w = cmToPx(11.25) 
#h = cmToPx(18)
#g = cmToPx(1.25) # pm: g
#h1 = cmToPx(2)   #pm: h1
#k4 = cmToPx(1.5)   #pm:k4
#kr = cmToPx(0.15) #pm: kr*
#bottomDustFlapGap = cmToPx(1)
#topDustFlapGap = cmToPx(2)
#
#x2 = cmToPx(0.02)
#x3 = cmToPx(.16)
#s2 = cmToPx(.5) #s2
#n =  cmToPx(0.0)
#t2 = cmToPx(2.5)
#tabCrack = cmToPx(0.0)
#e = cmToPx(1)
#overhangTabCloser = cmToPx(.01)
#cr = cmToPx(.5)
#c = cmToPx(1.25) 
#thisGridSize = 1200
#docu = document.Document(gridSize=thisGridSize)
#initializeVariables(l, w, h, g, h1, k4, kr, bottomDustFlapGap,topDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c)
#elem = makeBox(plotOverlaps=3, twoPart=True, glueTab=False)
#docu.append(elem[0])
#docu.append(elem[1])
#docu.writeSVG(outputFolder + "gromb_p1.svg", pathAbsolute=True )
#
#docu = document.Document(gridSize=thisGridSize)
#docu.append(elem[2])
#docu.append(elem[3])
#docu.writeSVG(outputFolder + "gromb_p2.svg",  pathAbsolute=True )

#outputFolder ="/home/cosmo/SpaceCraft Cutpaths/ProBoxes/"
#l =  cmToPx(13.5)
#w = cmToPx(15) 
#h = cmToPx(15.25)
#g = cmToPx(1.25)  # 
#h1 = cmToPx(4) #   
#k4 = cmToPx(2) # 
#kr = cmToPx(0.15) # 
#bottomDustFlapGap = cmToPx(1) #
#topDustFlapGap = cmToPx(2) #
#
#x2 = cmToPx(0.02)#
#x3 = cmToPx(.16)#
#s2 = cmToPx(.5) #
#n =  cmToPx(0.3) #
#t2 = cmToPx(3)
#tabCrack = cmToPx(0.0)
#e = cmToPx(1.5)
#overhangTabCloser = cmToPx(.01)
#cr = cmToPx(.5)
#c = cmToPx(2) 
#thisGridSize = 1800
#docu = document.Document(gridSize=thisGridSize)
#initializeVariables(l, w, h, g, h1, k4, kr, bottomDustFlapGap,topDustFlapGap, 
#            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c)
#elem = makeBox(plotOverlaps=3, twoPart=True, glueTab=False)
#docu.append(elem[0])
#docu.append(elem[1])
#docu.writeSVG(outputFolder + "startet_p1.svg", pathAbsolute=True )
#
#docu = document.Document(gridSize=thisGridSize)
#docu.append(elem[2])
#docu.append(elem[3])
#docu.writeSVG(outputFolder + "startet_p2.svg",  pathAbsolute=True )

#
outputFolder ="/home/cosmo/SpaceCraft Cutpaths/ProBoxes/"
l =  cmToPx(10.5)
w = cmToPx(15) 
h = cmToPx(15.25)
g = cmToPx(1.25)  # 
h1 = cmToPx(4) #   
k4 = cmToPx(2) # 
kr = cmToPx(0.15) # 
bottomDustFlapGap = cmToPx(1) #
topDustFlapGap = cmToPx(2) #

x2 = cmToPx(0.02)#
x3 = cmToPx(.16)#
s2 = cmToPx(.5) #
n =  cmToPx(0.3) #
t2 = cmToPx(3)
tabCrack = cmToPx(0.0)
e = cmToPx(1.5)
overhangTabCloser = cmToPx(.01)
cr = cmToPx(.5)
c = cmToPx(2) 
thisGridSize = 1800
docu = document.Document(gridSize=thisGridSize)
initializeVariables(l, w, h, g, h1, k4, kr, bottomDustFlapGap,topDustFlapGap, 
            x2, x3, s2, n, t2, tabCrack, e, overhangTabCloser, cr, c)
makeBox(plotOverlaps=3, twoPart=False, glueTab=False)


docu.writeSVG(outputFolder + "earthgrid_full.svg", pathAbsolute=True )

#
#docu.append(elem[0])
#docu.append(elem[1])
#docu.writeSVG(outputFolder + "earthgrid_p1.svg", pathAbsolute=True )
#
#docu = document.Document(gridSize=thisGridSize)
#docu.append(elem[2])
#docu.append(elem[3])
#docu.writeSVG(outputFolder + "startet_p2.svg",  pathAbsolute=True )




print "done"
#TODO: remove tabCrack
#TODO: transform variable list into dictionary passing