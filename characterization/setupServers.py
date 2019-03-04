import paramiko
import threading
from scp import SCPClient
import time
import os


def setupServers(servers, port):
    nodeFile = open(servers, "r")
    allServers = []
	
    allLines = nodeFile.read().splitlines()
	
    for line in allLines:
        hostname = line
        allServers.append([hostname, port])
		
	## start single stand-alone server on each node
    threads = []
    for server in allServers:
        t = threading.Thread(target=setupOneServer, args=server)
        threads.append(t)
        
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

def createSSHClient(node, timeout=30):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=node, port=22, username='ubc_cpen431_6', timeout=timeout, look_for_keys=True)
    return client
    
def setupOneServer(hostname, port):
    ## create server file
    serverFileName = './' + hostname + '_evalServer.txt'
    serverFile = open(serverFileName, 'w+')
    serverFile.write(hostname + ":" + port)
    serverFile.close()
    
    try:
        ssh = createSSHClient(hostname)
    except:
        print('Error attempting to ssh into ' + hostname)
    else:
        ## check if already running on that port
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo netstat -anp | grep ':" + port +"'")
            for line in ssh_stdout.readlines():
                for substr in line.split(' '):
                    if('/java' in substr):
                        pid = substr[:-5]
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo kill "+ pid)
        except: 
            print('Error attempting to ensure port free on ' + hostname)
        else:
            try:
                scp = SCPClient(ssh.get_transport())
                scp.put(serverFileName, "evalServer.txt")
                scp.close()
            except:
                print('Error attempting to scp text file onto ' + hostname)
            else:
                ## start server
                try:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('jdk1.8.0_201/bin/java -Xmx64M -jar A8.jar 44 evalServer.txt 0', timeout=1)
                    ssh_stdout.channel.settimeout = 1
                except:
                    print('Error attempting to start server on ' + hostname)
                else:
                    confirmation = ssh_stdout.readline()
                    if 'Starting' not in confirmation:
                        print('Error starting server on ' + hostname)
                        print(confirmation)
                    else:
                        print(hostname + " started!")
        
        ssh.close()
        
    os.remove(serverFileName)
    