'''Base is the SVG document representation, provides file I/O and access to the DOM '''
from copy import deepcopy
from amara import binderytools
import os

def allSubnodesIteratorHelp(subnodes, node):
    children = node.xml_children
    for i in range(len(children)):
        if not type(children[i]).__name__ == 'unicode' and not type(children[i]).__name__ == 'metadata' :
            subnodes.append(children[i])
            allSubnodesIteratorHelp(subnodes, subnodes[-1])
    return subnodes
def allSubnodesIterator(node):
    subnodes = []
    return allSubnodesIteratorHelp(subnodes, node)

class Base:
    def __init__(self, gridSize=295):
        '''returns a base for the API in the form of an amara doc with attached canvas (page-centred square co-ordinate system)'''
        #FIXME: documents/canvases with different size and co-ordinate configurations
        self.dok = binderytools.create_document()
        svgAttributes = {u'xmlns':u'http://www.w3.org/2000/svg',u'xmlns:svg':u'http://www.w3.org/2000/svg',u'height':unicode(gridSize*2), u'width':unicode(gridSize*2)}  
        
        svgNode = self.dok.xml_element(u"svg", attributes = svgAttributes)
        self.dok.xml_append(svgNode)
        
        #append definitions node
        defs = self.dok.xml_element(u'defs')
        self.defs = defs
        svgNode.xml_append(defs)
        
        #append canvas, the co-ordinate system group
        canvasAtts = {u'id':u'canvas', u'transform':(u'matrix(1,0,0,-1,0,'+str(gridSize*2) +u') ' + u'translate('+unicode(gridSize)+ u','+ unicode(gridSize)+u')')}
        canvas = self.dok.xml_element(u'g', attributes = canvasAtts)
        self.canvas = canvas
        svgNode.xml_append(canvas)
    def appendElement(self, node):
        self.canvas.xml_append(node)
    def makeGroup(self):
        return self.dok.xml_element(u'g')
    def appendDefinition(self, definition):
        self.defs.xml_append(definition)
    def writeSVG(self, filename ="default.svg"):
        imagePath = os.getcwd() + "/images/"
        if not os.path.exists(imagePath):
            os.mkdir(imagePath)  
        file = open((imagePath+filename),'w')
        file.write(self.dok.xml(indent=u"yes"))
        file.close()
    #FIXME: will not read SVG file into the DOM
    def readSVG(self, filename):
        self.dok = binderytools.bind_file(filename)
    def searchByID(self,idval):
        allnodes = []
        allSubnodesIteratorHelp(allnodes, self.dok.svg)
        print allnodes
        for i in range(len(allnodes)):
            
            if hasattr(allnodes[i],'xml_attributes'):
                print allnodes[i].xml_attributes['id']
                if allnodes[i].xml_attributes[u'id']== idval:
                    return allnodes[i]
    
    
    
      

