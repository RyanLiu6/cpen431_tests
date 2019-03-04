from ping3 import ping

def compileResults(xFileName, yFileName, resultFileName):
    xFile = open(xFileName, "r")
    yFile = open(yFileName, "r")
    resultFile = open(resultFileName, "w")

    hostmap = {}
    for line in xFile:
        parsedLine = line.replace('\n', '').split(':')
        key = parsedLine[0]
        xVal = parsedLine[1]
        
        hostmap[key] = xVal

    for line in yFile:
        parsedLine = line.replace('\n', '').split(':', 1)
        
        key = parsedLine[0]
        yVal = parsedLine[1].replace(':', ' ')
        
        resultFile.write(key + ' ' + hostmap[key] + ' ' + yVal + '\n')
        
    xFile.close()
    yFile.close()
    resultFile.close()
