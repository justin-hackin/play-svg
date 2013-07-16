"""
Functions for constructing SVG elements to be added to a document
See `SVG specifications <http://www.w3.org/TR/SVG/>`_ for more information  how nodes are structured, including the optional attributes and styles.
See `lxml documentation <http://lxml.de/tutorial.html>`_ for clarification on etree usage 

The element module is transitionally implementing the use of sympy.geometry.Point instead of geom.Point for greater functionality.  For sympy use, use makeXXX instead of buildXXX.
"""
import io 
from copy import *
import string
import re
from geom import *
from path import PathData
import document
try:
    from lxml import etree
except:
    sys.exit('The document.py module requires lxml etree. ')

#default style used for all elements except text when no elementAttrs is specified
defaultStyleAttrs = { 'style': "fill:none;stroke:black;stroke-width:1"}
#default style used for text elements when no elementAttrs is specified
defaultTextStyleAttrs = { 'style': "fill:black;stroke:none;font-size:24;"}

def buildGroup(id=None):
    """returns a group element lxml node with given id
    DEPRECATED, as no longer document-dependent, use element.buildGroup()"""
    groupElement = etree.Element('g')
    if id != None:
        groupElement.set('id', id)
    return groupElement

def buildCircle(point,radius, elementAttrs=defaultStyleAttrs):
    """create an lxml circle element centered at point with given radius and optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs['cx'] = aNum(point.x)
    elementAttrs['cy'] = aNum(point.y)
    elementAttrs['r'] = aNum(radius)
    circleElement = etree.Element('circle')
    document.setAttributesFromDict(circleElement, elementAttrs)
    return circleElement

def makeCircle(circle, elementAttrs=defaultStyleAttrs):
    """FOR SYMPY: create an lxml circle element from sympy Circle with optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs['cx'] = aNum(circle.center.x)
    elementAttrs['cy'] = aNum(circle.center.y)
    elementAttrs['r'] = aNum(circle.radius)
    circleElement = etree.Element('circle')
    document.setAttributesFromDict(circleElement, elementAttrs)
    return circleElement
   
def buildLine(pointA, pointB,elementAttrs=defaultStyleAttrs):
    """create an lxml line element from pointA to pointB with optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs['x1'] = aNum(pointA.x)
    elementAttrs['y1'] = aNum(pointA.y)
    elementAttrs['x2'] = aNum(pointB.x)
    elementAttrs['y2'] = aNum(pointB.y)
    lineElement = etree.Element('line')
    document.setAttributesFromDict(lineElement, elementAttrs)
    return lineElement

def makeLine(line,elementAttrs=defaultStyleAttrs):
    """FOR SYMPY: create an lxml line element from sympy Line with optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs['x1'] = aNum(line.p1.x)
    elementAttrs['y1'] = aNum(line.p1.y)
    elementAttrs['x2'] = aNum(line.p2.x)
    elementAttrs['y2'] = aNum(line.p2.y)
    lineElement = etree.Element('line')
    document.setAttributesFromDict(lineElement, elementAttrs)
    return lineElement
        
def buildRect(pointA, height, width,  elementAttrs=defaultStyleAttrs):
        """create an lxml rectangle element with bottom left corner pointA, and given width/height,  with optional elementAttrs dictionary defining node attributes"""
        elementAttrs = copy(elementAttrs)
        elementAttrs['x'] = aNum(pointA.x)
        elementAttrs['y'] = aNum(pointA.y)
        elementAttrs['height'] = aNum(height)
        elementAttrs['width'] = aNum(width)
        rectElement = etree.Element('rect')
        document.setAttributesFromDict(rectElement, elementAttrs)
        return rectElement
        

def buildPath( pathData,  elementAttrs=defaultStyleAttrs):
    """create an lxml path using a PathData object and optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs['d'] = str(pathData)
    pathElement = etree.Element('path')
    document.setAttributesFromDict(pathElement, elementAttrs)
    return pathElement

def makePath( pathData,  elementAttrs=defaultStyleAttrs):
    """FOR SYMPY: create an lxml path using a PathData object initialized using sympy Point objects and optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs['d'] = pathData.getD()
    pathElement = etree.Element('path')
    document.setAttributesFromDict(pathElement, elementAttrs)
    return pathElement


def buildText( text, elementAttrs=defaultTextStyleAttrs):
    """create a text node with given text and optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    textElement = etree.Element('text')
    document.setAttributesFromDict(textElement, elementAttrs)
    textElement.text = text
    return textElement

def makeText( text, position, elementAttrs=defaultTextStyleAttrs):
    """create a text node with given text and optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    textElement = etree.Element('text')
    elementAttrs['x'] = aNum(position.x)
    elementAttrs['y'] = aNum(position.y)
    elementAttrs['transform'] = "translate(" + aNum(position.x ) + ", " + aNum(position.y) + ") scale(1,-1) translate(" + aNum(-1*position.x) + "," + aNum(-1*position.y)  + ")"
    textElement.text = text
    document.setAttributesFromDict(textElement, elementAttrs)
    return textElement

def buildUse(id, elementAttrs={} ):
    """create a use node (for cloning) with id of node to be cloned (set in its elementAttrs).  Use elementAttrs to set transform of object."""
    elementAttrs = copy(elementAttrs)
    useElement = etree.Element('use')
    elementAttrs["{http://www.w3.org/1999/xlink}href"] = '#'+str(id)
    document.setAttributesFromDict(useElement, elementAttrs)
    return useElement
    
def makeTriangle(triangle, elementAttrs=defaultStyleAttrs):
    verts = triangle.vertices
    triPath = PathData().moveTo(verts[0]).lineTo(verts[1]).lineTo(verts[2]).closePath()
    return makePath(triPath, elementAttrs)

    
  
##def makeItGoRound(base, node, duration):
##    animator = base.xml_element('animateTransform')
##    animatorAtts['attributeName'] = 'transform'
##    animatorAtts['attributeType'] = 'XML'
##    animatorAtts['type'] = 'rotate'
##    animatorAtts['from'] = '0'
##    animatorAtts['to'] = '360'
##    animatorAtts['begin'] = '0s'
##    animatorAtts['dur'] = aNum(duration)+'s'
##    animatorAtts['fill'] = 'freeze'
##   
##  

#formats number decimal places to comply with SVG
def aNum(theNum):
    return '%.5f'% float(theNum) #another magic number :S
