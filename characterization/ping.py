from ping3 import ping

def pingServers(input, output):
    serverFile = open(input, "r")
    resultFile = open(output, "w")

    for line in serverFile:
        hostname = line.split("\n")[0]
        resultFile.write(hostname + ":" + str(ping(hostname, unit="ms")) + "\n")

    serverFile.close()
    resultFile.close()