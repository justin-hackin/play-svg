import io

def convertFileToArrayText(fileName, length):
    inFile = open(fileName+".csv", 'r')
    outFile = open(fileName+ "00.csv", 'w')
    outFile.write("[")
    for i in range(length):
        line = inFile.readline()[0:-1]
        print line
        outFile.write("[" + str(line) + "]")
        if inFile: outFile.write(",")
    outFile.write("]")
    inFile.close()
    outFile.close()
convertFileToArrayText("hexagram_names", 64)
convertFileToArrayText("hexagram_names_nc", 64)
convertFileToArrayText("hex_num_table_fuhsui", 8)

