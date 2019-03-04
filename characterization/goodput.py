import subprocess
import threading
import time
import os
from multiprocessing.pool import ThreadPool
from setupServers import createSSHClient

baseCommand = ["java -jar cpen431_closedloop_2019_v1.jar ", "serverlist.txt" ," single 32 60"]
outputLock = threading.Lock()

def genGoodput():
    testCommand = "java -jar a3_basic_tests_2019_v1.jar basic.txt"

    subprocess.run(testCommand, stdout=subprocess.PIPE, shell=True)

    logFile = open("A3.log", "r")

    for line in logFile:
        print(line)

        
def runTests(servers, outputFileName, port):
    if os.path.isfile('./' + outputFileName):
        os.remove(outputFileName)

    nodeFile = open(servers, "r")
    allServers = []
	
    allLines = nodeFile.read().splitlines()
    
    nodeFile.close()
	
    for line in allLines:
        hostname = line
        allServers.append([hostname, port])
	
    totalNum = len(allServers)
    count = 0
    
    threads = []
    for server in allServers:
        t = threading.Thread(target=runOneTest, args=[server, outputFileName])
        threads.append(t)
        
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
        
    print('all threads done')
        

        
def runOneTest(server, outputFileName):
    hostname = server[0]
    port = server[1]
    
    filename = 'evalServer' + hostname + '_' + port + '.txt'
    
    serverFile = open(filename, 'w+')
    serverFile.write(hostname + ":" + port)
    serverFile.close()

    command = baseCommand[0] + filename + baseCommand[2]
    
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(checkMemCpu, (server, 5, 60))

     # get the return value from your function.
    t = threading.Thread(target=checkMemCpu, args=[server, 5, 60])
    t.start()
    
    # Set up the echo command and direct the output to a pipe
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        goodput = '0'
        
        # Run the command
        output, error = p.communicate()
        
        for line in output.decode().split('\r\n'):
            parsedLine = line.split(' ')
            if len(parsedLine) > 0 and 'Goodput:' == parsedLine[0]:
                goodput = parsedLine[1]
    except:
        print('Error occurred when attempting to test ' + hostname)
    else:
        cpu, mem = async_result.get()
        
        outputLock.acquire()
        
        try:
            outputFile = open(outputFileName, 'a')
            outputFile.write(hostname + ':' + goodput + ':' + cpu[0] + ':' + cpu[1] + ':' + cpu[2] + ':' + mem[0] + ':' + mem[1] + ':' + mem[2] + '\n')
            outputFile.close()
        except:
            print('Error writing to output file with ' + hostname)
        
        outputLock.release()

    t.join()
    os.remove(filename)
    
    
    
def checkMemCpu(server, sleepTime, numSeconds):
    usedFreeMemCommand = 'free | awk -F \' \' \'FNR == 2 {print $3"|"$4}\''
    percentCommand = 'ps aux | awk -F \' \' \'{print $2"|"$3"|"$4}\''
    
    startTime = time.time()
    
    hostname = server[0]
    port = server[1]
    
    
    percentCount = 0
    
    ## min, max, total
    cpuArr = [0, 0, 0]
    memArr = [0, 0, 0]
    
    try:
        ssh = createSSHClient(hostname)
    except:
        print('Error attempting to ssh into ' + hostname)
    else:
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo netstat -anp | grep ':" + port +"'")
            pid = 0
            for line in ssh_stdout.readlines():
                for substr in line.split(' '):
                    if('/java' in substr):
                        pid = substr[:-5]
        except:
            print('fetching pid on ' + hostname)
        else:
            while(True):
                cpu = 0
                mem = 0
                
                try:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(percentCommand)
                    ssh_stdout.channel.settimeout = 1
                    for line in ssh_stdout.readlines():
                        parsedLine = line.replace('\n', '').split('|')
                        if(parsedLine[0] == str(pid)):
                            percentCount += 1
                            cpu = float(parsedLine[1])
                            mem = float(parsedLine[2])
                except:
                    print('fetching Memry/CPU percentage on ' + hostname)
                else:
                    cpuArr[2] += cpu
                    
                    if(cpuArr[0] == 0 or cpuArr[0] > cpu):
                        cpuArr[0] = cpu
                    
                    if(cpuArr[1] == 0 or cpuArr[1] < cpu):
                        cpuArr[1] = cpu
                        
                    memArr[2] += mem
                    
                    if(memArr[0] == 0 or memArr[0] > mem):
                        memArr[0] = mem
                    
                    if(memArr[1] == 0 or memArr[1] < mem):
                        memArr[1] = mem
                
                if(time.time() - startTime > numSeconds):
                    break
                
                time.sleep(sleepTime)
            
        if(percentCount != 0):
            cpuArr[2] = (cpuArr[2]/percentCount)
            memArr[2] = (memArr[2]/percentCount)
        else:
            cpuArr[2] = 0.0
            memArr[2] = 0.0
        
        ssh.close()
    
    for i in range(3):
        cpuArr[i] = str(cpuArr[i])
        memArr[i] = str(memArr[i])
    
    return (cpuArr, memArr)
        
    
    
    
    
    
    
    
    
    

    
    

    