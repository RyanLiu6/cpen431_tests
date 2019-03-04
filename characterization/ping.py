from ping3 import ping
import subprocess

def pingServers(input, output):

    command = ["ping -c 4 ", "www.stackoverflow.com", " | tail -1| awk '{print $4}' | cut -d '/' -f 2"]
    serverFile = open(input, "r")
    resultFile = open(output, "w")

    for line in serverFile:
        hostname = line.split("\n")[0]
        latency = ""
        try:
            latency = str(ping(hostname, unit="ms"))
        except: 
            try:
                toRun = command[0] + hostname + command[2]
                p = subprocess.Popen(toRun, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, error = p.communicate()
                latency = output.decode().split('\r\n')[0].replace('\n', '')
            except:
                print("Unable to ping " + hostname)

        resultFile.write(hostname + ":" + latency + "\n")
    
    serverFile.close()
    resultFile.close()