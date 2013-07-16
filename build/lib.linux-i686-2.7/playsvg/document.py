"""SVG document representation, provides file I/O and access to the DOM"""
import os
from copy import copy
from element import *
from geom import *
try:
    from lxml import etree
except:
    sys.exit('The document.py module requires lxml etree. ')

def setAttributesFromDict(element,dict):
    """uses a dictionary to populate xml attributes for a particular lxml element """
    for key, val in dict.items():
        element.set(key, val)

##def allSubnodesIteratorHelp(subnodes, node):
##    children = node.xml_children
##    for i in range(len(children)):
##        if not type(children[i]).__name__ == 'unicode' and not type(children[i]).__name__ == 'metadata' :
##            subnodes.append(children[i])
##            allSubnodesIteratorHelp(subnodes, subnodes[-1])
##    return subnodes
##def allSubnodesIterator(node):
##    subnodes = []
##    return allSubnodesIteratorHelp(subnodes, node)
    


class Document:
    """represents a single SVG document, a square of width and height gridSize"""
    def __init__(self, gridSize=1280, notCentered=False):
        
        #TODO: enable different width and height               
        NSMAP = {"xmlns" : "http://www.w3.org/2000/svg", \
                 "xlink" : 'http://www.w3.org/1999/xlink', \
                 "{http://www.w3.org/2000/svg}svg": "http://www.w3.org/2000/svg"}
        #root xml node
        self.xdoc= etree.Element('svg', NSMAP)
        svgAttributes = {'height':str(gridSize), 'width':str(gridSize)}  
        setAttributesFromDict(self.xdoc, svgAttributes)
        #definitions for use in linking
        self.defs = etree.SubElement(self.xdoc, 'defs')
        if notCentered:
            self.transformMatrix = ""
        else:
            self.transformMatrix = 'matrix(1,0,0,-1,0,'+str(gridSize) +') ' + 'translate('+str(gridSize/2)+ ','+ str(gridSize/2)+')'        
        canvasAtts = {'id':'canvas', 'transform':self.transformMatrix}
        #the co-ordinate system group
        self.canvas = etree.SubElement(self.xdoc,'g')
        setAttributesFromDict(self.canvas, canvasAtts)
    
    def append(self, element):
        """append element as lxml node to canvas"""
        self.canvas.append(element)
    def makeGroup(self, id=None):
        """returns a group element lxml node with given id
        DEPRECATED, as no longer document-dependent, use element.buildGroup()"""
        groupElement = etree.Element('g')
        if id != None:
            groupElement.set('id', id)
        return groupElement
    def appendDefinition(self, definition):
        """adds lxml node element to defs"""
        self.defs.append(definition)
    def writeSVG(self, filename, pathAbsolute=False ):
        """writes SVG document to file"""
        imagePath = ""
        file = None 
        if (not pathAbsolute):
            imagePath = os.getcwd() + "/images/"
            if not os.path.exists(imagePath):
                os.mkdir(imagePath)
            file = open((imagePath+filename),'w')
        else:
            file = open(filename,'w')  
        
        file.write(etree.tostring(self.xdoc, pretty_print=True))
        file.close()
    def __str__(self):
        """for console output in testing"""
        return etree.tostring(self.xdoc, pretty_print=True)
 
