'''functions for constructing SVG elements '''

from copy import *
import string
import re
from geom import *
import document
try:
    from lxml import etree
except:
    sys.exit('The document.py module requires lxml etree. ')


styleDefs = {}    
styleDefs[u'default'] = {u'fill' :u'none',u'stroke':u'black',u'stroke-width':u'1'}

def buildCircle(point,radius, elementAttrs ):
    elementAttrs = copy(elementAttrs)
    elementAttrs[u'cx'] = unicode(point.x)
    elementAttrs[u'cy'] = unicode(point.y)
    elementAttrs[u'r'] = unicode(radius)
    circleElement = etree.Element(u'circle')
    document.setAttributesFromDict(circleElement, elementAttrs)
    return circleElement
   
def buildLine(pointA, pointB,elementAttrs):
    elementAttrs = copy(elementAttrs)
    elementAttrs[u'x1'] = uNum(pointA.x)
    elementAttrs[u'y1'] = uNum(pointA.y)
    elementAttrs[u'x2'] = uNum(pointB.x)
    elementAttrs[u'y2'] = uNum(pointB.y)
    lineElement = etree.Element(u'line')
    document.setAttributesFromDict(lineElement, elementAttrs)
    return lineElement
        
def buildRect(pointA, height, width,  elementAttrs):
        elementAttrs = copy(elementAttrs)
        elementAttrs[u'x'] = uNum(pointA.x)
        elementAttrs[u'y'] = uNum(pointA.y)
        elementAttrs[u'height'] = uNum(height)
        elementAttrs[u'width'] = uNum(width)
        rectElement = etree.Element(u'rect')
        document.setAttributesFromDict(rectElement, elementAttrs)
        return rectElement
        

def buildPath( pathData,  elementAttrs):
    elementAttrs = copy(elementAttrs)
    elementAttrs[u'd'] = unicode(pathData)
    pathElement = etree.Element(u'path')
    document.setAttributesFromDict(pathElement, elementAttrs)
    return pathElement

def buildText( text, elementAttrs):
    elementAttrs = copy(elementAttrs)
    textElement = etree.Element(u'text')
    document.setAttributesFromDict(textElement, elementAttrs)
    textElement.text = text
    return textElement
  
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
    return u'%.5f'% float(theNum)
    
