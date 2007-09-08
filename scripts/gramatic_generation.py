import playsvg.document
import math
import permutations
from playsvg.geom import *
from playsvg.element import *


lineHeightToWidth = 1.0/8
lineSpacing = 1
singleGapWidthRatio = 1.0/5
doubleGapWidthRatio = 1.0/5
names =[["01. Force","The Creative"],["02. Field","The Receptive"],["03. Sprouting","Difficulty at the Beginning"],["04. Enveloping","Youthful Folly"],["05. Attending","Waiting"],["06. Arguing","Conflict"],["07. Leading","The Army"],["08. Grouping","Holding Together"],["09. Small Accumulating","Small Taming"],["10. Treading","Treading (Conduct)"],["11. Prevading","Peace"],["12. Obstruction","Standstill"],["13. Concording People","Fellowship"],["14. Great Possessing","Great Possession"],["15. Humbling","Modesty"],["16. Providing-For","Enthusiasm"],["17. Following","Following"],["18. Corrupting","Work on the Decayed"],["19. Nearing","Approach"],["20. Viewing","Contemplation"],["21. Gnawing Bite","Biting Through"],["22. Adorning","Grace"],["23. Stripping","Splitting Apart"],["24. Returning","Return"],["25. Without Embroiling","Innocence"],["26. Great Accumulating","Great Taming"],["27. Swallowing","Mouth Corners"],["28. Great Exceeding","Great Preponderance"],["29. Gorge","The Abysmal Water"],["30. Radiance","The Clinging"],["31. Conjoining","Influence"],["32. Persevering","Duration"],["33. Retiring ","Retreat"],["34. Great Invigorating","Great Power"],["35. Prospering","Progress"],["36. Brightness Hiding","Darkening of the Light"],["37. Dwelling People","The Family"],["38. Polarising","Opposition"],["39. Limping","Obstruction"],["40. Taking-Apart","Deliverance"],["41. Diminishing","Decrease"],["42. Augmenting","Increase"],["43. Parting","Breakthrough"],["44. Coupling","Coming to Meet"],["45. Clustering","Gathering Together"],["46. Ascending","Pushing Upward"],["47. Confining","Oppression"],["48. Welling","The Well"],["49. Skinning","Revolution"],["50. Holding","The Cauldron"],["51. Shake","Arousing"],["52. Bound","The Keeping Still"],["53. Infiltrating","Development"],["54. Converting The Maiden","The Marrying Maiden"],["55. Abounding","Abundance"],["56. Sojourning","The Wanderer"],["57. Ground","The Gentle"],["58. Open","The Joyous"],["59. Dispersing","Dispersion"],["60. Articulating","Limitation"],["61. Centre Confirming","Inner Truth"],["62. Small Exceeding","Small Preponderance"],["63. Already Fording","After Completion"],["64. Not-Yet Fording","Before Completion"]]
numChart = [[1,43,14,34,9,5,26,11],[10,58,38,54,61,60,41,19],[13,49,30,55,37,63,22,36],[25,17,21,51,42,3,27,24],[44,28,50,32,57,48,18,46],[6,47,64,40,59,29,4,7],[33,31,56,62,53,39,52,15],[12,45,35,16,20,8,23,2]]



lineAttributes = {u'fill':u'black', u'stroke':u'none'}

# convert a decimal (denary, base 10) integer to a binary string (base 2)
# tested with Python24   vegaseat    6/1/2005
# from http://www.daniweb.com/code/snippet285.html

def Denary2Binary(n):
    '''convert denary integer n to list of ints'''
    bStr = ''
    if n < 0:  raise ValueError, "must be a positive integer"
   
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    while len(bStr) < 6:
        bStr = "0" + bStr
     
    bList = []
    for i in range(len(bStr)):
        bList.append(int(bStr[i]))
    return bList

def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])



def buildTriLine(docu, value,position, width):
        lineGroup = docu.makeGroup()
        if value == 0:
            lineGroup.appendChild(buildRect(docu,Point(position.x - 0.5*width,position.y),lineHeightToWidth*width, width, lineAttributes))
        elif value == 1:
            blockWidthRatio = 0.5*(1 - singleGapWidthRatio)
            lineGroup.appendChild(buildRect(docu,Point(position.x - 0.5*width,position.y),lineHeightToWidth*width, blockWidthRatio*width, lineAttributes))
            lineGroup.appendChild(buildRect(docu,Point(position.x + 0.5*singleGapWidthRatio*width,position.y),lineHeightToWidth*width,  blockWidthRatio*width,  lineAttributes))
        elif value == 2:
            blockWidthRatio = 1.0/3*(1.0 - 2*doubleGapWidthRatio)
            lineGroup.appendChild(buildRect(docu,Point(position.x - 0.5*width,position.y),lineHeightToWidth*width, blockWidthRatio*width, lineAttributes))
            lineGroup.appendChild(buildRect(docu,Point(position.x - 0.5*width+ blockWidthRatio*width +doubleGapWidthRatio*width,position.y),lineHeightToWidth*width,  blockWidthRatio*width, lineAttributes))
            lineGroup.appendChild(buildRect(docu,Point(position.x -0.5*width + 2*blockWidthRatio*width +2*doubleGapWidthRatio*width,position.y),lineHeightToWidth*width,  blockWidthRatio*width, lineAttributes))
            
        return lineGroup
    


def buildTieredGram(docu, valuePair, position, width):
    gramGroup = docu.makeGroup()
    currentPosition = position
    for i in range(len(valuePair)):
        gramGroup.appendChild(buildTriLine(docu, valuePair[i], currentPosition, width))
        currentPosition = currentPosition + Point(0, lineHeightToWidth*width*(1+lineSpacing))
    return gramGroup
    
    print

