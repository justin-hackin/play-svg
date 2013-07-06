from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *


def buildConcentricCirclePacking(circles, radius, packingRatio, passive=False):
    circleGroup = etree.Element('g', id='circlePacking')
    plotPoints = createRadialPlots(Point(), radius, circles, passive)
    circleRadius = distanceBetween(plotPoints[0], plotPoints[1]) / 2 * packingRatio
    for point in plotPoints:
        circleGroup.append(buildCircle(point, circleRadius))
    return circleGroup

docu = Document()
docu.append(buildConcentricCirclePacking( ) )