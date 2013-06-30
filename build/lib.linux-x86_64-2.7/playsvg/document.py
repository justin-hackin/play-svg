'''Document is the SVG document representation, provides file I/O and access to the DOM '''
import os
from copy import copy
from element import *
from geom import *
try:
    from lxml import etree
except:
    sys.exit('The document.py module requires lxml etree. ')

def setAttributesFromDict(element,dict):
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
    def __init__(self, file=None,  gridSize=295, alignment='mm'):
        #FIXME: test file support
        #FIXME: add support for different canvas alignments and sizes of document
        if file != None:
                print 'file import not yet supported'
        else:
            
            self.xdoc= etree.Element('{http://www.w3.org/2000/svg}svg')
            svgAttributes = {u'xmlns':'http://www.w3.org/2000/svg', u'height':unicode(gridSize*2), u'width':unicode(gridSize*2)}  
            setAttributesFromDict(self.xdoc, svgAttributes)
            self.defs = etree.SubElement(self.xdoc, 'defs')
            
            #append canvas, the co-ordinate system group
            canvasAtts = {u'id':u'canvas', u'transform':(u'matrix(1,0,0,-1,0,'+str(gridSize*2) +u') ' + u'translate('+unicode(gridSize)+ u','+ unicode(gridSize)+u')')}
            self.canvas = etree.SubElement(self.xdoc,'g')
            setAttributesFromDict(self.canvas, canvasAtts)
    
    def append(self, element):
        """appends element to canvas"""
        self.canvas.append(element)
    def makeGroup(self, id=None):
        """returns a group element"""
        groupElement = etree.Element('g')
        if id != None:
            groupElement.set('id', id)
        return groupElement
    def appendDefinition(self, definition):
        """adds element to defs"""
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
        
        file.write(etree.tostring(self.xdoc))
        file.close()


if __name__ == "__main__":
    docu = Document()
    docu.append(buildCircle(docu, Point(0,0), 100, {u'style':u'fill:black'}))
    docu.writeSVG('testdocum.svg')
    print 'done'
    