def digramCentred(docu,value, centrePoint, width):
    gramGroup = docu.makeGroup()
    bottomLine = (value-1) % 3 
    topLine = ((value-1) - ((value-1)%3))/3
    gramGroup.appendChild(buildTriLine(docu, topLine, centrePoint + Point(0,0.5*lineHeightToWidth*width*lineSpacing), width))
    gramGroup.appendChild(buildTriLine(docu, bottomLine, centrePoint - Point(0,0.5*lineHeightToWidth*width*lineSpacing+lineHeightToWidth*width), width))
    return gramGroup

def makeTHCBigrams():
    
    for p in permutations.xselections((0,1,2), 2):
        docu = document.Document()
        docu.appendElement(buildTieredGram(docu,p, Point(), 64))
        docu.writeSVG('THC-bigrams/THC_bigram-'+str(p[1])+str(p[0])+'.svg')

def makeTHCTrigrams():
    
    for p in permutations.xselections((0,1,2), 3):
        docu = document.Document()
        docu.appendElement(buildTieredGram(docu,p, Point(), 64))
        docu.writeSVG('THC-trigrams/THC_trigram-'+str(p[2])+str(p[1])+str(p[0])+'.svg')

def makeTHCQuadgrams():
    
    for p in permutations.xselections((0,1,2), 4):
        docu = document.Document()
        docu.appendElement(buildTieredGram(docu,p, Point(), 64))
        docu.writeSVG('THC-quadgrams/THC_quadgram-'+str(p[3])+str(p[2])+str(p[1])+str(p[0])+'.svg')

def makeTHCHexagrams():
    
    for p in permutations.xselections((0,1,2), 6):
        docu = document.Document()
        docu.appendElement(buildTieredGram(docu,p, Point(), 64))
        docu.writeSVG('THC-hexagrams/THC_hexagram-'+str(p[5])+str(p[4])+str(p[3])+str(p[2])+str(p[1])+str(p[0])+'.svg')

def makeDescendingHeavenGrid():
    docu = document.Document()
    vertSpacing = 30
    horizSpacing = 60
    hexWidth = 50
    gridGroup = docu.makeGroup()    
    textGroup = docu.makeGroup()
    inverseBinaryConversion = {0:0, 1:4, 2:2, 3:6, 4:1,5:5, 6:3,7:7}
    for i in range(64):
        columnNum = (i%8) 
        rowNum = int(math.floor(float(i)/8))
        xPos = columnNum*(horizSpacing+hexWidth)
        yPos = -1*rowNum*(vertSpacing+hexWidth*(lineHeightToWidth*6*(1+lineSpacing)))
        textIndex = numChart[inverseBinaryConversion[columnNum]][inverseBinaryConversion[7-rowNum]]
        digList = Denary2Binary(i)
        digList.reverse()
        hexagram = buildTieredGram(docu, digList, Point(xPos, yPos), hexWidth)
        fontHeight = 8
        nameText = buildText(docu, names[textIndex-1][0], {'x':str(xPos-0.5*hexWidth), 'y':str( yPos), 'style':'fill: black; font-size:' + str(fontHeight) + 'px'})
        nameText2 = buildText(docu, names[textIndex-1][1], {'x':str(xPos-0.5*hexWidth), 'y':str(yPos+fontHeight+4), 'style':'fill: black; font-size:' + str(fontHeight) + 'px'})
        textGroup.appendChild(nameText)
        textGroup.appendChild(nameText2)
        gridGroup.appendChild(hexagram)
        
    docu.appendElement(gridGroup)
    docu.appendElement(textGroup)
    docu.writeSVG("hexagram_grid_dh.svg")

def makeAscendingEarthGrid():
    docu = document.Document()
    vertSpacing = 30
    horizSpacing = 60
    hexWidth = 50
    gridGroup = docu.makeGroup()    
    textGroup = docu.makeGroup()
    
    for i in range(63, -1, -1):
        columnNum = (i%8) 
        rowNum = int(math.floor(float(i)/8))
        xPos = -1*columnNum*(horizSpacing+hexWidth)
        yPos = rowNum*(vertSpacing+hexWidth*(lineHeightToWidth*6*(1+lineSpacing)))
        textIndex = numChart[7-rowNum][columnNum]
        digList = Denary2Binary(i)
        hexagram = buildTieredGram(docu, digList, Point(xPos, yPos), hexWidth)
        fontHeight = 8
        nameText = buildText(docu, names[textIndex-1][0], {'x':str(xPos-0.5*hexWidth), 'y':str( yPos), 'style':'fill: black; font-size:' + str(fontHeight) + 'px'})
        nameText2 = buildText(docu, names[textIndex-1][1], {'x':str(xPos-0.5*hexWidth), 'y':str(yPos+fontHeight+4), 'style':'fill: black; font-size:' + str(fontHeight) + 'px'})
        textGroup.appendChild(nameText)
        textGroup.appendChild(nameText2)
        gridGroup.appendChild(hexagram)
        
    docu.appendElement(gridGroup)
    docu.appendElement(textGroup)
    docu.writeSVG("hexagram_grid_ae.svg")    
    
if   __name__ == '__main__':
    #makeTHCBigrams()
    makeTHCTrigrams()
    #makeTHCQuadgrams()
    #makeTHCHexagrams()
    #makeDescendingHeavenGrid()
    #makeAscendingEarthGrid()
##    
##    docu = document.Document()
####    docu.appendElement(buildDigramLine(docu, 2 ,Point(0,0), 40) )
##    
##    docu.appendElement(buildTieredGram(docu, (0,2,1,1,0) ,Point(0,0), 64) )
##    
    
##    docu.writeSVG('trigramTest.svg')

    
    
    
    
