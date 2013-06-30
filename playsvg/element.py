"""
Functions for constructing SVG elements to be added to a document
See `SVG specifications <http://www.w3.org/TR/SVG/>`_ for more information  how nodes are structured, including the optional attributes and styles.
See `lxml documentation <http://lxml.de/tutorial.html>`_ for clarification on etree usage 
"""
import io 
from copy import *
import string
import re
from geom import *
import document
try:
    from lxml import etree
except:
    sys.exit('The document.py module requires lxml etree. ')
#TODO: can the aNum and implement specialized get methods for point variables ??
#TODO: buildGroup 

#default style used for all elements except text when no elementAttrs is specified
defaultStyleAttrs = { 'style': "fill:none;stroke:black;stroke-width:1"}
#default style used for text elements when no elementAttrs is specified
defaultTextStyleAttrs = { 'style': "fill:black;stroke:none;font-size:24;"}

def buildCircle(point,radius, elementAttrs=defaultStyleAttrs):
    """create an lxml circle element centered at point with given radius and optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs[u'cx'] = unicode(point.x)
    elementAttrs[u'cy'] = unicode(point.y)
    elementAttrs[u'r'] = unicode(radius)
    circleElement = etree.Element(u'circle')
    document.setAttributesFromDict(circleElement, elementAttrs)
    return circleElement
   
def buildLine(pointA, pointB,elementAttrs=defaultStyleAttrs):
    """create an lxml line element from pointA to pointB with optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs[u'x1'] = uNum(pointA.x)
    elementAttrs[u'y1'] = uNum(pointA.y)
    elementAttrs[u'x2'] = uNum(pointB.x)
    elementAttrs[u'y2'] = uNum(pointB.y)
    lineElement = etree.Element(u'line')
    document.setAttributesFromDict(lineElement, elementAttrs)
    return lineElement
        
def buildRect(pointA, height, width,  elementAttrs=defaultStyleAttrs):
        """create an lxml rectangle element with bottom left corner pointA, and given width/height,  with optional elementAttrs dictionary defining node attributes"""
        elementAttrs = copy(elementAttrs)
        elementAttrs['x'] = uNum(pointA.x)
        elementAttrs['y'] = uNum(pointA.y)
        elementAttrs['height'] = uNum(height)
        elementAttrs['width'] = uNum(width)
        rectElement = etree.Element(u'rect')
        document.setAttributesFromDict(rectElement, elementAttrs)
        return rectElement
        

def buildPath( pathData,  elementAttrs=defaultStyleAttrs):
    """create an lxml path using a PathData object and optional elementAttrs dictionary defining node attributes"""
    elementAttrs = copy(elementAttrs)
    elementAttrs['d'] = unicode(pathData)
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

def buildUse(id, elementAttrs={} ):
    """create a use node (for cloning) with id of node to be cloned (set in its elementAttrs).  Use elementAttrs to set transform of object."""
    elementAttrs = copy(elementAttrs)
    useElement = etree.Element('use')
    elementAttrs["{http://www.w3.org/1999/xlink}href"] = '#'+str(id)
    document.setAttributesFromDict(useElement, elementAttrs)
    return useElement
    
  
##def makeItGoRound(base, node, duration):
##    animator = base.xml_element(u'animateTransform')
##    animatorAtts[u'attributeName'] = u'transform'
##    animatorAtts[u'attributeType'] = u'XML'
##    animatorAtts[u'type'] = u'rotate'
##    animatorAtts[u'from'] = u'0'
##    animatorAtts[u'to'] = u'360'
##    animatorAtts[u'begin'] = u'0s'
##    animatorAtts[u'dur'] = unicode(duration)+u's'
##    animatorAtts[u'fill'] = u'freeze'
##   
##  

#formats number decimal places to comply with SVG
def uNum(theNum):
    return u'%.5f'% float(theNum) #another magic number :S
    
